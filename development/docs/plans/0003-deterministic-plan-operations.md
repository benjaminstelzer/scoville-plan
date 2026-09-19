---
format_version: 1
id: PLAN-0003
status: completed
created: 2026-09-19
updated: 2026-09-19
---

# Make Plan context and Workflow dispatch token-bounded

## Goal

- Provide a deterministic semantic projection for current Plan work so agents never need to emit complete unrelated records.
- Preserve one-Step dispatch as the default while defining when an explicitly invoked Workflow may bundle adjacent compatible Steps.

## Non-goals

- Change format-version-1 record semantics, lifecycle authority, or retained Markdown ownership merely for compactness.
- Introduce a writing helper, hidden state, a database, daemon, planning service, or private shorthand.
- Make Step bundling implicit, universal, or available without an accepted compatibility Decision.

## Work items

### W-001 Deliver the deterministic read-only Plan selector

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0001, ADR-0002]
Outcome: `scoville-plan/scripts/select_context.py` returns the exact semantic context needed for current or named Work Item recovery without exposing unrelated Plan or Decision bodies.
Acceptance: The selector supports a project root plus current or explicit Work Item ID and emits deterministic JSON containing exactly Plan frontmatter, Goal and Non-goals, the complete selected Work Item, direct-dependency status lines, and complete Decisions referenced by that item. It reads complete source internally, verifies format version and exact section boundaries, rejects ambiguity, path escape, malformed references, and configured output-budget overflow with structured diagnostics, and never truncates or falls back to raw files. Existing bounded operations remain responsible for proposal discovery, relevant dependency Evidence, graph or paused-return inspection, and complete relevant-item reads; they never broaden the selector response. Fixtures include a Plan above one MiB, large Evidence, missing records, malformed boundaries, unrelated Decisions, an unrelated proposal, relevant dependency Evidence, queued and paused successors, and exact Unicode preservation. Existing validator and record tests remain green.
Steps:
1. [route: medium] Implement `scoville-plan/scripts/select_context.py` as a read-only parser over canonical format-version-1 files with deterministic JSON and structured errors.
2. [route: medium] Add focused fixtures and tests under `development/tests/` for current and named selection, dependency and Decision projection, one-MiB isolation, ambiguity, path safety, and output-budget failure.
3. [route: low] Update `scoville-plan/references/read-only.md`, `SKILL.md`, and `README.md` so selection uses the exact selector projection while proposal, preflight, graph, and successor semantics retain separate bounded reads and a bounded manual fallback.
Evidence: [Fourteen selector tests passed including one-MiB isolation exact headings path safety and recovery-only exclusions, Full 66-test repository suite passed after the Astra correction set, Live selector on the active development profile emitted only plan work_item direct_dependencies and decisions, All five JSON contract files parsed successfully, Native profile validator passed with zero errors and warnings after the Astra correction set]

### W-005 Define guarded Workflow Step-bundle compatibility

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0003]
Outcome: Scoville Plan preserves one Step as the default dispatch unit while exposing an explicit compatibility contract for Workflow-owned bundles of adjacent Steps.
Acceptance: Implementation begins only after ADR-0003 is accepted. `scoville-plan/SKILL.md`, `scoville-plan/references/native-work-items.md`, and focused tests state that bundling is available only to an explicitly invoked Workflow with its own accepted Decision, only for adjacent Steps sharing one outcome, owner, authorization, route, workspace, and Acceptance boundary, and never across a changed Decision, external effect, materially higher risk, or independently resumable result. The bundle adds no Plan field, changes no format-version-1 semantics, and leaves Plan order and Acceptance ownership unchanged.
Steps:
1. [route: medium] Resolve ADR-0003 and, only if accepted, update `scoville-plan/SKILL.md` and `scoville-plan/references/native-work-items.md` with the compatibility boundary.
2. [route: medium] Add focused contract tests for compatible adjacency and every mandatory bundle boundary.
3. [route: low] Document the unchanged default and explicit Workflow-only exception in `README.md` and `CHANGELOG.md`.
Evidence: [Accepted ADR-0003 is reflected in SKILL.md and native-work-items.md with one-Step default behavior and guarded bundle boundaries, README and CHANGELOG document the public compatibility contract without adding Plan fields, Three focused evaluation cases cover default compatible and boundary behavior, Full 61-test repository suite passed after the contract update, Native profile validator passed with zero errors and warnings]

### W-004 Qualify and publish deterministic Plan selection

Status: done
Depends on: [W-001, W-005]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0003]
Outcome: The read-only selector and accepted Step-bundle compatibility contract are independently reviewed, installed, and published for downstream real-project observation with preserved recovery behavior.
Acceptance: The full repository suite, native profile validator, selector large-Plan fixtures, Step compatibility fixtures, cold-start recovery cases, repository-structure checks, and an independent review pass succeed. The canonical package and local installation match by relative path and SHA-256, the public release documents the read-only selector boundary and unchanged default dispatch behavior, and remote state matches the reviewed commit. Practical token impact remains owned by the downstream Workflow real-project observation rather than a synthetic token benchmark in this Plan.
Steps:
1. [route: medium] Run the complete selector, Step compatibility, recovery, validator, and repository-structure suite on the final tree.
2. [route: medium] Obtain an independent review of deterministic projection, dispatch compatibility, and recovery behavior.
3. [route: low] Install the exact reviewed package locally, publish the approved repository update and release, and verify package, tag, release assets, and remote commit parity.
Evidence: [Public 67-test suite passed after the real DIVI boundary fix, Fresh Terra Medium agents used select_context.py for DIVI PLAN-0012 W-003 and EMPCO PLAN-0001 W-290 without raw Plan fallback, Direct selector values and corrected semantic fingerprints matched both Terra reports, Astra High consultation 04 found no material issue in both Skills all Python helpers or the real-project boundary fix, Canonical scoville-plan package and installed package matched 15 files by relative path and SHA-256, Commit 2d0afe397d89929bf325a97f592ab8fc0eaec460 was pushed to public main and annotated tag v1.5.0 peeled to that commit, Published v1.5.0 contained 14 verified assets with matching names sizes and SHA-256 digests, Final publication audit passed with one release one release-version tag complete package structure family alignment and profile alignment]
