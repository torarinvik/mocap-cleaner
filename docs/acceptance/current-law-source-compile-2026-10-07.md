# Recent law source compilation (2026-10-07)

Eleven recent law graphs compile at O0 with the matched repaired compiler
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
