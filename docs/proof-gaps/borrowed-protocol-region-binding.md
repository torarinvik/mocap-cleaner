# Borrowed standard-library and protocol region binding

## Current evidence

The current proof CLI rebuild has not produced a qualified product. Its std
graph exposed borrowed deque/packed-store APIs whose region-less return
signatures do not express the owner lifetime. Scoped explicit region ties
expose additional caller-propagation and protocol-conformance requirements.

Compile-only reductions under the immutable `22cf6e5b` Studio generation show:

- A borrowed field returned through an unannotated owner reproduces the
  region-less-return error. A tied owner and return compile.
- Generic indexed and optional borrowed returns compile with explicit ties.
- A mutable indexed borrow can be narrowed to the existing readonly API with
  a typed cast; returning function-local storage as a caller lifetime refuses
  emission in the negative reduction.
- A tied implementation and tied direct use compile in a Stage1 protocol
  reduction. The Go Stage0 conformance checker nevertheless requires exact
  region-parameter/return-region equality with the unannotated protocol shape.
- An earlier protocol syntax reduction refused annotation; the subsequent
  current Go repair uses an explicitly tied Store declaration. The earlier
  refusal does not describe the repaired source.

Current Go repair `91be03e0` canonicalizes the specialized protocol container
borrow using the same container-region stamping as source type resolution.
Previously, `Self& @r` retained its region on the outer reference after
substitution, while source `darray[T]& @r` stored it on the container. This
representation mismatch declined the correctly tied darray implementation.
The fresh committed Go build passes its provenance check. A compile-only
generic protocol dispatch reduction now passes; a wrong-owner return refuses
with region escape and `@b` versus `@a` diagnostics. These artifacts are in
the compiler worker's `build/borrowed-return-reductions/protocol-current/`.
Stage1 seed attempt 5 was terminated by the wrapper's RSS guard at 6463088 KB
against a 6291456 KB limit. Its log reported no terminal semantic decline and
it emitted no new product. Attempt 6 also used the default guard because the
override named the runtime limit rather than the seed limit. Attempt 7 used
the correct 10 GiB seed limit and exposed the Stage1 parser scanner treating
`@r` inside a method signature as a leading decorator.

Attempt 8, with the line-boundary scanner repair, completed with exit 0.
Compiler/std repairs are committed as `d2754a8eebfeaffbe137ed9201afdeb21735a29b`;
the built source-tree hash remained unchanged when the commit was recorded.
Freshness and source/product provenance checks pass. Product SHA-256:
`0da393abce7e82920db3560cd15aed93642c23df6d185099011caea1aeb0a740`.
Runtime object SHA-256:
`d6f6e22e02740dfdf3a2d1461660e726a9ea5ef211a4ddda29b14ef5329dc9f3`.
The prover pin advanced to that compiler in proof commit `03d515d4`. That
complete CLI build failed; retained diagnostics required borrowed-return
repairs and correction of runtime source attribution. No current pair was
qualified by that run.

Stage1 interface emission accepts the generic darray protocol positive and
preserves tied signatures. Direct non-generic wrong-owner and function-local
escape negatives refuse. An uninstantiated generic wrong-owner function is
still accepted by interface emission; concrete generic object-call reductions
decline before useful lifetime diagnostics. Stage0 rejects that generic
wrong-owner body, but this does not qualify Stage1 generic call-site safety.
Complete that negative and concrete dispatch code generation before closing
the protocol gap.

These reductions do not establish full std compatibility, sound interface
dispatch, proof authentication or runtime ownership. Failed seed attempts
cannot qualify their source, even when they emitted an intermediate product.

## Required repair and qualification

Preserve readonly deque return types and independent arena/row lifetimes.
Propagate state-owned ties through packed-store forwarding callers without
tying unrelated borrows together. A protocol conformance refinement must
retain the implementation's parameter-to-return owner relation at actual
interface call sites; erasing syntax for signature comparison must not erase
the lifetime rule from type checking.

Compile direct and protocol-dispatched positive calls, local-owner escape,
different-owner, mutability and signature negatives. Inspect refusal before
LLVM emission. Rebuild from current Go source preserving upstream/local
repairs, then rebuild the exact compiler/std/runtime and proof CLI pair.
Check complete source/product provenance before running authenticated proofs
and the authorized full check. This remains an open toolchain gate.

## Isolated bootstrap local-borrow inference (2026-10-07)

Small sources under `build/region-inference-reduction/` distinguish a
current seed failure from generic protocol conformance. The clean detached
Go bootstrap at source `4a68f508` has product SHA-256
`c62c72051b37a02a48a87c4ddcd6a158c9133dc14b6a6833aa036df003e87bc7`.
Each source was compiled directly with `-emit obj -O0`; no executable ran.

| Source | Case | Terminal outcome |
| --- | --- | --- |
| `input.elisa` | A local mutable `Box` is passed as `&local` to `borrowed[@r](box: Box& @r) -> Box& @r`. | Refused: cannot infer region parameter `r`; no object. |
| `plain.elisa` | The same local is passed to `measure(box: Box&) -> i64`. | Exit 0; 568-byte object. |
| `forward.elisa` | An explicitly tied caller parameter is forwarded to the tied `borrowed` helper. | Exit 0; 456-byte object. |

Source SHA-256 values, in the table's order:

- `691a61bf8a17f6121d83ee9b907f99742dfa343f46243e327a9eb159b12c568c`
- `24086b893de358b9a74b5ca5f920c3640a1396796c6380cb71692cd7b1b968b4`
- `6f2f88ef443a517316c1aa03c36fb79d363456a7b6139513d58f7fe5b599aa94`

Further reduction narrows the actionable case to copying a container-bearing
record. Scalar-only record region inference may reflect a value-shape rule;
do not change lifetime validation solely to admit that first reduction.

| Additional source | Case | Terminal outcome |
| --- | --- | --- |
| `container.elisa` | `Box` has an empty `darray[i64]` field; borrow the freshly constructed local. | Exit 0; 608-byte object. |
| `copied-container.elisa` | Same fields and borrow, but initialize `seed` from the literal and `local` from `seed`. | Refused: cannot infer region `r`; no object. |
| `named.elisa` | Explicit named region annotation on the scalar-only record local. | Refused: named values do not carry an independent region; inference also fails. |

Additional source SHA-256 values, in that table's order:

- `721676c6eb14ed331348d50acbf16ac60e41aaa26cc08d3ce815f1f0fe9dd8e5`
- `24ece343afd5ae61e154dd5756754df449997c18b30f41f4380cfd52a6ed8b8e`
- `c9d6880f4fe902f47c86e68706779a844e89b445a3e49eeef10613f7eaa3350b`

The compiler worker received these reductions. Inspect region adoption through
record copies, matching the driver's `compile_file = file` pattern, separately
from owner mismatch and interface conformance. Do not add artificial container
fields or erase owner ties as a workaround. This is diagnostic evidence, not
current Stage1 or application qualification.

Inspection of the selected Go source identifies the missing path:
`semantic/region_struct_local.go::recordStructLocalAllocRegion` records fresh
struct literals and region-polymorphic builder results, but not identifier-copy
initializers. The reduction already has an ambient region from its fresh seed;
creating another ambient region is not the missing fact. A repair must propagate
the known source owner's region, rather than assume every copy belongs to the
current ambient region. Preserve the existing use-site liveness check and
reassignment invalidation. Qualify copied-local use, shorter-lived owner escape,
reassignment to a different owner, dead/destroyed regions and unknown-owner
copies separately before rebuilding the seed. The source finding has been
assigned to the compiler worker; no repaired product is established yet.

Compile-only negative reductions are prepared beside the positive copy case:
`reassigned-owner.elisa` replaces a copied local from a shorter-lived region;
`expired-owner.elisa` uses an assigned owner after that region exits; and
`copy-escape.elisa` returns a reference into the copied local. The original
`4a68f508` product refuses the first two at region inference and the last with
an explicit function-local dangling-reference diagnostic. These are baseline
comparisons only once the bootstrap source is patched. Rerun the positive and
all three negatives against the repaired, source-matched product; accepting
the copy must not turn any negative into an emitted object. No executable was
run and these reductions do not qualify the integrated compiler.
