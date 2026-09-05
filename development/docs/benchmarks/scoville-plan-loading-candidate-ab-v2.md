# Scoville Plan loading candidate

Date: 2026-08-08

Terra Medium ran three fresh isolated repetitions per arm on a narrow Plan-only
task and a full four-Skill task. Both arms used unstructured `read_skill`
results. All 12 model runs were valid; failed quality checks remain included.

## Result

**Rejected.** The candidate improved the narrow route but failed the frozen
family payload, repeated-read, and quality-parity gates.

| Route | Condition | Cached median | Uncached median | Output median | Provider-total median | Skill-payload median | Repeated payload |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Narrow | v1.2.0 | 133,120 | 18,620 | 930 | 156,753 | 2,840 | 0 |
| Narrow | Candidate | 130,816 | 14,266 | 950 | 151,702 | 2,410 | 0 |
| Family | v1.2.0 | 454,912 | 47,631 | 8,180 | 514,228 | 22,897 | 1,812 |
| Family | Candidate | 397,312 | 49,801 | 9,172 | 447,454 | 23,741 | 3,149 |

Skill payload is the exact successful `read_skill` tool text tokenized with
`o200k_base`; it is not added to provider usage. Provider total is reported
`input_tokens + output_tokens`; reasoning output remains separate.

## Quality

The narrow route passed 3/3 in both arms. Full-family strict quality passed 1/3
in both arms: all six builds and browser evaluations passed, while authored
tests passed 1/3 baseline and 2/3 candidate, and native profile validation
passed 3/3 baseline and 2/3 candidate. The candidate repeated more successful
unchanged references in two of three paired family runs.

The first frozen series is retained but invalid: recoverable tool errors were
aborted and correct narrow answers were rejected for punctuation. The v2
protocol changed only those harness defects. A post-run analysis correction
excluded failed `read_skill` calls from the successful-payload metric and
preserved the superseded result hashes.

Transport probing separately observed duplicate structured and unstructured
result fields. Provider-request double counting remains unknown, so both v2
arms used unstructured results and make no transport-cost claim.

Machine-readable aggregates and provenance hashes:
[scoville-plan-loading-candidate-ab-v2.json](scoville-plan-loading-candidate-ab-v2.json).
