# Const enum distinct-value exclusion replay

The export-validation laws compare a result against `READY` after requiring a specific error
variant. Elisa const enum variants may alias the same integer, so variant names alone cannot
justify that those comparisons are disjoint.

The proof assistant now emits a pairwise exclusion fact only when both variants belong to one
uniquely resolved const enum, both declarations carry explicit integer literal tags, the tags
differ, and the enum does not define custom equality. The independent replay checker verifies
those same facts from the source declarations. Implicit tags, expression-valued tags, aliases,
ambiguous ownership, and custom equality produce no exclusion fact.

With compiler source revision `f292cbe0766f2d5086f174c984b0f2cd0a64d85c` and prover commit
`5776350b3765bc563f52e3df30331b8290c3d824`, the export-validation source has 6/6 obligations
proven and replayed. `proof/studio_export_validation_laws.elisa` has 14/14 obligations proven
and replayed, with zero findings and zero replay gaps. The proof build used strict mode and a
clean source snapshot.
