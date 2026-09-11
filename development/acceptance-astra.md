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

No tests or model probes have run. Keep F03 natural-language drafting and F08
other Skills' opt-out candidates unimplemented until the planned baseline probes
establish a need. Resume acceptance only on user request and identify the loaded
package/version. Structural validity alone cannot establish the new behavior.
