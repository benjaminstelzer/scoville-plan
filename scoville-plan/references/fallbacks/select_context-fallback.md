<!-- helper-fallback: scripts/select_context.py -->
# Select Work Item context without Python

Use this route only when no suitable Python 3.11+ is available. Read PROJECT_INDEX.md and
require `format_version: 1`. Choose the requested operation below. If several
are requested, keep their results separate; position and dispatch select
different Steps. Supply original records, not summaries. For saved JSON, use
a native UTF-8 writer and serializer; read the complete saved result before
dependent work. Do not implement a character-to-byte encoder yourself.

## Next ID

For next-ID lookup, an active Plan is not required. Work Item IDs
require an explicit Plan and its matching ID/file; inspect its canonical H3
Work Item IDs. For Plan or Decision IDs inspect every canonical file in the
corresponding docs directory, require format_version 1 and valid metadata IDs,
and take the maximum of both filename and metadata numbers. Report mismatches.
Return `next ID = maximum + 1`, never an interior gap, and the required filename
pattern for Plans/Decisions. Empty directories begin at 0001. Stop at W-999 or
PLAN-/ADR-9999; obtain a format decision. Do not write or reserve anything;
recheck collisions immediately before manual creation. Do not combine this
lookup with position, proposal or context selection.

## Structural start check

Inspect the explicitly named W-NNN in the active
or explicitly named Plan. Return Plan lifecycle and index selection, current_item
match, item status, direct dependency statuses, external blockers, other
in_progress item IDs and linked proposed Decision facts. List violations:
Plan not active or selected, item not current, terminal or already started item,
dependency not done, external blockers and other in_progress items. Distinguish
todo from paused resume; already started work is not a new start. Missing items,
dependencies or malformed records stop the check. Do not inspect proposal
contents to infer relevance, choose successors or interpret Returns/priorities.
Facts never authorize or accept work; make no writes or selections.

## Resolve the Plan for position or context

Resolve `active_plan` and require exactly
one matching active Plan with `format_version: 1`. For an explicit PLAN-NNNN,
resolve that exact Plan instead, retaining its real lifecycle. With a null
`active_plan` and no explicit Plan, report idle and no current Work Item.
Next-ID lookup and the project-wide proposal inventory also work when idle.

## Proposal inventory

Inspect every Decision file's
frontmatter and H1 title. Require unique matching ADR/file IDs, format_version 1,
a supported status, lowercase slash-separated scope and one nonempty H1 outside
backtick or tilde code fences. Ignore fenced contents when locating Plan sections
and titles too; preserve their original text in returned context.
Return each proposed Decision's ID, title, scope and repository-relative path,
including unlinked proposals. Read relevant bodies afterward (all for a full
audit). This works with an idle index and selects no Plan or Work Item. Stop on
malformed or ambiguous metadata; never report a partial list as complete.

## Position

1. Return stored current_item, status, blockers and Acceptance/Evidence;
   retain legacy Next action when present.
2. Determine current and next Steps under the rules below.
3. Return unchanged Instructions, paused_context, historical priorities and
   linked proposed Decisions as described below; infer no return or acceptance.

Current Steps
are only lines whose first annotation is `[status: in_progress]`. A `todo`,
`done` or `cancelled` Step is never current, even when a dispatch selects it.
Group adjacent current Step numbers only. With no active Step, choose the first unfinished
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

## Work Item recovery

1. Choose explicit `W-NNN` when supplied, otherwise active current_item.
2. Require exactly one matching H3 Work Item block.
3. Return every context area below, preserving boundaries and source order:

| Area | Required content |
| --- | --- |
| Plan | Exact frontmatter, Goal and Non-goals. |
| Work Item | Complete block, including Steps, Evidence, Instructions and legacy Next action when present. |
| Direct dependencies | Each ID and Status line. |
| Decisions | Every complete Decision referenced by the item. |

Never trim recovery to a dispatch unit or infer a missing field.

## Dispatch context

1. Select the exact requested unit using its `W-NNN`, not current_item.
2. Resolve canonical records and required context areas below.
3. Return complete context only; missing or ambiguous records, boundaries or
   references stop selection.

Require one matching active Plan and one matching Work Item. `W-NNN` selects its whole
scope, including all existing Steps. With Steps, `W-NNN/step-N` or
`W-NNN/steps-N-M` selects an existing Step or an ascending adjacent range of
at least two Steps. Without Steps, require `W-NNN` alone.

Return the four semantic areas described in [read-only.md](../read-only.md):

| Area | Required content |
| --- | --- |
| Plan | Exact frontmatter, Goal and Non-goals. |
| Unit | Requested unit ID; selected Work Item's heading, Status, Depends on, Blocked by, Decisions, Outcome, Acceptance and Instructions when present; only selected Step lines. |
| Direct dependencies | Each ID and Status line. |
| Decisions | Every complete Decision referenced by the Work Item. |

Include source_text as the exact selected Step lines or complete item
block without Steps, normalized to LF with one final newline and no trailing
separator blank lines. For an item without Steps, retain Evidence and Next
action. Exclude unselected Steps and Work Item-wide Next action from Step units. Resolve each
reference from canonical records. If a record, boundary or reference is missing
or ambiguous, stop without supplying a partial dispatch context.
