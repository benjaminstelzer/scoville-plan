# Read-only project state

Use this route to answer questions about existing project knowledge without
changing canonical files. It does not require the native format guides.

## Read the smallest canonical state

1. Read `PROJECT_INDEX.md` and require `format_version: 1`.
2. If `active_plan` is `null`, report the project as idle and do not infer a
   current Work Item.
3. If it names a Plan, require that Plan's `format_version: 1`; read its
   frontmatter and the complete H3 block named by `current_item`. Include the
   title, Goal, and Non-goals when interpreting direction or resuming work.
   Read other Work Items only for the requested state, dependencies, blockers,
   or authored content. Read a prerequisite's status for readiness; load its
   full block when its result or evidence matters.
4. Read Decisions referenced by the selected Work Item only when their choice
   or rationale is needed. Inventory Decision frontmatter to find every
   `proposed` record; read and surface those proposals without loading unrelated
   accepted Decisions.
5. For a Plan or Decision listing, read only frontmatter and the H1 title unless
   the request asks for record content.

Extract sections by their boundaries rather than dumping a large file or
truncating it at an arbitrary line count. For a graph or item inventory, ordered
H3 headings and `Status`, `Depends on`, and `Decisions` lines expose identity,
order, and references without loading Outcome, Steps, or Evidence history.
This is a graph view, not complete structural validation. Resolve ambiguous
boundaries or diagnostics from the original blocks; never treat missing output
from a truncated read as a missing record. Shell searches and range reads suffice;
no Python helper, generated index, or cached status file is required.

Completed Work Items stay in their original format-version-1 Plan. Load their
details when relevant; do not delete, summarize in place, or move them into an
unsupported archive to shorten context. Use a successor Plan only when the old
goal is actually complete and the ordinary lifecycle permits the transition.

Do not infer status, completion, authority, or acceptance from filenames,
directory presence, implementation files, Git history, or old audit evidence.
Stop if the index is malformed, the declared version is unsupported, or a
referenced record cannot be resolved unambiguously.

## Surface proposals

For every `proposed` Decision, including unrelated proposals, report its ID,
title, recommended choice, and practical effect. Ask for accept, reject, or
revise only when requested work depends on the choice or the user asks to handle
Decisions. A status/listing request does not require a decision answer. Preserve
unresolved proposals at handoff without repeating unchanged decision questions
on each status turn. New decision-relevant evidence may warrant asking again.
Continue unrelated work, but stop before work whose direction depends on a
proposal. Never infer acceptance from silence, continued work, or implementation
that follows the recommendation.

## Report the boundary

Name the canonical records that supplied the answer. Do not claim complete
project validation when only the index, selected Work Item, and proposal
summaries were inspected.
