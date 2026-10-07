# Suggestion measurement admission: source compilation

Status: object compilation passed; proof and native qualification remain open.

The policy bounds computed, unit-scaled distances before integer conversion.
Admission requires finite, nonnegative binary64 input within the declared exact
conversion range. Preservation tolerances are unchanged. Laws cover negative,
oversized and nonfinite refusal, zero, rounded bounds and tolerance boundaries.

## Captured inputs and result

- Primary source revision: `8cf407f`.
- Compiler revision: `5b3546508e36c35fcff94ae4b7631874e651e62c`, clean
  worktree at observation; selected through its freshness-checking wrapper.
- Compiler binary SHA-256:
  `89d1b2ea78f8fbfe675386d0d2b84767077bb1572e23dece46f30d9749d59ce4`.
- Policy SHA-256:
  `120acf05f4d72ba50a38ce777d8c9071b8c7fd475ffee9e88e276014cc1112fd`.
- Law source SHA-256:
  `0d88a27bd100d8aca9d3fcbefe055174bfe8806999b69c9e047b50408d2a42f8`.
- Object SHA-256:
  `671d7bab777a4e6f4fc6efdc16fbea6150072950822b5ffb2f8d53892bc326af`.

Command from the repository root:

```sh
../Elisa-compiler-m5-numeric-call-lowering/scripts/elisac_stage1.sh \
  proof/studio_suggestion_metric_laws.elisa -emit obj \
  -o build/suggestion-metric-qualification/laws.o
```

Observed exit: 0. Retained diagnostic log:
`build/suggestion-metric-qualification/compile.log` (empty on success).
No executable or test suite ran. This small graph imports only the policy;
concurrent application/report edits were not part of this compilation.

## Remaining acceptance

- Integrate guards before boundary/velocity casts and verify unavailable display
  and preservation admission through the complete current Studio graph.
- Authenticate and replay intended obligations, including floating-point
  semantics; unsupported reasoning remains an explicit gap.
- Qualify NaN, infinity, overflow from finite coordinates, negative and oversized
  results, rounding boundaries and normal motion in native execution.
- Qualify exact sampling-domain checks and unchanged candidate/history after
  refused evidence. Source compilation does not establish any of these results.
