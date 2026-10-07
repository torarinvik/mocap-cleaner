# Generated build cleanup FFI boundary

This inventory describes the current C ABI between `src/studio/io` and
`../elisa-engine-mocap/native`. It does not claim that missing native pointer
extents are checked by Elisa.

## Calling convention and scalar types

All listed exports use the C calling convention and return an `int32_t` status.
The Elisa declarations keep each C `uint32_t` capacity as `u32`; those values
must not be widened to `usize` without changing the C ABI. The current Elisa
compiler's `@bounds` attribute consumes the pointer/capacity pair and supplies
the capacity from the bounded view, whose C ABI uses `usize`. It therefore
cannot annotate these existing `u32` pairs without changing the ABI. Device and inode
arguments on move admission are `uint64_t`; native handles, revisions, ages,
counts, receipt sizes and status phases use their declared `int64_t`, `int32_t`
or enum-compatible widths.

## Trash transaction exports

The current header declares 11 exports in
`studio_build_generation_trash_appkit.h`:

| Export | Pointer extent and lifetime |
| --- | --- |
| `elisa_studio_build_trash_begin_move` | Reads four NUL-terminated input strings; writes one scalar to each out pointer and at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_persist_move_intent` | Writes at most `operation_id_capacity` bytes to the ID buffer, scalar facts, and at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_commit_move` | Writes at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_abort_move` | Writes at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_begin_restore` | Reads root and operation ID C strings; writes scalar facts, at most `artifact_id_capacity`, `relative_path_capacity`, and `error_capacity` bytes to their buffers. |
| `elisa_studio_build_trash_persist_restore_intent` | Writes one receipt-size scalar and at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_commit_restore` | Writes at most `error_capacity` bytes to `error`. |
| `elisa_studio_build_trash_reconcile` | Reads root and operation ID C strings; writes two scalar facts, bounded ID/path buffers, and bounded error text. |
| `elisa_studio_build_trash_close` | Consumes an opaque integer handle; no caller buffer. |
| `elisa_studio_build_trash_receipt_scope` | Reads an opaque handle and writes one `int32_t` scalar. |
| `elisa_studio_build_trash_validate_reviewed` | Reads four digest C strings and writes bounded error text. |

Native calls do not retain caller pointers after return. An acquired integer
handle indexes native-owned transaction state, descriptors and locks; it is
not a retained pointer. `close` releases that native state, and uncertain
release status remains represented by the Elisa owner.

## Candidate snapshot exports

The current header declares four exports in
`studio_build_generation_candidate_provider_appkit.h`:

| Export | Pointer extent and lifetime |
| --- | --- |
| `elisa_studio_build_candidates_open` | Reads a NUL-terminated build-root string; writes one snapshot token, outcome/count/refusal scalars, and at most `error_capacity` bytes. |
| `elisa_studio_build_candidates_row` | Writes scalar row facts; artifact ID, relative path and error are bounded by their `uint32_t` capacities. The eight digest outputs are fixed 65-byte buffers in the C implementation and have no capacity argument in this ABI. |
| `elisa_studio_build_candidates_incomplete` | Writes six scalar facts from the immutable snapshot row; it has no character buffers. |
| `elisa_studio_build_candidates_close` | Consumes the snapshot token and releases its native snapshot slot. |

The snapshot slot owns copied row values; filesystem locks are released before
`open` returns. It retains no caller pointer. A snapshot token is still a
resource that must be closed exactly once.

## Recovery discovery export

`elisa_studio_build_recovery_discover` in
`studio_build_generation_recovery_discovery_appkit.h` reads a NUL-terminated
root string, writes at most `capacity` bytes of ID hints, and writes count and
pending-record scalars. The current native contract uses 512 rows with a
39-byte stride (`19,968` bytes total); the final byte of every row is NUL.
These are hints only. The per-operation reconcile call remains authoritative.
No caller pointer is retained.

## Extent gaps requiring an additive bridge

The current C ABI has no explicit length for input C strings and no capacity
argument for scalar out pointers or the eight fixed-size candidate digest
buffers. The Elisa adapters validate their own fixed request arrays and pass
the C strings synchronously; native code also performs bounded string checks.
Those facts do not provide a compiler-enforced extent on the raw FFI call.
The paired output pointers are not yet compiler-bounded. Existing adapter
buffers and native capacity checks are runtime safeguards, not FFI type-level
extent contracts.

To bind all extents without changing the existing ABI, an additive C bridge
should accept bounded views using the compiler's `usize` view convention and
validate/convert lengths before delegating to the existing `uint32_t` entry
points. It should expose scalar and fixed-size digest outputs as bounded
records or explicit capacities and retain no pointer. Until that bridge is
implemented and registered, input strings, paired output pointers, scalar
outputs, and fixed-digest outputs remain an open FFI qualification gap.
