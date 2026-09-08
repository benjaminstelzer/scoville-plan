# Case 03 report

## Decision

- Selected `scoville-plan` only. The requested text is the `Outcome` field of a native todo Work Item, and Plan owns native-record wording and wording audits.
- Did not select `scoville-scribe-anti-ai-slop`: its frontmatter defers native planning-record rewriting to Plan unless Scribe is explicitly requested.
- Rewrote only `W-001`'s `Outcome`; its `todo` status permits authored-text refinement. No lifecycle, evidence, acceptance, Decision, or scope field changed.
- ADR-0001 remains `proposed`. Its staged-migration recommendation was read as required proposal inventory; this wording-only edit is not dependent on accepting it.

## Actual reads

1. Discovery frontmatter only: `Z:/Projekts/AI/scoville-plan/scoville-plan/SKILL.md`.
2. Discovery frontmatter only: `Z:/Projekts/AI/scoville-scribe-anti-ai-slop/scoville-scribe-anti-ai-slop/SKILL.md`.
3. Selected Plan Core: `Z:/Projekts/AI/scoville-plan/scoville-plan/SKILL.md`.
4. Selected routes: `references/native-plan-format.md`, `references/native-work-items.md`, and `references/native-editing.md`.
5. Copied fixture root inventory; then copied native `PROJECT_INDEX.md`, Plan identity/headings, current and affected Work Item, and proposed Decision `ADR-0001`.
6. Before write: exact affected Plan hash `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C` and original Outcome line.
7. Post-write validator route: `references/profile-validation.md`.

## Output

- Copied fixture: `verbose-before/docs/plans/0001-migrate-cli-cache.md`.
- Changed output: `Outcome: Existing reports remain available in schema 2 with IDs and timestamps preserved.`
- No source fixture was modified.

## Validation

- Re-read changed Plan frontmatter and complete W-001 block.
- Prepared expected full Plan bytes matched written bytes: `True`.
- Scoped diff contains exactly the one Outcome-line replacement.
- `python Z:/Projekts/AI/scoville-plan/scoville-plan/scripts/validate_profile.py --root <copied fixture root> --format json`: exit 0, `valid: true`, 0 errors, 0 warnings; 3 files, 1 Plan, 1 Work Item, and 1 Decision checked.
- Final Plan SHA-256: `A252D66C395064D22271ECD517B819C3A7908AADC3BD1E0BD7025416B0920643`.
