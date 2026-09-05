---
format_version: 1
id: PLAN-0002
status: completed
created: 2026-08-08
updated: 2026-08-08
---

# Benchmark the complete Scoville suite and its token cost

## Goal

Produce a controlled, reproducible A/B evaluation of no Skills versus exactly
the four Scoville Skills. Run three fresh samples per condition with Sol Medium
and Terra Medium, exercise Plans and Decisions alongside code, UI, and wording,
and publish quality-qualified token totals suitable for the GitHub repository.

## Non-goals

- Do not attribute a bundle-level result to an individual Scoville Skill.
- Do not compare Skills with `AGENTS.md`, ambient Skills, memory, or another
  persistent instruction mechanism.
- Do not silently discard or replace contaminated, failed, or incomplete runs.
- Do not let benchmark agents execute evaluator commands, browse, mutate the
  package baseline, or claim evaluator-owned checks passed.
- Do not convert tokens to currency without an applicable verified price.
- Do not generalize from this task and sample to all repositories or models.

## Work items

### W-001 Freeze the controlled dual-model benchmark

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0002]
Outcome: A new versioned benchmark directory contains one frozen integrated task, current complete Skill snapshots, identical fixtures, an exact run matrix, contamination gates, usage capture, deterministic evaluators, and tests sufficient to start model calls without changing the protocol afterward.
Acceptance: The protocol identifies both models at medium effort, three paired repetitions per condition, sequential counterbalanced order, exactly four treatment Skills, zero control Skills and no control Skill-read capability; the task requires a durable Plan and at least one accepted Decision plus calculator code, responsive Mantine UI, accessible behavior, meaningful interface wording, and truthful handoff; hashes cover the task, fixture, prompts, harness, evaluator, and complete Skill trees; harness tests pass before the first model call.
Steps:
1. Inspect the mature prior family benchmark and retain only protocol and evaluator behavior that still matches the current request.
2. Freeze current released Skill trees, one identical clean fixture, an integrated task with an explicit human Decision, and the twelve-run counterbalanced order.
3. Extend provenance and evaluators for Decision structure, Decision-to-Work-Item links, Skill-package contents, instruction-read isolation, token fields, and model-specific aggregation.
4. Run static and fixture-level harness tests without invoking a model.
Evidence: [8 Python harness tests passed before model calls, 12 fresh manifests share one fixture hash, four released Skill snapshots byte-match source repositories, native MCP schema omits the Skill reader]

### W-002 Execute and retain all twelve isolated trials

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0002]
Outcome: Three native and three complete-suite runs exist for each requested model, with a fresh repository and session per run and enough raw evidence to audit condition isolation and provider usage.
Acceptance: Every scheduled run retains its prompt, model event stream, final response, produced fixture, manifest, Skill-read trace, file operations, timing, and final `turn.completed.usage`; native runs expose no Skill files or Skill-read tool, treatment runs expose only the four frozen Scoville packages, all instruction reads stay within the assigned condition, and any invalid run remains visibly invalid without an unreported replacement.
Steps:
1. Execute the frozen sequential counterbalanced run order one call at a time.
2. After each call, record completion, usage, isolation evidence, and artifact hashes in the benchmark and external audit log.
3. Stop interpretation if the frozen protocol or shared fixture changes after calls begin; retain all affected evidence.
Evidence: [12 of 12 scheduled calls retain final usage, 12 of 12 calls pass condition isolation, all raw rollouts and fixture hashes are recorded in the external audit]

### W-003 Evaluate quality and aggregate token cost

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: [ADR-0002]
Outcome: Evaluator-owned structural, test, build, browser, interface, wording, and reporting checks determine whether the two conditions produced comparable usable results before their token consumption is compared.
Acceptance: The evaluator checks Plan and Decision validity, accepted Decision linkage, next-action progression, source behavior, agent tests, production builds, named interactions, responsive layouts at both viewports, accessible names and live status, error wording and recovery, and truthful final reports; aggregates include per-run input, cached input, uncached input, output, reasoning output, total tokens, and elapsed time, plus per-model sums, medians, ranges, paired deltas, quality gates, and the complete twelve-run token total without double-counting reasoning tokens.
Steps:
1. Run the deterministic profile validator and product evaluator against every retained fixture.
2. Run browser checks and capture rendered evidence for every buildable fixture.
3. Audit validity and contamination before computing per-model and overall descriptive aggregates.
4. Compare token deltas only beside the quality outcomes that make the comparison interpretable.
Evidence: [6 of 6 Family profiles passed the frozen validator, 12 of 12 production builds passed, 10 of 12 authored test suites passed, browser evidence covers all 12 variants, analyzer revision 1 and its corrected revision 2 are both retained]

### W-004 Publish the reproducible GitHub-facing report

Status: done
Depends on: [W-003]
Blocked by: []
Decisions: [ADR-0002]
Outcome: The repository contains a concise public summary and complete local evidence map that state what one run and the requested suite consumed, what quality was observed, and what the small controlled sample does not establish.
Acceptance: The report identifies exact models, effort, conditions, repetitions, task and Skill versions, validity, quality results, token semantics, per-model three-run condition costs, six-run per-model suite costs, complete twelve-run benchmark cost, and limitations; all numeric claims map to retained machine-readable evidence; repository validation and scoped diff inspection pass.
Steps:
1. Generate machine-readable results and a human-readable audit from retained evidence.
2. Add the narrow GitHub-facing benchmark summary without hiding failed or invalid cases.
3. Recompute all aggregates independently and validate links, hashes, profile structure, and the complete scoped diff.
Evidence: [benchmark AUDIT.md maps every claim to retained evidence, GitHub benchmark Markdown and JSON were added, all 12 published run rows match review results, 44 per-model numeric fields match review results, 36 repository tests passed, Markdown links and git diff checks passed]
