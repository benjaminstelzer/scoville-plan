---
name: scoville-plan
description: Create, maintain, resume, audit, and hand off project Plans, Work Items, and Decision records stored in the repository. Edit their Markdown and YAML directly. Owns their concise writing and wording audits under its own writing rules. Scribe writing rules do not apply to these records. Use when a task invokes Scoville Plan, requests repository-owned planning or decision records, must survive interruption or compaction, works in a format-version-1 project, receives a new instruction while an active Plan is running, or asks to add, remove, reorder, or clean up Plan points. Apply Plan-record maintenance directly and never create a Work Item whose only outcome is maintaining the Plan. Do not use for a pure informational question that requires no retained action, a small contained task that needs no durable plan, or an explicit opt-out.
compatibility: "Any Agent Skills host with read and write access to the repository's PROJECT_INDEX.md, docs/plans and docs/decisions. Direct Markdown and YAML edits only; requires no planning CLI, MCP server, database or network. Optional read-only selector and structural validator need Python 3. Developed for Codex and Claude Code; other hosts untested."
---

# Scoville Plan

Maintain repository direction through direct Markdown and YAML edits. Preserve
supported native `format_version: 1` behavior: setup, read-only
recovery, Plans, Work Items, Decisions, proposals, lifecycles, blockers,
evidence, and narrow repair. Require no CLI, MCP server, database, journal, or
hidden state; remove or reinterpret no project-knowledge feature.

A record does not prove work.

On explicit opt-out: read no references; do not create or change planning files;
make no Skill-derived claims. Report any exact conflict with a higher-priority
project instruction requiring this Plan system.

## Ownership and limits

Precedence:

1. system, safety, and explicit current-request instructions;
2. repository instructions and their canonical planning mechanism;
3. an existing supported native profile (the project index, Plans, and Decisions);
4. these defaults for gaps.

Use the existing durable owner; never create a parallel Plan. Apply compatible
guardrails only; runtime plans are disposable mirrors.

Never invoke a planning CLI. The optional bundled selector and validator are
strictly read-only and never a write path. The selector owns only the exact
current-or-named Work Item or dispatch-unit projection defined in the read-only route; proposal
discovery, relevant Evidence, graph inspection, and successor recovery remain
separate bounded reads. Claim no locking, atomic publication, typed mutation,
or semantic proof; report observations only.

Finding another Skill in this family does not make it installed, active, applicable, or required. If that Skill is absent or inactive, ignore it. Do not require, install, simulate, or reimplement it. If it is active and applicable, let it handle only its stated concern while this Skill continues its own authorized work. An opt-out applies only to the Skill the user excluded, not to independently authorized work.

Family owners, in suite order:

- `scoville-brainstorm`: deliberate divergence before selection.
- `scoville-research`: source-backed research and synthesis.
- `scoville-code-anti-ai-slop`: engineering scope, implementation, risk, and validation.
- `scoville-design-anti-ai-slop`: visual definition, art direction, critique, and repair.
- `scoville-ui-anti-ai-slop`: framework UI implementation, accessibility mechanics, and rendered proof.
- `scoville-scribe-anti-ai-slop`: wording, terminology, meaning, and source fidelity.
- `scoville-plan`: durable Plans, Work Items, Decisions, and lifecycle state.
- `scoville-handoff`: active-work transfer.

The private optional `scoville-workflow-codex` Skill may make Steps usable as
later dispatch units without activating or loading that Workflow. Group each
Step around one coherent outcome slice with comparable routing risk and
reasoning demand. Separate a trivial text edit from a complex structural change;
do not split code, UI, browser work, or other activities that share the same
outcome, risk, authorization, and Acceptance boundary. A user-selected executor
model or reasoning effort may be recorded only through the strict Step
annotation in the native format; otherwise the Workflow chooses the model and reasoning effort for execution.

Plan owns wording and fidelity of its native records. An explicit target
language takes precedence. Otherwise preserve the language of an existing Plan,
including new or edited Work Items in it. Use the user's request language for a
new Plan. Preserve an existing Decision's language; write a new Decision in its
Plan's language, or the user's request language when no Plan supplies one. Keep
required field names, section labels, IDs, and other format literals unchanged.
When Plan is available and applicable, load it if needed and use its own writing
rules for these records. Do not activate, load, or apply Scribe to their creation,
rewriting, or wording audit. A request to use Scribe does not override Plan's
writing rules. Plan also owns permitted edits, format, and lifecycle unless
opted out. If Scribe is active for another text segment, keep it scoped there.
Plan works without Scribe and never requires its installation.

## Choose planning and route references

Use a Plan for dependent outcomes, material sequencing, durable
handoff, or a binding workflow. Implement one small reversible change directly
unless the project requires a tracked Work Item.

Exact reference codes: `R` [read-only.md](references/read-only.md); `G`
[planning-granularity.md](references/planning-granularity.md); `P`
[native-plan-format.md](references/native-plan-format.md); `L`
[native-project-lifecycle.md](references/native-project-lifecycle.md); `E`
[native-editing.md](references/native-editing.md); `W`
[native-work-items.md](references/native-work-items.md); `D`
[native-decision-format.md](references/native-decision-format.md); `B`
[native-decision-batches.md](references/native-decision-batches.md); `V`
[profile-validation.md](references/profile-validation.md).

Classify the operation and edited record, then load exactly its route. An edit
inside a Work Item uses the Work Item route even though its file is a Plan.

| Operation | Load |
| --- | --- |
| Read direction or list records; no write | R |
| Initialize a wholly absent profile | G, P, L, E |
| Create or restructure Plan | G, P, L, E |
| Queue additive work received during active work | G, P, W, E |
| Directly insert, refine, move, select, block, advance, or remove Work Item | P, W, E |
| Record explicit human choice or possible material Decision | D, P, E |
| Apply explicitly authorized Decision transition | D, P, E |
| Apply explicitly authorized accept-or-reject batch | D, B, P, E |
| Activate, complete, or cancel Plan | P, L, W only if current work changes, E |
| Audit Plan structure or lifecycle | P; add G only for decomposition judgment |
| Audit Decision structure or lifecycle | D |
| Audit record wording | P for Plans or Work Items; D for Decisions |
| Rewrite Plan Goal or Non-goals | P, L, E |
| Rewrite Work Item wording | P, W, E |
| Rewrite Decision wording | D, P, E |
| Validate after writes or diagnose a complete supported profile | Use V for validation: run its optional validator when available, otherwise use the manual inspection described there. Then load only the native reference needed for a reported diagnostic or correction |

For read-only, preload no format guides. If profile existence is unknown,
list the root before canonical reads; never probe absent
`PROJECT_INDEX.md`. When the bundled selector and Python 3 are available, use
it for current-or-named Work Item selection through R; use R's bounded manual
fallback when it is unavailable. For an explicitly requested new durable Plan, use the
workspace as setup root, classify the whole profile, and initialize only if all
three canonical paths are absent. Use an existing complete supported profile.
If all three paths are absent and no durable Plan was requested, report that
absence without initializing. Preserve and stop
on partial, foreign, unsupported, invalid, or intent-invalid state unless the
route permits intent-preserving repair.

## Preserve authority and lifecycle

| Input or state | Required treatment |
| --- | --- |
| Goal, Non-goals, blocker, dependency, acceptance result, evidence, or lifecycle choice | Never invent. Implementation, ordinary documentation, source, silence, and current behavior are evidence, not authorization. |
| Activation, cancellation, changed scope, weaker Acceptance, ambiguous successor, or adoption of a possible material choice | If the required explicit choice has not already been authorized, ask before changing durable state. |
| User selects a direction, asks to preserve it in project rules, or applicable project instruction clearly records the human-selected direction | Create and accept its Decision without re-asking. |
| Analysis reveals a possible material Decision about scope, architecture, public behavior, stored data, security, dependencies, reversibility, Acceptance, migration, or rollout | Create `proposed`; report recommendation, alternatives, tradeoffs, and effect; ask to accept, reject, or revise. Do not pre-accept. |

Link each created Decision to every affected mutable Work Item.

Apply a historical stop to its recorded subject and scope. Compare it with the
current authorized work before blocking a different workflow; a stop for one
provider does not automatically stop another. Preserve applicable restrictions.
If their scope is material and unresolved, ask only about the dependent action;
do not infer permission from silence or discard a stop because it is old.

A proposal request creates `proposed`; a clear request to record the stated
choice authorizes acceptance. Reject, deprecate, supersede, activate, or cancel
only with the explicit lifecycle choice required by the route. For an
authorized multi-Decision accept-or-reject transition, use B and its helper
route; never substitute single-transition or audit behavior.

At work start, inventory Decision frontmatter and read every proposal. Report
ID/title/recommendation/effect, including proposals unrelated to current work.
Request accept|reject|revise when the requested work depends on that choice or
the user asks to handle Decisions. A status/listing request does not require a
decision answer. Preserve unresolved proposals at handoff; do not repeat an
unchanged decision question merely because another status turn occurs. New
decision-relevant evidence may warrant asking again. Stop only dependent work.

Mark a Work Item `done` only after observing Acceptance and adding concise
evidence. A captured structural-validation result supports only structural
judgment and reporting, never acceptance evidence or mutation authority. Keep
failed or partial work `in_progress`, `paused`, or explicitly blocked.

## Apply Plan maintenance without recursion

A request to add, remove, reorder, rewrite, or clean up Plan records is a direct
Plan-maintenance operation, not additive project work. Apply the permitted
record mutation through its normal route. Never create or queue a Work Item
whose Outcome is to maintain, update, or clean up the Plan.

When the user asks to add a Plan point for substantive future work, create or
refine only the Work Item that represents that substantive outcome. Do not add
a wrapper item such as "add the Plan point" or "update the Plan." A request
that only removes or reorganizes records creates no replacement Work Item.

Classify this direct-maintenance case before the mid-task rules below. Preserve
all ordinary lifecycle, history, dependency, Decision, and validation limits;
the recursion guard does not authorize deleting or rewriting a started or
terminal Work Item.

## Handle messages received during active work

When a supported active Plan owns running work and the user sends a message
before that work finishes, classify each part before changing execution or
native state:

- An explicit stop, pause, cancellation, or immediate redirect stops the live
  work at once. Apply only the lifecycle change the user actually authorized.
  When the user explicitly requires a later return to paused work, preserve
  that return in its live `Next action` through the Work Item route.
- A correction that invalidates or materially changes current execution stops
  that execution before more work is performed. Reconcile its effect through
  the ordinary Work Item or Decision routes. Do not rewrite started authored
  fields or infer cancellation from the need to stop.
- An additive request is work to perform after the current task. A plain
  imperative such as "do X" is additive unless the user makes it immediate or
  it corrects current execution. Persist it through the deferred-work operation
  without pausing, cancelling, or replacing the current item, and without
  beginning the deferred work.
- A pure informational or status question that requires no retained action
  receives the requested response and creates no Work Item. Continue the
  current work unless another part of the message changes it.

Classify mixed messages by part. Handle an interrupting correction first and
queue any independent additive part, so neither intent hides the other. For
additive work, make only the planning mutation needed to persist the queue,
verify that mutation, identify the affected Work Item to the user, and resume
the unchanged current work. Never acknowledge work as queued before its native
record is durable. Keep queue and explicit successor provenance visible in the
native Work Item titles defined by the deferred-work route, never only in chat.

This queue behavior requires a complete supported active native Plan. If the
request would exceed its Goal, violate its Non-goals, or require an unresolved
scope or lifecycle choice, keep the current work unchanged and ask only for
that choice while independent work continues. Do not claim a durable queue,
initialize a profile, or broaden the Plan implicitly. An explicit stop or
immediate redirect still governs live execution.

## Keep behavior-complete work

- Before starting the next `todo` Work Item in the active Plan, run a pre-flight
  for that item against the current repository state and evidence from its
  completed dependencies or other directly relevant completed Work Items in
  that Plan. For this pre-flight, do not scan completed or historical Plans or
  reread the entire active Plan without a concrete relevance reason. Check
  whether that evidence changed the item's premises, signatures, data models,
  contracts, paths, or validation assumptions. If so, refine that still-`todo`
  item through its normal route before execution. Never run stale instructions
  or rewrite started history.
- Split independently resumable outcomes when Acceptance, dependencies,
  ownership, or rollout timing differs. Put subordinate order in optional
  Steps. Put testing, review, documentation, and release checks in Acceptance
  or Evidence unless independently requested as resumable outcomes.
- For later Scoville Workflow use, one Step is one subplan dispatch point by
  default. An explicitly invoked Workflow with its own accepted Decision may
  bundle adjacent Steps only when they share one outcome, owner, authorization,
  route, workspace, and Acceptance boundary. A changed Decision, external
  effect, materially higher risk, different route, or independently resumable
  result forces a new dispatch. A bundle adds no Plan field and changes no
  authored order or Acceptance ownership. Give each Step a single routing class
  when confidently known, using an optional
  `[route: ultra_low|low|medium|high|ultra_high]` prefix. Record an explicit
  user-selected executor model or reasoning effort only through the optional
  Step execution annotation defined by P and W. When a still-`todo` Work Item
  has no Steps, add one behavior-complete annotated Step only if an explicit
  point choice must be retained. Without Steps, the whole Work Item remains one
  default-routed dispatch unit.
- Keep at most one Work Item `in_progress`, equal to `current_item`. This limits
  concurrency, not total Plan items.
- Change authored content or order only while `todo`. After start, preserve the
  starting approach and change only live state allowed by the route, except
  that W permits an explicit user choice to replace only the execution
  annotation of one named unperformed Step while preserving its action, route,
  and completed or running history.
- `Next action` is the first unperformed concrete action. After implementation,
  advance to the first unobserved test, build, browser check, review, or
  evaluator-owned verification.
- Select current work only when dependencies are done and the successor is
  explicit. Use `complete_and_advance` only when completion and the exact
  replacement start form one valid prepared result.
- When final real work finishes, complete its Work Item and Plan and set the
  index idle. Never invent a successor to keep the Plan active.

## Mutate narrowly and verify

### Write compact worker-ready records

Before drafting or refining a Plan, Work Item, or Decision:

1. Keep only facts needed to choose, execute, review, resume, or verify the work.
2. Assign each fact once to its owning field or section.
3. Put prerequisites before dependent actions and checks after the behavior they prove.
4. Remove any sentence that changes no choice, action, order, constraint, check, or recovery fact.

Before any Goal write, classify every fact in the complete proposed Goal, not
only the changed sentences. Goal owns only the current target, its boundary,
and genuinely plan-wide constraints. Route exclusions to Non-goals, material
choices to Decisions, point-specific scope, order, checks, model, or reasoning
to the affected Work Item or Step, observed results to Evidence, the next move
to Next action, and repository policy to its canonical project instruction;
omit irrelevant prose. Operational messages that change none of the Goal-owned
semantics leave its bytes unchanged. Moving existing Goal facts to other fields requires separate authorization.
Before that normalization, check that every affected future dispatch can still
reach each needed requirement through its selected Work Item, a referenced
Decision, or a repository contract demonstrably loaded for that dispatch. Do
not create a second requirement registry, truncate selector output, or use a
size limit as a substitute for ownership.

State the concept first in Goal, Outcome, or Decision. Use compact bullets for
equal-rank facts and numbered Steps for execution order. Each Step names one
concrete action, its target, and the necessary result. When a repository-relative
file is already known, cite it directly in the Step that changes or checks it.
When the owner is unknown, prefer bounded read-only discovery before starting
the item, then refine its `todo` Steps with the observed path. If discovery must
happen after start, keep its ownership criterion in the immutable Step and put
the observed path in Evidence and the next concrete action. Never invent a path.

Write for a worker with lower reasoning and no hidden conversation context. The
worker and reviewer must be able to identify the result, scope, applicable
choices, exact order, targets, blockers, and proof without reconstructing omitted
intent. Split a dense compound instruction instead of compressing it into an
ambiguous sentence. Do not repeat rationale to make a record look complete.

Preserve constraints, alternatives, tradeoffs, uncertainty, exact identifiers,
Acceptance, and Evidence. Brevity never authorizes immutable-history changes,
weaker proof, or invented verification. Keep already concise text. Use no fixed
word or sentence count as a quality substitute. The structural validator does
not perform this semantic check.

### Apply and check edits

Before writing, confirm root, format, active Plan, current Work Item, affected
bytes, outcome, and required acceptance evidence. Use context-bound patches;
preserve unrelated work. Prepare and inspect the full multi-file result before
applying any member.

After writing:

1. reread changed frontmatter and complete affected Work Item or Decision blocks;
2. inspect the scoped diff and check changed prose against the compact-record rules;
3. check index ownership, active-Plan count, current-item status, Work Item key
   order, dependency order and cycles, Decision and Plan references, blockers,
   lifecycle fields, Evidence, and `Next action`;
4. when its script and Python are already available, run the optional validator
   through V; otherwise perform and report the scoped manual inspection;
5. record only acceptance evidence observed for the mutation.

Use E's scoped-read rules: complete byte and structural checks need not print
unchanged history. Widen reads when the operation or a diagnostic requires it.

During mutation, also stop on concurrent changes, ambiguous lifecycle authority,
or a partial multi-file transition.
Do not overwrite a problem into apparent validity.

## Report durable state

Lead with Plan outcome. Name changed canonical files, active/blocked work,
observed checks/evidence, unresolved choices, and next action. Distinguish native
structural inspection from behavioral verification; omit routine file narration.
