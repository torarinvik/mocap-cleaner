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

## Latest performance compiler: 0fb79267

Fetched upstream `96761822e6469efb929c5d50a804bb765f6bc3f7` contains the
new performance work. Merge `0fb7926798d867f456ef15675611ed35476547b8`
preserves project repairs in `../Elisa-compiler-m5-numeric-call-lowering`.
Fresh optimized Stage1 and runtime builds completed successfully; provenance
checks passed before and after the project compile below. Stage1 SHA-256 is
`0e49ff4092572c8e9f81ee68d0443d0ac3d7e8209d709663e92ee4d578061fb0`;
runtime SHA-256 remains
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
The first seed hit its 6 GiB RSS guard; the successful retry used a 10 GiB
limit on the 24 GiB host, retaining O3 optimization. Logs are in the compiler's
`build/latest-seed-20261007*.log`.

The 21 creation-journal laws compiled at O0 after correcting their precondition
keyword and multiline parentheses in `9dd3c12`: exit 0, 73,472-byte object,
0.17 seconds wall time. This is not a comparative speed benchmark, executable
test or authenticated proof. Source/product/object hashes and the platform
recipe hash are in `build/latest-compiler-qualification/evidence.json`.

Select this compiler with `ELISA_STAGE1=../Elisa-compiler-m5-numeric-call-lowering`.
Both CLI build and check entry points now derive their default compiler wrapper
from that selection (`fc593fd`); Studio already honors it. Earlier compiler
results are comparison evidence. The current full app and paired prover must
be rebuilt/qualified against this compiler before accepting those deliverables.

### Owner-local `view` collision repair

Compiler revision `e34f2c0656aac1232ad72da6516c7eb89f866a47` preserves
same-owner nongeneric call resolution before generic return inference. The
Studio `view(i)` call previously entered imported generic template slot 75,
inferred zero generic arguments and became Unmodeled before the owner-local
return scan. Temporary tracing has been removed and the compiler checkout is
clean at this revision.

The fresh product SHA256 is
`b2e4d197df34892b4f7a43a5ff751aecd6c95c08a998783c5687548f50559ae1`;
runtime object SHA256 is
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
The app-unit compile succeeds, producing `build/view-narrowing-current/app.fixed.o`
with SHA256 `9a07b1bd4fb20ae39c5f4dfef2b4f2d6672e8db9ef764a3b26817d2466f666b5`
and an empty diagnostic log. This is app-unit compilation evidence, not full
build, native linkage, runtime or proof qualification.

The sourced `scripts/platform.sh` SHA256 is
`eedfa210c0cb8d34741f4aae87b50a11d548cb8c1bf2b83ba820fc1012257b16`.
It remains an explicitly captured extra recipe input while the compiler's
provenance recipe omits this newly sourced script. Full current Studio and
proof-pair qualification are in progress and must retain that distinction.

### Complete Studio build at the repaired compiler snapshot

The full `scripts/build_studio.sh` invocation with `STUDIO_SKIP_CHECKS=1`
completed successfully: main-unit compilation, native linking, source snapshot
recheck, product seal, executable publication and app packaging. The generation
is `build/studio-build.PNkqnW`; its input record SHA256 is
`4d7c3fcbb3c6c95125749465a5f894a38bb17161fd781348e9a7b39e03f8a67d`
and input inventory SHA256 is
`f379d483991c0175fa31dcf504c9f71854bc375ee0f0cd1006e5375702a6ca0c`.
Main object SHA256 is
`4470da305105babae43553bbfc04b250e71fec44c78f26edc6df0bce789eca53`;
executable SHA256 is
`1bfb7ca42058646413ee8bc3cc081b0053aa68fa58f66ffba91b2af781801b7d`.
Selected engine revision is `c52023cea002f8295f72d0b304ed1f5743cc10e5`.
The UI's selected HEAD is `f33e439b3dc25eb28bb62b282128c0b0c9d6838a`
with dirty inputs captured before/after; the snapshot check passed.

This run did not execute checks, prove laws or establish native interaction.
The new cleanup transaction/controller is outside the app input closure and
its reduced-unit backend declines remain open. Dependency integration with
fetched engine upstream remains open. Newly added package verifier code has
not been exercised by this earlier build and is not yet wired into packaging.
