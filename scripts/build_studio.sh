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
# Use the configured current compiler. Its wrapper enforces build provenance;
# do not silently select a historical worktree or permit a stale Stage1.

[[ "$(uname -s)" == "Darwin" ]] || { echo "the studio window is macOS only" >&2; exit 2; }
[[ -f "$RUNTIME" ]] || { echo "no runtime object at $RUNTIME" >&2; exit 2; }
mkdir -p "$OUT" "$OUT/test"
cd "$ROOT"
python3 "$ROOT/tools/svg_icons.py" "$OUT/generated/studio_icon_paths.elisa"

clang -c -fobjc-arc -O2 -o "$OUT/studio_canvas_shim.o" "$UI/src/platform/appkit/appkit_canvas_shim.m"
clang -c -fobjc-arc -O2 -o "$OUT/studio_viewport_metal.o" "$ENGINE/native/viewport_metal.m"
clang -c -fobjc-arc -O2 -o "$OUT/studio_file_panel.o" "$ENGINE/native/file_panel_appkit.m"
clang -c -fobjc-arc -O2 -o "$OUT/studio_file_trash.o" "$ENGINE/native/file_trash_appkit.m"
clang -std=c11 -O2 -c -o "$OUT/studio_file_path.o" "$ENGINE/native/file_path.c"
clang -fobjc-arc -Wall -Wextra -Werror -O2 -c -o "$OUT/studio_file_path_namespace.o" "$ENGINE/native/file_path_namespace_appkit.m"
clang -fobjc-arc -Wall -Wextra -Werror -O2 -c -o "$OUT/studio_workspace_root.o" "$ENGINE/native/workspace_root_appkit.m"
clang -std=c11 -Wall -Wextra -Werror -O2 -c -o "$OUT/studio_storage_manifest_lock.o" "$ENGINE/native/storage_manifest_lock.c"
clang++ -c -std=c++17 -O2 -o "$OUT/studio_native_fallbacks.o" "$ENGINE/native/elisa_native_fallbacks.cpp"
bash "$STAGE1/scripts/elisac_stage1.sh" -O2 -o "$OUT/studio_main.o" "$ROOT/src/studio/app/main.elisa"
clang -o "$OUT/mocap_studio" \
  "$OUT/studio_main.o" "$OUT/studio_canvas_shim.o" "$OUT/studio_viewport_metal.o" "$OUT/studio_file_panel.o" "$OUT/studio_file_trash.o" "$OUT/studio_file_path.o" "$OUT/studio_file_path_namespace.o" "$OUT/studio_workspace_root.o" "$OUT/studio_storage_manifest_lock.o" \
  "$OUT/studio_native_fallbacks.o" "$RUNTIME" \
  -framework Cocoa -framework Foundation -framework CoreText -framework CoreGraphics -framework ImageIO \
  -framework QuartzCore -framework IOSurface -framework Metal -framework UniformTypeIdentifiers
echo "built $OUT/mocap_studio"

[[ "${STUDIO_SKIP_CHECKS:-0}" == "1" ]] && exit 0

status=0
if bash "$ROOT/scripts/check_storage_io.sh"; then
  :
else
  echo "FAIL storage_io"; status=1
fi
if clang -std=c11 -Wall -Wextra -Werror -O2 \
  -o "$OUT/test/file_path_test" "$ENGINE/native/file_path.c" "$ENGINE/native/file_path_test.c" \
  && TMPDIR="$OUT/test" "$OUT/test/file_path_test"; then
  :
else
  echo "FAIL file_path_test"; status=1
fi
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
