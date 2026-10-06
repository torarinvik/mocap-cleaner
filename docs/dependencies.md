# Dependency revisions

These are observed checkout revisions, not a claim that every integration gate
passes. The Studio and CLI builds use the paths described in the README.

| Dependency | Worktree | Branch | Observed revision | Provides |
| --- | --- | --- | --- | --- |
| Elisa-engine | `../elisa-engine-mocap` | `mocap-track` | `bc98339e` | Viewport, motion math, GLB IO, native path/Trash/manifest-lock adapters and reserved namespace comparison. |
| elisa-ui | `../elisa-ui` | `main` | `c9ff0b64` | AppKit canvas, input and accessibility hosting. |
| elisa-proof | `../elisa-proof-mocap` | `mocap-cleaner-proofs` | `6e3e8754` | Contract proving and certificate replay; remaining gaps are indexed in `proof-gaps.md`. |
| Elisa compiler | `../Elisa-compiler` | Current local checkout | `c5bfd9cf` | Elisa compilation and runtime. Product provenance must match its sources for strict checks. |

## Current integration evidence (2026-10-06)

- Studio builds successfully with `STUDIO_SKIP_CHECKS=1`; the old blanket
  statement that the UI cannot build is obsolete. Native UI journey acceptance
  is still incomplete.
- The latest completed authorized full check rebuilt and passed 78 Elisa
  executables and four CLI scenarios. Its native Storage gate stopped at stale
  compiler provenance, and its proof gate reported remaining regressions.
  Subsequent focused builds are documented with their own changes; they do not
  establish a green full check at the current head.
- The compiler checkout is now clean. A normal seed rebuild stopped at the
  upstream stage0 freshness guard because that source tree has uncommitted
  changes. No stale-oracle override was used. Until a fresh seed build succeeds
  and the strict checks rerun, native Storage acceptance remains open.
- Native lock, Unicode namespace and transaction wiring have build evidence;
  concurrent-process, crash/release-failure and Unicode filesystem scenarios
  still need runtime acceptance.

Keep historical failure details in `proof-gaps.md` and current acceptance work
in the implementation plan rather than treating old dependency snapshots as
current blockers.
