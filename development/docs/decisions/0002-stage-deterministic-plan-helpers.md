---
format_version: 1
id: ADR-0002
status: accepted
created: 2026-09-19
accepted: 2026-09-19
scope: project/planning
---

# Adopt deterministic read-only Plan selection

## Decision
Add a deterministic read-only Python selector and retain direct Markdown and YAML edits as the only Plan write path. Do not evaluate or implement a writing helper in the current Plan.

## Problem
The current natural-language extraction contract is correct but agents still reconstruct shell ranges independently, which allowed complete megabyte-scale Plan output.

## Drivers

- Scoville Plan already defines the exact semantic slice required for recovery and current work.
- Two observed coordinators emitted nearly one MiB of unrelated Plan text despite that instruction.
- Current public compatibility promises direct Markdown and YAML edits and no planning CLI.
- Read-only selection changes no authority, while a writing helper would materially change the public mutation contract and expand the current work.

## Considered alternatives

- Keep instruction-only extraction and direct edits: Preserves the current contract but retains the observed output and reconstruction failures.
- Add only a read-only selector: Removes the dominant Plan-read cost without changing the write contract.
- Add selector and unrestricted writer together: Reduces more agent work but risks hidden authority, stale writes, and misleading atomicity.
- Stage selector first and evaluate a guarded typed mutator: Could reduce lifecycle patch construction later but adds evaluation and architecture scope now.

## Consequences

- The selector may read complete files internally but emits only the requested semantic projection or a structured error.
- Direct Markdown and YAML edits remain the only authoritative write path.
- The current Plan contains no mutator prototype, evaluation, implementation, integration, or publication work.
- A future writing-helper proposal requires a separate Decision and Plan scope.

## Confirmation

1. Use a fixture whose active Plan exceeds one MiB and prove the selector emits only frontmatter, Goal and Non-goals, the selected Work Item, direct-dependency statuses, and referenced Decisions.
2. Verify that Plan writes still use guarded direct edits and that no writing-helper entry point is added.
3. Require all existing profile validation, cold-start recovery, and public compatibility tests to pass before publishing the selector.

## Revisit when
Reconsider a writing helper only through a separate proposal when measured direct-edit cost justifies expanding the architecture and validation surface.
