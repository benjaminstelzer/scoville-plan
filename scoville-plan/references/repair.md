# Inspect and repair Plan progress

Load only for an explicit Plan-progress inspection, repair or migration request, such as
“Check and correct the Plan”. Ordinary editing and recovery do not load this
route. Inspection alone is read-only; “correct”, “repair” or an equivalent
request authorizes bounded record corrections, not changes to work products.

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
3. Classify each Step from observed facts: unstarted is todo; actual work with
   unfinished action/checks is in_progress; completed action and required checks
   is done; cancelled requires an explicit cancellation. An interruption or
   failed check is not cancellation. If facts are insufficient, retain unknown
   or the recorded status and report the specific uncertainty; never guess.
4. For an authorized repair, load edit.md and correct only established progress,
   Evidence and Instructions. Put additional binding conditions in Instructions,
   results in Evidence and ordinary progression in Step status. Read legacy
   Next action too. Add missing Step status when established,
   including in retained terminal history without rewriting actions or original
   acceptance. Preserve completed effects, order, scope, execution choices,
   stops and due reviews. Record unresolved evidence limits once. A Work Item
   is done only after every Acceptance criterion and required review is observed;
   completed Steps or partial successful checks alone do not close it.
5. Follow edit.md and the lifecycle route for Work Item/Plan/index transitions;
   prepare related changes together and validate the entire resulting profile.
   Reopening terminal work, removing blockers without proof, cancellation or
   changed scope still needs its applicable explicit decision. If an incorrect
   terminal closure requires reopening, report it and request that lifecycle
   direction; do not silently rewrite historical acceptance. On concurrent
   changes stop the affected write and retain the findings.

Report corrected items/Steps, actual checks, unresolved facts and the concrete
continuation. A code or text inspection is evidence only for what it established,
not proof of unrun tests, missing reviews or external effects.

## Migrate old records

Only an authorized correction/migration writes. Reconcile existing Next action,
Evidence and relevant original instructions before setting Instructions; missing
facts stay unrecorded, not []. Transfer additional binding conditions, not the
next ordinary Step. Link relevant proposed ADRs in Decisions; their ADR owns status.
If a legacy item has no Steps, add a coherent Step only when its original task
and observed state are established. Preserve the whole original scope and effects,
not just remaining work. Unknown history stays unchanged and is reported.

Remove Next action only after all binding contents are preserved in Instructions,
Steps or retained historical evidence. Keep accessible original reports when
cleaning up Evidence. Conflicting legacy/new instructions require clarification;
neither source wins automatically. Historical Step annotations may be filled from
proof without reopening terminal work. Historical terminal instructions remain
history; report contradictions without treating them as a new executable return.
