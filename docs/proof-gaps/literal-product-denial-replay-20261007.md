# Literal multiplication in denied integer orders (2026-10-07)

The prover and replay kernel now admit multiplication while normalizing a denied
integer comparison only when the complete expression has a scalar witness and
one operand is a closed, nonnegative integer literal. Existing wrap guards
remain required before the product can be used as integer arithmetic. This
closed the `digit_step` obligation in the GoTo draft policy without widening
admission to general nonlinear arithmetic.

## Current paired products

The qualified pair is
`../elisa-proof-mocap/build/elisa-proof-generations/9c4f775de9b0442885ee8283602a7c58`.
Both manifests identify proof HEAD `cb92d0b35807a65935567c617d9e8f25bc7ba66e`
(clean source tree `6fae80a7d9970ae699b69f4b94b2cdae89b6194fa3b3dd55032f0761d1ec3404`)
and compiler source/product revision `bb1f4095e350aa8dcb232a0e56b53c684b44ce2f`
(product SHA-256 `203009661b41a4aed677487848d300b7232d0801f76fa19a65222309ffe039a7`).
The runtime is the compiler checkout's
`build/runtime/elisacore_runtime.o` (SHA-256
`02d868eb68739e517830684eb89bb820bec16f8d07f92ff7bbacee35ef188cb6`). The pair
was built with only `ELISA_COMPILER_BIN=../Elisa-compiler/bin/elisac-stage1`,
without a runtime override. `verify_product_pair.py check-current` and
`check_prover_freshness.py` both passed.

| Product | SHA-256 | Manifest SHA-256 |
| --- | --- | --- |
| `elisa-proof` | `19d09b91e41b9900bf34bf9801e29a0ac51b37b9ab77c3d305d389a537389f87` | `18693a74f12837d1ad58ad0344cfbff64d16ccae631180f505d354bc07aa6f58` |
| `elisa-proof-replay` | `fefcdc35318a24f80a9f8673554a7a6009c9fe4051522b73c0684a35b78f7732` | `bf0f62a990cc67550efd9e56ae585295dc4dec6e7bc96835dd6d2bff9d810ac0` |

The previous generation `f74f69896e2d47e19011c166a93a46df` selected the global
`~/.elisac/elisacore_runtime.o` (SHA-256
`b51e6114f0576681e432e1162a3dbdcdac46c140d3b7e7256c0069be0bd11897`) and was
rejected by current-provenance freshness. It is not qualification evidence.
The build resolver now infers the checkout beside an explicitly selected
`elisac-stage1` only when stage1 provenance metadata and that checkout's runtime
are present. `ELISA_RUNTIME_OBJ` remains the explicit override for comparisons.

## Producer and replay results

Each source was run with the current producer's JSON mode and package mode. The
package was replayed by the separate `elisa-proof-replay` executable. “Replayed”
means the kernel checked every emitted theorem in the package; the package trust
metadata still reports adapter-provided hypotheses/source correspondence and
`source_authenticated: false`.

| Source (SHA-256) | Producer result | Independent package replay |
| --- | --- | --- |
| `src/studio/timeline_goto_draft_policy.elisa` (`f3b70645df9888a1b83d45c5f555ee706951acbf5863a59e2626c60cbf05ea4d`) | 16/16 proven; 16 certificates | replayed 16/16 |
| `proof/studio_timeline_goto_policy_laws.elisa` (`b24576a22c453f9121808ff3b35c4687a56e0a316a69edbe9c3ce956fa1231fe`) | 14/14 proven; 14 certificates | replayed 14/14 |
| `proof/studio_timeline_goto_draft_laws.elisa` (`e7f8d4709cd0f67b408f4c111584894ba6d8cb8ee14500b407a30496003df3a0`) | 25/30 proven; 5 unknown refusal-gate obligations; 25 certificates | replayed 25/25 |
| `proof/studio_timeline_goto_focus_laws.elisa` (`2245f5edc86d0020c647b66fce8ba31d73bdfa87a773fc2d710c6b94d2097a3e`) | 20/37 proven; 17 unknown/unsupported obligations; 20 certificates | replayed 20/20 |
| `proof/studio_timeline_goto_input_laws.elisa` (`5c2477796bfc53528f53ef848b2f703be1cea581e863ebbe61165a8c2a1e9e89`) | 28/28 proven; 28 certificates | replayed 28/28 |
| `proof/studio_timeline_navigation_laws.elisa` (`acfe74db05add211e6d7f9112c3bc2cebc98eabf4b3b1b9e3bcd8d8510752e81`) | 49/74 proven; 25 timeout/unknown/unsupported obligations; 49 certificates | replayed 49/49 |
| `proof/studio_timeline_time_input_laws.elisa` (`56aa78b0ef193b7e2d0fb2a70885303a9a943ee4521c62cb9c9524e5cbfb2371`) | 34/59 proven; 22 findings; 37 certificates, 34 internal replays and 3 gaps | package export rejected as `source-inadmissible`; standalone replay rejected the package |

## Fail-closed boundaries

Three temporary direct-proof inputs in `/tmp` checked rejected multiplication
shapes. Variable-by-variable multiplication (`9ac0a098df15f1adde40e811ba700778eaa1366201f0ab5055b34aa54d90b5d7`), a negative
literal multiplier (`8b131f188c1e9962243b7b2a382a1e51bebeecd3e4968bfeead94b9e97c3dad7`),
and positive-literal multiplication with possible overflow
(`85f7ad0a3cc12ce28cd4d2b797c19cbe8823df8564f7751895f828a277c5252f`) each
left the target obligation unknown with refusal gate `wrap-guard-fact`. These
were diagnostic proof inputs, not executable tests.

This focused qualification does not establish that the complete corpus passes.
The last full check used older products and a changing source tree; it exited
nonzero and is comparison evidence only. A fresh full check still needs a stable
source snapshot and current matching products.

## Time and clock law follow-up

The same generation was also run against the current time, entry, clock, and
navigation law files. These are live-source observations; the pair manifests
identify the compiler and prover binaries above, while the source hashes below
identify the exact app files read for each report. The package reader correctly
refused every source that had internal replay gaps.

| Source (SHA-256) | Producer report | Independent replay |
| --- | --- | --- |
| `proof/studio_timeline_time_input_laws.elisa` (`56aa78b0ef193b7e2d0fb2a70885303a9a943ee4521c62cb9c9524e5cbfb2371`) | 59 obligations; 34 proven; 22 findings; 37 certificates, 34 replayed, 3 gaps | rejected `source-inadmissible` |
| `proof/studio_timeline_entry_laws.elisa` (`4ac3f82ba8dbead81c0a7f060136666cae1df09a03dfa7b1d989679688ac0df6`) | 54 obligations; 39 proven; 11 findings; 43 certificates, 39 replayed, 4 gaps | rejected `source-inadmissible` |
| `proof/studio_timeline_clock_laws.elisa` (`142e657751ff1e39040c5bb2ed1d647e4d1a6fee4c6d769aa1e0d3cc99507ee4`) | 56 obligations; 22 proven; 32 findings; 24 certificates, 22 replayed, 2 gaps | rejected `source-inadmissible` |
| `proof/studio_timeline_rational_clock_laws.elisa` (`919d2481399518a763263deb68f7acc5a44d919d2da38c99ec16d1aa30dcffce`) | 39 obligations; 12 proven; 25 findings; 14 certificates, 12 replayed, 2 gaps | rejected `source-inadmissible` |
| `proof/studio_timeline_goto_input_laws.elisa` (`5c2477796bfc53528f53ef848b2f703be1cea581e863ebbe61165a8c2a1e9e89`) | 28/28 proven; 28 certificates, all internally replayed | replayed 28/28 |
| `proof/studio_timeline_goto_focus_laws.elisa` (`2245f5edc86d0020c647b66fce8ba31d73bdfa87a773fc2d710c6b94d2097a3e`) | 20/37 proven; 17 unsupported/unknown; 20 certificates, all internally replayed | replayed 20/20 |
| `proof/studio_timeline_navigation_laws.elisa` (`acfe74db05add211e6d7f9112c3bc2cebc98eabf4b3b1b9e3bcd8d8510752e81`) | 49/74 proven; 25 unsupported/unknown; 49 certificates, all internally replayed | replayed 49/49 |

The time-input gaps are `seconds_digit` (line 20), `milliseconds` (line 36),
and `frame` (line 51). Entry laws inherit those three and add `capacity`
(line 169). The two clock report gaps are both `rate_valid` obligations in the
included rational clock policy. Thus the time and clock packages remain
inadmissible; the producer's partial proofs and the standalone replay of other
admissible law files do not clear these gaps. This is not a full corpus result.
