# Edit and resume work

## Read and write

Only when Python is available, use the session interpreter verified with
`--version` wherever examples say `python` (Windows: `py -3`, then `python`;
macOS/Linux: `python3`), following the [runtime rule](../SKILL.md#load-only-the-current-route).
Without Python, use the manual routes named there; do not invoke these commands.

Read PROJECT_INDEX.md, the active Plan header and the complete affected blocks.
Read referenced Decisions and relevant proposals. Before starting a todo item,
check its premises, paths and checks against current sources and relevant
completed dependencies in this Plan. Refine stale instructions before start.
Do not scan historical Plans without a concrete relevance reason.

For current or named recovery, run the selector rather than reconstructing its
projection. Read paused return instructions and historical priority segments
separately because the selector does not include unrelated Work Items.

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --format json
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --work-item W-001 --format json
```

A selector diagnostic stops selection; do not truncate or invent partial
context. Read read-only.md only for dispatch-unit selection or wider read tasks.

Edit only the owning records. Use context-bound edits, UTF-8 without BOM and
LF; reject redirected targets or paths outside this project. Preserve unrelated
changes. Specify `encoding="utf-8"` for every text read and write; for Python
writes also use `newline="\n"`. Never rely on the platform encoding. For
PowerShell pipes, set `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)`
and invoke Python with `-X utf8` so source text and stdin agree. After writing,
decode the saved bytes as UTF-8 and compare changed non-ASCII text with the
intended text; a structural pass alone cannot detect already-corrupted words. For multi-file changes prepare the consistent result together and write
the index last. Stop on concurrent changes or a partial write. An interrupted
lifecycle transition needs user direction before completing or undoing it.

Reread affected complete blocks and inspect the scoped diff. Check meaning,
authority, preserved history and acceptance evidence, then validate below.
A successful result applies only to the inspected bytes. Reuse available,
unchanged instructions; no routine saved copies or byte receipts are required.

## Editable fields

| Work Item status | Permitted changes |
| --- | --- |
| todo in draft/active Plan | Authored fields, Evidence and Next action; move or delete a whole block; change state by the rules below |
| in_progress or paused | Status, Blocked by, Evidence and Next action only |
| done or cancelled | Retained history; no routine edits or state transitions |

IDs never change. Started title, dependencies, Decisions, Outcome, Acceptance,
Steps and position stay immutable. Paused work resumes to in_progress, never
todo. The Plan lifecycle reference owns the explicit wholly-unstarted exception.
An explicit user choice may replace only the execution annotation of a named
unperformed Step after start, preserving its action, route and execution history.

## Insert, refine and order

Allocate the highest Work Item ID plus one; recheck collisions and never reuse
an interior gap. Append new outcomes in arrival order. Only an explicit priority
permits another position; dependencies still precede dependents. Keep the current
item unchanged when queueing. Do not invent dependencies to force an order.
Do not write new Deferred/Prioritized title prefixes. Preserve existing prefixes
and their historical priority; read special cases in the lifecycle reference
when they affect selection. Persist and validate before acknowledging a queue.

Combine only the last todo outcome when the new work shares its result,
Acceptance, dependencies, Decisions, blockers, owner, timing, authority and risk.
Do not move an addition across a separate earlier outcome. Otherwise append a
new item. New work must fit Goal and Non-goals; ask only about unresolved scope.

Move whole todo blocks without renumbering. Delete only when another item
remains and no incoming dependency targets it. Deleting the current item needs
a dependency-ready todo or paused replacement in the same change.

Write Outcome as the result, Acceptance as decisive checks, and Steps as the
ordered mechanism. Include known paths, interacting owners, required discovery
and checks that need interpretation. Keep all context needed without chat history.
Preserve explicit route/execute annotations; Plan never infers them. For a todo
item without Steps, an explicit executor choice may add one coherent annotated
Step. See granularity only when boundaries need judgment.

## Evidence and Next action

Evidence contains actual observations with precise artifact references, not
expected results or a diary. Prefer one-line plain text, for example:
`Evidence: tests/results.txt records passing Unicode cases, including brackets [x].`
Keep it within the supported 200 characters; link a
report for more detail. Commas and brackets within the text are allowed; do not
start plain text with `[`. Use `[]` when nothing was observed. Preserve existing
supported lists without migration. New writes retain LF.

Next action names the first unfinished action. Once implementation exists, name
the first unobserved test, build, browser check, review or evaluator check.
Changing it alone changes no other field. Resolve only a named blocker, with
observed evidence and a new next action; adding a blocker also updates that action.

## Select and finish

Only the active Plan selects current_item. Select todo or paused work only with
done dependencies and no other in_progress item. Selection may retain blockers;
starting current todo or resuming current paused work requires no blockers or
unresolved dependent Decision. Pause current in_progress work on authorization.

Complete current todo or in_progress work only with observed Acceptance, done
dependencies, cleared blockers and an eligible exact successor. Resume paused
work before completion. Keep Evidence, empty Blocked by and remove Next action.
Select the authorized successor in the same prepared change. Start it only after
its pre-flight; selection alone does not start it. Validate each completed write
operation. No named compound operation or additional progress record is needed.

Honor recorded returns and explicit historical priority before default document
order; if those obligations conflict, ask for a choice. Inspect the records
before selection. On an
ambiguous, missing, blocked or dependency-invalid return, retain it and ask
rather than skip it. For historical prefixes or an immediate redirect read the
special cases in the Plan lifecycle reference.

Cancellation needs explicit direction, evidence and cleared blockers; cancelled
work satisfies no dependency. Terminal fields match completion. When all other
items are terminal, finish the final item and Plan through the lifecycle route
and set the index idle; invent no successor.

## Structural check

```text
python "<skill-directory>/scripts/validate_profile.py" --root "<project-root>" --format json
```

Invoke helpers without loading their Python source. They inspect structure and
references, not authorization, meaning or acceptance truth. No planning CLI is
a write path. Read both exit code and JSON valid:

| Exit / valid | Action |
| --- | --- |
| 0 / true | Structural check passed for these bytes; assess semantics separately |
| 1 / false | Follow ordered file/field diagnostics; repair only unambiguous representation defects and rerun |
| 2 / null | Inspection incomplete (path, access, I/O or concurrent change); resolve the condition, claim no pass |
| 3 / null | Helper failure; report it and leave structural acceptance open |

Runtime requirements and the sole no-Python fallback are in SKILL.md. Never
turn a helper error into a manual pass. Report a remaining lifecycle or scope
choice instead of inventing state to satisfy a diagnostic.
