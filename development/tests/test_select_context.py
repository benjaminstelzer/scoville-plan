from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
SCRIPT = REPOSITORY.parent / "scoville-plan" / "scripts" / "select_context.py"


DECISION = """---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-09-19
accepted: 2026-09-19
scope: project/testing
---

# Preserve exact Unicode

## Decision
Keep the value café and the symbol ✓ unchanged.

## Problem
The selector must preserve source text.

## Drivers

- Exact Unicode matters.

## Considered alternatives

- Escape everything: Harder to read.

## Consequences

- JSON remains UTF-8.

## Confirmation
Read the selected record.

## Revisit when
Encoding rules change.
"""


def plan(unrelated_size: int = 0) -> str:
    unrelated = "x" * unrelated_size
    return f"""---
format_version: 1
id: PLAN-0001
status: active
created: 2026-09-19
updated: 2026-09-19
current_item: W-003
---

# Selector fixture

## Goal

Preserve café exactly.

## Non-goals

- Emit unrelated work.

## Work items

### W-001 First dependency

Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: First result.
Acceptance: Observed.
Evidence: [first passed]

### W-002 Second dependency

Status: paused
Depends on: []
Blocked by: []
Decisions: []
Outcome: Second result.
Acceptance: Observed.
Evidence: []
Next action: Resume later.

### W-003 Selected café item

Status: todo
Depends on: [W-001, W-002]
Blocked by: []
Decisions: [ADR-0001]
Outcome: Return ✓ without unrelated bodies.
Acceptance: Exact projection.
Evidence: []
Next action: Run selector.

### W-004 Unrelated large item

Status: todo
Depends on: []
Blocked by: []
Decisions: []
Outcome: {unrelated}
Acceptance: Not selected.
Evidence: []
Next action: Stay absent.
"""


class SelectContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="scoville-selector-")
        self.root = Path(self.temp.name) / "project"
        (self.root / "docs" / "plans").mkdir(parents=True)
        (self.root / "docs" / "decisions").mkdir(parents=True)
        self.write("PROJECT_INDEX.md", "---\nformat_version: 1\nactive_plan: PLAN-0001\n---\n")
        self.write("docs/plans/0001-selector-fixture.md", plan())
        self.write("docs/decisions/0001-preserve-unicode.md", DECISION)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str) -> Path:
        target = self.root.joinpath(*relative.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), *extra, "--format", "json"],
            cwd=REPOSITORY,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_current_selection_emits_only_four_semantic_components(self) -> None:
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        completed = self.run_cli()

        self.assertEqual(0, completed.returncode, completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertEqual(["plan", "work_item", "direct_dependencies", "decisions"], list(payload))
        self.assertEqual(["frontmatter", "goal", "non_goals"], list(payload["plan"]))
        self.assertIn("current_item: W-003", payload["plan"]["frontmatter"])
        self.assertEqual("## Goal\n\nPreserve café exactly.", payload["plan"]["goal"])
        self.assertIn("### W-003 Selected café item", payload["work_item"])
        self.assertNotIn("Unrelated large item", completed.stdout)
        self.assertEqual(
            [
                {"id": "W-001", "status_line": "Status: done"},
                {"id": "W-002", "status_line": "Status: paused"},
            ],
            payload["direct_dependencies"],
        )
        self.assertEqual([DECISION], payload["decisions"])
        self.assertIn("café", completed.stdout)
        self.assertIn("✓", completed.stdout)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_plan_h1_may_immediately_follow_frontmatter(self) -> None:
        source = plan().replace("current_item: W-003\n---\n\n# Selector fixture", "current_item: W-003\n---\n# Selector fixture")
        self.write("docs/plans/0001-selector-fixture.md", source)

        completed = self.run_cli()

        self.assertEqual(0, completed.returncode, completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertIn("### W-003 Selected café item", payload["work_item"])
        self.assertEqual("## Goal\n\nPreserve café exactly.", payload["plan"]["goal"])

    def test_explicit_item_selection(self) -> None:
        completed = self.run_cli("--work-item", "W-001")
        self.assertEqual(0, completed.returncode, completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertIn("### W-001 First dependency", payload["work_item"])
        self.assertEqual([], payload["direct_dependencies"])
        self.assertEqual([], payload["decisions"])

    def test_megabyte_plan_does_not_emit_unrelated_item(self) -> None:
        marker = "UNRELATED-MEGABYTE-MARKER"
        self.write("docs/plans/0001-selector-fixture.md", plan(1_100_000) + marker)
        completed = self.run_cli()
        self.assertEqual(0, completed.returncode, completed.stdout[:500])
        self.assertLess(len(completed.stdout.encode("utf-8")), 10_000)
        self.assertNotIn(marker, completed.stdout)

    def test_recovery_only_state_stays_outside_the_projection(self) -> None:
        proposal = DECISION.replace("id: ADR-0001", "id: ADR-0002").replace(
            "status: accepted\ncreated: 2026-09-19\naccepted: 2026-09-19",
            "status: proposed\ncreated: 2026-09-19",
        ).replace("Preserve exact Unicode", "Choose unrelated recovery behavior")
        source = (
            plan()
            .replace("Evidence: [first passed]", "Evidence: [DEPENDENCY-EVIDENCE-MARKER]")
            .replace("Next action: Resume later.", "Next action: PAUSED-RETURN-MARKER")
            .replace(
                "### W-004 Unrelated large item",
                "### W-004 Deferred after W-003: QUEUED-SUCCESSOR-MARKER",
            )
        )
        self.write("docs/plans/0001-selector-fixture.md", source)
        self.write("docs/decisions/0002-unrelated-proposal.md", proposal)

        completed = self.run_cli()
        self.assertEqual(0, completed.returncode, completed.stdout)
        for excluded in (
            "DEPENDENCY-EVIDENCE-MARKER",
            "PAUSED-RETURN-MARKER",
            "QUEUED-SUCCESSOR-MARKER",
            "ADR-0002",
            "Choose unrelated recovery behavior",
        ):
            self.assertNotIn(excluded, completed.stdout)

    def test_large_dependency_evidence_does_not_expand_projection(self) -> None:
        entries = ", ".join(f"DEPENDENCY-LARGE-{index:03d}-" + ("x" * 150) for index in range(100))
        self.write(
            "docs/plans/0001-selector-fixture.md",
            plan().replace("Evidence: [first passed]", f"Evidence: [{entries}]"),
        )
        completed = self.run_cli()
        self.assertEqual(0, completed.returncode, completed.stdout[:500])
        self.assertLess(len(completed.stdout.encode("utf-8")), 10_000)
        self.assertNotIn("DEPENDENCY-LARGE-099", completed.stdout)

    def test_budget_overflow_returns_structured_diagnostic_without_truncation(self) -> None:
        selected = plan().replace("Outcome: Return ✓ without unrelated bodies.", "Outcome: " + ("é" * 2_000))
        self.write("docs/plans/0001-selector-fixture.md", selected)
        completed = self.run_cli("--max-output-bytes", "512")
        self.assertEqual(1, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertEqual("OUTPUT_BUDGET_EXCEEDED", payload["diagnostics"][0]["code"])
        self.assertNotIn("ééééé", completed.stdout)

    def test_missing_referenced_decision_is_rejected(self) -> None:
        (self.root / "docs" / "decisions" / "0001-preserve-unicode.md").unlink()
        completed = self.run_cli()
        self.assertEqual(1, completed.returncode)
        self.assertEqual("RECORD_RESOLUTION_INVALID", json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_malformed_plan_boundaries_are_rejected(self) -> None:
        self.write("docs/plans/0001-selector-fixture.md", plan().replace("## Non-goals", "## Goal"))
        completed = self.run_cli()
        self.assertEqual(1, completed.returncode)
        self.assertEqual("PLAN_SECTION_BOUNDARY_INVALID", json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_duplicate_and_unknown_headings_are_rejected(self) -> None:
        cases = (
            (
                plan().replace(
                    "Preserve café exactly.",
                    "Preserve café exactly.\n\n## Goal\n\nDuplicate direction.",
                ),
                "PLAN_SECTION_BOUNDARY_INVALID",
            ),
            (
                plan().replace(
                    "Outcome: Return ✓ without unrelated bodies.",
                    "### Notes\n\nOutcome: Return ✓ without unrelated bodies.",
                ),
                "WORK_BOUNDARY_INVALID",
            ),
        )
        for source, code in cases:
            with self.subTest(code=code):
                self.write("docs/plans/0001-selector-fixture.md", source)
                completed = self.run_cli()
                self.assertEqual(1, completed.returncode)
                self.assertEqual(code, json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_invalid_utf8_is_rejected(self) -> None:
        path = self.root / "docs" / "plans" / "0001-selector-fixture.md"
        path.write_bytes(b"\xff")
        completed = self.run_cli()
        self.assertEqual(1, completed.returncode)
        self.assertEqual("FILE_UTF8_INVALID", json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_bom_and_crlf_are_rejected(self) -> None:
        path = self.root / "docs" / "plans" / "0001-selector-fixture.md"
        for data, code in ((b"\xef\xbb\xbf---\n", "FILE_BOM_FORBIDDEN"), (plan().replace("\n", "\r\n").encode(), "FILE_LINE_ENDING_INVALID")):
            with self.subTest(code=code):
                path.write_bytes(data)
                completed = self.run_cli()
                self.assertEqual(1, completed.returncode)
                self.assertEqual(code, json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_symlinked_plan_is_rejected_when_supported(self) -> None:
        path = self.root / "docs" / "plans" / "0001-selector-fixture.md"
        target = self.root / "outside.md"
        target.write_text(plan(), encoding="utf-8", newline="\n")
        path.unlink()
        try:
            os.symlink(target, path)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"file symlinks are unavailable: {type(error).__name__}")
        completed = self.run_cli()
        self.assertEqual(2, completed.returncode)
        self.assertEqual("PATH_REDIRECTED", json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_idle_project_is_rejected(self) -> None:
        self.write("PROJECT_INDEX.md", "---\nformat_version: 1\nactive_plan: null\n---\n")
        completed = self.run_cli()
        self.assertEqual(1, completed.returncode)
        self.assertEqual("ACTIVE_PLAN_MISSING", json.loads(completed.stdout)["diagnostics"][0]["code"])

    def test_invalid_explicit_work_item_is_usage_error(self) -> None:
        completed = self.run_cli("--work-item", "../W-001")
        self.assertEqual(2, completed.returncode)
        self.assertEqual("WORK_ITEM_ID_INVALID", json.loads(completed.stdout)["diagnostics"][0]["code"])


if __name__ == "__main__":
    unittest.main()
