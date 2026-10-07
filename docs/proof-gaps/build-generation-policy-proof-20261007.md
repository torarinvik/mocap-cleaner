# Build generation policy proof and replay (2026-10-07)

Status: the producer/replay products passed integrity and dependency freshness
checks. The policy law graph is incomplete and source correspondence is not
established. Replaying its 33 emitted theorems does not qualify the source
snapshot. This is focused evidence, not a full-corpus or application
qualification.

## Current tool pair

The proof repository pin was advanced in `b7f10b234f63cd19407ba3d5ce8ccdf608ace098`
to compiler commit `9667344cf0fd2e955a4e233ada1ea60033a16837`. The all-products
build completed with exit 0 and published generation
`ef1317585270400a8aa51deeb92ed517`. `verify_product_pair.py check-current` and
`scripts/check_prover_freshness.py` both exited 0.

The prover binary SHA-256 is
`0a4ad84b087eede626005f95fc05b344cdb87afee6c2b3c6b6770bd692745934`; its
manifest SHA-256 is
`7991ad918cd94ae281c9403e5e3cb6b9cc73f0007a7e7135c6444779b4b6f9d3`.
The independent replay binary SHA-256 is
`caa9533988aab8337b8c8893dd257c4fe1bbd01de9fb67a358359f8f571df169`; its
manifest SHA-256 is
`5fe743de86de47471ac4732356077e2b78fcc22277514bc17af51b5715ba0ab5`.
Both manifests record strict O2 builds from proof HEAD
`b7f10b234f63cd19407ba3d5ce8ccdf608ace098`, compiler product SHA-256
`bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b`, runtime
SHA-256 `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`,
and compiler source tree SHA-256
`0c654d0bb8e9c564fa3cdfa33116e96b0a442da0881a56037a75b47bf1897dcb`.

## Focused law result

The inspected source pair was:

- `src/studio/build_generation_policy.elisa`, SHA-256
  `7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`.
- `proof/studio_build_generation_policy_laws.elisa`, SHA-256
  `2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e`.

The producer's `--json` report exited 1 with status `failed` and verification
state `unsupported`: 89 obligations, 33 proven, 56 unproven, 45 findings, and
no semantic errors. `protection_reason` and `eligible` exceed the control-flow
fact snapshot limit (1875 and 421 facts, respectively; limit 128). Calls from
`may_cleanup` to `eligible` are unsupported and leave its executable summary
unverified; dependent ensures remain unknown. Other law ensures are unknown
under connective, non-comparison, or ambiguous-constant refusal gates.

The package contained 33 theorems. The standalone replay returned exit 0 with
status `replayed`: 33/33 replayed, zero rejected. Its trust record correctly
states `source_authenticated: false`; package replay does not establish that
the theorem statements are obligations of the source.

The producer's independent `--correspondence` check returned exit 1. It found
an exact source identity and `source_admissible: true`, but reported
`source_authenticated: false`, 0 checked obligations, 0 unmatched obligations,
and 22 unsupported functions. Initial refusals are `parameter-type` for
`facts_valid` and `eligible`, and `return-type` for `protection_reason`, which
use struct and enum types. No source authentication claim follows from this
run.

Retained JSON is in the proof checkout at
`build/focused-qualification-9667344/` (`build-generation-policy.report.json`,
`.package.json`, `.replay.json`, and `.correspondence.json`). The full
`scripts/check.sh` run remains pending the parent task's source freeze.
