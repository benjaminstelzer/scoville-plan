# Progress

## Start or resume

1. Classify the planning profile with SKILL.md's table, or reuse an unchanged
   classification. For a complete profile, run the proposal inventory and read
   the relevant proposals; an inventory error does not change the
   classification.
2. Read PROJECT_INDEX.md, the active Plan header and the complete affected
   blocks, with the Decisions they reference; complete text held from an
   unchanged file need not be reread. Read a completed or cancelled Plan only
   for a concrete reason it is relevant.
3. Read the known Work Item's context directly and compare `current_item`,
   item status and active Step with your assignment. Use position mode
   when the ID is unknown or a recorded return matters, and after that read
   when those facts disagree.
4. Before starting a todo item, compare its assumptions, paths and checks with
   the current files and its completed dependencies in this Plan, and refine
   stale instructions first.
5. Before starting a todo item or resuming a paused one, run the start check
   and apply [Status changes](#status-changes). An empty `violated_conditions`
   grants no permission: judge proposal relevance and whether the start is
   permitted yourself.

## After an interruption

An in_progress Step may be partly done. Settle it from the evidence (the
Evidence field, original reports, actual results) or the result check the
authorized work needs; repeat no completed effect.

If compaction occurs, continue the same original assignment with its
remaining work. Compaction changes neither assignee nor original Step
boundaries.

## Continuation contract

Keep records resumable from the files alone, with current item and Step,
remaining work, completed effects, governing Decisions and relevant
proposals, live permissions and stops, binding Acceptance, the responsible
source files, and observations and their limits; the first unfinished Step is
what comes next. Write no recovery log.

## Step status

Set Step status only from observed progress: at start, completion,
interruption and correction, and before handoff or compaction. A Step begins
in_progress when its work starts, not on selection; inspecting or reviewing
starts none. It is
done when its action and required checks are complete; cancelled needs explicit direction and is
never done. In an open item, a confirmed correction may return a done Step to
in_progress, with its completed effects and the reason in Evidence. A status
change rewrites no action, order, route or execution choice; pause and
blockers stay on the Work Item. Reviews and Acceptance due on the Work Item
stay due: all Steps done neither completes the item nor authorizes repeating
them.

## Evidence

Record what you ran or inspected and what it showed, specific enough to
repeat (the command, test, file or review), a required review's outcome,
confirmed open defects and the limits of what was checked. For an effect
that cannot be repeated, keep what it was and how it ended; do not repeat an
accepted effect to recreate its evidence. Keep facts that further
development or a retention rule needs, not review transcripts or run
chronology.

The field is normally sufficient. Link existing reports for needed detail;
create or update one only when the task requires that detail. Keep
progression in its Plan fields.

Prefer one line of plain text. More than 200 characters of plain text, or
more than 200 in one entry of a bracketed list `[a, b]`, makes the profile
invalid. For example:
`Evidence: pytest tests/test_thumbnails.py passed, 12 tests; required review found no defects; open: animated GIF input untested (Step 3).`

## Instructions

Instructions holds the additional conditions binding the item now: stops,
limits, explicit returns or required overall reviews. Repeat no Outcome,
Acceptance or history.

When conditions change, replace the whole field with the remaining conditions
in current words, dropping fulfilled or superseded ones, so that old and new
text cannot contradict each other. Keep an unclear live condition briefly and
ask only if the work at hand depends on its meaning. Before completion,
confirm that no binding condition remains unmet. Instructions of a terminal
item are historical direction.

## Blockers

Each label in Blocked by names an actual external prerequisite; one invented
to satisfy validation would block real work. Remove a named blocker from
continuing work only with proof.

## Status changes

An explicit request to execute the whole Plan authorizes continuing item by
item within that scope, without asking again after each.

| Change | Only when | Record |
| --- | --- | --- |
| Select | Active Plan; target todo or paused; its dependencies done; no other item in_progress | Set `current_item`; blockers may remain. Selecting starts nothing. |
| Start or resume | Selected current todo or paused item; dependencies done; no blockers or unresolved Decision the work depends on; scope and Instructions allow it | Set in_progress (paused work never returns to todo), mark the Steps actually started, and save before execution. |
| Pause | Current in_progress item; explicit direction or an authorized pause or return | Set paused; keep the observed Step position and constraints. For a requested return, add it to Instructions, such as `After W-004 completes, resume W-001 at Step 3.` |
| Complete | Current todo or in_progress item (resume paused work first); Acceptance observed; all due Steps, checks, reviews and binding conditions fulfilled; dependencies done; blockers cleared | Set done with Evidence naming the observations that establish completion, and select the successor in the same update. |

Before selecting the successor, check paused items' Instructions for a
return to the finished item. A recorded return comes before document order:
select that item, resume it at its recorded Step, and move the fulfilled
return from its Instructions to its Evidence. Ask about an ambiguous,
missing, blocked or dependency-invalid return instead of skipping it.
Otherwise select the first eligible item in document order; if open items
remain but none is eligible, keep the finished item open with its result in
Evidence and the open succession in Instructions, and ask. Repeat no
completed work for it. Start a selected successor only after the checks under
[Start or resume](#start-or-resume) and within the authorized scope.

When the completed item was the last nonterminal one, complete the Plan in
the same update: `status: completed` without `current_item`, and the index
`active_plan: null`. Create no placeholder work to avoid idle.

## Started items

In an in_progress or paused item, change only Status, Blocked by,
Instructions, Evidence, observed Step status and added Decision links; leave
done and cancelled items unchanged. Any other change follows
[maintenance.md](maintenance.md).
