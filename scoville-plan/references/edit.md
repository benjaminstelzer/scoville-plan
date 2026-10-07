# Edit and resume work

## Read and write

Only when Python is available, use the session interpreter verified with
`--version` wherever examples say `python` (Windows: `py -3`, then `python`;
macOS/Linux: `python3`), following the [runtime rule](../SKILL.md#runtime-helpers).
Without Python, use the manual routes named there; do not invoke these commands.

Read PROJECT_INDEX.md, the active Plan header and the complete affected blocks.
Read referenced Decisions and relevant proposals. Before starting a todo item,
check its premises, paths and checks against current sources and relevant
completed dependencies in this Plan. Refine stale instructions before start.
Do not scan historical Plans without a concrete relevance reason.

On recovery, use position mode to locate the recorded Work Item and Steps,
then select its full context with the commands below.
Its key fields are `plan`, `plan_status`, `work_item`, `work_status`,
`current_steps`, `current_units`, `next_step`, `instructions`, `paused_context`
and `historical_priorities`; [read-only.md](read-only.md) explains further fields.
Do not reconstruct the position or load repair.md for ordinary recovery. Unknown
Steps require only the evidence or result check needed for the authorized work.
Use paused_context and historical_priorities to check relevant return directions;
the full-context mode contains only the selected Work Item.

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --position --format json
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --format json
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --work-item W-001 --format json
```

A selector diagnostic stops selection; do not truncate or invent partial
context. Read read-only.md only for further output-field details, dispatch-unit
selection or wider read tasks.

Edit only the records that own the state. Use context-bound edits: anchor each
replacement to unique surrounding text so it changes only the intended location.
Use UTF-8 without BOM and LF endings. Reject redirected targets or paths
outside this project, and preserve unrelated changes.

Specify `encoding="utf-8"` for every text read and write. Never rely on the
platform encoding. For Python replacement writes, prepare the complete
LF-normalized UTF-8 bytes before opening the target and write those prepared
bytes. If using a text-mode writer, `newline` must contain the actual LF
character, never the two literal characters backslash and n. For
PowerShell pipes, set `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)`
and invoke Python with `-X utf8` so source text and stdin agree. After writing,
decode the saved bytes as UTF-8 and compare changed non-ASCII text with the
intended text. A structural pass alone cannot detect already-corrupted words.

For changes across files, prepare the consistent result together and write the
index last. Stop dependent execution on concurrent changes or a partial write.
An interrupted lifecycle transition needs user direction before completing or
undoing it. Existing explicit direction suffices only for the same prepared,
unambiguous result with unchanged affected sources; otherwise ask.

Reread affected complete blocks and inspect the scoped diff. Check meaning,
authority, current constraints and acceptance evidence, then validate below.
The checked edit and its validation cover only the file contents actually inspected.
Reuse available instructions while they remain unchanged; do not routinely
save extra instruction copies or receipts of their exact bytes.

## Editable fields

| Work Item status | Permitted changes |
| --- | --- |
| todo in draft or active Plan | Authored fields, Evidence and Next action; move or delete a whole block; change state by the rules below |
| in_progress or paused | Status, Blocked by, Instructions, Evidence, legacy Next action and observed Step status; bounded amendments below |
| done or cancelled | No routine edits or state transitions; explicit record cleanup under repair.md may shorten Instructions and Evidence and apply the editorial exception below |

IDs never change. Preserve started scope, dependencies, order and completed effects.
For any status, explicit cleanup under repair.md may shorten Outcome, Acceptance
and Step wording without changing requirements, actions or historical meaning.
This editorial exception needs no old-text note, copy or separate approval.

A started item may add a relevant proposed or accepted Decision, retaining older
links as history. It may correct a stale path, version reference or other purely
formal wording only when evidence shows unchanged behavior, compatibility,
data, authority and verification scope. Retain the old wording and reason in
one referenced note or existing Git history. A changed expected result or weaker
Acceptance is material, not a formal correction; obtain the user's decision
before dependent work and record it in the existing Decision system. Do not
create a replacement Work Item merely to add a Decision or fix formal wording.

Remaining work in a started Step or group may be split into consecutive Steps
in the same Work Item without changing its Outcome, Acceptance, constraints or
authored order. Preserve completed parts and their Evidence, and update affected
Step references so pending assignments still identify the remaining work.
Other started fields remain fixed except for that editorial cleanup. Resume paused work to in_progress, never
todo. The Plan lifecycle reference owns the explicit wholly-unstarted exception.
An explicit user choice may replace only the execution annotation of a named
unperformed Step after start, preserving its action, route and execution history.

## Insert, refine and order

Allocate the highest Work Item ID plus one; recheck collisions and never reuse
an interior gap. Read it with `select_context.py --root "<project-root>"
--next-id work-item --plan PLAN-NNNN --format json`. This only suggests an ID;
recheck immediately before manual creation. Append new outcomes in arrival order. Only an explicit priority
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

Write Outcome as one result sentence and Steps as the ordered mechanism.
Put known paths, interacting owners, discovery, methods and check execution in
Steps. Keep the context needed to execute without chat history.

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

Preserve explicit route and execute annotations; Plan never infers them. For a todo
item without Steps, an explicit executor choice may add one coherent annotated
Step. See granularity only when boundaries need judgment.
Pin a version or count in Acceptance only when
that exact value is itself required; record the tested candidate in Evidence.
Fix test or fixture drift within the existing outcome when it preserves scope
and Acceptance. A separate owner or independently acceptable result warrants a
new item; each failed check does not.

## Step progress

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
These formats do not prove model availability or support. The validator below
names malformed annotations and their correction; it never writes the record.

During ordinary work, add or update status only from observed progress. Begin
in_progress when work starts, not on selection alone. Jointly started Steps
may share in_progress; no separate group record is needed. Mark done when the
Step's action and required checks are complete. Preserve due Work Item reviews
and acceptance. Cancelled needs explicit direction and is never done.
In a nonterminal item, a confirmed correction may return a done Step to
in_progress; retain its completed effects and reason in Evidence. Status changes
do not rewrite the action, order, route or execution choice. Pause and blockers
remain on the Work Item. Update observed Step status at start, completion,
interruption and correction, and before handoff or compaction.
All Steps done does not itself complete the Work Item or authorize repeating them.

## Evidence

Record the observed result briefly. For a required review, record that it took
place. Keep confirmed open defects as current work, not as a review transcript.
Do not copy or archive reviews or a run chronology. Review texts serve only the
development process; full worker results serve the running assessment and
correction. Keep only facts needed for further development or an independently
binding retention requirement.

The field is normally sufficient. Link an existing report only for needed detail;
create or update a separate report only when the task requires that detail.
Do not create archives, copies, hashes or inventories merely to document checks,
reviews or cleanup. Progress and next actions belong in their Plan fields.

Prefer one-line plain text, for example:
`Evidence: Unicode cases passed; Sol high review performed; open: installer ordering, Step 3.`
Keep it within the supported 200 characters. Commas and brackets within the text
are allowed; do not start plain text with `[`. Use `[]` when nothing was observed.
Preserve existing supported lists without routine migration. Explicit cleanup
uses repair.md; it needs no copy of the old Evidence or new report. New writes retain LF.

## Instructions

Use Instructions only for current binding conditions applying to the Work Item
that are not already stated in its Steps, such as a user stop or limit, an
explicit return or a required overall review. Do not repeat or paraphrase Steps,
Outcome or Acceptance, or put status summaries, results, review text, versions,
counts or history here. Ordinary actions remain in Steps; results belong in Evidence.

Use one short line or exactly []; absence is legacy unknown, not []. New items
write it explicitly. When conditions change, replace the whole field with the
remaining conditions in current words. Drop fulfilled or superseded conditions;
do not prepend new text to old instructions. Keep an unclear live condition
briefly and ask only if the next action depends on its meaning. Before new
terminal closure no unmet binding condition remains. Do not reinterpret terminal
history as live instructions. Explicit cleanup of old fields uses repair.md.

## Legacy continuation

Read legacy Next action for binding conditions too; preserve existing return
authority. Legacy nonterminal work without written Step status still needs its nonempty
Next action. When retained during legacy work, keep it consistent with observed
progress. New work uses Steps instead.

## Blockers

Blocked by is `[]` or a comma-space-separated list such as `[EXT-API-KEY]`.
Labels match `[A-Z][A-Z0-9]{1,15}-[A-Z0-9][A-Z0-9._-]{0,47}`; prefixes
`ADR`, `PLAN` and `W` are reserved. Use unique labels for actual external
prerequisites, never invent one to satisfy validation. Resolve only a named
blocker with proof; retain unresolved prerequisites and their effect in Evidence.

## Select and finish

An explicit request to execute the whole Plan authorizes ordinary continuation
within that scope; do not ask again after each item. Read older stops in their
recorded scope. A newer explicit direction replaces an older instruction only
where they conflict; it does not satisfy dependencies, Acceptance or substantive
cost, safety or external prerequisites. Ask only if a material conflict remains.

Only the active Plan selects current_item. Select todo or paused work only with
done dependencies and no other in_progress item. Selection may retain blockers;
starting current todo or resuming current paused work requires no blockers or
unresolved dependent Decision. Pause current in_progress work under explicit
user direction or an already authorized pause or return instruction.

Read structural facts with `select_context.py --root "<project-root>"
--check-start W-NNN --format json`; add --plan PLAN-NNNN to inspect a named
Plan, including a draft or inactive one. The output distinguishes todo, paused
resume, already started and terminal work, checks current_item and lists
dependencies, blockers, other started items and linked open proposals. A
successful read and an empty violated_conditions list grant no permission or
acceptance. Determine proposal relevance and actual authority yourself;
the helper neither chooses a successor nor writes a start.

At execution start, write `Status: in_progress` on the current Work Item and
record the actually started Steps under Step progress. Selecting current_item
or assigning a range alone starts no Step. Save and validate this state before
delegated execution begins. Read-only review does not restart completed Steps.

Complete current todo or in_progress work only with observed Acceptance, done
dependencies, cleared blockers and an eligible exact successor. Resume paused
work before completion. Keep Evidence, empty Blocked by and remove Next action.
Select the authorized successor in the same prepared change. Start it only after
its pre-flight; selection alone does not start it. Validate each completed write
operation. These related field edits need no separate named operation or
additional progress record beyond the native Plan fields.
An eligible ordinary successor may be blocked: select it without starting it.
This does not apply to an explicit return governed by the lifecycle rules.
If no successor can be selected, retain observed Acceptance in Evidence and
name the unresolved succession in Instructions; do not repeat accepted work.
For a bounded execution request, selecting the successor grants no permission
to start work outside that request.

Honor recorded returns and explicit historical priority before default document
order; if those obligations conflict, ask for a choice. Inspect the records
before selection. On an
ambiguous, missing, blocked or dependency-invalid return, retain it and ask
rather than skip it. For historical prefixes or an immediate redirect read the
special cases in the Plan lifecycle reference.

Cancellation needs explicit direction, evidence and cleared blockers; cancelled
work satisfies no dependency. On cancellation, retain Evidence, empty Blocked by
and remove Next action, as on completion. When all other
items are terminal, finish the final item and Plan through the lifecycle route
and set the index idle; invent no successor.

## Structural check

```text
python "<skill-directory>/scripts/validate_profile.py" --root "<project-root>" --format json
```

Read warning diagnostics too: FILE_MOJIBAKE_SUSPECTED gives file, line and
column for common misdecoding sequences in prose. Warnings alone retain
valid=true and exit 0. Fenced/inline code is excluded; an unquoted literal
encoding example may warn. This heuristic misses other damage. Compare changed
non-ASCII text manually with intended wording and never repair it automatically.

Invoke helpers without loading their Python source. They inspect structure and
references, not authorization, meaning or acceptance truth. No planning CLI is
a write path. Read both exit code and JSON valid:

| Exit / valid | Action |
| --- | --- |
| 0 / true | Structural check passed for these bytes; assess semantics separately |
| 1 / false | Follow ordered file and field diagnostics; repair only unambiguous representation defects and rerun |
| 2 / null | Inspection incomplete (path, access, I/O or concurrent change); resolve the condition, claim no pass |
| 3 / null | Helper failure; report it and leave structural acceptance open |

Follow the [Runtime helpers rule](../SKILL.md#runtime-helpers). Never
turn a helper error into a manual pass. Report a remaining lifecycle or scope
choice instead of inventing state to satisfy a diagnostic.
