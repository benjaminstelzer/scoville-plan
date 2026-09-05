from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY = Path(__file__).resolve().parent.parent
SCRIPT = REPOSITORY.parent / "scoville-plan" / "scripts" / "compute_decision_batch.py"
SPEC = importlib.util.spec_from_file_location("decision_batch", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
batch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = batch
SPEC.loader.exec_module(batch)


def changed_stat(info: os.stat_result, **changes: int) -> SimpleNamespace:
    fields = {
        key: getattr(info, key, 0)
        for key in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
                    "st_mode", "st_file_attributes")
    }
    fields.update(changes)
    return SimpleNamespace(**fields)


class ComputeDecisionBatchCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="scoville-batch-")
        self.workspace = Path(self.temp.name)
        self.root = self.workspace / "project"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, data: bytes = b"fixture\n") -> Path:
        target = self.root.joinpath(*relative.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *arguments],
            cwd=REPOSITORY,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def arguments(self, *transitions: str, transition_date: str = "2026-08-10") -> list[str]:
        result = ["--root", str(self.root), "--date", transition_date]
        for transition in transitions:
            result.extend(("--transition", transition))
        return [*result, "--format", "json"]

    def test_happy_path_hashes_exact_bytes_in_authorized_order_without_mutation(self) -> None:
        first = "docs/decisions/0001-first.md"
        second = "docs/decisions/0002-second.md"
        first_bytes = b"first\n"
        second_bytes = b"second\r\n"
        self.write(first, first_bytes)
        self.write(second, second_bytes)
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*.md")}

        completed = self.run_cli(
            *self.arguments(
                f"ADR-0001:accept:{first}",
                f"ADR-0002:reject:{second}",
            )
        )

        first_hash = hashlib.sha256(first_bytes).hexdigest()
        second_hash = hashlib.sha256(second_bytes).hexdigest()
        payload = (
            "date:2026-08-10\n"
            f"ADR-0001:accept:{first_hash}\n"
            f"ADR-0002:reject:{second_hash}\n"
        ).encode("utf-8")
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(
            {
                "sha256": hashlib.sha256(payload).hexdigest(),
                "members": ["ADR-0001", "ADR-0002"],
                "member_file_sha256": {
                    "ADR-0001": first_hash,
                    "ADR-0002": second_hash,
                },
            },
            json.loads(completed.stdout),
        )
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*.md")}
        self.assertEqual(before, after)

    def test_rejects_parent_traversal(self) -> None:
        completed = self.run_cli(*self.arguments("ADR-0001:accept:../outside.md"))
        self.assertEqual(2, completed.returncode)
        self.assertIn("normalized repository-relative", completed.stderr)

    def test_windows_path_and_descriptor_ctime_may_differ(self) -> None:
        path = self.write("docs/decisions/0001-first.md")
        info = os.lstat(path)
        descriptor_info = changed_stat(info, st_ctime_ns=info.st_ctime_ns + 100)
        transition = batch.parse_transition("ADR-0001:accept:docs/decisions/0001-first.md")
        with mock.patch.object(batch.sys, "platform", "win32"), mock.patch.object(
            batch.os, "fstat", return_value=descriptor_info
        ):
            self.assertEqual(hashlib.sha256(b"fixture\n").hexdigest(), batch.hash_member(self.root, transition))

    def test_posix_cross_api_ctime_change_is_rejected(self) -> None:
        path = self.write("docs/decisions/0001-first.md")
        info = os.lstat(path)
        transition = batch.parse_transition("ADR-0001:accept:docs/decisions/0001-first.md")
        with mock.patch.object(batch.sys, "platform", "linux"), mock.patch.object(
            batch.os, "fstat", return_value=changed_stat(info, st_ctime_ns=info.st_ctime_ns + 100)
        ):
            with self.assertRaisesRegex(batch.CliError, "changed during inspection"):
                batch.hash_member(self.root, transition)

    def test_windows_still_rejects_identity_size_or_mtime_changes(self) -> None:
        path = self.write("docs/decisions/0001-first.md")
        info = os.lstat(path)
        transition = batch.parse_transition("ADR-0001:accept:docs/decisions/0001-first.md")
        for field in ("st_dev", "st_ino", "st_size", "st_mtime_ns"):
            with self.subTest(field=field), mock.patch.object(batch.sys, "platform", "win32"), mock.patch.object(
                batch.os, "fstat", return_value=changed_stat(info, **{field: getattr(info, field) + 1})
            ):
                with self.assertRaisesRegex(batch.CliError, "changed during inspection"):
                    batch.hash_member(self.root, transition)

    def test_windows_rejects_descriptor_ctime_change_during_read(self) -> None:
        path = self.write("docs/decisions/0001-first.md")
        info = os.lstat(path)
        transition = batch.parse_transition("ADR-0001:accept:docs/decisions/0001-first.md")
        with mock.patch.object(batch.sys, "platform", "win32"), mock.patch.object(
            batch.os, "fstat", side_effect=[info, changed_stat(info, st_ctime_ns=info.st_ctime_ns + 100)]
        ):
            with self.assertRaisesRegex(batch.CliError, "changed during inspection"):
                batch.hash_member(self.root, transition)

    def test_rejects_path_change_after_read(self) -> None:
        path = self.write("docs/decisions/0001-first.md")
        transition = batch.parse_transition("ADR-0001:accept:docs/decisions/0001-first.md")
        real_lstat, real_read = os.lstat, os.read
        read_started = False

        def read(descriptor: int, size: int) -> bytes:
            nonlocal read_started
            read_started = True
            return real_read(descriptor, size)

        def lstat(target: object, *args: object, **kwargs: object) -> object:
            info = real_lstat(target, *args, **kwargs)
            if read_started and Path(target) == path:
                return changed_stat(info, st_ctime_ns=info.st_ctime_ns + 100)
            return info

        with mock.patch.object(batch.os, "read", side_effect=read), mock.patch.object(
            batch.os, "lstat", side_effect=lstat
        ):
            with self.assertRaisesRegex(batch.CliError, "changed during inspection"):
                batch.hash_member(self.root, transition)

    def test_rejects_duplicate_decision_id(self) -> None:
        first = "docs/decisions/0001-first.md"
        second = "docs/decisions/0001-second.md"
        self.write(first)
        self.write(second)
        completed = self.run_cli(
            *self.arguments(
                f"ADR-0001:accept:{first}",
                f"ADR-0001:reject:{second}",
            )
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("duplicate Decision ID", completed.stderr)

    def test_rejects_path_outside_decision_directory(self) -> None:
        path = "docs/plans/0001-example.md"
        self.write(path)
        completed = self.run_cli(*self.arguments(f"ADR-0001:accept:{path}"))
        self.assertEqual(2, completed.returncode)
        self.assertIn("must match docs/decisions/NNNN-kebab-subject.md", completed.stderr)

    def test_rejects_filename_number_that_differs_from_decision_id(self) -> None:
        path = "docs/decisions/0002-example.md"
        self.write(path)
        completed = self.run_cli(*self.arguments(f"ADR-0001:accept:{path}"))
        self.assertEqual(2, completed.returncode)
        self.assertIn("must match the Decision ID", completed.stderr)

    def test_rejects_invalid_date(self) -> None:
        path = "docs/decisions/0001-example.md"
        self.write(path)
        completed = self.run_cli(
            *self.arguments(f"ADR-0001:accept:{path}", transition_date="2026-02-30")
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("actual ISO YYYY-MM-DD", completed.stderr)

    def test_rejects_invalid_action(self) -> None:
        path = "docs/decisions/0001-example.md"
        self.write(path)
        completed = self.run_cli(*self.arguments(f"ADR-0001:approve:{path}"))
        self.assertEqual(2, completed.returncode)
        self.assertIn("must be accept or reject", completed.stderr)

    def test_rejects_missing_file(self) -> None:
        completed = self.run_cli(
            *self.arguments("ADR-0001:accept:docs/decisions/0001-missing.md")
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("does not exist", completed.stderr)

    def test_rejects_symlink_when_supported(self) -> None:
        target = self.write("docs/decisions/0001-target.md")
        link = self.root / "docs" / "decisions" / "0001-link.md"
        try:
            os.symlink(target, link)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"file symlinks are unavailable: {type(error).__name__}")
        completed = self.run_cli(
            *self.arguments("ADR-0001:accept:docs/decisions/0001-link.md")
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("symlink or reparse point", completed.stderr)


if __name__ == "__main__":
    unittest.main()
