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

## Workflow-ready subplan points

When Scoville Workflow is available, shape optional Steps so the Workflow can
later dispatch them without re-decomposing the Work Item. This planning aid does
not activate the Workflow, require it, or authorize execution.

One Step is one subplan dispatch point. Keep its outcome slice, authorization,
Acceptance cue, and expected reasoning demand coherent. Split Steps when their
routing needs differ materially: for example, a simple text correction and a
complex persistence redesign must not share one Step. Do not split merely
because the same result needs code, UI, copy, installation, browser work, or
live QA; those activities stay together when they share one risk and Acceptance
boundary.

When the routing class is confidently known, prefix the Step with exactly one
of `[route: ultra_low]`, `[route: low]`, `[route: medium]`, `[route: high]`, or
`[route: ultra_high]`. Record the class, not a model or reasoning level, because
the Workflow configuration owns that live mapping. Omit the prefix rather than
inventing a class. The coordinator rechecks stale or newly changed risk at
dispatch. Without Steps, the complete Work Item is one dispatch unit.

Keep independently resumable outcomes as separate Work Items even when their
routing class matches. Workflow-ready Steps remain subordinate sequence: they
gain no status, ID, dependency, blocker, Evidence, or lifecycle of their own.

## Representative shapes

For a small application, use two or three Work Items rather than one omnibus
item or one lifecycle item per action. A calculator can separate its arithmetic
domain from its responsive interface. Each item owns its implementation steps,
acceptance, evidence, and current action.

For a stored workflow, domain transition, persistence adapter, and user-facing
flow may have independent outcomes. For a structural change, migration,
compatibility, consumer update, and rollout may be separately resumable.

For one UI behavior, a suitable Workflow-ready shape could be:

```text
Steps:
1. [route: ultra_low] Correct the approved button label and verify the exact copy.
2. [route: medium] Implement and browser-check the responsive interaction across its affected component states.
```

The different routing demand justifies two Steps. The second Step keeps code,
UI, and browser validation together because they prove the same behavior.

Dependencies express genuine boundary order. Keep subordinate sequence in
Steps. After each performed phase, rewrite `Next action` to the first unobserved
action. If implementation exists but the agent cannot run checks, explicitly
name evaluator-owned tests, build, browser verification, or review.
