# Native Plan format

This Skill writes the Plan and Work Item part of the Scoville Plan native profile
`format_version: 1` directly. Load [native-decision-format.md](native-decision-format.md)
only when the operation creates, changes, transitions, or audits a Decision.

## Contents

- Files and encoding
- IDs and filenames
- Project index
- Plan profile
- Work Item block
- State invariants

## Files and encoding

- Use UTF-8 without a byte-order mark and LF line endings.
- `PROJECT_INDEX.md` owns the format version and active Plan routing.
- `docs/plans/` contains one Plan per Markdown file.
- `docs/decisions/` contains one Decision per Markdown file.
- Generated files, caches, runtime plans, and UI state own no project facts.

## IDs and filenames

Plan IDs match `PLAN-[0-9]{4}`. Work Item IDs match `W-[0-9]{3}` and are unique
inside their Plan. Plan filenames use the numeric ID followed by a lowercase
ASCII kebab-case subject, for example:

```text
docs/plans/0007-ship-local-app.md
```

Allocate the next Plan ID as the highest valid Plan ID plus one. Allocate a new
Work Item ID as the highest ID in its Plan plus one. Recheck filename and
internal ID immediately before creation. Never reuse an interior gap, overwrite
a collision, or renumber an existing Work Item. A deleted highest provisional
ID may be reused; reaching `PLAN-9999` or `W-999` exhausts that ID space.

## Project index

Use exactly these frontmatter keys in this order:

```yaml
---
format_version: 1
active_plan: PLAN-0001
---
```

`active_plan` is one Plan ID or literal `null`. A referenced Plan must be
`active`, and exactly one Plan may be active. `null` requires zero active Plans.
The optional body may explain reading order but must not duplicate status,
current work, blockers, or Decision lists.

## Plan profile

Use these frontmatter keys and order:

```yaml
---
format_version: 1
id: PLAN-0001
status: active
created: 2026-08-07
updated: 2026-08-07
current_item: W-001
---
```

`format_version`, `id`, `status`, `created`, and `updated` are required.
`current_item` is required only for `active`. It names one `todo`,
`in_progress`, or `paused` Work Item in the same Plan.

Plan status is `draft`, `active`, `completed`, or `cancelled`. After the
frontmatter, write one H1 title followed by these H2 sections in order:

```text
Goal
Non-goals
Work items
```

Goal and Non-goals must be explicit and non-empty.
State the target result in Goal and only actual scope exclusions in Non-goals.
Use one sentence for one concept and compact bullets for several equal-rank
facts. Keep implementation order and rationale in their owning fields or
Decisions.

## Work Item block

Each Work Item is one contiguous H3 block. Use exactly this field order and one
physical line per value:

```text
### W-001 Describe the observable outcome

Status: todo
Depends on: []
Blocked by: []
Decisions: []
Outcome: One independently resumable observable result.
Acceptance: A command or direct observation that proves the result.
Steps:
1. Inspect the current behavior.
2. Apply the bounded change.
Evidence: []
Next action: The first concrete action that has not happened yet.
```

Allowed keys are `Status`, `Depends on`, `Blocked by`, `Decisions`, `Outcome`,
`Acceptance`, optional `Steps`, `Evidence`, and `Next action`. Unknown or
repeated keys are invalid. Inline lists use only `[]` or `[ID, ID]`.

When present, Steps contain consecutive numbered, non-empty, single-line prose
starting at `1.` with no blank lines inside the block. Steps express order only;
they have no IDs, status, dependencies, blockers, evidence, checkboxes, or
completion semantics. `Next action` is the sole current move.

Use Steps whenever execution requires two or more ordered actions. Write them in
the exact order a worker should perform them. Each Step starts with a concrete
verb and names its target. Cite every known repository-relative file in the Step
that changes or checks it, for example:

```text
Steps:
1. Update `src/cache/migrate.py` to stage schema-2 output before publication.
2. Update `src/cache/reader.py` to call the staged migration after validation.
3. Add interruption coverage in `tests/test_cache_migration.py`.
```

Do not write vague Steps such as "make the changes" or "update the relevant
files." Resolve an unknown canonical target through bounded read-only discovery
before starting when practical, then add the observed path while the item is
still `todo`. If discovery must occur after start, keep a criterion-based Step
and use the live-state procedure in native-work-items.md. Do not invent a path.
Use unordered bullets only for equal-rank Goal or Non-goal facts, never for a
required execution sequence.

When a Plan is being shaped for later Scoville Workflow use, each Step may act
as one subplan dispatch point. Keep materially different routing needs in
separate Steps and optionally start the prose with one
`[route: ultra_low|low|medium|high|ultra_high]` prefix. This annotation remains
ordinary Step prose: it adds no field, lifecycle, or structural guarantee. Do
not store a model or reasoning level; the live Workflow configuration owns that
mapping. Without Steps, the Work Item is one dispatch unit.

Keep Outcome to the observable result, Acceptance to the checks and expected
results that establish it, and Next action to the first unperformed action.
Prefer a short direct sentence where sufficient. One physical line may contain
several sentences when necessary criteria would otherwise be lost. Steps add
subordinate order, not another description of the outcome. Evidence records the
observed result and a precise reference when needed, not an execution diary.
The concept and sequence together must let a lower-reasoning worker execute and
a reviewer trace every Step to the result and Acceptance without chat context.

## State invariants

- Work Item status is `todo`, `in_progress`, `paused`, `done`, or `cancelled`.
- Dependencies reference earlier Work Items in the same Plan and form no cycle.
- Decision references name existing Decision records. Use `[]` when none exist.
- An active Plan has at most one `in_progress` item. If present, it equals
  `current_item`; otherwise `current_item` names a `todo` or `paused` item.
- A draft or cancelled Plan contains no `in_progress` item.
- A completed Plan contains only `done` or `cancelled` items.
- `done` or `cancelled` requires non-empty Evidence, empty Blocked by, and no
  `Next action` line.
- `todo`, `in_progress`, or `paused` requires a non-empty `Next action` line;
  Evidence may be empty.

External blocker labels are unique within one Work Item and match
`[A-Z][A-Z0-9]{1,15}-[A-Z0-9][A-Z0-9._-]{0,47}`. `ADR`, `PLAN`, and `W` are
reserved prefixes.

Evidence entries are unique, case-sensitive strings of at most 200 Unicode
scalar values, without leading or trailing whitespace, comma, square bracket,
line break, or ASCII control character. Shape does not prove sufficiency.

Dates use ISO `YYYY-MM-DD`. `updated` must not precede `created`. IDs are
case-sensitive. Canonical paths use forward slashes relative to the project
root. Required text remains explicit; never infer status, completion,
authorization, evidence, or relationships from prose, source files, or Git.
