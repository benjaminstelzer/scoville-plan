---
format_version: 1
id: PLAN-0007
status: completed
created: 2026-09-07
updated: 2026-09-07
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
Acceptance: Missing vertical separation is repaired, comparable relationships use the same spacing tokens, the project name appears above Plan identity, Plan goals use the full card width and are collapsed by default inside a rounded white card, only expanded Goal content scrolls beyond its height limit while the card keeps visible lower padding, Plan identity and current Plan point identity remain visibly distinct, Project and Plan labels precede their selectors in one aligned top-bar row at normal widths, medium windows use two rows, very narrow windows use three rows with all three actions visible and named accessibly, status messages clear the responsive top bar, optional Work Item badges never move disclosure arrows, completed markers are green with white checks, every Plan-point row retains a separately visible dynamically padded step number, open active paused completed and cancelled states use distinct symbols and semantic colors, paused and cancelled carry text badges, blocked remains independently visible, Decision rows use no badges and expose lifecycle plus active-Plan-point linkage when expanded, filtered Plan-point and Decision lists paginate after 100 entries and reset to their first page when their context changes, long row titles remain readable, the native and interface icons share one mark, and rendered responsive states show no overlap or page-level horizontal overflow.
Steps:
1. Audit the complete spacing inventory instead of checking only repeated numeric values.
2. Repair missing or inconsistent relationships with the smallest layout change.
3. Render representative states and widths and inspect the results.
Evidence: [Rendered wide 900px 720px 520px 420px and 360px views have no page overflow, Empty loading error overview Plan Goal Work detail and Decision detail states were rerendered after the global type and spacing pass, Empty-state geometry measures 12px from heading to description and 24px from description to action, Plan goal is collapsed by default and expands inside a white rounded card with overflow auto and 16px separation plus bottom padding around its scrollable content, Expanded Work detail text aligns with its title column within 0.17px at both 900px and 360px, All six tested disclosure arrows share the same X position including combined Paused and Blocked badges, Paused and Blocked both compute to 12px text at weight 500 with 16px line height 20px total height and identical padding and baseline, Completed marker resolves to green with white text while Paused uses a pause icon and Cancelled uses an X, Step numbers remain visible beside every state icon and derive their width from Plan length, Decision panes and tabs contain no badges while expanded Decisions state applicability and active-point linkage, Synthetic 205-entry Plan and Decision lists render 100 rows per page expose three accessible pages and retain zero horizontal overflow at 360px, Page changes move both lists beneath the 145px mobile top bar focus their first new row and announce the new page, Changing filters from page two resets each list to page one and removes pagination when fewer than 101 rows remain, Three top-bar actions remain present at 360px, The UI favicon and native icon formats use the same transparent three-bar mark and colors, Astra Medium found no P1 or P2 release blocker and its remaining Work-detail alignment finding was corrected and rendered]

### W-002 Prepare versioned cross-platform release assets

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: []
Outcome: The release candidate has one coherent version and a CI workflow that retains each native executable, installer, application archive, package, and checksum needed by end users.
Acceptance: Windows provides portable EXE, MSI, and NSIS files, macOS provides Apple Silicon and Intel DMG and app archives, Linux provides a portable binary, AppImage, DEB, and RPM files, and the Skill ZIP remains available.
Steps:
1. Align application and repository release versions.
2. Stage deterministic per-platform asset names in GitHub Actions.
3. Validate source, package structure, and workflow configuration before publication.
Evidence: [Viewer version owners agree on 1.3.0, Windows portable EXE MSI and NSIS packages were rebuilt and the final EXE launched responsively with product and file version 1.3.0, Portable builds keep executable-adjacent XML while read-only installed locations fall back to the platform user configuration directory, Workflow stages portable and native package downloads for Windows x64 Linux x64 macOS Apple Silicon and macOS Intel, Current official runner labels are used for both macOS architectures, GitHub Actions run 34133861138 built all four platform targets successfully from release commit 85b408ec7db7406feb1a1bfaa8314f6d66ab6018, Eleven native downloads plus the Skill archive and checksum files were staged with stable versioned names, Astra High found no remaining P1 or P2 release blockers after the storage expanded-title and pagination corrections]

### W-003 Publish and verify the GitHub Release

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: []
Outcome: GitHub exposes one stable current release whose assets match the verified release commit and whose older release records and release-version tags have been retired.
Acceptance: The default branch, annotated tag, release, asset checksums, public copy, Skill package, profile entry, and one-current-release state pass remote verification.
Steps:
1. Commit and push the validated candidate to the default branch.
2. Build all platform assets from that commit and publish the replacement release.
3. Verify every asset and checksum before deleting the prior release and tag, then run the publication audit.
Evidence: [Annotated tag v1.3.0 resolves to release commit 85b408ec7db7406feb1a1bfaa8314f6d66ab6018, Stable GitHub Release v1.3.0 publishes fourteen uploaded assets with direct platform links, Remote asset sizes and SHA-256 digests match every locally verified release file, Release notes copy the README Skill-install prompts and identify local versus runner validation boundaries, Prior release and release-version tag v1.2.15 were removed only after the replacement passed its pre-cleanup audit, Final publication audit reports one published release one release-version tag zero warnings and zero issues, Repository structure profile placement and all eight Scoville family members pass]
