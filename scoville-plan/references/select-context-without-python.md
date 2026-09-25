# Select Work Item context without Python

Use this route only when Python 3 is unavailable. First read `PROJECT_INDEX.md`
and require `format_version: 1`. Resolve its `active_plan` and require exactly
one matching active Plan with `format_version: 1`. A null `active_plan` is idle;
do not infer a current Work Item.

For current-or-named Work Item recovery, choose the explicit `W-NNN` ID when
supplied; otherwise use the active Plan's `current_item`. Require exactly one
matching H3 Work Item block. Return the exact Plan frontmatter, Goal and
Non-goals; the complete selected Work Item block, including Steps, Evidence
and Next action; each direct dependency ID and Status line; and every complete
Decision referenced by the Work Item. Preserve record boundaries and source
order. Do not trim the Work Item into a dispatch unit or replace a missing
field with an inference.

For a worker dispatch, select the exact unit instead:

Use the `W-NNN` ID in the requested unit, not `current_item`. Require one
matching active Plan and one matching Work Item. If the item has Steps, require
`W-NNN/step-N` or `W-NNN/steps-N-M` with an existing Step or an ascending
adjacent range of at least two Steps. Without Steps, require `W-NNN` alone.

Return the same four semantic areas described in [read-only.md](read-only.md):
exact Plan frontmatter, Goal and Non-goals; the requested unit ID and selected
Work Item's heading, Status, Depends on, Blocked by, Decisions, Outcome and
Acceptance lines, plus only the selected Step lines; direct dependency IDs
with their Status lines; and every complete Decision referenced by the Work
Item. Include source_text as the exact selected Step lines or complete item
block without Steps, normalized to LF with one final newline and no trailing
separator blank lines. For an item without Steps, retain Evidence and Next
action. Exclude unselected Steps and Work Item-wide Next action from Step units. Resolve each
reference from canonical records. If a record, boundary or reference is missing
or ambiguous, stop without supplying a partial dispatch context.
