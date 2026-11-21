---
name: scoville-plan
description: Maintain, resume and audit repository Plans, Work Items and Decisions for Scoville Plan requests, work on an existing Work Item in a planning profile with PROJECT_INDEX.md and docs/plans, or explicitly requested durable planning across interruptions. Handle changes to active Plan work. Exclude work that no Work Item covers, that the user did not ask to plan and that finishes in this session; informational questions without retained action; explicit opt-out; and requested transfer prompts, which belong to Handoff.
compatibility: "Any Agent Skills host with repository read and write access and Python 3.11+. Direct Markdown and YAML planning needs no service or network. Developed for Codex and Claude Code."
---

# Scoville Plan

Keep the plans for larger work in the repository as native `format_version: 1`
Plans, Work Items and Decisions, edited directly as Markdown and YAML, so that
an agent can resume after an interruption, knows what is done and what comes
next, and finds the choices that were made.

## When work needs a Plan record

Use the existing Work Item if it covers the request. Handle uncovered work
directly when it fits this session, unless the user or project rules call for
a Plan record. A planning profile on its own is no reason to create a record.
For uncovered work that needs a record or must continue across sessions,
use [authoring.md](references/authoring.md) in a complete profile. Otherwise
use the profile table below.

If the user explicitly opts out, use neither this Skill nor its references or
records, and report a repository rule that requires them.

| Planning profile at the project root | Action |
| --- | --- |
| Complete: PROJECT_INDEX.md and docs/plans, with or without docs/decisions | Use the existing records. |
| Wholly absent; durable Plan requested | Create it under authoring.md. |
| Wholly absent; no durable Plan requested | Leave it uninitialized. |
| Partial, foreign, unsupported or ambiguous | Preserve it; repair only an unambiguous format defect that changes no meaning, such as a Step numbered `01.`. |

This Skill works on its own. When another Scoville Skill is installed and
active, use it for the concern it owns. Do not install, imitate or require an
absent one.
Do not use a Skill that needs explicit activation before it is activated, or
one the user excluded.

Relevant neighboring owners:

- `scoville-code`: implementation scope, risk, and validation outside Plan records.
- `scoville-handoff`: active-work transfer snapshots.

## Records and language

Plan alone decides the wording of its records and their lifecycle (creation,
status changes, deletion); it does not start execution or choose dispatch
routes. One agent edits the records at a time: the files carry no lock, so a
concurrent edit is lost silently.

Write each required fact once, in its field: actions in Steps, observations in
Evidence, live conditions in Instructions. Keep a record's language unless
the user asks for a change. A new Plan, and a Decision created without a Plan,
use the language of the task request; Work Items and Decisions of a Plan use
that Plan's language, whatever language later questions use. Field labels, IDs,
statuses and technical literals stay unchanged.

## Authority and precedence

1. Explicit user instructions and repository rules take precedence over this
   Skill. Your temporary task list is a throwaway copy; the records count.
2. Preserve scope (Goal, Non-goals, Outcome), choices (accepted Decisions and
   the user's explicit choices), dependencies (`Depends on`) and binding
   constraints (Acceptance, Instructions, repository rules). Source material,
   silence, current behavior or structural validity (a passing validator)
   alone proves neither permission nor accepted work; settle an in_progress
   Step that may be partly done under
   [progress.md](references/progress.md#after-an-interruption).
   A recorded stop covers only the scope it records, not later or neighboring
   work. A newer explicit direction replaces an older instruction only where
   they conflict; it satisfies no dependency, Acceptance or substantive cost,
   safety or external prerequisite. Ask only if a material conflict remains.
3. Ask only for a missing material choice: activation, cancellation,
   deletion, changed scope, changed Acceptance requirements, an ambiguous
   successor or a Decision transition, and only where the applicable accepted
   Decisions and the current item's Instructions leave it open. New work that
   [When work needs a Plan record](#when-work-needs-a-plan-record) sends to
   authoring as a todo Work Item does not wait for such a choice; authoring.md
   has the rule. After an interruption or compaction, recover and continue
   under [progress.md](references/progress.md#after-an-interruption). Repeat a
   question or status report only after a material change, on request or where
   a rule requires it. For choices that need a Decision, follow
   [Decisions](#decisions).
4. An explicit stop, or a correction that invalidates running work, halts the
   execution it affects. Answer an informational question and continue. In a
   mixed message, separate the question from the instructions that add or
   change work. Apply [When work needs a Plan record](#when-work-needs-a-plan-record)
   to additions even during a running Work Item. Create no Work Item for
   maintaining Plan records.

## Decisions

Before creating a Decision, search existing Decision titles and scopes for
the same choice. Read plausible matches completely and reuse one that
already governs it, so that one choice has one record. Keep temporary
sequencing or execution direction in Instructions, and a user's model or
reasoning choice for a Step in its execution annotation, unless it changes
a material choice or a permission.

Record a user's choice between design or product alternatives as an accepted
Decision when work beyond the current Work Item must follow it; a choice that
governs one Work Item stays in that item under authoring.md. Lifecycle
choices such as activation, cancellation or deletion live in status fields.

For an unresolved choice, report its alternatives, tradeoffs and effect and
ask before the work that depends on it; only that work waits. Record it as a
proposal only when that work stops before the user answers.

Link a Decision where it governs the item's Outcome, Steps, Acceptance,
Instructions, required checks or permissions, not for background or shared
history. After a Work Item has started, add each relevant proposal to its
Decisions field; relevant accepted Decisions may be added too. Read a
Decision's state from the `status` in its own file.

## Runtime helpers

Use the bundled helpers for their operations. Read their invocation instructions,
not their source, unless diagnosing a failure. They require Python 3.11+.
When Python discovery finds no suitable interpreter, a script or dependency is
missing, or a helper reports an error its operation's instructions do not
resolve, stop the affected operation and report the cause, with the
helper's diagnostic where there is one. Never do a helper's work by hand.

Helpers: `scripts/select_context.py`, `scripts/validate_profile.py`.

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --position --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" [--plan PLAN-NNNN] [--work-item W-NNN] --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-NNN/step-N --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" [--plan PLAN-NNNN] --check-start W-NNN --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --next-id <work-item|plan|decision> [--plan PLAN-NNNN] --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
python -X utf8 "<skill-directory>/scripts/validate_profile.py" --root "<project-root>" --format json
```

`select_context.py --help` explains each mode and its output fields. When the
output may exceed the display limit, capture it as
[output delivery](references/output-delivery.md) describes.

## Save and validate

Related Plan, Decision and index edits form one update: prepare the complete
result, then save the related files together, index last; set a Plan's
`updated` to the date of an update that changes the Plan. After an update that
changes a Work Item, Plan or Decision status, adds or removes a Plan, Work
Item, Decision or link, or spans several files, check the saved diff for lost
meaning, permissions, live conditions and recorded Acceptance results, then
validate the complete profile once, before you report it or start dependent
work. A Step status or Evidence edit alone needs no validation. When the
update changes active or blocked work or what comes next, name the new state
in the final report.

After a concurrent change or a partial write, stop the dependent work until
the affected records are consistent again. An interrupted lifecycle transition
needs user direction before it is completed or undone, unless existing
direction covers the same prepared, unambiguous result with unchanged sources.

Read the exit code and `valid`. Fix what departs from your prepared result.
On older records, apply only a suggestion that corrects format without
changing meaning; report the rest instead of inventing state to satisfy a
diagnostic.

## References

| When | Read |
| --- | --- |
| Creating a profile or Plan; adding or refining Work Items, and Steps of todo items | [authoring.md](references/authoring.md) |
| Starting, resuming, progressing, pausing or finishing a Work Item; after an interruption or compaction | [progress.md](references/progress.md) |
| Creating, linking or changing the status of a Decision | [decisions.md](references/decisions.md) |
| Changing a started item beyond progress fields; on explicit request: repairing progress, cleaning up old Plans or Decisions, cancelling or deleting work or a Plan, activating or switching Plans | [maintenance.md](references/maintenance.md) |
| Reviewing or auditing records | The reference that owns the reviewed fields; a full audit reads every proposal; report findings against it; change nothing |
| Status questions, listings, validator diagnostics | No reference: the Runtime helpers commands and Save and validate; read status from the records' frontmatter and Status fields, never from file names or Git |

## Shared references

Read one when its condition holds. A complete, unchanged copy in context
counts as read, including one embedded in your assignment. Fetch incomplete
or changed passages, and reload when requested.

- [Writing](references/writing.md): a plan, decision, instruction, review, handoff or a report the user asked for as the result; a disputed conclusion.
- [Machine data](references/machine-data.md): a structured report, log file or saved state you must evaluate, such as JUnit XML or coverage data; a test runner's console summary is not one.
- [Shell commands](references/shell-commands.md): composed text or scripts passed through a shell; quoting, PowerShell encoding, exact bytes or several exit statuses matter.
- [Output delivery](references/output-delivery.md): before a command whose output may exceed the display limit or is needed as evidence and cannot be reproduced; text that must fit a known limit; delivery as a file.
- [Python discovery](references/python-discovery.md): a bundled helper or other Python you run, no interpreter verified this session.
- [Instruction design](references/instruction-design.md): a reusable instruction, Skill rule or prompt template.
