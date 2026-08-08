# Changelog

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
