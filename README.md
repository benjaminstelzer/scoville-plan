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

## Why "Scoville"?

The family is named for useful signal that remains detectable after dilution. In planning, the
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

### Install this Skill

In a local Codex or Claude Code session, ask:

```text
Install this Agent Skill for all my projects from this exact package directory:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
Preserve existing customizations and ask before overwriting conflicting files.
Report the installed location and whether the host discovers the Skill.
```

The agent needs source access and permission to write to its personal Skills
location. Manual fallback: [Codex Skills guide](https://learn.chatgpt.com/docs/build-skills)
or [Claude Code Skills guide](https://code.claude.com/docs/en/skills).

Install only the linked package for the focused option.

### Install the complete Scoville suite

```text
Install the complete Scoville Skill suite for all my projects. Fetch and install every exact package directory below:

https://github.com/benjaminstelzer/scoville-brainstorm/tree/main/scoville-brainstorm
https://github.com/benjaminstelzer/scoville-research/tree/main/scoville-research
https://github.com/benjaminstelzer/scoville-code-anti-ai-slop/tree/main/scoville-code-anti-ai-slop
https://github.com/benjaminstelzer/scoville-design-anti-ai-slop/tree/main/scoville-design-anti-ai-slop
https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop/tree/main/scoville-ui-anti-ai-slop
https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop/tree/main/scoville-scribe-anti-ai-slop
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
https://github.com/benjaminstelzer/scoville-handoff/tree/main/scoville-handoff

Preserve existing customizations and ask before overwriting conflicting files. Report every installed location and whether the host discovers each Skill.
```

### Download the Plan Viewer

The desktop viewer reads existing Scoville Plan projects without changing them.
Download the file that matches your system from the
[current release](https://github.com/benjaminstelzer/scoville-plan/releases/latest):

- Windows x64: portable EXE, MSI, or setup EXE.
- macOS Apple Silicon and Intel: DMG or zipped app.
- Linux x64: portable binary, AppImage, DEB, or RPM.

The project list stays portable in `scoville-plan-viewer.xml` beside the
application. macOS stores it beside the app bundle. AppImage builds store it
beside the AppImage file.

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

Routine updates read the relevant complete blocks without printing unrelated
history. Full-file change detection and complete structural checks remain in
place. Completed records stay in their original Plans, available when needed.

For repository structure and development tools, see
[maintenance notes](development/docs/maintenance.md).

## Scoville family

Each Skill works independently. Combine only the concerns the task actually
needs:

- [Brainstorm](https://github.com/benjaminstelzer/scoville-brainstorm) explores
  materially different mechanisms before selection.
- [Research](https://github.com/benjaminstelzer/scoville-research) turns web,
  GitHub, and scholarly evidence into a decision-ready, claim-traceable result.
- [Code](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop) owns
  engineering scope, implementation, risk, and validation.
- [Design](https://github.com/benjaminstelzer/scoville-design-anti-ai-slop) owns
  visual definition, art direction, design systems, critique, and repair.
- [UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop) owns
  framework-aligned implementation, interface mechanics, accessibility, and
  rendered evidence, with a standalone design fallback.
- [Scribe](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop) owns
  wording, terminology, factual meaning, and source fidelity.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) owns durable Plans,
  Work Items, Decisions, and lifecycle state.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) transfers active
  work to another agent or session.

## Status

The historical package qualified on 2026-08-10 passed 30/30 final cases.
Its exact Core and package hashes are retained in
[benchmark evidence](development/docs/benchmark-evidence.md).

The current source has changed since that qualification. Historical scores and
token reductions do not qualify it. Read-only helper tests establish the
contracts they exercised, not general agent behavior or transactional writes.

The [selective-read comparison](development/docs/benchmarks/plan-hygiene.md) covers synthetic
profiles and deterministic checks. It measures returned text for scripted
operations, not provider tokens, cost savings, or actual agent compliance.

Repository development and the current path mapping are in [development/](development/README.md).

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable package and progressive disclosure.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit outcomes, constraints, planning, and completion evidence.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for durable decisions and rationale in reviewable project files.

## License

MIT. See [LICENSE](LICENSE).
