# Decisions

SKILL.md's Decisions section says when to record and link a Decision.

## Create a Decision

Get the ID and filename with `--next-id decision`. Create the Decision as
proposed unless the user has already made the choice it records; record such
a choice as accepted without asking again. A proposal permits nothing.

```text
---
format_version: 1
id: ADR-0074
status: proposed
created: 2026-09-25
scope: project/concern
---

# Concrete choice

## Decision

Recommended result or explicit human choice, with necessary reasons.

## Problem

Background situation.

## Drivers

- Nonbinding background consideration.

## Considered alternatives

- Nonbinding alternative.

## Consequences

Benefits, costs and limits introduced by this choice.

## Confirmation

Checks that would verify the choice, not an assertion they already passed.

## Revisit when

Concrete reconsideration trigger.
```

An accepted Decision adds `accepted: YYYY-MM-DD` between `created` and `scope`.

Write each condition, exception, permission limit and reason that the choice,
its implementation, verification or revisit needs once, in a binding section:
Decision, Consequences, Confirmation or Revisit when. Problem, Drivers and
Considered alternatives hold only background, without discussion history or
unnecessary rationale: the choice must be implementable and verifiable
without them. Write `[]` under a section with nothing to record rather than
invent a consequence, check or trigger.

## Binding mark

Write exactly `Binding sections: complete` as the first non-blank content
line under Decision only when the four binding sections alone carry
everything the choice, its implementation, verification and revisit need.
A context consumer may then deliver the binding sections without
background; unmarked Decisions are delivered complete. If an edit adds binding
content to a background section, remove the mark or move that content to its
binding section. A mark does not change lifecycle, permissions or format
version.

## Links and transitions

A proposal's concrete effect may be recorded in Instructions. Changing a
proposal's status does not remove its links.

Apply only explicitly authorized transitions:

| From | To |
| --- | --- |
| proposed | accepted or rejected |
| accepted | deprecated or superseded |
| deprecated | superseded |

Rejected and superseded Decisions are terminal and stay unchanged. Edit a
proposal's content within the authorized scope. Change an accepted or
deprecated Decision materially only by supersession; equivalent shortening is
cleanup under [maintenance.md](maintenance.md).

Supersession keeps both records:

1. Create the accepted replacement with `supersedes: ADR-0001`.
2. Set the old Decision superseded with `superseded_by: ADR-0002`.
3. Replace the link in affected todo items; in started items, append the
   replacement and keep the older link as history.

Links from done or cancelled items and from completed or cancelled Plans do
not block replacement. Rejecting a proposal in favor of another is not
supersession.
