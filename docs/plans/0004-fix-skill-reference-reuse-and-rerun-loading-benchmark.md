---
format_version: 1
id: PLAN-0004
status: completed
created: 2026-08-08
updated: 2026-08-08
---

# Fix Skill-reference reuse and rerun the loading benchmark

## Goal

Produce a Fable-reviewed Scoville Plan loading fix that prevents avoidable
Plan-owned reference refreshes without suppressing required first reads, then
measure its quality and token effect against the released baseline with a
frozen, isolated, provider-reported A/B evaluation.

## Non-goals

- Do not change the Skill, benchmark harness, evaluators, or retained benchmark
  evidence before Fable has reviewed this Plan.
- Do not weaken or remove any individual format, authority, evidence,
  lifecycle, validator, test, build, browser, standalone, or family-boundary
  check.
- Do not change `profile-validation.md`, sibling Scoville Skills, broker
  transport, or add a hash or stat tool in this candidate.
- Do not add estimated Skill tokens to provider-reported usage or count one
  Skill read twice through separate accounting.
- Do not impose an artificial per-run timeout or silently replace a failed,
  contaminated, or incomplete run.
- Do not commit, push, tag, release, install, or otherwise publish the
  candidate without separate authorization.

## Work items

### W-001 Produce a Fable-reviewed fix specification

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0004]
Outcome: The exact implementation boundaries, benchmark protocol, adoption gate, and rollback rule are reviewed by Fable before any Skill or harness file changes.
Acceptance: Fable reviews this Plan and ADR-0004 read-only against the released Skill, rejected candidate, retained raw runs, and current Scoville-family boundaries; every actionable contradiction or missing safeguard is corrected while this Work Item remains editable; the review is retained in the audit; native profile validation passes; and the scoped diff proves no Skill or benchmark-harness file changed before review completion.
Steps:
1. Preserve the released baseline, rejected candidate, raw-run, protocol, analyzer, and result evidence paths in the Fable prompt.
2. Ask Fable in the existing consultation to inspect only the fix Plan, Decision, loading mechanism, family boundaries, quality gate, and smallest sufficient corrections.
3. Verify each finding against repository evidence and revise only the still-todo Plan or, if a material accepted choice must change, record the required Decision lifecycle explicitly.
Evidence: [Fable 5 High session 451a33bc-8cac-4f09-b0b0-2c2c05c1322e returned ready after corrections, audit records the five reviewed findings and applied Plan corrections, native profile validator returned zero errors and warnings, scoped diff showed no Skill or benchmark-harness edit before review completion]

### W-002 Implement the bounded deferred-loading candidate

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0004]
Outcome: A reviewable candidate changes only Scoville Plan route timing and unchanged-reference reuse while preserving all supported operations and standalone or family guarantees.
Acceptance: `scoville-plan/SKILL.md` states that mutation routes share `native-plan-format.md` and `native-editing.md`, loads this Skill's operation-specific references when the operation begins rather than during an opening survey, treats a routed reference as satisfied only after a successful read of its full logical path in the current session, thereafter reuses it without rereading unless the environment reports a Skill change or its content is no longer available in the current context, never counts a same-named reference of another Skill or a Core description toward that read, and includes `native-work-items.md` when a created or restructured Plan authors Work Items; `native-editing.md` uses the same environment-reported-change contract while always rereading live project state; `profile-validation.md`, sibling Skills, and broker behavior are byte-identical to the released baseline; a candidate-v2 retained-rule map naming, for every rule absent from Core relative to the released baseline, its owning reference and the routing row that loads that reference in each supported flow where the rule applies, plus direct links, package file list, Skill validator, repository tests, profile validator, token counts, and complete scoped diff pass.
Steps:
1. Reconstruct only the safe compact routing and core wording from the rejected candidate while retaining the released profile-validation guidance.
2. Apply Fable's reviewed deferred-load, unchanged-reference reuse, and conditional Work Item route language to the two authorized Skill files.
3. Create a candidate-v2 rule-retention map and run all static, package, repository, profile, link, token, and scoped-diff checks before model calls.
Evidence: [candidate changed only SKILL.md and references/native-editing.md, candidate-v2 retention map proves owner and route reachability, Skill quick validator passed, 36 repository tests passed, native profile validator returned zero errors and warnings, all 9 direct Core links resolve and the 12-file package list is unchanged, profile-validation.md and all three sibling Skills are byte-identical to baseline, raw o200k Core tokens fell from 2207 to 1924, raw o200k narrow tokens fell from 2590 to 2307, raw o200k family-route tokens fell from 8293 to 8063, scoped diff and whitespace check passed]

### W-003 Run the frozen paired Terra Medium evaluation

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: [ADR-0004]
Outcome: Retained raw evidence determines whether the second candidate reduces Plan-owned repeated Skill payload without a quality regression in standalone and complete-family use.
Acceptance: The released baseline and candidate each run six family and four narrow fresh isolated Terra Medium Medium-effort trials with identical prompts, fixtures, sibling Skills, broker, tokenizer, corrected analyzer, evaluator checks, and a frozen counterbalanced ABBA/BAAB order; no call receives an artificial per-run timeout; all failures remain retained; every run records direct cached input, uncached input, output, reasoning output, total usage, literal Skill payload, Plan-owned and sibling-owned repeated payload, first-read positions, isolation, profile, test, build, browser, and evaluator results; on each route separately, candidate strict-pass and record/profile-pass counts are not below baseline; Plan-owned failure classes are the frozen family record-check and profile-validator identifiers fixed before any model call, and no candidate run fails a class that no baseline run fails; candidate Plan-owned repeated-payload median is not above baseline and no candidate Plan-owned repeat count exceeds the baseline maximum; candidate narrow Skill-payload median is below baseline; on neither route does the candidate Skill-payload or uncached-input median exceed baseline by more than that route's baseline between-run range; and each retained run records whether any repeated Plan-owned read occurred between the final fixture inspection and the first fixture write.
Steps:
1. Create a new v3 evaluation directory without modifying either retained v1 or v2 evidence and freeze all sources, snapshots, evaluators, analyzer tests, order, and hashes before model calls.
2. Execute all twenty calls sequentially, retain incomplete or failed calls without substitution, and complete deterministic profile, test, build, browser, and evaluator-owned checks.
3. Recompute the primary mechanism and quality gates plus secondary narrow payload, family payload, cached input, uncached input, output, and sibling-repeat measures from raw records.
Evidence: [v3 attempted all 20 frozen calls with 19 valid and retained family-baseline-r2 invalid without replacement, review/results.json records reject because family baseline metric completeness is false, candidate Plan and profile records passed 6 of 6 versus baseline 4 of 5 measurable, candidate family Plan-repeat payload median was 605.5 versus baseline 1812, project profile and browser evaluators completed for every applicable valid fixture, external audit records the raw-rollout cause of the family-candidate-r3 cache outlier]

### W-004 Adopt or restore the candidate and reconcile claims

Status: done
Depends on: [W-003]
Blocked by: []
Decisions: [ADR-0004]
Outcome: The working tree and concise benchmark documentation reflect the measured gate result without rewriting earlier evidence or implying publication.
Acceptance: A candidate meeting every frozen primary and quality gate remains in the working tree; a failing candidate is restored byte-for-byte to the released baseline; the new Markdown and machine-readable benchmark result link retained evidence and distinguish provider-reported cached input, uncached input, output, total usage, literal Skill payload, Plan-owned repeats, and sibling repeats; all published aggregates independently recompute; all links, repository tests, Skill validation, native profile validation, and complete scoped diff pass; no commit, push, tag, release, installation, or remote mutation occurs.
Steps:
1. Apply the frozen adoption rule without changing thresholds after seeing results.
2. Restore the baseline on failure or retain the candidate on success, preserving both snapshots and all raw calls.
3. Add the concise v3 result and audit evidence, recompute every published number, and run the complete final validation set.
Evidence: [SKILL.md and references/native-editing.md match their frozen release-baseline SHA-256 values byte-for-byte, v3 Markdown and JSON report links and retained evidence hashes were added, published v3 JSON fields independently match raw analyzer aggregates, all relative Markdown links resolve and git diff check passed, all 36 repository tests passed, Agent Skill quick validation passed, native profile validation returned zero errors and warnings]
