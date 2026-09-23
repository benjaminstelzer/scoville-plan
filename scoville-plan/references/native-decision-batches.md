# Native Decision batches

Load this reference only for one explicitly authorized multi-Decision
accept-or-reject transition in `format_version: 1`.

Every affected Decision stores the same SHA-256 `transition_batch` and ordered
complete `transition_batch_members`. Prefer the bundled read-only helper when
its script and Python 3 are available. After reading every member's stable
pre-mutation state, invoke it exactly once for that batch attempt:

```text
python "<skill-directory>/scripts/compute_decision_batch.py" --root "<project-root>" --date YYYY-MM-DD --transition "ADR-0001:accept:docs/decisions/0001-example.md" --transition "ADR-0002:reject:docs/decisions/0002-example.md" --format json
```

Pass transitions in authorized request order. Require output containing exactly
`sha256`, ordered `members`, and `member_file_sha256`. Check that `members` and
the hash-map IDs exactly match the requested transitions, then copy `sha256` and
the same member order into every affected Decision. Never invent or mentally
compute a hash. A helper error stops the batch; do not bypass its path, file, or
input checks.

The helper hashes each file's exact pre-mutation bytes and then hashes these
UTF-8, LF-ended lines:

```text
date:YYYY-MM-DD
ADR-0001:accept:<pre-mutation-sha256>
ADR-0002:reject:<pre-mutation-sha256>
```

If Python 3 is unavailable, load
[decision-batch-without-python.md](decision-batch-without-python.md) for the
byte-exact alternative. If Python is available but the helper fails, stop the
batch and report its diagnostic.

Member IDs are unique, each member lists itself, and every member carries the
same identifier and exact member order. Preserve this metadata on later
deprecation or supersession. Missing, extra, or asymmetric membership is an
incomplete transition: publish none of the prepared changes and stop further
mutation.
