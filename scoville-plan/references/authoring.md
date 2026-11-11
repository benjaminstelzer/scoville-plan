# Author Work Items

[progress.md](progress.md) owns safe edits, field rights and validation; the
entrypoint's route loads it together with this file, and the authoring rules
here work within those rights. Step annotations at the end matter only when
authoring or changing route/execute settings.

Write agent-facing record text under
[agent instruction design](instruction-design.md); the native fields and
lifecycle rules below still decide what goes where.

## Contents

- Work Item template
- Insert, refine and order
- Step annotations

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
1. [status: todo] Perform one bounded action at the known repository-relative paths; name its own observable completion condition and the required checks that verify it.
Evidence: []
```

New Work Items write Instructions on one line or use [], include at least one
Step with status and omit Next action. Work Item Status and Acceptance cover
the whole outcome. Each Step names its bounded action, its own observable
completion condition and required checks; status records observed progress.
Steps have no separate Acceptance or dependencies. See progress.md for field
permissions and legacy continuation.
[Granularity](planning-granularity.md) helps where outcome or Step boundaries
need judgment; a routine insertion with known boundaries does not need it.

## Insert, refine and order

Use the entrypoint's ID-allocation rule with
`select_context.py --root "<project-root>" --next-id work-item --plan PLAN-NNNN --format json`.
Append new outcomes in arrival order. Only an explicit priority
permits another position; dependencies still precede dependents. Keep the current
item unchanged when queueing. `Depends on` records real prerequisites; using it
to force an order would block work that could proceed. Write no new Deferred
or Prioritized title prefix, on new or existing items. Preserve existing prefixes
and their historical priority; read special cases in the lifecycle reference
when they affect selection. Persist and validate before acknowledging a queue.

Combine only the last todo outcome when the new work shares its result,
Acceptance, dependencies, Decisions, blockers, owner, timing, authority and risk;
an addition is not moved across a separate earlier outcome. Otherwise append a
new item. New work normally fits Goal and Non-goals. When the user asks to
record work that conflicts with Goal, Non-goals or an accepted Decision, record
it anyway: append the item as todo and state the stop in its Instructions, such
as `Do not start before <choice> is decided: <conflict>`. Link the affected
Decision where one exists; where the choice would change an accepted Decision,
record it as a proposed Decision and link that too, so the start check sees it.
Put the question in your report. The item is not started until the choice is
made. Ask before recording only
when it is unclear what to record.

Reuse established intent for lifespan, maintenance and further development. Ask
only about uncertainty that materially affects the solution, and reuse the
answer. Retain the intent and any clarification in the existing Goal or Non-goals
under the [Goal lifecycle](native-project-lifecycle.md#create-and-refine), so a
fresh recipient can use it without chat history.

Move whole todo blocks without renumbering. Delete only when another item
remains and no incoming dependency targets it. Deleting the current item needs
a dependency-ready todo or paused replacement in the same change.

Write Outcome as one desired result sentence. Steps hold the ordered mechanism,
known paths, interacting owners, discovery and methods; distinguish investigation
from implementation. Use progress.md's continuation contract to keep the record
independently resumable. Evidence states observations, not desired outcomes;
proposals grant no authority.

Derive Acceptance from the requested observable outcome. State each distinct
necessary case, result and binding limit once: failure must prevent acceptance,
or the check itself must be explicitly required. Merge equivalent conditions;
omit recipes, matrices, reasons, history and copied fields or project rules.
Retain required methods, values, variants, exceptions, compatibility, prohibitions
and verification obligations. Keeping an existing mechanism needs its own
requirement. Cite an accessible authoritative specification by exact path and
section with a reading instruction instead of copying it. Create no document
merely to move criteria out of the Plan. No character or criterion quota applies.
A defect against an existing condition adds no criterion; authorized added
conditions require a coherent rewrite, preserving the acceptance standard.

When authorized remaining work moves to another Work Item or Plan, write the
receiving item from the remaining outcome. Acceptance states each condition
still binding that outcome once, or cites the source Acceptance by exact path
and section. Name an already fulfilled guarantee only when this work could
plausibly break it; project rules and Decisions bind the rest without
restatement. Steps hold takeover and remaining actions; Evidence records
accepted source contributions and their limits. Completed actions and results
stay out of Acceptance, which states what must still hold. When another agent
continues the same item, fields and criteria stay as they are.

Preserve explicit route and execute annotations; Plan never infers them. For a todo
item without Steps, an explicit execution choice may add one coherent annotated
Step. See granularity only when boundaries need judgment.
Pin a version or count in Acceptance only when
that exact value is itself required; record the tested candidate in Evidence.
Fix test or fixture drift within the existing outcome when it preserves scope
and Acceptance. A separate owner or independently acceptable result warrants a
new item; each failed check does not.

## Step annotations

Annotation syntax (see the [Plan template](native-project-lifecycle.md#create-and-refine)):

```text
1. [status: todo] Update the named parser; required invalid-input cases return the specified errors and existing valid-input checks pass.
```

Status comes first: todo, in_progress, done or cancelled. A Step without status
is legacy unknown, which is neither todo nor done. Route and execution
annotations are optional: preserve explicit choices and add none by inference,
because they record an explicit choice. Order: status, route, execute, action. CLASS: ultra_low, low, medium, high, ultra_high. Execute may omit either
property; if both exist, model comes first with exactly `; ` between them.
MODEL_ID uses lowercase ASCII letters, digits, dots and hyphens and starts
and ends with a letter or digit. LEVEL: none, minimal, low, medium, high, xhigh,
max, ultra.
These formats do not prove model availability or support. The validator in progress.md
names malformed annotations and their correction; it never writes the record.
