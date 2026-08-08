# Native Decision batches

Load this reference only for one explicitly authorized multi-Decision
accept-or-reject transition in `format_version: 1`.

Every affected Decision stores the same SHA-256 `transition_batch` and ordered
complete `transition_batch_members`. Hash these UTF-8, LF-ended lines in the
authorized request order, substituting each record's exact pre-mutation
SHA-256:

```text
date:YYYY-MM-DD
ADR-0001:accept:<pre-mutation-sha256>
ADR-0002:reject:<pre-mutation-sha256>
```

Member IDs are unique, each member lists itself, and every member carries the
same identifier and exact member order. Preserve this metadata on later
deprecation or supersession. Missing, extra, or asymmetric membership is an
incomplete transition: publish none of the prepared changes and stop further
mutation.
