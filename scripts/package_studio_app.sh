#!/usr/bin/env bash
# Package the just-built Studio executable as a Finder-launchable app bundle.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="$(cd -- "${ELISA_ENGINE_ROOT:-$ROOT/../elisa-engine-mocap}" && pwd)"
UI="$(cd -- "${ELISA_UI_ROOT:-$ROOT/../elisa-ui}" && pwd)"
STAGE1="$(cd -- "${ELISA_STAGE1:-$ROOT/../Elisa-compiler}" && pwd)"
EXECUTABLE="${1:-$ROOT/build/mocap_studio}"
INPUT_RECORD="${2:-}"
final_app="$ROOT/build/MocapStudio.app"

[[ -x "$EXECUTABLE" ]] || { echo "Studio executable missing or not executable: $EXECUTABLE" >&2; exit 2; }
if [[ -n "$INPUT_RECORD" ]]; then
  python3 "$ROOT/tools/studio_build_identity.py" --check-snapshot "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$INPUT_RECORD"
fi
pending_package="$(mktemp -d "$ROOT/build/studio-package.XXXXXX")"
APP="$pending_package/MocapStudio.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp -p "$EXECUTABLE" "$APP/Contents/MacOS/MocapStudio"
cat >"$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDevelopmentRegion</key><string>en</string>
  <key>CFBundleExecutable</key><string>MocapStudio</string>
  <key>CFBundleIdentifier</key><string>org.elisa.mocap-studio</string>
  <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
  <key>CFBundleName</key><string>Mocap Studio</string>
  <key>CFBundleDisplayName</key><string>Mocap Studio</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>0.1.0</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>NSPrincipalClass</key><string>NSApplication</string>
</dict>
</plist>
PLIST
printf 'APPL????' >"$APP/Contents/PkgInfo"

python3 - "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$APP/Contents/MacOS/MocapStudio" "$APP/Contents/Resources/BUILD-INFO.txt" "$INPUT_RECORD" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

project, engine, ui, compiler, executable, output = map(Path, sys.argv[1:7])
input_record = Path(sys.argv[7]) if sys.argv[7] else None

def repo_revision(root):
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

def repo_dirty(root):
    return bool(subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip())

input_paths = []
for base, suffixes in ((project / "src/studio", {".elisa"}),
                       (engine / "src", {".elisa"}),
                       (ui / "src", {".elisa", ".m", ".c", ".cpp"})):
    input_paths.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in suffixes)
input_paths.extend(engine / "native" / name for name in (
    "viewport_metal.m", "file_panel_appkit.m", "file_trash_appkit.m",
    "file_path.c", "file_path_namespace_appkit.m", "workspace_root_appkit.m",
    "storage_manifest_lock.c", "elisa_native_fallbacks.cpp"))
input_paths.extend((project / "scripts/build_studio.sh", project / "scripts/package_studio_app.sh",
                    project / "tools/svg_icons.py", project / "build/generated/studio_icon_paths.elisa",
                    project / "tools/studio_build_identity.py", project / "build/generated/studio_build_identity.elisa",
                    compiler / "scripts/elisac_stage1.sh", compiler / "build/runtime/elisacore_runtime.o"))
input_paths.extend(path for path in (project / "assets/icons").rglob("*.svg"))
source_hash = hashlib.sha256()
for path in sorted(set(input_paths)):
    if not path.is_file():
        continue
    try:
        label = path.relative_to(project.parent)
    except ValueError:
        label = path
    source_hash.update(str(label).encode("utf-8"))
    source_hash.update(b"\0")
    source_hash.update(path.read_bytes())

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

captured_hash = "unavailable"
qualification = "unrecorded: packaging observations do not establish compilation inputs"
if input_record is not None:
    record_bytes = input_record.read_bytes()
    record = json.loads(record_bytes)
    product = record.get("product", {})
    if product.get("filename") != "mocap_studio" or product.get("sha256") != sha256(executable):
        raise SystemExit("Packaged executable does not match the sealed build input record")
    (output.parent / "BUILD-INPUTS.json").write_bytes(record_bytes)
    captured_hash = hashlib.sha256(record_bytes).hexdigest()
    qualification = "sealed inputs and exact copied executable verified; runtime acceptance remains separate"

lines = [
    "Mocap Studio development bundle build provenance",
    f"project_revision={repo_revision(project)}",
    f"project_worktree_dirty={str(repo_dirty(project)).lower()}",
    f"engine_revision={repo_revision(engine)}",
    f"engine_worktree_dirty={str(repo_dirty(engine)).lower()}",
    f"ui_revision={repo_revision(ui)}",
    f"ui_worktree_dirty={str(repo_dirty(ui)).lower()}",
    f"compiler_revision={repo_revision(compiler)}",
    f"compiler_worktree_dirty={str(repo_dirty(compiler)).lower()}",
    f"build_inputs_sha256={captured_hash}",
    f"packaging_observed_inputs_sha256={source_hash.hexdigest()}",
    f"input_qualification={qualification}",
    f"executable_sha256={sha256(executable)}",
    f"runtime_object_sha256={sha256(compiler / 'build/runtime/elisacore_runtime.o')}",
]
Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

# Prepare the whole bundle before moving the previous one. Keep a recoverable
# backup, and restore it if publishing the new bundle fails.
restore_previous_bundle() {
  local package_status=$?
  trap - EXIT
  if [[ ! -e "$final_app" && ! -L "$final_app" ]] &&
     [[ -e "$pending_package/previous.app" || -L "$pending_package/previous.app" ]]; then
    if ! mv "$pending_package/previous.app" "$final_app"; then
      echo "previous Studio bundle retained at $pending_package/previous.app; restore failed" >&2
      package_status=1
    fi
  fi
  exit "$package_status"
}
trap restore_previous_bundle EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
if [[ -e "$final_app" || -L "$final_app" ]]; then
  mv "$final_app" "$pending_package/previous.app"
fi
if ! mv "$APP" "$final_app"; then
  if [[ -e "$pending_package/previous.app" || -L "$pending_package/previous.app" ]]; then
    mv "$pending_package/previous.app" "$final_app"
  fi
  echo "could not publish Studio bundle" >&2
  exit 1
fi
echo "packaged $final_app"
