# Case 06 ledger

## Actual read order

1. Extracted frontmatter only from the available Plan and Scribe `SKILL.md` files with the prescribed PowerShell expression.
2. Selected Plan: the requested text is the native `Goal` field of a Plan, whose concise writing is owned by Plan. Scribe was not selected.
3. Read the complete Plan `SKILL.md` Core.
4. Copied the immutable `record-test/verbose-before` directory to this case scratch directory.
5. Read the selected Plan references `native-plan-format.md`, `native-project-lifecycle.md`, and `native-editing.md` for the native Plan wording rewrite route.
6. Read the copied `PROJECT_INDEX.md`, complete affected Plan, and Decision frontmatter/complete proposed Decision; captured initial SHA-256 values.
7. Re-read the complete affected Plan and its SHA-256 immediately before the context-bound patch.
8. Read `profile-validation.md`, then ran its read-only validator after the write.

## Prior-turn fact

The supplied fact that Scribe had been active for an unrelated release note was treated as scoped to that other segment. Its content and Core were not read, and it did not change selection for this native Plan field.

## Decision and output

Changed only the copied Plan Goal to: `Preserve all existing cached reports when migrating to schema 2.` The wording preserves the target, existing-report scope, and schema-2 migration while removing repetition. No lifecycle, work-item, Decision, index, or non-goal content changed.

## Validation

- Pre-write Plan SHA-256: `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C`.
- Post-write Plan SHA-256: `28AADEF17EB134ACC3D7DEFFDD3F31A0BD794D98F006A7AE28EAF959A45A0F4B`.
- Scoped diff contains only the Goal-line replacement.
- UTF-8 BOM absent; CR-byte count is zero.
- Read-only native-profile validator: exit `0`, `valid: true`, zero errors and warnings across 3 files, 1 Plan, 1 Work Item, and 1 Decision.
