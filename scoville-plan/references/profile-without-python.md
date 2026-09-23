# Inspect a Plan profile without Python

Load this reference only when the bundled validator cannot run because Python
is unavailable. The format stays native Markdown and YAML; do not install a
runtime or create a cache.

Use shell searches, bounded range reads, and byte or hash comparisons to
inspect the complete supported `format_version: 1` profile. Require the
`PROJECT_INDEX.md`, its referenced Plan, every referenced Work Item and
Decision, and all records needed for dependency and lifecycle checks. Follow
the shapes in [native-plan-format.md](native-plan-format.md),
[native-work-items.md](native-work-items.md),
[native-decision-format.md](native-decision-format.md), and
[native-project-lifecycle.md](native-project-lifecycle.md). For a Decision
batch, load [native-decision-batches.md](native-decision-batches.md) and its
no-Python hash route.

Check required fields, unique IDs, record boundaries, allowed statuses,
current-item consistency, direct dependencies, blockers, Decision references,
ordered batch membership, and the exact records affected by a transition.
Expand to full records when a scoped read cannot establish an invariant.
Never treat truncated output as absence or a missing diagnostic as success.
Reread the final unchanged state after edits. Report the inspected paths and
invariants as `native structural inspection`, never as validator output.
If any required record or relation cannot be resolved, report it and leave
structural acceptance open.
