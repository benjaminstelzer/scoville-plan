# Plan lifecycle and special cases

Use edit.md for writing and validation. The index is the sole active-Plan owner.

## Create and refine

Initialize only a wholly absent profile on explicit request. Prepare
PROJECT_INDEX.md, docs/plans, docs/decisions and the first Plan together. Require
the supplied title, Goal, Non-goals and first Work Item with its acceptance;
never invent missing direction. Select the initial todo W-001 without starting
it. Write the index last. An existing partial or unsupported profile is not setup.

Allocate the highest PLAN number plus one, never an interior gap; check ID and
filename collisions. Use `docs/plans/0014-subject.md` for PLAN-0014. A later Plan
starts draft with at least one todo item. Use this template with actual values:

```text
---
format_version: 1
id: PLAN-0014
status: draft
created: 2026-09-25
updated: 2026-09-25
---

# Plan title

## Goal

Current target, boundary and genuinely plan-wide constraints.

## Non-goals

Explicit exclusions.

## Work items

Insert the Work Item template from SKILL.md.
```

An active Plan adds `current_item: W-001` after updated. The index uses:

```text
---
format_version: 1
active_plan: PLAN-0014
---
```

Its optional body must not duplicate live state. Use `active_plan: null` when
idle. A generic Plan edit changes only title, Goal and Non-goals, plus updated
on real changes. Preserve identity, lifecycle and Work Items. Classify the whole
proposed Goal before writing: target and plan-wide constraints stay there;
exclusions belong to Non-goals, choices to Decisions, item-specific actions and
checks to their Work Item, observations to Evidence, and policy to repository
instructions. Operational messages leave Goal bytes unchanged. Moving existing
facts requires authorization and continued access by every affected dispatch
through its item, Decisions or a demonstrably loaded repository contract.

## Activate

Activation requires a target draft Plan, explicit direction and a selected
dependency-ready todo or paused current item. It does not start execution. From idle, prepare the target
and index together. From an active Plan, also prepare the outgoing Plan with
the user's chosen draft/completed/cancelled status and exact current-item action:
preserve todo/paused, pause in_progress, or complete/cancel under edit.md.
Preserve every other item. Validate the complete resulting profile.

## Complete or cancel a Plan

When final current todo/in_progress work meets Acceptance and every other item
is terminal, prepare together: item `Status: done`, retained observed Evidence,
empty Blocked by and no Next action; Plan `status: completed` without
current_item; index `active_plan: null`. Validate the complete resulting profile
through edit.md. Paused work must first resume. Do not create placeholder work
to avoid idle.

Cancel a draft only on explicit direction. An active Plan cannot be cancelled
or completed with a standalone status edit: reconcile current work and index
in the same prepared change. Cancelled and completed Plans are terminal: do not reactivate them. The
wholly-unstarted exception below permits only its stated rewrite or deletion,
never a lifecycle transition.

## Rewrite or delete an unstarted Plan

An explicit rewrite or deletion may use this exception only when the whole
Plan has never executed. Activation alone is not execution. Any in_progress,
paused or done item, or actual execution evidence, defeats the exception.
Check cancelled-item Evidence; if start history is unclear, ask.

A confirmed unstarted Plan may have requested authored fields rewritten on
todo or cancelled items, even in a cancelled Plan. Preserve IDs, references,
Evidence, order and lifecycle. Cancelled items remain cancelled, with empty
blockers and no Next action. This neither reopens work nor applies to executed
history. Ordinary todo refinement remains governed by edit.md.

Before authorized deletion inspect incoming references and validate the complete
proposed remaining profile. Resolve invalid references without rewriting
retained history or deleting linked Decisions. If active, set the index idle
unless an eligible replacement was explicitly selected. Retain the index and
canonical directories even when no Plans remain. No cancellation record or
placeholder is required. Once execution began, retain the Plan and cancel
through the ordinary route instead of deleting it.

## Historical priority and explicit returns

Do not create new title prefixes. Read existing `Deferred after W-001:` as an
anchored deferred segment in its stored arrival order, and `Prioritized after
W-001:` as an explicitly chosen successor. Preserve that priority on recovery.
A missing/later anchor, duplicate priorities for one anchor or a conflict with
an explicit return requires a choice; never silently normalize history.

Only when the user explicitly requests return after redirect, pause the outgoing
started item and keep its first unfinished action in Next action:
`After W-004 completes, resume W-001 and perform ACTION.` Keep title and position.
An ordinary pause keeps the ordinary next action. Permit only one unambiguous
paused return target per redirected item.

Before completing current work, compare every paused return naming that item
with every `Prioritized after <current-item>:` successor. If they name different
targets, keep the current item nonterminal, preserve both instructions and ask
which target should follow; observed Acceptance alone does not resolve this
conflict. Record that observation without selecting or resuming either target.

Only after successor selection is unambiguous and Acceptance is observed,
complete current work while selecting the paused return target, resume it and
restore its saved concrete action. Validate the completed write operation.
A blocked, missing or dependency-invalid return stays recorded and needs a
choice; do not skip to another item.
