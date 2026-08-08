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
