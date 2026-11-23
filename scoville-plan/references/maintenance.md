# Maintenance

## Inspect and repair progress

Inspection only reads. A correction request authorizes bounded corrections
to the Plan records, not product changes.

1. Read the requested Plan (default: the active one) with its complete Work
   Items, referenced Decisions and relevant proposals. Start from Evidence
   and original reports; inspect item status and every Step.
2. Where evidence is insufficient or conflicts, inspect the actual results
   against the Step's action and the item's Acceptance, running only
   necessary focused checks within existing permissions. Existence alone
   proves no completion. Judge historical acceptance against its original
   requirements, not today's unrelated product state. Product fixes are
   remaining work, not Plan repair.
3. Classify each Step from observed facts: todo if unstarted, in_progress if
   its action or checks are begun but unfinished, done only when both are
   complete, cancelled only after explicit cancellation. Interruption or
   failure is no cancellation. Leave a status unchanged when the facts are
   insufficient and report the uncertainty.
4. An authorized repair corrects established progress, Evidence and
   Instructions and clarifies a Step's established completion condition and
   required checks. It keeps actions, original acceptance, effects, order, scope,
   execution choices, stops and due reviews. If an incorrect closure needs
   reopening, report it and ask for that direction.

When you repair or shorten Step text, take every condition only from the
originally authorized action and its binding requirements, never from
current code, tests or assumptions, and do not copy whole-item Acceptance.
Ask before editing text of uncertain meaning. Leave a Step unchanged while
its execution or review is running.

Report corrected items and Steps, actual checks, unresolved facts and the
continuation.

## Amend a started item

Keep IDs, scope, dependencies, order and completed effects. Beyond the
fields progress.md lists, a started item permits only the following;
splitting or appending a Step needs no separate request when the authorized
work needs it:

- Correcting a stale path, version reference or other purely formal wording
  when evidence shows unchanged behavior, compatibility, data, permissions
  and verification scope. A changed expected result or weaker Acceptance is
  material: with the user's decision, change the Acceptance and state in
  Evidence what the user changed and when; record a Decision only when the
  change applies beyond this item.
- Splitting the remaining work of a started Step into consecutive Steps
  without changing Outcome, Acceptance, constraints or order; keep completed
  parts with their Evidence and update Step references in pending
  assignments.
- After a required review finds an omitted implementation with no matching
  Step, appending one Step that fulfils a named, already binding
  Acceptance criterion or requirement; it then goes through the
  implementation, checks and reviews of the active execution route.
- On an explicit user choice, replacing the execution annotation of a named
  unperformed Step.

## Cancel a Work Item or Plan

Cancel only on explicit direction. Cancellation establishes no Acceptance and
satisfies no dependency; resolve any open item that would depend on cancelled
work before saving. First fulfil the conditions that govern the cancellation
itself; keep outstanding execution and Acceptance conditions in Instructions
as history.

A cancelled Work Item has empty Blocked by and Evidence of its unresolved
prerequisites and effects, or, without observed work, of the user's direction
and its date. Cancelling a non-current item keeps `current_item`; cancelling
the current one selects the successor under progress.md, like completion. If
the request leaves the Plan's resulting state open, ask before saving.

A cancelled Plan has `status: cancelled` and no `current_item`; it is saved
with its current item's authorized transition and, if it was active, the
index's `active_plan: null`. Keep its other items as recorded unless the
request covers them. No successor Plan is selected.

## Activate or switch a Plan

Activation needs an explicit direction, a draft target Plan and a selected
todo or paused item whose dependencies are done; it starts nothing. Update the
target Plan and the index together. When switching, the outgoing Plan gets the
user's chosen draft, completed or cancelled status and loses its
`current_item` in the same update; its current item stays todo or paused, is
paused if in_progress, or is completed or cancelled, as the user chooses.
Preserve every other item. Completed and cancelled Plans are never
reactivated.

## Rewrite or delete records

Rewrite or delete a whole Plan only when it never executed. Activation is not
execution; any in_progress, paused or done item, or other evidence of
performed work, rules it out, and where cancelled items' Evidence leaves this
unclear, ask. In such a Plan the requested authored fields of todo or
cancelled items may be rewritten, keeping IDs, references, Evidence, order and
statuses. A Plan that executed is cancelled instead.

Before deleting a Plan, resolve references to it in other records without
rewriting history or deleting linked Decisions, and set the index idle if it
was active, unless the user selected an eligible replacement.

Delete a todo Work Item only when another item remains and no `Depends on`
names it; the current item needs a dependency-ready todo or paused
replacement in the same update. Delete a proposal only when nothing links to
it.

Delete a file only after verifying that its current contents are committed;
otherwise ask, and delete only with the user's explicit approval of that
deletion. A tracked path or an older committed version does not suffice.
Add no archive, replacement report or state registry.

## Clean up old Plans and Decisions

Only an explicit cleanup request covering the records authorizes cleanup,
including old, started, completed or cancelled Plans and their linked
Decisions in the requested scope; creating a Plan, reading and continuing work
clean up nothing. Read the complete affected blocks and the sources needed to
separate live conditions from redundancy.

| Field | Keep | Remove |
| --- | --- | --- |
| Instructions | Live conditions; an unclear condition. | Repeated actions or criteria, progress, results, obsolete conditions. Terminal fields normally become `[]`; report apparent unmet conditions without erasing them. |
| Evidence | Observed results, a required review's outcome, open defects and limits needed for development. | Review text, chronology, duplicate summaries, counts, versions or inventories without continuing purpose. |
| Goal | What [Write Goal](authoring.md#write-goal) keeps. | Superseded or demonstrably ended constraints, duplicated rationale and history; never an effect replaced by an unreadable ID. |
| Non-goals | Every still-binding exclusion. | Reasons and drafting notes. |

- Cleanup may shorten Outcome, Acceptance, Steps, Goal, Non-goals and accepted
  or deprecated Decisions in scope, including started and terminal history.
  Remove only filler and redundancy or merge equivalent conditions, apart
  from Decision relocation below; style alone permits no rewrite. Compare
  with the original: preserve the requested act, every required result, case,
  value, limit, quantifier, negation, exception, action, method and full
  verification scope. The same results must pass or fail before and after;
  `every endpoint` must not become `endpoints`. An obligation is not filler
  even when general or repeated elsewhere; selected cases cannot replace a
  general check. Keep required methods and checks in their historical field
  and replace no historical condition with a reference to text that can
  change. Keep uncertain text and resolve a material change before editing.
- Preserve IDs, Plan and Work Item statuses, execution annotations, Step
  order, dependencies, material Decisions under their lifecycle rules,
  completed effects and live user permissions, limits and stops. Change
  nothing outside the requested scope.
- For every Decision in scope, keep the ID, choice, every binding condition
  in its owning section including required checks and revisit triggers,
  authority, permissions, what is recorded as verified or unverified, and
  necessary reasons. Move binding content into its binding section without
  changing meaning; add or keep the [binding mark](decisions.md#binding-mark)
  only when nothing left in
  the background would affect choice, implementation, verification or
  revisit, and otherwise remove it and report the statement. A material
  change needs supersession under decisions.md.

Remove a Decision link only where it demonstrably governs nothing; keep
uncertain links and report missing relevant ones. Apply these transitions:

| Finding | Action |
| --- | --- |
| A temporary Decision's end or fulfilment is proved; no binding condition remains. | Deprecate it if accepted, reject it if proposed. |
| Equivalent duplicate; every binding effect remains with its owning Decision. | Deprecate or reject it; move its links to the owner, linking no item it did not govern. |
| A binding condition remains or its end is uncertain. | Keep the conditions and status. |

Age, status, a temporary title, filename or cancellation alone proves no end;
cancellation or expiry proves no passed check, waived condition or new
permission.

Delete a Decision file only when the request asks to remove records and no
kept Decision names it in `superseded_by`: a temporary one whose end is
proved, or a superseded one whose still-binding effects are readable in a
current record. First search all records for its
ID; keep constraints still in force, even unlinked, and what other open Plans
depend on. Remove its links and reciprocal supersession links in the same
update. Keep a record of uncertain meaning or relevance.

Do not repeat product tests, old reviews or a progress audit merely to shorten
records. Report the cleaned scope and any unresolved live condition briefly,
without a separate report.
