# Proof and standalone replay snapshot (2026-10-07)

The immutable proof/replay pair in
`../elisa-proof-mocap/build/elisa-proof-generations/232f491a63094a1781ce455f4143d98c`
passes `verify_product_pair.py resolve` and `check-current`. Both manifests carry
pair generation `232f491a63094a1781ce455f4143d98c`, strict mode, O2, compiler
and frontend revision `23a0e16a854cddec3016746a0cb9480db0c4db22`, and clean proof
source snapshot `01c953c66f1c86569464150d644d9ffe34eee78f`. The proof binary SHA-256
is `5b33fd8061bc71019f64afc2cab0afbb6abdc837cbad922e03871aa7f1b72423`; the
standalone replay binary SHA-256 is
`3013fe156900a39b5e10d4774269917f502fb523db008893fe05be3fd5fb43eb`.
`check_prover_freshness.py` also passed against the local prover source and
compiler; the compiler revision is the fetched `origin/HEAD`.

On `proof/stability_laws.elisa`, the selected proof binary reported 56/56
obligations proven, zero unproven, zero findings and zero semantic diagnostics.
The proof report contained 56 certificates and replayed all 56 internally,
with zero replay gaps and no trusted assumptions. The proof binary then emitted
a portable package; the separate `elisa-proof-replay` binary independently
reported 56/56 theorems replayed and zero not replayed. Its output marks the
kernel checked, while package reading, hypotheses and source correspondence
remain adapter trust boundaries; `source_authenticated` is false.

After fetching proof origin, `origin/main` was
`2610ddb60b3ac207016ca281a8e93e8212d7cb13`; it is an ancestor of the clean
integrated proof source HEAD `01c953c66f1c86569464150d644d9ffe34eee78f`
(`HEAD...origin/main` is `115 0`). The generation therefore qualifies the
current adopted integrated source, which includes all fetched upstream commits
and project repairs. The `build/check-current-2026-10-06.log` file ends after
`test builds: 0 cached, 78 rebuilt` and has no terminal full-check result, so
full-check status remains unconfirmed. The unrelated dirty
`proof/flight_laws.elisa` was left untouched.
