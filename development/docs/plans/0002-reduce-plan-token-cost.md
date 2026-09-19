---
format_version: 1
id: PLAN-0002
status: cancelled
created: 2026-09-16
updated: 2026-09-17
---

# Reduce Plan token cost without weakening recovery

## Goal

- Reduce the tokens needed to store and consume Scoville Plans while preserving exact scope, lifecycle, execution order, acceptance, evidence, and safe resumption by a fresh lower-reasoning worker.
- Prefer removal of repeated information over private notation, abbreviated field names, or implicit semantics.

## Non-goals

- Optimize general Skill prose, routing, or reference loading.
- Change Plan behavior, authority, lifecycle, or evidence requirements merely to reduce size.
- Adopt a format change before measured token savings and cold-start recovery results justify its compatibility and migration cost.
- Treat character count, visual compactness, or structural validation as proof of token efficiency or semantic sufficiency.

## Work items

### W-001 Establish a Plan token and recovery baseline

Status: todo
Depends on: []
Blocked by: []
Decisions: [ADR-0001]
Outcome: A representative corpus measures current Plan token cost and the ability of fresh workers to reconstruct and resume the recorded work without chat context.
Acceptance: The corpus covers small, ordered, blocked, Decision-linked, paused, completed, and mixed deferred-queue work. Before variants are created, one compact protocol fixes tokenizer and encoding identity, input bytes, worker model and effort, canonical context, run count, expected facts, safe-action rubric, and paired comparison method. Full-record tokens are measured directly; field counts are diagnostic and need not sum to the full record. Every case scores Goal, Non-goals, status, current_item, dependencies, blockers, proposal authority, Decisions, successor provenance and order, ordered actions, Acceptance, Evidence, terminal behavior, and Next action. Safety-critical recovery must be correct per case. Baseline failures remain failures and trigger corpus or scope correction rather than becoming an acceptable candidate baseline. The declared token gate requires a positive aggregate saving without a per-case token regression that lacks an explicit recovery benefit. Consumption claims count the complete canonical context supplied to the worker, including the index and referenced Decisions.
Steps:
1. Extend `development/tests/fixtures/record-writing/` with representative valid Plans, including one mixed deferred queue with a current item, existing successor, blocked or proposed-Decision successor, explicit arrival order, and expected safe action.
2. Add a read-only measurement harness under `development/tests/` that records tokenizer identity, per-field counts, total counts, and corpus summaries without rewriting fixtures.
3. Add cold-start and resume evaluations to `development/tests/evaluation-cases.json` that use the frozen protocol and require exact reconstruction of the canonical state and first safe action.
4. Record baseline token counts, reconstruction errors, and recurring duplication classes in a concise repository-owned result.
Evidence: []
Next action: Await revised plan scope per ADR-0001 before establishing the baseline.

### W-002 Validate a format-version-1 compact writing profile

Status: todo
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001]
Outcome: A format-version-1 writing profile removes repeated wording while retaining every fact needed to choose, execute, review, resume, and verify work.
Acceptance: Before-and-after Plans remain valid, meet the frozen W-001 token gate, and preserve every required recovery fact and safe action in every case. The profile defines ownership boundaries for titles, Goal, Non-goals, Outcome, Steps, Acceptance, Evidence, and Next action, and identifies intentional redundancy that must remain for direct recovery.
Steps:
1. Produce bounded variants that remove duplicated rationale, repeated subjects, execution diaries, and restated status while preserving canonical field names and order.
2. Compare concise titles, single-owner facts, compact equal-rank bullets, direct Step targets, and result-only Evidence through the frozen W-001 protocol, including adversarial conditions, exceptions, time bases, thresholds, metrics, uncertainty, and reference frames.
3. Record the supported candidate profile and rejected compressions with their measured failure modes in the W-001 evaluation result, naming `scoville-plan/references/native-plan-format.md` and `scoville-plan/references/planning-granularity.md` only as later implementation targets.
Evidence: []
Next action: Create the first format-version-1 variants from the W-001 corpus after baseline revision.

### W-003 Decide whether structural compression is justified

Status: todo
Depends on: [W-002]
Blocked by: []
Decisions: [ADR-0001]
Outcome: An evidence-backed proposal determines whether any remaining token cost justifies a compatible structural change or a new format version.
Acceptance: The proposal separately measures the cost and recovery value of explicit empty lists, full field labels, title and Outcome overlap, Steps and Next action overlap, repeated IDs, and frontmatter. Each candidate states token savings, ambiguity risk, direct-resume cost, validator impact, migration impact, and compatibility boundary. Version-1 records retain their existing interpretation; incompatible syntax requires a new version and an accepted support and migration boundary. Every material format choice is recorded as a proposed Decision and linked to every affected mutable Work Item before dependent implementation. Retaining the existing contract without a material choice needs no Decision; material choices require acceptance even without a schema change. An evidence-backed no-safe-gain result returns for an explicit scope choice and does not authorize W-004.
Steps:
1. Measure each suspected structural redundancy independently against the validated W-002 profile.
2. Reject candidates whose savings depend on private notation, inferred absence, hidden chat context, or weaker cold-start recovery.
3. Compare a no-schema-change result with the smallest viable compatible change and, only when necessary, a new-version alternative.
4. Record material choices as proposed Decisions linked to every affected mutable Work Item and require acceptance before dependent implementation.
Evidence: []
Next action: Measure explicit empty lists and field labels against the W-002 profile after W-002.

### W-004 Implement and verify the selected Plan-writing improvement

Status: todo
Depends on: [W-003]
Blocked by: []
Decisions: [ADR-0001]
Outcome: The selected Plan-writing contract and its compatibility boundary are implemented with measurable token savings and unchanged recovery behavior.
Acceptance: `scoville-plan/references/native-plan-format.md`, `scoville-plan/references/planning-granularity.md`, selected validator or contract files, `development/tests/evaluation-cases.json`, `development/tests/fixtures/record-writing/`, README.md, and CHANGELOG.md agree on the selected contract where affected. The complete test suite and frozen W-001 protocol pass. Version-1 records retain their existing interpretation unless an accepted Decision establishes a new version and support boundary. An independent review reports no unresolved material defect.
Steps:
1. Apply the accepted contract to `scoville-plan/references/native-plan-format.md` and `scoville-plan/references/planning-granularity.md`, limited to the files and compatibility boundary selected by W-003.
2. Update `development/tests/evaluation-cases.json`, `development/tests/fixtures/record-writing/`, and only the validator or contract files affected by the selected change.
3. Update README.md and CHANGELOG.md with the measured benefit, compatibility boundary, and rejected unsafe shortcuts.
Evidence: []
Next action: After W-003, apply its accepted contract to the selected canonical format references.