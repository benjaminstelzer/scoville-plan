# Changelog

## v1.3.4 - 2026-09-11

- Report every proposed Decision without requiring a decision response to a status request. Ask for acceptance, rejection or revision when work depends on the proposal or the user requests decision handling.
- Behavioral acceptance remains deferred. This release adds no live-model or cross-host qualification.

## v1.3.1 - 2026-09-08

- Added compact writing rules and wording checks for native Plans, Work Items,
  and Decisions.
- Preserve facts, uncertainty, verification criteria, and immutable history
  when shortening records.
- Keep native record wording with Plan when Scribe is installed unless the user
  explicitly requests Scribe.

## v1.3.0 - 2026-09-07

- Added the responsive Scoville Plan Viewer for Windows, macOS, and Linux.
- Show active, completed, paused, blocked, and upcoming Plan points together
  with current and historical Decisions.
- Store the project registry in a portable XML file and fall back to the
  platform application-data directory when an installed app cannot write beside
  its executable.
- Refresh visible projects every four seconds and paginate after 100 Plan
  points or Decisions with keyboard focus restored after page changes.

## v1.2.14 - 2026-09-05

- Limit routine recovery and progress reads to the relevant complete blocks
  while preserving full-file change detection and complete validation.
- Keep completed records in their version-1 Plans. No archive format or
  automatic project conversion was introduced.

## v1.2.13 - 2026-09-05

- Fixed Decision batch inspection on Windows volumes where path and descriptor
  metadata report different creation times.

## v1.2.7 - 2026-08-11

- Made every Scoville Skill optional and independently usable. Discovering a
  sibling does not install or activate it.

## 2026-08-08: Read-only native profile validator

- Added an optional read-only validator for complete native
  `format_version: 1` profiles with deterministic JSON or text diagnostics.
- Detect redirected paths, concurrent changes, graph defects, invalid Decision
  lifecycles, and incomplete reads without modifying project records.
- Keep manual inspection available when Python or the helper is unavailable.

## 2026-08-08: Native Decisions and complete lifecycle

- Added native Decision records and complete lifecycle guidance without adding
  a CLI dependency.
- Added read-only recovery, profile initialization, Plan and Work Item changes,
  blockers, evidence, proposals, Decision lifecycle, and narrow repair through
  direct Markdown and YAML edits.
- Accept clear user choices and applicable project rules without asking for the
  same decision again.
- Store material inferred choices as proposals and require explicit acceptance,
  rejection, or revision before they become authoritative.

## 2026-08-08: Initial release

- Added repository-native Plans and Work Items for durable planning, recovery,
  progress tracking, audits, and handoffs.
- Added conditional guidance for planning granularity and safe direct-file
  lifecycle changes under native `format_version: 1`.
