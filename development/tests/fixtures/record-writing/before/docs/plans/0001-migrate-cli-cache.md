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
Acceptance: Verify successful migration preserves reports, IDs, and timestamps. Simulate an interrupted write and confirm original reports remain available. Reject a malformed source without publishing migrated data. Run read-only commands and confirm no migration occurs. Compare the original cache before and after successful migration and every failure case; it must remain byte-identical and available for rollback.
Steps:
1. Inspect the current cache reader.
2. After implementation is authorized, implement the selected migration mechanism.
Evidence: []
Next action: The next action to take is to inspect the current cache reader; inspecting the current cache reader is the first action to perform.
