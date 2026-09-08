---
format_version: 1
id: ADR-0007
status: accepted
created: 2026-09-08
accepted: 2026-09-08
scope: planning/record-writing
---

# Let Scoville Plan own record writing

## Decision

Scoville Plan owns wording, brevity, fidelity, and review of its native Plans, Work Items, and Decisions. If Scribe is installed, do not additionally activate or load it for those records. If Plan is unavailable or inactive, Scribe remains usable under the existing record owner's rules. An explicit user instruction to use Scribe takes precedence.

## Problem

Plan specifies record structure but lacks a general concision check. Scribe excludes normal domain records, yet its explicit rewriting trigger can restore overlapping ownership.

## Drivers

- Keep records precise, sufficient for continuation, and inexpensive to reread.
- Give record writing one owner with standalone rules.
- Preserve facts, verification criteria, authority, and authored history.

## Considered alternatives

- Compose Plan with Scribe: retains generic writing guidance but introduces overlapping rules and additional loading.
- Add hard word limits: easy to check but can remove necessary detail or encourage dense sentences.

## Consequences

Plan needs its own brief writing rules and a mandatory semantic review. Scribe needs a matching routing exception. Apply the exception only to native planning records, not unrelated prose in the same task. Any numeric lint threshold remains a separately justified advisory choice.

## Confirmation

Exercise create, permitted rewrite, audit, mixed-task, Scribe-absent, Scribe-installed, and explicit-Scribe cases. Inspect actual routing and output for completeness, repetition, and lifecycle preservation.

## Revisit when

The routing remains ambiguous, compact records lose required facts, or supported record formats change.
