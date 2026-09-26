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

Group Steps to avoid repeated setup and handoffs while keeping a clear,
checkable result. A useful group produces one coherent result that a worker can
implement and verify with the supplied context. Keep its implementation and
necessary checks together; do not group merely to reduce the number of workers.
Before choosing a group, identify the repeated setup it saves and the concrete
result its final checks can prove. If either is unclear, revise the grouping.
Group small, related consecutive Steps when they can be implemented and checked
together. Keep independently substantial sections separate. Preserve Step order
within and across groups. Workflow follows supplied grouping, or chooses it at
dispatch when none is supplied. Grouping changes no authored Steps or acceptance
ownership and adds no separate lifecycle. Context rollover continues the same
assigned group with its remaining work.

When proposing groups, name the Plan, Step ranges and why they belong together
in one or two sentences. This is a brief explanation, not Workflow activation.
