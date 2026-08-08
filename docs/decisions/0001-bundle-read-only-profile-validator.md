---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-08-08
accepted: 2026-08-08
scope: skill/profile-validation
---

# Bundle a strictly read-only native profile validator

## Decision

Scoville Plan will bundle one optional Python validator for native
`format_version: 1` profiles. It may read `PROJECT_INDEX.md`, `docs/plans/`, and
`docs/decisions/` and emit diagnostics, but it must never create, edit, delete,
rename, normalize, repair, or otherwise mutate project files. The Skill remains
fully usable when Python or the validator is unavailable.

## Problem

Direct Markdown and YAML edits preserve portability but make local and
cross-record format mistakes easy to miss. Manual inspection alone gives an
agent no deterministic list of violated invariants or precise location from
which to plan a safe correction.

## Drivers

- Preserve the repository-native file format and Skill-only workflow.
- Provide deterministic evidence without introducing a planning CLI.
- Keep validation independent from mutation and human authority.
- Return enough context for an agent to correct unambiguous defects and surface
  ambiguous lifecycle choices to the user.
- Avoid making Python an installation or activation requirement.

## Considered alternatives

- Keep manual inspection only: preserves zero executables but repeats fragile
  parsing work and produces inconsistent diagnostics.
- Add a mutating CLI with repair commands: could automate corrections but would
  create a second write path and violate the selected read-only boundary.
- Use an external validation service or package: reduces bundled code but adds
  availability, privacy, versioning, and dependency risk.
- Bundle an optional read-only Python validator: keeps deterministic checks next
  to the format contract without owning project mutations.

## Consequences

The repository must maintain parser, graph-validation, diagnostic-contract, and
non-mutation tests. Validator success proves only native structure and
relationships; it cannot prove human authorization, decision quality, evidence
truth, acceptance sufficiency, or that reported work occurred. Agents apply any
correction through Scoville Plan's existing native-editing rules.

## Confirmation

Automated tests must run the validator against valid and invalid fixtures,
assert its documented diagnostics and exit codes, and confirm identical file
paths and SHA-256 hashes before and after every invocation.

## Revisit when

Revisit if a later format version cannot be validated without a new runtime,
the optional Python path materially harms portability, or observed agent use
shows that deterministic diagnostics cannot distinguish safe structural fixes
from choices requiring human authority.
