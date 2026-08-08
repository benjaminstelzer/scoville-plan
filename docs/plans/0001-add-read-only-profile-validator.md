---
format_version: 1
id: PLAN-0001
status: completed
created: 2026-08-08
updated: 2026-08-08
---

# Add a read-only native profile validator

## Goal

Bundle an optional deterministic Python validator that checks the complete
Scoville Plan `format_version: 1` profile without changing any bytes. It must
validate local file shape, cross-record relationships, and lifecycle
invariants, then return diagnostics an agent can use to plan a correction.

The primary JSON result contains `schema_version`, `valid`, `root`, detected
`format_version`, a count summary, and an ordered `diagnostics` array. Each
diagnostic contains a stable `code`, `severity`, repository-relative `file`,
best available `line`, `record`, `field`, concise `message`, `expected`,
`observed`, safe `suggestion`, and any `related` records. Output order is
the total key `(file, line-is-absent, line-or-zero, record-or-empty,
field-or-empty, code, canonical-observed, message)`; diagnostics without a line
sort after located diagnostics in the same file, and duplicate root causes are
suppressed.

Suggestions may state an exact correction only for an unambiguous structural
defect. When correction would select intent, evidence, authority, lifecycle,
scope, or a successor, the diagnostic instead names the conflict and tells the
agent which human choice is required. Severity is `error` or `warning`; warnings
never change validity or the exit code. A complete inspection with no errors
returns `valid: true` and exit `0`, while a complete inspection with contract
errors returns `valid: false` and exit `1`. Missing required profile files,
invalid UTF-8, a BOM, and invalid line endings are contract errors. Permission,
I/O, or concurrent-byte failures return `valid: null`, an error diagnostic, and
exit `2` because no structural verdict is possible. An unexpected validator
failure returns `valid: null`, an internal-error diagnostic, and exit `3`.

Before opening canonical files, resolve the project root and every candidate
path without following symlinks, junctions, reparse-point redirects, traversal,
or any target outside the immutable root. An unsafe or redirected canonical
path is an incomplete inspection with `valid: null` and exit `2`, never a valid
profile result.

## Non-goals

- Do not add repair, formatting, normalization, migration, ID allocation, or
  lifecycle-transition commands.
- Do not create a general Scoville Plan CLI, daemon, MCP server, database,
  network call, hidden state, or second project-knowledge owner.
- Do not require the validator or Python for ordinary Scoville Plan use.
- Do not infer human authorization, choose between material alternatives, or
  claim that evidence, acceptance, rationale, or reported work is true.
- Do not change the native `format_version: 1` file contract.
- Do not validate unrelated repository files.

## Work items

### W-001 Deliver deterministic local parsing and diagnostics

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0001]
Outcome: A bundled read-only Python entry point resolves the immutable profile root safely, parses the canonical index, Plan, Work Item, and Decision shapes, and reports stable actionable diagnostics without external services or project writes.
Acceptance: Automated valid, locally malformed, missing-file, unreadable-file, concurrent-change, symlink, junction or reparse-point redirect, traversal, and root-escape fixtures observe the documented JSON fields, null-validity behavior, severity and exit mapping, total diagnostic order, precise file and line attribution where available, authority-safe suggestions, no network or third-party runtime dependency, and identical paths and SHA-256 hashes before and after every invocation.
Steps:
1. Define the command arguments, JSON schema, diagnostic taxonomy, severity rules, and exit-code contract.
2. Implement no-follow root and canonical-path resolution, read-consistency checks, and strict UTF-8, BOM, newline, frontmatter, identifier, filename, date, heading, section-order, field-order, inline-list, blocker, Evidence, Steps, and Next-action parsing.
3. Distinguish unambiguous format corrections from lifecycle or authority conflicts that require a human choice.
4. Add table-driven valid, single-defect, partial-read, unsafe-path, and concurrent-change fixtures plus a write-attempt guard and recursive pre/post hash assertion.
Evidence: [python -B -m unittest discover passed 27 validator tests, repository and stable fixture validation returned exit 0, recursive fixture path and SHA-256 snapshots remained identical]

### W-002 Validate graph and lifecycle invariants across the profile

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001]
Outcome: The validator checks the complete proposed profile graph and reports causally useful root diagnostics for index routing, Plan and Work Item state, dependencies, Decision links, supersession, batches, and interrupted multi-file transitions.
Acceptance: A table-driven suite contains at least one isolated fixture for every cross-record invariant owned by the current Plan, Work Item, Decision, batch, and project-lifecycle references; valid profiles exit `0`, invalid profiles exit `1`, multi-defect output remains deterministic and deduplicated, ambiguous lifecycle conflicts never receive an autonomous repair instruction, and all fixture bytes remain unchanged. Batch hashes are checked only for 64-hex shape, one shared identifier, and exact ordered symmetric self-including membership; the validator never claims to recompute a hash derived from unavailable pre-mutation bytes.
Steps:
1. Build an immutable in-memory profile model only after local parsing succeeds far enough to identify records safely.
2. Validate active-plan ownership, current-item and in-progress alignment, dependency order and cycles, terminal-state evidence, blockers, and Decision references.
3. Validate Decision lifecycle fields, reciprocal supersession, verifiable transition-batch shape and membership, incoming Work Item links, ID collisions, and canonical paths without claiming unavailable pre-mutation hash verification.
4. Collapse cascades behind one root diagnostic while retaining related records needed for correction.
Evidence: [profile-invariants.json maps all cross-record rules, 34 validator tests passed, positive todo paused completed and valid batch profiles returned exit 0]

### W-003 Integrate optional validation and prove agent recovery behavior

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: [ADR-0001]
Outcome: Scoville Plan routes agents to the validator only for native profile audits, post-write verification, or diagnosis, explains its evidentiary limit, and preserves complete manual fallback when it cannot run.
Acceptance: The canonical Skill validator, repository link and JSON checks, and focused routing cases pass; a missing-Python case uses the existing manual structural inspection without weakening claims; fresh-agent evaluations use diagnostics to correct representative unambiguous defects through native edits, request human direction for ambiguous lifecycle defects, never invoke a write mode in the validator, and advance `Next action` to evaluator-backed verification after implementation.
Steps:
1. Add the smallest Core and native-editing routing needed to execute the bundled validator without loading its source into context.
2. Document diagnostic interpretation, structural-proof limits, manual fallback, and the ban on validator-authored corrections.
3. Extend static feature contracts, README, changelog, and focused activation, non-activation, and progressive-disclosure cases.
4. Forward-test valid, unambiguous-invalid, ambiguous-invalid, unavailable-Python, partial-read, concurrent-change, redirected-path, root-escape, and adversarial no-write scenarios in isolated repositories.
Evidence: [canonical Skill validator passed source Codex and Claude copies, 36 Python validator tests passed, JSON contracts and relative Markdown links passed, three isolated fresh-agent recovery evaluations passed, local Codex and Claude copies are SHA-256 identical to source]
