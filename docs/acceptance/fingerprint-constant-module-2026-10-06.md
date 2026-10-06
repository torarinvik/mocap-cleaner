# Fingerprint constants

The two residue moduli now belong to `StudioSourceFingerprint::Residue`, a
const module. They are numeric algorithm parameters, so an enum or algebraic
data type would not represent them better. Every source, law and existing test
consumer uses the scoped names; arithmetic and identifiers remain unchanged.

Normal compiler `04b384ec` compiled the fingerprint law composition without
diagnostics. Clean isolated prover `3ac99624`, built with compiler/frontend
`f292cbe0`, proved and independently replayed source 6/6 and laws 34/34 with
zero gaps, findings or semantic errors. Reports are
`build/source-fingerprint-const-module-source.json` and
`build/source-fingerprint-const-module-proof.json`. Existing baseline counts
remain unchanged. No executable tests were added or run.

This local refactor does not establish completion of the repository-wide
constants audit or qualify downstream native Studio behavior.
