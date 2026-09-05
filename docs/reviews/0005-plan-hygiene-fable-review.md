# Plan hygiene: Fable review and disposition

Review date: 2026-09-05. Requested model: `claude-fable-5-1`, effort `high`.
The wrapper returned no reported backend model. Persistent consultation session:
`5dc4b51a-5a3a-4409-97f0-f9bbfd22ef4a`. The call completed successfully with
read-only tools and no permission denials. This is a summary of Fable's initial
opinion and the author's subsequent corrections, not a second review of the
revised files or user acceptance of an architectural choice.

Reviewed records:

- [PLAN-0005](../plans/0005-introduce-plan-hygiene-and-lossless-archives.md)
- [ADR-0005](../decisions/0005-use-staged-plan-hygiene-with-lossless-archives.md)

## Fable's opinion

Fable found the problem real and the first selective-reading outcome useful.
No finding blocks retaining a draft. Before activation, however, the comparison
must precede archive implementation rather than justify an already-built
mechanism. Fable recommended narrowing ADR-0005 to selective reading and early
measurement, with a separate archive Decision afterward. The repository's small
existing Plans alone do not establish a large-project archive benefit.

Fable considered stable IDs, lossless evidence, optional validation, conversion
opt-in, cancelled-dependency rejection, and explicit interruption handling sound.

## Findings and verified disposition

| Finding | Disposition in the revised draft |
| --- | --- |
| Measurement followed all archive implementation. | Move W-004 immediately after W-001 without renumbering. W-002 depends on both and needs a separate explicit archive choice. W-003 later checks implemented behavior against the early projection. |
| Include successor Plans as a cheaper alternative. | Add this comparison only at genuine completed-goal boundaries. The author does not adopt the broader suggestion that prose references replace live dependencies: version 1 requires same-Plan dependencies and valid completion. |
| Selective reads need a concrete mechanism. | Specify heading and graph-field extraction plus non-printing hashes and relevant full blocks. This supports graph inspection; it does not independently prove Evidence, all syntax, or complete-profile validity. Preserve optional-validator and manual inspection paths. |
| Existing readers can ignore archive directories or report misleading missing dependencies. | Make index and resolved-Plan version checks, archive discovery, and legacy-reader rejection explicit contract requirements. No nested-folder-only extension is treated as compatible by assumption. |
| Decision-batch helper may be unaffected. | Verified that the helper operates on Decision files, not Plan bodies. Add verified-unaffected as an inventory outcome; do not require an unnecessary helper edit or rejection. |
| Physical document position conflicts with archival. | Explicitly distinguish preserved logical order in a new archive format from unchanged version-1 physical-position semantics. Terminal authored content remains immutable. |
| Decision relations must include archived Work Items. | Name incoming Decision references used by proposal deletion and supersession in the archive contract acceptance. |

The conditional archive work remains `todo`, not accepted or started. If it is
not selected, the Plan describes explicit removal of those eligible items before
guarded final completion, avoiding an idle current-item dead end. A hand-authored
archive projection measures potential returned-text reduction only; actual
retrieval behavior, reliability, and provider cost require later observation.

## Evidence boundary

Only planning and review records were authored for this request. No Skill rule,
consumer, test implementation, existing project record, or installation was
changed. The native profile validator checks the resulting record structure;
it does not verify the proposed archival behavior or the predicted savings.
