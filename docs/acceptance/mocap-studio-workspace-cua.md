# Mocap Studio workspace UI qualification

Date: 2026-10-06

## Bundle inspected

- Bundle: `build/MocapStudio.app`
- `CFBundleIdentifier`: `org.elisa.mocap-studio`
- `CFBundleExecutable`: `MocapStudio`
- Executable SHA-256 (same for `build/mocap_studio` and the bundle executable):
  `d413b721586538e79839378fdef87c3e87a40c57568535295b323426d92b2a97`
- Build input fingerprint: `46b5120dc47aa6bdac1d82b8ef60606b34fb4eaa6af1a051c23258003556c673`
- Source revision recorded by the build: `dac26e253beca8ff26fac602359a950e8e4cd6e9`; project worktree was dirty. Engine `01f5aec758b98640cd3dc4ba214390cc09c4ec31`, UI `8ab2eb395e2c4457748961a801384d11dc44a515`, compiler `f292cbe0766f2d5086f174c984b0f2cd0a64d85c` were clean at build time. Full hashes are in `Contents/Resources/BUILD-INFO.txt`.

## Observed

CUA launched the bundle and exposed a native “Mocap Studio” window. Its accessibility tree included the workspace container and a File button. The window showed “Workspace unavailable. Choose Locate workspace to select a writable build folder.” No take was loaded.

CUA did not activate the File button through AX click. `Cmd-O` and Tab produced no visible state change. Coordinate click returned `-10005 noWindowsAvailable`. Read-only process inspection showed the bundle executable still running as PID 13335 with AppKit resources loaded; the ten-minute unified-log query returned no matching records. These observations do not establish a packaging or window-creation defect.

## Still open

Locate/Create menu behavior, keyboard and accessibility focus, chooser cancellation preserving a loaded take, and successful workspace selection remain unqualified. No valid take was loaded, so cancellation preservation was not exercised. Do not treat this record as closure of the native workflow gate.

## Follow-up build

After the CUA attempt, the no-take accessibility tree was updated to expose
the workspace status as a Status node after File. Compile and package-only
build succeeded. The resulting bundle executable SHA-256 is
`3d90aab321ffacab030f0a176a8c6ba12ffa23a674dfe2cb6e27141b17a2a169`, with
build input fingerprint
`194a0b0869d70f265d8a448b99495cd188340c100d1b77d92ef0c1e76b2c09de`.
The build record names source revision `4686b26de4d6809437caeaad268a6f5fe86e0d2b`
and marks the project worktree dirty. This follow-up binary has not been
inspected through CUA: the existing app process remained alive, and its input
path still reports `noWindowsAvailable`. The new status node is compile-qualified
only, not natively observed.
