#!/usr/bin/env bash
# Build Mocap Studio (src/studio/app/main.elisa): an elisa-ui AppKit canvas
# window hosting three Elisa engine Metal viewports. Then run the studio's
# headless tests and prove the studio kernels.
#
#   scripts/build_studio.sh            build + test + prove
#   STUDIO_SKIP_CHECKS=1 scripts/...   build only
#   build/mocap_studio [clip.glb [animation]]
#
# Environment: ELISA_UI_ROOT (../elisa-ui), ELISA_ENGINE_ROOT
# (../elisa-engine-mocap), ELISA_STAGE1 (../Elisa-compiler), ELISA_PROOF
# (../elisa-proof-mocap/build/elisa-proof).
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
UI="$(cd -- "${ELISA_UI_ROOT:-$ROOT/../elisa-ui}" && pwd)"
ENGINE="$(cd -- "${ELISA_ENGINE_ROOT:-$ROOT/../elisa-engine-mocap}" && pwd)"
STAGE1="$(cd -- "${ELISA_STAGE1:-$ROOT/../Elisa-compiler}" && pwd)"
PROOF="${ELISA_PROOF:-$ROOT/../elisa-proof-mocap/build/elisa-proof}"
RUNTIME="$STAGE1/build/runtime/elisacore_runtime.o"
OUT="$ROOT/build"
export ELISA_ALLOW_STALE_STAGE1="${ELISA_ALLOW_STALE_STAGE1:-1}"
# The main compiler checkout's bin/elisac-stage1 predates two fixes the studio
# needs: the current module winning name lookup (compiler e2871b2c; otherwise
# Ops::Kind clashes with elisa-ui's Kind) and keeping values stored into module
# globals out of the storing function's auto region (branch studio-globals;
# otherwise the Studio's clip/memo globals read freed memory and the window
# shows an empty rig and timeline). Prefer that binary; ELISA_STAGE1_BIN
# overrides it.
STUDIO_STAGE1="$ROOT/../elisa-compiler-worktrees/studio-globals/bin/elisac-stage1"
if [[ -z "${ELISA_STAGE1_BIN:-}" && -x "$STUDIO_STAGE1" ]]; then export ELISA_STAGE1_BIN="$STUDIO_STAGE1"; fi
[[ -n "${ELISA_STAGE1_BIN:-}" ]] || echo "warning: no studio-globals stage1; Studio globals may read freed memory" >&2

[[ "$(uname -s)" == "Darwin" ]] || { echo "the studio window is macOS only" >&2; exit 2; }
[[ -f "$RUNTIME" ]] || { echo "no runtime object at $RUNTIME" >&2; exit 2; }
mkdir -p "$OUT" "$OUT/test"
cd "$ROOT"
python3 "$ROOT/tools/svg_icons.py" "$OUT/generated/studio_icon_paths.elisa"

clang -c -fobjc-arc -O2 -o "$OUT/studio_canvas_shim.o" "$UI/src/platform/appkit/appkit_canvas_shim.m"
clang -c -fobjc-arc -O2 -o "$OUT/studio_viewport_metal.o" "$ENGINE/native/viewport_metal.m"
clang -c -fobjc-arc -O2 -o "$OUT/studio_file_panel.o" "$ENGINE/native/file_panel_appkit.m"
clang++ -c -std=c++17 -O2 -o "$OUT/studio_native_fallbacks.o" "$ENGINE/native/elisa_native_fallbacks.cpp"
bash "$STAGE1/scripts/elisac_stage1.sh" -O2 -o "$OUT/studio_main.o" "$ROOT/src/studio/app/main.elisa"
clang -o "$OUT/mocap_studio" \
  "$OUT/studio_main.o" "$OUT/studio_canvas_shim.o" "$OUT/studio_viewport_metal.o" "$OUT/studio_file_panel.o" \
  "$OUT/studio_native_fallbacks.o" "$RUNTIME" \
  -framework Cocoa -framework CoreText -framework CoreGraphics -framework ImageIO \
  -framework QuartzCore -framework IOSurface -framework Metal -framework UniformTypeIdentifiers
echo "built $OUT/mocap_studio"

[[ "${STUDIO_SKIP_CHECKS:-0}" == "1" ]] && exit 0

status=0
for t in "$ROOT"/test/studio_*.elisa; do
  name="$(basename "$t" .elisa)"
  if bash "$STAGE1/scripts/elisac_stage1.sh" -emit exe -o "$OUT/$name" "$t" && "$OUT/$name"; then
    echo "PASS $name"
  else
    echo "FAIL $name"; status=1
  fi
done
if [[ -x "$PROOF" ]]; then
  for f in "$ROOT"/src/studio/*.elisa; do
    if "$PROOF" "$f" | grep -q "state: proved"; then
      echo "PROVED $(basename "$f")"
    else
      echo "NOT PROVED $(basename "$f")"; status=1
    fi
  done
else
  echo "no prover at $PROOF; proofs skipped"
fi
exit $status
