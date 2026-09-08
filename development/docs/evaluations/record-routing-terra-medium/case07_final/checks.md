# Checks

- Exact pre-write SHA-256 for `docs/plans/0001-migrate-cli-cache.md`: `88581DA745C6B8EA9271110AA281C2BB083C43ED33976B900ABD48404C04364C`.
- Scoped diff shows one changed line, the `Outcome` field of `W-001`.
- Post-write SHA-256 for `docs/plans/0001-migrate-cli-cache.md`: `CFD4940777C826C67103B9D05C1D87DF710C944AFB6B131A82F15B1F0373A85E`.
- `PROJECT_INDEX.md` and `docs/decisions/0001-stage-cache-migration.md` retained their source SHA-256 values.
- Complete reread of `W-001` confirmed Work Item field order, `Status: todo`, `Depends on: []`, `Blocked by: []`, `Decisions: [ADR-0001]`, unchanged Acceptance, Steps, Evidence, and Next action.
- Native structural validator command: `C:/Python314/python.exe Z:/Projekts/AI/scoville-plan/scoville-plan/scripts/validate_profile.py --root case07_final --format json`.
- Validator result: exit `0`, `valid: true`, `errors: 0`, `warnings: 0`, 3 files checked, 1 Plan, 1 Work Item, 1 Decision.
- No behavioral migration or acceptance verification was performed. Structural validation does not establish acceptance evidence.
