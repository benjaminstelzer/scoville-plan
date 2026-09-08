---
format_version: 1
id: ADR-0001
status: proposed
created: 2026-09-08
scope: cli/cache
---

# Stage cache migration before publication

## Decision

The recommendation is to write migrated data to a temporary sibling file and rename it after validation. In other words, migrated data should first be written to a temporary sibling file, and the file should then be renamed after validation.

## Problem

Existing cached reports must survive the migration to schema 2.

## Drivers

Preserve report IDs and timestamps. Read-only commands must not trigger migration. Keep the original cache available for rollback.

## Considered alternatives

Migrate in place: needs less temporary storage but risks an interrupted write damaging cached data.

## Consequences

Staging requires temporary storage and lets validation precede publication. Implementation has not been authorized. There is currently no authorization to implement this recommendation.

## Confirmation

Verify preserved reports, IDs, and timestamps after migration. Simulate an interrupted write and check original reports remain available. Supply malformed source data and confirm no migrated data is published. Run read-only commands and confirm no migration occurs. Compare the original cache before and after migration and each failure case to establish byte identity and rollback availability.

## Revisit when

Revisit this Decision when atomic rename is unsupported. Lack of support for atomic rename is the trigger for revisiting this Decision.
