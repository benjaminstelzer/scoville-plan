# Read-only project state

Use this route to answer questions about existing project knowledge without
changing canonical files. It does not require the native format guides.

## Select Work Item or dispatch-unit context

When Python 3 is present, select the current or explicitly named Work Item
with the bundled script. A missing script or script error is a blocker; it
never enables manual selection. The commands below specify the complete
invocation; do not load the Python source just to call them. Run:

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" [--work-item W-001] --format json
```

For a worker dispatch, select the exact unit instead:

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-001 --format json
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/step-2 --format json
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --unit W-003/steps-2-3 --format json
```

The success object contains exactly four top-level semantic areas:

- `plan`: the exact Plan frontmatter plus Goal and Non-goals sections;
- `work_item`: the complete selected Work Item block in recovery mode, or exact
  structured unit fields in dispatch mode;
- `direct_dependencies`: only each direct dependency ID and its `Status` line;
- `decisions`: the complete Decision records referenced by the selected item.

Dispatch mode accepts a complete Work Item, an exact Step or adjacent Step
range. Scoville Workflow can group consecutive Steps in one worker while
preserving their authored order. `source_text` is
the unchanged selected single-line Step text, adjacent lines, or complete Work
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

This projection does not replace every read operation. Inventory Decision
frontmatter and load relevant proposals separately, or all for a full audit. Read relevant dependency
Evidence, bounded graph state, queued or paused return state, and complete
relevant Work Items separately when the operation requires them. Keep those
reads bounded and never widen the selector response. If Python 3 is unavailable,
load [select-context-without-python.md](select-context-without-python.md) only
for current-or-named recovery or manual unit selection; do not install a runtime. If Python is available but
the helper fails, report its diagnostic and do not invent partial context.

## Read state outside the selector

Use direct reads for Plan or Decision listings, proposal inventory, relevant
dependency Evidence, and graph inspection. These operations complement the
selector; they never replace current-or-named Work Item or dispatch-unit
selection when Python is available.

For a Plan or Decision listing, read only frontmatter and the H1 title unless
the request asks for record content. Read other Work Items only for the
requested state, dependencies, blockers, or authored content. Read a
prerequisite's status for readiness and its full block when its result or
Evidence matters. Inventory Decision frontmatter and surface proposals through
the next section without loading unrelated accepted Decisions.

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

Apply the entrypoint's proposal policy: inventory IDs and status, read and
report relevant proposals (all for a full audit), and request a choice only
for dependent work or explicit Decision handling. Keep unrelated work moving.

## Report the boundary

Name the canonical records that supplied the answer. Do not claim complete
project validation when only the index, selected Work Item, and proposal
summaries were inspected.
