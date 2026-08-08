---
name: scoville-plan
description: Repository-native planning guardrail for creating, maintaining, resuming, auditing, and handing off durable project Plans, Work Items, and Decision records through direct Markdown and YAML edits only. Use when a task invokes Scoville Plan, requests repository-owned implementation planning or decision records, must survive interruption or compaction, or works in a format-version-1 project with PROJECT_INDEX.md, docs/plans, and docs/decisions. Do not use for a small contained task that needs no durable plan, or when the user explicitly opts out of Scoville Plan.
---

# Scoville Plan

Keep project direction in reviewable repository files without requiring a
planning CLI, MCP server, database, journal, or hidden state. This Skill owns
planning discipline and native Plan and Decision maintenance. It records
choices humans have already made and preserves a material unresolved choice as
a proposal before asking for its lifecycle decision. It does not grant inferred
choices authority or prove that reported work happened.

Keep the complete supported `format_version: 1` feature surface: read-only
recovery, setup, Plans, Work Items, Decisions, proposals, lifecycle, blockers,
evidence, and narrow repair. Use direct native edits without removing or
reinterpreting a project-knowledge feature.

On explicit opt-out, do not read references, create or change planning files,
or make Skill-derived claims. If a higher-priority project instruction requires
this Plan system, report that exact conflict. A sibling Scoville opt-out excludes
only that sibling.

## Follow the existing owner

Resolve planning requirements in this order:

1. system, safety, and explicit instructions for the current request;
2. repository instructions and its existing canonical planning mechanism;
3. an existing supported native profile; and
4. this Skill's defaults for what remains unspecified.

Never create a second plan beside a project-owned plan. If another durable plan
system already owns state, use it and apply only this Skill's planning-quality
guardrails where compatible. A runtime plan is a disposable mirror, never a
second canonical owner.

This Skill has no required executable dependency and never invokes a planning
CLI. Its bundled Python validator is an optional strictly read-only structural
check, never a write path. Do not claim locking, atomic multi-file publication,
typed mutation safety, or semantic proof. Use ordinary scoped file tools and
report only the checks actually performed.

This Skill works independently. Never require, install, or simulate Code, UI,
or Scribe. When a sibling is independently applicable, compose only its owned
implementation, interface, or wording concern; its absence does not weaken
Plan structure, lifecycle, authority, or evidence rules.

## Decide whether durable planning is warranted

Use a repository Plan for multiple dependent outcomes, material sequencing,
work that must survive interruption or handoff, or a binding project workflow.
For one small reversible change, implement and validate directly unless the
project already requires a tracked Work Item.

Classify the operation before loading details:

| Operation | Load |
| --- | --- |
| Read current direction or list records without writing | [read-only.md](references/read-only.md) |
| Initialize a wholly absent profile | [planning-granularity.md](references/planning-granularity.md), [native-plan-format.md](references/native-plan-format.md), [native-project-lifecycle.md](references/native-project-lifecycle.md), and [native-editing.md](references/native-editing.md) |
| Create or restructure a Plan | [planning-granularity.md](references/planning-granularity.md), [native-plan-format.md](references/native-plan-format.md), [native-project-lifecycle.md](references/native-project-lifecycle.md), and [native-editing.md](references/native-editing.md) |
| Insert, refine, move, select, block, advance, or remove a Work Item | [native-plan-format.md](references/native-plan-format.md), [native-work-items.md](references/native-work-items.md), and [native-editing.md](references/native-editing.md) |
| Record an explicit human choice or a material possible Decision | [native-decision-format.md](references/native-decision-format.md), [native-plan-format.md](references/native-plan-format.md), and [native-editing.md](references/native-editing.md) |
| Apply an explicitly authorized Decision transition | [native-decision-format.md](references/native-decision-format.md), [native-plan-format.md](references/native-plan-format.md), and [native-editing.md](references/native-editing.md) |
| Apply an explicitly authorized accept-or-reject batch | [native-decision-format.md](references/native-decision-format.md), [native-decision-batches.md](references/native-decision-batches.md), [native-plan-format.md](references/native-plan-format.md), and [native-editing.md](references/native-editing.md) |
| Activate, complete, or cancel a Plan | [native-plan-format.md](references/native-plan-format.md), [native-project-lifecycle.md](references/native-project-lifecycle.md), [native-work-items.md](references/native-work-items.md) when current work changes, and [native-editing.md](references/native-editing.md) |
| Audit native Plan structure or lifecycle | [native-plan-format.md](references/native-plan-format.md); add [planning-granularity.md](references/planning-granularity.md) only when judging decomposition |
| Audit native Decision structure or lifecycle | [native-decision-format.md](references/native-decision-format.md) |
| Validate after native writes or diagnose a complete supported profile | Run the bundled check through [profile-validation.md](references/profile-validation.md), then load only the native reference needed for a reported diagnostic or correction |

Do not preload format details for a read-only status answer.

When profile existence is unknown, list the project root before reading any
canonical path. If `PROJECT_INDEX.md` is absent, do not attempt to read it. For
an explicitly requested new durable Plan, treat the current workspace as the
setup root, classify the complete profile, and initialize only when all three
canonical paths are wholly absent. If creation was not requested, report that
no profile exists instead of initializing one implicitly. Preserve and stop on
a partial, foreign, unsupported, or intent-invalid profile.

## Preserve authority and evidence

- Never invent the Goal, Non-goals, acceptance result, blocker, dependency,
  evidence, or an accepted lifecycle choice. Treat implementation, ordinary
  documentation, source code, silence, and current behavior as evidence, not as
  human authorization.
- Ask before activation, cancellation, changed scope, weaker acceptance, an
  ambiguous successor, or adopting a merely possible material choice.
- When the user explicitly selects a direction, asks to preserve it in project
  rules, or an applicable project instruction unmistakably states a
  human-selected direction, create and accept the corresponding Decision
  without asking again. Link every affected mutable Work Item.
- When analysis only reveals a possible material Decision about scope,
  architecture, public behavior, stored data, security, dependencies,
  reversibility, acceptance, migration, or rollout, create it as `proposed`,
  link every affected mutable Work Item, report its recommendation,
  alternatives, tradeoffs, and practical effect, then ask the user to accept,
  reject, or revise it. Do not accept it before that answer.
- A request to draft a proposal creates `proposed`. A clear choice to record
  the stated direction authorizes its acceptance. Never reject, deprecate, or
  supersede a Decision without that explicit lifecycle choice.
- At the start of project work, inventory Decision frontmatter, read every
  proposal, report its ID, title, recommended choice, and practical effect, and
  ask the user to accept, reject, or revise it. Repeat unresolved proposals at
  handoff. Only dependent work stops.
- Mark a Work Item `done` only after observing its Acceptance result and adding
  concise evidence. A file-shape check proves structure only.
- Keep failed or partial work `in_progress`, `paused`, or explicitly blocked.

## Keep behavior-complete Work Items

- Keep at most one Work Item `in_progress`, equal to `current_item`. This limits
  concurrent execution; it does not limit a Plan to one Work Item in total.
- Split independently resumable outcomes with distinct acceptance boundaries,
  dependencies, owners, or rollout timing into separate Work Items.
- Keep implementation order inside optional Steps. Testing, review,
  documentation, and release checks belong in Acceptance or Evidence unless
  independently requested deliverables need their own resumable outcome.
- Change authored content or ordering only while an item is `todo`. After it
  starts, preserve its starting approach and update only live state.
- Keep `Next action` equal to the first concrete action not yet performed. Once
  implementation exists, advance it to the next unobserved test, build, browser
  check, review, or evaluator-owned verification.
- Select new current work only when its dependencies are done and the successor
  is explicit. Use `complete_and_advance` only when completion and the exact
  replacement start are both valid as one prepared result.
- When final real work completes, complete its Work Item and Plan and set the
  project index to idle. Never invent a successor merely to keep it active.

## Work natively and narrowly

Before writing, confirm the project root, supported format, active Plan,
current Work Item, affected bytes, observable outcome, and acceptance evidence.
Use context-bound patches and preserve unrelated work. Prepare a complete
multi-file change before applying any member, while acknowledging that direct
edits are not atomic.

After writing:

1. reread every changed canonical file;
2. inspect the complete scoped diff;
3. check index ownership, active-Plan count, current-item status, Work Item key
   order, dependency order and cycles, Decision and Plan references, blockers,
   lifecycle fields, Evidence, and `Next action`;
4. run the bundled optional validator through
   [profile-validation.md](references/profile-validation.md) when its script and
   Python are already available, otherwise perform and report the scoped manual
   inspection; and
5. record only observed acceptance evidence.

Stop on unsupported format, concurrent changes, ambiguous lifecycle authority,
invalid state whose repair would alter intent, or a partial multi-file
transition. Do not overwrite the problem into apparent validity.

## Report the durable state

Lead with the current Plan outcome. Name changed canonical files, active and
blocked work, observed checks, recorded evidence, unresolved material choices,
and the next concrete action. Distinguish native structural inspection from
behavioral verification. Do not narrate routine file operations.
