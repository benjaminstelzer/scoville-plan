---
format_version: 1
id: PLAN-0003
status: completed
created: 2026-08-08
updated: 2026-08-08
---

# Optimize Scoville Plan loading and token measurement

## Goal

Establish whether the benchmark harness exposes duplicated Skill content to the
model and, independently, reduce Scoville Plan context only where rules or
routing text are provably duplicated. Preserve the native format, lifecycle,
authority, evidence, standalone operation, and family composition while producing direct
provider-usage evidence for any token claim.

## Non-goals

- Do not remove, weaken, or relocate authority, ownership, lifecycle,
  validation, evidence, opt-out, or stop rules beyond their safe loading route.
- Do not make Scoville Plan depend on another Scoville Skill.
- Do not split `native-plan-format.md` or decouple Decision-only operations in
  the initial low-risk candidate.
- Do not add estimated Skill tokens to provider-reported usage or rewrite old
  usage records as though a corrected transport had produced them.
- Do not publish, tag, release, or replace installed Skills as part of this
  Plan without separate authorization.

## Work items

### W-001 Determine the model-facing Skill-read transport

Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: A controlled transport probe shows whether the current annotated `read_skill` return exposes duplicate unstructured and structured content to the model and quantifies any effect on direct provider usage.
Acceptance: Three fresh Terra Medium runs per condition use one frozen prompt, Skill payload, effort, model, evaluator, and counterbalanced order; the variant differs only by disabling structured output for `read_skill`; for every read, the unstructured tool text and returned file SHA-256 are byte-identical across conditions; every run retains the raw rollout, returned tool payload, cached input, uncached input, output, reasoning output, total provider usage, hashes, and isolation result; the conclusion separates observed transport behavior from anything the provider request cannot reveal.
Steps:
1. Freeze a minimal benchmark-local Skill-read probe, payload, evaluator, environment, and source hashes without changing retained benchmark evidence.
2. Run three fresh counterbalanced repetitions with the current transport and three with only `read_skill` structured output disabled.
3. Inspect the model-visible tool results and direct provider usage, retain failed or contaminated runs, and state whether transport duplication is observed, excluded, or still unknown.
Evidence: [3 broker tests passed before model calls, protocol SHA-256 036169808560B1D883CE333B24079B0A4E6F1A1B7909C315E53432FD08CF8375 frozen, v1 structured-r1 retained invalid after zero tool calls, v2 protocol SHA-256 0FEA4B3EFD1A41782DB2A48C9CCD5F11E15EDCC7FAFA8397888F1BBAE3CF467D frozen, v2 structured-r1 retained invalid after bare tool name was unavailable, v3 protocol SHA-256 BA91E60F8EC39F7845A814097EEB419D0CB9B38B9B14CA2CE0129304F94E2A65 frozen, v3 structured-r1 retained invalid while direct MCP listing passed, v4 protocol SHA-256 110B3CF56A93E23E41069752C288F3D8E8353F61A4F20262B55B8641DB013802 frozen, v4 structured-r1 retained invalid after broker-wide approval, v5 protocol SHA-256 9669E247874C867AF3C9ED20A3BE1A28D2111143C49999B3EB450CC4E9CF621D frozen, v5 structured-r1 retained invalid after fallback response, v6 protocol SHA-256 9D0CA11C187DABD75C03FE96C9262CF8CE5726D29756C9A1AAA84867315ADB82 frozen, v6 6 of 6 runs valid with byte-identical text and file hashes, v6 AUDIT.md records observed envelope duplication and unknown provider double-counting]

### W-002 Produce a low-risk Scoville Plan loading candidate

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0003]
Outcome: A reviewable candidate reduces always-loaded and repeatedly loaded Scoville Plan text without changing any supported operation, rule, direct route, or standalone guarantee.
Acceptance: The candidate moves the unchanged-reference hash and no-reload rule into the core, retains only the Work Item invariants that at most one item is `in_progress` and equals `current_item` and that `done` requires observed acceptance evidence, replaces duplicated after-writing prose with direct routed guidance, compresses repeated routing and validator diagnostics only where every reference path remains discoverable, and records exact before-and-after o200k token counts; the bundled Skill validator, repository tests, native profile validator, retained-rule map, package-file checks, and scoped diff all pass before behavioral evaluation.
Steps:
1. Map every proposed move or deletion to its single retained authoritative location and reject any edit that would hide a required standalone rule.
2. Apply only the mapped core, routing, editing, Work Item, and profile-validation reductions while leaving Plan-format and Decision-only routing unchanged.
3. Recount core, routed-reference, and representative route tokens and run all static, package, profile, and repository checks.
Evidence: [W002-retention-map.md maps every moved or compressed rule, quick_validate passed, 36 repository tests passed, native profile validator returned zero errors and warnings, all 9 direct reference files resolve, core reduced from 2207 to 1785 o200k tokens, full lifecycle route reduced from 8293 to 7798 o200k tokens, scoped diff and whitespace check passed]

### W-003 Prove standalone and family behavior parity

Status: done
Depends on: [W-001, W-002]
Blocked by: []
Decisions: [ADR-0003]
Outcome: A frozen paired evaluation determines whether the candidate lowers Skill-read and provider token cost while matching the released baseline in standalone Scoville Plan use and complete Scoville-family composition.
Acceptance: An immutable released baseline and candidate are each run three times with Terra Medium on one narrow Plan-only task and one full-lifecycle four-Skill task using fresh isolated sessions, identical fixtures, counterbalanced order, no ambient Skills, one identical transport configuration selected from W-001, direct usage capture, deterministic profile validation, evaluator-owned acceptance checks, and complete Skill-read traces; all failures remain retained; adoption eligibility requires no quality, authority, evidence, format, lifecycle, standalone, or family-boundary regression, no candidate run with more repeated reads of an unchanged reference than its paired baseline run, a lower candidate median repeated-read payload wherever the baseline median is nonzero, and, as the primary measure, a lower candidate median model-visible Skill-payload cost on at least one route with no payload median increase on the other route exceeding the corresponding baseline between-run range and no uncached-input median increase on either route exceeding its baseline between-run range; adoption itself occurs only through explicit acceptance of ADR-0003.
Steps:
1. Freeze baseline and candidate trees, the two task prompts, fixtures, evaluators, contamination gates, hashes, and twelve-run order before model calls.
2. Execute and retain all standalone and family trials with direct provider usage and reference-read traces.
3. Compare structural validity, task quality, rule fidelity, cached and uncached input, output, total usage, Skill payload, and repeated reads before accepting or rejecting the candidate.
Evidence: [Frozen acceptance matrix defines every pre-model gate, narrow fixture passes the released validator with zero errors and warnings, five initial broker tests pass, all 12 invalid v1 calls remain retained, v2 protocol SHA-256 0B97FBEECE503E8DC799392CEA42FC050BA5FADE172955A74BFF2912D2A5CAD0, all 12 v2 model runs are valid, all six family builds pass, all six family browser evaluations pass, baseline family quality passes one of three runs, candidate family quality passes one of three runs, candidate narrow Skill payload median falls from 2840 to 2410 o200k tokens, candidate family Skill payload median rises from 22897 to 23741 o200k tokens, candidate family repeated-read median rises from 2 to 3, corrected analyzer verdict is reject, rejected Skill candidate was restored to the released baseline]

### W-004 Reconcile benchmark and README claims

Status: done
Depends on: [W-001, W-003]
Blocked by: []
Decisions: [ADR-0003]
Outcome: Repository documentation states the transport finding, accepted or rejected optimization result, and direct token evidence without obscuring the provenance of earlier benchmark runs.
Acceptance: Every affected benchmark and concise README claim distinguishes provider-reported cached input, uncached input, output, total usage, literal Skill payload, and any observed transport overhead; original results and hashes remain auditable; superseded interpretations receive a specific correction rather than silent replacement; links, numeric recomputation, repository validation, and the complete scoped diff pass with no release or remote mutation.
Steps:
1. Inventory every repository claim whose interpretation depends on Skill-read transport or the candidate token counts.
2. Add the minimal correction and result summaries with direct links to retained machine-readable evidence.
3. Recompute every published aggregate independently and validate links, profile structure, and the complete scoped diff.
Evidence: [README and complete-suite benchmark claims use direct provider usage without adding literal Skill payload, earlier structured read_skill transport is now known to duplicate the returned envelope while provider-request double counting remains unknown, rejected-candidate Markdown and JSON records were added, README and Changelog contain the concise rejection result, 24 published token fields recompute from raw summaries and rollouts, protocol and result hashes match, every published quality count matches evaluator output, all Markdown links resolve, 36 repository tests pass, canonical Skill validation passes, native profile validation returns zero errors and warnings, complete diff whitespace check passes]
