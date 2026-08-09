# Scoville Plan

Keeps project direction recoverable. Keeps planning machinery out of the way.

Planning slop looks organized while making the work harder to resume:

- One omnibus item hides several independently blockable outcomes.
- Implementation, testing, review, and release become separate Work Items even
  though none produces an independently resumable result.
- A new journal or runtime plan appears beside the repository's real plan.
- A choice already settled by a human remains trapped in chat or project rules
  instead of becoming a linked Decision record.
- An item becomes `done` because files exist, not because its acceptance result
  was observed.
- `Next action` still says "implement" after the implementation was written.

Scoville Plan is an Agent Skill for creating, maintaining, resuming, auditing,
and handing off durable project Plans, Work Items, and Decisions through direct
Markdown and YAML edits. It preserves one canonical planning owner, records
clear human choices without redundant approval loops, keeps Work Items
behavior-complete, and separates authored state from observed evidence. It
does not require a planning CLI, MCP server, database, journal, or hidden state.

Its native `format_version: 1` profile provides the complete Skill-only
workflow: setup, read-only recovery, Plan and Work Item operations, Decision
proposals and lifecycle, blockers, evidence, activation, completion, and narrow
repair. An optional standard-library Python validator checks the complete
profile without changing it. Direct writes still have no publication gate,
typed requests, expected-hash writer, rollback, or multi-file atomicity; native
editing compensates but does not rename those missing guarantees into
existence.

The plan is a map of unfinished outcomes, not a scrapbook of agent activity.

## Why "Scoville Plan"?

The Scoville family is named for signal that remains detectable after
dilution. In planning, that signal is the project direction another person or
agent must recover: what outcome matters, what is active, what blocks it, what
proves completion, and what happens next. Scoville Plan keeps that signal in
reviewable repository files instead of diluting it across status messages,
private state, and ceremonial checklists.

## Install

Works with any coding agent that supports the Agent Skills format: a `SKILL.md`
instruction file with its name and description at the top. Compatible agents
include Claude Code and Codex.

Usually, let your coding agent install the skill. Send it this prompt:

```text
Install this Agent Skill from GitHub and make it available for my project planning work:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
```

Add "for all my projects" or "only for this project" when the installation
scope matters. The agent should choose its supported skills directory, install
the skill directory under the unchanged name `scoville-plan`, and refresh its
skill list.

If your agent cannot install skills itself, copy the repository's
`scoville-plan/` directory so the final path is:

```text
<skills-dir>/scoville-plan/SKILL.md
```

For Claude Code, `<skills-dir>` is `~/.claude/skills/` for all projects or
`.claude/skills/` inside a repository for that project only. For other agents,
consult their documentation; paths differ per agent.

**Verify it works.** Ask the agent: *"Use Scoville Plan to review whether a
migration's schema, compatibility, consumer update, and rollout outcomes should
be separate Work Items. Do not change files."* The agent should distinguish
independently resumable outcomes from subordinate implementation steps, retain
the repository's existing planning owner, and avoid creating a parallel plan.

As a negative check, ask for one small reversible change in a repository with
no durable planning requirement. Scoville Plan should not initialize a profile
or turn the change into a planning exercise.

**What it costs.** Skill discovery exposes only the name and description. After
activation, the core loads first and selects planning granularity, Plan format,
Decision format, batch-transition, and native editing guidance only when the
operation needs them. Provider token usage also depends on the host and
conversation.

## What it enforces

- **One durable planning owner.** Existing repository instructions and planning
  records stay authoritative. A runtime plan may mirror them temporarily but
  never becomes a second canonical source.
- **Durable planning only when it earns its keep.** Multiple dependent outcomes,
  material sequencing, interruption, handoff, or a binding workflow justify a
  repository Plan. One small reversible change normally does not.
- **Behavior-complete Work Items.** Independently resumable outcomes receive
  separate items. Implementation order belongs in optional Steps; testing,
  review, documentation, and release checks remain Acceptance or Evidence
  unless they are independently requested deliverables.
- **Concurrency is not cardinality.** At most one Work Item may be
  `in_progress`, and it must match `current_item`. The Plan may still contain as
  many `todo`, `done`, or `cancelled` items as its real outcome boundaries need.
- **Evidence before completion.** A Work Item becomes `done` only after its
  Acceptance result was observed and concise evidence was recorded. File shape
  proves structure, not behavior.
- **A real next action.** `Next action` names the first concrete action not yet
  performed. After implementation, it advances to the next unobserved test,
  build, browser check, review, or evaluator-owned verification.
- **Complete native lifecycle.** The skill initializes a wholly absent profile,
  creates and refines Plans, inserts, moves, selects, blocks, advances, and
  removes eligible Work Items, activates replacement Plans, and completes final
  work into a valid idle project.
- **Visible unresolved direction.** Every material open choice becomes a linked
  `proposed` Decision and is repeated at handoff until accepted, rejected, or
  revised. Only dependent work stops.
- **Honest native editing.** Direct edits use narrow reads, context-bound
  patches, complete diff inspection, and manual invariant checks. The skill
  never claims transactional or typed CLI guarantees it does not possess.
- **Optional read-only validation.** A bundled Python script reports stable
  JSON diagnostics for local format, cross-record links, lifecycle invariants,
  unsafe paths, incomplete reads, and concurrent changes. It has no repair
  mode and never replaces behavioral evidence or human authority.
- **Decisions without approval theatre.** An explicit user choice or an
  applicable project rule that unmistakably records a human-selected direction
  becomes an accepted Decision without asking again. The skill links it from
  affected mutable Work Items.
- **Proposals before inferred authority.** When analysis reveals a material
  possible Decision, the skill stores it as `proposed`, links affected mutable
  Work Items, reports its recommendation, alternatives, tradeoffs, and
  practical effect, then asks for `accept`, `reject`, or `revise`. It never
  treats creating the proposal as acceptance.
- **No invented lifecycle authority.** Draft-only requests remain `proposed`.
  Rejection, deprecation, and supersession require the corresponding explicit
  human choice; implementation and silence never count.

The full rules live in [SKILL.md](scoville-plan/SKILL.md).

## Use with the Scoville family

Plan works independently. When companion Skills are installed, combine them
only for the concerns they own.

Use [Scoville Code Anti-AI-Slop](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop)
for implementation scope, canonical code ownership, engineering risk, and
proportionate verification. Use
[Scoville UI Anti-AI-Slop](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop)
for interface hierarchy, framework alignment, accessibility, responsiveness,
and rendered evidence. Use
[Scoville Scribe Anti-AI-Slop](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop)
for reader-facing wording, terminology, factual meaning, and source fidelity.

Plan owns durable direction and Work Item lifecycle. Code, UI, and Scribe own
the quality and proof of the implementation and artifacts needed to deliver
that direction. A Plan acceptance boundary may require their evidence without
copying their rules into the Plan.

## Design

Scoville Plan first resolves the existing planning owner and decides whether
the task warrants durable state. It conditionally loads nine focused guides:

- [references/planning-granularity.md](scoville-plan/references/planning-granularity.md)
  distinguishes independently resumable outcomes from subordinate steps and
  acceptance checks.
- [references/native-plan-format.md](scoville-plan/references/native-plan-format.md)
  defines the supported `format_version: 1` Plan and Work Item file contract.
- [references/native-decision-format.md](scoville-plan/references/native-decision-format.md)
  defines Decision records, links, and explicitly authorized lifecycle
  transitions.
- [references/native-decision-batches.md](scoville-plan/references/native-decision-batches.md)
  adds deterministic metadata only for an explicitly authorized multi-Decision
  accept-or-reject transition.
- [references/read-only.md](scoville-plan/references/read-only.md)
  recovers current state and unresolved proposals without loading write
  contracts.
- [references/native-work-items.md](scoville-plan/references/native-work-items.md)
  owns Work Item refinement, current selection, blockers, progress, and
  `complete_and_advance`.
- [references/native-project-lifecycle.md](scoville-plan/references/native-project-lifecycle.md)
  owns setup, Plan creation, activation, cancellation, and final completion.
- [references/native-editing.md](scoville-plan/references/native-editing.md)
  owns exact-byte guards, native publication limits, recovery stops, and manual
  integrity checks shared by every write route.
- [references/profile-validation.md](scoville-plan/references/profile-validation.md)
  owns optional validator invocation, result interpretation, progressive
  diagnostic routing, proof limits, and manual fallback.

For a read-only direction query, the agent loads only the read-only guide and
then reads the project index, active Plan, current Work Item, referenced
Decisions, and unresolved proposal summaries. Work Item, project-lifecycle,
Decision, batch, and recovery details load only for their matching operations.
An audit adds only the format and decomposition guidance its target needs.

The native profile remains usable without the skill installed. Scoville Plan
owns its `format_version: 1` Plans, Work Items, and Decisions and has no
required executable dependency. When Python is absent, the complete manual
inspection route remains available.

## Sources and inspirations

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable `SKILL.md` package contract and progressive disclosure model.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit goals, constraints, completion evidence, proportionate planning,
  and focused verification.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for keeping durable decisions and their rationale in reviewable project
  records rather than reconstructing them from implementation history.

## Repository contents

The installable `scoville-plan/` directory contains the core skill, nine
conditionally loaded references, one optional standard-library Python
validator, and display metadata. This README, the changelog, the evaluation
cases, and the MIT license remain outside that directory and are not loaded as
skill instructions. The repository contains no network integration, planning
service, mutating command, or generated project state.

## Status

The installable directory passes the canonical Agent Skill validator, and the
repository includes validator contract and invariant suites plus focused static
evaluation cases for ownership, setup, recovery, granularity, Decision
authority, lifecycle, evidence, validation routing, and non-activation
behavior.

The complete-family benchmark passed 5/6 strict quality gates versus 3/6
without Skills, while uncached input rose 124.1% and cached input rose 389.4%.
Skills should therefore be activated by concern rather than as a permanent
bundle.

## License

MIT - see [LICENSE](LICENSE).
