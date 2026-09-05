---
format_version: 1
id: ADR-0002
status: accepted
created: 2026-08-08
accepted: 2026-08-08
scope: evaluation/scoville-suite-cost
---

# Use a dual-model no-Skill versus Scoville-suite A/B matrix

## Decision

Measure the complete Scoville suite against a no-Skill control with three
independent runs per condition on both `gpt-5.6-sol` and `gpt-5.6-terra` at
medium reasoning effort. The treatment exposes exactly Scoville Code, Scribe,
UI, and Plan; the control exposes no Skills. Both conditions receive the same
integrated implementation task, which requires repository-owned Plans and
Decisions as well as code, interface behavior, and reader-facing wording.

## Problem

The existing family benchmark covers only Terra Medium and predates the current
Scoville Plan Decision behavior and bundled validator. It cannot establish the
current token cost or quality of the full suite across both frontier model
families requested for the public repository.

## Drivers

- Compare exactly the two requested conditions rather than Skills against an
  `AGENTS.md` substitute.
- Exercise all four Skills in one shared task, including Plans and Decisions.
- Retain per-model results instead of hiding model-specific behavior in one
  pooled number.
- Capture provider token fields and evaluator-owned quality evidence together.
- Make contamination, missing usage, or incomplete evaluation invalidate a run
  without silently replacing it.

## Considered alternatives

- Reuse the previous Terra-only result: cheaper, but it does not test the
  current suite or Sol Medium.
- Compare Skills with an `AGENTS.md` bundle: measures a different delivery
  mechanism than the requested no-Skill control.
- Run one sample per condition: reduces cost but makes a single stochastic run
  dominate the result.
- Run the requested three paired repetitions per model: costs twelve model
  calls but exposes within-model variation and supports paired comparisons.

## Consequences

The benchmark will make twelve sequential isolated model calls plus
evaluator-owned checks. Results must report each model and condition, the
complete twelve-run consumption, quality failures, invalid runs, and sample
limits. Token counts may be reported as observed usage; a currency estimate
requires an applicable verified price and must not be inferred from token
counts alone.

## Confirmation

The frozen protocol, prompt hashes, fixture hash, current Skill tree hashes,
run manifests, instruction-read provenance, raw event streams, provider usage,
and evaluator outputs must make every comparison and aggregate independently
recomputable.

## Revisit when

Revisit when the four Skill trees, model generation, benchmark task, harness,
or provider usage semantics change materially.
