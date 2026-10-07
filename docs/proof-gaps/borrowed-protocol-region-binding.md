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
The prover pin advanced to that compiler in proof commit `03d515d4`; its new
complete CLI build is running and is not yet qualification evidence.

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
