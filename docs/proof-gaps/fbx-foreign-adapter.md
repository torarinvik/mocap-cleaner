# Tracked FBX foreign adapter

`2003894` extracts foreign calls into `StudioFbxImportNative`; `c7a99b3`
integrates it into the worker. `979f8b5` corrects capability handling: operation-
specific `can` grants retain propagation, and newly introduced `trusted` blocks
and extern trust exemptions are removed. A future trust boundary needs an explicit
reason to stop propagation, not merely a desire to silence a diagnostic.

The adapter accepts bounded terminated arrays, initializes native output buffers,
checks returned paths/digests and returns owned data with explicit caller regions.
Staging results are destructured once, preserving affine consumption. These checks
do not establish native pointer non-retention, buffer extent or source preservation.

## Captured source evidence

Selected compiler `48dc78e2`/product `461d377b`, runtime `51365ba4`:

- Adapter source SHA-256: `3325dddc05e19ef0aff89878e34b01e9d9258e5e775ab3f947ec2e1361763ea2`.
- Worker source SHA-256: `c6e85c35488af933385d7e64f482c103911de16c71381eeb4ead73a77366320a`.
- Adapter and worker object compilation exits 0; logs are
  `build/fbx_native_adapter_tracked.log` and
  `build/fbx_native_adapter_tracked_worker.log`.
- Unsafe report `build/fbx_native_adapter_tracked_unsafe.json` is compiler text,
  despite its historical filename. SHA-256:
  `777ca9a1e08dd3e13db0ae8eabc85821e36a22ca8869362b2520d8b62e9ca12f`.
  It reports PointerCast/RawExtern on all four wrappers and `trusted-total: 0`.
  It also reports unchecked indexing and buffer reinterpretation, which must
  remain visible in the safety audit.

## Strict extern gate remains open

The earlier strict-extern compile relied on `@trusted` exemptions and is superseded.
Without them, `-strict-externs` exits 1: four declarations lack boundary contracts,
and staging/digest mutable output pointers lack declared extents. Exact diagnostics
are in `build/fbx_native_adapter_tracked_strict.log`. Ordinary source compilation
and runtime output checks cannot close this gate.

Implement explicit native pointer/length bridges, preserve old APIs, and use
supported C-callconv bounds/contracts without changing the native ABI accidentally.
Check path termination, each output extent (including the 65-byte digest),
initialization, synchronous non-retention, blocking effects and failure outputs.
Requalify the ABI guard, current source/link closure and authorized FBX runtime
checks. Actual asynchronous import, result-region ownership and the complete UI
journey remain separate open gates.
