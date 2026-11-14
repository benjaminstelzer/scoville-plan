# Author Work Items

[progress.md](progress.md) has the rules for safe edits, editable fields and
validation; the entrypoint's route loads it with this file, and the rules
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
1. [status: todo] Perform one bounded action at the known repository-relative paths; add how to tell it is done only where the action leaves that unclear.
Evidence: []
```

New Work Items write Instructions on one line or use [], include at least one
Step with status and omit Next action. Work Item Status and Acceptance cover
the whole outcome. Each Step names its bounded action and, where the action
does not make it evident, how to tell it is done and any check the Step
itself requires; status records observed progress.
Steps have no separate Acceptance or dependencies. See progress.md for legacy
continuation.
[Granularity](planning-granularity.md) helps where outcome or Step boundaries
need judgment; a routine insertion with known boundaries does not need it.

## Insert, refine and order

Added work that no Work Item covers, that the user did not ask to plan or
track and that finishes in this session gets no Work Item unless a
repository rule requires a record; do it directly under the entrypoint's
rule 7.

Use the entrypoint's ID-allocation rule with
`select_context.py --root "<project-root>" --next-id work-item --plan PLAN-NNNN --format json`.
Append new outcomes in arrival order. Only an explicit priority
permits another position; dependencies still precede dependents. Keep the current
item unchanged when queueing. `Depends on` records real prerequisites; using it
to force an order would block work that could proceed. Write no new Deferred
or Prioritized title prefix, on new or existing items. Preserve existing prefixes
and their historical priority; read special cases in the lifecycle reference
when they affect selection. Save and validate before acknowledging a queue.

Combine new work only with the last todo outcome, and only when it shares
that item's result, Acceptance, dependencies, Decisions, blockers, owner
(responsible file, component or person), timing, permissions and risk; never
move an addition across a separate earlier outcome. Otherwise append a new
item.

New work normally fits Goal and Non-goals. When the user asks to
record work that conflicts with Goal, Non-goals or an accepted Decision, record
it anyway: append the item as todo and state the stop in its Instructions, such
as `Do not start before <choice> is decided: <conflict>`. Link the affected
Decision where one exists; where the choice would change an accepted Decision,
record it as a proposed Decision and link that too, so the start check sees it.
Put the question in your report. The item is not started until the choice is
made. Ask before recording only
when it is unclear what to record.

Reuse established intent for the result's lifespan, maintenance and further
development. Ask only about uncertainty that would change the solution, such
as a one-off script versus a maintained module, and reuse the answer. Retain
the answer where a fresh recipient reads it without chat history: in the Work
Item it governs (Outcome or Instructions of a todo item, Instructions of a
started one), or in Goal or Non-goals when it binds the whole Plan and a Goal
change is authorized under the [Goal lifecycle](native-project-lifecycle.md#create-and-refine).

Move whole todo blocks without renumbering. Delete an item only when another
item remains and no `Depends on` names it. Deleting the current item needs a
dependency-ready todo or paused replacement in the same change.

Write Outcome as one desired result sentence. Steps hold the ordered actions, known paths, interacting owners (files, components or people), needed
discovery and methods; keep investigation and implementation distinguishable. Use
progress.md's continuation contract to keep the record independently
resumable. Evidence states observations, not desired outcomes; a proposal
permits nothing.

Derive Acceptance from the requested observable outcome:

- State once each distinct case, result or limit whose failure must prevent
  acceptance, or whose check is explicitly required.
- Merge equivalent conditions; omit recipes, matrices, reasons, history and
  copied fields or project rules.
- Retain required methods, values, variants, exceptions, compatibility,
  prohibitions and verification obligations. Keeping an existing mechanism
  needs its own requirement.
- Cite an accessible authoritative specification by exact path and section
  with a reading instruction instead of copying it. Create no document merely
  to move criteria out of the Plan. No character or criterion quota applies.
- A defect against an existing condition adds no criterion; authorized added
  conditions require a coherent rewrite, preserving the acceptance standard.
- Pin a version or count only when that exact value is itself required;
  record the tested candidate in Evidence.

When authorized remaining work moves to another Work Item or Plan, write the
receiving item from the remaining outcome. Acceptance states each condition
still binding that outcome once, or cites the source Acceptance by exact path
and section. Name an already fulfilled guarantee only when this work could
plausibly break it; project rules and Decisions bind the rest without
restatement. Steps hold takeover and remaining actions; Evidence records the
source item's accepted results and their limits. Completed actions and
results stay out of Acceptance, which states what must still hold. When
another agent continues the same item, fields and criteria stay as they are.

For a todo item without Steps, an explicit execution choice may add one
coherent annotated Step. Fix test or fixture drift within the existing outcome when
that preserves scope and Acceptance. A separate owner or an independently
acceptable result warrants a new item; a single failed check does not.

## Step annotations

Annotation syntax (see the [Plan template](native-project-lifecycle.md#create-and-refine)):

```text
1. [status: todo] Update the named parser; required invalid-input cases return the specified errors and existing valid-input checks pass.
```

Status comes first: todo, in_progress, done or cancelled. Route and execution annotations are optional and record an explicit choice: preserve them and infer none. Order: status, `[route: CLASS]`,
`[execute: model=MODEL_ID; reasoning=LEVEL]`, action. CLASS: ultra_low, low,
medium, high, ultra_high. Execute may omit either
property; if both exist, model comes first with exactly `; ` between them.
MODEL_ID uses lowercase ASCII letters, digits, dots and hyphens and starts
and ends with a letter or digit. LEVEL: none, minimal, low, medium, high, xhigh,
max, ultra.
The validator in progress.md
names malformed annotations and their correction; it never writes the record.
