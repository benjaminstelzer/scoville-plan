# Scoville Plan

A useful plan lets you pick up the work again without reconstructing the whole
conversation. It says what is active, which decisions apply and what needs to
happen next. If maintaining the plan becomes most of the work, the structure
is getting in the way.

Scoville Plan keeps Plans, Work Items and Decisions in the repository. Use it
when work spans dependent outcomes, needs explicit decisions or must survive
interruption. It preserves the existing planning owner and keeps completion
tied to an observed result, rather than the presence of a file or a checked box.
Small reversible changes usually need no durable Plan.

## Why "Scoville"?

The family is named for useful signal that remains detectable after dilution.
In Plan, that means keeping the direction of the work recoverable across sessions.

## Companion app

The optional Scoville Plan Viewer turns the repository records into a compact,
read-only desktop overview. Point it at a project containing
`PROJECT_INDEX.md`, `docs/plans`, and `docs/decisions` to see the active Plan
point, completed and upcoming work, paused, blocked, or cancelled steps, and
the current and historical Decisions. It rereads visible projects every four
seconds while the window is active, so edits made by an agent or editor appear
without a second tracking system.

[Download the current release](https://github.com/benjaminstelzer/scoville-plan/releases/latest)
for Windows x64, macOS Apple Silicon or Intel, and Linux x64. Windows offers a
portable EXE and installers; macOS offers DMGs and zipped apps; Linux offers a
portable binary, AppImage, DEB, and RPM packages.

The saved project list is one `scoville-plan-viewer.xml` file beside a portable
application. Installed copies in read-only system folders use the platform user
configuration directory for the same XML file. Removing a project from the
Viewer never changes its repository.

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

## Compatibility

Any Agent Skills host with read and write access to the repository's PROJECT_INDEX.md, docs/plans and docs/decisions. Direct Markdown and YAML edits only; requires no CLI, MCP server, database or network. Optional structural validator needs Python 3. Developed for Codex and Claude Code; other hosts untested.

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

## What it enforces

- **One planning owner.** Existing repository instructions and records stay
  authoritative.
- **Compact worker-ready records.** State each necessary fact once, put equal-rank
  facts in bullets, and write required execution order as numbered Steps. Each
  known file appears directly in the Step that changes it. Plan remains usable
  without Scribe.
- **Outcome-sized Work Items.** Separately resumable outcomes become items.
  Implementation steps and checks remain steps or acceptance evidence.
- **Workflow-ready Steps.** When Scoville Workflow is available, optional Steps
  can carry one routing class each. A simple text edit and complex redesign stay
  separate, while code, UI, and browser checks for one result stay together.
- **One active item.** At most one Work Item is `in_progress` and it matches the
  Plan's `current_item`.
- **Durable deferred work.** Mid-task additions leave current work running,
  batch compatible small changes into one queued item, and keep complex or
  independently resumable changes separate. Visible Work Item title prefixes
  preserve deferred anchors and explicit successor priority across sessions.
  A paused item's live Next action preserves an explicitly requested return
  after an immediate redirect. Explicit stops, redirects, and execution-changing
  corrections still take effect immediately. Pure questions that require no
  retained action create no Plan work.
- **Non-recursive Plan maintenance.** Requests to add, remove, reorder, or clean
  up Plan points change the records directly. Only a requested substantive
  outcome becomes a Work Item; maintaining the Plan never becomes one itself.
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

## How it was developed

Plan developed through real project records and the difficulty of picking work
up again. The records need to say what is active, which decisions apply and
what remains to be done. More structure is useful only while it makes those
answers easier to recover.

I compare complete task histories with the records agents read and change.
That shows unnecessary rereading, stale state and planning that consumes time
without moving the work forward. Earlier
[optimization work](https://github.com/benjaminstelzer/scoville-plan/blob/6efa0c0c3ee566a5874206a1709c8079758f6108/CHANGELOG.md)
explored shorter instructions and selective loading. Later changes narrowed
routine reads while retaining checks for changed records and missing
instructions.

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

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for the
  portable package and progressive disclosure.
- [OpenAI coding-agent best practices](https://developers.openai.com/codex/learn/best-practices)
  for explicit outcomes, constraints, planning, and completion evidence.
- [Michael Nygard's architecture decision records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for durable decisions and rationale in reviewable project files.

## License

MIT. See [LICENSE](LICENSE).
