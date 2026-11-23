# Scoville Plan

Scoville Plan keeps goals, decisions and progress in the repository so longer
work survives the next conversation. You can see what is done, what remains
and why a choice was made without reconstructing it from chat history.

Use it for work with dependencies or several sessions. Settle the requirements
and acceptance criteria before implementation, get independent advice where
useful, and revise the Plan when the facts change. A contained fix can stay small.

Scoville measures chili heat. Plan keeps the direction from being diluted by
one more perfectly reasonable detour.

[Plan Viewer](https://github.com/benjaminstelzer/scoville-plan-viewer/releases/latest)
shows these records on Windows, macOS and Linux.

## How it works

- Plan keeps a Plan, its Work Items and your Decisions as Markdown files in
  the repository: `PROJECT_INDEX.md`, `docs/plans` and `docs/decisions`. A
  Work Item has ordered Steps with a status, dependencies and acceptance
  criteria.
- Before the next item starts, the agent checks the current sources and not
  only the record.
- Progress is recorded as it is observed. Finished means the acceptance was
  checked.
- Confirmed choices become Decisions. Open questions stay proposals and block
  only the work that depends on them.
- A bundled validator checks structure and references. It can't tell whether
  an acceptance result is true.
- Edit Plan records from one session at a time.

## What it costs

Maintaining the records takes tokens and time.

## How to use

```text
Use Scoville Plan to create an implementation plan for migrating the billing schema, including dependencies and acceptance criteria.
```

```text
Plan the billing migration in the repository so another session can carry out each step without this conversation.
```

State the result you want and the constraints that matter. Plan asks only when
an unknown would materially change the solution. It writes the records and
doesn't start agents to do the work. New Plans use the language of your task.

To correct a record, ask "Review and correct PLAN-0001". Without such a
request, inspection stays read-only. On an explicit cleanup request Plan
shortens old Plans and Decisions and, if you ask for removal, deletes expired
or superseded Decisions. Deleting a file needs its contents committed or your
approval.

The [authoring guide](scoville-plan/references/authoring.md) has the templates
if you write Plans by hand.

## Install

Works in Codex and Claude Code. It needs read and write access to the repository
and Python 3.11+ for its bundled helpers.

Use `gpt-6.2-sol` or Claude Opus 5.5 at medium reasoning effort or higher. Below
that, steps get skipped more often.

Ask your agent host:

```text
Install this Skill for all my projects from this exact package directory:
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
Preserve personal settings and unrelated Skills. Report the installed location
and whether the host discovers the Skill.
```

The host needs write access to its Skills directory. The
[Codex](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code](https://code.claude.com/docs/en/skills) Skills guides say where
that is. This Skill works on its own. The other Scoville Skills are in the
[Scoville Suite](https://github.com/benjaminstelzer/scoville-suite).

## Background

Long-running projects shaped Plan. As the records grew, keeping every old note
became a problem of its own, so maintenance became part of the design: keep
current decisions and accepted results without turning routine updates into
more work.

The [full instructions](https://github.com/benjaminstelzer/scoville-plan/blob/main/scoville-plan/SKILL.md) are what the agent reads.
Sources: the [Agent Skills specification](https://agentskills.io/specification),
[OpenAI's coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
and [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## License

MIT. See [LICENSE](LICENSE).
