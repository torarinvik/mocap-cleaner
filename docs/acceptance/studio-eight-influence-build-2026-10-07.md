# Studio eight-influence build and remaining import refusal

## Captured build

`scripts/build_studio.sh` completed with exit 0 using `STUDIO_SKIP_CHECKS=1`
and selected compiler `../Elisa-compiler-ui-result-regionless`. This invocation
compiled, linked and packaged; it did not run the full test/proof suite.
The log is `build/latest-compiler-qualification/studio-eight-influence-build.log`.

The sealed package records:

- Project revision `db1ede9a727a94f2814adb75a3a71861d054aee7`.
- Engine revision `1cbed086200636fdea1aca83b460a8c9e9ba65e2`, clean.
- UI revision `f33e439b3dc25eb28bb62b282128c0b0c9d6838a`, with captured local changes.
- Compiler revision `48dc78e2ce51873a459a689b4d8bb63a1c76bd4f`, clean.
- Runtime SHA-256 `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
- Executable SHA-256 `e8c9fdc8afa1ce1a5ee30a9a494fd11887cf2e3ce94609037b6f9bed47f63f56`.
- Build generation `studio-build.6P1zvD`; package generation `studio-package.pQNZaT`.
- Build-input SHA-256 `42345db3712c5d8387940b1e0bc0ea089f8ec00cc36d8fe4f58224e3ecef4b75`.

Primary worktree dirtiness includes the unrelated `.gitignore` change, which was
not committed as part of this work. Exact captured input closure, rather than a
clean revision claim, is authoritative. The package was published normally to
`build/MocapStudio.app`.

## Actual app result

Launching the packaged app with the user's `high block_Unreal5.6.fbx` argument
produced a visible ready-workspace status and a generic FBX import refusal.
The empty viewport correctly lacked an unsaved-changes badge. This result
contradicts completion of the requested FBX journey; Character/Skeleton switching
and edited surface behavior remain unverified in Studio.

## Native isolation check

The exact captured native staging/converter/ufbx objects were linked into
`build/latest-compiler-qualification/studio-fbx-eight-influence.dylib`.
Calling staging against the user's selected workspace build root returned 0;
conversion with the correct `double` argument at 30 Hz also returned 0.
The derived GLB SHA-256 was
`36cba16f28c3c09fc777357a218c61f7f9d4a8b5e8f84d6c18505ee96085717e`.
The source digest remained
`50048a8a08f307d378e83d976462addcac62b5529bf60ae690da200d9d9f4485`.
The artifact `build/latest-compiler-qualification/current-user-stage.json`
records exclusively created snapshot and output paths under that workspace's
`build/imports/` directory.

These checks isolate the remaining failure above successful native staging and
conversion. They do not establish correct worker handoff, memo loading, source
reference admission or application publication. Diagnose those before accepting
the user journey.
