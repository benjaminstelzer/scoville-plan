---
format_version: 1
id: PLAN-0001
status: draft
created: 2026-09-08
updated: 2026-09-08
---

# Migrate the CLI cache to schema 2

## Goal

The goal of this Plan is to preserve all existing cached reports through migration to schema 2. All existing cached reports must be preserved when the cache is migrated to schema 2.

## Non-goals

- Network access.
- Deletion of the original cache.

## Work items

### W-001 Preserve cached reports during migration

Status: todo
Depends on: []
Blocked by: []
Decisions: [ADR-0001]
Outcome: The outcome of this Work Item is that existing reports remain available in schema 2, with report IDs and timestamps preserved. This means that existing reports remain available after migration and their report IDs and timestamps remain preserved.
Acceptance: Run python -m unittest tests.test_cache_migration and verify successful migration preserves reports, IDs, and timestamps. Simulate an interrupted write and confirm original reports remain available. Reject a malformed source without publishing migrated data. Run read-only commands and confirm no migration occurs. Compare the original cache before and after successful migration and every failure case; it must remain byte-identical and available for rollback.
Steps:
1. Inspect the current cache reader in src/cache/reader.py and inspect the current cache reader before changing it.
2. After implementation is authorized, implement the selected migration mechanism in src/cache/migrate.py and then update src/cache/reader.py to use the selected migration mechanism.
3. Update tests/test_cache_migration.py with migration tests and interruption tests and malformed-input tests and read-only tests.
Evidence: []
Next action: The next action to take is to inspect src/cache/reader.py; inspecting src/cache/reader.py is the first action to perform.
