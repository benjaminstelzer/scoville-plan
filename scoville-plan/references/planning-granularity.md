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

## Write the execution sequence

Use numbered Steps when order affects correctness or when several file changes
must be coordinated. Keep the concept in Goal and Outcome; Steps contain only
the ordered work needed to realize it. For authored prose, follow an explicit target language first. Otherwise keep
the existing Plan's language, including for added Steps or Work Items. For a new
Plan, use the user's request language. Keep required labels and technical
identifiers unchanged.

1. Place prerequisites and canonical-owner changes before dependent consumers.
2. Name each known repository-relative file in the Step that changes it.
3. Keep one action slice per Step so a lower-reasoning worker can stop and resume safely.
4. Put proof in Acceptance and observed results in Evidence, not in duplicate Steps.

Do not add a Step solely to locate an owner or file that is already known. Keep
bounded behavior or contract inspection when its result can change the
implementation or when it is an explicit prerequisite. When ownership is
unknown, prefer bounded read-only discovery before the Work Item starts and
refine its `todo` Steps with the observed path. If discovery must occur during
execution, keep the ownership criterion in the immutable Step and continue
through permitted live fields. A reviewer must be able to follow the Step order
and map each action to the outcome without inferring missing intermediate work.

## Batch deferred additions

When the core classifies a mid-task request as additive, combine it with the
latest queued `todo` Work Item only when all requested changes remain one small,
behavior-complete outcome. They must share the same observable result,
Acceptance boundary, dependencies, Decisions, blockers, ownership, rollout
timing, authorization, and material risk. One joint check must be able to prove
every included change. Size alone never makes unrelated work compatible.

Keep the requests in arrival order as Steps when subordinate order matters, and
rewrite the batch Outcome, Acceptance, and Next action so every addition remains
explicit. Never use a vague maintenance or follow-up bucket. Merge only into a
`todo` item and only when doing so does not move the new request across an
earlier separate queued item. Preserve the visible deferred title prefix while
refining the batch. The prefix records queue provenance, while the remaining
title and Outcome still name the observable result.

Create a separate Work Item when the new request is complex, independently
resumable, separately acceptable, differently dependent or blocked, owned by a
different component, subject to another Decision or rollout, or materially
different in risk or routing demand. A small request that arrives after such an
item starts a new small batch rather than jumping ahead to an older batch.

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
`[route: ultra_high]`. The route prefix records only the class, not a model or reasoning level.
The Workflow configuration maps that class to execution settings. An explicit
user choice of model or reasoning may be recorded separately in the existing
`[execute: ...]` annotation defined by the native Plan format. Omit the prefix rather than
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
