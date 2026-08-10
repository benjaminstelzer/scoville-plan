#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath


DECISION_ID_RE = re.compile(r"ADR-[0-9]{4}\Z")
DECISION_PATH_RE = re.compile(
    r"docs/decisions/([0-9]{4})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md\Z"
)
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class CliError(Exception):
    pass


@dataclass(frozen=True)
class Transition:
    decision_id: str
    action: str
    relative_path: PurePosixPath


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute read-only Scoville Plan Decision-batch metadata."
    )
    parser.add_argument("--root", required=True, help="Project root containing the Decision files.")
    parser.add_argument("--date", required=True, help="Authorized transition date in YYYY-MM-DD form.")
    parser.add_argument(
        "--transition",
        action="append",
        required=True,
        help="Ordered ADR-NNNN:accept|reject:relative/path.md transition; repeat for each member.",
    )
    parser.add_argument("--format", choices=("json",), required=True)
    return parser


def parse_date(value: str) -> str:
    if not DATE_RE.fullmatch(value):
        raise CliError("date must be an actual ISO YYYY-MM-DD value")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise CliError("date must be an actual ISO YYYY-MM-DD value") from error
    if parsed.isoformat() != value:
        raise CliError("date must be an actual ISO YYYY-MM-DD value")
    return value


def parse_transition(value: str) -> Transition:
    parts = value.split(":", 2)
    if len(parts) != 3:
        raise CliError("transition must use ADR-NNNN:accept|reject:relative/path.md")
    decision_id, action, raw_path = parts
    if not DECISION_ID_RE.fullmatch(decision_id):
        raise CliError("transition Decision ID must match ADR-NNNN")
    if action not in {"accept", "reject"}:
        raise CliError(f"transition action for {decision_id} must be accept or reject")
    if not raw_path or "\\" in raw_path or ":" in raw_path:
        raise CliError(
            f"transition path for {decision_id} must be a normalized repository-relative forward-slash path"
        )
    relative_path = PurePosixPath(raw_path)
    if (
        relative_path.is_absolute()
        or relative_path.as_posix() != raw_path
        or any(part in {"", ".", ".."} for part in relative_path.parts)
        or relative_path.suffix != ".md"
    ):
        raise CliError(
            f"transition path for {decision_id} must be a normalized repository-relative forward-slash path"
        )
    path_match = DECISION_PATH_RE.fullmatch(raw_path)
    if path_match is None:
        raise CliError(
            f"transition path for {decision_id} must match docs/decisions/NNNN-kebab-subject.md"
        )
    if path_match.group(1) != decision_id.removeprefix("ADR-"):
        raise CliError(
            f"transition filename number for {decision_id} must match the Decision ID"
        )
    return Transition(decision_id, action, relative_path)


def is_redirect(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & REPARSE_POINT)


def snapshot(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def resolve_root(value: str) -> Path:
    raw = Path(os.path.abspath(os.path.expanduser(value)))
    try:
        info = os.lstat(raw)
    except FileNotFoundError as error:
        raise CliError("root must be an existing directory") from error
    except OSError as error:
        raise CliError(f"root could not be inspected ({type(error).__name__})") from error
    if is_redirect(info) or not stat.S_ISDIR(info.st_mode):
        raise CliError("root must be a regular non-symlink directory")
    return raw.resolve(strict=True)


def hash_member(root: Path, transition: Transition) -> str:
    candidate = root.joinpath(*transition.relative_path.parts)
    current = root
    info: os.stat_result | None = None
    for part in transition.relative_path.parts:
        current /= part
        try:
            info = os.lstat(current)
        except FileNotFoundError as error:
            raise CliError(f"transition file for {transition.decision_id} does not exist") from error
        except OSError as error:
            raise CliError(
                f"transition file for {transition.decision_id} could not be inspected ({type(error).__name__})"
            ) from error
        if is_redirect(info):
            raise CliError(
                f"transition file for {transition.decision_id} must not traverse a symlink or reparse point"
            )
    assert info is not None
    if not stat.S_ISREG(info.st_mode):
        raise CliError(f"transition file for {transition.decision_id} must be a regular file")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise CliError(f"transition path for {transition.decision_id} escapes the project root")
    before = snapshot(info)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as error:
        raise CliError(
            f"transition file for {transition.decision_id} could not be read ({type(error).__name__})"
        ) from error
    try:
        opened_info = os.fstat(descriptor)
        if (
            is_redirect(opened_info)
            or not stat.S_ISREG(opened_info.st_mode)
            or snapshot(opened_info) != before
        ):
            raise CliError(f"transition file for {transition.decision_id} changed during inspection")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            digest.update(chunk)
        after_info = os.fstat(descriptor)
        if (
            is_redirect(after_info)
            or not stat.S_ISREG(after_info.st_mode)
            or snapshot(after_info) != snapshot(opened_info)
        ):
            raise CliError(f"transition file for {transition.decision_id} changed during inspection")
        return digest.hexdigest()
    except CliError:
        raise
    except OSError as error:
        raise CliError(
            f"transition file for {transition.decision_id} could not be read ({type(error).__name__})"
        ) from error
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass


def compute(root: Path, transition_date: str, transitions: list[Transition]) -> dict[str, object]:
    seen: set[str] = set()
    member_hashes: dict[str, str] = {}
    lines = [f"date:{transition_date}"]
    for transition in transitions:
        if transition.decision_id in seen:
            raise CliError(f"duplicate Decision ID: {transition.decision_id}")
        seen.add(transition.decision_id)
        file_hash = hash_member(root, transition)
        member_hashes[transition.decision_id] = file_hash
        lines.append(f"{transition.decision_id}:{transition.action}:{file_hash}")
    batch_payload = ("\n".join(lines) + "\n").encode("utf-8")
    return {
        "sha256": hashlib.sha256(batch_payload).hexdigest(),
        "members": [transition.decision_id for transition in transitions],
        "member_file_sha256": member_hashes,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = resolve_root(args.root)
        transition_date = parse_date(args.date)
        transitions = [parse_transition(value) for value in args.transition]
        result = compute(root, transition_date, transitions)
    except CliError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
