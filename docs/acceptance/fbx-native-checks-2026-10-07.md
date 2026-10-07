# Captured native FBX checks — 2026-10-07

These authorized focused checks use native objects from Studio generation
`build/studio-build.yOXPzH`, built against compiler `bb274b14`. They do not
qualify the newer compiler merge `48dc78e2` or establish UI acceptance.

## ABI correction and repeat

The original Python converter invocation declared its frame-rate argument as
`c_int64`, while the native function expects `double`. Those converter calls
cannot qualify the requested sampling rate. The staging FIFO check does not
call that ABI and remains a separate observation. Studio had the same mismatch;
commit `fcc7da4` fixes its declaration and explicit conversion.

Corrected `c_double` calls at 30.0 fps are recorded in
`build/fbx-correct-rate-h32e__xd/results.json`. The bladed fixture succeeds and
produces the identical GLB digest recorded below. The user
`high block_Unreal5.6.fbx` still refuses with skin status -6 and no output. Both
sources retain their original digests. The corrected matrix in `build/fbx-correct-rate-h32e__xd/matrix.json` also
confirms deterministic repeat, existing-destination refusal with unchanged bytes,
and malformed/truncated refusal with no output and preserved source bytes.
These results still describe the captured old native objects; qualify the new
eight-influence/joint-limit implementation separately.

## Original observed results (sampling rate unqualified)

- The selected fixture produced a GLB with one mesh, one skin and one animation.
- A second conversion produced an identical GLB SHA-256.
- An existing destination was refused and its bytes remained unchanged.
- Malformed and truncated FBX inputs were refused with no published output;
  their source bytes remained unchanged.
- Staging a FIFO refused immediately (0.000159 seconds), with empty returned
  paths/digest.
- The original fixture retained SHA-256
  `4aac7f8dda4a03d9a452dcec450ced74e7057cdb807434eb7314b2d3ce28fec8`.

## Artifacts

The test dylib links the captured converter, ufbx and staging object files.
The JSON results retain paths, return statuses and digest observations.

- `build/latest-compiler-qualification/studio-fbx-native.dylib`: SHA-256 `01d795cb72fbd30e706664842dfd6af435e7351caeec66057ba9863d726a6730`.
- `build/fbx-runtime-8t_omy1p/results.json`: SHA-256 `08787ffc45104823723e1449fac752605e7c0172087fcbf636a27192a2c2fa7c`.
- `build/fbx-runtime-8t_omy1p/additional-results.json`: SHA-256 `21f3c12f472559c5670ccc1c05ad0ba4a1dcbbf2dbc3c4e8862f30511bfc56cf`.

## Remaining evidence

Independent posed skin correspondence, edits, actual viewport switching,
cancellation/restart and session reopen/Locate remain required. Passing these
checks does not establish proof source correspondence or native IO correctness
outside the observed cases.
