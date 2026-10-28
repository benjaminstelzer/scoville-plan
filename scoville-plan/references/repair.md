# Inspect, repair and maintain Plans

Load only for an explicit Plan-progress inspection, repair, migration or maintenance request, such as
“Check and correct the Plan”. Ordinary editing and recovery do not load this
route. Inspection alone is read-only; “correct”, “repair” or an equivalent
request authorizes bounded record corrections, not changes to work products.
For cleanup of record text without reassessing progress, use Maintenance below
instead of the progress inspection steps.

For a repair or cleanup of Step text, apply [authoring.md](authoring.md)'s
bounded-action, observable-completion and required-check rules. Derive every
condition only from the original authorized action and binding requirements,
never current code, tests or assumptions. Do not copy whole-item Acceptance.
Preserve scope, safeguards, negative criteria, order and completed effects.
Keep uncertain meaning and ask before an affected edit. Leave a Step unchanged
while its execution or review is running.

1. Read the requested Plan's complete Work Items, referenced Decisions and
   relevant proposals. Use the active Plan when none is named. Inspect existing
   Evidence and its relevant original reports first. Compare both Work Item
   status and every Step, including unmarked Steps in historical Plans.
2. When evidence is insufficient or conflicts, inspect the actual task results
   against the Step's action and Work Item Acceptance: code and tests, authored
   text, documents, configurations or other deliverables. Run only necessary
   focused checks within existing permissions. Existence alone proves no
   completion. Preserve the result; product fixes are remaining work, not Plan
   repair. Historical acceptance is judged against its original requirements
   and evidence, not today's unrelated product state.
3. Classify each Step from observed facts. Use todo for unstarted work and
   in_progress for work that began but still has an unfinished action or checks.
   Use done only after the action and required checks are complete. Use cancelled
   only after explicit cancellation. An interruption or
   failed check is not cancellation. If facts are insufficient, retain unknown
   or the recorded status and report the specific uncertainty; never guess.
4. For an authorized repair, load progress.md and correct only established progress,
   Evidence, Instructions and the Step completion wording required above. Put
   additional binding conditions in Instructions,
   results in Evidence and ordinary progression in Step status. Read legacy
   Next action too. Add missing Step status when established,
   including in retained terminal history without rewriting actions or original
   acceptance. Preserve completed effects, order, scope, execution choices,
   stops and due reviews. Record unresolved evidence limits once. A Work Item
   is done only after every Acceptance criterion and required review is observed;
   completed Steps or partial successful checks alone do not close it.
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

## Migrate old records

Only an authorized correction or migration writes. Reconcile existing Next action,
Evidence and relevant original instructions before setting Instructions. Leave
unknown facts unrecorded; do not use [] to claim that no conditions exist.
Transfer additional binding conditions, not the next ordinary Step. Link
proposed Decisions to affected Work Items under SKILL.md's linking policy.
If a legacy item has no Steps, add a coherent Step only when its original task
and observed state are established. Preserve the whole original scope and effects,
not just remaining work. Unknown history stays unchanged and is reported.

Remove Next action only after all still-binding contents are preserved in
Instructions or Steps, with relevant results in Evidence. Conflicting legacy
and new instructions require clarification;
neither source wins automatically. Historical Step annotations may be filled from
proof without reopening terminal work. Historical terminal instructions remain
history. Report contradictions, but do not use historical terminal instructions
as a new direction to return to and execute that work.

## Maintenance: clean up existing Plans

Only an explicit cleanup request authorizes these edits, including in old,
completed or cancelled Plans. Read the affected complete blocks and only the
sources needed to distinguish live conditions from redundant text. Apply progress.md's
field rules to those records:
| Field | Keep | Remove |
| --- | --- | --- |
| Instructions | Additional live conditions under progress.md; retain an unclear condition. | Repeated actions/criteria, progress, results and obsolete conditions. Terminal fields normally become []; report apparent unmet conditions without erasing them or reopening work. |
| Evidence | Observed results, required review occurrence and open defects/limits needed for development. | Review text, chronology, duplicate summaries and counts, versions or inventories without continuing purpose. |
| Goal | Current target, boundary and each binding constraint's effect plus Decision ID under the lifecycle route. | Superseded constraints or constraints whose binding effect has demonstrably ended under the Decision lifecycle rules; duplicated rationale and history; never replace an effect by an unreadable ID alone. |
| Non-goals | Every still-binding exclusion. | Reasons and drafting notes. |
| Decisions in the requested scope | Every condition in its owning section, including required checks and revisit triggers. Preserve identity, the choice, authority, evidence status and decision-relevant reasons; apply the Decision lifecycle rules. | Equivalent repetition, filler, discussion history, and reasons or alternatives that neither explain the choice, constrain implementation nor determine revisit. Material changes still require the Decision supersession route. |

- Explicit cleanup also authorizes editorial shortening of Outcome, Acceptance
  and Step text, plus Goal, Non-goals and accepted or deprecated Decisions within
  the requested scope, including started and terminal history. Apart from the
  Decision relocation below, shortening only removes filler and redundant
  wording and merges equivalent conditions. Leave other text unchanged. Read the
  relevant lifecycle contract for Goal or Non-goals edits. Authoring style
  does not justify rewriting existing text. Before
  saving, compare each edited text with its original. It must keep the requested
  act, such as investigation or implementation, every required result, case,
  value, limit, quantifier, negation, exception and action, and the full
  verification scope. The same results must pass or fail before and after the
  edit. Wording that states an obligation is not filler, even when it is general
  or repeated in other records. Do not replace a general check or condition with
  selected cases or checks. Keep required methods and checks even when new
  writing would place them in Steps. Do not replace historical conditions with a mutable reference. If
  equivalence is uncertain or a requirement would change, keep the original
  text and resolve only the material choice before the affected edit. Equivalent
  shortening needs no separate approval, old-text copy, note or report.
- Explicit maintenance of existing Plans includes their linked Decisions within
  the requested scope, including started and terminal Plans. Before assessing
  or editing them, read [native-decision-format.md](native-decision-format.md)
  for its maintenance table, lifecycle and nonbinding-history writing rules.
  Shortening reduces a full Decision; only a valid binding mark lets Workflow
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

  A requirement, limit, exception, authority limit or necessary reason for the
  choice, implementation, verification or revisit is binding wherever it stands.
  Binding sections are Decision, Consequences, Confirmation and Revisit when.
  Preserve identity, the stated choice, authority, evidence status, historical
  files and IDs. Redirect duplicate links to the owner without widening scope.
  Cancellation or expiry grants no passed check, waived independent condition
  or new permission. Keep an unmarked Decision fully readable.

  Remove links only when they demonstrably govern nothing, including in started
  or terminal items; shared subject matter or history alone proves no relevance.
  Retain uncertain links. Keep a still-needed historical exception or missing
  review occurrence briefly in Evidence. Add no unrelated links; report a
  missing relevant link instead. Do not migrate other records or expand scope.
- Apply the same future-use criterion to reports within the requested cleanup
  scope. Keep a report reference only when its detail remains useful or required.
  Reviews are temporary development input, not retained reports; remove their
  archived text within the requested cleanup scope. A passed review needs only
  a short occurrence record, not its file list, checks or worker recap. Open
  findings remain current work until resolved.
  Do not create an archive, before-copy, hash chain, new report or Work Item for
  cleanup. No complete project history needs to be reconstructed or retained.
- Preserve IDs, Plan and Work Item statuses, execution annotations, Step order,
  the meaning of Outcome, Step actions and Acceptance, dependencies, material
  Decisions under their lifecycle rules, completed effects and live user
  permissions, limits and stops. Cleanup changes neither acceptance nor authorization. Do not delete
  files or alter Decisions outside the requested scope.

This is ordinary record maintenance, not a new worker or review phase. Do not
repeat product tests, old reviews or a progress audit merely to shorten records.
An independently required review or retention rule still applies. Validate once
after the coherent profile edit under progress.md. Report the cleaned scope and any
unresolved live condition briefly; no separate cleanup report is needed.
