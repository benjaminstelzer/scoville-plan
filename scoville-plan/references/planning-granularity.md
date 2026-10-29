# Work Item and Step checklist

Size and shape work for the maintenance and development intent retained in
Goal/Non-goals under [authoring.md](authoring.md). Use the simplest sound solution
at the responsible owner.

- Use a Work Item for a result that can be accepted, blocked, resumed or handed
  off independently. Separate materially different acceptance, dependency,
  ownership, rollout or blocker boundaries.
- Keep implementation, tests, review and documentation together when they prove
  the same behavior. Make them separate items only for independently requested
  outcomes; file count and activity names do not define boundaries.
- Keep prerequisite test and fixture corrections with that outcome when they
  preserve its scope and Acceptance. Group repairs with a common cause; do not
  create a Work Item for every failure or formal metadata change.
- Use numbered Steps for ordered behavior-complete units within an item. Keep
  necessary intermediate actions inside their unit, not as extra dispatches.
  Put prerequisites and canonical-owner changes before dependent consumers.
- Name known repository-relative paths, interacting owners, necessary discovery
  and verification that needs interpretation. Resolve unknown owners before
  start when practical; otherwise retain the criterion and record the discovered
  path in Evidence without rewriting started Steps.
- Use progress.md's continuation contract and authoring.md's field rules.
  Do not create duplicate testing or bookkeeping Steps.

Separate Steps with materially different consequence or reasoning demand.
Preserve existing `[route: ...]` and `[execute: ...]` annotations; Plan defines
no route classes or inferred execution settings. Writing Steps does not activate
Workflow.

Size planned Steps as manageable, checkable results, normally finishable within
the executing agent's context window with their necessary intermediate actions and checks.
Before execution, split planned work whose required sources, checks or output would not fit,
using progress.md's editing rights. Do not split by file, owner or sentence quotas
or create separate bookkeeping or duplicate verification Steps.
If compaction nevertheless occurs, continue the same original assignment with
its remaining work. It changes neither ownership nor the original Step boundaries.
A legacy item without Steps may be one default
execution unit.
