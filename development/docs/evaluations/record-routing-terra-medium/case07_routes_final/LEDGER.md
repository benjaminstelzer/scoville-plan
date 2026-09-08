# Case 07 execution ledger

## Scope

- Source copied before inspection: `record-test/verbose-before`
- Working root only: `terra-routing/case07_routes_final`
- Changed canonical file: `docs/plans/0001-migrate-cli-cache.md`
- Added scratch-only records: `REPORT.md`, `LEDGER.md`

## Actual reads in order

1. `scoville-plan/SKILL.md` frontmatter only, prescribed discovery regex. Output selected Plan as the native Plan and Work Item owner.
2. `scoville-scribe-anti-ai-slop/SKILL.md` frontmatter only, prescribed discovery regex. Output selected Scribe because the user explicitly requested it.
3. Full `scoville-plan/SKILL.md` Core. Output required Plan routing for native Work Item wording.
4. Full `scoville-scribe-anti-ai-slop/SKILL.md` Core. Output limited Scribe to Core-only for this fixed short native field and required Plan plus its route.
5. `scoville-plan/references/native-plan-format.md` (`P`). Output defined Outcome as one physical line and required observable-result content.
6. `scoville-plan/references/native-work-items.md` (`W`). Output permitted refinement of this `todo` Work Item in a draft Plan.
7. `scoville-plan/references/native-editing.md` (`E`). Output required root resolution, affected-state reads, pre-write bytes/hash, context-bound patch, and post-write checks.
8. Scratch-root directory listing. Output found `PROJECT_INDEX.md`, one Plan, and one Decision.
9. Scratch `PROJECT_INDEX.md`. Output `format_version: 1`, `active_plan: null`.
10. Scratch `docs/plans/0001-migrate-cli-cache.md`. Output Plan `PLAN-0001`, `draft`, Work Item `W-001` `todo`, its complete block, Goal, and Non-goals.
11. Scratch `docs/decisions/0001-stage-cache-migration.md`. Output linked `ADR-0001` is `proposed`.
12. Pre-write reread of the affected Plan Outcome and SHA-256. Output matched the captured Outcome and hash `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C`.
13. `scoville-plan/references/profile-validation.md` (`V`) and validator-path listing. Output instructed a read-only JSON validation.
14. Post-write complete affected Work Item block and byte/hash checks. Output matched the prepared result exactly.
15. Bundled validator complete-profile read. Output exit 0 and `valid: true`.

## Write

- Context-bound one-line patch replaced only the W-001 `Outcome` value.
- Old: `The outcome of this Work Item is that existing reports remain available in schema 2, with report IDs and timestamps preserved. This means that existing reports remain available after migration and their report IDs and timestamps remain preserved.`
- New: `Existing reports remain available after migration to schema 2, with report IDs and timestamps preserved.`

## Hashes

| File | Before SHA-256 | After SHA-256 | Result |
| --- | --- | --- | --- |
| `PROJECT_INDEX.md` | `F913A8061B4F846220B6001813A06059A6111341718FF505A20A3972FA6C824B` | `F913A8061B4F846220B6001813A06059A6111341718FF505A20A3972FA6C824B` | unchanged |
| `docs/plans/0001-migrate-cli-cache.md` | `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C` | `5E67D67655AA2BA3CEF3406187A366B5D14914595B16499A86D8E5EFB810B970` | Outcome only |
| `docs/decisions/0001-stage-cache-migration.md` | `A467C988D0260CB9BCC1F4D92E9F8B9C7AB51BFE6762B180C8FE03D2B1EE95FF` | `A467C988D0260CB9BCC1F4D92E9F8B9C7AB51BFE6762B180C8FE03D2B1EE95FF` | unchanged |

## Checks and boundary

- Exact prepared-result comparison: pass.
- New Outcome occurrences: 1. Old Outcome occurrences: 0.
- Plan encoding check: no UTF-8 BOM, LF-only line endings.
- Validator: exit 0, `valid: true`, 0 errors, 0 warnings, 3 files checked.
- Structural validation does not prove acceptance, implementation, or authorization.
- Unresolved ambiguity: `ADR-0001` remains `proposed`; no lifecycle decision was made or inferred.
