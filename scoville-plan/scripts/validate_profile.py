#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable


EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_INCOMPLETE = 2
EXIT_INTERNAL = 3

PLAN_ID_RE = re.compile(r"PLAN-[0-9]{4}\Z")
WORK_ID_RE = re.compile(r"W-[0-9]{3}\Z")
DECISION_ID_RE = re.compile(r"ADR-[0-9]{4}\Z")
PLAN_FILE_RE = re.compile(r"([0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
DECISION_FILE_RE = re.compile(r"([0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
SCOPE_RE = re.compile(r"[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*\Z")
BLOCKER_RE = re.compile(r"[A-Z][A-Z0-9]{1,15}-[A-Z0-9][A-Z0-9._-]{0,47}\Z")
HASH_RE = re.compile(r"[0-9a-fA-F]{64}\Z")

PLAN_STATUSES = {"draft", "active", "completed", "cancelled"}
WORK_STATUSES = {"todo", "in_progress", "paused", "done", "cancelled"}
DECISION_STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
TERMINAL_WORK_STATUSES = {"done", "cancelled"}

DIAGNOSTIC_CODES = {
    "DATE_INVALID",
    "DATE_ORDER_INVALID",
    "DECISION_ACCEPTED_FORBIDDEN",
    "DECISION_ACCEPTED_REQUIRED",
    "DECISION_BATCH_ASYMMETRIC",
    "DECISION_BATCH_HASH_INVALID",
    "DECISION_BATCH_MEMBER_INVALID",
    "DECISION_BATCH_MEMBER_MISSING",
    "DECISION_BATCH_PAIR_REQUIRED",
    "DECISION_PROPOSAL_METADATA_FORBIDDEN",
    "DECISION_SCOPE_INVALID",
    "DECISION_SUPERSESSION_ASYMMETRIC",
    "DECISION_SUPERSESSION_CYCLE",
    "DECISION_SUPERSESSION_MISSING",
    "DECISION_SUPERSESSION_STATUS",
    "DIRECTORY_UNREADABLE",
    "FILE_BOM_FORBIDDEN",
    "FILE_CHANGED_DURING_READ",
    "FILE_LINE_ENDING_INVALID",
    "FILE_UNREADABLE",
    "FILE_UTF8_INVALID",
    "FORMAT_VERSION_UNSUPPORTED",
    "FRONTMATTER_CLOSE_MISSING",
    "FRONTMATTER_ENTRY_INVALID",
    "FRONTMATTER_KEY_DUPLICATE",
    "FRONTMATTER_KEY_MISSING",
    "FRONTMATTER_KEY_ORDER",
    "FRONTMATTER_KEY_UNKNOWN",
    "FRONTMATTER_OPEN_MISSING",
    "INDEX_ACTIVE_PLAN_INVALID",
    "INDEX_ACTIVE_PLAN_MISSING",
    "INDEX_ACTIVE_PLAN_STATUS",
    "PATH_ESCAPES_ROOT",
    "PATH_REDIRECTED",
    "PLAN_COMPLETED_NONTERMINAL",
    "PLAN_CURRENT_ITEM_FORBIDDEN",
    "PLAN_CURRENT_ITEM_MISSING",
    "PLAN_CURRENT_ITEM_REQUIRED",
    "PLAN_CURRENT_ITEM_STATUS",
    "PLAN_IN_PROGRESS_COUNT",
    "PLAN_IN_PROGRESS_CURRENT_MISMATCH",
    "PLAN_NONACTIVE_IN_PROGRESS",
    "PROFILE_ACTIVE_PLAN_COUNT",
    "PROFILE_PATH_MISSING",
    "PROFILE_PATH_NOT_DIRECTORY",
    "RECORD_FILENAME_INVALID",
    "RECORD_ID_DUPLICATE",
    "RECORD_ID_FILENAME_MISMATCH",
    "RECORD_ID_INVALID",
    "ROOT_MISSING",
    "ROOT_NOT_DIRECTORY",
    "ROOT_TRAVERSAL",
    "SECTION_EMPTY",
    "SECTION_H1_INVALID",
    "SECTION_H2_ORDER",
    "STATUS_INVALID",
    "USAGE_ERROR",
    "VALIDATOR_INTERNAL_ERROR",
    "WORK_BLOCKER_INVALID",
    "WORK_CURRENT_DEPENDENCY_NOT_DONE",
    "WORK_DECISION_MISSING",
    "WORK_DEPENDENCY_CANCELLED",
    "WORK_DEPENDENCY_CYCLE",
    "WORK_DEPENDENCY_MISSING",
    "WORK_DEPENDENCY_ORDER",
    "WORK_EVIDENCE_INVALID",
    "WORK_FIELD_DUPLICATE",
    "WORK_FIELD_MISSING",
    "WORK_FIELD_ORDER",
    "WORK_FIELD_UNKNOWN",
    "WORK_ITEM_ID_DUPLICATE",
    "WORK_ITEM_MISSING",
    "WORK_LIST_INVALID",
    "WORK_NEXT_ACTION_FORBIDDEN",
    "WORK_NEXT_ACTION_REQUIRED",
    "WORK_STEPS_INVALID",
    "WORK_TERMINAL_BLOCKED",
    "WORK_TERMINAL_EVIDENCE_REQUIRED",
    "WORK_TEXT_EMPTY",
    "WORK_UNEXPECTED_LINE",
}


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    file: str
    line: int | None
    record: str | None
    field: str | None
    message: str
    expected: str | None
    observed: str | None
    suggestion: str
    related: tuple[str, ...] = field(default_factory=tuple)

    def sort_key(self) -> tuple[Any, ...]:
        return (
            self.file,
            self.line is None,
            self.line or 0,
            self.record or "",
            self.field or "",
            self.code,
            self.observed or "",
            self.message,
        )

    def identity(self) -> tuple[Any, ...]:
        return self.sort_key()


@dataclass
class ParsedFile:
    logical_path: str
    lines: list[str]
    frontmatter: dict[str, str]
    key_lines: dict[str, int]
    body_start: int


@dataclass
class WorkItem:
    id: str
    title: str
    line: int
    fields: dict[str, str]
    field_lines: dict[str, int]
    steps: list[str]
    dependencies: list[str]
    blockers: list[str]
    decisions: list[str]
    evidence: list[str]

    @property
    def status(self) -> str:
        return self.fields.get("Status", "")


@dataclass
class PlanRecord:
    path: str
    id: str
    status: str
    created: str
    updated: str
    current_item: str | None
    line: int
    items: list[WorkItem]


@dataclass
class DecisionRecord:
    path: str
    id: str
    status: str
    created: str
    accepted: str | None
    scope: str
    supersedes: str | None
    superseded_by: str | None
    transition_batch: str | None
    transition_batch_members: list[str]
    line: int


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


class Validator:
    def __init__(self, root_argument: str) -> None:
        self.root_argument = root_argument
        self.root = Path(os.path.abspath(os.path.expanduser(root_argument)))
        self.diagnostics: list[Diagnostic] = []
        self.incomplete = False
        self.files_checked = 0
        self.format_version: int | None = None
        self.index_active_plan: str | None = None
        self.plans: dict[str, PlanRecord] = {}
        self.decisions: dict[str, DecisionRecord] = {}

    def add(
        self,
        code: str,
        file: str,
        message: str,
        suggestion: str,
        *,
        line: int | None = None,
        record: str | None = None,
        field_name: str | None = None,
        expected: str | None = None,
        observed: str | None = None,
        related: Iterable[str] = (),
        incomplete: bool = False,
        severity: str = "error",
    ) -> None:
        if code not in DIAGNOSTIC_CODES:
            raise RuntimeError(f"Undeclared diagnostic code: {code}")
        if severity not in {"error", "warning"}:
            raise RuntimeError(f"Unsupported diagnostic severity: {severity}")
        self.incomplete = self.incomplete or incomplete
        self.diagnostics.append(
            Diagnostic(
                code=code,
                severity=severity,
                file=file,
                line=line,
                record=record,
                field=field_name,
                message=message,
                expected=expected,
                observed=observed,
                suggestion=suggestion,
                related=tuple(sorted(set(related))),
            )
        )

    def logical(self, path: Path) -> str:
        try:
            relative = os.path.relpath(os.fspath(path), os.fspath(self.root))
        except ValueError:
            return os.fspath(path)
        return Path(relative).as_posix()

    @staticmethod
    def _is_redirect_stat(info: os.stat_result) -> bool:
        attributes = getattr(info, "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        return stat.S_ISLNK(info.st_mode) or bool(attributes & reparse_flag)

    @staticmethod
    def _snapshot(info: os.stat_result) -> tuple[int, int, int, int]:
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)

    def _inside_root(self, path: Path) -> bool:
        try:
            root = os.path.normcase(os.fspath(self.root))
            candidate = os.path.normcase(os.fspath(path))
            return os.path.commonpath((root, candidate)) == root
        except ValueError:
            return False

    def _check_root(self) -> bool:
        raw_parts = Path(self.root_argument).parts
        if ".." in raw_parts:
            self.add(
                "ROOT_TRAVERSAL",
                ".",
                "The requested root contains a parent traversal segment.",
                "Pass the exact project root without `..`; do not normalize an ambiguous target silently.",
                observed=self.root_argument,
                incomplete=True,
            )
            return False
        current = Path(self.root.anchor)
        parts = self.root.parts[1:] if self.root.anchor else self.root.parts
        final_info: os.stat_result | None = None
        if not parts:
            try:
                final_info = os.lstat(self.root)
            except FileNotFoundError:
                self.add(
                    "ROOT_MISSING",
                    ".",
                    "The requested project root does not exist.",
                    "Pass an existing directory containing the native profile.",
                    observed=os.fspath(self.root),
                    incomplete=True,
                )
                return False
            except OSError as error:
                self.add(
                    "FILE_UNREADABLE",
                    os.fspath(self.root),
                    "The project root could not be inspected.",
                    "Resolve the filesystem access failure before validating; do not infer a structural verdict.",
                    observed=str(error),
                    incomplete=True,
                )
                return False
        for part in parts:
            current /= part
            try:
                info = os.lstat(current)
            except FileNotFoundError:
                self.add(
                    "ROOT_MISSING",
                    ".",
                    "The requested project root does not exist.",
                    "Pass an existing directory containing the native profile.",
                    observed=os.fspath(self.root),
                    incomplete=True,
                )
                return False
            except OSError as error:
                self.add(
                    "FILE_UNREADABLE",
                    os.fspath(current),
                    "A project-root component could not be inspected.",
                    "Resolve the filesystem access failure before validating; do not infer a structural verdict.",
                    observed=str(error),
                    incomplete=True,
                )
                return False
            final_info = info
            if self._is_redirect_stat(info):
                self.add(
                    "PATH_REDIRECTED",
                    os.fspath(current),
                    "The project root passes through a symlink, junction, or reparse point.",
                    "Use the physical project root directly; the validator does not follow redirected canonical paths.",
                    observed=os.fspath(current),
                    incomplete=True,
                )
                return False
        if final_info is None or not stat.S_ISDIR(final_info.st_mode):
            self.add(
                "ROOT_NOT_DIRECTORY",
                ".",
                "The requested project root is not a directory.",
                "Pass the repository directory, not a file.",
                observed=os.fspath(self.root),
                incomplete=True,
            )
            return False
        return True

    def _check_canonical_path(self, path: Path) -> bool:
        logical = self.logical(path)
        if not self._inside_root(path):
            self.add(
                "PATH_ESCAPES_ROOT",
                logical,
                "A canonical profile path escapes the immutable project root.",
                "Stop and resolve the project-root or path-selection conflict before reading files.",
                observed=os.fspath(path),
                incomplete=True,
            )
            return False
        try:
            info = os.lstat(path)
        except FileNotFoundError:
            return True
        except OSError as error:
            self.add(
                "FILE_UNREADABLE",
                logical,
                "A canonical path could not be inspected.",
                "Resolve the filesystem access failure before validating; do not infer a structural verdict.",
                observed=str(error),
                incomplete=True,
            )
            return False
        if self._is_redirect_stat(info):
            self.add(
                "PATH_REDIRECTED",
                logical,
                "A canonical profile path is a symlink, junction, or reparse point.",
                "Replace the redirected canonical path only with explicit authority; the validator will not follow it.",
                observed=logical,
                incomplete=True,
            )
            return False
        return True

    def _read_file(self, path: Path) -> str | None:
        logical = self.logical(path)
        if not self._check_canonical_path(path):
            return None
        try:
            before = os.lstat(path)
        except FileNotFoundError:
            self.add(
                "PROFILE_PATH_MISSING",
                logical,
                "A required native profile file is missing.",
                "Restore the required canonical file from known project facts; do not invent its authored content.",
                observed="missing",
            )
            return None
        except OSError as error:
            self.add(
                "FILE_UNREADABLE",
                logical,
                "A canonical profile file could not be inspected.",
                "Resolve the filesystem access failure before validating; do not infer a structural verdict.",
                observed=str(error),
                incomplete=True,
            )
            return None

        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor: int | None = None
        try:
            descriptor = os.open(path, flags)
            opened = os.fstat(descriptor)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
            after_open = os.fstat(descriptor)
            data = b"".join(chunks)
        except OSError as error:
            self.add(
                "FILE_UNREADABLE",
                logical,
                "A canonical profile file could not be read completely.",
                "Resolve permissions or I/O failure before validating; no structural verdict is available.",
                observed=str(error),
                incomplete=True,
            )
            return None
        finally:
            if descriptor is not None:
                os.close(descriptor)

        try:
            after_path = os.lstat(path)
        except OSError as error:
            self.add(
                "FILE_CHANGED_DURING_READ",
                logical,
                "The canonical file disappeared or became uninspectable during the read.",
                "Re-read stable project state before making any correction.",
                observed=str(error),
                incomplete=True,
            )
            return None

        snapshots = {self._snapshot(before), self._snapshot(opened), self._snapshot(after_open), self._snapshot(after_path)}
        if len(snapshots) != 1:
            self.add(
                "FILE_CHANGED_DURING_READ",
                logical,
                "The canonical file changed while it was being read.",
                "Re-run validation against stable bytes before making any correction.",
                observed="file metadata changed during read",
                incomplete=True,
            )
            return None

        self.files_checked += 1
        if data.startswith(b"\xef\xbb\xbf"):
            self.add(
                "FILE_BOM_FORBIDDEN",
                logical,
                "The file starts with a UTF-8 byte-order mark.",
                "Remove only the BOM while preserving every decoded character.",
                line=1,
                expected="UTF-8 without BOM",
                observed="UTF-8 BOM",
            )
            data = data[3:]
        if b"\r" in data:
            first = data.index(b"\r")
            self.add(
                "FILE_LINE_ENDING_INVALID",
                logical,
                "The file contains a carriage return instead of LF-only line endings.",
                "Convert line endings to LF without changing text content.",
                line=data[:first].count(b"\n") + 1,
                expected="LF",
                observed="CR or CRLF",
            )
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            self.add(
                "FILE_UTF8_INVALID",
                logical,
                "The file is not valid UTF-8.",
                "Restore valid UTF-8 bytes from the intended authored text; do not guess damaged content.",
                line=data[: error.start].count(b"\n") + 1,
                expected="valid UTF-8",
                observed=f"decode error at byte {error.start}",
            )
            return None
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _scan_markdown(self, directory: Path) -> list[Path]:
        logical = self.logical(directory)
        if not self._check_canonical_path(directory):
            return []
        try:
            info = os.lstat(directory)
        except FileNotFoundError:
            self.add(
                "PROFILE_PATH_MISSING",
                logical,
                "A required native profile directory is missing.",
                "Create the canonical directory only through an authorized Scoville Plan profile operation.",
                observed="missing",
            )
            return []
        except OSError as error:
            self.add(
                "DIRECTORY_UNREADABLE",
                logical,
                "A canonical profile directory could not be inspected.",
                "Resolve the filesystem access failure before validating.",
                observed=str(error),
                incomplete=True,
            )
            return []
        if not stat.S_ISDIR(info.st_mode):
            self.add(
                "PROFILE_PATH_NOT_DIRECTORY",
                logical,
                "A canonical profile directory path is not a directory.",
                "Restore the canonical directory shape without overwriting the unexpected path.",
                observed="not a directory",
            )
            return []
        try:
            entries = list(os.scandir(directory))
        except OSError as error:
            self.add(
                "DIRECTORY_UNREADABLE",
                logical,
                "A canonical profile directory could not be listed.",
                "Resolve permissions or I/O failure before validating.",
                observed=str(error),
                incomplete=True,
            )
            return []

        paths: list[Path] = []
        for entry in sorted(entries, key=lambda item: item.name):
            if not entry.name.endswith(".md"):
                continue
            path = Path(entry.path)
            if not self._check_canonical_path(path):
                continue
            try:
                entry_info = entry.stat(follow_symlinks=False)
            except OSError as error:
                self.add(
                    "FILE_UNREADABLE",
                    self.logical(path),
                    "A canonical record could not be inspected.",
                    "Resolve the filesystem access failure before validating.",
                    observed=str(error),
                    incomplete=True,
                )
                continue
            if not stat.S_ISREG(entry_info.st_mode):
                self.add(
                    "PROFILE_PATH_NOT_DIRECTORY",
                    self.logical(path),
                    "A Markdown record path is not a regular file.",
                    "Restore a regular canonical Markdown file without following the unexpected path.",
                    observed="not a regular file",
                )
                continue
            paths.append(path)
        return paths

    def _parse_frontmatter(self, logical: str, text: str) -> ParsedFile | None:
        lines = text.split("\n")
        if not lines or lines[0] != "---":
            self.add(
                "FRONTMATTER_OPEN_MISSING",
                logical,
                "The file does not begin with the frontmatter delimiter.",
                "Add the canonical opening delimiter before the existing frontmatter keys.",
                line=1,
                expected="---",
                observed=lines[0] if lines else "empty file",
            )
            return None
        try:
            closing = lines.index("---", 1)
        except ValueError:
            self.add(
                "FRONTMATTER_CLOSE_MISSING",
                logical,
                "The frontmatter has no closing delimiter.",
                "Add the closing delimiter after the canonical key block.",
                line=1,
                expected="closing ---",
                observed="missing",
            )
            return None

        values: dict[str, str] = {}
        key_lines: dict[str, int] = {}
        for index, line in enumerate(lines[1:closing], 2):
            match = re.fullmatch(r"([a-z_]+):(?: (.*))?", line)
            if not match:
                self.add(
                    "FRONTMATTER_ENTRY_INVALID",
                    logical,
                    "A frontmatter line is not a canonical key-value entry.",
                    "Rewrite only this line as `key: value` using a permitted key.",
                    line=index,
                    observed=line,
                )
                continue
            key, value = match.group(1), match.group(2) or ""
            if key in values:
                self.add(
                    "FRONTMATTER_KEY_DUPLICATE",
                    logical,
                    "A frontmatter key occurs more than once.",
                    "Keep one canonical occurrence without discarding conflicting authored values silently.",
                    line=index,
                    field_name=key,
                    observed=value,
                )
                continue
            values[key] = value
            key_lines[key] = index
        return ParsedFile(logical, lines, values, key_lines, closing + 1)

    def _validate_keys(
        self,
        parsed: ParsedFile,
        required: list[str],
        canonical: list[str],
        record: str | None,
    ) -> None:
        actual = list(parsed.frontmatter)
        unknown = [key for key in actual if key not in canonical]
        for key in unknown:
            self.add(
                "FRONTMATTER_KEY_UNKNOWN",
                parsed.logical_path,
                "The frontmatter contains an unsupported key.",
                "Remove the unsupported key only after preserving any authored fact in its canonical owner.",
                line=parsed.key_lines.get(key),
                record=record,
                field_name=key,
                expected=", ".join(canonical),
                observed=key,
            )
        for key in required:
            if key not in parsed.frontmatter:
                self.add(
                    "FRONTMATTER_KEY_MISSING",
                    parsed.logical_path,
                    "A required frontmatter key is missing.",
                    "Add the key at its canonical position using known project facts; do not invent its value.",
                    record=record,
                    field_name=key,
                    expected=key,
                    observed="missing",
                )
        known_actual = [key for key in actual if key in canonical]
        expected_order = [key for key in canonical if key in parsed.frontmatter]
        if known_actual != expected_order:
            self.add(
                "FRONTMATTER_KEY_ORDER",
                parsed.logical_path,
                "Frontmatter keys are not in canonical order.",
                "Move existing keys into canonical order without changing their values.",
                line=min(parsed.key_lines.values(), default=1),
                record=record,
                expected=", ".join(expected_order),
                observed=", ".join(known_actual),
            )

    def _validate_format_version(self, parsed: ParsedFile, record: str | None) -> None:
        value = parsed.frontmatter.get("format_version")
        if value != "1":
            self.add(
                "FORMAT_VERSION_UNSUPPORTED",
                parsed.logical_path,
                "The record does not declare supported format_version 1.",
                "Use a validator matching the declared format; do not migrate or rewrite the record automatically.",
                line=parsed.key_lines.get("format_version"),
                record=record,
                field_name="format_version",
                expected="1",
                observed=value or "missing",
            )

    def _parse_date(self, parsed: ParsedFile, key: str, record: str | None) -> date | None:
        value = parsed.frontmatter.get(key)
        if value is None:
            return None
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            parsed_date = None
        else:
            try:
                parsed_date = date.fromisoformat(value)
            except ValueError:
                parsed_date = None
        if parsed_date is None:
            self.add(
                "DATE_INVALID",
                parsed.logical_path,
                "A lifecycle date is not a valid ISO calendar date.",
                "Replace it only with the actual authorized lifecycle date.",
                line=parsed.key_lines.get(key),
                record=record,
                field_name=key,
                expected="YYYY-MM-DD",
                observed=value,
            )
        return parsed_date

    def _validate_headings(
        self,
        parsed: ParsedFile,
        expected_h2: list[str],
        record: str | None,
    ) -> dict[str, tuple[int, int]]:
        body = parsed.lines[parsed.body_start :]
        nonempty = [(index + parsed.body_start + 1, line) for index, line in enumerate(body) if line]
        h1 = [(line_no, line[2:]) for line_no, line in nonempty if line.startswith("# ")]
        first = nonempty[0] if nonempty else (parsed.body_start + 1, "")
        if len(h1) != 1 or not first[1].startswith("# ") or not first[1][2:].strip():
            self.add(
                "SECTION_H1_INVALID",
                parsed.logical_path,
                "The record must contain one non-empty H1 title immediately after frontmatter.",
                "Restore one canonical H1 title without changing the record's identity or lifecycle.",
                line=first[0],
                record=record,
                expected="one non-empty H1",
                observed=str([title for _, title in h1]),
            )

        h2 = [(index + 1, line[3:]) for index, line in enumerate(parsed.lines) if line.startswith("## ")]
        observed_h2 = [title for _, title in h2]
        if observed_h2 != expected_h2:
            self.add(
                "SECTION_H2_ORDER",
                parsed.logical_path,
                "The required H2 sections are missing, extra, or out of order.",
                "Restore the exact section names and order while preserving authored content.",
                line=h2[0][0] if h2 else parsed.body_start + 1,
                record=record,
                expected=" | ".join(expected_h2),
                observed=" | ".join(observed_h2),
            )

        bounds: dict[str, tuple[int, int]] = {}
        for position, (line_no, title) in enumerate(h2):
            end = h2[position + 1][0] - 1 if position + 1 < len(h2) else len(parsed.lines)
            bounds[title] = (line_no, end)
            content = [line for line in parsed.lines[line_no:end] if line and not line.startswith("### ")]
            if title in expected_h2 and title != "Work items" and not content:
                self.add(
                    "SECTION_EMPTY",
                    parsed.logical_path,
                    "A required section has no content.",
                    "Add the known authored content; do not infer rationale, evidence, or intent.",
                    line=line_no,
                    record=record,
                    field_name=title,
                    observed="empty",
                )
        return bounds

    def _parse_inline_list(
        self,
        value: str,
        *,
        parsed: ParsedFile,
        line: int | None,
        record: str,
        field_name: str,
        item_pattern: re.Pattern[str] | None = None,
    ) -> list[str]:
        if value == "[]":
            return []
        valid_shape = value.startswith("[") and value.endswith("]")
        inner = value[1:-1] if valid_shape else ""
        items = inner.split(", ") if inner else []
        if not valid_shape or not items or ", ".join(items) != inner or any(not item for item in items):
            self.add(
                "WORK_LIST_INVALID",
                parsed.logical_path,
                "An inline list does not use canonical `[]` or `[value, value]` syntax.",
                "Rewrite only the list delimiters and separators; preserve every intended member.",
                line=line,
                record=record,
                field_name=field_name,
                expected="[] or [value, value]",
                observed=value,
            )
            return []
        if len(set(items)) != len(items):
            self.add(
                "WORK_LIST_INVALID",
                parsed.logical_path,
                "An inline list contains duplicate members.",
                "Remove only duplicate occurrences while preserving authored order.",
                line=line,
                record=record,
                field_name=field_name,
                observed=value,
            )
        if item_pattern is not None:
            for item in items:
                if not item_pattern.fullmatch(item):
                    self.add(
                        "WORK_LIST_INVALID",
                        parsed.logical_path,
                        "An inline list member has an invalid identifier shape.",
                        "Correct the identifier only from an existing canonical record; do not invent a target.",
                        line=line,
                        record=record,
                        field_name=field_name,
                        expected=item_pattern.pattern,
                        observed=item,
                    )
        return items

    def _parse_work_items(self, parsed: ParsedFile, plan_id: str, work_bounds: tuple[int, int] | None) -> list[WorkItem]:
        if work_bounds is None:
            return []
        start, end = work_bounds
        starts: list[tuple[int, re.Match[str]]] = []
        for line_no in range(start + 1, end + 1):
            match = re.fullmatch(r"### (W-[0-9]{3}) (.+)", parsed.lines[line_no - 1])
            if match:
                starts.append((line_no, match))
        if not starts:
            self.add(
                "WORK_ITEM_MISSING",
                parsed.logical_path,
                "The Plan contains no Work Item block.",
                "Add at least one behavior-complete Work Item from known project outcomes.",
                line=start,
                record=plan_id,
                observed="none",
            )
            return []

        items: list[WorkItem] = []
        seen_ids: set[str] = set()
        expected_fields = [
            "Status",
            "Depends on",
            "Blocked by",
            "Decisions",
            "Outcome",
            "Acceptance",
            "Steps",
            "Evidence",
            "Next action",
        ]
        required_fields = [field for field in expected_fields if field not in {"Steps", "Next action"}]

        for index, (heading_line, match) in enumerate(starts):
            item_id, title = match.group(1), match.group(2).strip()
            record = f"{plan_id}/{item_id}"
            block_end = starts[index + 1][0] - 1 if index + 1 < len(starts) else end
            if item_id in seen_ids:
                self.add(
                    "WORK_ITEM_ID_DUPLICATE",
                    parsed.logical_path,
                    "A Work Item ID occurs more than once in the Plan.",
                    "Assign a new ID only through the Plan's allocation rule; do not renumber existing items.",
                    line=heading_line,
                    record=record,
                    observed=item_id,
                )
            seen_ids.add(item_id)
            if not title:
                self.add(
                    "WORK_TEXT_EMPTY",
                    parsed.logical_path,
                    "The Work Item title is empty.",
                    "Add the known observable outcome as the title.",
                    line=heading_line,
                    record=record,
                    field_name="title",
                    observed="empty",
                )

            fields: dict[str, str] = {}
            field_lines: dict[str, int] = {}
            field_order: list[str] = []
            steps: list[str] = []
            in_steps = False
            expected_step = 1
            for line_no in range(heading_line + 1, block_end + 1):
                line = parsed.lines[line_no - 1]
                if not line:
                    if in_steps:
                        self.add(
                            "WORK_STEPS_INVALID",
                            parsed.logical_path,
                            "Steps contain a blank line.",
                            "Keep consecutive non-empty single-line numbered Steps.",
                            line=line_no,
                            record=record,
                            field_name="Steps",
                            observed="blank line",
                        )
                    continue
                field_match = re.fullmatch(r"([A-Za-z][A-Za-z ]*):(.*)", line)
                if field_match:
                    name = field_match.group(1)
                    tail = field_match.group(2)
                    if name not in expected_fields:
                        self.add(
                            "WORK_FIELD_UNKNOWN",
                            parsed.logical_path,
                            "The Work Item contains an unsupported field.",
                            "Remove the field only after preserving its fact in the canonical allowed field.",
                            line=line_no,
                            record=record,
                            field_name=name,
                            observed=name,
                        )
                        in_steps = False
                        continue
                    value = tail[1:] if tail.startswith(" ") else tail
                    if tail and not tail.startswith(" "):
                        self.add(
                            "WORK_UNEXPECTED_LINE",
                            parsed.logical_path,
                            "A Work Item field lacks the required space after the colon.",
                            "Insert one space after the colon without changing the value.",
                            line=line_no,
                            record=record,
                            field_name=name,
                            observed=line,
                        )
                    if name in fields:
                        self.add(
                            "WORK_FIELD_DUPLICATE",
                            parsed.logical_path,
                            "A Work Item field occurs more than once.",
                            "Keep one canonical occurrence without discarding conflicting authored values silently.",
                            line=line_no,
                            record=record,
                            field_name=name,
                            observed=value,
                        )
                        continue
                    if name == "Steps" and value:
                        self.add(
                            "WORK_STEPS_INVALID",
                            parsed.logical_path,
                            "The Steps field must not have an inline value.",
                            "Move each known step to a consecutive numbered line below `Steps:`.",
                            line=line_no,
                            record=record,
                            field_name="Steps",
                            observed=value,
                        )
                    fields[name] = value
                    field_lines[name] = line_no
                    field_order.append(name)
                    in_steps = name == "Steps"
                    expected_step = 1
                    continue
                if in_steps:
                    step_match = re.fullmatch(r"([0-9]+)\. (.+)", line)
                    if not step_match or int(step_match.group(1)) != expected_step:
                        self.add(
                            "WORK_STEPS_INVALID",
                            parsed.logical_path,
                            "Steps are not consecutive numbered non-empty single lines.",
                            "Renumber existing Steps consecutively from `1.` without changing their order or meaning.",
                            line=line_no,
                            record=record,
                            field_name="Steps",
                            expected=f"{expected_step}. non-empty text",
                            observed=line,
                        )
                    else:
                        steps.append(step_match.group(2))
                        expected_step += 1
                    continue
                self.add(
                    "WORK_UNEXPECTED_LINE",
                    parsed.logical_path,
                    "The Work Item block contains a line outside its fields or Steps.",
                    "Move known content into its canonical field; do not discard authored information silently.",
                    line=line_no,
                    record=record,
                    observed=line,
                )

            for name in required_fields:
                if name not in fields:
                    self.add(
                        "WORK_FIELD_MISSING",
                        parsed.logical_path,
                        "A required Work Item field is missing.",
                        "Add the field at its canonical position using known project facts; do not invent content.",
                        line=heading_line,
                        record=record,
                        field_name=name,
                        expected=name,
                        observed="missing",
                    )
            expected_order = [name for name in expected_fields if name in fields]
            if field_order != expected_order:
                self.add(
                    "WORK_FIELD_ORDER",
                    parsed.logical_path,
                    "Work Item fields are not in canonical order.",
                    "Move existing fields into canonical order without changing their values.",
                    line=field_lines.get(field_order[0]) if field_order else heading_line,
                    record=record,
                    expected=", ".join(expected_order),
                    observed=", ".join(field_order),
                )

            status_value = fields.get("Status", "")
            if status_value and status_value not in WORK_STATUSES:
                self.add(
                    "STATUS_INVALID",
                    parsed.logical_path,
                    "The Work Item status is unsupported.",
                    "Use a permitted status only when it matches the authorized lifecycle state.",
                    line=field_lines.get("Status"),
                    record=record,
                    field_name="Status",
                    expected=", ".join(sorted(WORK_STATUSES)),
                    observed=status_value,
                )

            dependencies = self._parse_inline_list(
                fields.get("Depends on", ""),
                parsed=parsed,
                line=field_lines.get("Depends on"),
                record=record,
                field_name="Depends on",
                item_pattern=WORK_ID_RE,
            ) if "Depends on" in fields else []
            blockers = self._parse_inline_list(
                fields.get("Blocked by", ""),
                parsed=parsed,
                line=field_lines.get("Blocked by"),
                record=record,
                field_name="Blocked by",
            ) if "Blocked by" in fields else []
            decisions = self._parse_inline_list(
                fields.get("Decisions", ""),
                parsed=parsed,
                line=field_lines.get("Decisions"),
                record=record,
                field_name="Decisions",
                item_pattern=DECISION_ID_RE,
            ) if "Decisions" in fields else []
            evidence = self._parse_inline_list(
                fields.get("Evidence", ""),
                parsed=parsed,
                line=field_lines.get("Evidence"),
                record=record,
                field_name="Evidence",
            ) if "Evidence" in fields else []

            for blocker in blockers:
                if not BLOCKER_RE.fullmatch(blocker) or blocker.split("-", 1)[0] in {"ADR", "PLAN", "W"}:
                    self.add(
                        "WORK_BLOCKER_INVALID",
                        parsed.logical_path,
                        "A blocker label is invalid or uses a reserved prefix.",
                        "Replace it only with the actual external blocker label; do not invent a blocker.",
                        line=field_lines.get("Blocked by"),
                        record=record,
                        field_name="Blocked by",
                        observed=blocker,
                    )
            for entry in evidence:
                invalid = (
                    len(entry) > 200
                    or entry != entry.strip()
                    or any(character in entry for character in ",[]\r\n")
                    or any(ord(character) < 32 or ord(character) == 127 for character in entry)
                )
                if invalid:
                    self.add(
                        "WORK_EVIDENCE_INVALID",
                        parsed.logical_path,
                        "An Evidence entry violates the native scalar-value shape.",
                        "Correct only the representation of observed evidence; never invent or strengthen evidence.",
                        line=field_lines.get("Evidence"),
                        record=record,
                        field_name="Evidence",
                        observed=entry,
                    )
            for text_field in ("Outcome", "Acceptance"):
                if text_field in fields and not fields[text_field].strip():
                    self.add(
                        "WORK_TEXT_EMPTY",
                        parsed.logical_path,
                        "A required authored Work Item field is empty.",
                        "Supply the known authored content or ask the user; do not infer it from implementation.",
                        line=field_lines.get(text_field),
                        record=record,
                        field_name=text_field,
                        observed="empty",
                    )

            next_action = fields.get("Next action")
            if status_value in TERMINAL_WORK_STATUSES:
                if not evidence:
                    self.add(
                        "WORK_TERMINAL_EVIDENCE_REQUIRED",
                        parsed.logical_path,
                        "A terminal Work Item has no Evidence.",
                        "Stop and ask how to resolve invalid terminal history; do not invent Evidence or rewrite status.",
                        line=field_lines.get("Evidence"),
                        record=record,
                        field_name="Evidence",
                        observed=fields.get("Evidence", "missing"),
                    )
                if blockers:
                    self.add(
                        "WORK_TERMINAL_BLOCKED",
                        parsed.logical_path,
                        "A terminal Work Item still has blockers.",
                        "Stop and ask how the terminal transition should be reconciled; do not clear blockers retroactively.",
                        line=field_lines.get("Blocked by"),
                        record=record,
                        field_name="Blocked by",
                        observed=fields.get("Blocked by"),
                    )
                if next_action is not None:
                    self.add(
                        "WORK_NEXT_ACTION_FORBIDDEN",
                        parsed.logical_path,
                        "A terminal Work Item contains a Next action field.",
                        "Remove the field only if terminal status and Evidence are already authoritative.",
                        line=field_lines.get("Next action"),
                        record=record,
                        field_name="Next action",
                        observed=next_action,
                    )
            elif status_value in WORK_STATUSES:
                if next_action is None or not next_action.strip():
                    self.add(
                        "WORK_NEXT_ACTION_REQUIRED",
                        parsed.logical_path,
                        "A non-terminal Work Item has no non-empty Next action.",
                        "Set the first concrete action not yet performed using current project state.",
                        line=field_lines.get("Next action") or heading_line,
                        record=record,
                        field_name="Next action",
                        observed=next_action if next_action is not None else "missing",
                    )

            items.append(
                WorkItem(
                    id=item_id,
                    title=title,
                    line=heading_line,
                    fields=fields,
                    field_lines=field_lines,
                    steps=steps,
                    dependencies=dependencies,
                    blockers=blockers,
                    decisions=decisions,
                    evidence=evidence,
                )
            )
        return items

    def _parse_index(self, path: Path) -> None:
        text = self._read_file(path)
        if text is None:
            return
        parsed = self._parse_frontmatter("PROJECT_INDEX.md", text)
        if parsed is None:
            return
        self._validate_keys(parsed, ["format_version", "active_plan"], ["format_version", "active_plan"], None)
        self._validate_format_version(parsed, None)
        if parsed.frontmatter.get("format_version") == "1":
            self.format_version = 1
        active = parsed.frontmatter.get("active_plan")
        if active == "null":
            self.index_active_plan = None
        elif active and PLAN_ID_RE.fullmatch(active):
            self.index_active_plan = active
        elif active is not None:
            self.add(
                "INDEX_ACTIVE_PLAN_INVALID",
                parsed.logical_path,
                "active_plan is neither a Plan ID nor literal null.",
                "Use the human-selected active Plan ID or `null`; do not infer project direction.",
                line=parsed.key_lines.get("active_plan"),
                field_name="active_plan",
                expected="PLAN-0001 or null",
                observed=active,
            )

    def _parse_plan(self, path: Path) -> None:
        logical = self.logical(path)
        text = self._read_file(path)
        if text is None:
            return
        parsed = self._parse_frontmatter(logical, text)
        if parsed is None:
            return
        plan_id = parsed.frontmatter.get("id", "")
        record = plan_id if PLAN_ID_RE.fullmatch(plan_id) else None
        keys = ["format_version", "id", "status", "created", "updated", "current_item"]
        self._validate_keys(parsed, ["format_version", "id", "status", "created", "updated"], keys, record)
        self._validate_format_version(parsed, record)

        filename = PLAN_FILE_RE.fullmatch(path.name)
        if filename is None:
            self.add(
                "RECORD_FILENAME_INVALID",
                logical,
                "The Plan filename is not numeric-ID plus lowercase ASCII kebab-case subject.",
                "Rename it only through an authorized Plan edit after checking references and collisions.",
                record=record,
                observed=path.name,
            )
        if not PLAN_ID_RE.fullmatch(plan_id):
            self.add(
                "RECORD_ID_INVALID",
                logical,
                "The Plan ID is invalid.",
                "Restore the canonical ID from known project records; do not allocate a replacement implicitly.",
                line=parsed.key_lines.get("id"),
                field_name="id",
                expected="PLAN-[0-9]{4}",
                observed=plan_id or "missing",
            )
        elif filename and plan_id[5:] != filename.group(1):
            self.add(
                "RECORD_ID_FILENAME_MISMATCH",
                logical,
                "The Plan ID does not match the numeric filename prefix.",
                "Ask which existing identity is canonical before renaming or changing the ID.",
                line=parsed.key_lines.get("id"),
                record=plan_id,
                field_name="id",
                expected=f"PLAN-{filename.group(1)}",
                observed=plan_id,
            )

        status_value = parsed.frontmatter.get("status", "")
        if status_value and status_value not in PLAN_STATUSES:
            self.add(
                "STATUS_INVALID",
                logical,
                "The Plan status is unsupported.",
                "Use a permitted status only when it matches an authorized lifecycle result.",
                line=parsed.key_lines.get("status"),
                record=record,
                field_name="status",
                expected=", ".join(sorted(PLAN_STATUSES)),
                observed=status_value,
            )
        created = self._parse_date(parsed, "created", record)
        updated = self._parse_date(parsed, "updated", record)
        if created and updated and updated < created:
            self.add(
                "DATE_ORDER_INVALID",
                logical,
                "The Plan updated date precedes its created date.",
                "Restore the actual lifecycle dates; do not fabricate chronology.",
                line=parsed.key_lines.get("updated"),
                record=record,
                field_name="updated",
                expected=f">= {created.isoformat()}",
                observed=updated.isoformat(),
            )

        current = parsed.frontmatter.get("current_item")
        if status_value == "active" and current is None:
            self.add(
                "PLAN_CURRENT_ITEM_REQUIRED",
                logical,
                "An active Plan has no current_item.",
                "Ask the user which dependency-ready item is current before changing project state.",
                record=record,
                field_name="current_item",
                observed="missing",
            )
        if status_value != "active" and current is not None:
            self.add(
                "PLAN_CURRENT_ITEM_FORBIDDEN",
                logical,
                "A non-active Plan contains current_item.",
                "Reconcile the intended Plan lifecycle before removing or changing current work.",
                line=parsed.key_lines.get("current_item"),
                record=record,
                field_name="current_item",
                observed=current,
            )
        if current is not None and not WORK_ID_RE.fullmatch(current):
            self.add(
                "PLAN_CURRENT_ITEM_STATUS",
                logical,
                "current_item is not a valid Work Item ID.",
                "Restore the intended existing Work Item ID; do not invent a successor.",
                line=parsed.key_lines.get("current_item"),
                record=record,
                field_name="current_item",
                observed=current,
            )

        bounds = self._validate_headings(parsed, ["Goal", "Non-goals", "Work items"], record)
        items = self._parse_work_items(parsed, plan_id or logical, bounds.get("Work items"))
        if PLAN_ID_RE.fullmatch(plan_id):
            if plan_id in self.plans:
                self.add(
                    "RECORD_ID_DUPLICATE",
                    logical,
                    "The Plan ID is owned by more than one file.",
                    "Stop and ask which record owns the identity; do not merge or renumber automatically.",
                    record=plan_id,
                    observed=plan_id,
                    related=(self.plans[plan_id].path,),
                )
            else:
                self.plans[plan_id] = PlanRecord(
                    path=logical,
                    id=plan_id,
                    status=status_value,
                    created=parsed.frontmatter.get("created", ""),
                    updated=parsed.frontmatter.get("updated", ""),
                    current_item=current,
                    line=parsed.key_lines.get("id", 1),
                    items=items,
                )

    def _parse_decision(self, path: Path) -> None:
        logical = self.logical(path)
        text = self._read_file(path)
        if text is None:
            return
        parsed = self._parse_frontmatter(logical, text)
        if parsed is None:
            return
        decision_id = parsed.frontmatter.get("id", "")
        record = decision_id if DECISION_ID_RE.fullmatch(decision_id) else None
        keys = [
            "format_version",
            "id",
            "status",
            "created",
            "accepted",
            "scope",
            "supersedes",
            "superseded_by",
            "transition_batch",
            "transition_batch_members",
        ]
        self._validate_keys(parsed, ["format_version", "id", "status", "created", "scope"], keys, record)
        self._validate_format_version(parsed, record)

        filename = DECISION_FILE_RE.fullmatch(path.name)
        if filename is None:
            self.add(
                "RECORD_FILENAME_INVALID",
                logical,
                "The Decision filename is not numeric-ID plus lowercase ASCII kebab-case subject.",
                "Rename only an editable proposal after checking every incoming reference and collision.",
                record=record,
                observed=path.name,
            )
        if not DECISION_ID_RE.fullmatch(decision_id):
            self.add(
                "RECORD_ID_INVALID",
                logical,
                "The Decision ID is invalid.",
                "Restore the canonical ID from known project records; do not allocate a replacement implicitly.",
                line=parsed.key_lines.get("id"),
                field_name="id",
                expected="ADR-[0-9]{4}",
                observed=decision_id or "missing",
            )
        elif filename and decision_id[4:] != filename.group(1):
            self.add(
                "RECORD_ID_FILENAME_MISMATCH",
                logical,
                "The Decision ID does not match the numeric filename prefix.",
                "Ask which existing identity is canonical before renaming or changing the ID.",
                line=parsed.key_lines.get("id"),
                record=decision_id,
                field_name="id",
                expected=f"ADR-{filename.group(1)}",
                observed=decision_id,
            )

        status_value = parsed.frontmatter.get("status", "")
        if status_value and status_value not in DECISION_STATUSES:
            self.add(
                "STATUS_INVALID",
                logical,
                "The Decision status is unsupported.",
                "Use a permitted status only after the required explicit lifecycle choice.",
                line=parsed.key_lines.get("status"),
                record=record,
                field_name="status",
                expected=", ".join(sorted(DECISION_STATUSES)),
                observed=status_value,
            )
        created = self._parse_date(parsed, "created", record)
        accepted = self._parse_date(parsed, "accepted", record)
        if created and accepted and accepted < created:
            self.add(
                "DATE_ORDER_INVALID",
                logical,
                "The Decision accepted date precedes its created date.",
                "Restore the actual authorized dates; do not fabricate chronology.",
                line=parsed.key_lines.get("accepted"),
                record=record,
                field_name="accepted",
                expected=f">= {created.isoformat()}",
                observed=accepted.isoformat(),
            )
        if status_value in {"accepted", "deprecated", "superseded"} and "accepted" not in parsed.frontmatter:
            self.add(
                "DECISION_ACCEPTED_REQUIRED",
                logical,
                "This Decision status requires an accepted date.",
                "Ask for the actual authorized acceptance date; do not infer it from implementation or Git.",
                record=record,
                field_name="accepted",
                observed="missing",
            )
        if status_value in {"proposed", "rejected"} and "accepted" in parsed.frontmatter:
            self.add(
                "DECISION_ACCEPTED_FORBIDDEN",
                logical,
                "This Decision status must omit the accepted date.",
                "Ask which explicitly authorized lifecycle result is intended before changing either field.",
                line=parsed.key_lines.get("accepted"),
                record=record,
                field_name="accepted",
                observed=parsed.frontmatter.get("accepted"),
            )
        if status_value == "proposed":
            forbidden = [key for key in ("accepted", "supersedes", "superseded_by", "transition_batch", "transition_batch_members") if key in parsed.frontmatter]
            if forbidden:
                self.add(
                    "DECISION_PROPOSAL_METADATA_FORBIDDEN",
                    logical,
                    "A proposed Decision contains lifecycle metadata that proposals must omit.",
                    "Ask whether the Decision is still proposed before removing metadata; do not infer a transition.",
                    line=min((parsed.key_lines[key] for key in forbidden), default=None),
                    record=record,
                    observed=", ".join(forbidden),
                )

        scope = parsed.frontmatter.get("scope", "")
        if scope and not SCOPE_RE.fullmatch(scope):
            self.add(
                "DECISION_SCOPE_INVALID",
                logical,
                "The Decision scope is not a canonical slash-separated domain label.",
                "Correct only the representation of the known scope; do not broaden it.",
                line=parsed.key_lines.get("scope"),
                record=record,
                field_name="scope",
                expected="lowercase slash-separated domain label",
                observed=scope,
            )

        transition_batch = parsed.frontmatter.get("transition_batch")
        member_value = parsed.frontmatter.get("transition_batch_members")
        if (transition_batch is None) != (member_value is None):
            self.add(
                "DECISION_BATCH_PAIR_REQUIRED",
                logical,
                "Decision batch hash and member list must occur together.",
                "Stop as an incomplete transition; do not add or remove batch metadata without the authorized batch facts.",
                line=parsed.key_lines.get("transition_batch") or parsed.key_lines.get("transition_batch_members"),
                record=record,
                observed=f"hash={transition_batch is not None}, members={member_value is not None}",
            )
        if transition_batch is not None and not HASH_RE.fullmatch(transition_batch):
            self.add(
                "DECISION_BATCH_HASH_INVALID",
                logical,
                "The transition_batch value is not a 64-hex SHA-256 shape.",
                "Restore the recorded batch identifier from all batch members; it cannot be recomputed from post-transition bytes.",
                line=parsed.key_lines.get("transition_batch"),
                record=record,
                field_name="transition_batch",
                expected="64 hexadecimal characters",
                observed=transition_batch,
            )
        members = self._parse_inline_list(
            member_value,
            parsed=parsed,
            line=parsed.key_lines.get("transition_batch_members"),
            record=record or logical,
            field_name="transition_batch_members",
            item_pattern=DECISION_ID_RE,
        ) if member_value is not None else []

        self._validate_headings(
            parsed,
            ["Decision", "Problem", "Drivers", "Considered alternatives", "Consequences", "Confirmation", "Revisit when"],
            record,
        )
        if DECISION_ID_RE.fullmatch(decision_id):
            if decision_id in self.decisions:
                self.add(
                    "RECORD_ID_DUPLICATE",
                    logical,
                    "The Decision ID is owned by more than one file.",
                    "Stop and ask which record owns the identity; do not merge or renumber automatically.",
                    record=decision_id,
                    observed=decision_id,
                    related=(self.decisions[decision_id].path,),
                )
            else:
                self.decisions[decision_id] = DecisionRecord(
                    path=logical,
                    id=decision_id,
                    status=status_value,
                    created=parsed.frontmatter.get("created", ""),
                    accepted=parsed.frontmatter.get("accepted"),
                    scope=scope,
                    supersedes=parsed.frontmatter.get("supersedes"),
                    superseded_by=parsed.frontmatter.get("superseded_by"),
                    transition_batch=transition_batch,
                    transition_batch_members=members,
                    line=parsed.key_lines.get("id", 1),
                )

    def _validate_plans(self) -> None:
        active = [plan for plan in self.plans.values() if plan.status == "active"]
        if self.index_active_plan is None:
            if active:
                self.add(
                    "PROFILE_ACTIVE_PLAN_COUNT",
                    "PROJECT_INDEX.md",
                    "The index is idle but one or more Plans are active.",
                    "Ask which lifecycle result is intended before changing the index or Plan statuses.",
                    expected="zero active Plans",
                    observed=", ".join(plan.id for plan in active),
                    related=(plan.path for plan in active),
                )
        else:
            selected = self.plans.get(self.index_active_plan)
            if selected is None:
                self.add(
                    "INDEX_ACTIVE_PLAN_MISSING",
                    "PROJECT_INDEX.md",
                    "active_plan references a Plan record that does not exist.",
                    "Restore the referenced record or ask which existing Plan should be active; do not invent one.",
                    field_name="active_plan",
                    expected=self.index_active_plan,
                    observed="missing record",
                )
            elif selected.status != "active":
                self.add(
                    "INDEX_ACTIVE_PLAN_STATUS",
                    "PROJECT_INDEX.md",
                    "active_plan references a Plan whose status is not active.",
                    "Ask which lifecycle state is intended before aligning the index and Plan.",
                    field_name="active_plan",
                    expected="referenced Plan status active",
                    observed=f"{selected.id} status {selected.status}",
                    related=(selected.path,),
                )
            if len(active) != 1 or (active and active[0].id != self.index_active_plan):
                self.add(
                    "PROFILE_ACTIVE_PLAN_COUNT",
                    "PROJECT_INDEX.md",
                    "The set of active Plans does not match the index.",
                    "Ask which single Plan is intended to be active before changing lifecycle state.",
                    expected=self.index_active_plan,
                    observed=", ".join(plan.id for plan in active) or "none",
                    related=(plan.path for plan in active),
                )

        for plan in self.plans.values():
            items = {item.id: item for item in plan.items}
            positions = {item.id: index for index, item in enumerate(plan.items)}
            in_progress = [item for item in plan.items if item.status == "in_progress"]
            if len(in_progress) > 1:
                self.add(
                    "PLAN_IN_PROGRESS_COUNT",
                    plan.path,
                    "The Plan has more than one in_progress Work Item.",
                    "Ask which item is actually in progress before changing statuses or current_item.",
                    record=plan.id,
                    expected="at most one",
                    observed=", ".join(item.id for item in in_progress),
                )
            if plan.status == "active":
                if plan.current_item and plan.current_item not in items:
                    self.add(
                        "PLAN_CURRENT_ITEM_MISSING",
                        plan.path,
                        "current_item does not name a Work Item in this Plan.",
                        "Ask which existing dependency-ready item is current; do not invent a successor.",
                        record=plan.id,
                        field_name="current_item",
                        expected="existing Work Item ID",
                        observed=plan.current_item,
                    )
                elif plan.current_item:
                    current = items[plan.current_item]
                    if current.status not in {"todo", "in_progress", "paused"}:
                        self.add(
                            "PLAN_CURRENT_ITEM_STATUS",
                            plan.path,
                            "current_item names a terminal Work Item.",
                            "Ask which eligible item should be current before changing lifecycle state.",
                            line=current.line,
                            record=f"{plan.id}/{current.id}",
                            field_name="Status",
                            expected="todo, in_progress, or paused",
                            observed=current.status,
                        )
                    for dependency in current.dependencies:
                        target = items.get(dependency)
                        if target is not None and target.status != "done":
                            self.add(
                                "WORK_CURRENT_DEPENDENCY_NOT_DONE",
                                plan.path,
                                "The current Work Item has a dependency that is not done.",
                                "Ask whether current selection or dependency lifecycle is wrong; do not advance either automatically.",
                                line=current.field_lines.get("Depends on"),
                                record=f"{plan.id}/{current.id}",
                                field_name="Depends on",
                                expected="all dependencies done",
                                observed=f"{target.id} status {target.status}",
                                related=(f"{plan.id}/{target.id}",),
                            )
                if in_progress and plan.current_item != in_progress[0].id:
                    self.add(
                        "PLAN_IN_PROGRESS_CURRENT_MISMATCH",
                        plan.path,
                        "The in_progress Work Item does not equal current_item.",
                        "Ask which item is actually current before aligning status and current_item.",
                        record=plan.id,
                        expected=in_progress[0].id,
                        observed=plan.current_item or "missing",
                        related=(f"{plan.id}/{in_progress[0].id}",),
                    )
            elif in_progress:
                self.add(
                    "PLAN_NONACTIVE_IN_PROGRESS",
                    plan.path,
                    "A non-active Plan contains an in_progress Work Item.",
                    "Ask how the interrupted lifecycle should be resolved; do not pause, cancel, or complete it automatically.",
                    record=plan.id,
                    observed=", ".join(item.id for item in in_progress),
                )
            if plan.status == "completed":
                nonterminal = [item.id for item in plan.items if item.status not in TERMINAL_WORK_STATUSES]
                if nonterminal:
                    self.add(
                        "PLAN_COMPLETED_NONTERMINAL",
                        plan.path,
                        "A completed Plan contains non-terminal Work Items.",
                        "Ask how the completion transition should be reconciled; do not invent terminal Evidence.",
                        record=plan.id,
                        expected="only done or cancelled items",
                        observed=", ".join(nonterminal),
                    )

            for item in plan.items:
                record = f"{plan.id}/{item.id}"
                for dependency in item.dependencies:
                    target = items.get(dependency)
                    if target is None:
                        self.add(
                            "WORK_DEPENDENCY_MISSING",
                            plan.path,
                            "A Work Item dependency does not exist in the same Plan.",
                            "Restore the referenced item or ask which dependency was intended; do not invent one.",
                            line=item.field_lines.get("Depends on"),
                            record=record,
                            field_name="Depends on",
                            observed=dependency,
                        )
                        continue
                    if positions[dependency] >= positions[item.id]:
                        self.add(
                            "WORK_DEPENDENCY_ORDER",
                            plan.path,
                            "A dependency does not precede its dependent Work Item.",
                            "Reorder only eligible todo items or ask whether the dependency relation is wrong.",
                            line=item.field_lines.get("Depends on"),
                            record=record,
                            field_name="Depends on",
                            expected="earlier Work Item",
                            observed=dependency,
                            related=(f"{plan.id}/{dependency}",),
                        )
                    if target.status == "cancelled":
                        self.add(
                            "WORK_DEPENDENCY_CANCELLED",
                            plan.path,
                            "A Work Item depends on cancelled work, which never satisfies a dependency.",
                            "Ask whether the dependent outcome or dependency relation must change; do not select a replacement silently.",
                            line=item.field_lines.get("Depends on"),
                            record=record,
                            field_name="Depends on",
                            observed=dependency,
                            related=(f"{plan.id}/{dependency}",),
                        )
                for decision_id in item.decisions:
                    if decision_id not in self.decisions:
                        self.add(
                            "WORK_DECISION_MISSING",
                            plan.path,
                            "A Work Item references a Decision record that does not exist.",
                            "Restore the record or ask which Decision was intended; do not invent rationale or lifecycle.",
                            line=item.field_lines.get("Decisions"),
                            record=record,
                            field_name="Decisions",
                            observed=decision_id,
                        )

            visiting: set[str] = set()
            visited: set[str] = set()

            def visit(item_id: str, trail: tuple[str, ...]) -> None:
                if item_id in visiting:
                    cycle = trail + (item_id,)
                    item = items[item_id]
                    self.add(
                        "WORK_DEPENDENCY_CYCLE",
                        plan.path,
                        "Work Item dependencies contain a cycle.",
                        "Ask which dependency relation is incorrect; do not remove one arbitrarily.",
                        line=item.field_lines.get("Depends on"),
                        record=f"{plan.id}/{item_id}",
                        observed=" -> ".join(cycle),
                    )
                    return
                if item_id in visited:
                    return
                visiting.add(item_id)
                item = items[item_id]
                for dependency in item.dependencies:
                    if dependency in items:
                        visit(dependency, trail + (item_id,))
                visiting.remove(item_id)
                visited.add(item_id)

            for item_id in items:
                visit(item_id, ())

    def _validate_decisions(self) -> None:
        for decision in self.decisions.values():
            if decision.supersedes and decision.status not in {"accepted", "deprecated", "superseded"}:
                self.add(
                    "DECISION_SUPERSESSION_STATUS",
                    decision.path,
                    "A Decision with supersedes has never entered an accepted lifecycle state.",
                    "Ask which authorized lifecycle result is intended before changing metadata or status.",
                    record=decision.id,
                    field_name="supersedes",
                    expected="accepted, deprecated, or superseded",
                    observed=decision.status,
                )
            if decision.superseded_by and decision.status != "superseded":
                self.add(
                    "DECISION_SUPERSESSION_STATUS",
                    decision.path,
                    "A Decision with superseded_by is not in superseded status.",
                    "Ask which authorized lifecycle state is intended before changing metadata or status.",
                    record=decision.id,
                    field_name="superseded_by",
                    observed=f"status {decision.status}",
                )
            if decision.status == "superseded" and not decision.superseded_by:
                self.add(
                    "DECISION_SUPERSESSION_MISSING",
                    decision.path,
                    "A superseded Decision does not identify its replacement.",
                    "Restore the authorized replacement link; do not invent a Decision.",
                    record=decision.id,
                    field_name="superseded_by",
                    observed="missing",
                )
            if decision.supersedes:
                previous = self.decisions.get(decision.supersedes)
                if previous is None:
                    self.add(
                        "DECISION_SUPERSESSION_MISSING",
                        decision.path,
                        "supersedes references a Decision that does not exist.",
                        "Restore the referenced Decision or ask which authorized replacement relation was intended.",
                        record=decision.id,
                        field_name="supersedes",
                        observed=decision.supersedes,
                    )
                elif previous.superseded_by != decision.id:
                    self.add(
                        "DECISION_SUPERSESSION_ASYMMETRIC",
                        decision.path,
                        "The supersession relation is not reciprocal.",
                        "Stop as an incomplete transition and ask whether to complete or revert the authorized supersession.",
                        record=decision.id,
                        field_name="supersedes",
                        expected=f"{previous.id}.superseded_by={decision.id}",
                        observed=previous.superseded_by or "missing",
                        related=(previous.path,),
                    )
            if decision.superseded_by:
                replacement = self.decisions.get(decision.superseded_by)
                if replacement is None:
                    self.add(
                        "DECISION_SUPERSESSION_MISSING",
                        decision.path,
                        "superseded_by references a Decision that does not exist.",
                        "Restore the referenced replacement or ask how the interrupted supersession should be resolved.",
                        record=decision.id,
                        field_name="superseded_by",
                        observed=decision.superseded_by,
                    )
                elif replacement.supersedes != decision.id:
                    self.add(
                        "DECISION_SUPERSESSION_ASYMMETRIC",
                        decision.path,
                        "The supersession relation is not reciprocal.",
                        "Stop as an incomplete transition and ask whether to complete or revert the authorized supersession.",
                        record=decision.id,
                        field_name="superseded_by",
                        expected=f"{replacement.id}.supersedes={decision.id}",
                        observed=replacement.supersedes or "missing",
                        related=(replacement.path,),
                    )

            if decision.transition_batch is not None:
                members = decision.transition_batch_members
                if len(set(members)) != len(members) or decision.id not in members:
                    self.add(
                        "DECISION_BATCH_MEMBER_INVALID",
                        decision.path,
                        "Decision batch members are duplicate or do not include this Decision.",
                        "Stop as an incomplete batch; restore the exact authorized ordered member list from all records.",
                        record=decision.id,
                        field_name="transition_batch_members",
                        observed=", ".join(members),
                    )
                for member_id in members:
                    member = self.decisions.get(member_id)
                    if member is None:
                        self.add(
                            "DECISION_BATCH_MEMBER_MISSING",
                            decision.path,
                            "A Decision batch member record is missing.",
                            "Stop as an incomplete batch; do not create a replacement Decision automatically.",
                            record=decision.id,
                            field_name="transition_batch_members",
                            observed=member_id,
                        )
                        continue
                    if member.transition_batch != decision.transition_batch or member.transition_batch_members != members:
                        self.add(
                            "DECISION_BATCH_ASYMMETRIC",
                            decision.path,
                            "Decision batch metadata is not identical across every ordered member.",
                            "Stop as an incomplete batch and ask whether to complete or revert the authorized transition.",
                            record=decision.id,
                            field_name="transition_batch_members",
                            expected=f"{decision.transition_batch} [{', '.join(members)}]",
                            observed=f"{member.id}: {member.transition_batch} [{', '.join(member.transition_batch_members)}]",
                            related=(member.path,),
                        )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(decision_id: str, trail: tuple[str, ...]) -> None:
            if decision_id in visiting:
                decision = self.decisions[decision_id]
                self.add(
                    "DECISION_SUPERSESSION_CYCLE",
                    decision.path,
                    "Decision supersession links contain a cycle.",
                    "Ask which authorized supersession relation is wrong; do not remove one arbitrarily.",
                    record=decision.id,
                    observed=" -> ".join(trail + (decision_id,)),
                )
                return
            if decision_id in visited:
                return
            visiting.add(decision_id)
            target = self.decisions[decision_id].superseded_by
            if target in self.decisions:
                visit(target, trail + (decision_id,))
            visiting.remove(decision_id)
            visited.add(decision_id)

        for decision_id in self.decisions:
            visit(decision_id, ())

    def run(self) -> tuple[dict[str, Any], int]:
        if not self._check_root():
            return self.result(), EXIT_INCOMPLETE
        index_path = self.root / "PROJECT_INDEX.md"
        plans_dir = self.root / "docs" / "plans"
        decisions_dir = self.root / "docs" / "decisions"
        self._parse_index(index_path)
        for path in self._scan_markdown(plans_dir):
            self._parse_plan(path)
        for path in self._scan_markdown(decisions_dir):
            self._parse_decision(path)
        self._validate_plans()
        self._validate_decisions()
        if self.incomplete:
            exit_code = EXIT_INCOMPLETE
        elif any(diagnostic.severity == "error" for diagnostic in self.diagnostics):
            exit_code = EXIT_INVALID
        else:
            exit_code = EXIT_VALID
        return self.result(), exit_code

    def result(self) -> dict[str, Any]:
        unique = {diagnostic.identity(): diagnostic for diagnostic in self.diagnostics}
        diagnostics = sorted(unique.values(), key=Diagnostic.sort_key)
        errors = sum(diagnostic.severity == "error" for diagnostic in diagnostics)
        warnings = sum(diagnostic.severity == "warning" for diagnostic in diagnostics)
        if self.incomplete:
            valid: bool | None = None
        else:
            valid = errors == 0
        return {
            "schema_version": 1,
            "valid": valid,
            "root": os.fspath(self.root),
            "format_version": self.format_version,
            "summary": {
                "errors": errors,
                "warnings": warnings,
                "files_checked": self.files_checked,
                "plans": len(self.plans),
                "work_items": sum(len(plan.items) for plan in self.plans.values()),
                "decisions": len(self.decisions),
            },
            "diagnostics": [asdict(diagnostic) for diagnostic in diagnostics],
        }


def render_text(result: dict[str, Any], exit_code: int) -> str:
    state = {
        EXIT_VALID: "VALID",
        EXIT_INVALID: "INVALID",
        EXIT_INCOMPLETE: "INCOMPLETE",
        EXIT_INTERNAL: "INTERNAL ERROR",
    }[exit_code]
    summary = result["summary"]
    lines = [
        f"{state}: {result['root']}",
        f"errors={summary['errors']} warnings={summary['warnings']} files={summary['files_checked']} plans={summary['plans']} work_items={summary['work_items']} decisions={summary['decisions']}",
    ]
    for diagnostic in result["diagnostics"]:
        location = diagnostic["file"]
        if diagnostic["line"] is not None:
            location += f":{diagnostic['line']}"
        context = "/".join(value for value in (diagnostic["record"], diagnostic["field"]) if value)
        if context:
            location += f" [{context}]"
        lines.append(f"{diagnostic['severity'].upper()} {diagnostic['code']} {location}: {diagnostic['message']}")
        if diagnostic["expected"] is not None:
            lines.append(f"  Expected: {diagnostic['expected']}")
        if diagnostic["observed"] is not None:
            lines.append(f"  Observed: {diagnostic['observed']}")
        lines.append(f"  Next: {diagnostic['suggestion']}")
        if diagnostic["related"]:
            lines.append(f"  Related: {', '.join(diagnostic['related'])}")
    return "\n".join(lines)


def usage_result(message: str, root: str = ".") -> dict[str, Any]:
    diagnostic = Diagnostic(
        code="USAGE_ERROR",
        severity="error",
        file=".",
        line=None,
        record=None,
        field=None,
        message="The validator invocation is invalid.",
        expected="validate_profile.py [--root PATH] [--format json|text]",
        observed=message,
        suggestion="Use only the documented read-only arguments.",
    )
    return {
        "schema_version": 1,
        "valid": None,
        "root": os.path.abspath(os.path.expanduser(root)),
        "format_version": None,
        "summary": {"errors": 1, "warnings": 0, "files_checked": 0, "plans": 0, "work_items": 0, "decisions": 0},
        "diagnostics": [asdict(diagnostic)],
    }


def internal_result(root: str, error: Exception) -> dict[str, Any]:
    diagnostic = Diagnostic(
        code="VALIDATOR_INTERNAL_ERROR",
        severity="error",
        file=".",
        line=None,
        record=None,
        field=None,
        message="The validator failed before it could produce a structural verdict.",
        expected="deterministic read-only validation",
        observed=f"{type(error).__name__}: {error}",
        suggestion="Report the validator failure; do not treat the profile as valid or mutate it to bypass the failure.",
    )
    return {
        "schema_version": 1,
        "valid": None,
        "root": os.path.abspath(os.path.expanduser(root)),
        "format_version": None,
        "summary": {"errors": 1, "warnings": 0, "files_checked": 0, "plans": 0, "work_items": 0, "decisions": 0},
        "diagnostics": [asdict(diagnostic)],
    }


def build_parser() -> Parser:
    parser = Parser(add_help=True, description="Read-only validator for Scoville Plan format_version 1 profiles")
    parser.add_argument("--root", default=".", help="project root containing PROJECT_INDEX.md")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="diagnostic output format")
    return parser


def main(argv: list[str] | None = None) -> int:
    root = "."
    output_format = "json"
    try:
        arguments = build_parser().parse_args(argv)
        root = arguments.root
        output_format = arguments.format
    except UsageError as error:
        result = usage_result(str(error), root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return EXIT_INCOMPLETE

    try:
        result, exit_code = Validator(root).run()
    except Exception as error:  # pragma: no cover - defensive process boundary
        result = internal_result(root, error)
        exit_code = EXIT_INTERNAL
    if output_format == "text":
        print(render_text(result, exit_code))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
