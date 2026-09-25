#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


PLAN_ID_RE = re.compile(r"PLAN-[0-9]{4}\Z")
WORK_ID_RE = re.compile(r"W-[0-9]{3}\Z")
UNIT_RE = re.compile(
    r"(?P<work_item>W-[0-9]{3})(?:/step-(?P<step>[1-9][0-9]*)|/steps-(?P<first>[1-9][0-9]*)-(?P<last>[1-9][0-9]*))?\Z"
)
DECISION_ID_RE = re.compile(r"ADR-[0-9]{4}\Z")
PLAN_FILE_RE = re.compile(r"([0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
DECISION_FILE_RE = re.compile(r"([0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
WORK_HEADING_RE = re.compile(r"^### (W-[0-9]{3}) [^\n]+$", re.MULTILINE)
MARKDOWN_HEADING_RE = re.compile(r"^#{1,6} [^\n]+$", re.MULTILINE)
FRONTMATTER_ENTRY_RE = re.compile(r"([a-z_]+): (.*)\Z")
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
DEFAULT_MAX_OUTPUT_BYTES = 65_536


class SelectorError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        path: str | None = None,
        expected: object | None = None,
        observed: object | None = None,
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
        self.expected = expected
        self.observed = observed
        self.exit_code = exit_code


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise SelectorError("USAGE_ERROR", message, exit_code=2)


@dataclass(frozen=True)
class ParsedRecord:
    frontmatter: dict[str, str]
    raw_frontmatter: str
    body: str
    newline: str = "\n"


@dataclass(frozen=True)
class WorkItem:
    item_id: str
    block: str
    status: str
    dependencies: list[str]
    decisions: list[str]


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        description="Select deterministic read-only Scoville Plan context."
    )
    parser.add_argument("--root", required=True, help="Project root containing PROJECT_INDEX.md.")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--work-item",
        help="Optional W-NNN item from the active Plan; defaults to current_item.",
    )
    selection.add_argument(
        "--unit",
        help="Exact dispatch unit: W-NNN, W-NNN/step-N, or W-NNN/steps-N-M.",
    )
    parser.add_argument(
        "--max-output-bytes",
        type=int,
        default=DEFAULT_MAX_OUTPUT_BYTES,
        help=f"Maximum UTF-8 success payload size; default {DEFAULT_MAX_OUTPUT_BYTES}.",
    )
    parser.add_argument("--format", choices=("json",), required=True)
    return parser


def is_redirect(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & REPARSE_POINT)


def resolve_root(value: str) -> Path:
    raw = Path(os.path.abspath(os.path.expanduser(value)))
    try:
        info = os.lstat(raw)
    except FileNotFoundError as error:
        raise SelectorError(
            "ROOT_MISSING", "root must be an existing directory", exit_code=2
        ) from error
    except OSError as error:
        raise SelectorError(
            "ROOT_UNREADABLE",
            f"root could not be inspected ({type(error).__name__})",
            exit_code=2,
        ) from error
    if is_redirect(info) or not stat.S_ISDIR(info.st_mode):
        raise SelectorError(
            "ROOT_INVALID",
            "root must be a regular non-symlink directory",
            exit_code=2,
        )
    return raw.resolve(strict=True)


def normalized_relative_path(value: str) -> PurePosixPath:
    if not value or "\\" in value or ":" in value:
        raise SelectorError("PATH_INVALID", "canonical path must use repository-relative forward slashes")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or relative.as_posix() != value
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise SelectorError("PATH_INVALID", "canonical path must be normalized and root-contained")
    return relative


def inspect_path(root: Path, relative: PurePosixPath) -> tuple[Path, os.stat_result]:
    current = root
    info: os.stat_result | None = None
    for part in relative.parts:
        current /= part
        try:
            info = os.lstat(current)
        except FileNotFoundError as error:
            raise SelectorError(
                "PATH_MISSING", "canonical path does not exist", path=relative.as_posix(), exit_code=2
            ) from error
        except OSError as error:
            raise SelectorError(
                "PATH_UNREADABLE",
                f"canonical path could not be inspected ({type(error).__name__})",
                path=relative.as_posix(),
                exit_code=2,
            ) from error
        if is_redirect(info):
            raise SelectorError(
                "PATH_REDIRECTED",
                "canonical path must not traverse a symlink or reparse point",
                path=relative.as_posix(),
                exit_code=2,
            )
    assert info is not None
    try:
        resolved = current.resolve(strict=True)
    except OSError as error:
        raise SelectorError(
            "PATH_UNREADABLE",
            f"canonical path could not be resolved ({type(error).__name__})",
            path=relative.as_posix(),
            exit_code=2,
        ) from error
    if not resolved.is_relative_to(root):
        raise SelectorError(
            "PATH_ESCAPES_ROOT",
            "canonical path escapes the project root",
            path=relative.as_posix(),
            exit_code=2,
        )
    return current, info


def safe_directory_entries(root: Path, relative_value: str) -> list[str]:
    relative = normalized_relative_path(relative_value)
    directory, before = inspect_path(root, relative)
    if not stat.S_ISDIR(before.st_mode):
        raise SelectorError(
            "PATH_NOT_DIRECTORY", "canonical path must be a directory", path=relative_value, exit_code=2
        )
    try:
        names = sorted(entry.name for entry in os.scandir(directory))
    except OSError as error:
        raise SelectorError(
            "PATH_UNREADABLE",
            f"canonical directory could not be listed ({type(error).__name__})",
            path=relative_value,
            exit_code=2,
        ) from error
    return names


def safe_read_text(root: Path, relative_value: str) -> str:
    relative = normalized_relative_path(relative_value)
    candidate, path_info = inspect_path(root, relative)
    if not stat.S_ISREG(path_info.st_mode):
        raise SelectorError(
            "PATH_NOT_FILE", "canonical path must be a regular file", path=relative_value, exit_code=2
        )
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as error:
        raise SelectorError(
            "FILE_UNREADABLE",
            f"canonical file could not be opened ({type(error).__name__})",
            path=relative_value,
            exit_code=2,
        ) from error
    try:
        opened = os.fstat(descriptor)
        if is_redirect(opened) or not stat.S_ISREG(opened.st_mode):
            raise SelectorError(
                "FILE_CHANGED_DURING_READ",
                "canonical file changed during inspection",
                path=relative_value,
                exit_code=2,
            )
        chunks: list[bytes] = []
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
    except SelectorError:
        raise
    except OSError as error:
        raise SelectorError(
            "FILE_UNREADABLE",
            f"canonical file could not be read ({type(error).__name__})",
            path=relative_value,
            exit_code=2,
        ) from error
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
    raw = b"".join(chunks)
    if raw.startswith(b"\xef\xbb\xbf"):
        raise SelectorError("FILE_BOM_FORBIDDEN", "canonical files must not contain a UTF-8 BOM", path=relative_value)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise SelectorError("FILE_UTF8_INVALID", "canonical file is not valid UTF-8", path=relative_value) from error
    if "\r" in text.replace("\r\n", "") or ("\r\n" in text and "\n" in text.replace("\r\n", "")):
        raise SelectorError("FILE_LINE_ENDING_INVALID", "canonical files must use consistent LF or CRLF line endings", path=relative_value)
    return text


def parse_record(text: str, relative_path: str) -> ParsedRecord:
    newline = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise SelectorError("FRONTMATTER_OPEN_MISSING", "record must start with frontmatter", path=relative_path)
    close = text.find("\n---\n", 4)
    if close < 0:
        raise SelectorError("FRONTMATTER_CLOSE_MISSING", "record frontmatter is not closed", path=relative_path)
    raw_frontmatter = text[: close + 5]
    entries: dict[str, str] = {}
    for line in text[4:close].split("\n"):
        match = FRONTMATTER_ENTRY_RE.fullmatch(line)
        if match is None:
            raise SelectorError("FRONTMATTER_ENTRY_INVALID", "frontmatter entry is malformed", path=relative_path)
        key, value = match.groups()
        if key in entries:
            raise SelectorError("FRONTMATTER_KEY_DUPLICATE", f"frontmatter key is repeated: {key}", path=relative_path)
        entries[key] = value
    return ParsedRecord(entries, raw_frontmatter.replace("\n", newline), text[close + 5 :], newline)


def require_format_version(record: ParsedRecord, relative_path: str) -> None:
    if record.frontmatter.get("format_version") != "1":
        raise SelectorError(
            "FORMAT_VERSION_UNSUPPORTED",
            "record format_version must be 1",
            path=relative_path,
            expected="1",
            observed=record.frontmatter.get("format_version"),
        )


def find_record_path(
    root: Path,
    directory: str,
    record_id: str,
    id_pattern: re.Pattern[str],
    filename_pattern: re.Pattern[str],
) -> str:
    if id_pattern.fullmatch(record_id) is None:
        raise SelectorError("RECORD_ID_INVALID", f"invalid record ID: {record_id}")
    number = record_id.split("-", 1)[1]
    matches = [
        name
        for name in safe_directory_entries(root, directory)
        if filename_pattern.fullmatch(name) is not None and name.startswith(number + "-")
    ]
    if len(matches) != 1:
        raise SelectorError(
            "RECORD_RESOLUTION_INVALID",
            f"record {record_id} must resolve to exactly one canonical file",
            path=directory,
            expected=1,
            observed=len(matches),
        )
    return f"{directory}/{matches[0]}"


def parse_inline_ids(value: str, pattern: re.Pattern[str], field: str, relative_path: str) -> list[str]:
    if value == "[]":
        return []
    if not value.startswith("[") or not value.endswith("]"):
        raise SelectorError("WORK_LIST_INVALID", f"{field} must be an inline ID list", path=relative_path)
    items = value[1:-1].split(", ")
    if any(pattern.fullmatch(item) is None for item in items) or len(set(items)) != len(items):
        raise SelectorError("WORK_LIST_INVALID", f"{field} contains invalid or duplicate IDs", path=relative_path)
    return items


def single_field(block: str, name: str, relative_path: str) -> str:
    matches = re.findall(rf"^{re.escape(name)}: (.*)$", block, re.MULTILINE)
    if len(matches) != 1:
        raise SelectorError(
            "WORK_FIELD_INVALID",
            f"selected Work Item must contain exactly one {name} field",
            path=relative_path,
            expected=1,
            observed=len(matches),
        )
    return matches[0].rstrip("\r")


def parse_steps(block: str, relative_path: str) -> list[str]:
    block = block.replace("\r\n", "\n")
    match = re.search(r"^Steps:\n(?P<body>.*?)(?=^Evidence: )", block, re.MULTILINE | re.DOTALL)
    if match is None:
        if re.search(r"^Steps:", block, re.MULTILINE):
            raise SelectorError("WORK_STEPS_INVALID", "selected Work Item Steps are malformed", path=relative_path)
        return []
    lines = match.group("body").splitlines()
    if not lines:
        raise SelectorError("WORK_STEPS_INVALID", "selected Work Item Steps must not be empty", path=relative_path)
    for expected, line in enumerate(lines, 1):
        if re.fullmatch(rf"{expected}\. .+", line) is None:
            raise SelectorError(
                "WORK_STEPS_INVALID",
                "selected Work Item Steps must be consecutive non-empty single lines",
                path=relative_path,
            )
    return lines


def project_unit(
    selected: WorkItem,
    unit: str,
    relative_path: str,
) -> dict[str, object]:
    unit_match = UNIT_RE.fullmatch(unit)
    if unit_match is None:
        raise SelectorError("UNIT_INVALID", "--unit has an invalid shape", exit_code=2)
    steps = parse_steps(selected.block, relative_path)
    requested_step = unit_match.group("step")
    requested_first = unit_match.group("first")
    requested_last = unit_match.group("last")
    if steps and requested_step is None and requested_first is None:
        raise SelectorError("UNIT_STEP_REQUIRED", "a Work Item with Steps requires an exact Step or adjacent Step range")
    if not steps and (requested_step is not None or requested_first is not None):
        raise SelectorError("UNIT_HAS_NO_STEPS", "a Work Item without Steps is one complete dispatch unit")
    if requested_step is not None:
        selected_numbers = [int(requested_step)]
    elif requested_first is not None and requested_last is not None:
        first = int(requested_first)
        last = int(requested_last)
        if first >= last:
            raise SelectorError("UNIT_RANGE_INVALID", "a Step range must contain at least two adjacent Steps")
        selected_numbers = list(range(first, last + 1))
    else:
        selected_numbers = []
    if any(number > len(steps) for number in selected_numbers):
        raise SelectorError(
            "UNIT_STEP_MISSING",
            "selected Step does not exist in the Work Item",
            expected={"maximum_step": len(steps)},
            observed={"selected_steps": selected_numbers},
        )
    lines = selected.block.splitlines()
    projection: dict[str, object] = {
        "unit": unit,
        "header": lines[0],
        "status": f"Status: {single_field(selected.block, 'Status', relative_path)}",
        "depends_on": f"Depends on: {single_field(selected.block, 'Depends on', relative_path)}",
        "blocked_by": f"Blocked by: {single_field(selected.block, 'Blocked by', relative_path)}",
        "decisions": f"Decisions: {single_field(selected.block, 'Decisions', relative_path)}",
        "outcome": f"Outcome: {single_field(selected.block, 'Outcome', relative_path)}",
        "acceptance": f"Acceptance: {single_field(selected.block, 'Acceptance', relative_path)}",
        "steps": [steps[number - 1] for number in selected_numbers],
        "source_text": ("\n".join(steps[number - 1] for number in selected_numbers) + "\n"
                        if steps else selected.block.replace("\r\n", "\n").rstrip("\n") + "\n"),
    }
    if not steps:
        projection["next_action"] = f"Next action: {single_field(selected.block, 'Next action', relative_path)}"
    return projection


def parse_plan(record: ParsedRecord, relative_path: str) -> tuple[str, str, dict[str, WorkItem]]:
    match = re.fullmatch(
        r"\n*# [^\n]+\n\n## Goal\n(?P<goal>.+?)\n\n## Non-goals\n(?P<non_goals>.+?)\n\n## Work items\n(?P<work_items>.*)",
        record.body,
        re.DOTALL,
    )
    if match is None:
        raise SelectorError(
            "PLAN_SECTION_BOUNDARY_INVALID",
            "Plan must contain one H1 followed by Goal, Non-goals, and Work items in exact order",
            path=relative_path,
        )
    goal_body = match.group("goal")
    non_goals_body = match.group("non_goals")
    work_text = match.group("work_items")
    if not goal_body.strip() or not non_goals_body.strip():
        raise SelectorError("PLAN_SECTION_EMPTY", "Goal and Non-goals must be non-empty", path=relative_path)
    if MARKDOWN_HEADING_RE.search(goal_body) or MARKDOWN_HEADING_RE.search(non_goals_body):
        raise SelectorError(
            "PLAN_SECTION_BOUNDARY_INVALID",
            "Goal and Non-goals must not contain nested or duplicate Markdown headings",
            path=relative_path,
        )
    headings = list(WORK_HEADING_RE.finditer(work_text))
    all_work_headings = list(MARKDOWN_HEADING_RE.finditer(work_text))
    if (
        not headings
        or work_text[: headings[0].start()].strip()
        or [heading.start() for heading in all_work_headings]
        != [heading.start() for heading in headings]
    ):
        raise SelectorError("WORK_BOUNDARY_INVALID", "Work items must contain canonical H3 blocks", path=relative_path)
    items: dict[str, WorkItem] = {}
    for index, heading in enumerate(headings):
        item_id = heading.group(1)
        if item_id in items:
            raise SelectorError("WORK_ITEM_ID_DUPLICATE", f"duplicate Work Item ID: {item_id}", path=relative_path)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(work_text)
        block = work_text[heading.start() : end]
        status = single_field(block, "Status", relative_path)
        dependencies = parse_inline_ids(single_field(block, "Depends on", relative_path), WORK_ID_RE, "Depends on", relative_path)
        decisions = parse_inline_ids(single_field(block, "Decisions", relative_path), DECISION_ID_RE, "Decisions", relative_path)
        items[item_id] = WorkItem(item_id, block.replace("\n", record.newline), status, dependencies, decisions)
    return ("## Goal\n" + goal_body).replace("\n", record.newline), ("## Non-goals\n" + non_goals_body).replace("\n", record.newline), items


def select_context(
    root: Path,
    requested_item: str | None,
    unit: str | None = None,
) -> dict[str, object]:
    index_path = "PROJECT_INDEX.md"
    index = parse_record(safe_read_text(root, index_path), index_path)
    require_format_version(index, index_path)
    active_plan = index.frontmatter.get("active_plan")
    if active_plan is None or active_plan == "null":
        raise SelectorError("ACTIVE_PLAN_MISSING", "project has no active Plan", path=index_path)
    plan_path = find_record_path(root, "docs/plans", active_plan, PLAN_ID_RE, PLAN_FILE_RE)
    plan = parse_record(safe_read_text(root, plan_path), plan_path)
    require_format_version(plan, plan_path)
    if plan.frontmatter.get("id") != active_plan or plan.frontmatter.get("status") != "active":
        raise SelectorError("ACTIVE_PLAN_INVALID", "index must reference one matching active Plan", path=plan_path)
    goal, non_goals, items = parse_plan(plan, plan_path)
    unit_match = UNIT_RE.fullmatch(unit) if unit is not None else None
    selected_id = unit_match.group("work_item") if unit_match is not None else requested_item or plan.frontmatter.get("current_item")
    if selected_id is None or WORK_ID_RE.fullmatch(selected_id) is None:
        raise SelectorError("CURRENT_ITEM_INVALID", "selected Work Item must match W-NNN", path=plan_path)
    selected = items.get(selected_id)
    if selected is None:
        raise SelectorError("WORK_ITEM_MISSING", f"selected Work Item does not exist: {selected_id}", path=plan_path)
    dependency_statuses: list[dict[str, str]] = []
    for dependency_id in selected.dependencies:
        dependency = items.get(dependency_id)
        if dependency is None:
            raise SelectorError("WORK_DEPENDENCY_MISSING", f"dependency does not exist: {dependency_id}", path=plan_path)
        dependency_statuses.append(
            {"id": dependency_id, "status_line": f"Status: {dependency.status}"}
        )
    decisions: list[str] = []
    for decision_id in selected.decisions:
        decision_path = find_record_path(root, "docs/decisions", decision_id, DECISION_ID_RE, DECISION_FILE_RE)
        decision_text = safe_read_text(root, decision_path)
        decision = parse_record(decision_text, decision_path)
        require_format_version(decision, decision_path)
        if decision.frontmatter.get("id") != decision_id:
            raise SelectorError("DECISION_ID_MISMATCH", f"Decision file does not contain {decision_id}", path=decision_path)
        decisions.append(decision_text)
    work_item: object = selected.block
    if unit is not None:
        work_item = project_unit(selected, unit, plan_path)
    return {
        "plan": {
            "frontmatter": plan.raw_frontmatter,
            "goal": goal,
            "non_goals": non_goals,
        },
        "work_item": work_item,
        "direct_dependencies": dependency_statuses,
        "decisions": decisions,
    }


def diagnostic_payload(error: SelectorError) -> dict[str, object]:
    diagnostic: dict[str, object] = {"code": error.code, "message": error.message}
    if error.path is not None:
        diagnostic["path"] = error.path
    if error.expected is not None:
        diagnostic["expected"] = error.expected
    if error.observed is not None:
        diagnostic["observed"] = error.observed
    return {"schema_version": 1, "valid": None, "diagnostics": [diagnostic]}


def encode_json(payload: object) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if args.work_item is not None and WORK_ID_RE.fullmatch(args.work_item) is None:
            raise SelectorError("WORK_ITEM_ID_INVALID", "--work-item must match W-NNN", exit_code=2)
        if args.max_output_bytes < 512:
            raise SelectorError("OUTPUT_BUDGET_INVALID", "--max-output-bytes must be at least 512", exit_code=2)
        if args.unit is not None and UNIT_RE.fullmatch(args.unit) is None:
            raise SelectorError("UNIT_INVALID", "--unit has an invalid shape", exit_code=2)
        root = resolve_root(args.root)
        payload = select_context(root, args.work_item, args.unit)
        encoded = encode_json(payload)
        if len(encoded) > args.max_output_bytes:
            raise SelectorError(
                "OUTPUT_BUDGET_EXCEEDED",
                "selected semantic context exceeds the configured output budget",
                expected={"maximum_bytes": args.max_output_bytes},
                observed={"required_bytes": len(encoded)},
            )
    except SelectorError as error:
        sys.stdout.buffer.write(encode_json(diagnostic_payload(error)))
        return error.exit_code
    except Exception as error:  # pragma: no cover - final containment boundary
        internal = SelectorError(
            "SELECTOR_INTERNAL_ERROR",
            f"selector failed unexpectedly ({type(error).__name__})",
            exit_code=3,
        )
        sys.stdout.buffer.write(encode_json(diagnostic_payload(internal)))
        return 3
    sys.stdout.buffer.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
