---
format_version: 1
id: ADR-0001
status: proposed
created: 2026-09-08
scope: cli/cache
---

# Stage cache migration before publication

## Decision

Recommend writing migrated data to a temporary sibling file and renaming it after validation. Implementation remains unauthorized.

## Problem

Existing cached reports must survive the migration to schema 2.

## Drivers

- Preserve report IDs and timestamps.
- Prevent read-only commands from triggering migration.
- Keep the original cache available for rollback.

## Considered alternatives

- Migrate in place: uses less temporary storage but an interrupted write can damage cached data.

## Consequences

- Requires temporary storage.
- Lets validation precede publication.

## Confirmation

1. Run `python -m unittest tests.test_cache_migration`; confirm migration preserves report IDs and timestamps, interruption preserves original reports, malformed input publishes nothing, and read-only commands do not migrate.
2. Compare original cache bytes after success and every failure; require byte identity and rollback availability.

## Revisit when

- The target filesystem does not support atomic rename.
