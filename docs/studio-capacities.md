# Studio and GLB capacity inventory

Updated 2026-10-05. This is a source audit for M0, not a claim that the
limits have all been stress-tested. “Configured limit” means a constant or
fixed array in the named source. “Observed behavior” records only behavior
demonstrated by a focused test or explicit branch in the current code. Where
there is no boundary test, the behavior remains an M0 verification task.

## Document and timeline limits

| Resource | Configured limit | Source and behavior | Boundary evidence |
|---|---:|---|---|
| GLB file bytes | 2,147,483,648 bytes (2 GiB) | `../elisa-engine-mocap/src/assets/glb_document.elisa` (`MAX_BYTES`); the parsed byte count above the limit raises `GlbDocumentError.Capacity`. CLI maps this to “input exceeds the supported GLB size or data capacity”. | The GLB fixture suite exercises malformed and valid small files; an actual near-limit allocation was not located. At-limit/over-limit stress evidence is open. |
| GLB document nodes | 65,536 | Same `glb_document.elisa` (`MAX_NODES`); node arrays larger than the limit raise `Capacity`. This is the file-format document-node ceiling, not the number of mapped/usable mocap joints. | Existing GLB tests prove a two-node fixture loads and include an error-code mapping for `Capacity`; a generated 65,536/65,537-node pair was not located. |
| GLB animations | No separate animation-count constant found | Animation, channel, track and value tables are dynamically sized; the document byte cap, JSON parser limits and available memory bound them indirectly. No supported maximum animation count is currently documented. | Exact/over-limit behavior is undefined as a product guarantee. Establish a safe practical import budget and user-facing explanation in M2. |
| JSON nesting | 64 levels | `../elisa-engine-mocap/src/assets/gltf_json_index.elisa` (`MAX_DEPTH`). | Import-boundary cases should be listed with M2 malformed and oversized-input evidence; no exact depth-boundary fixture confirmed in this audit. |
| Timeline frames | 10,000,000 | `src/studio/timeline.elisa` (`MAX_FRAMES`); `TimelineState::create` and `safe` clamp counts into 1…10,000,000. | Timeline policy has proof laws; exact end-to-end studio behavior at 10,000,000 and rejection/limiting above it has not been visually exercised. |
| Foot/contact/performance-cache frames | 1,000,000 | `src/studio/foot_policy.elisa`, `src/studio/contact_editor.elisa` and `src/core/perf_cache.elisa` each define this bound. Contact edits reject invalid frames; foot policy and cache operations require their supported range. | This is a feature ceiling below the overall timeline ceiling. M0/M5 must verify a 1,000,001-frame clip remains understandable and that unsupported contact/foot actions explain the limit rather than silently appearing successful. |
| Performance-cache tracks | 65,536 | `src/core/perf_cache.elisa` (`MAX_TRACKS`); per-track four-component cache slots. | Pure policy proofs cover slot arithmetic; cache allocation and graceful fallback at/above the limit need an integration fixture. |
| Rig solver bones | 256 | `src/core/gate.elisa` (`MAX_BONES`). The GLB can contain more nodes; solver role mapping and eligible bones are a separate bounded subset. | Prover/tests cover gate logic, but a dense rig import and visible explanation for unmapped/unsupported joints remains open. |

## Editing and interaction limits

| Resource | Configured limit | Source and behavior | Boundary evidence |
|---|---:|---|---|
| Cleanup operations | 16 | `src/studio/stack_policy.elisa` (`MAX_OPS`) and fixed `StackState::Stack.ops[16]`. `StackPolicy::can_add` returns false when the stack is full. | Operation policy proof exists. Verify the UI disables or explains Add at 16 and still permits inspect, reorder, edit, bypass and removal. |
| Keyed corrections | 16 | `src/ops/corrections.elisa` (`MAX`) and `StackState::Stack.fixes[16]`. | No user-facing correction-capacity message was confirmed during this source audit. Verify full, undo and redo behavior in M4. |
| Authored contact intervals | 32 total records per stack | `src/studio/contact_editor.elisa` (`MAX_EDITS`) and `StackState::Stack.edits[32]`; this is shared across left/right feet and hands. Add/split/reset reject operations that cannot fit; split/reset build a temporary array before committing. | Contact editor laws/tests exist for interval operations. Exact UI behavior at 31/32/33, including atomic rejection and understandable feedback, remains open. |
| Retime bands | 8 | `StackState::MAX_BANDS` and fixed `bands[8]`; additions reject a full list. | Studio retime tests cover normal interval behavior; verify full-capacity feedback, undo and session round-trip. |
| Undo history snapshots | 64 actual snapshots | `src/studio/state/history_state.elisa` (`CAPACITY`) stores whole stack snapshots in a fixed array. At capacity, recording shifts out the oldest snapshot and keeps the newest 64; if the saved cursor is evicted, dirty state is conservatively retained. | `test/studio_state.elisa` exercises overflow and undo at capacity. `src/studio/history.elisa`'s `MAX_CAPACITY=4096` is a proof-policy ceiling, not the runtime studio history capacity. Measure memory cost and expose the practical undo horizon. |
| UI draw commands per frame | 1,024 | `../elisa-ui/src/core/ui_core_types.elisa` (`MAX_COMMANDS`); the studio bins curve segments (`CURVE_SEGMENTS=40`) and marker bins (`MARKER_BINS=120`) to stay within budget. | No draw-command overflow signal or dense-window visual exercise confirmed. M0/M1 must verify that dense lists/curves are clipped, virtualized or intentionally summarized instead of silently losing essential controls. |
| UI accessibility nodes per frame | 256 | Same `ui_core_types.elisa` (`MAX_ACCESSIBILITY_NODES`). `ui_core_accessibility.elisa` rejects invalid IDs and marks overflow as dropped. | Inspect `accessibility_dropped` in a dense studio frame and exercise VoiceOver; node count alone does not prove useful accessibility or discoverability. |

## Product interpretation and verification work

- These values are implementation bounds, not recommended take sizes or
  service-level guarantees. A take may load while a particular studio feature
  cannot operate over its entire duration.
- Distinguish container nodes, mocap-mapped joints and solver-eligible bones
  in user-facing copy. They are not interchangeable counts.
- The editor should explain a reached limit at the action that hits it,
  preserve the last valid state, and offer an appropriate cleanup path (for
  example remove/merge old contact entries or remove a correction) where that
  operation is safe.
- M0 still needs a reproducible boundary matrix for below/at/above cases,
  realistic long/dense GLBs, measured memory/runtime, a dense accessibility
  frame, and running-window screenshots. Avoid allocating multi-gigabyte test
  inputs merely to check a guard if a small parser-level fixture can prove it.
- M5 must resolve the 10× gap between timeline duration and foot/contact/cache
  feature duration, or communicate a deliberate supported-work-range model.
