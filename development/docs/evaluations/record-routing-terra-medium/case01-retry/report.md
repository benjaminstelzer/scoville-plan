# Case 01 retry report

## Decision

Selected `scoville-plan`: the request rewrites a `todo` Work Item Outcome in an existing native Plan. No other Skill was available or used. The required route was P/W/E: native Plan format, Work Item operations, and native editing.

`ADR-0001` is `proposed`, recommends staging migration in a temporary sibling file before validation and rename, and says implementation is not authorized. It was not changed; shortening the Outcome does not adopt it.

## Exact reads

- Source directory entry listing, then copied source into this case directory.
- The sole available `SKILL.md` frontmatter, using the prescribed `ReadAllText` plus anchored frontmatter regex only.
- Full selected Plan core: `SKILL.md`.
- Routed references only: `references/native-plan-format.md`, `references/native-work-items.md`, `references/native-editing.md`, and post-write `references/profile-validation.md`.
- Native records: `PROJECT_INDEX.md`; complete `PLAN-0001` record; Decision frontmatter inventory; complete proposed `ADR-0001` record.
- Pre-write SHA-256 and exact affected Outcome context; post-write frontmatter, complete affected block, scoped diff, and full-profile validator output.

## Output

Changed only `verbose-before/docs/plans/0001-migrate-cli-cache.md` in this copied fixture.

```text
Outcome: Existing reports remain available in schema 2 with report IDs and timestamps preserved.
```

The post-write Plan SHA-256 is `CFD4940777C826C67103B9D05C1D87DF710C944AFB6B131A82F15B1F0373A85E`.

## Validation

- Pre-write SHA-256 guard matched `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C`.
- Prepared-result bytes matched the written file; it is UTF-8 without BOM and LF-only.
- Scoped diff contains exactly the Outcome replacement. Manual checks confirmed the inactive index, draft Plan, one `todo` Work Item, existing ADR reference, and required non-terminal `Evidence` and `Next action` fields.
- `validate_profile.py --format json`: exit 0, `valid: true`, 0 errors, 0 warnings (3 files, 1 Plan, 1 Work Item, 1 Decision).

No behavioral implementation or acceptance evidence was claimed.
