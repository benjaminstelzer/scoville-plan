# Scoville Plan Viewer

A local, read-only desktop viewer for Scoville Plan format version 1 projects.
It shows the active Plan point, completed and upcoming work, current Decisions,
and superseded Decision history across a saved list of project folders.

## Run locally

Install Node.js 22 and the stable Rust MSVC toolchain, then run:

```text
npm ci
npm run tauri dev
```

The folder picker accepts a project root containing `PROJECT_INDEX.md`,
`docs/plans`, and `docs/decisions`. The portable project list is stored as
`scoville-plan-viewer.xml` next to the executable. Removing an entry does not
edit its repository. On macOS the file sits beside the `.app` bundle; an
AppImage uses its outer `APPIMAGE` location instead of the read-only runtime
mount. When an installer places the application in a read-only system folder,
the same XML file is stored in the platform user configuration directory.

## Interface system

The interface uses current shadcn-svelte components and tokens with Svelte 5,
Tailwind CSS 4, Bits UI primitives, Inter, and Lucide icons. Local CSS owns only
the viewer layout and the domain-specific Plan and Decision status
visualization.

## Validation

```text
npm run check
npm run build
cargo test --manifest-path src-tauri/Cargo.toml
npm run tauri build
```

The GitHub Actions matrix builds Linux x64, Windows x64, macOS Apple Silicon,
and macOS Intel bundles without publishing a release. Platform signing and
notarization are intentionally outside this development build. Windows x64 was
built and launched locally. macOS and Linux runtime behavior remains unverified;
their jobs validate compilation, tests, and packaging only.
