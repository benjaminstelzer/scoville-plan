---
format_version: 1
id: PLAN-0001
status: active
created: 2026-08-08
updated: 2026-08-08
current_item: W-001
---

# Validate a native profile

## Goal

Observe one valid profile.

## Non-goals

- Do not mutate project state.

## Work items

### W-001 Validate local records

Status: in_progress
Depends on: []
Blocked by: []
Decisions: [ADR-0001]
Outcome: The local record shapes are valid.
Acceptance: The validator reports a valid profile.
Steps:
1. Read the canonical files.
2. Check the local record shapes.
Evidence: []
Next action: Run the structural validator.

### W-002 Validate relationships

Status: todo
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001]
Outcome: Cross-record relationships are valid.
Acceptance: The graph validator reports no error.
Evidence: []
Next action: Wait for W-001 acceptance evidence.
