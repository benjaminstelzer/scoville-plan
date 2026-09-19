---
format_version: 1
id: ADR-0003
status: accepted
created: 2026-09-19
accepted: 2026-09-19
scope: project/workflow-compatibility
---

# Allow guarded Workflow Step bundles

## Decision
Keep one Step as the default dispatch unit, but permit an explicitly invoked Workflow with its own accepted Decision to bundle adjacent Steps that share one outcome, owner, authorization, route, workspace, and Acceptance boundary.

## Problem
The current public guidance requires one dispatch per Step even when adjacent Steps form one behavior-complete unit, preventing Workflow from reducing repeated task startup and recovery cost.

## Drivers

- Scoville Plan owns Step meaning and the public compatibility boundary.
- Workflow owns runtime dispatch, task creation, routing, and review mechanics.
- Compatible bundling can reduce token and task overhead without changing retained Plan records.
- Independently resumable work and materially different risk or authority still require separate Steps and dispatches.

## Considered alternatives

- Keep one dispatch per Step without exception: Preserves the simplest contract but blocks measured Workflow optimization.
- Let Workflow bundle any Steps: Maximizes flexibility but weakens Plan-authored routing and resumability boundaries.
- Permit only guarded adjacent bundles under accepted Decisions: Preserves the default while exposing a bounded compatibility contract.

## Consequences

- Plan files gain no field, bundle marker, lifecycle state, or hidden metadata.
- One Step remains one dispatch unless an explicitly invoked compatible Workflow and accepted project Decision authorize the exception.
- A changed Decision, external effect, materially higher risk, different route, or independently resumable result forces a new dispatch.
- Workflow must publish and test its own bundling mechanics before relying on the exception.

## Confirmation

1. Verify unchanged one-Step dispatch without an explicitly authorized Workflow exception.
2. Verify one bundle for adjacent compatible Steps and separate dispatches at every mandatory boundary.
3. Run native Plan profile, recovery, routing, and existing Work Item contract tests unchanged.

## Revisit when
Reconsider if bundling weakens recovery, obscures Plan-authored boundaries, or fails to produce material task and token savings.
