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

The prover owner is implementing the fix. The current full check is using the
existing binary; a changed binary must not replace it during that run. Results
from the fixed prover require a separate qualified run before acceptance.
