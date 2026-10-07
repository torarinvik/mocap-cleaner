#!/usr/bin/env bash
# Package the just-built Studio executable as a Finder-launchable app bundle.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${MOCAP_STUDIO_GENERATION_LOCK_VERIFIED:-}" != "1" ]]; then
  exec python3 "$ROOT/tools/studio_generation_lock.py" run -- "$BASH" "$0" "$@"
fi
python3 "$ROOT/tools/studio_generation_lock.py" check
ENGINE="$(cd -- "${ELISA_ENGINE_ROOT:-$ROOT/../elisa-engine-mocap}" && pwd)"
UI="$(cd -- "${ELISA_UI_ROOT:-$ROOT/../elisa-ui}" && pwd)"
STAGE1="$(cd -- "${ELISA_STAGE1:-$ROOT/../Elisa-compiler}" && pwd)"
EXECUTABLE="${1:-$ROOT/build/mocap_studio}"
INPUT_RECORD="${2:-}"
final_app="$ROOT/build/MocapStudio.app"

[[ -x "$EXECUTABLE" ]] || { echo "Studio executable missing or not executable: $EXECUTABLE" >&2; exit 2; }
if [[ -z "$INPUT_RECORD" ]]; then
  resolved_executable="$(python3 - "$EXECUTABLE" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve(strict=True))
PY
)"
  adjacent_record="$(dirname -- "$resolved_executable")/inputs.json"
  [[ ! -f "$adjacent_record" ]] || INPUT_RECORD="$adjacent_record"
fi
if [[ -n "$INPUT_RECORD" ]]; then
  python3 "$ROOT/tools/studio_build_identity.py" --check-snapshot "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$INPUT_RECORD"
fi
pending_package="$(mktemp -d "$ROOT/build/studio-package.XXXXXX")"
APP="$pending_package/MocapStudio.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp -p "$EXECUTABLE" "$APP/Contents/MacOS/MocapStudio"
install -m 0600 /dev/null "$APP/Contents/Resources/.studio-generation.lease"
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

python3 - "$ROOT" "$ENGINE" "$UI" "$STAGE1" "$APP/Contents/MacOS/MocapStudio" "$APP/Contents/Resources/BUILD-INFO.txt" "$INPUT_RECORD" "$pending_package" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

project, engine, ui, compiler, executable, output = map(Path, sys.argv[1:7])
input_record = Path(sys.argv[7]) if sys.argv[7] else None
package_root = Path(sys.argv[8])
sys.path.insert(0, str(project / "tools"))
from studio_generation_lock import verified_lock
from studio_generation_contents import verify_record
from studio_generation_controls import seal_control

def generated_id(directory, prefix):
    name = directory.name
    suffix = name[len(prefix):] if name.startswith(prefix) else ""
    if not suffix or not all(char.isascii() and (char.isalnum() or char in "_-") for char in suffix):
        raise SystemExit("Studio package generation directory has no valid generated ID")
    return name

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
    "storage_manifest_lock.c", "studio_generation_lease_appkit.m",
    "studio_generation_lease_appkit.h", "elisa_native_fallbacks.cpp"))
input_paths.extend((project / "scripts/build_studio.sh", project / "scripts/package_studio_app.sh",
                    project / "tools/svg_icons.py", project / "build/generated/studio_icon_paths.elisa",
                    project / "tools/studio_generation_lock.py",
                    project / "tools/studio_generation_contents.py",
                    project / "tools/studio_generation_controls.py",
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
package_generation_id = generated_id(package_root, "studio-package.")
build_generation_id = "unavailable"
executable_hash = sha256(executable)
package_record = {
    "schema": "mocap-studio-package-generation-v2",
    "lease_protocol": 0,
    "package_generation_id": package_generation_id,
    "build_generation_id": None,
    "executable_sha256": executable_hash,
}
if input_record is not None:
    record_bytes = input_record.read_bytes()
    record = json.loads(record_bytes)
    if not isinstance(record, dict):
        raise SystemExit("Build input record is not an object")
    product = record.get("product", {})
    if (not isinstance(product, dict) or product.get("filename") != "mocap_studio" or
            product.get("sha256") != executable_hash):
        raise SystemExit("Packaged executable does not match the sealed build input record")
    generation = record.get("generation", {})
    if not isinstance(generation, dict):
        raise SystemExit("Build input record has no exact generation-directory identity")
    build_generation_id = generation.get("id", "")
    if (generation.get("schema") != "mocap-studio-generation-v1" or
            generation.get("artifact") != "studio-build" or
            generation.get("lease_protocol") != 1 or
            build_generation_id != generated_id(input_record.parent, "studio-build.")):
        raise SystemExit("Build input record has no exact generation-directory identity")
    package_record["build_generation_id"] = build_generation_id
    package_record["lease_protocol"] = 1
    (output.parent / "BUILD-INPUTS.json").write_bytes(record_bytes)
    captured_hash = hashlib.sha256(record_bytes).hexdigest()
    qualification = "sealed inputs and exact copied executable verified; runtime acceptance remains separate"
(output.parent / "PACKAGE-GENERATION.json").write_text(
    json.dumps(package_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
lease_record = {
    "schema": "mocap-studio-artifact-lease-v1",
    "lease_protocol": package_record["lease_protocol"],
    "artifact": "studio-package",
    "id": package_generation_id,
    "executable_sha256": executable_hash,
}
lease_path = package_root / "MocapStudio.app/Contents/Resources/.studio-generation.lease"

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
    f"package_generation_id={package_generation_id}",
    f"build_generation_id={build_generation_id}",
    f"packaging_observed_inputs_sha256={source_hash.hexdigest()}",
    f"input_qualification={qualification}",
    f"executable_sha256={sha256(executable)}",
    f"runtime_object_sha256={sha256(compiler / 'build/runtime/elisacore_runtime.o')}",
]
Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
# Register only the paths produced above. An extra descendant refuses sealing.
artifact = str((package_root / "MocapStudio.app").relative_to(project / "build"))
command = [sys.executable, str(project / "tools/studio_generation_contents.py"),
           "--project", str(project), "--artifact", artifact,
           "--artifact-id", package_generation_id, "--kind", "studio-package"]
for path in ("Contents", "Contents/MacOS", "Contents/Resources"):
    command.extend(("--directory", path))
for path in ("Contents/Info.plist", "Contents/PkgInfo", "Contents/MacOS/MocapStudio",
             "Contents/Resources/BUILD-INFO.txt"):
    command.extend(("--file", path))
import os
lock_fd, _, _ = verified_lock(project, os.environ)
subprocess.run(command, pass_fds=(lock_fd,), check=True)
inventory_hash = verify_record(project, artifact, package_generation_id, "studio-package")
package_record["contents_inventory_sha256"] = inventory_hash
lease_record["contents_inventory_sha256"] = inventory_hash
if input_record is not None:
    seal_control(output.parent / "BUILD-INPUTS.json", record_bytes.decode("utf-8"))
seal_control(output.parent / "PACKAGE-GENERATION.json",
             json.dumps(package_record, indent=2, sort_keys=True) + "\n")
seal_control(lease_path, json.dumps(lease_record, sort_keys=True) + "\n", readonly=True)

PY

sync_package_publication() {
  python3 "$ROOT/tools/studio_generation_controls.py" --project "$ROOT" \
    --directory "$(basename "$pending_package")" --directory .
}

# Prepare the whole bundle before moving the previous one. Keep a recoverable
# backup, and restore it if publishing the new bundle fails.
restore_previous_bundle() {
  local package_status=$?
  trap - EXIT
  if [[ ! -e "$final_app" && ! -L "$final_app" ]] &&
     [[ -e "$pending_package/previous.app" || -L "$pending_package/previous.app" ]]; then
    if ! mv "$pending_package/previous.app" "$final_app" || ! sync_package_publication; then
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
  sync_package_publication
fi
if ! mv "$APP" "$final_app"; then
  if [[ -e "$pending_package/previous.app" || -L "$pending_package/previous.app" ]]; then
    mv "$pending_package/previous.app" "$final_app"
    sync_package_publication
  fi
  echo "could not publish Studio bundle" >&2
  exit 1
fi
sync_package_publication
echo "packaged $final_app"
