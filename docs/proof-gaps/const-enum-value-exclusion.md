# Const enum distinct-value exclusion replay

The export-validation laws compare a result against `READY` after requiring a specific error
variant. Elisa const enum variants may alias the same integer, so variant names alone cannot
justify that those comparisons are disjoint.

The proof assistant emits a pairwise exclusion fact only when both variants belong to one
exactly resolved const enum, both declarations carry explicit integer literal tags, the tags
differ, and the enum does not define custom equality. The independent replay checker verifies
those same facts from the source declarations. Implicit tags, expression-valued tags, aliases,
ambiguous ownership, and custom equality produce no disequality fact. Equal tags instead yield
an equality fact, so repeated variant names or names alone never imply inequality.

With compiler source revision `f292cbe0766f2d5086f174c984b0f2cd0a64d85c` and prover commit
`5776350b3765bc563f52e3df30331b8290c3d824`, the export-validation source has 6/6 obligations
proven and replayed. `proof/studio_export_validation_laws.elisa` has 14/14 obligations proven
and replayed, with zero findings and zero replay gaps. The proof build used strict mode and a
clean source snapshot.

## Exact scoped values — 2026-10-06

Prover commit `6bced403` extends the value evidence to exact qualified enum owners and validates
the declared integer values during independent replay. An isolated candidate built with
compiler `f292cbe0766f2d5086f174c984b0f2cd0a64d85c` replayed 5/5 focused certificates with no
gaps. The probe established a disequality for different tags in `Outer::Status` and equality for
same-valued aliases in sibling `Other::Status`. The false disequality for same-valued aliases
remained unproved. This does not qualify the default proof binary: broader function contracts
still have unsupported proposition cases, and the non-comparison return-goal refusal remains.

## Reverse disequality orientation — 2026-10-07

The existing publication durability law exposed a producer gap: source-derived const-enum facts
contained `NotPublished != PublishedDurabilityUnknown`, while the contract asked for the reverse
comparison. The replay validator already re-derived both member owners and literal tag values in
either orientation; the producer had emitted only the declaration-order orientation. Commit
`897798bfafaaab5a3b02fab30f24bddca8dc3fbf` now emits the reverse `!=` fact only when the exact
const-enum literal tags differ. Equal-valued aliases still produce equality only, and implicit or
expression-valued tags remain unsupported.

The clean paired generation
`../elisa-proof-mocap/build/elisa-proof-generations/8147b64172c74ca5b5f92ba3eb065033`
passes `verify_product_pair.py check-current` and
`scripts/check_prover_freshness.py`. Both products use proof source commit `897798bf`, clean
source snapshot SHA-256 `2a049e295cf566eefd0ce1383c7293083f2b3e13a1f73956a3b59f7c8560fe71`,
compiler source `bb1f4095e350aa8dcb232a0e56b53c684b44ce2f` (binary SHA-256
`203009661b41a4aed677487848d300b7232d0801f76fa19a65222309ffe039a7`), and explicit runtime
SHA-256 `02d868eb68739e517830684eb89bb820bec16f8d07f92ff7bbacee35ef188cb6`.

On the unchanged `proof/studio_publication_durability_laws.elisa` source (SHA-256
`2646cfd05483b9d8834a4aa3a2cb2308dfbd591a07a90c7a4463fa426f927afe`), the producer now reports
17/17 obligations proven, zero findings and zero replay gaps. The independent replay binary
replays all 17/17 packaged theorems. The report has one non-error semantic diagnostic. The
package remains adapter-bound: `source_authenticated` is false, so this evidence qualifies
producer and certificate replay for the law source but does not establish source authentication
or source-to-obligation correspondence.
