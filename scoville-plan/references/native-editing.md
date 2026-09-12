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
2. Read the index and resolved Plan frontmatter and require `format_version: 1`
   in each. Read the current and affected complete Work Item blocks, the title,
   Goal and Non-goals needed to interpret the work, referenced Decisions, and
   every `proposed` Decision found through a frontmatter inventory. Load other
   records only for the selected operation's relation or evidence checks.
3. Inventory all valid records only when allocating an ID, validating the
   complete profile, or checking a cross-record relation.
4. Capture the exact bytes and SHA-256 of every affected existing file. Re-read
   and compare those exact bytes immediately before a context-bound patch.
   Keep complete byte snapshots in the execution environment; return the hash
   or comparison result, not unchanged file bodies, to model context. A hash
   detects change; it proves neither valid content nor permission to write.

### Scope output without narrowing checks

For identity, order, or graph checks, extract ordered H3 headings and `Status`,
`Depends on`, and `Decisions` lines. For current work, changed authored text,
acceptance, or evidence, read the complete relevant blocks. ID allocation must
still inspect all IDs in its namespace. Proposal discovery still covers every
Decision. A selected slice never proves that unrelated records are valid.

Machine reads may cover whole files or the complete proposed profile while
returning only selected blocks, hashes, scoped diffs, and validator diagnostics.
Preserve the full captured bytes for unchanged-content comparisons. Verify
proposed and written structure completely when required; do not replace this
with a grep result, a zero-length diff, or an old validator result.

Without the optional validator, use shell searches, range reads, and byte/hash
comparisons plus manual inspection of the required invariants. Expand to full
records wherever those checks cannot establish structure or relation validity.
Use full reads for full-content audits and relevant malformed-state diagnosis.
If extraction boundaries or output completeness are uncertain, widen the read;
never interpret truncated output as absence. This changes output scope, not
format, history retention, concurrency checks, or the manual proof boundary.

Reuse relevant Skill instructions while their contents remain available and
their source identity is current. Reload missing contents even when a retained
hash is unchanged. Observed edits, version changes or stale-source signals
require reloading the affected reference before dependent work; if freshness is
uncertain, inspect that source. Do not hash or reload every reference merely
because another operation began. Reread the required live project records and
preserve their exact-byte write guards above; unchanged instructions do not
establish unchanged project state.

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

After writing, reread changed frontmatter and the complete affected Work Item
or Decision blocks, inspect the complete scoped diff, and compare full resulting
bytes with the prepared result so unexpected edits outside those blocks are
not hidden. Recheck the affected graph and lifecycle invariants. When the bundled
read-only validator and Python are available, run it as described in
[profile-validation.md](profile-validation.md). Otherwise preserve the manual
inspection fallback; never make an executable a dependency of this Skill.
Also review changed prose using the core compact-record rules. Structural
validity alone does not establish precision, sufficiency, or lack of repetition.

Report exact changed records, manual checks, validator output when actually
observed, unresolved proposals, partial-state risk, and the next concrete
action. Say `native structural inspection passed`; do not imply executable,
transactional, or typed validation that did not occur.
