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

## Historical strict extern refusal

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

## Bounded adapter qualification

`5320ffd7` replaces these declarations with pointer/length bridges from engine
commit `3c51102b2d748984634d1594e09f9bc8f837c773`. All five operations declare C
calling convention, bounds and contracts. Unsafe.RawExtern propagates through
`can`; this adapter has no intentional trust-erasure boundary. Native pointer
non-retention remains an external implementation obligation.

The closed adapter probe compiled with `-strict-externs -O2`, linked and ran with
exit 0 against the installed compiler source `50b16e6800fe03e3369a78aa85fffb55ee2f38e3`:

- Compiler product: `a0a9b2951d68c64f3a3c56cf20ff99eee8256af3f0ff467c591cecaac6eb1bae`.
- Runtime object: `ca40ba1db8a74110936ad5cdaf808707020c5c74ebb6e491bda2198696d13b8a`.
- Probe source: `ac94f23455f4ad0d3138ddcb24bba951d3bb437e645070ea559c2f7874c010dd`.
- Probe object: `2dc74ecc2c2a9f288d14a778e0081694458f571fbf9518d076dcce2b1746420c`.
- Executable: `94e59413bcdafdc12a59c8d24038f7f875f06bc43d88a23f2bc9fec145e5e009`.

The probe stages and converts the user's high-block FBX, verifies source and
derived digests and cache admission, refuses overwriting the existing output,
and checks that the source digest remains unchanged. Logs are
`build/fbx_bounded_adapter_runtime_probe.log`,
`build/fbx_bounded_adapter_runtime_link.log` and
`build/fbx_bounded_adapter_runtime_result.log`.

This closes the bounded adapter slice for that tuple. It does not qualify task
ownership, the application import path or Character/Skeleton presentation.
Upstream subsequently advanced to `75568f8`; current application qualification
must use a fresh matching compiler/runtime build with the pending ABI repairs.
