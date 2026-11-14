---
name: scoville-plan
description: Maintain, resume and audit repository Plans, Work Items and Decisions for Scoville Plan requests, work on an existing Work Item in a planning profile with PROJECT_INDEX.md and docs/plans, or explicitly requested durable planning across interruptions. Handle changes to active Plan work. Exclude work that no Work Item covers, that the user did not ask to plan and that finishes in this session; informational questions without retained action; explicit opt-out; and requested transfer prompts, which belong to Handoff.
compatibility: "Any Agent Skills host with repository read and write access. Direct Markdown and YAML planning needs no service or network. Python helpers require Python 3.11+. Manual alternatives load only without suitable Python 3.11+. Helper errors remain errors. Developed for Codex and Claude Code."
---

# Scoville Plan

Maintain native `format_version: 1` Plans, Work Items and Decisions through
direct Markdown and YAML edits to the repository's existing planning records.
Do work that no Work Item covers, that the user did not ask to plan and that
finishes in this session directly, without a Plan record or helper run, unless
a repository rule requires one. A planning profile alone does not make work
Plan work.

If the user explicitly opts out, use neither this Skill nor its references or
records, and report a repository rule that requires them.

This Skill works on its own. When another Scoville Skill is installed and
active, use it for the concern it owns. Do not install, imitate or require an
absent one.
Do not use a Skill that needs explicit activation before it is activated, or
one the user excluded.

Relevant neighboring owners:

- `scoville-code`: implementation scope, risk, and validation outside Plan records.
- `scoville-handoff`: active-work transfer snapshots.

Plan alone decides the wording of its records and their lifecycle (creation, status changes, deletion); it does not start execution
or choose dispatch routes. One agent edits the records at a time: the files
carry no lock, so a concurrent edit is lost silently.
Reads and Skill upgrades need no migration.

## Authority and evidence

1. Explicit user instructions and repository rules take precedence over this
   Skill. Your temporary task list is a throwaway copy; the records count.
2. Preserve scope (Goal, Non-goals, Outcome), choices (accepted Decisions and the user's explicit choices), dependencies (`Depends on`) and binding constraints (Acceptance, Instructions, repository rules). Source material, silence, current behavior or structural validity (a passing validator or manual inspection) alone proves neither permission nor accepted work; settle a Step of unknown status under progress.md.
   A recorded stop covers only the scope it records, not later or neighboring
   work.
3. Ask only for a missing material choice: activation, cancellation,
   deletion, changed scope, changed Acceptance requirements, an ambiguous
   successor or a Decision transition, and only where the applicable accepted
   Decisions and the current item's Instructions leave it open. New work
   that rule 7 sends to a todo Work Item does not wait for such a choice;
   authoring.md has the rule. After an interruption or compaction, recover
   and continue under progress.md. Repeat a question or status report only
   after a material change, on request or where a rule requires it.
4. Before creating a Decision, search existing Decision titles and scopes for
   the same choice. Read plausible matches completely and reuse one that
   already governs it, so that one choice has one record. Keep temporary
   sequencing or execution direction in Instructions unless it changes a
   material choice or a permission. Record a user's choice between design or
   product alternatives that later work must follow as an accepted Decision;
   lifecycle choices such as activation, cancellation or deletion live in
   status fields. For an unresolved choice, report its alternatives,
   tradeoffs and effect and ask before the work that depends on it; only that
   work waits. Record it as a proposal only when that work stops before the
   user answers. Link a Decision where it governs the
   item's Outcome, Steps, Acceptance, Instructions, required checks or
   permissions, not for background or shared history. After a Work Item has
   started, add each relevant proposal to its Decisions field; relevant
   accepted Decisions may be added too. Read a Decision's state from the
   `status` in its own file.
5. When you start or resume a Work Item, except for an assigned read-only
   field review, classify the planning profile with the table below, or reuse
   an unchanged classification. For a complete supported profile, run the
   proposal inventory and read the relevant proposals (all for a full audit);
   an inventory error does not change the classification.
6. Set a Work Item to done through progress.md only after observing every
   Acceptance criterion; Evidence names what you ran or inspected and what it
   showed.
7. An explicit stop, or a correction that invalidates running work, halts the execution it affects. Answer an informational question and continue. In
   a mixed message, separate the question from the instructions that add or
   change work. Do added work directly, also during a running Work Item, when
   no Work Item covers it, the user did not ask to plan it and it finishes in
   this session, unless a repository rule requires a record. Append it through
   authoring.md only when the user wants it tracked or it will not finish now.
   Create no Work Item for maintaining Plan records.
8. Write each required fact once, in its field: actions in Steps, observations in
   Evidence, live conditions in Instructions. Keep a record's language unless
   the user asks for a change. A new Plan uses the language of the task
   request; its Work Items and Decisions use that Plan's language, whatever
   language later questions use. Field labels, IDs, statuses and technical
   literals stay unchanged.

## Helper invocations

Run the selector and validator commands here and in the references directly,
with complete UTF-8 output. When their output may exceed the display limit,
use output delivery's capture call; pass `--max-output-tokens` only with a
declared token limit, never an invented one:

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" [--max-output-tokens <limit>] [--publish-full --project-root "<project-root>"] --run -- python -X utf8 "<skill-directory>/scripts/<helper.py>" <arguments>
```

The selector's byte budget limits successful context only. A diagnostic is
always complete and means nothing was selected: read it whole. ID allocation:
every `--next-id` mode suggests the highest ID plus one and never reuses an
interior gap. It counts filename and metadata numbers, reports mismatches and
reserves nothing, so recheck ID and filename collisions directly before
creating the record.

## Proposal inventory

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
```

Read relevant Decisions from the returned paths. The inventory includes
unlinked proposals and works without an active Plan and without any Decision
yet. Open [Inventory details](references/read-only.md#surface-proposals) only
for output fields or selection-mode constraints.

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
| Review assigned native fields without maintenance | read-only.md and the applicable field rules in progress.md or authoring.md; the Decision reference for Decision sections. Read the assigned sources only: no proposal inventory, maintenance, selectors, validators or tests. |
| Audit wording | authoring.md and progress.md; the Decision reference for Decision sections |
| Validate or diagnose structure | progress.md; an operation reference only if a diagnostic needs it |

If the planning profile is unknown, list the project root to locate
PROJECT_INDEX.md, docs/plans and docs/decisions. Index and docs/plans alone
are a complete profile without Decisions, since Git stores no empty directory.

| Observed profile | Action |
| --- | --- |
| Complete supported profile | Use the existing records and the operation's route. |
| Wholly absent; durable Plan requested | Initialize through the lifecycle route. |
| Wholly absent; no durable Plan requested | Leave it uninitialized. |
| Partial, foreign, unsupported or ambiguous | Preserve it; repair only an unambiguous format defect that changes no meaning, such as a Step numbered `01.`. |

Related Plan, Decision and index edits form one update. Validate the complete
profile once after the update is saved and before you report it or start
dependent work, not after each field write. A Step status or Evidence edit
needs no validation of its own until the Work Item's status changes or the
work is handed off. progress.md has the command, the diagnostic handling and
the safe-write and continuation rules. In the final report, also name active
or blocked work and the next action.

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

Read one when its condition holds. A complete copy already in context counts
as read, including one embedded in your assignment. Read it again only when
that copy is incomplete or a reload is requested.

- [Writing](references/writing.md): a plan, decision, instruction, review, handoff or a report the user asked for as the result; a disputed conclusion.
- [Machine data](references/machine-data.md): a structured report, log file or saved state you must evaluate, such as JUnit XML or coverage data; a test runner's console summary is not one.
- [Shell commands](references/shell-commands.md): composed text or scripts passed through a shell; quoting, PowerShell encoding, exact bytes or several exit statuses matter.
- [Output delivery](references/output-delivery.md): before a command whose output may exceed the display limit; text that must fit a known limit; delivery as a file.
- [Python discovery](references/python-discovery.md): a Python command or bundled helper, no interpreter verified this session.
- [Instruction design](references/instruction-design.md): a reusable instruction, Skill rule or prompt template.
