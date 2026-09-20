# Changelog

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
- State the complete eight-Skill ownership boundary in suite order and keep the
  private workflow helper optional rather than treating it as an installation
  dependency.

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
