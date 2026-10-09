# Changelog

## v1.12.9 - 2026-10-09

- Use a complete reader command when continuing document reads, and an existing directory with a file filter when searching. Prefer direct shell commands for simple file inventories.

## v1.12.8 - 2026-10-09

- Recheck new IDs immediately before creation and reserve complete Work Item Acceptance for Work Item completion. Preserve full input and failure status when reading or transferring Plan context.

## v1.12.7 - 2026-10-08

- Make Plan selection, editing and paused continuation conditions explicit, so blockers are resolved before a dependent action.

## v1.12.6 - 2026-10-08

- Follow ordered preparation, writing and verification steps when editing Plan records.

## v1.12.5 - 2026-10-08

- Diagnose shortened output from the observed failing layer; a later shortened query does not prove that the original capture lost information.

## v1.12.4 - 2026-10-08

- Require Python 3.11+ consistently and distinguish the reader program from its document input.
- Preserve every binding Acceptance condition when remaining work changes owner. Keep field reviews read-only.
- Make manual selection and profile inspection use exact records, the current profile and strict UTF-8 decoding before display.

## v1.12.3 - 2026-10-08

- Read Markdown as documentation and use complete UTF-8 helper invocations. Capture selector diagnostics as well as successful context before display.
- Keep complete input available through bounded reads and preserve the manual route when Python is unavailable.

## v1.12.2 - 2026-10-07

- Define Acceptance through distinct necessary results and binding checks. Keep methods, test catalogs and history out of the field unless a method or check is itself required for acceptance.
- Allow explicitly requested Maintenance to shorten Outcome, Acceptance and Step wording, including started and completed items, without changing requirements or keeping another copy of the old text.

## v1.12.1 - 2026-10-07

- Keep Instructions limited to current conditions beyond the Steps. Retain concise results and required review occurrence in Evidence.
- Clean old and completed Plans through Maintenance without reconstructing history, archiving reviews or repeating completed checks.
- Show the real position fields when resuming work and provide directly usable selection commands. Check large inputs before reading them.

## v1.12.0 - 2026-10-07

- Query the next unused Work Item, Plan or Decision ID and a named item's structural start conditions without writing records or granting execution authority.
- Warn about likely text-decoding damage without treating intentional examples as invalid UTF-8 or repairing them automatically.
- Keep Plan updates focused on decisions and progress, preserve completed drafting notes as evidence, and reuse decisive checks for unchanged work.
- Preserve complete oversized context through compaction or a hashed temporary file, with clear diagnostics for invalid paths and arguments.
- Keep long Project and Plan history menus scrollable and their first and last entries selectable in Plan Viewer 1.4.3.

## v1.11.4 - 2026-10-03

- Report the required context size in budget errors and provide an invocation that returns the complete result.

## v1.11.3 - 2026-10-02

- Find all open Decision proposals, including unlinked choices and projects without an active Plan.
- Preserve fenced examples when selecting Plan context instead of reading their headings as part of the record.
- Explain invalid blocker, route and execution values with concrete correction guidance. Keep material human choices distinct from routine editing decisions.

## v1.11.2 - 2026-10-01

- Show Plan progress beneath the title in Plan Viewer 1.4.2. Collapse the Plan and current point independently, and keep long Step details out of the current-point header.
- Keep project, Plan and current-point labels compact with consistent type and spacing. The current point's description aligns with its heading.
- Distinguish a display-only scope mismatch from a real instruction conflict without changing the authorized work.

## v1.11.1 - 2026-10-01

- Record the active Work Item and actually started Steps before delegated execution. Read-only review preserves completed Step progress.
- Add Paused and Cancelled filters in Plan Viewer 1.4.1, covering every Plan point status.

## v1.11.0 - 2026-10-01

- Give each new Plan point at least one Step with explicit progress. Preserve older and mixed records, with unknown progress kept unknown.
- Replace Next action in new records with Steps and optional Instructions. Return active Step groups, paused context and linked open Decisions through the context helper.
- Repair proven Plan and Step progress from Evidence, original reports and actual results, without inventing completion or changing a read-only review.
- Ship Plan Viewer 1.4.0 with Step icons, written active groups, safe Next step selection, Instructions and linked open Decisions.

## v1.10.0 - 2026-09-29

- Continue explicitly requested Plan execution through eligible work while preserving recorded stops, priority conflicts and unresolved Decisions.
- Load the named manual procedures only when Python is unavailable in the general edition. Codex uses the packaged helpers without manual fallbacks.

## v1.9.4 - 2026-09-28

- Split unfinished work in a started Step into ordered Steps while preserving scope, acceptance criteria and completed evidence.
- Keep unresolved Decisions in a started item's next action until accepted, without changing its Decision links prematurely.

## v1.9.3 - 2026-09-27

- Report exact Evidence limits and invalid characters with concrete correction steps. Explain valid Decision scope spelling.
- Keep Plans and Decisions focused on execution-relevant facts, constraints and reasons.

## v1.9.2 - 2026-09-27

- Add accepted Decisions and make verified formal corrections to started Work Items without replacing them.
- Keep related test repairs in the existing scope and link concise evidence to retained reports.

## v1.9.1 - 2026-09-26

- Name an unresolved blocking decision before the concrete next action it prevents.
- Complete a final Work Item, Plan and active index together with retained evidence and full profile validation.

## v1.9.0 - 2026-09-25

- Select consecutive Step groups with the relevant Work Item and preserve explicit model choices.
- Simplify direct Plan editing while retaining validation, historical decisions and the general edition's manual route.
- Add plain-text Evidence and CRLF support in Plan Viewer 1.3.3. Older Viewers still need bracketed lists and LF.

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

- Make Workflow-ready Steps describe the work and checks needed to execute them. Unknown complexity requires at least medium routing, with the final choice left to Workflow.

## v1.7.4 - 2026-09-21

- Let Workflow choose execution routing while Plan preserves supplied minimums and separates work with materially different risks. Keep model and reasoning choices distinct.

## v1.7.3 - 2026-09-20

- Bind validation to the complete records checked. Changed records need fresh structural validation, while authority, meaning and evidence still require judgment.

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

- Select an exact Step, adjacent range or whole Work Item for dispatch, keeping its Decisions while excluding unrelated Steps and later actions. Existing Plan files remain compatible.

## v1.6.0 - 2026-09-19

- Keep the Plan goal focused on current direction, with evidence and next actions beside their work.
- Record explicitly selected models or reasoning in Step annotations without confusing them with routing risk or rewriting started history.

## v1.5.0 - 2026-09-19

- Add a read-only context selector for the active Plan and relevant work. Malformed or oversized records receive a diagnostic instead of truncated context.
- Reject invalid structure and redirected paths, and report validator errors correctly on Windows.
- Allow explicitly approved adjacent Step groups with one scope and acceptance boundary.

## v1.4.4 - 2026-09-19

- Show each Work Item's ordered Steps in the companion viewer, so the Plan's
  subordinate actions remain visible without opening the source Markdown.

## v1.4.3 - 2026-09-19

- Check only the next item, current sources and relevant completed dependencies before starting work. Avoid rereading unrelated Plan history.

## v1.4.2 - 2026-09-19

- Verify the next item against current sources and completed work before execution, correcting stale assumptions. Keep Workflow integration optional.

## v1.4.1 - 2026-09-15

- Apply requests to add, remove, reorder, rewrite, or clean up Plan points
  directly. Only substantive future work becomes a Work Item. Maintaining the
  Plan never creates another Plan point.

## v1.4.0 - 2026-09-15

- Apply stops and corrections immediately, while queueing additional work without replacing the active task.
- Preserve requested return points, stable work order and dependencies. Write execution details where the responsible worker can find them.

## v1.3.9 - 2026-09-14

- Fix the release archive so the installable package has one `scoville-plan`
  root instead of a duplicated directory level.

## v1.3.8 - 2026-09-14

- Shape optional Steps for later Workflow assignments without activating Workflow. Separate materially different work and preserve related implementation and checks together.

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
