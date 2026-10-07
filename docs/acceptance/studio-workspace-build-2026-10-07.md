# Workspace setup build — 2026-10-07

Compiler merge `48dc78e2ce51873a459a689b4d8bb63a1c76bd4f` includes upstream
performance changes through `63585c5f` and preserves project repairs.
Reseed completed with exit 0 after increasing the serialized memory allowance
from 6 GiB to 12 GiB on a 24 GiB host. No performance claim is established.

- Stage1 SHA-256: `461d377b3e61307ac4a4cb46e56729d84a21c509e38ddd57f39935002abe959f`.
- Runtime SHA-256: `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
- Studio source revision: `df0072d5`.
- Build generation: `build/studio-build.DhRq20`.
- Executable SHA-256: `ff39f85489be552ea800800d7c2290de2f408046b00ed7012e376f7fbbbf1d4d`.
- Retained package: `build/studio-package.nVauk1/MocapStudio.app`.
- Log: `build/latest-compiler-qualification/studio-workspace-fix-build-final.log`.

Compilation, linking and executable publication succeeded. Overall build command
returned 1 because package publication could not acquire the previous bundle's
lease. `lsof` identified running old Studio process 27368 holding that lease.
The retained bundle executable matches the new generation, and it was launched
without closing the old instance.

Computer-use screenshot inspection confirmed the Workspace / File control is
visible below the toolbar and separate from Pending exports. Accessibility exposes
its workspace help and status. Opening the menu could not yet be verified: AX
click left the tree unchanged, and the subsequent coordinate operation reported
`noWindowsAvailable`. Both app processes remained live. Full setup, cancellation,
FBX import and character switching acceptance remain open.
