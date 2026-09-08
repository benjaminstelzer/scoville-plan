# Case 01 raw report

## Request

Shorten the `todo` Outcome in the supplied native Plan without losing constraints.

## Routing decision

Available/discoverable package: `scoville-plan` only. Its YAML frontmatter says it owns repository-native Plan and Work Item records, including concise writing, and works without Scribe. The request is a rewrite of a `todo` Work Item Outcome in an existing `format_version: 1` native Plan. Selected owner: Scoville Plan. Route loaded: P (native Plan format), W (native Work Item operations), E (native editing). Scribe was stipulated absent and was neither loaded nor simulated.

## Actual read ledger

1. Read `Z:/Projekts/AI/scoville-plan/scoville-plan/SKILL.md` with `Get-Content -TotalCount 200` for discovery. This was an execution mistake: it read the complete YAML frontmatter and also the entire Core because the file is shorter than 200 lines. Thus the instruction to read only complete YAML frontmatter before the routing decision was not met exactly. No other Skill was read.
2. Copied source directory `C:/Users/benja/AppData/Local/Temp/scoville-record-writing-906c32ca89244ff7bec8a2d315f82862/record-test/verbose-before` to `C:/Users/benja/AppData/Local/Temp/scoville-record-writing-906c32ca89244ff7bec8a2d315f82862/terra-routing/case01/native-plan`; source was never edited.
3. Read the complete Core in `SKILL.md` (again), then the complete selected references `references/native-plan-format.md` (P), `references/native-work-items.md` (W), and `references/native-editing.md` (E).
4. Listed copied native files, captured SHA-256 hashes, and read complete `PROJECT_INDEX.md`, `docs/plans/0001-migrate-cli-cache.md`, and `docs/decisions/0001-stage-cache-migration.md`.
5. Read complete `references/profile-validation.md` (V) after detecting bundled `scripts/validate_profile.py` and an available Python interpreter.
6. After the edit, reread complete copied `PROJECT_INDEX.md`, the changed Plan, and the referenced proposed Decision; captured resulting hashes; inspected the scoped diff; and ran the validator.

## Source state and decision inventory

- Root: copied `native-plan`, with `PROJECT_INDEX.md`, `docs/plans/`, and `docs/decisions/`.
- Index: `format_version: 1`, `active_plan: null`.
- Plan: `PLAN-0001`, `draft`, `W-001` is `todo`.
- Proposed Decision discovered and read: `ADR-0001`, “Stage cache migration before publication”. It recommends temporary sibling-file staging then rename after validation; it is not accepted and does not block this wording-only edit.
- Affected pre-write Plan SHA-256: `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C`; immediate pre-write comparison matched it.

## Output

Changed only `docs/plans/0001-migrate-cli-cache.md`, W-001 `Outcome`:

```text
Outcome: All existing cached reports remain available in schema 2 with their report IDs and timestamps preserved.
```

This retains the result and constraints: all existing cached reports, schema 2 availability, and preservation of report IDs and timestamps. It does not alter Acceptance, Steps, Evidence, Next action, lifecycle, dependencies, Decision reference, Goals, or Non-goals.

## Validation ledger

- Changed Plan SHA-256 after write: `687511AA6916BF719CFFC5695BECCE614BC732A237612D24852D360BCED6B5F7`.
- Index SHA-256 unchanged: `F913A8061B4F846220B6001813A06059A6111341718FF505A20A3972FA6C824B`.
- Decision SHA-256 unchanged: `A467C988D0260CB9BCC1F4D92E9F8B9C7AB51BFE6762B180C8FE03D2B1EE95FF`.
- Scoped `git diff --no-index` showed exactly one changed line, the Outcome line. Git emitted CRLF-normalization warnings; no line-ending conversion occurred in the observed scoped diff.
- Manual inspection: frontmatter/key order, draft lifecycle, `todo` status, empty blockers/evidence, non-empty Next action, Decision reference, and active-plan relation remain valid. The Outcome is direct and contains no repeated rationale.
- `python Z:/Projekts/AI/scoville-plan/scoville-plan/scripts/validate_profile.py --root <copied-root> --format json`: exit `0`, `valid: true`, errors `0`, warnings `0`, files checked `3`, plans `1`, work items `1`, decisions `1`.

This is native structural validation only; it does not establish implementation acceptance or authorize the still-proposed Decision.
