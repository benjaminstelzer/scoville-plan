# Create Plans and Work Items

Status changes and started items follow [progress.md](progress.md).

## Create a profile or Plan

A new profile consists of PROJECT_INDEX.md, docs/plans, docs/decisions and
the first Plan, created in one update. Derive title, Goal, Non-goals and the
first Work Item with its Acceptance from the request and binding repository
rules; ask only for missing material direction and invent no scope,
exclusions or acceptance requirements. The first Plan is `PLAN-0001` in
`docs/plans/0001-<lowercase-hyphenated-subject>.md`, active with
`current_item: W-001` (added after `updated`) and W-001 todo, which starts
nothing; on an explicit request for draft or idle it stays draft and the index
idle. A later Plan starts draft with at least one todo item; `--next-id plan`
gives its ID and filename. On explicit direction to work on it, activate it
under [maintenance.md](maintenance.md#activate-or-switch-a-plan).

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

Current target and boundary; each still-binding plan-wide constraint by its effect, with its Decision ID where a Decision records it.

## Non-goals

Explicit exclusions, without reasons or drafting notes; `[]` when there are none.

## Work items

Work Items follow the template below.
```

PROJECT_INDEX.md names the active Plan, or `active_plan: null` when idle; an
optional body repeats neither the active Plan, the current item nor any status:

```text
---
format_version: 1
active_plan: PLAN-0014
---
```

When creating a later Plan, read completely only the Decisions it would link
or supersede, or whose Work Items it replaces; creating a Plan removes no
Decision and no link.

## Write Goal

Keep Goal to the current target, its boundary and, for each still-binding
plan-wide constraint, what it requires plus its Decision ID where one exists,
as in `No new runtime dependency (ADR-0031)`: an agent may receive only the
Decisions linked to its item, not every ID in Goal. Keep exclusions in
Non-goals. Both describe the result: a condition on the working process, such
as when work may start or what a session may touch, is neither, and where it
binds later work it goes into the item's Instructions. Omit dated steering,
drafting notes, superseded constraints, copied ADR rationale and progress
history. Messages about ongoing work do not
authorize Goal edits; an authorized change replaces superseded constraint
wording with what binds now and leaves the history to its Decision.

## Work Item template

```text
### W-001 Observable outcome

Status: todo
Depends on: []
Blocked by: []
Decisions: []
Outcome: One independently resumable result.
Acceptance: Distinct necessary observable conditions and required results; follow the Acceptance rules below.
Instructions: []
Steps:
1. [status: todo] Perform one bounded action at the known repository-relative paths; add how to tell it is done only where the action leaves that unclear.
Evidence: []
```

Every field is one line; each Step is one numbered line below `Steps:`.
Write Outcome as one desired result sentence. Status and Acceptance cover the
whole outcome; Steps have no Acceptance or dependencies of their own.
`Depends on` records real prerequisites; using it to force an order would
block work that could proceed.

Derive Acceptance from the requested observable outcome:

- State once each distinct case, result or limit whose failure must prevent
  acceptance, or whose check is explicitly required.
- Merge equivalent conditions; omit recipes, matrices, reasons, history and
  copied fields or project rules.
- Retain required methods, values, variants, exceptions, compatibility,
  prohibitions and verification obligations. Keeping an existing mechanism
  needs its own requirement.
- Create no document merely to move criteria out of the Plan. No character
  or criterion quota applies.
- A defect against an existing condition adds no criterion; authorized added
  conditions require a coherent rewrite, preserving the acceptance standard.
- Pin a version or count only when that exact value is itself required;
  record the tested candidate in Evidence.

## Steps and their size

A Work Item is a result that can be accepted, blocked, resumed or handed off
independently; implementation, tests, review and documentation proving the
same behavior stay in one item. Steps are its ordered, behavior-complete
units. Each names its bounded action, known paths, interacting owners (files,
components or people), needed discovery and methods, and, where the action
leaves it unclear, how to tell it is done. Put prerequisites and changes to
the canonical source before their consumers; keep intermediate actions inside
their Step. Write no Step that only does bookkeeping or repeats another Step's
testing. Separate Steps whose consequences or reasoning demand differ.

Size a Step to finish, with its checks, within the executing agent's context
window; split larger work by result before execution. Record a path
discovered during work in Evidence. Keep the record resumable under the
[continuation contract](progress.md#continuation-contract).

## Add work to an existing Plan

Get the ID with `--next-id work-item --plan PLAN-NNNN`; IDs never change.
Append new outcomes in arrival order; only an explicit priority permits
another position, and dependencies still precede dependents. Move whole todo
blocks without renumbering. Keep the current item unchanged when queueing,
and save before acknowledging a queue.

Separate items whose acceptance, dependencies, responsible party, rollout or
blockers differ materially. Combine new work only with the last todo outcome,
and only when it shares that item's result, Acceptance, dependencies,
Decisions, blockers, owner, timing, permissions and risk; never move an
addition across a separate earlier outcome. Fix test or fixture drift within
the existing outcome when that preserves its scope and Acceptance; group
repairs with a common cause instead of an item per failure.

New work normally fits Goal and Non-goals. When the user asks to record work
that conflicts with Goal, Non-goals or an accepted Decision, record it anyway:
append the item as todo and state the stop in its Instructions, such as
`Do not start before <choice> is decided: <conflict>`. Link the affected
Decision where one exists; where the choice would change an accepted Decision,
record it as a proposed Decision and link that too, so the start check sees
it. Put the question in your report. The item is not started until the choice
is made. Ask before recording only when it is unclear what to record.

Reuse established intent for the result's lifespan, maintenance and further
development; ask only when an unknown would change the solution, such as a
one-off script versus a maintained module, and record the answer in the Work
Item it governs or, when it binds the whole Plan and a Goal change is
authorized, in Goal or Non-goals.

## Step annotations

Route and execution annotations are optional and record an explicit choice;
infer none. They follow the status, as in
`1. [status: todo] [route: medium] [execute: model=gpt-6.2-sol; reasoning=high] Update the parser.`;
the validator names malformed annotations and permitted values.

## Hand remaining work to another item

When authorized remaining work moves to another Work Item or Plan, write the
receiving item from the remaining outcome. Its Acceptance states each
condition still binding that outcome once, or cites the source Acceptance by
exact path and section; name a fulfilled guarantee only when this work could
plausibly break it. Steps hold takeover and remaining actions; Evidence
records the source item's accepted results and their limits. When another
agent continues the same item, fields and criteria stay as they are.
