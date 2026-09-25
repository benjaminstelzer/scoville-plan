# Inspect a profile without Python

General only: load this only when Python is unavailable. Never use it to
bypass a missing or failing helper when Python is present. Require the complete
supported profile and inspect all canonical records and relations after edits.
Use full records when bounded reads cannot establish an invariant. Truncated
output proves no absence. This is manual structural inspection, not validator
output or semantic acceptance. Leave acceptance open if a relation is unresolved.

## Files and identity

Write UTF-8 without BOM and LF. Readers also accept consistent CRLF, but not
mixed endings, bare CR, NUL or invalid UTF-8. Reject redirected paths and
cross-project escapes. Use one record per Markdown file and forward-slash paths.
IDs are case-sensitive: PLAN-0001, W-001 and ADR-0001 use exactly four, three and
four digits respectively. File subjects are lowercase ASCII kebab-case after
the four-digit Plan/Decision number. IDs must be unique in their namespace;
Work Item IDs are scoped to a Plan. Allocate highest plus one, never overwrite
or reuse interior gaps; maximum PLAN/ADR-9999 and W-999 exhaust the namespace.
Dates are valid ISO YYYY-MM-DD and updated/accepted cannot precede created.

## Index and Plan shape

PROJECT_INDEX.md frontmatter has only these ordered keys: format_version: 1,
active_plan: PLAN-NNNN or null. Optional body duplicates no mutable routing facts.
A non-null reference resolves to exactly one active Plan. Null requires none.

Plan frontmatter order is format_version, id, status, created, updated, then
current_item only when active. Required values are format_version: 1 and status
one of draft, active, completed, cancelled. Exactly one H1 precedes the H2s Goal,
Non-goals, Work items in that order; all are explicit and nonempty. A Plan has
at least one Work Item. Active current_item resolves to todo/in_progress/paused.
At most one item is in_progress and it equals current_item; nonactive Plans have
none. Completed Plans contain only done/cancelled items. Lifecycle exceptions
for a wholly unstarted Plan are in native-project-lifecycle.md.

## Work Item shape

Each H3 is `### W-001 Nonempty title` and starts one contiguous block. Exactly
these fields occur in order: Status, Depends on, Blocked by, Decisions, Outcome,
Acceptance, optional Steps, Evidence, Next action when nonterminal. Unknown,
repeated or missing fields are invalid. Each value occupies one physical line.
Status is todo/in_progress/paused/done/cancelled. Outcome and Acceptance are
nonempty. Steps are consecutive nonempty `1.`, `2.` lines without blank lines.
Steps have no IDs, statuses, dependencies, blockers, evidence or checkboxes.

Depends on and Decisions use `[]` or `[ID, ID]`, with unique correctly typed IDs.
Dependencies resolve to earlier items in the same Plan and form no cycles.
Cancelled dependencies satisfy no work. A current item's dependencies are done.
Decision references must resolve. Blocked by uses the same list syntax and
unique labels matching `[A-Z][A-Z0-9]{1,15}-[A-Z0-9][A-Z0-9._-]{0,47}`;
ADR, PLAN and W are reserved prefixes.

Done/cancelled work has nonempty Evidence, no blockers and no Next action.
Todo/in_progress/paused has nonempty Next action; Evidence may be empty.
Evidence is `[]`, a compatible list of unique entries or (for updated readers)
one-line plain text unless its value begins `[`. Each entry is 1–200 Unicode
scalar values without edge whitespace or ASCII controls. List entries contain
no comma or brackets because commas delimit entries. Plain text permits them;
quotes and backslashes remain literal. New writes follow edit.md compatibility.

Step annotations precede the action. Preserve an existing or explicitly
supplied `[route: CLASS]` with CLASS ultra_low/low/medium/high/ultra_high.
Plan defines no criteria for choosing one. The optional execution annotation
is `[execute: model=MODEL_ID; reasoning=LEVEL]`; either property can be omitted,
model first when both exist. MODEL_ID uses lowercase ASCII letters, digits,
dots and hyphens and begins/ends alphanumeric. LEVEL is none/minimal/low/medium/
high/xhigh/max/ultra. Route precedes execute; route never contains a model name.

Check historical Deferred/Prioritized anchors and explicit paused returns
through native-project-lifecycle.md. Those semantic order checks are not implied
by a valid parser result. Authored-history permissions are in edit.md.

## Decision shape and graph

Frontmatter keys in order: format_version, id, status, created, optional accepted,
scope, optional supersedes, superseded_by, transition_batch,
transition_batch_members. Unknown or repeated keys are invalid. Version is 1.
Scope consists of nonempty slash-separated `[a-z0-9][a-z0-9-]*` segments.
Status is proposed/accepted/rejected/deprecated/superseded. Accepted, deprecated
and superseded require accepted; proposed and rejected forbid it. New proposals
have no supersession or batch metadata. One H1 precedes exactly the nonempty H2s
Decision, Problem, Drivers, Considered alternatives, Consequences, Confirmation,
Revisit when, in that order.

Supersession references resolve to other Decisions, are reciprocal and acyclic.
A superseded record names its replacement; other statuses do not use
superseded_by. A replacement is accepted/deprecated/superseded and names the old
record in supersedes. Keep acceptance dates and immutable authored rationale.
A valid graph does not authorize a transition; use native-decision-format.md.

Historical batch fields appear as a pair. The ID is 64 hex digits or
`batch-YYYYMMDD-N` with valid date and positive integer N. Membership uses a
nonempty unique ADR list, resolves completely and includes the record itself.
Every member shares the same ID and identical ordered complete member list.
Reject absent members, malformed IDs and asymmetric metadata. Preserve existing
metadata, never generate new batches, and never claim to recompute an old hash.

After writes inspect the final unchanged profile. Report checked paths and
invariants as native structural inspection. Separately assess authority,
history, record meaning and evidence sufficiency under SKILL.md and edit.md.
