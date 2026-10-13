# Author Work Items

Before any write, read [progress.md](progress.md) for safe edits, field rights and
validation. This route adds authoring rules; it grants no extra editing rights.

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
Keep the context needed to execute without chat history.

Derive Acceptance from the requested observable outcome. Keep each distinct,
necessary condition once: the relevant case, required result and binding limits.
A condition belongs here when its failure alone prevents acceptance, or when
it is an explicitly binding verification requirement. Merge equivalent conditions.
Do not add implementation recipes, full test matrices, reasons, history or copies
of Outcome, Steps, Instructions or generic project rules. Methods belong here
only when that method is itself required. Preserve required values, variants,
exceptions, compatibility, must-not conditions and verification obligations.
Cite an existing authoritative specification by exact path and section instead
of copying it; the assigned agent must read that section. Create no document
merely to move criteria out of the Plan. No character or criterion quota applies.
A finding against an existing condition is a defect, not another criterion.
When authorized changes add a condition, rewrite Acceptance coherently rather
than appending history. Brevity never permits weaker acceptance.

When authorized remaining work moves to another Work Item or Plan, write the
receiving item from the remaining outcome. Acceptance states each condition
still binding that outcome once, including fulfilled guarantees the remaining
work must preserve, or cites the source Acceptance by exact path and section.
Steps hold takeover and remaining actions; Evidence records accepted source
contributions and their limits. Do not copy completed actions or results into
Acceptance. A manager or worker handoff of the same item changes no fields or
criteria.

Preserve explicit route and execute annotations; Plan never infers them. For a todo
item without Steps, an explicit executor choice may add one coherent annotated
Step. See granularity only when boundaries need judgment.
Pin a version or count in Acceptance only when
that exact value is itself required; record the tested candidate in Evidence.
Fix test or fixture drift within the existing outcome when it preserves scope
and Acceptance. A separate owner or independently acceptable result warrants a
new item; each failed check does not.

## Step annotations

Minimum Step syntax (see the [Plan template](native-project-lifecycle.md#create-and-refine)):

```text
1. [status: todo] Verify the result.
```

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
