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
