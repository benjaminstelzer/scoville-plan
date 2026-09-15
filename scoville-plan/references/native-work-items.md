# Native Work Item operations

Use this reference with the Plan format and native editing safety guides for
Work Item insertion, refinement, ordering, blockers, current selection, and
progress transitions.

## Contents

- Preserve authored history
- Refine todo work
- Select and advance work
- Manage blockers and next action
- Complete or cancel work

## Preserve authored history

- Edit, move, or physically remove only a `todo` Work Item in a `draft` or
  `active` Plan. Once an item leaves `todo`, retain its ID, title, dependencies,
  Decisions, Outcome, Acceptance, Steps, and document position.
- Update started work only through status, `Blocked by`, Evidence, and
  `Next action`. A `paused` item resumes to `in_progress`; it never returns to
  `todo` for editing.
- Move one complete H3 block without renumbering any item. Dependencies must
  exist, precede their dependents in authored order, and remain acyclic.

## Refine todo work

- Insert one `todo` block at the end, before an anchor, or after an anchor.
  Allocate the highest Work Item ID plus one and validate the complete Plan.
- A generic update may replace title, dependencies, Decisions, Outcome,
  Acceptance, optional Steps, Evidence, and `Next action` while preserving ID,
  status, blockers, position, and current selection.
- Delete only when at least one Work Item remains and no incoming dependency
  targets it. Deleting the current item requires an explicit dependency-ready
  `todo` or `paused` replacement in the same prepared patch.
- Preserve subordinate implementation order in Steps. Steps never receive IDs,
  status, checkboxes, blockers, evidence, or completion semantics.
- When preparing for later Scoville Workflow execution, keep each Step suitable
  for one worker dispatch with one routing class. Separate materially different
  risk or reasoning demand, but keep activities together when they share the
  same outcome and Acceptance boundary. A `[route: CLASS]` prefix is optional
  prose and may change only while the Work Item remains `todo`.
- When work has several ordered actions, use consecutive numbered Steps in the
  exact execution order. Name every known repository-relative file in its
  action Step. If ownership is unknown, perform bounded read-only discovery
  before start when practical and refine the `todo` item with the observed path.
  When discovery must run after start, retain its criterion-based Step, append
  the observed path to Evidence, and update Next action with that path. Never
  rewrite the started Steps.
- Keep Outcome conceptual, Steps executable, Acceptance decisive, and Next
  action limited to the first unperformed Step or unobserved Acceptance check.
  Do not repeat the same fact across those fields or rely on a worker to infer
  an omitted transition.

## Queue deferred work during a current item

Use this operation only after the core classifies the new message as additive
and a complete supported active Plan owns the running work. Queueing is a narrow
planning checkpoint, not a switch to the requested implementation. Preserve
`current_item` and every field of the current started Work Item.

First confirm that the request fits the active Plan's Goal and Non-goals. A new
instruction authorizes its requested work but does not silently authorize a
broader Plan scope, weaker Acceptance, or a conflicting lifecycle choice. Ask
only for a material missing choice and allow independent current work to
continue.

Record queue provenance in the existing H3 title. A newly queued Work Item uses
`Deferred after W-001: Describe the observable outcome`, replacing `W-001` with
the exact Work Item after which it belongs. Consecutive `todo` blocks with the
same `Deferred after W-001:` prefix are that anchor's deferred segment. Their
authored order is stable arrival order unless the user supplies another order.
The prefix is permanent truthful history after the item starts. It may be added,
changed, or removed only while the affected item remains `todo` and only when
the user-authorized order changes.

When the user explicitly chooses a future `todo` successor, record that fact
before acknowledging it with the title prefix `Prioritized after W-001:`.
Allow at most one such successor for an anchor. This
visible prefix distinguishes an explicit priority from ordinary future authored
order after restart. It records sequencing provenance, not status, and remains
truthful retained history after start. An unmarked Work Item is never treated as
having an unrecorded explicit priority.

Inspect the complete anchored segment and its final queued `todo` item. Apply
the batching rules from planning-granularity.md. When compatible, refine that
complete block in place, preserving its prefix, ID, position, status, blockers,
and current selection. When incompatible, allocate the next Work Item ID, use
the visible deferred prefix, and insert the new `todo` block after earlier items
with the same anchor, ahead of unmarked lower-priority future `todo` work. A
plain additive imperative carries this default after-current priority.

Do not override a `Prioritized after W-001:` successor, move a non-`todo` block,
or invent a dependency to force the preferred position. Ask when the new
default conflicts with that persisted priority. If the user preserves the
prioritized successor, anchor the deferred work after it. If a genuine
prerequisite must precede the new item, use that prerequisite as the deferred
anchor, place the item at the earliest valid position after it, and report that
it cannot be the immediate successor.

The visible title prefixes, ordered H3 blocks, stable Work Item IDs,
dependencies, blockers, Decisions, and authored fields are the complete durable
queue. Create no chat-only queue, new field, checkbox, or hidden marker. On
recovery, derive the exact successor and deferred segment only from those
records. Multiple priority prefixes for one anchor or a prefix whose anchor is
missing or does not precede it is invalid authored intent and requires human
direction, not silent normalization.

An immediate redirect with an explicit return to the outgoing started item uses
its mutable `Next action`, not its immutable title or position. When pausing
W-001 to run W-004, preserve the first unperformed action in this form:
`After W-004 completes, resume W-001 and perform ACTION.` Use this condition only
when the user explicitly requested the return. An ordinary pause keeps an
ordinary concrete Next action. Allow at most one paused return target for the
redirected item, and treat conflicting return instructions as a choice rather
than overwriting them.

On recovery, inspect paused Work Items for an explicit return condition naming
the current redirected item. After that item satisfies Acceptance, complete it
through ordinary completion while selecting the paused return target, then use
the guarded resume operation and restore its Next action to the preserved first
concrete action. Do not use `complete_and_advance`, which starts a `todo`
replacement rather than resuming paused work. If the return target is blocked,
dependency-invalid, missing, or ambiguous, preserve the recorded condition and
request the required choice without starting different work automatically.

After the guarded write and structural inspection succeed, acknowledge the
batched or created Work Item by ID and resume the unchanged current work. If
persistence fails, report that the request is not durably queued and do not
claim or begin it.

After current Acceptance is observed, reread the native order and identify the
exact intended successor. If it is start-eligible, use guarded
`complete_and_advance`. If its dependencies are done but an external blocker or
unresolved Decision prevents starting, ordinary completion may select it
without starting it, preserving the blocker or proposal. If dependency order
leaves no eligible replacement or the successor is ambiguous, keep the current
item non-terminal and request the required choice. Never skip queued work,
fabricate readiness, clear a blocker, invent Evidence, or complete the Plan
while deferred non-terminal work remains.

## Select and advance work

- Set `current_item` only in an active Plan. Its target is `todo`,
  `in_progress`, or `paused`, all dependencies are `done`, and no different
  item is `in_progress`. External blockers may remain visible on the selection.
- Start only the current `todo` item when dependencies are done and blockers
  empty. Pause only the current `in_progress` item. Resume only the current
  `paused` item when dependencies are done and blockers empty.
- Keep at most one `in_progress` item, always equal to `current_item`. This is a
  concurrency limit, not a one-Work-Item total limit.
- `complete_and_advance` is one prepared compound result: complete the exact
  current item, then start the explicit replacement through the ordinary start
  rules. If either side is invalid, publish neither result.

## Manage blockers and next action

Add one absent valid external blocker together with a changed `Next action`.
Resolve exactly the named blocker, append observed evidence, and set the next
concrete action. A blocker is not evidence.

`set-next-action` changes only that live field on a non-terminal item. Keep it
equal to the first concrete action not yet performed. After implementation
exists, advance it to the first unobserved test, build, browser check, review,
or evaluator-owned verification.

## Complete or cancel work

- Complete only the current `todo` or `in_progress` item in an active Plan when
  dependencies are done, observed acceptance evidence is supplied, every
  blocker is explicitly cleared, and an eligible replacement current item is
  named. A paused item must resume before completion.
- Cancel a `todo`, `in_progress`, or `paused` item in a draft or active Plan
  only with evidence and explicit blocker clearing. Current work requires an
  eligible replacement. `cancelled` never satisfies a dependency.
- Terminal work has no `Next action`, has empty blockers, and retains non-empty
  Evidence. `done` and `cancelled` never transition again.
- For the final real Work Item, use guarded active-Plan completion from
  [native-project-lifecycle.md](native-project-lifecycle.md). Do not invent a
  successor or handoff item merely to keep `current_item` populated.
