---
format_version: 1
id: PLAN-0005
status: completed
created: 2026-09-05
updated: 2026-09-05
---

# Introduce Plan hygiene and lossless archives

## Goal

Reduce completed Work Item history loaded during routine large-project work
while preserving canonical authored records, dependency readiness, Decisions,
acceptance evidence, and reliable resumption. First improve selective reading,
then add optional lossless archival if the reviewed contract and measured value
justify its additional complexity. The user authorized implementation of this
reviewed Plan on 2026-09-05; archive work retains its explicit decision gate.

The completed scope is W-001 followed by W-004. After the early comparison,
the user selected the recommendation to retain selective reading without
archives on 2026-09-05. The two unstarted conditional archive items were removed
in the prepared final completion; remaining IDs were preserved. No archive
format, project conversion, or installation was introduced.
The initial [Fable review and corrections](../reviews/0005-plan-hygiene-fable-review.md)
are retained separately from future Work Item acceptance evidence.

## Non-goals

- Do not convert existing projects or archive version-1 records as part of
  the selected reading-hygiene implementation.
- Do not delete or replace historical Acceptance or Evidence with summaries.
- Do not introduce a second planning owner, mandatory CLI, database, service,
  automatic writer, or dependency on Git for reading canonical project facts.
- Do not weaken dependency, lifecycle, authority, path-safety, concurrency, or
  complete-profile validation guarantees to reduce model-visible output.
- Do not impose a universal item-count or token threshold without measurements.
- Do not alter unrelated working-tree changes, sibling Skills, installations,
  releases, or retained earlier benchmarks; do not authorize additional paid
  model evaluations through this Plan.

## Work items

### W-001 Make routine Plan reads proportional to the affected work

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0005]
Outcome: Read-only recovery and ordinary progress edits load only required Plan content into model context while preserving relation checks and detection of concurrent changes.
Acceptance: The read-only and native-editing routes agree on frontmatter, current or affected full Work Item blocks, required goal context, relevant dependency facts, referenced Decisions, and proposed-Decision discovery; post-write verification inspects the changed records and affected relations without requiring the full unchanged Plan body in model output; complete structural validation still reads the complete profile internally; whole-file byte/hash checks remain possible without printing whole-file contents; a large-profile fixture demonstrates bounded unrelated-history output for resume and progress edits and still detects an invalid untouched dependency and a concurrent change; no archival or format change is needed for this outcome.
Steps:
1. Review the current read-only and editing rules together with the existing validator and test/evaluation conventions; distinguish machine file reads from text returned to the model.
2. Specify and implement the smallest consistent read and verification guidance in scoville-plan/SKILL.md and the relevant references; use a metadata extraction of H3 IDs and ordered Status, Depends on, and Decisions fields for graph questions plus hashes without body output, complete relevant blocks for authored meaning, and full validation or explicit manual inspection for remaining invariants; this extraction alone proves neither Evidence nor complete-profile validity.
3. Verify representative resume and progress-edit traces, relevant relation failures, and compact validator diagnostics; retain the observations and limits with the changed guidance.
Evidence: [Four owning Skill files now distinguish full checks from scoped output, Seven hygiene tests passed including untouched dependency and evidence failures plus stale-write refusal, PowerShell-only current-block read and unchanged SHA-256 passed, Agent Skill quick validation passed, Baseline sources and experiment protocol retained under docs/benchmarks/plan-hygiene]

### W-004 Measure residual history overhead before selecting archives

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0005]
Outcome: An early deterministic comparison identifies residual overhead after selective reading and supports a decision on whether archive implementation is worth pursuing.
Acceptance: Before measurement, freeze baseline and read-hygiene fixtures, a hand-authored archive-shaped projection, and a successor-Plan comparison only at genuine completed-goal boundaries; freeze identical task content, starting states, extraction operations, tokenizer if available, correctness checks, and reporting rules; include small and large profiles with contiguous and interleaved terminal history and resume, progress, prerequisite, history lookup, and complete-audit tasks; count returned text and lookups separately from internal bytes, Skill payload, actual provider usage, and cost; label synthetic fixtures, scripted output, projected archive savings, and unimplemented retrieval explicitly; verify the projection retains all required facts and account for estimated setup and maintenance work without calling it observed runtime behavior; retain failures and report where rollover is inapplicable; record a recommendation for read hygiene alone, valid Plan rollover, or a separate archive Decision based on measured residual overhead and projected incremental benefit; actual agent behavior and monetary savings remain unverified without a separately agreed provider experiment; absence of a representative real large Plan limits the recommendation rather than proving broad value.
Steps:
1. Freeze representative fixtures and extraction operations before measurement, using anonymized copies only when a real large Plan is available; no archive parser or format implementation is needed for the projection.
2. Compare existing and selective-read returned text with the archive projection and valid successor-Plan cases; preserve goal and dependency semantics instead of converting live dependencies into prose.
3. Write the bounded result and recommend whether to pursue a separate archive Decision; if no archive is selected, obtain the explicit scope choice and remove eligible conditional items before guarded final Plan completion.
Evidence: [Frozen protocol and raw results retained in docs/benchmarks/plan-hygiene, All 24 scripted comparisons and four guard traces completed, Two completed-goal successor profiles validated, Report docs/benchmarks/plan-hygiene.md recommends selective reads without archive implementation, All 57 repository tests passed, Agent Skill validation and package/report link checks passed, User selected the recommendation on 2026-09-05 and authorized removal of the two unstarted conditional archive items]
