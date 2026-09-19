# F02 acceptance deferred

2026-09-11: the user selected the reviewed change to status-query behavior and
deferred acceptance. Keep project-wide proposal visibility; request decisions
only for dependent work or explicit Decision handling. This replaces the old
question requirement in read-only-surfaces-proposals; its fixture was updated
to express the authorized contract, not to claim a passing test.

Pending cases:
- Status query with two unrelated proposals shows both without demanding choices.
- Repeated unchanged status query does not repeat the decision question.
- Dependent implementation asks before acting; unrelated work continues.
- Explicit Decision handling asks appropriately; an already explicit choice is
  not requested twice. Silence or existing code never establishes acceptance.
- Proposal visibility and native format/lifecycle remain intact.

At deferral, no tests or model probes had run. Keep F03 natural-language drafting and F08
other Skills' opt-out candidates unimplemented until the planned baseline probes
establish a need. Resume acceptance only on user request and identify the loaded
package/version. Structural validity alone cannot establish the new behavior.

## 2026-09-12 partial acceptance

The existing Python suite passed 50/50. Four fresh Astra Low supplied-text probes
showed both proposals without a decision demand for initial/repeated status,
and asked for choices for dependent work or explicit Decision handling. The
repeat probe supplied prior context; it was not a resumed session. No actual
reads, lifecycle writes or F03 drafting were tested. Full acceptance stays open.
Tested SKILL.md SHA-256:
`d534f0ccdb7e31b38a5dc9ccc1fba3319207808ca5f08ef04828b96cf9f2ba2d`.
Cross-Skill method and limits: Scoville Code's
`development/astra-acceptance-2026-09-12.md`.
