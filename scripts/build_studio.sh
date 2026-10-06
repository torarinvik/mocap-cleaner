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
if [[ "${STUDIO_SKIP_CHECKS:-0}" != 1 ]]; then
  python3 scripts/check_prover_freshness.py "$PROOF" "${ELISA_PROOF_ROOT:-$ROOT/../elisa-proof-mocap}" "$STAGE1"
fi
python3 "$ROOT/scripts/check_file_lengths.py"
python3 "$ROOT/tools/svg_icons.py" "$OUT/generated/studio_icon_paths.elisa"
python3 "$ROOT/tools/studio_build_identity.py" "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$OUT/generated/studio_build_identity.elisa"

pending_directory="$(mktemp -d "$OUT/studio-build.XXXXXX")"
pending_object="$pending_directory/main.o"
pending_inputs="$pending_directory/inputs.json"
python3 "$ROOT/tools/studio_build_identity.py" --snapshot "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$pending_inputs"

clang -c -fobjc-arc -O2 -o "$pending_directory/studio_canvas_shim.o" "$UI/src/platform/appkit/appkit_canvas_shim.m"
clang -c -fobjc-arc -O2 -o "$pending_directory/studio_viewport_metal.o" "$ENGINE/native/viewport_metal.m"
clang -c -fobjc-arc -O2 -o "$pending_directory/studio_file_panel.o" "$ENGINE/native/file_panel_appkit.m"
clang -c -fobjc-arc -O2 -o "$pending_directory/studio_file_trash.o" "$ENGINE/native/file_trash_appkit.m"
clang -std=c11 -O2 -c -o "$pending_directory/studio_file_path.o" "$ENGINE/native/file_path.c"
clang -fobjc-arc -Wall -Wextra -Werror -O2 -c -o "$pending_directory/studio_file_path_namespace.o" "$ENGINE/native/file_path_namespace_appkit.m"
clang -fobjc-arc -Wall -Wextra -Werror -O2 -c -o "$pending_directory/studio_workspace_root.o" "$ENGINE/native/workspace_root_appkit.m"
clang -std=c11 -Wall -Wextra -Werror -O2 -c -o "$pending_directory/studio_storage_manifest_lock.o" "$ENGINE/native/storage_manifest_lock.c"
clang++ -c -std=c++17 -O2 -o "$pending_directory/studio_native_fallbacks.o" "$ENGINE/native/elisa_native_fallbacks.cpp"
bash "$STAGE1/scripts/elisac_stage1.sh" -O2 -o "$pending_object" "$ROOT/src/studio/app/main.elisa"
[[ -s "$pending_object" ]] || { echo "compiler did not emit a fresh Studio object" >&2; exit 1; }
python3 "$ROOT/tools/studio_build_identity.py" --check-snapshot "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$pending_inputs"
clang -o "$pending_directory/mocap_studio" \
  "$pending_object" "$pending_directory/studio_canvas_shim.o" "$pending_directory/studio_viewport_metal.o" "$pending_directory/studio_file_panel.o" "$pending_directory/studio_file_trash.o" "$pending_directory/studio_file_path.o" "$pending_directory/studio_file_path_namespace.o" "$pending_directory/studio_workspace_root.o" "$pending_directory/studio_storage_manifest_lock.o" \
  "$pending_directory/studio_native_fallbacks.o" "$RUNTIME" \
  -framework Cocoa -framework Foundation -framework CoreText -framework CoreGraphics -framework ImageIO \
  -framework QuartzCore -framework IOSurface -framework Metal -framework UniformTypeIdentifiers
[[ -s "$pending_directory/mocap_studio" ]] || { echo "linker did not emit a fresh Studio executable" >&2; exit 1; }
python3 "$ROOT/tools/studio_build_identity.py" --check-snapshot "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$pending_inputs"
# Publish only after fresh compilation, linking and input revalidation pass.
# Failure preserves the previous executable and its recorded input identity.
python3 "$ROOT/tools/studio_build_identity.py" --seal-product "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$pending_inputs"
# Keep each executable beside its immutable objects and sealed input record.
# Renaming one symlink publishes that complete generation atomically.
ln -s "$(basename "$pending_directory")/mocap_studio" "$pending_directory/current-executable"
[[ ! -d "$OUT/mocap_studio" ]] || { echo "Studio output is a directory; refusing to replace it" >&2; exit 1; }
mv -f "$pending_directory/current-executable" "$OUT/mocap_studio"
echo "built $OUT/mocap_studio"
bash "$ROOT/scripts/package_studio_app.sh" "$OUT/mocap_studio" "$pending_inputs"

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
  # Use the same complete reviewed corpus as check.sh. A matching line from
  # a partial or crashed prover process is insufficient qualification.
  proof_files=(src/*/*.elisa src/studio/io/*_policy.elisa src/studio/io/storage_preferences_codec.elisa proof/*.elisa)
  if ! python3 scripts/prove.py "$PROOF" "${proof_files[@]}"; then
    status=1
  fi
  if ! python3 scripts/check_proof_baseline.py "${proof_files[@]}"; then
    status=1
  fi
else
  echo "no prover at $PROOF; proof qualification failed" >&2
  status=1
fi
exit $status
