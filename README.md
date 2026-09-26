# Scoville Plan

Work spread across conversations needs a durable record of the goal, decisions
and next action. Scoville Plan keeps those facts in the repository, with Work
Items that describe resumable outcomes and evidence required for completion.

Use it for dependent work and long-running projects. It follows the project's
existing planning system and keeps small tasks proportionate.

The name comes from the Scoville scale, which originally measured chili heat through dilution.
Here, the heat is the direction another agent can recover: the goal, decisions, current state and next action.

## How it works

- Use the repository's existing planning system and relevant Plan, Work Items and Decisions.
- Check current sources before starting the next item.
- Edit Markdown and YAML records with an explicit next action.
- Record evidence before completion, preserve accepted history and validate the records.

## What it enforces

- **Existing project records.** Follow the repository's planning rules and update its established records.
- **Clear work units.** Goals name the target, Work Items define resumable outcomes, and ordered Steps describe the work.
- **Current assumptions.** Check the next item against sources and completed work before execution.
- **One active item.** Record current work and its first unfinished action.
- **Changes of direction.** Record new priorities, pauses and work the user wants to return to.
- **Evidence before completion.** Record observed results that establish acceptance.
- **Explicit decisions.** Record the user's decisions. Keep unconfirmed choices marked as proposals.
- **Direct maintenance.** Update Plan records without creating extra work items for routine edits.

Edit the records from one session at a time. Concurrent changes must be reconciled.

See [SKILL.md](https://github.com/benjaminstelzer/scoville-plan/blob/main/scoville-plan/SKILL.md) for the full instructions and editing limits.

## What it costs

- Reading, updating and checking Plan records add token usage and maintenance time.

## How it was developed

- Real project records exposed the information needed to resume: active work, applicable decisions and remaining actions.
- Project histories and targeted simulations informed the record format and validation checks.

## Compatibility

A current Fable, Astra, SOL or Opus model is recommended. Luna was also used
in testing.

Any Agent Skills host with repository read/write access. Direct Markdown/YAML planning needs no service or network. Optional validation and selection helpers require Python 3.10+. Developed for Codex and Claude Code. Other hosts are untested.

This Skill works independently. Other Scoville Skills are optional.

## Install

### Install this Skill

This standalone package works independently. Ask your compatible agent host:

```text
Install this Skill for all my projects from this exact package directory:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
Preserve personal settings and unrelated Skills. Report the installed location
and whether the host discovers the Skill.
```

The host needs permission to write to its Skills directory. See the
[Codex Skills guide](https://learn.chatgpt.com/docs/build-skills) or the
[Claude Code Skills guide](https://code.claude.com/docs/en/skills)
for host-specific locations.

### Install the complete Scoville suite

Get the complete suite from the
[Scoville Suite monorepo](https://github.com/benjaminstelzer/scoville-suite).
Install its released Skill packages, not development templates.

## How to use

```text
Use Scoville Plan to create an implementation plan for migrating the billing schema, including dependencies and acceptance criteria.
```

```text
Create a detailed repository-owned implementation plan for the billing migration so workers can execute each point without this conversation.
```

State the outcome, acceptance criteria and next action directly in the Plan.

### Set reasoning for a Step

Plan does not choose a model or reasoning level on its own. When using Scoville
Workflow for Codex from the Codex suite, you can retain an explicit model or
reasoning choice on a Step. Plan itself does not dispatch work. Without an
explicit choice, Workflow assesses the Step and uses the configured pair for
its route. Scoville Setup displays or saves those project settings.

You can request a reasoning level for one Step:

```text
1. [execute: reasoning=high] Check the migration and its rollback behavior.
```

To specify the model as well, put it first:

```text
1. [execute: model=gpt-6-astra; reasoning=high] Check the migration and its rollback behavior.
```

The regular levels are `low`, `medium`, `high` and `xhigh`. Setup offers and
saves these four. The format also supports `none`, `minimal`, `max` and `ultra`
for explicit annotations or manual entries in `.scoville/config.json`. Setup
preserves those manual entries when you change other settings. Every selected
pair must be supported by the actual model. An unsupported pair stops with an
explanation, without silently choosing another level.

Route classes such as `ultra_low` describe task complexity. They are separate
from reasoning levels: an `ultra_low` task can use reasoning `low`.

### Companion app

The optional Scoville Plan Viewer turns the repository records into a compact,
read-only desktop overview. Point it at a project containing
`PROJECT_INDEX.md`, `docs/plans`, and `docs/decisions` to see the active Plan
point, completed and upcoming work, paused, blocked, or cancelled steps, and
the current and historical Decisions. It rereads visible projects every four
seconds while the window is active, so changes made by an agent or editor appear automatically.

[Download the current release](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
for Windows x64, macOS Apple Silicon or Intel, and Linux x64. Windows offers a
portable EXE and installers. macOS offers DMGs and zipped apps. Linux offers a
portable binary, AppImage, DEB, and RPM packages.

The saved project list is one `scoville-plan-viewer.xml` file beside a portable
application. Installed copies in read-only system folders use the platform user
configuration directory for the same XML file. Removing a project from the
Viewer never changes its repository.

### Record compatibility

Plan uses `format_version: 1`. Evidence accepts plain text such as
`Evidence: Tests A, B passed.` and bracketed lists. Files support LF or
consistent CRLF line endings. Use matching current Skill and Viewer versions.
Older readers require bracketed Evidence lists and LF.

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable package and progressive disclosure.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit outcomes, constraints, planning, and completion evidence.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for durable decisions and rationale in reviewable project files.

## Family

- [Code](https://github.com/benjaminstelzer/scoville-code) owns engineering scope, implementation, risk, and validation.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) owns durable Plans, Work Items, Decisions, and lifecycle state.
- [UI](https://github.com/benjaminstelzer/scoville-ui) owns UI implementation, information structure, accessibility and rendered evidence, with a conditional WordPress adapter.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) transfers active work to another agent or session.

## License

MIT. See [LICENSE](LICENSE).
