# Native editing and lifecycle

Direct edits have no ReasonKeep publication gate, expected-hash writer, typed
request validation, or multi-file atomicity. Compensate with narrow reads,
context-bound patches, complete proposed-state inspection, and honest reporting.

## Read before writing

1. When profile existence is unknown, list the workspace root. Do not read a
   canonical file until its presence is established.
2. For an existing profile, resolve the nearest project root containing
   `PROJECT_INDEX.md`, `docs/plans/`, and `docs/decisions/`, then read the index
   and confirm `format_version: 1`.
3. Resolve the active Plan. Read its current Work Item and only the related
   existing Decision records needed by the task.
4. Inventory all Plan IDs only when allocating a Plan. Inventory all Work Item
   IDs in the affected Plan only when allocating an item.
5. Re-read the exact affected bytes immediately before applying a context-bound
   patch.

For an explicitly requested new profile whose index is confirmed absent, use
the current workspace as the setup root. Create the two directories, one draft
Plan, and an idle index first. Never probe the absent index with a file read.
Activate only when the user or binding project workflow authorizes activation
and the selected current Work Item is explicit.

## Preserve authored history

- Edit, move, or physically remove only a `todo` Work Item. Removal also
  requires at least one remaining Work Item and no incoming dependency.
- Once an item leaves `todo`, retain its ID, title, dependencies, Decisions,
  Outcome, Acceptance, Steps, and document position.
- Update live execution through status, Blocked by, Evidence, and `Next action`.
- Move one complete H3 block without renumbering it or any sibling.
- Do not create, edit, accept, reject, deprecate, supersede, or delete Decision
  records through this Skill.

## Progress safely

- Start only the active Plan's current `todo` item whose dependencies are done
  and blockers empty; change it to `in_progress`.
- Pause `in_progress` to `paused`; resume the current `paused` item only when
  dependencies are done and blockers empty.
- Complete `todo` or `in_progress` only after observed acceptance evidence.
  Clear blockers explicitly, remove `Next action`, add Evidence, and select an
  explicit ready replacement when work remains.
- A paused item must resume before completion.
- Cancel only with evidence. `done` and `cancelled` are terminal, and cancelled
  work never satisfies a dependency.
- After implementation exists, set `Next action` to the first unobserved test,
  build, browser check, review, or evaluator-owned verification before handing
  off.

When the final real Work Item completes, update that item, set the Plan to
`completed`, remove `current_item`, and set the index to `active_plan: null` as
one prepared change. Do not invent a successor or handoff Work Item to keep the
project active.

## Blockers

Add an absent valid blocker label together with an updated Next action. Resolve
exactly the named label, append observed evidence for the resolution, and set
the next concrete action. A blocker is not evidence and a failed check is not
completion.

## Guard and inspect the change

Prepare every member of a multi-file lifecycle change before applying any one
file. If relevant bytes changed concurrently, stop and reconcile rather than
overwriting. After editing, reread every changed file and inspect the complete
scoped diff.

Manually check:

- index format and active-Plan ownership;
- exact Plan frontmatter and section order;
- Work Item field order and lifecycle invariants;
- one-or-zero `in_progress` item matching `current_item`;
- dependency existence, authored order, and acyclicity;
- existing Decision references and blocker syntax;
- terminal Evidence and absence of terminal `Next action`;
- non-terminal `Next action` reflecting the first action not yet performed;
- UTF-8 without BOM and LF endings.

An invalid partial transition is a stop. Do not repair it autonomously when the
repair would choose activation, cancellation, completion, evidence, scope, or
another authored lifecycle outcome.
