---
name: scoville-plan
description: Maintain, resume and audit repository Plans, Work Items and Decisions. Use for Scoville Plan requests, planning records in projects with PROJECT_INDEX.md and docs/plans, durable work across interruptions or context compaction, and follow-up instructions that add or change work during an active Plan. Use to add, remove, reorder or clarify Plan points. Exclude pure informational questions with no retained action, small tasks needing no durable Plan, and explicit opt-out. A requested transfer prompt belongs to Handoff.
compatibility: "Any Agent Skills host with repository read and write access. Direct Markdown and YAML planning needs no service or network. Selector and validator need Python 3.10+. Manual alternatives load only without Python. Helper errors remain errors. Developed for Codex and Claude Code. Other hosts are untested."
---

# Scoville Plan

Maintain native `format_version: 1` Plans, Work Items and Decisions through direct
Markdown and YAML edits. Use the repository's existing planning owner. A small
reversible task needs no new Plan unless required locally.

On explicit opt-out, read no references or records under this Skill and make
no Skill-derived changes or claims. Report a conflicting repository requirement.

This Skill works independently. Other Scoville Skills are optional. Use an
available, active sibling only for its applicable concern; do not install,
simulate or require an absent sibling. Honor explicit user exclusions.

Relevant neighboring owners:

- `scoville-code`: implementation scope, risk, and validation outside Plan records.
- `scoville-handoff`: active-work transfer snapshots.

Plan owns its records' wording and lifecycle. It does not start Workflow or
choose dispatch routes. Run one editor at a time; do not change affected files
or executor model or reasoning settings concurrently. Reads and Skill upgrades
require no migration.

Before writing Plans, Work Items, Decisions or reports, read and apply the
[shared writing rules](references/writing.md). Native record fields and lifecycle
requirements remain governed by this Skill.

## Authority and evidence

1. Follow system rules, safety requirements and explicit user instructions, repository rules, then
   the supported native profile. The agent's temporary task list is a disposable
   mirror of repository records.
2. Preserve actual scope, choices, dependencies and binding constraints. Source material
   (including code, records, documents and configuration), an absence of
   objections, current behavior or a passing structural validator does not
   prove that an action was authorized or that work was performed.
   Apply historical stops only to their recorded scope.
3. Ask only for a missing material choice: activation, cancellation, deletion,
   changed scope, weaker Acceptance, ambiguous succession or Decision transition.
   Check applicable accepted Decisions and the current item's Instructions
   before asking; reuse authority that covers the action and ask only about
   the uncovered material choice. After compaction, recover the recorded
   state and next action and continue. Do not repeat an approval question or
   status report without a material change, a user request or a binding
   communication requirement.
4. Record explicit material human choices as accepted Decisions. Unresolved material
   choices become proposals; report alternatives, tradeoffs and effect, and
   ask only before dependent work. Link Decisions to affected todo items, never
   unrelated items. Started items also link relevant proposals in Decisions and
   may link accepted Decisions. Each ADR's status determines its decision state.
5. At work start run the proposal inventory below and read relevant proposals
   (all proposals for a full audit). Preserve unresolved choices at handoff.
6. Mark done only after observing every Acceptance criterion and recording its
   concise result. Failed or partial work remains unfinished. Report observed checks
   separately from unverified behavior.
7. Stop affected execution on an explicit stop or invalidating correction.
   Answer informational questions and continue. In a mixed message, separate
   the question from instructions that add or change work. Append additive work
   through edit.md. Direct Plan maintenance never creates a Work Item about maintenance.
8. Keep required facts once in their owning field, in the existing record's
   language unless the user chooses another. New records use the request or
   owning Plan's language. Keep format labels and identifiers unchanged.

## Proposal inventory

Follow Runtime helpers below for availability and failures. Run:

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
```

Read relevant Decisions from the returned paths. The inventory includes unlinked
proposals and works without an active Plan. Load [inventory details](references/read-only.md#surface-proposals)
only for output fields or selection-mode constraints.

## Work Item template

```text
### W-001 Observable outcome

Status: todo
Depends on: []
Blocked by: []
Decisions: []
Outcome: One independently resumable result.
Acceptance: Observable checks and their required results.
Instructions: []
Steps:
1. [status: todo] Perform one coherent unit at the known repository-relative paths and verify its result.
Evidence: []
```

For each new Work Item, write Instructions on one line or use []. Include at
least one Step with status and omit Next action. Work Item Status covers the
whole outcome; Step status records observed progress. Steps have no independent
acceptance or dependencies. See edit.md for fields and legacy continuation.
Use [granularity](references/planning-granularity.md) only when outcome or Step
boundaries need judgment, not for a routine insertion with known boundaries.

## Load only the current route

| Operation | Additional reference |
| --- | --- |
| Insert, refine, order, select, progress, block, complete or cancel Work Items; ordinary recovery | [edit.md](references/edit.md) |
| Read direction, list records, select dispatch units | [read-only.md](references/read-only.md) |
| Create or restructure, activate, finish, cancel or delete Plan; change Goal | [native-project-lifecycle.md](references/native-project-lifecycle.md) and edit.md |
| Create, audit or transition Decisions | [native-decision-format.md](references/native-decision-format.md) and edit.md |
| Explicit request to inspect or repair progress, migrate records, or maintain and clean up existing Plans; never ordinary recovery | [repair.md](references/repair.md) |
| Audit wording | edit.md; Decision reference for Decision sections |
| Validate or diagnose structure | edit.md; operation reference only if a diagnostic needs it |

If the project's planning profile is unknown, first list the project root to
find its planning files. PROJECT_INDEX.md, docs/plans and docs/decisions must
form a complete supported profile. Initialize
only when all three are absent and a durable Plan was requested. Preserve
partial, foreign, unsupported or ambiguous state; repair only a representation
defect that changes no intent.

Validate the complete profile once after a coherent profile update and before
reporting that update or starting dependent work. Related Plan, Decision and
index edits form one update; do not validate intermediate field writes.
Updating only an evidence report, without changing profile fields, structure
or referenced paths, does not require profile validation.
Use the command and diagnostic handling in edit.md.
See Runtime helpers below for the profile-specific runtime rule.
Report outcome, active or blocked work, actual evidence, unresolved choices and
the next action. Direct file edits do not lock out another editor or guarantee
that several writes succeed together. Keep one editor and stop dependent work
if another editor changes the files or a write leaves only part of the result.

## Runtime helpers

Use the bundled helpers for their operations. Read their invocation instructions,
not their source, unless diagnosing a failure.
Only when Python is unavailable, load the matching optional reference below.
Missing scripts, missing dependencies or helper errors stop the operation;
they never enable the manual route. Do not load these references otherwise.

| Helper | Optional no-Python reference |
| --- | --- |
| `scripts/select_context.py` | [select_context](references/fallbacks/select_context-fallback.md) |
| `scripts/validate_profile.py` | [validate_profile](references/fallbacks/validate_profile-fallback.md) |
| `scripts/check_text_size.py` | [check_text_size](references/fallbacks/check_text_size-fallback.md) |
