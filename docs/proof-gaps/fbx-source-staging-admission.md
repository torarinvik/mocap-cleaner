# FBX source and staging admission proof boundary (2026-10-07)

## Historical paired evidence

The focused laws were evaluated with captured matched proof pair
`3fcd655ba5d043989419af8699c6e60c` (producer SHA-256
`6961f2be6941373848e31b690624b657ccba583c9e569c83145086f2c6f20b77`, replay
SHA-256 `973d99db5197fe7454b9d3891542c416e42c5233f672c304cd059cda87acf85`).
It uses compiler revision `bb274b14d139b298b78e7df90a0b478aa8b0f0fc`,
Stage1 SHA-256
`36389f6b18268d4266bd68aacd813c703cd788956b611b9fad9964da11a2aa32`, and
runtime SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
Pair integrity and the primary freshness check passed for that product tuple.
That pair records proof-tool source HEAD `2591c2583649472afb8a7480da15f908716f4448`.
The subsequent isolated replay repair commits `bcf4cbfb`, `1072e49e` and
`9729c6d9` changed proof-tool sources, so the captured pair is historical
diagnostic evidence and is not fresh for the repaired proof checkout.

The focused producer reports are retained under
`../elisa-proof-mocap-owner-aware/build/current-pair-source-auth/`:

- Take source reference: 63 obligations, 19 proven, 44 unproven, 27 findings.
- FBX staging evidence, after replacing a mutable digest fixture with an
  immutable literal: 135 obligations, 16 proven, 119 unproven, 115 findings,
  14 warnings and no semantic errors.
- Both packages are source-inadmissible and unauthenticated. Their replay
  results are rejected; correspondence reports zero checked obligations.

The source SHA-256 values at capture time were:

- `src/studio/take_source_ref_policy.elisa`:
  `1bc161137ba53450ece2788ab60684fc25466271564c93da20895739eb656a3d`.
- `proof/studio_take_source_ref_policy_laws.elisa`:
  `968b82f3a2f85695a73c64591cdd8e5f83fd91bda1a08390cb792c269e4f577d`.
- `src/studio/fbx_staging_evidence_policy.elisa`:
  `6629e3b6b4fcac6254f04311dced65ca1561dd36d133ca0ca146bd660be04a26`.
- `proof/studio_fbx_staging_evidence_policy_laws.elisa`:
  `3e947a1e48465180a963eb7f6889e20ff3050ff904816ddfbd3c13b123de07ea`.

After this capture, commit `89a4d10` changed the TakeSourceRef negative controls
to use complete literal path and digest values instead of indexed writes into
dynamically sized struct fields. Its resulting report is included below.

## Current matched-pair qualification

The current focused reports were generated after proof checkout commit
`0e7db7228fd9e6235a803525150ee94ed78ef5fc`, using matched generation
`ce0b63a0ae264349a74f818057e5c107`. Proof and replay product SHA-256 values are
`0d08a39dca5ea6b8d120afb82f779203b0b849e87e7e5e20998031bd83b486e6` and
`94b2c658fa5cd2e8acdfce00abec351df3204984d919e857e6e56bcf25ef8180`.
`verify_product_pair.py check-current` passed. The manifest records proof
source tree `cb66cbe4b308ef6a752fbbb2261e42007bed7d2febd4edfcc6aa081aea392ae3`
with a clean source pin, compiler revision
`48dc78e2ce51873a459a689b4d8bb63a1c76bd4f`, Stage1 SHA-256
`461d377b3e61307ac4a4cb46e56729d84a21c509e38ddd57f39935002abe959f`, recipe
SHA-256 `105bd840e8e6ce839d87eb77f5155a4600e33b44d102db614d9402e15d433073`,
and runtime SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.

Focused report files are under
`../elisa-proof-mocap-owner-aware/build/current-owner-summary-repair-final/`.
Each source package is admissible and all listed certificates replay, but each
package has `authenticated=false`; no producer/replay result establishes native
correspondence.

| Policy and laws | Obligations | Proven | Unproven | Replay | Correspondence |
| --- | ---: | ---: | ---: | --- | --- |
| TakeSourceRef | 59 | 34 | 25 | 34/34 | 0 checked, 30 unsupported |
| FBX staging | 117 | 21 | 96 | 21/21 | 0 checked, 38 unsupported |
| FBX refusal mapping | 43 | 26 | 17 | 26/26 | 0 checked, 4 unsupported, 1 unmatched |

The owner-aware resource-summary repair now verifies the resource bodies for
`path_valid`, `bytes_equal`, `path_bound`, `paths_bound` and
`copy_digest_bound`. The purity checker still marks these functions impure, so
`stage_admitted` has two unsupported helper calls in its contracts and 13
unproved ensures.
The `good` staging fixture still has two `region-call-opaque` findings because
its zero-argument generic `digest[@r]()` call has no argument from which to
derive the caller region. These are source-checker limitations; they do not
authenticate the native producer.

The refusal mapping policy has four open ensures in `classify` and unsupported
enum expressions in its laws. Its unknown-status rule still requires direct
qualification. Current primary policy/law SHA-256 values:

- `src/studio/take_source_ref_policy.elisa`:
  `1bc161137ba53450ece2788ab60684fc25466271564c93da20895739eb656a3d`.
- `proof/studio_take_source_ref_policy_laws.elisa`:
  `ccb719a894451dab7b00b266255adcb646c621a24eb15c060ae0c159c1de1761`.
- `src/studio/fbx_staging_evidence_policy.elisa`:
  `6629e3b6b4fcac6254f04311dced65ca1561dd36d133ca0ca146bd660be04a26`.
- `proof/studio_fbx_staging_evidence_policy_laws.elisa`:
  `d2d36122dd57e6f3a259f92c3e64a7ca26973438bb524847dc69c825e5e78930`.
- `src/studio/fbx_import_failure_policy.elisa`:
  `3c4311364c0d01d2daecc62d00f449fb5d11ac1ba6594a3861fea5e8f951491b`.
- `proof/studio_fbx_import_failure_policy_laws.elisa`:
  `013b743741ddfb817b9a186e390dff37cc134e1ca3b0645b3e11d551427c4924`.

## First remaining blockers

`StudioTakeSourceRefPolicy::valid` at source line 55 has a resource-safety
certificate rejected by replay (`kernel-replay-gap`, goal 8, kernel goal 467).
The producer's later laws consequently cannot rely on a checked summary for
that function. Several mutation laws also exceed the control-flow fact budget,
and indexed writes through dynamically sized struct fields lack a proved upper
bound.

In staging, `paths_bound` calls the borrowed-array `path_bound` helper three
times. Its producer resource-safety certificate is rejected by replay (goal
13, kernel goal 1064), and no verified summary is available for those calls.
`stage_admitted` therefore cannot use `paths_bound` and `copy_digest_bound` in
its postconditions: the producer rejects them as contract calls without a
verified total-pure summary (source lines 85 and 89). Its dependent ensures
remain unproved.

The positive fixture `good[@r]` returns an `Evidence` value containing nested
dynamic arrays and calls the region-polymorphic `digest` helper. The producer
cannot map those calls to the caller region. The digest fixture's former
mutable-array write was removed in commit `2e2f57e`; this clears that one
resource warning but does not authenticate the fixture or staging laws.

## Boundary

These Elisa predicates decide whether supplied evidence fields satisfy the
declared source, cache, path, identity, copy and durability conditions. A
checked theorem over those fields would not establish that native code actually
read or hashed the original FBX, resolved a canonical path, compared descriptor
and directory-entry identities, synced the snapshot, or left the original
unchanged. Native-to-policy correspondence remains a separate qualification
gate and is not established by the reports above.
