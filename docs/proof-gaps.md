# Elisa proof gaps found by Mocap Cleaner

Records are grouped by implementation area. Original gap identifiers,
status descriptions and evidence are preserved in the linked records.

- [Compiler and early core gaps (G1–G20)](proof-gaps/compiler-and-early-core.md)
- [Rig tools, physics and caches (G21–G42)](proof-gaps/rig-tools-and-caches.md)
- [Foot cleanup, retiming and tracks (G43–G82)](proof-gaps/foot-retime-track.md)
- [Recent proof and native boundary status (G83 onward)](proof-gaps/recent-status.md)

- [Regression summary composition and replay](proof-gaps/regression-composition.md)
- [Nested const enum source witness gap](proof-gaps/nested-enum-producer.md)
- [Const enum distinct-value exclusion replay](proof-gaps/const-enum-value-exclusion.md)
- [Strict positive quotient bound replay](proof-gaps/strict-positive-quotient.md)
- [Law assertion coverage audit](proof-gaps/law-assertion-audit.md)
- [JSON report string decoder qualification](proof-gaps/json-string-decoder.md)
- [Compiler UI event scope collision](proof-gaps/ui-event-scope.md)
- [Literal multiplication in denied integer orders (2026-10-07)](proof-gaps/literal-product-denial-replay-20261007.md)

- [Export publication outcome qualification](proof-gaps/export-publication-outcomes.md)
- [Scoped constant call summary replay](proof-gaps/summary-call-constant-rebind.md)
- [Export report-stage Boolean branch replay](proof-gaps/report-stage-boolean-replay.md)

- [Limb length and IEEE adapter qualification](proof-gaps/limb-length-float-boundary.md)
- [Session source binding and fingerprint limitations](proof-gaps/session-source-binding.md)
- [Borrowed std and protocol region binding](proof-gaps/borrowed-protocol-region-binding.md)
- [Void-return postcondition lowering](proof-gaps/void-return-postconditions.md)
- [Build generation policy proof and replay (2026-10-07)](proof-gaps/build-generation-policy-proof-20261007.md)
- [Export sheet row field resolution](proof-gaps/export-sheet-row-resolution.md)
- [Studio runtime source selection](proof-gaps/runtime-source-selection.md)
- [FBX source and staging admission proof boundary (2026-10-07)](proof-gaps/fbx-source-staging-admission.md)
- [Task callback allocation-region ABI and ownership](proof-gaps/function-value-region-abi.md)

## Current qualification limits

The complete check is not green. Native storage qualification requires fresh
compiler provenance, and some proof obligations remain unknown or unsupported.
See the recent records for exact revisions, counts and boundary limitations.
- [Proof and standalone replay snapshot (2026-10-07)](proof-gaps/proof-replay-snapshot-20261007.md)
