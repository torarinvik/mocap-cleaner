# Studio native build snapshot — 2026-10-07

This record establishes compilation, native linking and local packaging at one
captured input snapshot. Runtime, motion quality, proof authentication and user
acceptance remain open. The shared UI changed after publication; this package
cannot qualify that newer source.

## Command and terminal result

```sh
ELISA_STAGE1='../Elisa-compiler-ui-result-regionless' STUDIO_SKIP_CHECKS=1 \
  bash scripts/build_studio.sh
```

The owned session 92393 completed with **exit 0**. Tests and proofs were skipped.
The script compiled the complete app and native adapters, checked source/link
inputs before publication, sealed content inventories, published the executable
and packaged the app. It reported 982 maintained text files within 600 lines.

Platform: arm64 macOS 27.0.1, Apple M5, 24 GiB memory, Xcode SDK 27.0.

## Source and product identities

| Input | Captured identity |
| --- | --- |
| Project | `f2721fb29a0d8d7c0cc65f17bc914be3c44cb748`; dirty flag includes the unrelated `.gitignore` edit |
| Compiler | clean `ac0f4423189e7f554388a903888347400d74acee`, preserving repair `517aae39` and fetched upstream `218c2c22` |
| Compiler source tree | `1b34af95cfb8dc232f19df3db79377af92f071209650537b7eef85405f8e2f56` |
| Stage1 product | `e5ca2db0d650bd6bc28550f396dff9d390da6f7d6097f29e4c3cb6ef9a9e00fe` |
| Compiler recipe | `105bd840e8e6ce839d87eb77f5155a4600e33b44d102db614d9402e15d433073` |
| Runtime object | `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee` |
| Mocap engine | clean `e1e9d1d4e637126ed873001e2ae0f7239821de6d`, branch `mocap-track`; fetched main `55541b7b` is included |
| UI | `f33e439b3dc25eb28bb62b282128c0b0c9d6838a`, with preserved shared-agent changes; fetched main `dc6cd397` is included |

The runtime audit independently recomputed the stored input digest
`34a30d9c206fd1759e6458432c57db8b885a9900eaf5e63af0b0f13c14f1fd89`.
Its stamp binds the current source tree, Stage1 product, runtime build/hooks
recipe, O2 host settings and `/usr/bin/clang` partial linker to object `51365ba4`.
A different installed runtime hash is not by itself evidence of staleness.

Dirty revision flags alone do not identify source. The sealed input record lists
individual source/native/header/tool hashes and the build-environment digest.

## Retained artifacts

- Build generation: `build/studio-build.dM1BGO`.
- Package generation: `studio-package.aUwsFD`, recorded in the published app's
  `Contents/Resources/PACKAGE-GENERATION.json`.
- Executable and packaged executable SHA256:
  `9f84c3fef92c00fc7db879238c62bc6db643f66390695f1ecb222a131ebc60a7`.
- Sealed `inputs.json` and packaged `BUILD-INPUTS.json` SHA256:
  `2d1ecd32ec6c9f0eca6fd40018a592f96a64e77fc3b234a76a317bcf7792b9d2`.
- Build content inventory:
  `344c600a09370f03ac6de252e2d48d3580632559f359d85ae340258e3f1ec245`.
- Package content inventory:
  `66b83c677dbed60fcd05d7553671676494c1fb3576dbc50eeaba2eff73f7d4da`.
- Terminal log: `build/latest-compiler-qualification/studio-current-closed-build.log`,
  SHA256 `9238c952d240f115b61a8fc1c7d4d0846fa8c0f83eff0c49c309d6240b3ec92c`.

## Subsequent drift and remaining acceptance

`elisa-ui/src/widgets/ui_text_metrics.elisa` changed after publication:
recorded SHA256 `c9fb3f71921f1ec0ef8642b54df172707a1c2dc5c171e3ab9a922a48a9b06769`,
later SHA256 `6da4c3d39bd10548981f7c4e26183b3ccc888a5d2a1c094c547a2b0a7de5653b`.
A follow-up input check refused the changed snapshot. Verification also requires
the original build environment; a context with different build-affecting settings
must not be treated as the same snapshot.

Coordinate a stable UI checkpoint and rebuild before current runtime acceptance.
Use the matched current producer/replay pair for source-authenticated contracts.
Exercise generation inventory, reviewed Move, cancellation/draining, Retry Release,
exact Resolve Review, restart discovery, Restore, small windows, Unicode paths,
keyboard and VoiceOver. Preserve source hashes and all unresolved recovery files.
Failed/partial artifact admission remains an implementation gap; this successful
build does not establish that those protected rows can be cleaned up.
