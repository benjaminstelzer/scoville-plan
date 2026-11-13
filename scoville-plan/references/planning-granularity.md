# Work Item and Step checklist

Size and shape work for the maintenance and development intent retained in
Goal/Non-goals under [authoring.md](authoring.md). Use the simplest sound solution
in the responsible file or component.

- Use a Work Item for a result that can be accepted, blocked, resumed or handed
  off independently. Separate items whose acceptance, dependencies,
  responsible party, rollout or blockers differ materially.
- Keep implementation, tests, review and documentation together when they prove
  the same behavior. Make them separate items only for independently requested
  outcomes; file count and activity names do not define boundaries.
- Keep prerequisite test and fixture corrections with that outcome when they
  preserve its scope and Acceptance. Group repairs with a common cause; do not
  create a Work Item for every failure or formal metadata change.
- Use numbered Steps for ordered behavior-complete units within an item. Keep
  a unit's intermediate actions inside it, not as extra Steps. Put prerequisites and changes to the canonical source before its consumers.
- Name known repository-relative paths, interacting files or components,
  necessary discovery and checks that need interpretation. Find unknown ones
  before start when practical; otherwise retain the criterion and record the
  discovered path in Evidence without rewriting started Steps.
- Use progress.md's continuation contract and authoring.md's field rules.
  Write no Step that only does bookkeeping or repeats another Step's testing;
  it only adds a dispatch.

Separate Steps whose consequences or reasoning demand differ materially. Preserve existing `[route: ...]` and `[execute: ...]`
annotations; Plan defines no route classes and infers no execution settings.
Writing Steps does not start execution.

Size planned Steps as manageable, checkable results, normally finishable within
the executing agent's context window with their necessary intermediate actions and checks.
Before execution, split planned work whose required sources, checks or output would not fit,
using progress.md's editing rights. Split by result, not by file, owner or
sentence quotas.
If compaction nevertheless occurs, continue the same original assignment with
its remaining work. It changes neither assignee nor original Step boundaries.
A legacy item without Steps may be one default
execution unit.
