# Checked requires-call positional labels

The checked total-Boolean helper summary rejected every call whose AST carried an
`argument_names` array, including ordinary positional calls. Elisa's parser records an
empty label for each positional argument, so a two-argument positional call has two empty
labels. The summary gate now accepts either no labels or exactly one empty label per
argument; named and malformed partial label arrays remain refused. It still requires a
unique checked pure Boolean callee, matching arity, local arguments, ordered preconditions,
and a checked postcondition.

The repair is in proof-assistant commit `d1b2c77c780c481209c8984f5e79860170166113`.
The focused `scripts/test_correspondence_requires_call.py` suite passes against matched pair
generation `2e66637259b14336b1cfeb09c4fd3e72`. That generation used compiler revision
`90637b5192921827131615c799f7317af5752924`, Stage1 product SHA-256
`fe06da441eb844fc313946e2c58f25a0d227e65da82d569bdfdce26719c446db`, and runtime SHA-256
`6b5247cec30a39ac1d00e0e61a088ccb4d0901932d518d3f6be32e79b9f5412f`. Its producer source
tree digest is `cf70695255214ec663924b26bb30d8690decf0eef45f6f042ee5c8a02115822e`, identical
to the frozen build snapshot and the committed proof `src` tree. The build manifest marks
the source checkout dirty because the proof changes were not committed at build time; the
recorded source-tree digest captures the exact content that was later committed.

The controls cover positional calls, zero-argument calls, named and mixed-label refusals,
wrong-owner and changed-callee refusals, reordered arguments, missing or late preconditions,
and ineligible helper summaries. A call in a returned expression remains outside this
repair: the `empty_take_refused` control is not checked.

Current bounded-path law results are recorded in
`build/bounded-path-policy-2e666372-positional-label-pair-r2/result.json`. Declaration
formation reports 22/22 obligations proven; package replay and independent replay each
cover 22/22 theorems. Source correspondence remains partial: 7 functions checked, 2
unmatched, and 2 unsupported. In particular, `empty_path` and `empty_take_refused` are
unmatched, while `missing_terminator` and `invalid_take_path_refused` are unsupported.
These results do not establish source authentication for the whole bounded-path module.
