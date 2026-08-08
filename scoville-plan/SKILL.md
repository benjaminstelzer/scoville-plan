---
name: scoville-plan
description: Repository-native planning guardrail for creating, maintaining, resuming, auditing, and handing off durable project Plans and Work Items through direct Markdown and YAML edits only. Use when a task invokes Scoville Plan, requests a repository-owned implementation plan, must survive interruption or compaction, or works in a format-version-1 project with PROJECT_INDEX.md and docs/plans. Do not use for a small contained task that needs no durable plan, or when the user explicitly opts out of Scoville Plan.
---

# Scoville Plan

Keep project direction in reviewable repository files without requiring a
planning CLI, MCP server, database, journal, or hidden state. This Skill owns
planning discipline and native Plan maintenance, not product choices or proof
that reported work happened.

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

This Skill has no executable dependency and never invokes the ReasonKeep CLI.
Do not claim CLI validation, locking, atomic multi-file publication, or typed
mutation safety. Use ordinary scoped file tools and report the manual checks
actually performed.

## Decide whether durable planning is warranted

Use a repository Plan for multiple dependent outcomes, material sequencing,
work that must survive interruption or handoff, or a binding project workflow.
For one small reversible change, implement and validate directly unless the
project already requires a tracked Work Item.

Classify the operation before loading details:

| Operation | Load |
| --- | --- |
| Read current direction without writing | Read `PROJECT_INDEX.md`, then only the active Plan's current Work Item and its existing Decision references |
| Create or restructure a Plan | [planning-granularity.md](references/planning-granularity.md), then [native-plan-format.md](references/native-plan-format.md) and [native-editing.md](references/native-editing.md) |
| Change Plan or Work Item state | [native-plan-format.md](references/native-plan-format.md) and [native-editing.md](references/native-editing.md) |
| Audit native Plan structure or lifecycle | [native-plan-format.md](references/native-plan-format.md); add [planning-granularity.md](references/planning-granularity.md) only when judging decomposition |

Do not preload format details for a read-only status answer.

When profile existence is unknown, list the project root before reading any
canonical path. If `PROJECT_INDEX.md` is absent, do not attempt to read it. For
an explicitly requested new durable Plan, treat the current workspace as the
setup root, load the three creation references, and create the native profile.
If creation was not requested, report that no profile exists instead of
initializing one implicitly.

## Preserve authority and evidence

- Never invent the Goal, Non-goals, scope, acceptance result, blocker,
  dependency, Decision, evidence, or lifecycle choice.
- Ask before activation, cancellation, changed scope, weaker acceptance, an
  ambiguous successor, or a material product or architecture choice.
- Do not create or transition Decision records. Preserve existing Decision
  references; route new material decisions through the repository's established
  decision mechanism or ask the user.
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
   order, dependency order and cycles, references, blockers, lifecycle fields,
   Evidence, and `Next action`;
4. run the repository's validator only when it is independently available and
   authorized, never as a dependency of this Skill; and
5. record only observed acceptance evidence.

Stop on unsupported format, concurrent changes, ambiguous lifecycle authority,
invalid state whose repair would alter intent, or a partial multi-file
transition. Do not overwrite the problem into apparent validity.

## Report the durable state

Lead with the current Plan outcome. Name changed canonical files, active and
blocked work, observed checks, recorded evidence, unresolved material choices,
and the next concrete action. Distinguish native structural inspection from
behavioral verification. Do not narrate routine file operations.
