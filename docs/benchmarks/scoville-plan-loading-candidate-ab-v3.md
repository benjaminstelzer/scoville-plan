# Scoville Plan loading candidate v3

Date: 2026-08-08

Terra Medium ran four narrow and six full-family trials per arm in a frozen,
isolated ABBA/BAAB schedule. All 20 calls were attempted; 19 are valid. The
retained `family-baseline-r2` call used an invalid Skill ID and has no provider
usage. It was not retried or replaced.

## Result

**Rejected for adoption because the frozen metric-completeness gate failed.**
The measurable results show no candidate quality regression, but cannot replace
the missing sixth family-baseline result. The two candidate files were restored
byte-for-byte to the released baseline.

| Route | Condition | Strict | Plan/profile | Cached median | Uncached median | Output median | Provider-total median | Skill-payload median | Plan-repeat median |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Narrow | Baseline | 4/4 | 4/4 | 124,032 | 15,631 | 824.5 | 136,783.5 | 2,840 | 0 |
| Narrow | Candidate | 4/4 | 4/4 | 125,312 | 21,567.5 | 945 | 153,199 | 2,546 | 0 |
| Family | Baseline | 3/5 measurable | 4/5 measurable | 473,088 | 55,695 | 9,158 | 538,805 | 23,201 | 1,812 |
| Family | Candidate | 3/6 | 6/6 | 375,552 | 47,212 | 8,651.5 | 430,165 | 21,386.5 | 605.5 |

No candidate family run failed a Plan-owned record or profile check. Candidate
family Plan-repeat payload fell 66.6%, Skill payload fell 7.8%, and cached-input
median fell 20.6%. Narrow Skill payload fell 10.4%; narrow uncached-input median
rose 38.0% but stayed below the frozen baseline maximum of 28,546.

`family-candidate-r3` is the cached-input outlier at 856,320. Its Skill payload
was the smallest candidate-family payload and it made no successful repeated
Skill read. A malformed Skill call and a premature fixture read split the work
into seven model cycles instead of five; the two extra late continuations
replayed the enlarged cached prefix. Provider output contains only aggregate
turn usage, so the extra 368,896 cached tokens versus r2 cannot be divided
exactly between those two requests.

Raw evidence is retained locally under
`Z:\Projekts\AI\docs\evaluations\scoville-plan-candidate-ab-v3`. Machine-readable
aggregates and evidence hashes are in
[scoville-plan-loading-candidate-ab-v3.json](scoville-plan-loading-candidate-ab-v3.json).
