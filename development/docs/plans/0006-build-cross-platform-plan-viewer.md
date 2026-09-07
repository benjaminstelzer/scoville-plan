---
format_version: 1
id: PLAN-0006
status: completed
created: 2026-09-07
updated: 2026-09-07
---

# Build a cross-platform Scoville Plan viewer

## Goal

Deliver a local read-only desktop application for Windows, macOS, and Linux that lets users add and remove Scoville Plan project roots, switch projects from the top of the window, understand current, completed, and upcoming Work Items at a glance, and distinguish current Decisions from proposals and inactive history. The interface adapts meaningfully to wide, intermediate, and narrow window sizes without hiding required status information.

## Non-goals

- Do not edit Plan, Work Item, Decision, or project files from the application.
- Do not introduce a database, remote service, account, synchronization layer, or alternative source of project facts.
- Do not change the Scoville Plan format or infer lifecycle state that the files do not record.
- Do not publish installers or claim runtime verification on an operating system that was not actually exercised.

## Work items

### W-001 Read supported Scoville Plan projects into a deterministic view model

Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: A deterministic reader accepts a selected format-version-1 project root and returns Plans, Work Items, Decisions, active routing, relationships, progress counts, and actionable diagnostics without modifying project files.
Acceptance: Focused automated tests cover active and idle projects, Work Item ordering and statuses, Decision lifecycle and supersession links, malformed or unsupported input, and path containment; the final reader exposes every field needed by the viewer while preserving distinct native statuses.
Steps:
1. Define the typed view model and secure read boundary for canonical project paths.
2. Parse index, Plan, Work Item, and Decision records without making lifecycle inferences.
3. Exercise representative valid and invalid fixtures and inspect the final reader boundary.
Evidence: [Fifteen Rust tests pass for active, idle, malformed, truncated, unsupported, contained, duplicate, contradictory, superseded, cancelled-history, live-profile, missing-config, and portable XML and IPC round-trip cases.]

### W-002 Provide the responsive project and status workflow

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0006]
Outcome: Users can add, remove, recover, refresh, and switch projects and can inspect the selected project's active work, ordered Plan status, and Decision status and supersession history in a responsive interface.
Acceptance: A populated project can be added and survives restart; removing it deletes only the viewer entry; missing roots have a clear recovery action; the retained shadcn-svelte component set and tokens own controls and states without a competing local design language; keyboard and pointer flows expose selection, refresh, filters, details, and status feedback with the expected shadcn-svelte and Bits UI behavior; rendered wide, intermediate, and narrow windows preserve project switching, current item, next action, complete status text, and Decision relationships without page-level horizontal overflow; a final component and state inventory is checked against the selected design-system reference.
Steps:
1. Implement the Tauri shell, local project registry, and project workflow states.
2. Implement the hierarchy and responsive transformations around real profile content.
3. Render and inspect populated, empty, missing, loading, and error states across representative window sizes and repair observed failures.
Evidence: [Svelte check passed with zero diagnostics, Playwright rendered wide intermediate and narrow views with zero page overflow, Browser interaction verified filters pressed states tab panels supersession and blocker detail, The tested IPC boundary atomically saved and reloaded portable XML, The packaged Windows app loaded the same real project on two launches]

### W-003 Prepare native packages for the three target operating systems

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: []
Outcome: The repository can produce native Scoville Plan Viewer packages for Windows, macOS, and Linux from explicit platform jobs while keeping untested runtime claims bounded.
Acceptance: The final frontend build and focused tests pass; the Tauri configuration has least-privilege capabilities for the implemented workflow; a platform matrix defines Windows, macOS, and Linux build artifacts; the current host produces and launches its native development or packaged build when the required toolchain is available; unexercised platforms remain explicitly unverified.
Steps:
1. Add Tauri capabilities, metadata, icons, and platform build configuration required by the implemented workflow.
2. Add a repository-owned build matrix for Windows, macOS, and Linux.
3. Run available native checks and document the exact verified platform boundary.
Evidence: [Frontend production build passed, Fifteen Rust tests passed, Windows release EXE launched and responded, MSI and NSIS bundles were produced, GitHub Actions defines Linux Windows and two macOS architecture jobs, macOS and Linux runtime remain unverified]
