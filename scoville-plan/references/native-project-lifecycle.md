# Plan lifecycle and special cases

Use edit.md for writing and validation. Only PROJECT_INDEX.md selects the active Plan.

## Create and refine

Initialize only a wholly absent profile on explicit request. Prepare
PROJECT_INDEX.md, docs/plans, docs/decisions and the first Plan together. Require
the supplied title, Goal, Non-goals and first Work Item with its acceptance;
never invent missing direction. Select the initial todo W-001 without starting
it. Write the index last. An existing partial or unsupported profile is not setup.

Allocate the highest PLAN number plus one, never an interior gap; check ID and
filename collisions. Use `docs/plans/0014-subject.md` for PLAN-0014. A later Plan
may obtain its ID and filename pattern from `select_context.py --root
"<project-root>" --next-id plan --format json`. The read-only result includes
both filename and metadata numbers, exposes mismatches, and reserves nothing;
recheck collisions immediately before manual creation. A later Plan
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
on real changes. Preserve identity, lifecycle and Work Items.

Classify the whole proposed Goal before writing: target and plan-wide
constraints stay there;
exclusions belong to Non-goals, choices to Decisions, item-specific actions and
checks to their Work Item, observations to Evidence, and policy to repository
instructions. Messages about ongoing work do not authorize a Goal edit; leave
the Goal text unchanged when processing them.

Move existing facts only with authorization. Every affected dispatch must
still be able to read those facts through its Work Item, its Decisions or a
repository contract that the dispatched agent has demonstrably loaded.

## Activate

To activate a Plan, require an explicit direction, a target draft Plan and a
selected todo or paused item whose dependencies are done. Activation does not
start execution. From idle, prepare the target Plan and index together.

When switching from an active Plan, prepare the outgoing Plan in the same
change. Use the user's chosen draft, completed or cancelled Plan status.
Apply only the user's chosen action for its current item:

- Keep a todo or paused item, or
- pause an in_progress item, or
- complete or cancel the item under edit.md.

Preserve every other item. Validate the complete resulting profile.

## Complete or cancel a Plan

When final current todo or in_progress work meets Acceptance and every other
item is terminal, prepare one coherent update:

| Owner | Terminal fields |
| --- | --- |
| Work Item | `Status: done`; retain observed Evidence; empty Blocked by; no Next action. |
| Plan | `status: completed`; no current_item. |
| Index | `active_plan: null`. |

Write the index last and validate the complete profile through edit.md.
Paused work must first resume. Create no placeholder work to avoid idle.

Cancel a draft only on explicit direction. An active Plan cannot be cancelled
or completed with a standalone status edit: reconcile current work and index
in the same prepared change.

Cancelled and completed Plans are terminal; do not reactivate them. The
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
A missing or later anchor, duplicate priorities for one anchor or a conflict with
an explicit return requires a choice; never silently normalize history.

Only when the user explicitly requests return after redirect, pause the outgoing
started item and retain the binding return in Instructions:
`After W-004 completes, resume W-001 at Step N.` Keep title, Steps and position.
Read existing Next-action returns as equally binding; never silently discard them.
An ordinary pause preserves the observed Step position and remaining constraints.
Permit only one unambiguous paused return target per redirected item.

Before completing current work, compare every paused return naming that item
with every `Prioritized after <current-item>:` successor. Use the position
helper's paused_context and historical_priorities; read legacy Next action and Evidence
when Instructions was not captured. The helper does not interpret these texts.

| Return or priority result | Action |
| --- | --- |
| Different targets | Keep current item nonterminal and both instructions. Ask which target follows; record observed Acceptance without selecting or resuming either target. |
| Blocked, missing or dependency-invalid return | Retain return and obtain a choice; never skip to another item. |
| Unambiguous paused return satisfying edit.md's resume prerequisites, and observed Acceptance | Complete current work and select/resume that return through the sequence below. |

Historical priority without a paused return follows normal selection under
[edit.md](edit.md). For the eligible unambiguous paused return only:

1. Complete current work while selecting the return target.
2. Resume it and restore its recorded Step position or legacy concrete action.
3. Remove the consumed return from live Instructions; record fulfilment in Evidence.
4. Validate the complete write operation.
