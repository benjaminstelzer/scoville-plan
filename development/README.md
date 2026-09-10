# Development

The only installable package is [`scoville-plan/`](../scoville-plan/). The profile validator, regression fixtures, and optional desktop viewer are maintained here and are not part of the Skill installation.

## Validate

Run the Python contract suite from the repository root:

```text
python -B -m unittest discover -s development/tests -v
```

For viewer changes, run from `development/viewer`:

```text
npm ci
npm run check
cargo test --manifest-path src-tauri/Cargo.toml
```

These checks cover native profile structure and viewer behavior. They do not prove agent compliance or transactional filesystem writes.

## Retention

Keep current tests, fixtures, viewer source, dependency locks, and this maintenance summary. Create benchmark profiles, token measurements, model outputs, audits, and review packets in temporary storage. Retain evaluation evidence only as a concise repository-owned summary when a published release links it.
