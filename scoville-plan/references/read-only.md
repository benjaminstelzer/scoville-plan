# Read-only project state

Use this route to answer questions about existing project knowledge without
changing canonical files. It does not require the native format guides.

## Read the smallest canonical state

1. Read `PROJECT_INDEX.md` and require `format_version: 1`.
2. If `active_plan` is `null`, report the project as idle and do not infer a
   current Work Item.
3. If it names a Plan, read that Plan's frontmatter and the complete H3 block
   named by `current_item`. Read other Work Items only when the request asks
   about their state, dependencies, blockers, or authored content.
4. Read Decisions referenced by the selected Work Item only when their choice
   or rationale is needed. Inventory Decision frontmatter to find every
   `proposed` record; read and surface those proposals without loading unrelated
   accepted Decisions.
5. For a Plan or Decision listing, read only frontmatter and the H1 title unless
   the request asks for record content.

Do not infer status, completion, authority, or acceptance from filenames,
directory presence, implementation files, Git history, or old audit evidence.
Stop if the index is malformed, the declared version is unsupported, or a
referenced record cannot be resolved unambiguously.

## Surface proposals

For every `proposed` Decision, report its ID, title, recommended choice, and
practical effect, then ask the user to accept, reject, or revise it. Repeat
unresolved proposals at handoff. Continue unrelated work, but stop before work
whose direction depends on one. Never infer acceptance from silence, continued
work, or implementation that follows the recommendation.

## Report the boundary

Name the canonical records that supplied the answer. Do not claim complete
project validation when only the index, selected Work Item, and proposal
summaries were inspected.
