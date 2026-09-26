# Changelog

## v1.9.1 - 2026-09-26

- Name an unresolved blocking decision before the concrete next action it prevents.
- Complete a final Work Item, Plan and active index together with retained evidence and full profile validation.

## v1.9.0 - 2026-09-25

- Select consecutive Step groups with the complete Work Item as context and an explicit assigned range.
- Write plans directly without model-specific writing profiles or hash-based edit guards.
- Ship Plan Viewer v1.3.3 with plain-text Evidence and CRLF support. Keep writing legacy Evidence lists and LF for installed older Viewers.
- Use a Work Item template and one editing reference for ordinary Plan maintenance. Validate each completed write and preserve manual checks when Python is unavailable in General.
- Apply Decision transitions individually and append new work in arrival order unless the user chooses another priority. Preserve historical batches, priorities and return instructions.
- Read and write UTF-8 explicitly, including PowerShell-to-Python text transfers.
- Document explicit model and reasoning annotations without assigning them automatically.

## v1.8.0 - 2026-09-24

- Add independently configurable low, medium and high writing depth per plan point, with medium for unknown models.
- Preserve exact selected source text for Workflow dispatch and load unrelated proposal bodies only during a full audit.
- Keep manual selection outside the normal Python route. The new profile helper requires Python 3.11+.

## v1.7.7 - 2026-09-23

- Document the no-Python dispatch-unit selection procedure for exact Step
  ranges, dependency statuses, and complete referenced Decisions.
- Name the optional Decision-batch helper and its byte-exact SHA-256 alternative
  in compatibility requirements.

## v1.7.6 - 2026-09-22

- Use `scoville-workflow-for-codex` for optional Workflow dispatch integration.
  Workflow is available as a Codex-only Beta inside Scoville Suite.
- Keep the unchanged Plan Viewer v1.3.2 downloads available with this release.

## v1.7.5 - 2026-09-21

- Make Workflow-ready Steps expose discovery, interacting owners, cross-language
  or component contracts, helpers, harnesses, generators, and interpreted checks
  instead of describing only the small final edit.
- Treat unknown low-eligibility facts as at least a `medium` Step boundary while
  leaving final route ownership with the Workflow coordinator.

## v1.7.4 - 2026-09-21

- Give the Workflow coordinator sole ownership of route classification at
  dispatch. Plan still separates materially different consequence and reasoning
  boundaries with the Workflow's current class criteria, including unresolved
  helper contracts and local diagnostic discovery, but no longer assigns route
  classes while planning.
- Preserve existing and explicitly user-supplied route prefixes as planned
  minimums, while keeping route, executor model, and reasoning level separate.

## v1.7.3 - 2026-09-20

- Bind validator evidence to the exact complete profile bytes it inspected and
  invalidate that evidence after relevant changes.
- Let a complete successful validator run own its reported structural checks,
  while retaining manual review for authorization, meaning, Acceptance,
  Evidence, preserved history, and uncovered invariants.
- Narrow neighboring-Skill guidance to the owners relevant to Plan records.

## v1.7.2 - 2026-09-20

- Give Plan sole ownership of native record wording and define language
  selection for existing and new Plans, Work Items, and Decisions.
- Clarify validation fallback, existing authorization, Goal normalization, and
  the family rule for independently activated Skills.

## v1.7.1 - 2026-09-20

- Show Plan point and Decision pagination above and below each long list. Both
  controls share the same page state, while only the lower status announces a
  page change to assistive technology.

## v1.7.0 - 2026-09-20

- Add deterministic dispatch-unit selection for one exact Step, adjacent Step
  range, or complete Work Item without Steps. Unit output retains all referenced
  Decisions, excludes Evidence and unselected Steps, and omits the Work
  Item-wide `Next action` from Step units so a later Step cannot leak into the
  assigned task. Existing whole-Work-Item selector output and format-version-1
  Plan files remain unchanged.

## v1.6.0 - 2026-09-19

- Keep Goal as normalized current direction: target, boundary, and genuinely
  plan-wide constraints. Operational history, point-specific execution,
  evidence, and next actions remain with their canonical owners, and required
  facts move only when affected workers can still reach them.
- Record an explicitly selected executor model or reasoning level through one
  strict `[execute: ...]` annotation on a Step. Route risk remains separate,
  malformed or duplicated annotations fail validation, and started history is
  immutable except for an explicit change to one unperformed Step's execution
  annotation.

## v1.5.0 - 2026-09-19

- Add an optional deterministic read-only selector that emits only the active
  Plan direction, one current or named Work Item, direct dependency statuses,
  and Decisions referenced by that item. Oversized or malformed selections fail
  with a structured diagnostic instead of dumping or truncating source files.
- Reject duplicate or unknown selector headings, redirected canonical-path
  ancestors, empty required lifecycle values, and empty Steps. Validator
  diagnostics now emit UTF-8 JSON independently of the host stdout encoding.
- Keep one Step as the default Workflow dispatch unit, while allowing an
  explicitly invoked Workflow with an accepted Decision to bundle adjacent
  Steps only across one unchanged outcome, owner, authorization, route,
  workspace, and Acceptance boundary.

## v1.4.4 - 2026-09-19

- Show each Work Item's ordered Steps in the companion viewer, so the Plan's
  subordinate actions remain visible without opening the source Markdown.

## v1.4.3 - 2026-09-19

- Limit the pre-flight for the next `todo` Work Item to that item, the current
  repository, evidence from completed dependencies, and only directly relevant
  completed Work Items in the same active Plan. Do not scan completed or
  historical Plans or reread the entire active Plan without a concrete
  relevance reason.

## v1.4.2 - 2026-09-19

- Check each next `todo` Work Item against the current repository and completed
  predecessor evidence before it starts. Refine stale premises, signatures,
  data models, contracts, paths, or validation assumptions before execution.
- Keep the private workflow helper optional rather than treating it as an
  installation dependency.

## v1.4.1 - 2026-09-15

- Apply requests to add, remove, reorder, rewrite, or clean up Plan points
  directly. Only substantive future work becomes a Work Item; maintaining the
  Plan never creates another Plan point.

## v1.4.0 - 2026-09-15

- Classify messages received during active work before changing execution or
  Plan state. Stops, redirects, and execution-changing corrections act now;
  pure questions without a retained action create no Plan work.
- Queue additive requests without replacing current work. Batch compatible
  small changes, separate complex outcomes, preserve stable order and explicit
  successor priority, and keep blockers, Decisions, and dependencies intact.
- Preserve an explicitly requested return after immediate redirection in the
  paused Work Item's live Next action without rewriting started history.
- Write Plans and Work Items with the concept in Goal or Outcome, equal-rank
  facts as bullets, exact `1.`, `2.`, `3.` execution Steps, and every known file
  named in the Step that changes or checks it. Unknown owners use bounded
  discovery instead of invented paths.
- Keep Decision sections distinct, use bullets for comparable facts, and number
  Confirmation actions when their order matters. Records must remain clear to
  lower-reasoning workers and independently reviewable without chat context.

## v1.3.9 - 2026-09-14

- Fix the release archive so the installable package has one `scoville-plan`
  root instead of a duplicated directory level.

## v1.3.8 - 2026-09-14

- Shape optional Steps as later Scoville Workflow dispatch units, separating
  materially different routing needs while keeping related code, UI, copy, and
  browser work together. Workflow availability alone does not activate it.
- Store an optional routing class instead of a model or reasoning level. A Work
  Item without Steps remains one dispatch unit.

## v1.3.5 - 2026-09-12

- Reuse available unchanged instructions, reload missing or changed references, and keep live record checks separate. Apply historical stops to their recorded subject and scope.

## v1.3.4 - 2026-09-11

- Report every proposed Decision without requiring a decision response to a status request. Ask for acceptance, rejection or revision when work depends on the proposal or the user requests decision handling.

## v1.3.1 - 2026-09-08

- Added compact writing rules and wording checks for native Plans, Work Items,
  and Decisions.
- Preserve facts, uncertainty, verification criteria, and immutable history
  when shortening records.

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
