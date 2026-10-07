# Studio runtime source selection

The current-context viewport reduction ended without an object. Its source
closure included runtime declarations from both `Elisa-compiler` and the
historical `Elisa-compiler-m5-runtime-origin`. Duplicate std declarations and
dependent errors prevent attributing its later diagnostics to viewport
ownership. The log is `build/view-camera-reduction/actual-context.log`.
The Go bootstrap comparison failed while parsing current app syntax and
provides no evidence about the relevant Stage1 semantics.

Both Studio workers now include `build/generated/studio_runtime.elisa`.
The normal build-identity generation step writes that bridge from the exact
configured compiler's runtime source. Snapshot/check modes require the bridge
to match that selection and refuse any runtime source in the expanded closure
that resolves outside the selected compiler. Thus an `ELISA_STAGE1` override
selects declarations and the linked runtime together.

Generation and source snapshot creation pass with the matched compiler
`d2754a8e`. The closure record is
`build/view-camera-reduction/runtime-unified-inputs.json`. This establishes
source selection only: the complete app has not yet compiled or run with it.
Current UI/controller changes require a new immutable generation before
qualification. Regenerate identity/bridge files inside that generation so
absolute include paths refer to its copied compiler, then retain the expanded
closure and source/product manifests through compilation and linking.

## Proof build runtime attribution mismatch (2026-10-07)

The retained proof CLI build against `d2754a8e` also reported raw concurrency
refusals inside copied runtime sources. Source inspection identifies a separate
path mismatch that must be resolved before treating those refusals as compiler
semantic defects:

- The proof build's `scripts/compiler_snapshot.sh` exports pinned compiler
  sources into `build/snapshot/Elisa-compiler`, including `elisacore_std`.
- The copied proof `src/main.elisa` includes that adjacent exported std.
- The selected original compiler's `scripts/elisac_stage1.sh` unconditionally
  sets `ELISA_STAGE1_RUNTIME_STD_ROOT` to its own checkout's `elisacore_std`.
- `Lexer::source_line_is_runtime_std_from_map` grants runtime attribution only
  when the mapped source path has that exact root prefix and a path separator.

Identical source bytes do not make these different paths match. This explains
why the copied runtime can lose its runtime attribution; it does not establish
that every retained diagnostic has this cause. Borrowed-return diagnostics
require independent owner-region repairs.

The next proof build must align its selected runtime source paths and trusted
root through a provenance-checked compiler snapshot or validated root selection.
Keep the scanner's per-source checks intact. Retain the expanded paths, selected
environment, source hashes, product hashes and terminal build log. Then rebuild
both prover and replay products and authenticate their pair before replaying app
laws. No proof or native acceptance is claimed by this inspection.

The proof build now has a fail-closed selector in `elisa-proof-mocap`: it checks
the selected Stage1 provenance against the imported frontend pin, requires the
snapshot `.rev` to match that product, and recomputes the snapshot `src` plus
`elisacore_std` digest against the product's recorded source-tree digest. It then
exports the snapshot's `elisacore_std` path as
`ELISA_STAGE1_RUNTIME_STD_ROOT`; a conflicting caller-supplied path is rejected.
The build rechecks this source identity before object-identity capture, each
compiler launch, and sealing boundaries, including cache reuse. The legacy
blanket `ELISA_STAGE1_RUNTIME_STD` flag is unset, so per-source scanner checks
remain active. The selected path is part of the effective compiler environment
and therefore the build identity. A byte-digest check of the retained `d2754a8e` snapshot
matched its recorded source-tree hash, but the current candidate checkout has
advanced beyond that product, so full provenance validation and a paired build
are pending. The compiler wrapper must preserve this explicit selection only
after validating it against the selected product provenance; until that wrapper
change is available in a matching Stage1 product, no build may qualify it.
