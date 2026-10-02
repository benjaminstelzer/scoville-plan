# Scoville Plan

Scoville Plan keeps goals, decisions and progress in the repository so longer
work survives the next conversation. You can see what is done, what remains
and why a choice was made without reconstructing it from chat history.

Use it for work with dependencies or several sessions. Settle the requirements
and acceptance criteria before implementation, get independent advice where
useful, and revise the Plan when the facts change. A contained fix can stay small.

Scoville measures chili heat. Plan keeps the direction from being diluted by
one more perfectly reasonable detour.

[Plan Viewer](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
shows these records on Windows, macOS and Linux.

## How it works

- Use the repository's existing planning system and relevant Plan, Work Items and Decisions.
- Check current sources before starting the next item.
- Edit Markdown and YAML records with observed Step progress and any additional Instructions.
- Record evidence before completion, preserve accepted history and validate the records.

## What it enforces

- **Resumable work.** Goals, ordered Steps, dependencies and the current position
  stay explicit in the project's records.
- **Decisions with an owner.** Confirmed choices are recorded. Open questions
  remain proposals and block only the work that depends on them.
- **Evidence before completion.** Finished means acceptance was checked.
  Changes of direction preserve completed work and relevant history.

Edit records from one session at a time. Concurrent edits need reconciliation.
See the [full instructions](https://github.com/benjaminstelzer/scoville-plan/blob/main/scoville-plan/SKILL.md).

## What it costs

- Maintaining records takes tokens and time. It pays for continuity on dependent work. A small fix rarely needs a large Plan.

## How it was developed

Real project records shaped the resumable work units and progress checks.
The useful lesson was to keep decisions and accepted results close to the
work they explain, without turning routine updates into more work items.

## Compatibility

Developed for Codex and Claude Code with repository read/write access and a Fable, Astra, SOL or Opus model (5.0+). The optional helpers need Python 3.10+.

## Install

This Skill works independently. Other Scoville Skills are optional.

### Install this Skill

Ask your agent host:

```text
Install this Skill for all my projects from this exact package directory:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
Preserve personal settings and unrelated Skills. Report the installed location
and whether the host discovers the Skill.
```

The host needs permission to write to its Skills directory. The
[Codex Skills guide](https://learn.chatgpt.com/docs/build-skills) and the
[Claude Code Skills guide](https://code.claude.com/docs/en/skills)
list the locations for each host.

### Install the complete Scoville suite

The complete suite is in the
[Scoville Suite monorepo](https://github.com/benjaminstelzer/scoville-suite).
Install its released Skill packages, not development templates.

## How to use

```text
Use Scoville Plan to create an implementation plan for migrating the billing schema, including dependencies and acceptance criteria.
```

```text
Create a detailed repository-owned implementation plan for the billing migration so workers can execute each point without this conversation.
```

State the result you want and the constraints that matter. Plan records the
work, dependencies and acceptance criteria. It does not dispatch agents.

### Progress and decisions

New Plan points use ordered Steps with explicit progress:

```text
1. [status: done] Write the draft.
2. [status: in_progress] Review it against the brief.
3. [status: todo] Deliver the reviewed text.
```

The agent records observed progress, keeps open decisions visible and asks
before dependent work. Older unmarked Steps remain valid, with unknown progress.
Completed Steps still need the Plan point's acceptance checks.

To correct an existing record, ask: "Review and correct PLAN-0001." The agent
checks the evidence and actual result before changing progress. Inspection
without a correction request stays read-only.

### Companion app

[Plan Viewer downloads](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
include a portable EXE and installers for Windows x64, DMGs and zipped apps for
macOS Apple Silicon and Intel, and a portable binary, AppImage, DEB and RPM for
Linux x64.

Open a project containing `PROJECT_INDEX.md`, `docs/plans` and `docs/decisions`.
The read-only Viewer shows current work, Step progress and decisions, refreshing
automatically while active. Removing a project from its list leaves the
repository untouched.

Portable copies keep the project list in `scoville-plan-viewer.xml` beside the
application. An installed copy in a read-only folder uses the platform's user
configuration directory. Keep the Skill and Viewer updated together: older
readers do not understand all current progress fields.

### Model choices for Workflow

When using Scoville Workflow for Codex, you can request a model and reasoning
level for a Step. Otherwise Workflow uses its configured routing. Scoville
Setup shows or saves those settings. Unsupported model/effort combinations
stop the affected operation instead of silently changing your choice.

The [record guide](scoville-plan/references/edit.md) covers Step annotations,
field formats and helper commands. Plan uses `format_version: 1`.

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable package and progressive disclosure.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit outcomes, constraints, planning, and completion evidence.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for durable decisions and rationale in reviewable project files.

## Family

- [Code](https://github.com/benjaminstelzer/scoville-code) covers engineering scope, implementation, risk and validation.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) keeps Plans, Work Items, Decisions and their status in the repository.
- [UI](https://github.com/benjaminstelzer/scoville-ui) covers UI implementation, information structure, accessibility and rendered checks, with an optional WordPress adapter.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) passes active work to another agent or session.
- [Project Context Cleanup](https://github.com/benjaminstelzer/scoville-suite) keeps requested project rules and index text concise without losing required context.

## License

MIT. See [LICENSE](LICENSE).
