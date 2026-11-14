# Inspect, repair and maintain Plans

Load only for an explicit progress inspection, repair, migration or maintenance
request. Inspection is read-only; a correction request authorizes bounded
corrections to the Plan records, not product changes. Ordinary editing and
recovery do not load this route. For text cleanup without reassessing
progress, use Maintenance below.

When repairing or cleaning up Step text, apply [authoring.md](authoring.md):
each Step names a bounded action and, where the action leaves it unclear, its
completion condition and required checks. Take every condition only from
the originally authorized action and its binding requirements, never current code, tests or
assumptions. Do not copy whole-item Acceptance. Keep scope, safeguards,
prohibitions, order and completed effects. Keep text of uncertain meaning and
ask before editing it. Leave a Step unchanged while its execution or review
is running.

1. Read the requested Plan's complete Work Items, referenced Decisions and
   relevant proposals; use the active Plan if none is named. Start from Evidence
   and relevant original reports. Inspect item status and every Step, including
   unmarked historical Steps.
2. When evidence is insufficient or conflicts, inspect the actual task results
   against the Step's action and Work Item Acceptance: code and tests, authored
   text, documents, configurations or other deliverables. Run only necessary
   focused checks within existing permissions. Existence alone proves no
   completion. Leave the result unchanged; product fixes are remaining work,
   not Plan repair. Judge historical acceptance against its original
   requirements and evidence, not today's unrelated product state.
3. Classify Steps from observed facts: todo for unstarted work, in_progress for
   begun but unfinished actions or checks, done only after both are complete,
   cancelled only after explicit cancellation. Interruption or failure is no
   cancellation. Insufficient facts leave unknown or recorded status unchanged;
   report the specific uncertainty.
4. For authorized repair, apply progress.md's field and continuation rules.
   Correct established progress, Evidence, Instructions and the Step completion
   wording permitted above; reconcile legacy Next action. Add proved missing
   Step status even in terminal history without rewriting actions or original
   acceptance. Preserve effects, order, scope, execution choices, stops and due
   reviews. Complete items only after every Acceptance criterion and required
   review is observed.
5. Follow progress.md and the lifecycle route for Work Item, Plan and index transitions;
   prepare related changes together and validate the entire resulting profile.
   Reopening terminal work, removing blockers without proof, cancellation or
   changed scope still needs its applicable explicit decision. If an incorrect
   terminal closure requires reopening, report it and request that lifecycle
   direction; do not silently rewrite historical acceptance. On concurrent
   changes stop the affected write and retain the findings.

Report corrected items and Steps, actual checks, unresolved facts and the concrete
continuation. A code or text inspection is evidence only for what it established,
not proof of unrun tests, missing reviews or external effects.

## Contents

- Migrate old records
- Maintenance: clean up existing Plans

## Migrate old records

Only an authorized correction or migration writes. Compare existing Next action,
Evidence and relevant original instructions before setting Instructions. Leave
unknown facts unrecorded; do not use [] to claim that no conditions exist.
Transfer the additional binding conditions (stops, limits, explicit returns, required overall reviews) into Instructions, not the next ordinary action. Link proposed Decisions to affected Work Items under SKILL.md's
linking policy. If a legacy item has no Steps, add a coherent Step only when
its original task and observed state are established. Preserve the whole
original scope and effects, not just remaining work. Keep and report unknown
history.

Remove Next action only after everything in it that still binds stands in
Instructions or Steps, with relevant results in Evidence. When legacy and new
instructions conflict, ask; neither wins automatically. Instructions of
terminal items remain history: report
contradictions, but do not treat them as a new direction to return to and
execute that work.

## Maintenance: clean up existing Plans

Only explicit cleanup authorizes these edits, including in old, completed or
cancelled Plans. Read complete affected blocks and the sources needed to separate
live conditions from redundancy. Apply progress.md's field rules:

| Field | Keep | Remove |
| --- | --- | --- |
| Instructions | Additional live conditions under progress.md; retain an unclear condition. | Repeated actions/criteria, progress, results and obsolete conditions. Terminal fields normally become []; report apparent unmet conditions without erasing them or reopening work. |
| Evidence | Observed results, required review occurrence and open defects/limits needed for development. | Review text, chronology, duplicate summaries and counts, versions or inventories without continuing purpose. |
| Goal | Current target, boundary and each binding constraint's effect plus Decision ID under the lifecycle route. | Superseded constraints or constraints whose binding effect has demonstrably ended under the Decision lifecycle rules; duplicated rationale and history; never replace an effect by an unreadable ID alone. |
| Non-goals | Every still-binding exclusion. | Reasons and drafting notes. |
| Decisions in the requested scope | Every condition in its owning section, including required checks and revisit triggers. Preserve identity, the choice, authority, evidence status and decision-relevant reasons; apply the Decision lifecycle rules. | Equivalent repetition, filler, discussion history, and reasons or alternatives that neither explain the choice, constrain implementation nor determine revisit. Material changes still require the Decision supersession route. |

- Cleanup may shorten Outcome, Acceptance, Steps, Goal, Non-goals and accepted
  or deprecated Decisions in scope, including started and terminal history.
  Remove only filler and redundancy or merge equivalent conditions, apart
  from Decision relocation below; style alone permits no rewrite. Compare
  with the original: preserve the requested act, every required result, case,
  value, limit, quantifier, negation, exception, action, method and full
  verification scope. The same results must pass or fail before and after;
  `every endpoint` must not become `endpoints`. An obligation is not filler
  even when general or repeated elsewhere; selected cases cannot replace a
  general check. Keep required
  methods/checks in their historical field and replace no historical
  condition with a reference to text that can change. Keep uncertain text and
  resolve a material change before editing. Equivalent shortening needs no
  extra approval, old-text copy, note or report.
- Explicit maintenance of existing Plans includes their linked Decisions within
  the requested scope, including started and terminal Plans. Before assessing
  or editing them, read [native-decision-format.md](native-decision-format.md)
  for its maintenance table, lifecycle and nonbinding-history writing rules.
  Shortening reduces a full Decision; only a valid binding mark lets a context consumer
  omit nonbinding background. Apply this flow to every linked Decision in scope,
  including already marked ones:

  ```mermaid
  flowchart TD
    read["Read complete Decision"] --> classify["Classify statements by meaning"]
    classify --> lifecycle["Apply Decision maintenance table and lifecycle"]
    lifecycle --> links["Assess Work Item links under the linking policy"]
    links --> move["Move binding content to its binding section without changing meaning"]
    move --> reread["Reread Problem, Drivers and Considered alternatives"]
    reread --> background{"Would omitting any remaining statement affect choice, implementation, verification or revisit?"}
    background -->|yes| move
    background -->|no| mark["Add or retain Binding sections: complete as Decision's first non-blank line"]
    background -->|uncertain| unmark["Remove existing mark; report Decision ID and unresolved statement"]
  ```

  Binding content is every requirement, limit, exception, permission and
  necessary reason, in whichever section it stands; native-decision-format.md
  names the four binding sections. Keep historical files and IDs except for
  scoped deletion under that reference. When redirecting a duplicate's links,
  link no item it did not govern and do not widen the owner's scope. Cancellation or expiry proves no passed
  check, waived independent condition or new permission. Keep unmarked
  Decisions fully readable.

  Remove a link only when it demonstrably governs nothing, including in started
  or terminal items; retain uncertain links. Shared topic or history alone
  proves no relevance. Keep needed historical exceptions or missing reviews in
  Evidence. Report missing relevant links; add no unrelated ones or migrations.
- Apply progress.md's Evidence retention rule to reports in scope. Remove
  archived review text; retain required review occurrence and unresolved
  findings. Create no archive, before-copy, hash chain, report or Work Item for
  cleanup, and reconstruct no complete project history.
- Preserve IDs, Plan and Work Item statuses, execution annotations, Step order,
  the meaning of Outcome, Step actions and Acceptance, dependencies, material
  Decisions under their lifecycle rules, completed effects and live user
  permissions, limits and stops. Cleanup changes neither what is accepted nor what is permitted. File deletion follows native-decision-format.md's deletion
  safeguard; change nothing outside the requested scope.

A comprehensive cleanup of Plans and Decisions requires an explicit maintenance
request covering those records. New-Plan maintenance stays within the lifecycle
route's targeted ADR set.

This is ordinary record maintenance, not a new worker or review phase. Do not
repeat product tests, old reviews or a progress audit merely to shorten records.
An independently required review or retention rule still applies. Validate once
after the coherent profile edit under progress.md. Report the cleaned scope and any
unresolved live condition briefly; no separate cleanup report is needed.
