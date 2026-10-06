# Batch review binding — 2026-10-07

The new exact identity and review-token law source compiled with the normal
current compiler wrapper. Command:

```sh
../Elisa-compiler/scripts/elisac_stage1.sh -o build/batch-review-binding-compile.yDG0DV/review-laws.o proof/studio_export_batch_review_binding_laws.elisa
../Elisa-compiler/scripts/elisac_stage1.sh -o build/batch-review-binding-compile.yDG0DV/source-laws.o proof/studio_export_batch_source_identity_laws.elisa
```

Both commands exited 0 and emitted nonempty fresh objects: 54,648 bytes for
review laws and 10,800 bytes for source identity laws. No executable or native
test was run. Initial compile attempts found unsupported multiline Boolean
expressions and a reserved identifier; both were corrected. This is compile
evidence only, not proof replay or native qualification.

`StudioExportBatchReviewBinding` owns the queued identity and a private-field
review token. Review issuance requires explicit review, an exact byte/scalar
match with the current identity, and an AwaitingReview item. Publication has
no caller-supplied success or destination-absence booleans. It rechecks the
source through the new no-follow identity snapshot API, reads exact staged bytes, publishes the GLB
with `commit_new_with_status`, and compares the resulting final bytes against
the reviewed bytes. It publishes JSON and text using the existing create-only
sidecar API only after the GLB verifies, then reads each sidecar back and
compares exact bytes. A private publication receipt records the observed
publication and staging cleanup results before the existing queue transition.

The engine API was committed on `mocap-track` as `e11085c1`; it resolves a
canonical path, uses `lstat`, rejects final symlinks and non-regular files, and
returns device, inode, size and nanosecond mtime or a failure code. The source
proof laws compile, but native source was not built or tested. Source races
between identity observation and publication, recovery after partial report
writes, durability outcomes, preflight path/recipe/rig facts, proof replay, and
UI review wiring remain unqualified. The separate preflight policy still
accepts facts that its caller must establish from the OS.
