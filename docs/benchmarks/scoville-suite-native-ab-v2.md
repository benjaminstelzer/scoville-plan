# Complete Scoville suite cost benchmark

Date: 2026-08-08

This controlled A/B test compares no Skills with exactly the four Scoville
Skills: Code `v1.0.6`, Scribe `v1.0.6`, UI `v1.0.6`, and Plan `v1.2.0`.
`gpt-5.6-sol` Medium and `gpt-5.6-terra` Medium each ran the same integrated
calculator task three times per condition. Every run started in a fresh
repository and session. Native runs exposed no Skill files and no Skill-reading
tool; family runs exposed only the four frozen packages.

The task required Plans, an accepted linked Decision, code, tests, responsive
Mantine UI, accessible behavior, interface wording, and an honest handoff.
All twelve calls completed with valid condition isolation and final provider
usage. No failed call was silently replaced.

## Token cost

Provider total is `input_tokens + output_tokens` and includes cached input.
Reasoning output is reported separately and is not added again.

This retained benchmark used structured Skill-tool results. A later transport
probe observed an identical duplicate result envelope but could not determine
whether the provider billed both fields. The totals below remain direct
provider usage; they are not literal Skill-package cost and should not be
compared as though transport overhead had been removed.

| Model | Condition | 3-run provider total | Median per call | Uncached input | Cached input | Output | Strict quality |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol Medium | No Skills | 468,724 | 168,260 | 94,323 | 337,408 | 36,993 | 2/3 |
| Sol Medium | Four Skills | 2,530,064 | 892,546 | 217,492 | 2,267,136 | 45,436 | 3/3 |
| Terra Medium | No Skills | 519,181 | 178,785 | 75,141 | 420,608 | 23,432 | 1/3 |
| Terra Medium | Four Skills | 1,635,349 | 561,864 | 162,253 | 1,442,304 | 30,792 | 2/3 |

| Family increase | Provider total | Uncached input | Cached input | Output | Median elapsed |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol Medium | +439.8% | +130.6% | +571.9% | +22.8% | +40.7% |
| Terra Medium | +215.0% | +115.9% | +242.9% | +31.4% | +28.9% |
| Both models | +321.6% | +124.1% | +389.4% | +26.2% | +25.9% |

The complete twelve-call benchmark consumed 5,153,318 provider tokens:
5,016,665 input, including 4,467,456 cached and 549,209 uncached, plus 136,653
output. Reasoning output was 32,799. These are token-volume measurements, not a
currency estimate. No applicable public price was established for these exact
model aliases, and cached input cannot be priced as ordinary input without the
relevant provider contract.

## Quality qualification

The strict gate requires Plan and Decision quality, a passing authored test
suite, a production build, independent browser behavior, and rendered layout.

| Measure | No Skills | Four Skills |
| --- | ---: | ---: |
| Valid isolated calls | 6/6 | 6/6 |
| Plan and accepted Decision quality | 6/6 | 6/6 |
| Canonical Scoville Plan profile | 0/6 | 6/6 |
| Read-only profile-validator pass | not applicable | 6/6 |
| Production build | 6/6 | 6/6 |
| Agent-authored test suite | 5/6 | 5/6 |
| Browser-quality gate | 4/6 | 5/6 |
| Strict integrated gate | 3/6 | 5/6 |

The family produced two more strict successes in this sample and made the
canonical Plan/Decision profile reliable. It also consumed 4.2 times the
provider-token volume across both models. The largest increase was cached
input, not generated output.

One family run omitted `MantineProvider` from production and could not render.
One native run failed keyboard decimal arithmetic, another overflowed the
360-pixel viewport for a long value, and a third passed browser behavior but
failed its own component tests. Screenshot inspection found coherent but varied
designs in both arms and no general visual-quality win.

## Interpretation

The result supports route-specific activation. Load all four Skills when a
task genuinely spans durable Plans and Decisions, engineering, interface
quality, and variable reader-facing text. It does not support treating the
family as a permanent monolithic prompt.

This is a descriptive result from one task and three samples per cell. The
bundle test cannot attribute the measured benefit or cost to an individual
Skill. [Machine-readable aggregates and run usage](scoville-suite-native-ab-v2.json)
retain the exact values, source hashes, and analyzer revision.

## Analyzer note

The first frozen analyzer incorrectly treated canonical `Acceptance:` criteria
as claims of observed evidence. Its script and result were retained, then a
documented revision restricted canonical false-evidence checks to `Evidence`
and the final response. Two regression tests cover the correction. No task,
model output, or substantive quality criterion changed.
