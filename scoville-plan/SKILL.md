---
name: scoville-plan
description: Repository-native planning guardrail for creating, maintaining, resuming, auditing, and handing off durable project Plans, Work Items, and Decision records through direct Markdown and YAML edits only. Use when a task invokes Scoville Plan, requests repository-owned implementation planning or decision records, must survive interruption or compaction, or works in a format-version-1 project with PROJECT_INDEX.md, docs/plans, and docs/decisions. Do not use for a small contained task that needs no durable plan, or when the user explicitly opts out of Scoville Plan.
---

# Scoville Plan

Maintain repository direction through direct Markdown and YAML edits. Preserve
supported native `format_version: 1` behavior: setup, read-only
recovery, Plans, Work Items, Decisions, proposals, lifecycles, blockers,
evidence, and narrow repair. Require no CLI, MCP server, database, journal, or
hidden state; remove or reinterpret no project-knowledge feature.

Record human choices; preserve a material unresolved choice as `proposed`
pending its lifecycle decision. Inference grants no authority; a
record does not prove work.

On explicit opt-out: read no references; do not create or change planning files;
make no Skill-derived claims. Report any exact conflict with a higher-priority
project instruction requiring this Plan system. A sibling opt-out excludes only
that sibling.

## Ownership and limits

Apply this precedence:

1. system, safety, and explicit current-request instructions;
2. repository instructions and their canonical planning mechanism;
3. an existing supported native profile;
4. these defaults for gaps.

Use an existing durable owner; never create a parallel Plan. Apply only
compatible guardrails. A runtime plan is a disposable mirror.

Never invoke a planning CLI or require executables. The optional bundled
validator is strictly read-only and structural, never a write path. Claim no
locking, atomic multi-file publication, typed mutation safety, or semantic
proof; report only observed checks.

Never require, install, or simulate Code, UI, or Scribe. Compose an applicable
sibling only for owned implementation, interface, or wording; its
absence changes no Plan structure, lifecycle, authority, or evidence rule.

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

Classify the operation, then load exactly its route:

| Operation | Load |
| --- | --- |
| Read direction or list records; no write | R |
| Initialize a wholly absent profile | G, P, L, E |
| Create or restructure Plan | G, P, L, E |
| Insert, refine, move, select, block, advance, or remove Work Item | P, W, E |
| Record explicit human choice or possible material Decision | D, P, E |
| Apply explicitly authorized Decision transition | D, P, E |
| Apply explicitly authorized accept-or-reject batch | D, B, P, E |
| Activate, complete, or cancel Plan | P, L, W only if current work changes, E |
| Audit Plan structure or lifecycle | P; add G only for decomposition judgment |
| Audit Decision structure or lifecycle | D |
| Validate after writes or diagnose a complete supported profile | Run V; then only the native reference for a reported diagnostic or correction |

For read-only, preload no format guides. If profile existence is unknown,
list the root before canonical reads; never probe absent
`PROJECT_INDEX.md`. For an explicitly requested new durable Plan, use the
workspace as setup root, classify the whole profile, and initialize only if all
three canonical paths are absent. Otherwise report absence. Preserve and stop
on partial, foreign, unsupported, invalid, or intent-invalid state unless the
route permits intent-preserving repair.

## Preserve authority and lifecycle

| Input or state | Required treatment |
| --- | --- |
| Goal, Non-goals, blocker, dependency, acceptance result, evidence, or lifecycle choice | Never invent. Implementation, ordinary documentation, source, silence, and current behavior are evidence, not authorization. |
| Activation, cancellation, changed scope, weaker Acceptance, ambiguous successor, or adoption of a possible material choice | Ask before changing durable state. |
| User selects a direction, asks to preserve it in project rules, or applicable project instruction clearly records the human-selected direction | Create and accept its Decision without re-asking; link every affected mutable Work Item. |
| Analysis reveals a possible material Decision about scope, architecture, public behavior, stored data, security, dependencies, reversibility, Acceptance, migration, or rollout | Create `proposed`; link affected mutable Work Items; report recommendation, alternatives, tradeoffs, and effect; ask to accept, reject, or revise. Do not pre-accept. |

A proposal request creates `proposed`; a clear request to record the stated
choice authorizes acceptance. Reject, deprecate, supersede, activate, or cancel
only with the explicit lifecycle choice required by the route. For an
authorized multi-Decision accept-or-reject transition, use B and its helper
route; never substitute single-transition or audit behavior.

At project-work start, inventory Decision frontmatter and read every proposal.
Report ID, title, recommended choice, and practical effect; request accept,
reject, or revise. Repeat unresolved proposals at handoff; stop only dependent
work.

Mark a Work Item `done` only after observing Acceptance and adding concise
evidence. A captured structural-validation result supports only structural
judgment and reporting, never acceptance evidence or mutation authority. Keep
failed or partial work `in_progress`, `paused`, or explicitly blocked.

## Keep behavior-complete work

- Split independently resumable outcomes when Acceptance, dependencies,
  ownership, or rollout timing differs. Put subordinate order in optional
  Steps. Put testing, review, documentation, and release checks in Acceptance
  or Evidence unless independently requested as resumable outcomes.
- Keep at most one Work Item `in_progress`, equal to `current_item`. This limits
  concurrency, not total Plan items.
- Change authored content or order only while `todo`. After start, preserve the
  starting approach and change only live state allowed by the route.
- `Next action` is the first unperformed concrete action. After implementation,
  advance to the first unobserved test, build, browser check, review, or
  evaluator-owned verification.
- Select current work only when dependencies are done and the successor is
  explicit. Use `complete_and_advance` only when completion and the exact
  replacement start form one valid prepared result.
- When final real work finishes, complete its Work Item and Plan and set the
  index idle. Never invent a successor to keep the Plan active.

## Mutate narrowly and verify

Before writing, confirm root, format, active Plan, current Work Item, affected
bytes, outcome, and required acceptance evidence. Use context-bound patches;
preserve unrelated work. Prepare and inspect the full multi-file result before
applying any member; direct edits remain non-atomic.

After writing:

1. reread each changed canonical file;
2. inspect the scoped diff;
3. check index ownership, active-Plan count, current-item status, Work Item key
   order, dependency order and cycles, Decision and Plan references, blockers,
   lifecycle fields, Evidence, and `Next action`;
4. when its script and Python are already available, run the optional validator
   through V; otherwise perform and report the scoped manual inspection;
5. record only acceptance evidence observed for the mutation.

Stop on unsupported format, concurrent changes, ambiguous lifecycle authority,
invalid state whose repair changes intent, or a partial multi-file transition.
Do not overwrite a problem into apparent validity.

## Report durable state

Lead with Plan outcome. Name changed canonical files, active and blocked
work, observed checks, recorded evidence, unresolved material choices, and the
next action. Distinguish native structural inspection from behavioral
verification; omit routine file-operation narration.
