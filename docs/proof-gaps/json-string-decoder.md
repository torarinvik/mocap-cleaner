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
