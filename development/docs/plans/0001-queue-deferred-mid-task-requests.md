---
format_version: 1
id: PLAN-0001
status: completed
created: 2026-09-15
updated: 2026-09-15
---

# Improve deferred work and planning records

## Goal

- Queue mid-task requests without abandoning current work.
- Batch compatible small additions and separate complex outcomes.
- Write Plans and Decisions as compact, ordered instructions that preserve essential facts, name known files, and remain unambiguous to lower-reasoning workers and reviewers.

## Non-goals

- Change host-level message delivery or interrupt mechanics.
- Merge unrelated requests that need different outcomes, acceptance, dependencies, ownership, authorization, or rollout timing.
- Rewrite authored fields of a started Work Item or silently broaden the active Plan beyond its Goal and Non-goals.
- Treat pausing execution for a correction as implicit authority to cancel, rewrite, or switch durable lifecycle state.
- Implement the Skill change as part of creating this Plan.
- Impose arbitrary length limits or remove facts needed for scope, decisions, execution, review, recovery, or verification.

## Work items

### W-001 Define and verify deferred-request queueing

Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: The Skill gives agents one explicit, durable procedure for classifying mid-task user messages and queueing additive work without replacing the current Work Item.
Acceptance: SKILL.md and its routed references distinguish explicit immediate stop or redirect messages, corrections that affect current execution, additive requests, and pure informational or status questions. Frontmatter makes new instructions during an active Plan discoverable without treating questions that require no retained action as Plan work. Additive requests preserve current_item and the current Work Item, merge only compatible small requests into one todo successor, and create separate todo Work Items for complex or independently resumable requests. Separate additions retain stable arrival order unless the user sets another priority, reconcile with existing successors and dependencies, and remain recoverable with the exact intended successor from supported version-1 records without chat-only state or new metadata. A start-eligible successor uses the ordinary guarded complete-and-advance transition. An ineligible successor remains queued with its blocker, proposal, or prerequisite intact, and the ordinary lifecycle resolves any ambiguous replacement without fabricated dependencies, evidence, blocker clearing, or terminal completion. Evaluation cases cover explicit redirection without an error, mixed correction and deferred work, status-only messages, compatible batching, complex separation, repeated additions, restart recovery, an existing successor, scope boundaries, external blockers, unresolved Decisions, later prerequisites, and no eligible replacement. The JSON contracts parse, the Python test suite passes, and a fresh independent review finds no unresolved material defect in the implemented behavior.
Steps:
1. Add the mid-task classification and durable queue operation to SKILL.md with explicit stop, redirect, correction, additive, and informational categories and no implicit lifecycle transition.
2. Define compatible-small batching, complex-item separation, stable arrival order, native-state recovery, dependency-safe insertion, and started-history preservation in planning-granularity.md and native-work-items.md.
3. Define how queued requests interact with Plan scope, Decisions, blockers, existing successors, acknowledgements, start eligibility, complete_and_advance, and ordinary-lifecycle fallback.
4. Add focused evaluation cases and feature-contract coverage, then update README.md and CHANGELOG.md with the supported behavior and limits.
5. Run structural, JSON, and Python checks plus focused model probes, and retain only concise release-linked acceptance evidence.
Evidence: [2026-09-15 JSON contracts parsed and Python suite passed 50 of 50, 2026-09-15 native profile validation passed with 0 errors and 0 warnings, 2026-09-15 git diff check passed, 2026-09-15 Astra reviews ASTRA-SCOVILLE-QUEUE-IMPLEMENTATION-20260915-03 and ASTRA-SCOVILLE-FINAL-20260915-04 approved the corrected implementation and final activation boundary by source inspection]

### W-002 Deferred after W-001: Make planning records compact and execution-ready

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: []
Outcome: Plans and Decisions retain only facts needed to choose, implement, review, resume, and verify work, with ordered steps and direct references to known target files.
Acceptance: The writing contract requires concise fields without losing constraints, causal links, dependencies, decisions, risks, acceptance criteria, or evidence. Procedures use numbered Steps in exact 1., 2., 3. execution order; unordered bullets are reserved for equal-rank facts or criteria. Known target files are named directly in the relevant Step. Plans preserve the concept and implementation order clearly enough for a lower-reasoning worker and an independent reviewer to follow without reconstructing omitted intent. Focused before-and-after fixtures and evaluation cases demonstrate materially lower repetition and token use without ambiguity or schema changes.
Steps:
1. Tighten compact-record ownership and worker-readability rules in scoville-plan/SKILL.md.
2. Define concise Plan, Work Item, and ordered-Step requirements in scoville-plan/references/native-plan-format.md, scoville-plan/references/planning-granularity.md, and scoville-plan/references/native-work-items.md.
3. Define concise Decision facts and rationale boundaries in scoville-plan/references/native-decision-format.md.
4. Add compact low-reasoning-worker and reviewer cases in development/tests/evaluation-cases.json and focused before-and-after fixtures under development/tests/fixtures/record-writing/.
5. Update README.md and CHANGELOG.md, run JSON and Python checks, and obtain an independent Astra Low review.
Evidence: [2026-09-15 JSON contracts parsed and Python suite passed 50 of 50, 2026-09-15 native profile validation passed with 0 errors and 0 warnings, 2026-09-15 git diff check passed, 2026-09-15 compact fixtures reduced characters by 28.2 percent and words by 32.4 percent while retaining required outcomes, 2026-09-15 Astra reviews ASTRA-SCOVILLE-COMPACT-RECORDS-20260915-02 and ASTRA-SCOVILLE-FINAL-20260915-04 approved the corrected compact-record contract and final integrated Skill by source inspection]
