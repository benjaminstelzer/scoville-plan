# Plan hygiene: selective reads before archive implementation

The local Skill now separates complete byte and structural checks from the
text returned to model context. Routine progress edits reread the changed
frontmatter and complete affected blocks. They no longer require printing the
unchanged remainder of a large Plan. Version 1, immutable history, and the
optional validator remain intact.

The deterministic comparison supports retaining this change. It does not
establish a need for an archive format or measure agent compliance, provider
tokens, latency, or monetary savings.

## Reproduce and inspect

The [frozen protocol](plan-hygiene/protocol.json) records the implementation,
validator, fixture source, test, and extraction-script hashes before the
comparison. The [baseline manifest](plan-hygiene/baseline/manifest.json) and four
source snapshots preserve the previous rules. The
[raw result](plan-hygiene/results.json) retains all 24 operation comparisons,
four guard traces, and two valid successor-Plan cases.

Run from the repository root while the frozen sources still match:

```text
python -B tests/plan_hygiene_experiment.py
python -B -m unittest discover -s tests -p test_plan_hygiene.py -v
```

The experiment writes only disposable synthetic fixtures and prints JSON. It
does not edit real Plans, implement archives, or invoke an agent. A changed
frozen source causes an explicit failure; use a new protocol and retain the old
result when testing a later candidate.

## Method and limits

Four synthetic profiles contain 8 or 160 Work Items with either a completed
prefix or completed items interleaved with open items. Each has an active item,
an earlier completed prerequisite, retained evidence, an accepted Decision, and
a separate unresolved proposal. Their six requests cover resume, progress,
prerequisite inspection, historical evidence, item inventory, and complete audit.
No representative real large project was supplied or evaluated.

Both baseline and candidate use the same required initial context. Baseline
resume is already selective. For progress, the baseline adds the entire updated
Plan, matching its explicit post-write reread rule; the candidate adds the
header and changed block. Full byte comparisons and complete validator reads
remain required. Shared hash and validator output are excluded equally; table
values measure Plan and required Decision/index text, not total conversation
input. The changed Skill instructions' own size is separate overhead.

Across the four edited Skill files, guidance grew by 3,523 characters: 201 in
Core, 1,143 in the read-only route, 1,893 in native editing, and 286 in validation.
Only routed references are loaded. This added instruction payload is excluded
from the table, so the table does not demonstrate a total-context improvement
for a one-off resume or audit. Repeated progress edits are the targeted saving.

The archive arm is a hand-authored display projection that retains every
original block and reconstructs their original order and bytes. It selects the
same facts as the candidate plus routing text. This tests whether moving those
same selectively retrieved facts inherently saves output. It cannot test
whether smaller physical files improve a real agent's read choices, retrieval
reliability, or editing ergonomics. It is not an implemented archive consumer.

No tokenizer was installed in the selected Python runtime. Results therefore
use exact Unicode-character and UTF-8-byte counts, with tokens and provider
usage explicitly unavailable. No paid model calls were made.

## Observed returned text

| Fixture | Completed items | Progress baseline characters | Progress selective characters | Reduction in this scripted operation |
| --- | ---: | ---: | ---: | ---: |
| 8 items, prefix | 6 | 9,117 | 4,148 | 54.50% |
| 8 items, interleaved | 5 | 9,139 | 4,148 | 54.61% |
| 160 items, prefix | 128 | 117,089 | 4,148 | 96.46% |
| 160 items, interleaved | 127 | 117,111 | 4,148 | 96.46% |

These percentages describe the scripted progress operation only. They are not
token-cost reductions or observed agent results. Resume, prerequisite lookup,
history lookup, inventory, and full audit have identical baseline and candidate
output in these cases. A full audit still exposes the complete requested history;
an all-item inventory still grows with the graph.

The archive projection saves no additional required text over selective reads.
Its routing adds 81 characters in this illustrative representation and some
operations require another Plan-section lookup. That number is not a prediction
of a future archive implementation. Archive versioning, conversion, upkeep, and
recovery effort have not been measured; they remain additional implementation
work, not a hidden zero-cost assumption.

At an actual completed-goal boundary, native successor routing returned 2,389
characters with either 8 or 160 retained completed items in the predecessor.
Both complete profiles validated. This is a separate valid lifecycle case,
not a shortcut for an unfinished goal or a live same-Plan dependency.

## Preservation checks

Seven focused tests verify current work and proposal visibility, targeted
prerequisite/evidence retrieval, ordered inventory, complete audits, rejection
of ambiguous duplicate block IDs, hidden terminal-evidence defects, and scoped
progress editing with unchanged surrounding bytes and stale-source refusal.

For each measured profile, the existing validator accepted the original and
scoped progress result. It rejected a missing dependency injected into an
unreturned historical block. Whole-file equality and SHA-256 detected that
outside-slice change. The archive projection reconstructed all authored blocks
without loss. These checks prove fixture behavior, not human authority or the
truth of synthetic acceptance entries.

The complete repository suite passed 57 tests, including the seven new hygiene
tests. Agent Skill validation passed, and the package/report links resolve. All
seven pre-existing dirty or untracked file fingerprints remained unchanged.

A PowerShell-only boundary extraction against the active local Plan returned
the complete 2,070-character W-001 block from an 11,455-character file and
confirmed unchanged SHA-256. Python was not involved in that extraction. This
demonstrates the no-Python read path; it is not complete manual profile validation.

## Recommendation

Keep selective reading and use ordinary successor Plans at real goal boundaries.
The current evidence does not justify implementing an archive format. The
remaining question is empirical: does a real large project still cause agents
to load substantial irrelevant history despite the corrected guidance? If so,
retain those traces and compare archive ergonomics before selecting its format.

On 2026-09-05 the user selected this recommendation. PLAN-0005 was completed
after removing its two unstarted conditional archive items. No project was
converted, no archive schema adopted, and no installed Skill or release changed.
