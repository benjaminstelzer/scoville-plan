# Scoville Plan

Before an agent starts implementing, it should be clear what it is supposed to
achieve and how the result will be checked. A Plan makes the goal, dependencies
and acceptance criteria explicit. That matters in AI-assisted software
engineering, especially when the work spans several conversations.

Scoville Plan keeps those facts in the repository: Work Items, relevant
Decisions, accepted results and the next action. The next agent can pick up the
work from there. You can see what is finished, why a choice was made and what
still needs checking, without piecing it together from an entire chat.

Substantial work deserves a Plan that got real attention before anything is
executed. Clarify requirements, check dependencies and get independent
feedback, for example through Scoville Ask, then revise the Plan until the
important questions are settled. Complex work can take several rounds of
review and changes before Scoville Workflow starts implementing it. That
coordination overhead is worth it when the size and dependencies justify it.
Good planning is a large part of software engineering. AI helps with it, but
goals, architecture and tradeoffs still need informed judgment.

If implementation shows that an assumption was wrong, update the Plan. Its
job is to keep the direction while the work changes. Use it for dependent
work and long-term maintenance, inside whatever planning system the project
already has. And keep small tasks small: a large Plan for a contained fix
just adds work.

The heat, in this case, is the direction another agent can pick up again: the
goal, the decisions, the current state and the next action.

## How it works

- Use the repository's existing planning system and relevant Plan, Work Items and Decisions.
- Check current sources before starting the next item.
- Edit Markdown and YAML records with an explicit next action.
- Record evidence before completion, preserve accepted history and validate the records.

## What it enforces

- **Existing project records.** Plan follows the repository's planning rules
  and updates its established records.
- **Clear work units.** Goals name the target, Work Items describe outcomes
  that can be resumed, and ordered Steps describe the work.
- **Current assumptions.** Before the next item is executed, it's checked
  against the sources and the work already done.
- **One active item.** Only one item is active at a time, with its first
  unfinished action recorded.
- **Changes of direction.** New priorities, pauses and work you want to come
  back to get recorded.
- **Evidence before completion.** Nothing is marked complete without the
  observed results that show it meets acceptance.
- **Explicit decisions.** Your decisions get recorded. Choices you haven't
  confirmed stay marked as proposals.
- **Direct maintenance.** Routine edits update the Plan directly instead of
  creating extra Work Items.

Edit the records from one session at a time. If two sessions change them in
parallel, the changes have to be reconciled.

See [SKILL.md](https://github.com/benjaminstelzer/scoville-plan/blob/main/scoville-plan/SKILL.md) for the full instructions and editing limits.

## What it costs

- Reading, updating and checking Plan records add token usage and maintenance time.

## How it was developed

- Real project records showed what you need to resume work: the active item,
  the decisions that apply and what's left to do.
- Project histories and targeted simulations shaped the record format and the
  validation checks.

## Compatibility

Needs a frontier model from the Fable, Astra, SOL or Opus families, version
5.0 or newer. Luna was also used in testing.

Any Agent Skills host with read and write access to the repository will do.
Planning in plain Markdown and YAML needs no service and no network. The
optional validation and selection helpers need Python 3.10+. Developed for
Codex and Claude Code. Other hosts haven't been tested.



It works on its own. The other Scoville Skills are optional.

This Skill works independently. Other Scoville Skills are optional.

## Install

### Install this Skill

This package works on its own. Ask your agent host:

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

State the outcome, acceptance criteria and next action directly in the Plan.

### Set reasoning for a Step

Plan doesn't pick a model or reasoning level by itself, and it doesn't
dispatch work either. If you use Scoville Workflow for Codex from the Codex
suite, you can attach an explicit model or reasoning choice to a Step.
Without one, Workflow assesses the Step and uses the pair configured for its
route. Scoville Setup shows or saves those project settings.

You can request a reasoning level for one Step:

```text
1. [execute: reasoning=high] Check the migration and its rollback behavior.
```

To specify the model as well, put it first:

```text
1. [execute: model=gpt-6-astra; reasoning=high] Check the migration and its rollback behavior.
```

The regular levels are `low`, `medium`, `high` and `xhigh`, and those are the
four Setup offers and saves. The format also accepts `none`, `minimal`, `max`
and `ultra`, either as explicit annotations or as manual entries in
`.scoville/config.json`. Setup leaves such manual entries alone when you
change other settings. Whatever pair you choose, the model has to support it.
If it doesn't, the run stops and explains why instead of quietly picking
another level.

Route classes such as `ultra_low` describe how complex a task is. They're
separate from reasoning levels: an `ultra_low` task can use reasoning `low`.

### Companion app

The optional Scoville Plan Viewer shows the repository records as a compact,
read-only desktop overview. Point it at a project with `PROJECT_INDEX.md`,
`docs/plans` and `docs/decisions`, and you'll see the active Plan point,
finished and upcoming work, paused, blocked or cancelled steps, and current
and past Decisions. While the window is active, it rereads visible projects
every four seconds, so changes from an agent or an editor show up on their
own.

[Download the current release](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
for Windows x64, macOS Apple Silicon or Intel, and Linux x64. For Windows
there's a portable EXE and installers, for macOS DMGs and zipped apps, and for
Linux a portable binary, an AppImage and DEB and RPM packages.

The portable version saves its project list in a `scoville-plan-viewer.xml`
next to the application. Installed copies in read-only system folders keep
the same XML file in the platform's user configuration directory. Removing a
project from the Viewer never touches its repository.

### Record compatibility

Plan uses `format_version: 1`. Evidence can be plain text such as
`Evidence: Tests A, B passed.` or a bracketed list. Files can use LF or
consistent CRLF line endings. Keep the Skill and the Viewer on matching
current versions, because older readers need bracketed Evidence lists and LF.

The name comes from the Scoville scale, which originally measured chili heat through dilution.

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

## License

MIT. See [LICENSE](LICENSE).
