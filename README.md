# Scoville Plan

Work spread across conversations is easy to lose. A task may be marked done
without evidence, a decision may disappear into chat, or the next session may
have to reconstruct the project before making one change.

Scoville Plan keeps direction, Work Items and Decisions in the repository.
It makes the current work and next action recoverable while preserving the
project's existing planning owner. Use it for dependent work and long-running
projects, not to turn a small reversible edit into paperwork.

## How it works

- Resolve the existing planning owner and whether durable records are needed.
- Read the relevant Plan, Work Item and Decisions, then edit Markdown and YAML directly.
- Check the next item against current sources before starting it. Keep one current item and an explicit next action.
- Record evidence before completion and preserve accepted decisions and completed history.
- Validate the planning records and select the context needed for the current task.

## What it enforces

- **One planning owner.** Existing repository instructions and records stay authoritative.
- **Records a worker can use.** Each fact has one owner. Goals describe the current target, Work Items describe resumable outcomes, and numbered Steps name the actual work.
- **Check before starting.** Compare the next item with current sources and relevant completed work. Repair stale assumptions before executing them.
- **One active item.** The Plan names the current work and its first unfinished action.
- **Durable changes of direction.** Queue additions without losing current work. Preserve explicit stops, priorities and requested returns after a redirect.
- **Evidence before completion.** A file and a green structure check do not prove that the requested result works.
- **Explicit decisions.** Record human choices without asking twice. Keep inferred choices proposed until accepted.
- **No planning for the sake of planning.** Editing the Plan changes its records directly. It does not create another Work Item to maintain them.

- When Workflow is active, Steps expose the scope and boundaries needed for dispatch. The coordinator chooses the route. Plan can retain an explicit executor choice, but does not quietly turn a small-looking edit into low-risk work.

- The complete contract, including dispatch projections and direct-edit limits, is in [SKILL.md](https://github.com/benjaminstelzer/scoville-plan/blob/main/scoville-plan/SKILL.md).

Let the current run finish before editing the same records elsewhere. Plan does
not lock files. Concurrent changes require reconciliation.

## What it costs

- Reading, updating and checking Plan records add token usage and maintenance time.

## How it was developed

- Plan developed through real project records and the difficulty of picking work up again.
- The records need to say what is active, which decisions apply and what remains to be done.
- More structure is useful only while it makes those answers easier to recover.
- Real-project histories are analyzed alongside results to identify failures and unnecessary context use.
- Targeted simulation and optimization workflows inform revisions. Changes are retained only when the required behavior survives.

## Compatibility

Requires a frontier LLM from the Fable, Astra, SOL or Opus families, version 5.0
or newer. This requirement is separate from the models actually tested.

Any Agent Skills host with repository read/write access. Direct Markdown/YAML planning needs no service or network. Optional validation and selection helpers require Python 3.10+. Developed for Codex and Claude Code. Other hosts are untested.

This Skill works on its own. Other Scoville Skills are optional and handle
only their own concerns when available and applicable.

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
seconds while the window is active, so edits made by an agent or editor appear
without a second tracking system.

[Download the current release](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
for Windows x64, macOS Apple Silicon or Intel, and Linux x64. Windows offers a
portable EXE and installers. macOS offers DMGs and zipped apps. Linux offers a
portable binary, AppImage, DEB, and RPM packages.

The saved project list is one `scoville-plan-viewer.xml` file beside a portable
application. Installed copies in read-only system folders use the platform user
configuration directory for the same XML file. Removing a project from the
Viewer never changes its repository.

### Record compatibility

Existing format-version-1 Plans need no migration. Updated readers also accept
consistent CRLF and plain text such as `Evidence: Tests A, B passed.` No quoting
or escaping is needed. Existing bracketed lists keep their meaning. Update the
Skill and Viewer before using the new forms. Older readers may reject them.
Keep legacy Evidence lists and LF when working with older readers.

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
