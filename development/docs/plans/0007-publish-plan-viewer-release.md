---
format_version: 1
id: PLAN-0007
status: active
created: 2026-09-07
updated: 2026-09-07
current_item: W-002
---

# Publish the cross-platform Plan Viewer release

## Goal

Publish one current Scoville Plan GitHub Release that includes the installable Skill package and clearly named native Viewer downloads for Windows, macOS, and Linux, after correcting and rechecking the interface spacing across responsive states.

## Non-goals

- Do not claim that macOS or Linux packages were launched locally.
- Do not change Scoville family membership or unrelated Skill behavior.
- Do not retain obsolete GitHub Releases or release-version tags after the replacement release is verified.

## Work items

### W-001 Correct and verify interface spacing

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0006]
Outcome: Empty, loading, error, overview, Plan, and Decision states use deliberate shadcn-svelte-aligned spacing and remain usable at wide, intermediate, and narrow widths, while an unusually long active Plan header stays inside a bounded card and Plan history sits beside project selection in the top bar.
Acceptance: Missing vertical separation is repaired, comparable relationships use the same spacing tokens, Plan goals are collapsed by default inside a rounded white card and scroll within that card when expanded beyond its height limit, Plan identity and current Plan point identity remain visibly distinct, Project and Plan labels precede their selectors in one aligned top-bar row at normal widths, medium windows use two rows, very narrow windows use three rows with all three actions visible, optional status badges never move disclosure arrows, completed markers are green with white checks, and rendered responsive states show no overlap or page-level horizontal overflow.
Steps:
1. Audit the complete spacing inventory instead of checking only repeated numeric values.
2. Repair missing or inconsistent relationships with the smallest layout change.
3. Render representative states and widths and inspect the results.
Evidence: [Rendered wide 900px 720px 520px 420px and 360px views have no page overflow, Empty-state geometry measures 12px from heading to description and 24px from description to action, Plan goal is collapsed by default and expands inside a white rounded card with overflow auto, All six tested disclosure arrows share the same X position, Completed marker resolves to green with white text, Three top-bar actions remain present at 360px]

### W-002 Prepare versioned cross-platform release assets

Status: in_progress
Depends on: [W-001]
Blocked by: []
Decisions: []
Outcome: The release candidate has one coherent version and a CI workflow that retains each native executable, installer, application archive, package, and checksum needed by end users.
Acceptance: Windows provides portable EXE, MSI, and NSIS files, macOS provides Apple Silicon and Intel DMG and app archives, Linux provides a portable binary, AppImage, DEB, and RPM files, and the Skill ZIP remains available.
Steps:
1. Align application and repository release versions.
2. Stage deterministic per-platform asset names in GitHub Actions.
3. Validate source, package structure, and workflow configuration before publication.
Evidence: [Viewer version owners agree on 1.3.0, Windows portable EXE MSI and NSIS packages were built and the EXE launched responsively, Workflow stages portable and native package downloads for Windows x64 Linux x64 macOS Apple Silicon and macOS Intel, Current official runner labels are used for both macOS architectures]
Next action: Commit the validated candidate and run all four GitHub Actions package jobs from that commit.

### W-003 Publish and verify the GitHub Release

Status: todo
Depends on: [W-002]
Blocked by: []
Decisions: []
Outcome: GitHub exposes one stable current release whose assets match the verified release commit and whose older release records and release-version tags have been retired.
Acceptance: The default branch, annotated tag, release, asset checksums, public copy, Skill package, profile entry, and one-current-release state pass remote verification.
Steps:
1. Commit and push the validated candidate to the default branch.
2. Build all platform assets from that commit and publish the replacement release.
3. Verify every asset and checksum before deleting the prior release and tag, then run the publication audit.
Evidence: []
Next action: Wait for the versioned platform builds after the release commit is pushed.
