# Changelog

## 2026-08-09: README scope

### Changed

- Kept the README focused on installation, composition, design, and usage by
  removing embedded benchmark results and cost tables. The complete benchmark
  artifacts remain available under `docs/benchmarks`.

## 2026-08-08: Complete-suite cost evidence

### Added

- Added a controlled Sol Medium and Terra Medium no-Skill versus four-Skill
  benchmark with three runs per condition and model.
- Added per-run and aggregate provider-token usage, quality-qualified success
  rates, exact source hashes, and a machine-readable result summary.

### Findings

- The complete suite improved the strict integrated success rate from 3/6 to
  5/6 and produced validator-clean canonical profiles in 6/6 family runs.
- Across both models, family runs consumed 4,165,413 provider tokens versus
  987,905 native tokens; uncached input rose 124.1% and cached input rose
  389.4%.
- The result supports independent routing and does not justify loading the
  complete family for tasks that do not need all four Skills.
- A second Plan-loading candidate reduced family Skill payload from 23,201 to
  21,386.5 median tokens and repeated payload from 1,812 to 605.5. Its frozen
  adoption gate still rejected the series because one scheduled family-baseline
  run had no provider usage; the released Skill remains unchanged.
- A transport probe observed duplicate structured result fields. Provider-side
  double counting remains unknown; the candidate benchmark used unstructured
  Skill results and reports direct cached, uncached, output, and total usage
  separately from literal Skill payload.

## 2026-08-08: Read-only native profile validator

### Added

- Added an optional standard-library Python validator for complete native
  `format_version: 1` profiles with deterministic JSON diagnostics and text
  output.
- Added no-follow path inspection, consistent-read detection, local record
  parsing, cross-record graph checks, Decision lifecycle and batch validation,
  and stable exit semantics for valid, invalid, incomplete, and internal-error
  results.
- Added a focused validation guide that tells agents when to run the tool, how
  to interpret diagnostics, when human direction is required, and how to fall
  back to manual inspection without Python.

### Changed

- Full-profile diagnosis now loads the validation guide first and routes to
  only the native reference needed for a reported defect instead of preloading
  every format and lifecycle guide.
- Native post-write verification now uses the bundled validator when already
  available while retaining complete Skill-only operation without it.

### Validation

- Added immutable fixtures, recursive pre/post byte and path snapshots, a
  machine-readable result contract, and a complete cross-record invariant map.
- The local validator suite currently passes 36 tests, including valid terminal
  profiles, incomplete reads, redirected paths, concurrent changes,
  deterministic multi-defect output, and adversarial write-option rejection.

## 2026-08-08: Native Decisions and complete lifecycle

### Changed

- Added native `format_version: 1` Decision records and lifecycle guidance to
  Scoville Plan without adding a CLI dependency.
- Expanded Scoville Plan to its complete native feature surface:
  read-only recovery, profile initialization, Plan lifecycle, Work Item
  mutations, blockers, evidence, proposals, Decision lifecycle, and narrow
  repair through direct files.
- Clear user choices and applicable project rules that unmistakably record a
  human-selected direction are now written and accepted without asking for the
  same choice again.
- Material possible Decisions inferred during analysis are stored as
  `proposed`, linked from affected mutable Work Items, and surfaced for an
  explicit accept, reject, or revise choice.
- Added focused Decision routing so Plan-only operations do not load the
  Decision format reference.
- Split accept-or-reject batch metadata into a batch-only reference.
- Expanded the static evaluation set from six to sixteen cases and added a
  native feature-contract map.

### Validation

- The canonical Agent Skill validator and repository diff checks pass.
- A complete Fable review of all four Scoville cores and their thirteen
  references found no P0 or P1 issue and judged standalone and family operation
  coherent; its two P2 wording and navigation findings were corrected.
- Three isolated `gpt-5.6-terra` medium-effort cases passed exact behavior and
  exact reference-routing checks with all 58 ambient Skills disabled.
- The tested repository copy and the locally installed Skill are byte-identical.

## 2026-08-08: Initial release

### Added

- Added the repository-native Scoville Plan core for creating, maintaining,
  resuming, auditing, and handing off durable Plans and Work Items.
- Added conditional guidance for planning granularity, the supported native
  `format_version: 1` Plan contract, and safe direct-file lifecycle changes.
- Added portable display metadata, installation documentation, Scoville-family
  composition guidance, and six static evaluation cases.

### Validation

- Passed the canonical Agent Skill validator.
- Confirmed the installable repository copy matches the locally tested skill.
- Parsed all six evaluation cases and checked repository links, encoding, and
  line endings.
- In the current Terra Medium family benchmark, all eight completed
  Plan-related answers were semantically source-correct. One additional attempt
  failed in the benchmark broker before completion. The run also found two
  excess reference loads and one false activation; those routing limits remain
  documented rather than presented as resolved.
