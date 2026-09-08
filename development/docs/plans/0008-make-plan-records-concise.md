---
format_version: 1
id: PLAN-0008
status: completed
created: 2026-09-08
updated: 2026-09-08
---

# Make Plan records concise and self-owned

## Goal

Give Scoville Plan its own rules and review for precise, compact Plans, Work Items, and Decisions, with clear Scribe exclusion for those records.

## Non-goals

- Change native format version 1, lifecycle authority, or retained history.
- Rewrite accepted Decisions or immutable Work Item content for style.
- Run paid external evaluations or claim unmeasured token savings.

## Work items

### W-001 Define and verify compact record writing

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0007]
Outcome: Plan owns standalone writing rules and a mandatory precision and redundancy check for newly authored or permissibly edited record text.
Acceptance: Representative verbose and already concise records retain every required fact, constraint, alternative, tradeoff, uncertainty, verification criterion, and evidence reference while removing unnecessary repetition. Historical and out-of-scope text stays unchanged, and native structural validation passes.
Steps:
1. Add brief common rules in SKILL.md and field-specific guidance in the Plan and Decision references.
2. Prefer direct sentences and compact bullets where the format allows them. Keep each fact in its canonical field and repeat it only when needed for correct interpretation.
3. Keep Outcome focused on the result, Acceptance on observable proof, and Next action on the first unperformed action. Give each Decision section distinct content.
4. Add a semantic check to creation, permitted edits, and audits. Remove filler and irrelevant chronology without weakening meaning or compressing prose into opaque shorthand.
5. Assess optional read-only warnings for excessive field length or exact repetition. Propose thresholds separately if evidence justifies them, and keep stylistic warnings outside structural validity.
6. Compare candidate outputs with baseline records, document preservation and concision findings, and record observed limitations in the changelog.
Evidence: [Record-writing forward check preserved required meaning and immutable bytes, Eight fixture validations and 57 repository tests passed, See docs/evaluations/record-writing-v1.md for actual outputs and limits]

### W-002 Make record-writing ownership consistent across Skills

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0007]
Outcome: Plan and Scribe route native record creation, permitted rewriting, and wording audits to Plan, including when Scribe is installed.
Acceptance: Observed routing covers Scribe absent, installed, already active for another segment, and explicitly requested. Normal record work adds no Scribe load, mixed tasks retain their separate prose route, explicit user instructions take precedence, and existing lifecycle protections remain effective.
Steps:
1. Add the native-record ownership exception to Plan and mirror it in Scribe's activation rules and applicable routing metadata.
2. Inspect shared routing instructions for conflicts and change only rules that directly contradict the selected exception.
3. Run bounded routing and output cases for creation, rewriting, audit, mixed work, and explicit invocation. Distinguish declared rules from observed behavior.
4. Record scoped verification and limitations in the affected repositories' changelogs for later release review.
Evidence: [Nine fresh Terra Medium routing cases covered standalone mixed and explicit use, Explicit-use ownership and Work Item route gaps corrected and retested with Terra Medium, See docs/evaluations/record-routing-terra-medium/README.md for failures and limits]
