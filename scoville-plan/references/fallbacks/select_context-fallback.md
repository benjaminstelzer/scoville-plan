<!-- helper-fallback: scripts/select_context.py -->
# Select Work Item context without Python

Use this route only when Python 3 is unavailable. First read `PROJECT_INDEX.md`
and require `format_version: 1`. Resolve its `active_plan` and require exactly
one matching active Plan with `format_version: 1`. For an explicit PLAN-NNNN,
resolve that exact Plan instead of active_plan, retaining its real lifecycle.
A null `active_plan` is idle;
do not infer a current Work Item.

For position lookup, return the stored current_item and its status, blockers
and Acceptance/Evidence; retain legacy Next action when present. Only first-prefix `[status: in_progress]` Steps are current;
group adjacent numbers only. With no active Step, choose the first unfinished
written todo only if no earlier unfinished Step is unmarked. List unmarked
Steps as unknown. Tell the agent to determine their progress from Evidence,
relevant original reports and actual task results or changes against requirements;
never guess or repeat completed effects. Load repair.md only for an explicit
inspect/repair request. Without Steps return a whole-item
unit; without current_item return no selection. Selection grants no permission.
Preserve original Step numbers, text and scope even for done/cancelled Steps
used by review/correction. Optional status is first before route/execute, with
todo/in_progress/done/cancelled only; missing status remains unknown.

Return current Instructions unchanged: missing is null, [] expressly none.
Also return paused_context for every paused item in this Plan: ID, heading,
status, dependency status, blockers and Instructions; when missing include
legacy Next action/Evidence. Retain nonterminal historical priority headings.
Derive open_decisions from linked ADRs whose status is proposed, never copied
state. Do not infer return targets or acceptance from free text. Instructions
before Steps is optional in legacy records; new authors write it explicitly.

For current-or-named Work Item recovery, choose the explicit `W-NNN` ID when
supplied; otherwise use the active Plan's `current_item`. Require exactly one
matching H3 Work Item block. Return the exact Plan frontmatter, Goal and
Non-goals; the complete selected Work Item block, including Steps, Evidence
and any Instructions/legacy Next action; each direct dependency ID and Status line; and every complete
Decision referenced by the Work Item. Preserve record boundaries and source
order. Do not trim the Work Item into a dispatch unit or replace a missing
field with an inference.

For a worker dispatch, select the exact unit instead:

Use the `W-NNN` ID in the requested unit, not `current_item`. Require one
matching active Plan and one matching Work Item. `W-NNN` selects its whole
scope, including all existing Steps. With Steps, `W-NNN/step-N` or
`W-NNN/steps-N-M` selects an existing Step or an ascending adjacent range of
at least two Steps. Without Steps, require `W-NNN` alone.

Return the same four semantic areas described in [read-only.md](../read-only.md):
exact Plan frontmatter, Goal and Non-goals; the requested unit ID and selected
Work Item's heading, Status, Depends on, Blocked by, Decisions, Outcome and
Acceptance lines, Instructions when present, plus only the selected Step lines; direct dependency IDs
with their Status lines; and every complete Decision referenced by the Work
Item. Include source_text as the exact selected Step lines or complete item
block without Steps, normalized to LF with one final newline and no trailing
separator blank lines. For an item without Steps, retain Evidence and Next
action. Exclude unselected Steps and Work Item-wide Next action from Step units. Resolve each
reference from canonical records. If a record, boundary or reference is missing
or ambiguous, stop without supplying a partial dispatch context.
