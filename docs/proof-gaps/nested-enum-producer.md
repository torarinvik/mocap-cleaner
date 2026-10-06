# Nested const enum source proof witnesses

## Observed gap — 2026-10-06

Qualified prover `d3a17832`, built in strict mode with current compiler
`4c409da6`, leaves source obligations for `StudioMetricEvidencePolicy::State`
and `StudioExportValidation::Result` unproved. These are nested const enums.
The implementation must retain these types and explicit law assertions.

The prover investigation located a top-level-owner restriction in
`proof_unique_const_enum_member_owner`, in
`src/proof/check/enum_value_types.elisa` of the mocap prover checkout. Kernel
replay has qualified enum-member typing, but source witness generation does
not connect these nested owners to their enum members. Consequently summaries
for enum-returning `classify` and equality-based `is_ready` are unavailable to
composed law proofs. This is a support gap, not evidence that the laws hold.

## Required fix and qualification

- Resolve the exact qualified owner path, including nested modules.
- Keep visibility, declaration identity and backing type in the witness.
- Reject ambiguous short member names and mismatched owners or backing types.
- Qualify producer obligations and certificate replay on the same source and
  binary snapshot; report separate remaining arithmetic or composition gaps.
- Retain reviewed proof baselines and stronger law assertions. Do not replace
  enums with integers or relax replay validation to obtain passing counts.

## Candidate repair — 2026-10-06

Prover commit `6bced403` adds source-backed equality and disequality witnesses
for explicit const enum integer tags and exact scoped enum paths in the kernel
type environment. A focused generated probe under the isolated candidate,
built with compiler `f292cbe0766f2d5086f174c984b0f2cd0a64d85c`, proved and
independently replayed both `Outer::Status.Zero != Outer::Status.One` and
`Other::Status.Zero == Other::Status.ZeroAlias`; all 5 issued certificates
replayed with 0 gaps. The two `Status` declarations have repeated names in
sibling modules and different tag values. A same-value alias is accepted as
equal, and the false alias-disequality obligation remains unproved.

This is focused candidate evidence, not qualification of the default proof
binary. Broader source obligations still include unsupported proposition
formation and the existing non-comparison return-goal refusal. Keep reviewed
baselines and the default binary unchanged until those gaps have a separate
qualified replay run.
