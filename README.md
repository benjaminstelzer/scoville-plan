# Scoville Plan

A plan should make project direction recoverable. Once planning becomes the
project, it has missed its own point.

It usually looks harmless:

- A small reversible change receives a Plan, five Decisions, and fourteen Work
  Items before anyone opens the file that owns it.
- A Work Item becomes `done` because the expected file exists, although nobody
  observed the acceptance result.
- A second tracker appears beside the repository's existing Plan because the
  first source of truth was apparently lonely.
- The next action says "continue the work." The map has reached the useful
  precision of a sign marked "somewhere ahead."

That is planning slop: structure expands while direction becomes harder to
recover. Eventually the map needs its own map.

Scoville Plan is an Agent Skill for repository-owned Plans, Work Items, and
Decision records. It is useful when work spans dependent outcomes, must survive
interruption, or needs explicit lifecycle and completion evidence. It preserves
the repository's existing planning owner and does not create a parallel
journal, database, or hidden state. Small reversible changes normally need no
durable Plan. Not every checkbox needs a permanent address.

A Plan is a map of unfinished outcomes, not a scrapbook that happens to contain
YAML.

## Why "Scoville"?

The family is named for useful signal that survives dilution. In planning, the
heat is the direction another agent can still recover: the active outcome,
authority, blocker, evidence, and next action.

## How to use

Name Scoville Plan when the work needs durable repository state:

```text
Use Scoville Plan to create a repository-owned implementation Plan for migrating the billing schema, updating consumers, and rolling out safely. Preserve any existing planning owner and do not implement the work.
```

```text
Use Scoville Plan to resume the active Plan. Reconcile the current Work Item with observed repository state, update evidence and the next action, then continue only the authorized work.
```

```text
Use Scoville Plan to audit the existing Plan and Decision records for lifecycle, dependency, blocker, and completion-evidence defects. Do not change files.
```

Explicit `$scoville-plan` invocation also works on hosts that support named
Skill invocation.

## Install

Use an Agent Skills-compatible host and Terra 5.6 Medium or a comparably
capable executor such as Opus 4.8. Ask the agent to install:

```text
Install this Agent Skill and refresh the available Skill list:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
Keep the installed directory name scoville-plan. Use Terra 5.6 Medium or a comparably capable executor such as Opus 4.8.
```

The final path must end in `<skills-dir>/scoville-plan/SKILL.md`. For Claude
Code, use `~/.claude/skills/` globally or `.claude/skills/` inside one project.
Other hosts use their supported Skills directory.

**What it costs.** The 1,819-token Core is 17.58% smaller than `v1.2.2`. Format
guidance loads only when needed. The Skill can still use materially more tokens
than no Skill, buying durable direction, explicit Decision authority, and
reliable recovery. Use it for long-lived or interruptible work. Skip it for a
small change with no durable planning need. See
[benchmark evidence](docs/benchmark-evidence.md).
The [family run ledger](docs/optimization-history.md) shows the complete count.

## What it enforces

- **One planning owner.** Existing repository instructions and records stay
  authoritative.
- **Outcome-sized Work Items.** Separately resumable outcomes become items.
  Implementation steps and checks remain steps or acceptance evidence.
- **One active item.** At most one Work Item is `in_progress` and it matches the
  Plan's `current_item`.
- **Evidence before completion.** Files and passing structure checks do not
  substitute for the observed acceptance result.
- **Explicit decisions.** Human choices are recorded without asking twice.
  Inferred choices remain proposed rather than silently accepted.
- **A real next action.** The Plan points to the first unperformed action and
  becomes idle when final work is actually complete.
- **No invented guarantees.** Direct Markdown/YAML edits are validated, but
  never described as transactional or as behavioral proof.

The complete contract is in [SKILL.md](scoville-plan/SKILL.md).

## How it works

The Skill first resolves the existing planning owner and whether durable state
is justified. It then loads only the format and lifecycle guidance required for
the requested operation, edits the native `format_version: 1` Markdown/YAML
records directly, and checks links and invariants. Optional standard-library
Python helpers provide read-only validation. The profile remains usable without
them or without the Skill installed.

## Scoville family

Each Skill works independently. Combine only the concerns the task actually
needs:

- [Brainstorm](https://github.com/benjaminstelzer/scoville-brainstorm) explores
  materially different mechanisms before selection.
- [Code](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop) owns
  engineering scope, implementation, risk, and validation.
- [UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop) owns
  interface hierarchy, framework fit, accessibility, and rendered evidence.
- [Scribe](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop) owns
  wording, terminology, factual meaning, and source fidelity.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) owns durable Plans,
  Work Items, Decisions, and lifecycle state.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) transfers active
  work to another agent or session.

## Status

A reliability-first extension of
[Microsoft SkillOpt](https://github.com/microsoft/SkillOpt) tested the six
Scoville Skills across **1,201 optimization and evaluation runs**. Scoville
Plan passed **30/30 final cases** and its always-loaded instructions use
**17.58% fewer tokens than v1.2.2**. See
[benchmark evidence](docs/benchmark-evidence.md).

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable package and progressive disclosure.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit outcomes, constraints, planning, and completion evidence.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for durable decisions and rationale in reviewable project files.

## License

MIT - see [LICENSE](LICENSE).
