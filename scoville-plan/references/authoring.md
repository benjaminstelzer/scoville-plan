# Author Work Items

Before any write, read [progress.md](progress.md) for safe edits, field rights and
validation. This route adds authoring rules; it grants no extra editing rights.

For drafting or revising agent-facing record text, apply
[agent instruction design](instruction-design.md). Native fields and lifecycle
rules below govern the records, not Skill-authoring procedures.

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

For each new Work Item, write Instructions on one line or use []. Include at
least one Step with status and omit Next action. Work Item Status and Acceptance
cover the whole outcome. For every Step, write its bounded action, its own
observable completion condition and required checks in its text; its status
records observed progress. Steps have no separate Acceptance field or
dependencies. See progress.md for fields and legacy continuation.
Use [granularity](planning-granularity.md) only when outcome or Step
boundaries need judgment, not for a routine insertion with known boundaries.

## Insert, refine and order

Use the entrypoint's ID-allocation rule with
`select_context.py --root "<project-root>" --next-id work-item --plan PLAN-NNNN --format json`.
Append new outcomes in arrival order. Only an explicit priority
permits another position; dependencies still precede dependents. Keep the current
item unchanged when queueing. Do not invent dependencies to force an order.
Do not write new Deferred or Prioritized title prefixes. Preserve existing prefixes
and their historical priority; read special cases in the lifecycle reference
when they affect selection. Persist and validate before acknowledging a queue.

Combine only the last todo outcome when the new work shares its result,
Acceptance, dependencies, Decisions, blockers, owner, timing, authority and risk.
Do not move an addition across a separate earlier outcome. Otherwise append a
new item. New work must fit Goal and Non-goals; ask only about unresolved scope.

Move whole todo blocks without renumbering. Delete only when another item
remains and no incoming dependency targets it. Deleting the current item needs
a dependency-ready todo or paused replacement in the same change.

Write Outcome as one result sentence and Steps as the ordered mechanism under
the template rule above. Distinguish investigation from implementation explicitly. Put known paths, interacting owners, discovery and methods in Steps.
Keep enough context for a fresh agent to resume from repository records:
current item and Step, remaining action, completed effects, governing Decisions
and relevant unresolved proposals, live authority and stops, binding Acceptance,
source owners, observed evidence and its limits, and the next permitted action.
Keep each fact in its owning field rather than adding a recovery log. For a
required accessible source, give its exact path and section with a reading
instruction. State needed facts directly when the recipient cannot read it.
Requested future outcomes are not observations. Evidence records only what was
observed, and a proposal grants no authority.

Derive Acceptance from the requested observable outcome. Keep each distinct,
necessary condition once: the relevant case, required result and binding limits.
A condition belongs here when its failure alone prevents acceptance, or when it
is an explicitly binding verification requirement. Merge equivalent conditions.
Do not add implementation recipes, full test matrices, reasons, history or
copies of Outcome, Steps, Instructions or generic project rules. Methods belong
here only when that method is itself required. Preserve required values,
variants, exceptions, compatibility, must-not conditions and verification
obligations; a condition that forbids removing an existing mechanism needs its
own requirement. Cite an existing authoritative specification by exact path and
section instead of copying it; the assigned agent must read that section. Create
no document merely to move criteria out of the Plan. No character or criterion
quota applies. A finding against an existing condition is a defect, not another
criterion. When authorized changes add a condition, rewrite Acceptance
coherently rather than appending history. Brevity never permits weaker
acceptance.

When authorized remaining work moves to another Work Item or Plan, write the
receiving item from the remaining outcome. Acceptance states each condition
still binding that outcome once, or cites the source Acceptance by exact path
and section. Name an already fulfilled guarantee only when this work could
plausibly break it; project rules and Decisions bind the rest without
restatement. Steps hold takeover and remaining actions; Evidence records
accepted source contributions and their limits. Do not copy completed actions or
results into Acceptance. A manager or worker handoff of the same item changes no
fields or criteria.

Preserve explicit route and execute annotations; Plan never infers them. For a todo
item without Steps, an explicit executor choice may add one coherent annotated
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

This illustrates annotation syntax. A real Step also names its known paths
and the bounded action, completion condition and required checks under the
authoring rule above.

Status comes first: todo, in_progress, done or cancelled. A Step without status
is legacy unknown; never treat it as todo or done. Route and execution annotations
are optional;
preserve explicit choices, never infer them. Order: status, route, execute,
action. CLASS: ultra_low, low, medium, high, ultra_high. Execute may omit either
property; if both exist, model comes first with exactly `; ` between them.
MODEL_ID uses lowercase ASCII letters, digits, dots and hyphens and starts
and ends with a letter or digit. LEVEL: none, minimal, low, medium, high, xhigh,
max, ultra.
These formats do not prove model availability or support. The validator in progress.md
names malformed annotations and their correction; it never writes the record.
