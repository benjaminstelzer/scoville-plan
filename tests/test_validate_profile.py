from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY = Path(__file__).resolve().parent.parent
SCRIPT = REPOSITORY / "scoville-plan" / "scripts" / "validate_profile.py"
FIXTURE = REPOSITORY / "tests" / "fixtures" / "valid-profile"
CONTRACT = REPOSITORY / "tests" / "validator-contract.json"
INVARIANTS = REPOSITORY / "tests" / "profile-invariants.json"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("scoville_plan_validator", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validator module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator_module()


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            snapshot[relative] = f"L:{os.readlink(path)}"
        elif path.is_dir():
            snapshot[relative] = "D"
        else:
            snapshot[relative] = "F:" + hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


class ValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="scoville-validator-")
        self.root = Path(self.temporary.name) / "project"
        shutil.copytree(FIXTURE, self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def path(self, relative: str) -> Path:
        return self.root / Path(relative)

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.path(relative)
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

    def reset_fixture(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)
        shutil.copytree(FIXTURE, self.root)

    def replace_many(self, replacements: list[tuple[str, str, str]]) -> None:
        for relative, old, new in replacements:
            self.replace(relative, old, new)

    def run_json(self, *extra: str, root: Path | None = None, unchanged: bool = True):
        target = root or self.root
        before = tree_snapshot(target) if unchanged and target.exists() else None
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(target), "--format", "json", *extra],
            cwd=REPOSITORY,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        result = json.loads(completed.stdout)
        if before is not None:
            self.assertEqual(before, tree_snapshot(target), "validator changed fixture bytes or paths")
        return completed, result

    @staticmethod
    def codes(result: dict) -> set[str]:
        return {diagnostic["code"] for diagnostic in result["diagnostics"]}

    def assert_code(self, expected: str, *, exit_code: int = 1) -> dict:
        completed, result = self.run_json()
        self.assertEqual(exit_code, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn(expected, self.codes(result))
        return result

    def test_valid_profile_matches_contract_and_is_unchanged(self) -> None:
        completed, result = self.run_json()
        self.assertEqual(0, completed.returncode)
        self.assertTrue(result["valid"])
        self.assertEqual([], result["diagnostics"])
        self.assertEqual({"errors": 0, "warnings": 0, "files_checked": 3, "plans": 1, "work_items": 2, "decisions": 1}, result["summary"])

    def test_text_output_is_available_without_changing_exit_semantics(self) -> None:
        before = tree_snapshot(self.root)
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), "--format", "text"],
            cwd=REPOSITORY,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode)
        self.assertTrue(completed.stdout.startswith("VALID:"))
        self.assertEqual(before, tree_snapshot(self.root))

    def test_contract_declares_every_runtime_code_and_field(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(sorted(VALIDATOR.DIAGNOSTIC_CODES), contract["diagnostic_codes"])
        diagnostic = VALIDATOR.Diagnostic(
            code="STATUS_INVALID",
            severity="error",
            file="file.md",
            line=1,
            record="PLAN-0001",
            field="status",
            message="message",
            expected="expected",
            observed="observed",
            suggestion="suggestion",
        )
        self.assertEqual(contract["diagnostic_fields"], list(diagnostic.__dict__))

    def test_cross_record_invariant_manifest_is_complete(self) -> None:
        manifest = json.loads(INVARIANTS.read_text(encoding="utf-8"))
        self.assertEqual(1, manifest["format_version"])
        declared = {
            code
            for invariant in manifest["invariants"]
            for code in invariant["diagnostic_codes"]
        }
        expected = {
            "DECISION_ACCEPTED_FORBIDDEN",
            "DECISION_ACCEPTED_REQUIRED",
            "DECISION_BATCH_ASYMMETRIC",
            "DECISION_BATCH_HASH_INVALID",
            "DECISION_BATCH_MEMBER_INVALID",
            "DECISION_BATCH_MEMBER_MISSING",
            "DECISION_BATCH_PAIR_REQUIRED",
            "DECISION_PROPOSAL_METADATA_FORBIDDEN",
            "DECISION_SUPERSESSION_ASYMMETRIC",
            "DECISION_SUPERSESSION_CYCLE",
            "DECISION_SUPERSESSION_MISSING",
            "DECISION_SUPERSESSION_STATUS",
            "INDEX_ACTIVE_PLAN_MISSING",
            "INDEX_ACTIVE_PLAN_STATUS",
            "PLAN_COMPLETED_NONTERMINAL",
            "PLAN_CURRENT_ITEM_MISSING",
            "PLAN_CURRENT_ITEM_REQUIRED",
            "PLAN_CURRENT_ITEM_STATUS",
            "PLAN_IN_PROGRESS_COUNT",
            "PLAN_IN_PROGRESS_CURRENT_MISMATCH",
            "PLAN_NONACTIVE_IN_PROGRESS",
            "PROFILE_ACTIVE_PLAN_COUNT",
            "RECORD_ID_DUPLICATE",
            "WORK_CURRENT_DEPENDENCY_NOT_DONE",
            "WORK_DECISION_MISSING",
            "WORK_DEPENDENCY_CANCELLED",
            "WORK_DEPENDENCY_CYCLE",
            "WORK_DEPENDENCY_MISSING",
            "WORK_DEPENDENCY_ORDER",
            "WORK_ITEM_ID_DUPLICATE",
            "WORK_ITEM_MISSING",
            "WORK_NEXT_ACTION_FORBIDDEN",
            "WORK_NEXT_ACTION_REQUIRED",
            "WORK_TERMINAL_BLOCKED",
            "WORK_TERMINAL_EVIDENCE_REQUIRED",
        }
        self.assertEqual(expected, declared)
        test_names = {name for name in dir(self) if name.startswith("test_")}
        for invariant in manifest["invariants"]:
            self.assertIn(invariant["test"], test_names)
            self.assertTrue(invariant["source"])

    def test_json_output_is_byte_deterministic(self) -> None:
        first, _ = self.run_json()
        second, _ = self.run_json()
        self.assertEqual(first.stdout, second.stdout)

    def test_unknown_write_option_is_rejected_without_mutation(self) -> None:
        before = tree_snapshot(self.root)
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), "--repair"],
            cwd=REPOSITORY,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        result = json.loads(completed.stdout)
        self.assertEqual(2, completed.returncode)
        self.assertIsNone(result["valid"])
        self.assertEqual({"USAGE_ERROR"}, self.codes(result))
        self.assertEqual(before, tree_snapshot(self.root))

    def test_local_shape_defects_have_stable_codes(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        decision = "docs/decisions/0001-use-read-only-validation.md"
        cases = [
            (plan, "status: active\ncreated: 2026-08-08", "created: 2026-08-08\nstatus: active", "FRONTMATTER_KEY_ORDER"),
            (plan, "## Goal", "## Purpose", "SECTION_H2_ORDER"),
            (plan, "Status: in_progress\nDepends on: []", "Depends on: []\nStatus: in_progress", "WORK_FIELD_ORDER"),
            (plan, "1. Read the canonical files.", "2. Read the canonical files.", "WORK_STEPS_INVALID"),
            (plan, "Next action: Run the structural validator.", "Next action:", "WORK_NEXT_ACTION_REQUIRED"),
            (decision, "scope: skill/profile-validation", "scope: Skill Profile", "DECISION_SCOPE_INVALID"),
            (decision, "accepted: 2026-08-08\n", "", "DECISION_ACCEPTED_REQUIRED"),
        ]
        for relative, old, new, expected in cases:
            with self.subTest(expected=expected):
                self.reset_fixture()
                self.replace(relative, old, new)
                self.assert_code(expected)

    def test_filename_identity_mismatch_is_reported(self) -> None:
        source = self.path("docs/plans/0001-validate-profile.md")
        source.rename(source.with_name("0002-validate-profile.md"))
        self.assert_code("RECORD_ID_FILENAME_MISMATCH")

    def test_bom_crlf_and_invalid_utf8_are_contract_errors(self) -> None:
        index = self.path("PROJECT_INDEX.md")
        cases = [
            (b"\xef\xbb\xbf" + index.read_bytes(), "FILE_BOM_FORBIDDEN"),
            (index.read_bytes().replace(b"\n", b"\r\n"), "FILE_LINE_ENDING_INVALID"),
            (index.read_bytes() + b"\xff", "FILE_UTF8_INVALID"),
        ]
        for data, expected in cases:
            with self.subTest(expected=expected):
                self.reset_fixture()
                self.path("PROJECT_INDEX.md").write_bytes(data)
                self.assert_code(expected)

    def test_missing_required_path_is_invalid_not_incomplete(self) -> None:
        self.path("PROJECT_INDEX.md").unlink()
        completed, result = self.run_json()
        self.assertEqual(1, completed.returncode)
        self.assertFalse(result["valid"])
        self.assertIn("PROFILE_PATH_MISSING", self.codes(result))

    def test_parent_traversal_is_an_incomplete_inspection(self) -> None:
        traversing = self.root / "docs" / ".."
        completed, result = self.run_json(root=traversing, unchanged=False)
        self.assertEqual(2, completed.returncode)
        self.assertIsNone(result["valid"])
        self.assertEqual({"ROOT_TRAVERSAL"}, self.codes(result))

    def test_missing_root_is_an_incomplete_inspection(self) -> None:
        missing = self.root.parent / "missing"
        completed, result = self.run_json(root=missing, unchanged=False)
        self.assertEqual(2, completed.returncode)
        self.assertIsNone(result["valid"])
        self.assertEqual({"ROOT_MISSING"}, self.codes(result))

    def test_permission_failure_is_an_incomplete_inspection(self) -> None:
        validator = VALIDATOR.Validator(str(self.root))
        real_open = VALIDATOR.os.open

        def denied(path, flags):
            if os.fspath(path).endswith("PROJECT_INDEX.md"):
                raise PermissionError("denied by test")
            return real_open(path, flags)

        with mock.patch.object(VALIDATOR.os, "open", side_effect=denied):
            result, exit_code = validator.run()
        self.assertEqual(2, exit_code)
        self.assertIsNone(result["valid"])
        self.assertIn("FILE_UNREADABLE", self.codes(result))

    def test_concurrent_metadata_change_is_an_incomplete_inspection(self) -> None:
        validator = VALIDATOR.Validator(str(self.root))
        real_snapshot = VALIDATOR.Validator._snapshot
        calls = 0

        def changed(info):
            nonlocal calls
            calls += 1
            value = real_snapshot(info)
            if calls == 4:
                return value[:-1] + (value[-1] + 1,)
            return value

        with mock.patch.object(VALIDATOR.Validator, "_snapshot", side_effect=changed):
            result, exit_code = validator.run()
        self.assertEqual(2, exit_code)
        self.assertIsNone(result["valid"])
        self.assertIn("FILE_CHANGED_DURING_READ", self.codes(result))

    def test_reparse_point_flag_is_detected(self) -> None:
        info = SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        self.assertTrue(VALIDATOR.Validator._is_redirect_stat(info))

    def test_reparse_point_root_is_an_incomplete_inspection(self) -> None:
        validator = VALIDATOR.Validator(str(self.root))
        with mock.patch.object(VALIDATOR.Validator, "_is_redirect_stat", return_value=True):
            result, exit_code = validator.run()
        self.assertEqual(2, exit_code)
        self.assertIsNone(result["valid"])
        self.assertEqual({"PATH_REDIRECTED"}, self.codes(result))

    def test_canonical_root_escape_is_an_incomplete_inspection(self) -> None:
        validator = VALIDATOR.Validator(str(self.root))
        outside = self.root.parent / "outside.md"
        self.assertFalse(validator._check_canonical_path(outside))
        result = validator.result()
        self.assertIsNone(result["valid"])
        self.assertEqual({"PATH_ESCAPES_ROOT"}, self.codes(result))

    def test_symlinked_canonical_directory_is_not_followed(self) -> None:
        plans = self.path("docs/plans")
        target = self.root.parent / "outside-plans"
        shutil.copytree(plans, target)
        shutil.rmtree(plans)
        try:
            os.symlink(target, plans, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"directory symlink unavailable: {error}")
        completed, result = self.run_json()
        self.assertEqual(2, completed.returncode)
        self.assertIsNone(result["valid"])
        self.assertIn("PATH_REDIRECTED", self.codes(result))

    def test_index_and_active_plan_relationships(self) -> None:
        self.replace("PROJECT_INDEX.md", "active_plan: PLAN-0001", "active_plan: PLAN-9999")
        result = self.assert_code("INDEX_ACTIVE_PLAN_MISSING")
        self.assertIn("PROFILE_ACTIVE_PLAN_COUNT", self.codes(result))

    def test_current_item_must_exist_and_match_in_progress(self) -> None:
        self.replace("docs/plans/0001-validate-profile.md", "current_item: W-001", "current_item: W-999")
        result = self.assert_code("PLAN_CURRENT_ITEM_MISSING")
        self.assertIn("PLAN_IN_PROGRESS_CURRENT_MISMATCH", self.codes(result))
        suggestions = " ".join(diagnostic["suggestion"] for diagnostic in result["diagnostics"])
        self.assertIn("Ask", suggestions)

    def test_multiple_in_progress_items_are_reported(self) -> None:
        self.replace("docs/plans/0001-validate-profile.md", "Status: todo", "Status: in_progress")
        self.assert_code("PLAN_IN_PROGRESS_COUNT")

    def test_missing_and_later_dependencies_are_reported(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        self.replace(plan, "Depends on: [W-001]", "Depends on: [W-999]")
        self.assert_code("WORK_DEPENDENCY_MISSING")
        self.reset_fixture()
        self.replace(plan, "Depends on: []", "Depends on: [W-002]")
        result = self.assert_code("WORK_DEPENDENCY_ORDER")
        self.assertIn("WORK_DEPENDENCY_CYCLE", self.codes(result))

    def test_cancelled_dependency_never_satisfies_current_work(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        self.replace(plan, "current_item: W-001", "current_item: W-002")
        self.replace(plan, "Status: in_progress", "Status: cancelled")
        self.replace(plan, "Evidence: []\nNext action: Run the structural validator.", "Evidence: [cancelled by user]")
        result = self.assert_code("WORK_DEPENDENCY_CANCELLED")
        self.assertIn("WORK_CURRENT_DEPENDENCY_NOT_DONE", self.codes(result))

    def test_missing_decision_reference_is_reported(self) -> None:
        self.path("docs/decisions/0001-use-read-only-validation.md").unlink()
        self.assert_code("WORK_DECISION_MISSING")

    def decision_text(self, decision_id: str, status: str, extra: list[str]) -> str:
        number = decision_id.split("-")[1]
        accepted = ["accepted: 2026-08-08"] if status in {"accepted", "deprecated", "superseded"} else []
        frontmatter = [
            "---",
            "format_version: 1",
            f"id: {decision_id}",
            f"status: {status}",
            "created: 2026-08-08",
            *accepted,
            "scope: skill/profile-validation",
            *extra,
            "---",
        ]
        body = [
            "",
            f"# Decision {number}",
            "",
            "## Decision",
            "",
            "Choose the recorded result.",
            "",
            "## Problem",
            "",
            "A structural choice is required.",
            "",
            "## Drivers",
            "",
            "- Preserve native ownership.",
            "",
            "## Considered alternatives",
            "",
            "- Keep the prior choice.",
            "- Use the replacement.",
            "",
            "## Consequences",
            "",
            "The relationship is explicit.",
            "",
            "## Confirmation",
            "",
            "Inspect the resulting records.",
            "",
            "## Revisit when",
            "",
            "Revisit when requirements change.",
            "",
        ]
        return "\n".join(frontmatter + body)

    def add_decision(self, decision_id: str, status: str, extra: list[str]) -> Path:
        number = decision_id.split("-")[1]
        path = self.path(f"docs/decisions/{number}-decision-{number}.md")
        path.write_text(self.decision_text(decision_id, status, extra), encoding="utf-8", newline="\n")
        return path

    def test_supersession_must_be_reciprocal(self) -> None:
        self.add_decision("ADR-0002", "accepted", ["supersedes: ADR-0001"])
        self.assert_code("DECISION_SUPERSESSION_ASYMMETRIC")

    def test_cross_record_invariants_have_isolated_fixtures(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        decision = "docs/decisions/0001-use-read-only-validation.md"
        batch = "c" * 64

        cases = [
            (
                "idle index with active Plan",
                [("PROJECT_INDEX.md", "active_plan: PLAN-0001", "active_plan: null")],
                "PROFILE_ACTIVE_PLAN_COUNT",
            ),
            (
                "index targets non-active Plan",
                [(plan, "status: active", "status: draft")],
                "INDEX_ACTIVE_PLAN_STATUS",
            ),
            (
                "active Plan lacks current item",
                [(plan, "current_item: W-001\n", "")],
                "PLAN_CURRENT_ITEM_REQUIRED",
            ),
            (
                "current item is terminal",
                [
                    (plan, "Status: in_progress", "Status: done"),
                    (plan, "Evidence: []\nNext action: Run the structural validator.", "Evidence: [validator exit 0]"),
                ],
                "PLAN_CURRENT_ITEM_STATUS",
            ),
            (
                "in-progress item differs from current item",
                [(plan, "current_item: W-001", "current_item: W-002")],
                "PLAN_IN_PROGRESS_CURRENT_MISMATCH",
            ),
            (
                "multiple in-progress items",
                [(plan, "Status: todo", "Status: in_progress")],
                "PLAN_IN_PROGRESS_COUNT",
            ),
            (
                "non-active Plan retains in-progress work",
                [(plan, "status: active", "status: draft"), (plan, "current_item: W-001\n", "")],
                "PLAN_NONACTIVE_IN_PROGRESS",
            ),
            (
                "completed Plan contains live work",
                [(plan, "status: active", "status: completed"), (plan, "current_item: W-001\n", "")],
                "PLAN_COMPLETED_NONTERMINAL",
            ),
            (
                "current item depends on non-done work",
                [
                    (plan, "current_item: W-001", "current_item: W-002"),
                    (plan, "Status: in_progress", "Status: todo"),
                ],
                "WORK_CURRENT_DEPENDENCY_NOT_DONE",
            ),
            (
                "dependency record is absent",
                [(plan, "Depends on: [W-001]", "Depends on: [W-999]")],
                "WORK_DEPENDENCY_MISSING",
            ),
            (
                "dependency follows dependent",
                [(plan, "Depends on: []", "Depends on: [W-002]")],
                "WORK_DEPENDENCY_ORDER",
            ),
            (
                "dependency graph cycles",
                [(plan, "Depends on: []", "Depends on: [W-002]")],
                "WORK_DEPENDENCY_CYCLE",
            ),
            (
                "cancelled work is a dependency",
                [
                    (plan, "Status: in_progress", "Status: cancelled"),
                    (plan, "Evidence: []\nNext action: Run the structural validator.", "Evidence: [cancelled by user]"),
                ],
                "WORK_DEPENDENCY_CANCELLED",
            ),
            (
                "terminal Work Item lacks Evidence",
                [
                    (plan, "current_item: W-001", "current_item: W-002"),
                    (plan, "Status: in_progress", "Status: done"),
                    (plan, "Next action: Run the structural validator.\n", ""),
                ],
                "WORK_TERMINAL_EVIDENCE_REQUIRED",
            ),
            (
                "terminal Work Item retains a blocker",
                [
                    (plan, "current_item: W-001", "current_item: W-002"),
                    (plan, "Status: in_progress", "Status: done"),
                    (plan, "Blocked by: []", "Blocked by: [EXT-1]"),
                    (plan, "Evidence: []\nNext action: Run the structural validator.", "Evidence: [validator exit 0]"),
                ],
                "WORK_TERMINAL_BLOCKED",
            ),
            (
                "terminal Work Item retains Next action",
                [
                    (plan, "current_item: W-001", "current_item: W-002"),
                    (plan, "Status: in_progress", "Status: done"),
                    (plan, "Evidence: []", "Evidence: [validator exit 0]"),
                ],
                "WORK_NEXT_ACTION_FORBIDDEN",
            ),
            (
                "non-terminal Work Item lacks Next action",
                [(plan, "Next action: Run the structural validator.\n", "")],
                "WORK_NEXT_ACTION_REQUIRED",
            ),
            (
                "Work Item Decision is absent",
                [(plan, "Decisions: [ADR-0001]", "Decisions: [ADR-9999]")],
                "WORK_DECISION_MISSING",
            ),
            (
                "accepted lifecycle date is absent",
                [(decision, "accepted: 2026-08-08\n", "")],
                "DECISION_ACCEPTED_REQUIRED",
            ),
            (
                "rejected Decision retains acceptance date",
                [(decision, "status: accepted", "status: rejected")],
                "DECISION_ACCEPTED_FORBIDDEN",
            ),
            (
                "proposal carries transition metadata",
                [
                    (decision, "status: accepted", "status: proposed"),
                    (decision, "scope: skill/profile-validation", "scope: skill/profile-validation\nsupersedes: ADR-9999"),
                ],
                "DECISION_PROPOSAL_METADATA_FORBIDDEN",
            ),
            (
                "superseded Decision lacks replacement",
                [(decision, "status: accepted", "status: superseded")],
                "DECISION_SUPERSESSION_MISSING",
            ),
            (
                "supersession target is absent",
                [(decision, "scope: skill/profile-validation", "scope: skill/profile-validation\nsupersedes: ADR-9999")],
                "DECISION_SUPERSESSION_MISSING",
            ),
            (
                "supersession relation is asymmetric",
                [(decision, "scope: skill/profile-validation", "scope: skill/profile-validation\nsuperseded_by: ADR-0002")],
                "DECISION_SUPERSESSION_STATUS",
            ),
            (
                "batch pair is incomplete",
                [(decision, "scope: skill/profile-validation", f"scope: skill/profile-validation\ntransition_batch: {batch}")],
                "DECISION_BATCH_PAIR_REQUIRED",
            ),
            (
                "batch omits its own Decision",
                [
                    (
                        decision,
                        "scope: skill/profile-validation",
                        f"scope: skill/profile-validation\ntransition_batch: {batch}\ntransition_batch_members: [ADR-0002]",
                    )
                ],
                "DECISION_BATCH_MEMBER_INVALID",
            ),
            (
                "batch member record is absent",
                [
                    (
                        decision,
                        "scope: skill/profile-validation",
                        f"scope: skill/profile-validation\ntransition_batch: {batch}\ntransition_batch_members: [ADR-0001, ADR-0002]",
                    )
                ],
                "DECISION_BATCH_MEMBER_MISSING",
            ),
            (
                "batch hash shape is invalid",
                [
                    (
                        decision,
                        "scope: skill/profile-validation",
                        "scope: skill/profile-validation\ntransition_batch: bad\ntransition_batch_members: [ADR-0001]",
                    )
                ],
                "DECISION_BATCH_HASH_INVALID",
            ),
        ]

        for name, replacements, expected in cases:
            with self.subTest(invariant=name):
                self.reset_fixture()
                self.replace_many(replacements)
                result = self.assert_code(expected)
                matching = [item for item in result["diagnostics"] if item["code"] == expected]
                self.assertTrue(matching)
                self.assertTrue(all(item["suggestion"].strip() for item in matching))

    def test_relationship_invariants_have_isolated_fixtures(self) -> None:
        decision = "docs/decisions/0001-use-read-only-validation.md"
        plan = "docs/plans/0001-validate-profile.md"
        batch = "d" * 64

        def multiple_active_plans() -> None:
            source = self.path(plan).read_text(encoding="utf-8")
            second = source.replace("PLAN-0001", "PLAN-0002")
            self.path("docs/plans/0002-second-plan.md").write_text(second, encoding="utf-8", newline="\n")

        def asymmetric_supersession() -> None:
            self.add_decision("ADR-0002", "accepted", ["supersedes: ADR-0001"])

        def cyclic_supersession() -> None:
            self.replace_many(
                [
                    (decision, "status: accepted", "status: superseded"),
                    (
                        decision,
                        "scope: skill/profile-validation",
                        "scope: skill/profile-validation\nsupersedes: ADR-0002\nsuperseded_by: ADR-0002",
                    ),
                ]
            )
            self.add_decision(
                "ADR-0002",
                "superseded",
                ["supersedes: ADR-0001", "superseded_by: ADR-0001"],
            )

        def asymmetric_batch() -> None:
            self.replace(
                decision,
                "scope: skill/profile-validation",
                f"scope: skill/profile-validation\ntransition_batch: {batch}\ntransition_batch_members: [ADR-0001, ADR-0002]",
            )
            self.add_decision(
                "ADR-0002",
                "rejected",
                [f"transition_batch: {batch}", "transition_batch_members: [ADR-0002, ADR-0001]"],
            )

        def duplicate_plan_identity() -> None:
            shutil.copyfile(self.path(plan), self.path("docs/plans/0002-duplicate-plan.md"))

        def missing_work_items() -> None:
            path = self.path(plan)
            text = path.read_text(encoding="utf-8")
            path.write_text(text[: text.index("### W-001")], encoding="utf-8", newline="\n")

        def duplicate_work_item_identity() -> None:
            self.replace(plan, "### W-002 Validate relationships", "### W-001 Validate relationships")

        cases = [
            ("more than one active Plan", multiple_active_plans, "PROFILE_ACTIVE_PLAN_COUNT"),
            ("supersession is not reciprocal", asymmetric_supersession, "DECISION_SUPERSESSION_ASYMMETRIC"),
            ("supersession graph cycles", cyclic_supersession, "DECISION_SUPERSESSION_CYCLE"),
            ("Decision batch metadata differs by member", asymmetric_batch, "DECISION_BATCH_ASYMMETRIC"),
            ("record identity collision", duplicate_plan_identity, "RECORD_ID_DUPLICATE"),
            ("Plan contains no Work Item", missing_work_items, "WORK_ITEM_MISSING"),
            ("Plan repeats a Work Item ID", duplicate_work_item_identity, "WORK_ITEM_ID_DUPLICATE"),
        ]

        for name, arrange, expected in cases:
            with self.subTest(invariant=name):
                self.reset_fixture()
                arrange()
                result = self.assert_code(expected)
                matching = [item for item in result["diagnostics"] if item["code"] == expected]
                self.assertTrue(matching)
                self.assertTrue(all(item["suggestion"].strip() for item in matching))

    def test_supported_positive_lifecycle_states_are_valid(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        for status in ("todo", "paused"):
            with self.subTest(current_status=status):
                self.reset_fixture()
                self.replace(plan, "Status: in_progress", f"Status: {status}")
                completed, result = self.run_json()
                self.assertEqual(0, completed.returncode, completed.stdout)
                self.assertTrue(result["valid"])

        self.reset_fixture()
        self.replace_many(
            [
                ("PROJECT_INDEX.md", "active_plan: PLAN-0001", "active_plan: null"),
                (plan, "status: active", "status: completed"),
                (plan, "current_item: W-001\n", ""),
                (plan, "Status: in_progress", "Status: done"),
                (plan, "Evidence: []\nNext action: Run the structural validator.", "Evidence: [local validation passed]"),
                (plan, "Status: todo", "Status: done"),
                (plan, "Evidence: []\nNext action: Wait for W-001 acceptance evidence.", "Evidence: [graph validation passed]"),
            ]
        )
        completed, result = self.run_json()
        self.assertEqual(0, completed.returncode, completed.stdout)
        self.assertTrue(result["valid"])

    def test_ambiguous_lifecycle_diagnostics_require_human_direction(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        self.replace(plan, "current_item: W-001", "current_item: W-999")
        _, result = self.run_json()
        ambiguous = {
            "PLAN_CURRENT_ITEM_MISSING",
            "PLAN_IN_PROGRESS_CURRENT_MISMATCH",
        }
        matching = [item for item in result["diagnostics"] if item["code"] in ambiguous]
        self.assertEqual(ambiguous, {item["code"] for item in matching})
        self.assertTrue(all("ask" in item["suggestion"].lower() for item in matching))

    def test_invalid_multi_defect_output_is_deterministic_and_deduplicated(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        self.replace_many(
            [
                (plan, "current_item: W-001", "current_item: W-999"),
                (plan, "Depends on: [W-001]", "Depends on: [W-999]"),
            ]
        )
        first, first_result = self.run_json()
        second, second_result = self.run_json()
        self.assertEqual(1, first.returncode)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_result, second_result)
        diagnostic_keys = [
            (
                item["code"],
                item["file"],
                item["line"],
                item["record"],
                item["field"],
                item["observed"],
            )
            for item in first_result["diagnostics"]
        ]
        self.assertEqual(len(diagnostic_keys), len(set(diagnostic_keys)))

    def test_replacement_decision_must_have_entered_accepted_lifecycle(self) -> None:
        decision = "docs/decisions/0001-use-read-only-validation.md"
        self.replace_many(
            [
                (decision, "status: accepted", "status: superseded"),
                (decision, "scope: skill/profile-validation", "scope: skill/profile-validation\nsuperseded_by: ADR-0002"),
            ]
        )
        self.add_decision("ADR-0002", "rejected", ["supersedes: ADR-0001"])
        self.assert_code("DECISION_SUPERSESSION_STATUS")

    def test_batch_membership_must_be_complete_and_symmetric(self) -> None:
        batch = "a" * 64
        decision = "docs/decisions/0001-use-read-only-validation.md"
        self.replace(
            decision,
            "scope: skill/profile-validation",
            f"scope: skill/profile-validation\ntransition_batch: {batch}\ntransition_batch_members: [ADR-0001, ADR-0002]",
        )
        self.assert_code("DECISION_BATCH_MEMBER_MISSING")

    def test_valid_batch_checks_shape_and_symmetry_without_recomputing_hash(self) -> None:
        batch = "b" * 64
        decision = "docs/decisions/0001-use-read-only-validation.md"
        self.replace(
            decision,
            "scope: skill/profile-validation",
            f"scope: skill/profile-validation\ntransition_batch: {batch}\ntransition_batch_members: [ADR-0001, ADR-0002]",
        )
        self.add_decision(
            "ADR-0002",
            "rejected",
            [f"transition_batch: {batch}", "transition_batch_members: [ADR-0001, ADR-0002]"],
        )
        completed, result = self.run_json()
        self.assertEqual(0, completed.returncode, completed.stdout)
        self.assertTrue(result["valid"])

    def test_invalid_batch_hash_shape_is_reported(self) -> None:
        decision = "docs/decisions/0001-use-read-only-validation.md"
        self.replace(
            decision,
            "scope: skill/profile-validation",
            "scope: skill/profile-validation\ntransition_batch: not-a-hash\ntransition_batch_members: [ADR-0001]",
        )
        self.assert_code("DECISION_BATCH_HASH_INVALID")

    def test_duplicate_record_ids_are_reported(self) -> None:
        duplicate = self.path("docs/plans/0002-duplicate-plan.md")
        shutil.copyfile(self.path("docs/plans/0001-validate-profile.md"), duplicate)
        result = self.assert_code("RECORD_ID_DUPLICATE")
        self.assertIn("RECORD_ID_FILENAME_MISMATCH", self.codes(result))

    def test_diagnostics_use_total_order_and_have_all_fields(self) -> None:
        plan = "docs/plans/0001-validate-profile.md"
        self.replace(plan, "Status: in_progress", "Status: broken")
        completed, result = self.run_json()
        self.assertEqual(1, completed.returncode)
        diagnostics = result["diagnostics"]
        keys = [
            (
                item["file"],
                item["line"] is None,
                item["line"] or 0,
                item["record"] or "",
                item["field"] or "",
                item["code"],
                item["observed"] or "",
                item["message"],
            )
            for item in diagnostics
        ]
        self.assertEqual(sorted(keys), keys)
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for diagnostic in diagnostics:
            self.assertEqual(contract["diagnostic_fields"], list(diagnostic))


if __name__ == "__main__":
    unittest.main()
