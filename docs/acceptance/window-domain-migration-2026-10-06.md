# Sliding-window constant representation

`Window::Domain` groups unchanged frame (10,000,000), radius (1,000) and
reflection magnitude (1,000,000,000) limits. Contracts, law consumers, track
adapters and the existing fixture use qualified constants. These numeric limits
are not finite choices. No executable test was added or run for this migration.

Focused evidence uses the clean separate prover `4da37c97` built against compiler
`45330579`, not the older default prover. Source has 40/43 proven obligations;
laws have 242/248. Three source findings concern `middle` postconditions and
refuse at the proof budget gate; no semantic errors are reported. Full evidence
is `build/window-domain-source.json`; wrapper results are under `build/proof/`.

The unchanged source and laws from before this migration were separately proved
with the same candidate, under `build/repro/window-before-domain.elisa` and
`build/repro/window-laws-before-domain.elisa`. They also produce 40/43 and
242/248. Thus this candidate's unresolved results are not introduced by the
constant representation change. Historical baselines (42 and 244 proven) remain
unchanged; current proof closure and candidate promotion remain open.

Normal compilation awaits the current constructor-owner compiler rebuild.
The existing track fixture will be covered by the authorized full check after
the source/toolchain snapshot stabilizes.
