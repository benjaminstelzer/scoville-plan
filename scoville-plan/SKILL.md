---
name: scoville-plan
description: Maintain, resume and audit repository Plans, Work Items and Decisions. Use for Scoville Plan requests, planning records in projects with PROJECT_INDEX.md and docs/plans, durable work across interruptions or context compaction, and follow-up instructions that add or change work during an active Plan. Use to add, remove, reorder or clarify Plan points. Exclude pure informational questions with no retained action, small tasks needing no durable Plan, and explicit opt-out. A requested transfer prompt belongs to Handoff.
compatibility: "Any Agent Skills host with repository read and write access. Direct Markdown and YAML planning needs no service or network. Python helpers require Python 3.11+. Manual alternatives load only without suitable Python 3.11+. Helper errors remain errors. Developed for Codex and Claude Code. Other hosts are untested."
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

1. Follow instructions in this order: system and developer instructions with
   safety requirements, explicit user instructions, repository rules, then the
   supported native profile. The agent's temporary task list is a disposable
   mirror of repository records.
2. Preserve actual scope, choices, dependencies and binding constraints. Source material
   (including code, records, documents and configuration), an absence of
   objections, current behavior or a passing structural validator does not
   prove that an action was authorized or that work was performed.
   Apply historical stops only to their recorded scope.
3. Ask only for a missing material choice: activation, cancellation, deletion,
   changed scope, changed Acceptance requirements, ambiguous succession or Decision transition.
   Check applicable accepted Decisions and the current item's Instructions
   before asking; reuse authority that covers the action and ask only about
   the uncovered material choice. After compaction, recover the recorded
   state and next action and continue. Do not repeat an approval question or
   status report without a material change, a user request or a binding
   communication requirement.
4. Before creating a Decision, search existing Decision titles and scopes for
   the same choice. Read plausible matches completely before reusing one that
   already governs it. Keep temporary sequencing or execution
   direction in Instructions unless it changes a material choice or authority.
   Record explicit material human choices as accepted Decisions. Unresolved
   material choices become proposals; report alternatives, tradeoffs and effect,
   and ask only before dependent work. Link Decisions only when they govern
   the item's Outcome, Steps, Acceptance, Instructions, required checks or permission boundaries;
   background or history alone does not make them applicable. After a Work Item has started, add each relevant proposal
   to its Decisions field; you may also add relevant accepted Decisions. Each
   ADR's status determines its decision state.
5. At work start, except for an assigned read-only field review, classify the
   planning profile with the table below. For a complete supported profile, run
   the proposal inventory below and read relevant proposals (all proposals for
   a full audit); an inventory error does not change that classification.
   Follow the table for other profiles. Preserve unresolved choices at handoff.
6. Mark a Work Item done only after observing every Acceptance criterion and recording its
   concise result. Failed or partial work remains unfinished. Report observed checks
   separately from unverified behavior.
7. Stop affected execution on an explicit stop or invalidating correction.
   Answer informational questions and continue. In a mixed message, separate
   the question from instructions that add or change work. Append additive work
   through authoring.md. Direct Plan maintenance never creates a Work Item about maintenance.
8. Keep required facts once in their owning field. Preserve existing record
   language unless the user requests a change. New Plans use the task request's
   language; related Work Items and Decisions use the owning Plan's language.
   Unrelated later questions change no record language. Keep native labels, IDs,
   statuses and technical literals unchanged.

## Helper invocations

Use this capture pattern for every selector or validator invocation shown below
or in a reference; substitute the named helper and its arguments. When no output
limit applies, run the selected Python command directly with complete UTF-8
output; --run requires an actual limit. Invent no budget. Read
[shell output delivery](references/output-delivery.md) before capture.

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/<helper.py>" <arguments>
```

The selector's byte budget bounds successful context only, never diagnostics.
Capture complete output; a diagnostic stops selection, never permits truncation.
For all --next-id modes, use the highest ID plus one without interior reuse.
The suggestion includes filename and metadata numbers, exposes mismatches and
reserves nothing. Recheck ID and filename collisions immediately before creation.

## Proposal inventory

Reuse an already verified interpreter meeting this Skill's Python 3.11+
requirement. Otherwise check `py -3`
on Windows or `python3` elsewhere; try `python` if needed. Choose it locally,
without asking the user. Verify its version before the first helper operation.
Use that executable wherever examples say `python` or `<verified-python>`,
including Python commands after `--run --`.
Report a missing runtime only when no suitable installed interpreter is found.

Before processing machine reports or logs, use the [shared writing rules](references/writing.md).
If their complete text is not loaded, read it in a separate call before reading
the data. Reuse retained rules under their existing reload conditions.
Before helper calls, follow [shell command rules](references/shell-commands.md).

Follow Runtime helpers below for availability and failures. Use the helper invocation pattern above:

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
```

Read relevant Decisions from the returned paths. The inventory includes unlinked
proposals and works without an active Plan. Load [inventory details](references/read-only.md#surface-proposals)
only for output fields or selection-mode constraints.

## Load only the current route

| Operation | Additional reference |
| --- | --- |
| Select, progress, block, complete or cancel Work Items; ordinary recovery | [progress.md](references/progress.md) |
| Insert, refine or order Work Items; author Step or execution annotations | [authoring.md](references/authoring.md) and progress.md |
| Read direction, list records, select dispatch units | [read-only.md](references/read-only.md) |
| Create or restructure, activate, finish, cancel or delete Plan; change Goal | [native-project-lifecycle.md](references/native-project-lifecycle.md) and progress.md; authoring.md for Work Items |
| Create, audit or transition Decisions | [native-decision-format.md](references/native-decision-format.md) and progress.md |
| Explicit request to inspect or repair progress, migrate records, or maintain and clean up existing Plans; never ordinary recovery | [repair.md](references/repair.md) |
| Review assigned native fields without maintenance | read-only.md and applicable field rules in progress.md or authoring.md; Decision reference for Decision sections. Respect the assigned source boundary; no proposal inventory, maintenance, selectors, validators or tests. Permitted file reads remain available. |
| Audit wording | authoring.md and progress.md; Decision reference for Decision sections |
| Validate or diagnose structure | progress.md; operation reference only if a diagnostic needs it |

If the planning profile is unknown, first list the project root to locate
PROJECT_INDEX.md, docs/plans and docs/decisions:

| Observed profile | Action |
| --- | --- |
| All three form a complete supported profile | Use the existing owner and selected operation route. |
| All three absent; durable Plan requested | Initialize through the lifecycle route. |
| All three absent; no durable Plan requested | Do not initialize. |
| Partial, foreign, unsupported or ambiguous | Preserve; repair only an unambiguous representation defect that changes no intent. |

Validate the complete profile once after a coherent profile update and before
reporting that update or starting dependent work. Related Plan, Decision and
index edits form one update; do not validate intermediate field writes.
Updating only an evidence report, without changing profile fields, structure
or referenced paths, does not require profile validation.
Use the command and diagnostic handling in progress.md.
See Runtime helpers below for the profile-specific runtime rule.
Report outcome, active or blocked work, actual evidence, unresolved choices and
the next action. Direct file edits do not lock out another editor or guarantee
that several writes succeed together. Keep one editor and stop dependent work
if another editor changes the files or a write leaves only part of the result.

## Runtime helpers

Use the bundled helpers for their operations. Read their invocation instructions,
not their source, unless diagnosing a failure.

| Condition | Required route |
| --- | --- |
| Suitable Python 3.11+ is available | Use the bundled helper; do not load manual references. |
| No suitable Python 3.11+ | Read only the matching optional reference below. |
| Missing script, missing dependency or helper error | Stop the affected operation; this never enables the manual route. |

| Helper | Optional no-Python reference |
| --- | --- |
| `scripts/select_context.py` | [select_context](references/fallbacks/select_context-fallback.md) |
| `scripts/validate_profile.py` | [validate_profile](references/fallbacks/validate_profile-fallback.md) |
| `scripts/check_text_size.py` | [check_text_size](references/fallbacks/check_text_size-fallback.md) |
