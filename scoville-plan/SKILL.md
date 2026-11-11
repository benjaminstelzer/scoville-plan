---
name: scoville-plan
description: Maintain, resume and audit repository Plans, Work Items and Decisions for Scoville Plan requests, existing planning profiles with PROJECT_INDEX.md and docs/plans, or explicitly requested durable planning across interruptions. Handle changes to active Plan work; exclude informational questions without retained action, small tasks needing no durable Plan, explicit opt-out, and requested transfer prompts, which belong to Handoff.
compatibility: "Any Agent Skills host with repository read and write access. Direct Markdown and YAML planning needs no service or network. Python helpers require Python 3.11+. Manual alternatives load only without suitable Python 3.11+. Helper errors remain errors. Developed for Codex and Claude Code."
---

# Scoville Plan

Maintain native `format_version: 1` Plans, Work Items and Decisions through
direct Markdown and YAML edits, in the repository's existing planning owner. A
small reversible task needs no new Plan unless the repository requires one.

If the user explicitly opts out, leave this Skill out entirely, including its
references and records, and report a repository requirement that conflicts.

This Skill works on its own. Use another Scoville Skill for its concern when
it is installed and active; an absent one is neither installed, imitated nor
required.
A Skill that needs explicit activation stays out until it is activated, and
one the user excluded stays out.

Relevant neighboring owners:

- `scoville-code`: implementation scope, risk, and validation outside Plan records.
- `scoville-handoff`: active-work transfer snapshots.

Plan owns the wording and lifecycle of its records; it does not start
execution or choose dispatch routes. One editor changes the
records at a time, and affected files and the required model and reasoning
settings stay untouched meanwhile, because the files carry no lock and a
concurrent change is lost silently. Reads and Skill upgrades need no migration.

## Authority and evidence

1. Explicit user instructions and repository rules take precedence over this
   profile. The agent's temporary task list is a disposable mirror of the
   repository records.
2. Preserve scope, choices, dependencies and binding constraints. Source
   material, silence, current behavior and structural validity prove neither
   authority nor performed work. A recorded stop applies to its recorded scope,
   not to later or neighboring work.
3. Ask only for a missing material choice: activation, cancellation, deletion,
   changed scope, changed Acceptance requirements, ambiguous succession or a
   Decision transition, and only where applicable accepted Decisions and the
   current item's Instructions leave it open. Appending newly requested work as a todo
   Work Item does not wait for such a choice; authoring.md has the rule. After an interruption or
   compaction, recover and continue under progress.md. Repeat a question or
   status report only for a material change, a user request or a binding
   communication requirement.
4. Before creating a Decision, search existing Decision titles and scopes for
   the same choice, read plausible matches completely and reuse one that
   already governs it, so that one choice has one record. Keep temporary sequencing or execution direction in
   Instructions unless it changes a material choice or authority. Record
   explicit material human choices as accepted Decisions. Unresolved material
   choices become proposals: report their alternatives, tradeoffs and effect
   and ask before the work that depends on them; only that work waits. Link a Decision where it governs
   the item's Outcome, Steps, Acceptance, Instructions, required checks or
   permission boundaries; background or shared history is not a reason to
   link. After a Work Item has started, add each relevant proposal to its
   Decisions field; relevant accepted Decisions may be added too. Each ADR's
   status determines its decision state.
5. At work start, except for an assigned read-only field review, classify the
   planning profile with the table below, or reuse an unchanged classification.
   For a complete supported profile, run the proposal inventory and read the
   relevant proposals (all of them for a full audit); an inventory error does
   not change the classification. Preserve unresolved choices at handoff.
6. Complete a Work Item through progress.md only after observing every
   Acceptance criterion and recording its result, and keep checked behavior
   apart from unverified behavior.
7. An explicit stop or an invalidating correction halts the execution it
   affects. Answer informational questions and continue. In a mixed message,
   separate the question from the instructions that add or change work, and
   append additive work through authoring.md. Maintaining Plan records is not
   itself recorded as a Work Item.
8. Keep each required fact once, in its owning field. Preserve the existing
   record language unless the user requests a change: new Plans use the
   language of the task request, and related Work Items and Decisions use the
   owning Plan's language, whatever language later questions use. Native
   labels, IDs, statuses and technical literals stay unchanged.

## Helper invocations

Selector and validator commands here and in the references run directly with
complete UTF-8 output. Where an actual output limit applies, wrap them in the
capture call from output delivery; `--run` needs that real limit, not an
invented budget.

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/<helper.py>" <arguments>
```

The selector's byte budget bounds successful context only. Diagnostics are
always complete, and a diagnostic means nothing was selected, so read it rather
than cutting the output. For every `--next-id` mode the suggestion is the
highest ID plus one, without reusing interior gaps; it includes filename and
metadata numbers, exposes mismatches and reserves nothing, so recheck ID and
filename collisions directly before creating the record.

## Proposal inventory

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
```

Read relevant Decisions from the returned paths. The inventory includes
unlinked proposals and works without an active Plan and without any Decision
yet. [Inventory details](references/read-only.md#surface-proposals) are needed
only for output fields or selection-mode constraints.

## Load only the current route

| Operation | Reference |
| --- | --- |
| Select, progress, block, complete or cancel Work Items; ordinary recovery | [progress.md](references/progress.md) |
| Insert, refine or order Work Items; author Step or execution annotations | [authoring.md](references/authoring.md) and progress.md |
| Judge Work Item or Step boundaries where they are not obvious | [planning-granularity.md](references/planning-granularity.md) |
| Read direction, list records, select dispatch units | [read-only.md](references/read-only.md) |
| Create or restructure, activate, finish, cancel or delete a Plan; change Goal | [native-project-lifecycle.md](references/native-project-lifecycle.md) and progress.md; authoring.md for Work Items |
| Create, audit or transition Decisions | [native-decision-format.md](references/native-decision-format.md) and progress.md |
| Explicit request to inspect or repair progress, migrate records, or maintain and clean up existing Plans (ordinary recovery uses progress.md) | [repair.md](references/repair.md) |
| Review assigned native fields without maintenance | read-only.md and the applicable field rules in progress.md or authoring.md; the Decision reference for Decision sections. Stay inside the assigned source boundary: file reads only, without proposal inventory, maintenance, selectors, validators or tests. |
| Audit wording | authoring.md and progress.md; the Decision reference for Decision sections |
| Validate or diagnose structure | progress.md; an operation reference only if a diagnostic needs it |

If the planning profile is unknown, list the project root to locate
PROJECT_INDEX.md, docs/plans and docs/decisions. Index and docs/plans alone
are a complete profile without Decisions, since Git stores no empty directory.

| Observed profile | Action |
| --- | --- |
| Complete supported profile | Use the existing owner and the selected operation route. |
| Wholly absent; durable Plan requested | Initialize through the lifecycle route. |
| Wholly absent; no durable Plan requested | Leave it uninitialized. |
| Partial, foreign, unsupported or ambiguous | Preserve it; repair only an unambiguous representation defect that changes no intent. |

Validate the complete profile once after a coherent profile update and before
reporting that update or starting dependent work. Related Plan, Decision and
index edits form one update, validated once and not after intermediate field
writes. An edit confined to an evidence report that changes no profile fields,
structure or referenced paths needs no validation. progress.md has the command, the diagnostic
handling and the safe-write and continuation rules. Report outcome, active or
blocked work, actual evidence, unresolved choices and the next action.

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

## Shared references

Read one when its condition holds. A complete copy already in context from
this build, including one embedded in your assignment, counts as read; read it
again when it is incomplete or uncertain or a reload is requested.

- [Writing](references/writing.md): a plan, decision, instruction, review, handoff or report; a disputed conclusion.
- [Machine data](references/machine-data.md): a test report, log or structured state as a result.
- [Shell commands](references/shell-commands.md): composed text or scripts passed through a shell; quoting, PowerShell encoding, exact bytes or several exit statuses matter.
- [Output delivery](references/output-delivery.md): before a command whose output may exceed the display limit or whose effect or result cannot be repeated; text that must fit a known limit; delivery as a file.
- [Python discovery](references/python-discovery.md): a Python command or bundled helper, no interpreter verified this session.
- [Instruction design](references/instruction-design.md): a reusable instruction, Skill rule or prompt template.
