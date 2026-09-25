# Decisions

Use edit.md for safe edits and validation. Allocate the highest ADR number plus
one, without interior reuse or collisions. Store `ADR-0074` in
`docs/decisions/0074-subject.md`. A new proposal follows this template:

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

Recommended result, or the explicit human choice.

## Problem

The unresolved need.

## Drivers

- Supplied or observed constraint.

## Considered alternatives

- Option: material tradeoff.

## Consequences

Benefits, costs and limits introduced by this choice.

## Confirmation

Checks that would verify the choice, not an assertion they already passed.

## Revisit when

Concrete reconsideration trigger.
```

Keep each section's distinct information without invented alternatives or
repeated rationale. New Decisions use the owning Plan's language or request
language. Preserve an existing record's language unless explicitly changed.

## Links and transitions

Work Item Decisions lists own incoming links. Link every affected todo item and
no unrelated item, including for unresolved proposals. Started lists are immutable;
report that limitation rather than changing history. Proposal status does not
remove its links. Creating starts proposed; an already explicit human direction
authorizes immediate acceptance without another question.

Apply only explicitly authorized transitions:

| From | To |
| --- | --- |
| proposed | accepted or rejected |
| accepted | deprecated or superseded |
| deprecated | superseded |

Acceptance adds `accepted: YYYY-MM-DD` between created and scope. Deprecation
retains it. Proposed/rejected omit it. Rejected and superseded are terminal.
Use actual dates no earlier than creation. Generic content edits affect only
proposals and preserve identity and lifecycle. Delete a proposal only after
checking that no Work Item or Decision links to it.

Supersession preserves both records: create the accepted replacement with
`supersedes: ADR-0001` after scope, and set old status superseded with reciprocal
`superseded_by: ADR-0002` after any supersedes. An authorized change to accepted
or deprecated content uses this route, never an in-place rewrite. Replace links
in affected todo items. If still-relevant started work would need a new link,
stop that dependent change and report the immutable-record limit. Terminal
historical links alone do not block replacement. Rejection in favor of another
proposal is not supersession.

## Existing batch metadata

Write new accept/reject transitions individually and validate after each
completed operation. Never create transition_batch or transition_batch_members.
Preserve those fields when already present, including later lifecycle changes.
Existing batch IDs are `batch-YYYYMMDD-N` (positive N) or 64 hexadecimal digits.
Both fields occur together; members are existing unique ADR IDs, each lists
itself, and every member has the same batch ID and complete ordered membership.
Do not recompute historical hashes. The Viewer ignores these fields; validator
and selector retain historical integrity checks. Without Python, General uses
its manual profile reference for complete inspection.
