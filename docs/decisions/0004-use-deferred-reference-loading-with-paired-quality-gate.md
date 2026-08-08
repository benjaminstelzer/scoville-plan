---
format_version: 1
id: ADR-0004
status: accepted
created: 2026-08-08
accepted: 2026-08-08
scope: skill/loading
---

# Use deferred reference loading with a paired quality gate

## Decision

Implement a second bounded Scoville Plan loading candidate that loads routed
references when their operation begins, reuses an already loaded unchanged
Skill reference without rereading it, and adds the Work Item guide to Plan
creation only when Work Items are authored. Keep every format, authority,
evidence, validation, standalone, and family-composition rule unchanged. Adopt
the candidate in the working tree only if the frozen paired benchmark meets
the non-inferiority quality gate and the Plan-owned repeated-read gate;
otherwise restore the released baseline.

## Problem

The first loading candidate reduced the narrow route but increased full-family
Skill payload and unchanged-reference rereads. Its routing table behaved like
an instruction to load operation references during an opening survey, and its
hash-before-reuse wording offered no usable environment signal for deciding
whether a Skill reference had changed. The former all-runs-pass family gate
also failed equally in both arms, so it could not distinguish a candidate
regression from benchmark variance.

## Drivers

- Remove Plan-owned rereads immediately before the first native write without
  suppressing the first route-specific read.
- Preserve every individual evaluator, validator, build, browser, authority,
  evidence, format, lifecycle, standalone, and family-boundary check.
- Separate Plan-owned repeated payload from stochastic sibling-Skill rereads.
- Keep raw provider usage and failed runs auditable without estimates or
  silent replacement.
- Avoid artificial per-run time limits that can waste paid model calls.

## Considered alternatives

- Keep the released baseline. This avoids change risk but retains the observed
  Plan-owned refresh pattern.
- Reuse the first candidate. This is rejected because its family payload and
  repeated-read results regressed.
- Add a hash or stat broker tool. This could expose a formal change signal but
  would change the harness and runtime mechanism instead of fixing the Skill
  wording first.
- Use deferred route loading and session reuse with the existing broker and a
  paired non-inferiority evaluation. This isolates the proposed wording fix
  while retaining the existing quality checks.

## Consequences

Only `scoville-plan/SKILL.md` and
`scoville-plan/references/native-editing.md` are candidate implementation
surfaces; `profile-validation.md`, sibling Skills, and the broker remain at the
released behavior. The evaluation costs twenty Terra Medium calls: six family
and four narrow runs per arm in a counterbalanced order. A passing candidate
may remain in the working tree, but this Decision does not authorize a commit,
push, tag, release, installation, or other remote mutation.

## Confirmation

Have Fable review the exact fix Plan before changing the Skill, then run static
Skill, package, repository, and profile checks. Freeze baseline and candidate
snapshots, prompts, fixtures, evaluators, analyzer, isolation rules, order, and
hashes before model calls. Confirm adoption eligibility from retained raw runs:
candidate strict and record/profile pass counts are not below baseline, no new
Plan-owned failure class appears, candidate Plan-owned repeated-read median is
not above baseline, and no candidate Plan-owned repeat count exceeds the
baseline maximum.

## Revisit when

Revisit this choice if Fable finds a boundary defect in the Plan, the candidate
cannot preserve direct routing, the frozen evaluation fails its adoption gate,
or the runtime later exposes a reliable Skill-change signal that supports a
different reuse contract.
