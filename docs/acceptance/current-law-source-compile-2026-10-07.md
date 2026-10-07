# Recent law source compilation (2026-10-07)

## Earlier batch: compiler d2754a8e

Eleven law graphs compiled at O0 with the matched repaired compiler
`d2754a8eebfeaffbe137ed9201afdeb21735a29b`. All produced nonempty objects.
The 87-file transitive source closure was copied before compilation; original
hashes matched before/after copying, and copied hashes matched after compiling.
Compiler provenance and the selected product hash were checked before and
after the batch. No executable tests or authenticated proofs ran here.

Artifacts: `build/current-law-compile-d2754a8e/inputs.json`, frozen `inputs/`,
`results.json`, individual logs and objects.

| Graph | Object bytes |
|---|---:|
| storage_range_laws | 10248 |
| correction_identity_laws | 812520 |
| correction_transform_laws | 816224 |
| correction_output_laws | 809720 |
| correction_scope_policy_laws | 49688 |
| studio_restore_capacity_laws | 1401448 |
| session_authored_record_laws | 2177608 |
| session_authored_value_laws | 344280 |
| session_line_laws | 8680 |
| session_issue_annotation_laws | 47784 |
| studio_session_constant_domain_laws | 2197992 |

The initial copied-wrapper invocation refused before compilation because its
snapshot omitted `process_rss.sh`; those logs are preserved as
`*.wrapper-preflight.log`. The successful batch used the complete original
wrapper and the same source/product-matched compiler. Studio input snapshots
now include the RSS, seed and freshness helper scripts that the wrapper loads.
Future runnable compiler copies must retain them as well.

This is source compatibility evidence. Authenticated IEEE/integer proof replay,
complete app compilation, native refusal/undo behavior and corpus quality gates
remain open. No milestone closes on these object files.

## Generation cleanup policy: compiler 9667344c

The expanded `proof/studio_build_generation_policy_laws.elisa` at primary
commit `ab94857` compiled through the selected compiler wrapper with exit 0.
The object is 35,024 bytes. Eight added laws cover inclusive retention, changed
identity, symlinks, paths outside build, unverified manifests, invalid age/size,
and active/current protection despite complete selection/review/confirmation.

Command from the repository root:

```sh
../Elisa-compiler-m5-numeric-call-lowering/scripts/elisac_stage1.sh \
  -emit obj -o build/generation-policy-qualification/laws-966.o \
  proof/studio_build_generation_policy_laws.elisa
```

The retained log is `build/generation-policy-qualification/compile-966.log`.
Compiler source revision: `9667344cf0fd2e955a4e233ada1ea60033a16837`.

| Input/product | SHA-256 |
| --- | --- |
| Policy source | `7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7` |
| Law source | `2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e` |
| Law object | `d53d8180d70c77319a65a7deed536b1bfa40b8f0d77b868fa2f1251bf7604aa7` |
| Stage1 product | `bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b` |
| Runtime product | `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee` |

This narrow compile used the working-tree sources, without a copied snapshot.
It does not qualify lease acquisition, filesystem identity, directory moves,
receipt durability or Restore. Authenticated proof replay remains pending.
The earlier d2754a8e batch is comparison evidence relative to this compiler.

## Layout, truncation and creation laws: compiler cc657038

The latest source-matched Stage1 product is
`424fa9a82f6c0049bec123cec1786d36d32ca1fee874f27364d59c35886fbc23`, built
from `cc6570385d30090d0faa4e64a8f130f446764cec`. Before/after provenance
checks passed. Three working-tree O0 law graphs compiled with exit 0:

| Graph | Laws | Object bytes |
| --- | ---: | ---: |
| Storage footer layout | 8 | 14016 |
| Text truncation | 4 | 7320 |
| Incomplete generation creation admission | 16 | 53192 |

Seven source hashes and all object hashes are retained in
`build/storage-layout-qualification/cc657038/source-object-evidence.json`.
These are compile-only records, without executable tests, authenticated proof
or a copied transitive closure. Native creation journals and cleanup controller
integration remain open. All earlier compiler batches above are comparison
evidence relative to this compiler revision.
