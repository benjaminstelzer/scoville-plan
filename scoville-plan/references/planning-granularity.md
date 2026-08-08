# Planning granularity

Use Work Items for outcomes that can be resumed, blocked, accepted, or handed
over independently. Use Steps for ordered implementation work inside one such
outcome. Approval, testing, documentation, and release checks remain acceptance
or evidence unless they are independently requested deliverables.

Keeping at most one Work Item `in_progress` controls concurrent execution. It
does not limit the Plan to one Work Item. Multiple `todo`, `done`, or
`cancelled` items preserve the real outcome boundaries.

## Decomposition checks

Split an outcome when at least one of these differs materially:

- observable acceptance boundary;
- dependency readiness;
- responsible owner or component boundary;
- ability to pause and resume independently;
- rollout, migration, or compatibility timing; or
- blocker that should not stop otherwise independent work.

Do not split merely by activity. Implementing, testing, reviewing, documenting,
and releasing one behavior normally belong to the same Work Item.

## Representative shapes

For a small application, use two or three Work Items rather than one omnibus
item or one lifecycle item per action. A calculator can separate its arithmetic
domain from its responsive interface. Each item owns its implementation steps,
acceptance, evidence, and current action.

For a stored workflow, domain transition, persistence adapter, and user-facing
flow may have independent outcomes. For a structural change, migration,
compatibility, consumer update, and rollout may be separately resumable.

Dependencies express genuine boundary order. Keep subordinate sequence in
Steps. After each performed phase, rewrite `Next action` to the first unobserved
action. If implementation exists but the agent cannot run checks, explicitly
name evaluator-owned tests, build, browser verification, or review.
