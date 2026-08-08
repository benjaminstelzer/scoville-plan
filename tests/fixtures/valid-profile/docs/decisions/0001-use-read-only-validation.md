---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-08-08
accepted: 2026-08-08
scope: skill/profile-validation
---

# Use read-only validation

## Decision

Use a validator that never mutates project state.

## Problem

Manual inspection can miss structural errors.

## Drivers

- Deterministic structural evidence.
- Repository-native ownership.

## Considered alternatives

- Manual inspection only.
- A mutating repair command.

## Consequences

Validation remains independent from correction.

## Confirmation

Compare profile bytes before and after validation.

## Revisit when

Revisit when the native format version changes.
