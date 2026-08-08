# Native editing safety

Direct edits are the only Scoville Plan write path. They have no publication
gate, expected-hash writer, typed request validation, rollback, or multi-file
atomicity. Compensate with narrow reads, exact-byte checks, complete
proposed-state inspection, and honest reporting.

## Contents

- Read before writing
- Guard the write
- Preserve the profile
- Handle invalid or changing state
- Verify and report

## Read before writing

1. Resolve the nearest project root containing `PROJECT_INDEX.md`,
   `docs/plans/`, and `docs/decisions/`. When profile existence is unknown,
   list the workspace root before reading a canonical path.
2. Read the index and require `format_version: 1`. Resolve the active Plan and
   current Work Item when present, its referenced Decisions, and every
   `proposed` Decision. Load other records only for the selected operation's
   relation checks.
3. Inventory all valid records only when allocating an ID, validating the
   complete profile, or checking a cross-record relation.
4. Capture the exact bytes and SHA-256 of every affected existing file. Re-read
   those exact bytes immediately before applying a context-bound patch.

Within one conversation, retain the resolved path and SHA-256 of each loaded
Skill reference. Compare hashes before a later operation and reload only a
changed reference. Reread live project state; do not reload the full Plan or
unrelated accepted Decisions merely because another turn began.

## Guard the write

- Prepare every member of a multi-file change and inspect the complete proposed
  profile before applying any member. Publish the canonical routing file last
  when that reduces, but cannot eliminate, partial-state risk.
- Create new files exclusively after rechecking ID and path collisions. Never
  overwrite another record or reuse an interior ID gap.
- Use context-bound patches for existing files. If affected bytes changed,
  stop and reconcile instead of replaying a stale edit.
- For physical deletion, validate the complete proposed project with the exact
  file or Work Item absent before removing it.
- Never describe direct multi-file edits as atomic. If only a proper subset is
  written, report the exact partial state and stop.

## Preserve the profile

- Preserve UTF-8 without BOM, LF endings, exact frontmatter and section order,
  Work Item key order, stable IDs, authored H3 order, optional Steps, retained
  batch metadata, and every lifecycle invariant in the routed format guides.
- Keep canonical paths relative to the project root. Reject traversal,
  cross-project targets, redirected canonical files, and symlink escapes.
- Use the operation date for each permitted change. It may equal but never
  precede the affected record's stored date. A no-op changes no bytes or date.
- Verify every dependency, Decision, supersession, blocker, `current_item`, and
  active-Plan reference against the complete proposed profile.
- Never invent authored text, evidence, authority, status, acceptance, or a
  lifecycle result to make the profile valid.

## Handle invalid or changing state

Stop on an unsupported version, foreign or partial profile, ambiguous root,
path-security failure, ID exhaustion, changed bytes, or a write whose result is
unknown. Do not create a parallel profile or edit around the failure.

Repair invalid state autonomously only when an observed diagnostic identifies
one specific format defect and the repair changes no authored choice, scope,
acceptance, lifecycle result, or evidence. Never autonomously complete or
revert an interrupted multi-file transition. Interrupted activation,
completion, supersession, or Decision-batch state requires explicit user
authority.

## Verify and report

After writing, reread every changed canonical file, inspect the complete scoped
diff, and recheck the affected graph and lifecycle invariants. Run an
independently available repository validator when authorized, but never make it
a dependency of this Skill.

Report exact changed records, manual checks, validator output when actually
observed, unresolved proposals, partial-state risk, and the next concrete
action. Say `native structural inspection passed`; do not imply executable,
transactional, or typed validation that did not occur.
