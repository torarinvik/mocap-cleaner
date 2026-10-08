# Character rest-shape qualification

The full character fixture compiled and ran on the frozen current
`85eef9ff` compiler / `c9f02ea0` Stage1 tuple. Evidence:
`build/character-current-qualification/`. This covers character binding,
malformed binding, rest-count boundaries and posed-vertex comparison; it
cannot qualify Studio redraw, global cache lifetimes or the reported crash.

The matched proof pair generation `11b83922ca9e4ec3b5e9ffdd7c19e88f`
was used for declaration proving of `proof/studio_character_bind_laws.elisa`.
The initial implication form produced 75 obligations, 60 proven and 15 findings.
An exactly equivalent split disjunction contract produced 76 obligations,
63 proven and 13 findings: the two additional rest-shape law unknowns disappeared.
The complete file still exits 1. Evidence:
`build/character-rest-proof-current/declaration-equivalent.log`.

Remaining findings concern unsupported proposition formation and unverified
callee summaries in the existing binding/coverage laws. Diagnostic line numbers
refer to expanded input, so they must be mapped before attributing them to a
particular source declaration. The declaration result is not full current-source
correspondence or independent replay qualification. Preserve all contracts and
repair remaining prover gaps before closing the proof requirement.
