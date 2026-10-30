# Read-only project state

Use this route to answer questions about existing project knowledge without
changing canonical files. It does not require the native format guides.
Run the commands below under SKILL.md's Helper invocations rule.
A reviewer does not write source captures; report any required input that
cannot be read completely through a permitted read.

## Locate the current Work Item and Steps

Use the selector's position mode for a compact deterministic lookup:

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --plan PLAN-0001 --position --format json
```

Omit --plan to use the index's active Plan. The position response contains:

- `current_steps`: only Steps explicitly marked in_progress.
- `current_units`: adjacent active Step numbers compressed into ranges for position
  reporting. This representation does not authorize grouped execution.
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
- `legacy_next_action`: the old field, included only when it exists.

The helper reports position without inferring returns, instruction fulfilment,
acceptance or start permission; it selects and repairs nothing. All explicitly
active Steps appear even around unknown gaps, with a guidance warning. Unknown
progress uses progress.md's recovery route, not automatic repair. If all Steps
are terminal, inspect outstanding Acceptance/Evidence without inventing a Step
or repeating effects. No Steps means a whole-item unit; no current_item returns null.

## Select Work Item or dispatch-unit context

Select current or explicitly named Work Item context with the bundled script
under SKILL.md's Runtime helpers and Helper invocations rules. The commands
below are complete; no source read is needed to invoke them. Run:

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --format json
```

Add `--work-item W-001` to select that item. Add `--plan PLAN-0001` to select
from that named Plan instead of the index's active Plan; the two options may be combined.

For exact unit inspection, select the unit instead:

```text
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-001 --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/step-2 --format json
python -X utf8 "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/steps-2-3 --format json
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
UTF-8 output budget is 65,536 bytes, an internal default. If this default or an
agent-selected internal budget overflows, explicitly retry once with
`--max-output-bytes <required_bytes>` from the diagnostic. Never raise a binding
cap; capture complete output under the actual outer tool limit. A malformed profile, ambiguous record,
redirected path, missing reference, or budget overflow returns one structured
diagnostic and no partial context.

Load relevant proposals separately through the inventory below, all for a full
audit. Read dependency Evidence, bounded graph state, queued/paused returns and
other complete Work Items only as the operation needs; never widen the selector
response. Apply SKILL.md's profile-specific Runtime helpers rule when Python
3.11+ is unavailable. Helper failure stops selection, without invented partial context.

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
