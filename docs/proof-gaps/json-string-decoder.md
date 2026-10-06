# JSON report string decoder qualification

`src/io/json_string.elisa` decodes standard JSON escapes, Unicode surrogate
pairs, and validates raw UTF-8. Report parsing validates every string before
extracting metrics. Decoded keys drive container/name lookup, so escaped keys
cannot bypass structural identity checks. The CLI builds with compiler
`4c409da6`.

The scalar kernel has six assertion laws in `proof/json_scalar_laws.elisa`.
The decoder itself remains unqualified: published checker `d3a17832` reported
29/33 obligations producer-proven, 28 replayed, one replay gap, four unproven
index bounds, missing loop invariants, and a control-flow analysis budget limit.
That observation preceded adding the explicit `hex4` input-bound contract.
Loop summaries, decoder round-trip laws, malformed-input qualification, and
native comparison evidence remain required. No proof baseline was weakened.

Follow-up adds cursor invariants, an explicit short-hex rejection contract,
bounded hexadecimal output, and `proof/json_string_laws.elisa` assertions for
short hexadecimal inputs and empty content. Hexadecimal decoding uses four
explicit nibble reads. Current standalone compilation succeeds. The law closure
remains unsupported: 47/59 obligations producer-proven, with dependent decoder
summaries, index bounds, and control-flow budget failures. The laws are intended
requirements rather than accepted proof evidence.

Raw UTF-8 decoding is now isolated in a private `raw_sequence` helper with
an explicit successful cursor-bound contract. Public decoding retains the
same input and output behavior. Standalone object and full CLI compilation
succeed with current compiler `4c409da6`; focused source proof requalification
is running. This refactor does not establish decoder qualification by itself.
