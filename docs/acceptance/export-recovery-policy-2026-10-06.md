# Exact-snapshot recovery admission evidence

Policy `src/studio/export_recovery_policy.elisa`: 8/8 obligations proven and
8/8 certificates replayed. Laws `proof/studio_export_recovery_laws.elisa`:
22/22 obligations proven and 22/22 certificates replayed. Both reports have
zero findings, semantic errors and replay gaps on default prover 5776350b,
compiler/frontend f292cbe0. Laws compile on the current compiler.

Reports: `build/export-recovery-source.json`, `build/export-recovery-laws.json`.
The reviewed baseline adds only these two complete files; prior entries remain
unchanged. The policy requires all six facts simultaneously and the laws show
that each false fact rejects admission regardless of the other inputs.

This proves conditional admission, not those facts themselves. Durable recovery
records, exact published-byte identity, workspace binding, report existence and
operation state must be established by the eventual integration. Non-cryptographic
fingerprints must never be substituted for exact output matching. No recovery
UI or crash-recovery implementation is qualified by these proof results.
