---
format_version: 1
id: PLAN-0001
status: draft
created: 2026-09-08
updated: 2026-09-08
---

# Migrate the CLI cache to schema 2

## Goal

Preserve all existing cached reports through migration to schema 2.

## Non-goals

- Network access.
- Deletion of the original cache.

## Work items

### W-001 Preserve cached reports during migration

Status: todo
Depends on: []
Blocked by: []
Decisions: [ADR-0001]
Outcome: Existing reports remain available in schema 2, with report IDs and timestamps preserved.
Acceptance: Run `python -m unittest tests.test_cache_migration`; migration preserves reports, IDs, and timestamps; interruption preserves original reports; malformed input publishes nothing; read-only commands do not migrate; original bytes remain identical after success and failures for rollback.
Steps:
1. Inspect migration triggers and compatibility assumptions in `src/cache/reader.py`.
2. Update `src/cache/migrate.py` to stage schema-2 output before publication.
3. Update `src/cache/reader.py` to invoke migration only from authorized write paths.
4. Add migration and failure coverage in `tests/test_cache_migration.py`.
Evidence: []
Next action: Inspect migration triggers and compatibility assumptions in `src/cache/reader.py`.
