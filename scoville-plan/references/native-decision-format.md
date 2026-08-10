# Native Decision format

Load this reference only when creating, changing, transitioning, or auditing a
Decision in a Scoville Plan native profile with `format_version: 1`.

## Contents

- Files, IDs, and allocation
- Decision profile
- Links and lifecycle

## Files, IDs, and allocation

Store one UTF-8-without-BOM, LF-ended Decision in `docs/decisions/`. IDs match
`ADR-[0-9]{4}`. Filenames use the numeric ID followed by a lowercase ASCII
kebab-case subject, for example `0042-use-repository-native-files.md`.

Allocate the highest valid Decision number plus one. Recheck the internal ID
and filename immediately before creation, never overwrite a collision, and do
not reuse an interior gap. A deleted highest proposal releases that provisional
ID. `ADR-9999` exhausts the space.

## Decision profile

Use the required frontmatter keys in this order; add optional lifecycle keys
only when their conditions apply:

```yaml
---
format_version: 1
id: ADR-0001
status: proposed
created: 2026-08-08
accepted: 2026-08-08
scope: project/storage
supersedes: ADR-0000
superseded_by: ADR-0002
transition_batch: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
transition_batch_members: [ADR-0001, ADR-0002]
---
```

`format_version`, `id`, `status`, `created`, and `scope` are required. Scope is
a non-empty slash-separated domain label whose segments match
`[a-z0-9][a-z0-9-]*`; it is not a path. Status is `proposed`, `accepted`,
`rejected`, `deprecated`, or `superseded`.

Omit `accepted`, supersession keys, and transition-batch keys on a new
proposal. Require `accepted` for `accepted`, `deprecated`, and `superseded`,
and omit it for `proposed` and `rejected`. Dates use ISO `YYYY-MM-DD`; an
acceptance date must not precede creation.

After one H1 title, write these non-empty H2 sections in order:

```text
Decision
Problem
Drivers
Considered alternatives
Consequences
Confirmation
Revisit when
```

For a proposal, `Decision` states the recommended result before its rationale.
For a choice already made explicitly by a human, it states that selected
result. Separate observed or supplied constraints from the Skill's own
recommendation. Name actual alternatives and their material tradeoffs; do not
manufacture facts, approval, confirmation evidence, or certainty.
`Confirmation` states how the choice can be verified, not that verification
already happened.

## Links and lifecycle

Work Item `Decisions` lists are the sole canonical Plan-to-Decision links.
Decision frontmatter never stores incoming Plan links. Add a new proposal to
every affected `todo` item and no unrelated item. Preserve the immutable list
on items that have left `todo` and report that format-version-1 limitation.
Proposal status never removes a link: a proposed or otherwise unresolved
Decision links every mutable Work Item whose implementation, sequencing,
Acceptance, or Evidence could change under a viable alternative. Do not link a
Work Item when no such effect is established.

Creating a Decision always produces `proposed`. When the current user has
already selected the direction or an applicable project instruction clearly
records the human-selected direction, apply the accepted transition without
asking for the same choice again. Edit or physically delete only a proposal;
deletion requires no incoming Work Item reference. Never infer a lifecycle
transition from implementation, ordinary documentation, source code,
repository state, or silence. Apply these transitions only after the required
explicit human choice:

- `proposed` to `accepted` or `rejected`;
- `accepted` to `deprecated` or `superseded`; and
- `deprecated` to `superseded`.

`rejected` and `superseded` are terminal. Acceptance records the authorized
date; deprecation retains it. Supersession creates an accepted replacement,
sets `supersedes` on the replacement and `superseded_by` on the old record, and
preserves both files. Rejecting one proposal in favor of a separately authored
choice creates no supersession link.

A generic Decision update applies only to `proposed` and preserves ID, status,
creation date, acceptance date, and supersession fields. Physically delete only
an unreferenced proposal after checking every Work Item `Decisions` list and
every Decision `supersedes` and `superseded_by` field. Once a Decision leaves
`proposed`, preserve its ID, filename, authored rationale, and lifecycle
metadata.

Implement an explicitly authorized edit of an accepted or deprecated Decision
as one supersession result, not an in-place rewrite. Every affected mutable Work
Item must replace the old Decision ID explicitly. Block only an affected
started or otherwise immutable Work Item whose still-relevant implementation,
sequencing, Acceptance, or Evidence would have to adopt the replacement
Decision. A terminal historical Work Item is not a blocked item merely because
its unchanged Decision link remains as history. If a required replacement would
edit an immutable Work Item, stop and report the format limitation rather than
publishing an inconsistent replacement.

For an explicitly authorized accept-or-reject batch, additionally load
[native-decision-batches.md](native-decision-batches.md). Do not load that
reference for creation, a single transition, or an audit unrelated to batch
integrity.
