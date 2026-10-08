# Read-only project state

Use this route to answer questions about existing project knowledge without
changing canonical files. It does not require the native format guides.
Run the commands below under SKILL.md's Proposal inventory capture rule.
A reviewer does not write source captures; report any required input that
cannot be read completely through a permitted bounded read.

## Locate the current Work Item and Steps

Use the selector's position mode for a compact deterministic lookup:

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --plan PLAN-0001 --position --format json
```

Omit --plan to use the index's active Plan. The position response contains:

- `work_item`: the Plan's stored current_item.
- `current_steps`: only Steps explicitly marked in_progress.
- `current_units`: those active Steps, grouped only when their numbers are adjacent.
- `next_step`: the first written todo Step, only when no Step is active and no
  earlier unfinished Step has an unknown status.
- `untracked_steps`: Steps without a written status. The helper does not guess
  a position when the first unfinished Step's status is unknown.
- `reason`: why work can or cannot resume, alongside the Work Item status and blockers.
- `instructions`: additional binding conditions. null means the field is missing;
  "[]" explicitly means there are none.
- `paused_context`: all paused items' IDs, headings, status, dependency status,
  blockers and Instructions. When Instructions is unrecorded, this also includes
  the legacy Next action and Evidence fields.
- `historical_priorities`: nonterminal items' historical priority headings.
- `open_decisions`: proposed ADRs linked from the current item.
- `acceptance`: the Work Item's requirements.
- `evidence`: its recorded observations.
- `legacy_next_action`: the old field, included only when it exists.

The helper does not infer return targets, instruction fulfilment or acceptance.
Unknown progress never loads repair.md automatically. The helper selects no
work and repairs nothing.
All explicit active Steps are returned even around unknown gaps, with a warning
in guidance. If all Steps are terminal, inspect outstanding Work Item Acceptance
and Evidence; do not invent a next Step or repeat completed effects.
No Steps means a whole-item unit; a Plan without current_item returns null.
Position selects no work, changes no status and grants no start permission.

## Select Work Item or dispatch-unit context

With a verified Python 3.11+, select the current or explicitly named Work Item
with the bundled script. A missing script or script error is a blocker; it
never enables manual selection. The commands below specify the complete
invocation; do not load the Python source just to call them. Run:

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --format json
```

Add `--work-item W-001` to select that item. Add `--plan PLAN-0001` to select
from that named Plan instead of the index's active Plan; the two options may be combined.

For a worker dispatch, select the exact unit instead:

```text
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-001 --format json
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/step-2 --format json
python -X utf8 "<skill-directory>/scripts/check_text_size.py" --max-output-tokens <limit> --run -- python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/steps-2-3 --format json
```

The success object contains exactly four top-level semantic areas:

- `plan`: the exact Plan frontmatter plus Goal and Non-goals sections;
- `work_item`: the complete selected Work Item block in recovery mode, or exact
  structured unit fields in dispatch mode;
- `direct_dependencies`: only each direct dependency ID and its `Status` line;
- `decisions`: the complete Decision records referenced by the selected item.

Dispatch mode accepts a complete Work Item, an exact Step or adjacent Step
range. When selected Steps contain written status, `work_item.step_statuses`
adds their original numbers and status (null for unmarked selected Steps).
Without written status this field is absent. Source text and selected scope
remain exact, including done or cancelled Steps needed for review or correction.

`source_text` is the unchanged selected single-line Step text, adjacent lines, or complete Work
Item block, including its Evidence for a whole-item unit. Text uses UTF-8/LF
and one final newline; trailing block-separator blank lines are excluded.
context_text contains the complete parent Work Item once, for consumers that
need its overall context while assigning only the selected unit. Other
structured fields supply parent context. All referenced Decisions remain
present. Unselected Steps and Work Item-wide Next action are excluded from source_text
for Step units; they remain in context_text as background. Never rewrite source_text. Do not insert dependency Evidence into it.

The selector reads canonical files internally, emits no unrelated Work Item or
Decision body, never truncates, and never falls back to raw files. Its default
UTF-8 output budget is 65,536 bytes; use `--max-output-bytes` only when the
caller has an explicit bounded budget. A malformed profile, ambiguous record,
redirected path, missing reference, or budget overflow returns one structured
diagnostic and no partial context.

This projection does not replace every read operation. Use the proposal
inventory below and load relevant proposals separately, or all for a full audit.
Read relevant dependency Evidence, bounded graph state, queued or paused return state, and complete
relevant Work Items separately when the operation requires them. Keep those
reads bounded and never widen the selector response. Use the profile-specific Runtime helpers rule in SKILL.md when no suitable Python 3.11+ is available. A helper failure stops selection; do not invent partial context.

## Read state outside the selector

Use direct reads for Plan or Decision listings, relevant
dependency Evidence, and graph inspection. These operations complement the
selector; they never replace current-or-named Work Item or dispatch-unit
selection when suitable Python 3.11+ is available.

For a Plan or Decision listing, read only frontmatter and the H1 title unless
the request asks for record content. Read other Work Items only for the
requested state, dependencies, blockers, or authored content. Read a
prerequisite's status for readiness and its full block when its result or
Evidence matters. Surface proposals through the next section without loading
unrelated accepted Decisions.

Extract sections by their boundaries rather than dumping a large file or
truncating it at an arbitrary line count. For a graph or item inventory, ordered
H3 headings and `Status`, `Depends on`, and `Decisions` lines expose identity,
order, and references without loading Outcome, Steps, or Evidence history.
This is a graph view, not complete structural validation. Resolve ambiguous
boundaries or diagnostics from the original blocks; never treat missing output
from a truncated read as a missing record. These bounded reads require no
generated index or cached status file and never bypass a selector diagnostic.

Completed Work Items stay in their original format-version-1 Plan. Load their
details when relevant; do not delete, summarize in place, or move them into an
unsupported archive to shorten context. Use a successor Plan only when the old
goal is actually complete and the ordinary lifecycle permits the transition.

Do not infer status, completion, authority, or acceptance from filenames,
directory presence, implementation files, Git history, or old audit evidence.
Stop if the index is malformed, the declared version is unsupported, or a
referenced record cannot be resolved unambiguously.

## Surface proposals

Use the `--proposals` invocation in [SKILL.md](../SKILL.md#proposal-inventory).

The `proposals` list contains ID, title, scope and repository-relative path for
every proposed Decision, including unlinked proposals and proposals outside the
active Plan. An idle project is supported. The helper reads Decision metadata
and titles, emits no bodies, and does not judge relevance. Do not combine this
mode with --plan, --position, --work-item or --unit. The normal output budget
and diagnostic handling apply. This is an inventory, not full profile validation.

Use each returned path to read and report relevant proposals (all for a full
audit), then apply the entrypoint's choice policy. Keep unrelated work moving.
Without suitable Python 3.11+, follow the selector's manual route named in
SKILL.md.

## Report the boundary

Name the canonical records that supplied the answer. Do not claim complete
project validation when only the index, selected Work Item, and proposal
summaries were inspected.
