# Native project and Plan lifecycle

Use this reference with the Plan format and native editing safety guides for
profile initialization, Plan creation and updates, activation, cancellation,
and final completion.

## Contents

- Classify setup state
- Initialize a profile
- Create and refine Plans
- Activate a Plan
- Complete or cancel a Plan

## Classify setup state

List the workspace root before probing canonical files. Classify the profile as
one of:

- complete and supported: use the existing profile;
- wholly absent: initialize only when a durable Plan was explicitly requested;
- partial or foreign: preserve the reserved paths and stop;
- unsupported: require a matching Skill or explicit migration; or
- invalid: repair only a specific format defect that changes no authored
  intent, otherwise stop.

Never overwrite a partial or foreign profile, copy the format contract into the
project, or initialize merely because project state was requested.

## Initialize a profile

Require explicit Plan title, Goal, Non-goals, and one behavior-complete initial
Work Item with title, Outcome, Acceptance, optional Steps, and `Next action`.
Do not invent missing authored facts.

Prepare `docs/plans/`, `docs/decisions/`, `PLAN-0001`, `W-001`, and
`PROJECT_INDEX.md` as one complete profile. The initial Plan is `active`, the
initial item is `todo` and `current_item`, dependencies, blockers, Decisions,
and Evidence are empty, and the index points to `PLAN-0001`. Create the index
last. If any member fails, report the partial state and stop.

After initialization, record any explicit or possible material Decisions
through the ordinary Decision route and link them while the affected Work Item
is still `todo`.

## Create and refine Plans

Create each later Plan as `draft` with the next highest Plan ID and at least one
`todo` Work Item. Every initial Decision reference must already exist. A generic
Plan update changes only title, Goal, and Non-goals, preserves ID, lifecycle,
dates, current selection, and all Work Items, and advances `updated` only on a
real change.

Cancel a draft only after an explicit user choice. Completed and cancelled
Plans are terminal retained history.

## Activate a Plan

From idle state, activate one draft Plan by changing that Plan and the index as
one prepared change. The user selects a dependency-ready `todo` or `paused`
target as `current_item`. Setting current does not start it.

From active state, prepare the index, target draft Plan, and outgoing active
Plan together. Require the user to select the outgoing Plan status (`draft`,
`completed`, or `cancelled`) and the exact current-item action:

- preserve a `todo` or `paused` item;
- pause an `in_progress` item;
- complete a `todo` or `in_progress` item with evidence and blocker clearing;
  or
- cancel a `todo`, `in_progress`, or `paused` item with evidence and blocker
  clearing.

The final outgoing Plan must satisfy its selected status invariants. Change no
other Work Item implicitly. If any member is invalid or only partly written,
stop as an incomplete transaction.

## Complete or cancel a Plan

Complete the active Plan only together with its final current `todo` or
`in_progress` Work Item. Require observed evidence, explicit blocker clearing,
all dependencies done, and every other Work Item terminal. Set the item to
`done`, the Plan to `completed`, remove `current_item`, and set the index to
`active_plan: null` as one prepared two-file change. A paused item must resume
first.

The sole active Plan never cancels or completes through a standalone status
edit. Draft cancellation is the only standalone Plan lifecycle transition.
Never create a successor Plan or placeholder Work Item merely to avoid the
valid idle state.
