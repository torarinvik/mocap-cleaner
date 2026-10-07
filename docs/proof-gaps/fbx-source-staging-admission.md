# FBX source and staging admission proof boundary (2026-10-07)

## Paired evidence

The focused laws were evaluated with the current matched proof pair
`3fcd655ba5d043989419af8699c6e60c` (producer SHA-256
`6961f2be6941373848e31b690624b657ccba583c9e569c83145086f2c6f20b77`, replay
SHA-256 `973d99db5197fe7454b9d3891542c416e42c5233f672c304cd059cda87acf85`).
It uses compiler revision `bb274b14d139b298b78e7df90a0b478aa8b0f0fc`,
Stage1 SHA-256
`36389f6b18268d4266bd68aacd813c703cd788956b611b9fad9964da11a2aa32`, and
runtime SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
Pair integrity and the primary freshness check passed for that product tuple.

The focused producer reports are retained under
`../elisa-proof-mocap-owner-aware/build/current-pair-source-auth/`:

- Take source reference: 63 obligations, 19 proven, 44 unproven, 27 findings.
- FBX staging evidence, after replacing a mutable digest fixture with an
  immutable literal: 135 obligations, 16 proven, 119 unproven, 115 findings,
  14 warnings and no semantic errors.
- Both packages are source-inadmissible and unauthenticated. Their replay
  results are rejected; correspondence reports zero checked obligations.

The exact current source SHA-256 values are:

- `src/studio/take_source_ref_policy.elisa`:
  `1bc161137ba53450ece2788ab60684fc25466271564c93da20895739eb656a3d`.
- `proof/studio_take_source_ref_policy_laws.elisa`:
  `968b82f3a2f85695a73c64591cdd8e5f83fd91bda1a08390cb792c269e4f577d`.
- `src/studio/fbx_staging_evidence_policy.elisa`:
  `6629e3b6b4fcac6254f04311dced65ca1561dd36d133ca0ca146bd660be04a26`.
- `proof/studio_fbx_staging_evidence_policy_laws.elisa`:
  `3e947a1e48465180a963eb7f6889e20ff3050ff904816ddfbd3c13b123de07ea`.

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
