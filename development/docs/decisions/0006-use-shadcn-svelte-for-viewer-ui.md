---
format_version: 1
id: ADR-0006
status: accepted
created: 2026-09-07
accepted: 2026-09-07
scope: viewer/interface
---

# Use shadcn-svelte as the viewer interface reference

## Decision

Use the current Svelte 5 and Tailwind 4 generation of shadcn-svelte as the canonical component and token reference for the Scoville Plan Viewer. Scoville UI must implement and test the viewer against that system, including component structure, interaction states, spacing, typography, focus behavior, keyboard behavior, and responsive variants. Add only components required by the viewer; retain application-specific Plan and Decision status visualization within the same tokens and interaction rules.

## Problem

The initial functional interface used a bespoke editorial visual layer with large display typography and a decorative current-work surface. The user requested a simpler system that is commonly paired with Tauri and then explicitly selected shadcn-svelte as the reference Scoville UI must use and test against.

## Drivers

- The viewer needs a quiet, compact desktop interface that remains legible at narrow window sizes.
- Shared component states and tokens should replace one-off control styling.
- The Svelte 5 frontend needs maintained accessible interaction primitives for composite controls.
- The application should add no larger component suite than its actual controls require.

## Considered alternatives

- Keep the bespoke Svelte and CSS layer. This avoids another frontend dependency but retains a parallel control and token language that the user rejected as too visually elaborate.
- Use Bits UI alone. It supplies accessible headless behavior and is the primitive layer beneath shadcn-svelte, but it intentionally supplies no visual design system.
- Use Skeleton 5. It is a current adaptive Svelte design system, but its broader theme system is unnecessary for this focused viewer.
- Use Carbon Components Svelte. It offers mature, dense application components, but it would bring IBM's stronger product language into a small independent desktop tool.

## Consequences

The viewer adopts Tailwind 4, shadcn-svelte tokens, and the smallest copied component set needed for its controls. Local layout and status views must compose those components rather than restyling them through a competing system. Updates to copied components remain owned by this repository and require comparison with the current shadcn-svelte source when changed. Tauri continues to own the native window and file boundary; shadcn-svelte owns no project data or filesystem behavior.

## Confirmation

Confirm the installed Svelte and Tailwind versions match the selected shadcn-svelte generation, inventory every viewer control against the retained component set and tokens, run type and production builds, exercise keyboard and focus behavior for composite controls, and inspect populated, empty, unavailable, wide, intermediate, and narrow rendered states for divergence from the system or loss of required Plan and Decision information.

## Revisit when

Revisit when shadcn-svelte no longer supports the installed Svelte generation, a required desktop interaction cannot be implemented through its maintained primitives, or the retained copied components diverge enough from upstream that another maintained system reduces ownership without weakening the viewer workflow.
