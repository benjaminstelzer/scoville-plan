# Work Item and Step checklist

- Use a Work Item for a result that can be accepted, blocked, resumed or handed
  off independently. Separate materially different acceptance, dependency,
  ownership, rollout or blocker boundaries.
- Keep implementation, tests, review and documentation together when they prove
  the same behavior. Make them separate items only for independently requested
  outcomes; file count and activity names do not define boundaries.
- Use numbered Steps for ordered behavior-complete units within an item. Keep
  necessary intermediate actions inside their unit, not as extra dispatches.
  Put prerequisites and canonical-owner changes before dependent consumers.
- Name known repository-relative paths, interacting owners, necessary discovery
  and verification that needs interpretation. Resolve unknown owners before
  start when practical; otherwise retain the criterion and record the discovered
  path in Evidence and Next action without rewriting started Steps.
- Include enough context to execute without chat history. Acceptance owns proof
  criteria, Evidence owns observations, and Next action owns the next unfinished
  action. Do not create duplicate testing or bookkeeping Steps.

Separate Steps with materially different consequence or reasoning demand.
Preserve existing `[route: ...]` and `[execute: ...]` annotations; Plan defines
no route classes or inferred execution settings. Writing Steps does not activate
Workflow. An item without Steps is one default execution unit.

One Step is one dispatch by default. An explicitly invoked Workflow may bundle
adjacent Steps only under its accepted Decision and a shared outcome, owner,
authorization, route, workspace and Acceptance boundary. Changed Decisions,
external effects, higher risk, different routes or independently resumable
results require separate dispatch. Bundling changes no authored order, fields
or acceptance ownership. Steps gain no independent lifecycle.
