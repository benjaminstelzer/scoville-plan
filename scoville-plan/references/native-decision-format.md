# Decisions

Use edit.md for safe edits and validation. Allocate the highest ADR number plus
one, without interior reuse or collisions. Read the next ID and filename pattern
with `select_context.py --root "<project-root>" --next-id decision --format json`.
The result considers filename and metadata numbers, reports mismatches and
reserves nothing; recheck before creation.
For example, store `ADR-0074` in
`docs/decisions/0074-subject.md`. Use a lowercase slash-separated domain label
for `scope`, such as `product/import-pricing`. A new proposal follows this template:

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

Fenced code examples are literal content, including lines starting with `#`.
Only headings outside backtick or tilde fences define the title and sections.

Keep each section's distinct information without invented alternatives or
repeated rationale. Keep reasons and tradeoffs only where they explain the
choice, constrain implementation or determine when to revisit it; omit the
discussion history. New Decisions use the owning Plan's language or request
language. Preserve an existing record's language unless explicitly changed.

## Links and transitions

Record links to Decisions in each affected Work Item's Decisions field,
following the entrypoint's linking policy and edit.md's edit permissions.
A proposal blocks only dependent work; its concrete effect
may be recorded in Instructions. Changing proposal status does not remove links.
Create a new Decision as proposed unless explicit human direction already
authorizes its immediate acceptance. That direction needs no repeated question.

Apply only explicitly authorized transitions:

| From | To |
| --- | --- |
| proposed | accepted or rejected |
| accepted | deprecated or superseded |
| deprecated | superseded |

Acceptance adds `accepted: YYYY-MM-DD` between created and scope. Deprecation
retains it. Proposed and rejected Decisions omit the accepted date. Rejected
and superseded Decisions are terminal.
Use actual dates no earlier than creation. Generic content edits affect only
proposals and preserve identity and lifecycle. Delete a proposal only after
checking that no Work Item or Decision links to it.

Supersession preserves both records. An authorized change to accepted or
deprecated content uses this route, never an in-place rewrite:

1. Create the accepted replacement with `supersedes: ADR-0001` after scope.
2. Set old status superseded and reciprocal `superseded_by: ADR-0002` after any supersedes.
3. Replace links in affected todo items. For started items, append the accepted
   replacement, retain the older link as history and explain the change.
4. Validate the coherent transition through edit.md.

Terminal historical links alone do not block replacement. Rejection in favor
of another proposal is not supersession.

## Existing batch metadata

Write new accept or reject transitions individually and validate after each
completed operation. Never create transition_batch or transition_batch_members.
Preserve those fields when already present, including later lifecycle changes.
Existing batch IDs are `batch-YYYYMMDD-N` (positive N) or 64 hexadecimal digits.
Both fields occur together; members are existing unique ADR IDs, each lists
itself, and every member has the same batch ID and complete ordered membership.
Do not recompute historical hashes. The Viewer ignores these fields; validator
and selector retain historical integrity checks.
Without suitable Python 3.11+, use the validator manual route named under
[Runtime helpers](../SKILL.md#runtime-helpers) for complete inspection.
