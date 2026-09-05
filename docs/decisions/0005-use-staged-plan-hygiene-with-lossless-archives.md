---
format_version: 1
id: ADR-0005
status: accepted
created: 2026-09-05
accepted: 2026-09-05
scope: planning/history
---

# Introduce staged Plan hygiene with lossless archives

## Decision

Implement selective Plan reading and run an early deterministic
comparison before deciding whether to build archives. Include genuine Plan
completion followed by a successor where the goal boundary permits it. This
proposal selects no archive format: lossless archives remain a conditional
candidate requiring a separate proposed Decision and explicit user choice after
the comparison. Keep format-version-1 projects supported without automatic
changes. On 2026-09-05 the user instructed implementation of the reviewed Plan.
This accepts the initial reading and measurement direction; the archive format
still requires the separate choice described above.

## Problem

The read-only route already selects frontmatter and the current Work Item, and
native editing discourages full-Plan refreshes. Post-write guidance nevertheless
requires rereading every changed canonical file. A large active Plan can thus
repeatedly expose completed history. Native format version 1 requires contiguous
Work Item blocks, same-Plan dependencies, and preservation of started items'
document positions; it defines no archival representation or operation.

## Drivers

- Reduce completed history entering routine model context while preserving
  correct resumption, dependency readiness, Decisions, and acceptance evidence.
- Preserve one canonical owner per Work Item and its stable Plan-qualified ID.
- Preserve original authored content and logical order, including terminal work.
- Keep direct Markdown/YAML editing and optional read-only validation; add no
  mandatory writer, database, service, generated index, or hidden state.
- Measure loaded text separately from provider-reported usage and monetary cost.

## Considered alternatives

- Read hygiene only: lowest format risk and a useful independent improvement,
  but the active file still grows and broad inspections still expose history.
- Close Plans at genuine outcome boundaries: already appropriate when the goal
  is complete, but cannot remove historical detail from a still-active goal.
- Lossless archival within one logical Plan: a candidate for large ongoing
  Plans, at the cost of explicit ordering, resolution, and conversion rules;
  assess its additional value before adopting this direction.
- One file per Work Item from creation: avoids a growing monolithic body, but
  changes ordinary small-project authoring more broadly than optional archival.
- Summarize or delete completed entries, or rely on Git alone: smaller working
  text but inadequate as the canonical record of Acceptance and Evidence.

## Consequences

The initial implementation stage is selective reading. The next stage measures
whether enough avoidable historical context remains to justify archive contract
work. A hand-authored archive-shaped fixture can estimate visible-text potential
without changing consumers, but proves neither real agent retrieval nor working
archive support. A successor-Plan comparison is valid only at a completed goal;
prose links never substitute for unresolved same-Plan dependencies. If selective
reading is sufficient, recommend explicitly removing the still-todo conditional
archive items and finishing the bounded Plan after the measurement. Never
silently cancel them or leave an active Plan without eligible current work.

The following constraints apply only if archival is separately selected:

The active Plan would retain live work and compact archive routing; archived
blocks would remain canonical historical records belonging to that Plan. Routing
must not become a second independently mutable source of status or evidence.
The representation must preserve original logical order and account for archived
IDs during allocation, dependency validation, Decision relation checks, and
Plan completion. Archival changes location, not lifecycle: cancelled work never
satisfies a dependency and terminal items never reopen.

Recommend batching terminal blocks at meaningful checkpoints after checking that
historical text materially dominates the active document. Choose any numeric
threshold only from representative measurements; do not archive every completed
item by default. Active requirements remain discoverable through current work
and its Decision references. Archive contents load only for a relevant relation,
evidence question, or explicit historical inspection.

Exact archive paths, routing shape, partial-batch ordering, version number,
conversion/recovery sequence, and trigger remain conditional contract work.
A new format version is the expected boundary because version 1 preserves
physical document position and recognizes no archive routing. Define the full
version/discovery contract and record the archive Decision before implementation;
check supported versions in both the index and the resolved Plan. Automatic
project conversion, publication, installation, and additional paid evaluation are outside the
current request. Existing accepted Decisions retain their historical scope.

## Confirmation

Review this proposal and Plan with Fable before implementation. First compare
baseline and selective reading with a clearly labeled archive projection and a
successor-Plan arm only where valid. Record residual overhead, applicability,
and the recommendation before asking for the separate archive direction.
If archives are selected, verify scoped reads preserve relation and concurrency
checks, archive resolution has one canonical owner and stable IDs, and interrupted direct edits are diagnosed
without pretending they are atomic. Exercise valid legacy and archive-aware
profiles plus missing, duplicate, misordered, redirected, and corrupt archive
cases. Compare unchanged baseline, read-hygiene-only, and archive-aware operation
on the same representative tasks. Retain failures and report no observed benefit
when the data do not establish one.

Fable's first review and the author's corrections are recorded in
[the review note](../reviews/0005-plan-hygiene-fable-review.md). It is analysis,
not Decision acceptance or implementation evidence.

## Revisit when

Read hygiene alone removes the observed overhead, archive resolution costs more
than it saves, users need incompatible history editing, or conversion cannot
preserve canonical records and recovery without disproportionate complexity.
