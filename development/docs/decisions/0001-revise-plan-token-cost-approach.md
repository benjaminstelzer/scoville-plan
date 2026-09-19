---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-09-17
accepted: 2026-09-17
scope: project/planning
---

# Revise Plan token cost approach

## Decision
Close PLAN-0002 and revise the token cost reduction strategy to eliminate cryptic pseudo-code while reducing instruction bloat across the Scoville family.

## Problem
PLAN-0002 in its draft state focused narrowly on Plan record storage without addressing the broader instruction density and pseudo-code compression issues identified during the gemini-audit.

## Drivers
- Explicit user instruction to close the current plan item and record a decision that it will be revised.
- gemini-audit findings revealed that pseudo-code compression (e.g. `discovery != installed|active...`) creates parsing friction for LLMs and must be replaced with clear, natural language.
- Token reduction across the Skill family must not compromise cold-start recovery or rely on private abbreviations.

## Considered alternatives
- Keep PLAN-0002 as drafted: Limits token work strictly to docs/plans without resolving Skill-wide instruction overhead.
- Abandon token optimization entirely: Leaves high token consumption and quota pressure unmitigated.
- Revise the approach to unify Plan storage optimization and Skill instruction clarity: Delivers token savings while improving LLM readability and recovery.

## Consequences
- PLAN-0002 is closed with status cancelled, linking this decision.
- A revised plan will be drafted that combines Plan record compaction with instruction streamlining across the Scoville family.
- Maintains format-version-1 compatibility without private shorthand notation.

## Confirmation
1. Run validate_profile.py to ensure docs/decisions/0001-revise-plan-token-cost-approach.md and docs/plans/0002-reduce-plan-token-cost.md pass validation with zero errors.
2. Confirm the Decision is linked in PLAN-0002.

## Revisit when
A comprehensive plan for Scoville instruction and record token optimization is prepared for review.