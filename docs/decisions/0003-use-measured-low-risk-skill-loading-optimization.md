---
format_version: 1
id: ADR-0003
status: accepted
created: 2026-08-08
accepted: 2026-08-08
scope: skill/loading
---

# Use a measured low-risk Skill-loading optimization

## Decision

The proposal recommends separating the benchmark-transport investigation from
a low-risk Scoville Plan text-reduction candidate. The candidate may become the
released Skill only after paired standalone and full-family evaluation shows
the defined token improvement without rule, behavior, or boundary regression.

## Problem

Scoville Plan legitimately loads several references for a full-lifecycle task,
but its core and routed files repeat some guidance and agents have reread
unchanged references. The benchmark harness may also expose both unstructured
and structured copies of a Skill read. Without isolating those mechanisms,
provider usage cannot show which cost belongs to the Skill design and which
belongs to transport.

## Drivers

- Lower unnecessary model-visible Skill payload and uncached input.
- Preserve native format, lifecycle, authority, evidence, direct routing,
  standalone operation, and Scoville-family composition.
- Base token claims on direct provider usage and retained tool payloads without
  adding separate token estimates to reported totals.
- Keep the initial candidate small enough for exact rule-retention mapping and
  paired behavioral verification.

## Considered alternatives

- Keep the current Skill and harness unchanged. This avoids migration risk but
  leaves the suspected transport and repeated-read costs unresolved.
- Change only the harness transport. This can correct benchmark
  representativeness but does not remove duplicated Skill guidance.
- Split Plan-format or Decision-only references immediately. This may save more
  tokens on narrow routes but has a higher risk of hiding integrity rules.
- Measure transport separately and test a bounded text-reduction candidate.
  This costs additional calls but separates the two causal mechanisms.

## Consequences

The transport probe and candidate can proceed independently, while their
results meet in the paired evaluation. The work retains old benchmark evidence
instead of rewriting its provenance. The candidate remains ineligible for
adoption after any rule, quality, lifecycle, standalone, or family-boundary
regression, and a passing evaluation still does not accept this proposal.

## Confirmation

Confirm the recommendation through the frozen transport probe, exact retained
rule and token maps, repository validators, and three paired Terra Medium runs
per arm for both a narrow standalone task and a full-family lifecycle task.
Accepting the Decision remains an explicit human lifecycle transition.

## Revisit when

Revisit the proposal if the transport cannot be isolated, the candidate does
not reduce the defined primary measure, a safety or composition regression is
observed, or future evidence shows that Decision-only routing justifies a
separate higher-risk design.
