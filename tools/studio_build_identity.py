"""Generate constant build-input provenance; never query Git during export."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from build_environment import build_environment_digest


def fields(label, root):
    revision = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("invalid Git revision")
    dirty = bool(subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True).strip())
    return [(label + "_REVISION", revision),
            (label + "_DIRTY", str(dirty).lower())]


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def snapshot(project, engine, ui, compiler):
    # Reuse the maintained include reader. Missing or newly created includes
    # must invalidate a build; they cannot silently disappear from its identity.
    sys.path.insert(0, str(project / "scripts"))
    from prove import include_target, sources

    paths = []
    sources(str(project / "src/studio/app/main.elisa"), paths)
    selected_runtime = (compiler / "elisacore_std/elisacore_runtime.elisa").resolve(strict=True)
    selected_std = (compiler / "elisacore_std").resolve(strict=True)
    for source in paths:
        included = Path(source).resolve(strict=True)
        if included.name == "elisacore_runtime.elisa" and included != selected_runtime:
            raise SystemExit(f"Studio includes a runtime outside the selected compiler: {included}")
        # Prelude, collections and runtime fragments must share the selected
        # product's stdlib too. Inspect the lexical path as well so a symlink
        # inside elisacore_std cannot hide an include outside that root.
        if "elisacore_std" in Path(source).parts or "elisacore_std" in included.parts:
            if not included.is_relative_to(selected_std):
                raise SystemExit(f"Studio includes standard-library source outside the selected compiler: {included}")
    paths.extend(str(path) for path in (
        project / "scripts/build_studio.sh",
        project / "scripts/prove.py",
        Path(__file__).resolve(),
        Path(__file__).resolve().with_name("build_environment.py"),
        compiler / "bin/elisac-stage1",
        compiler / "build/runtime/elisacore_runtime.o",
        compiler / "scripts/elisac_stage1.sh",
        compiler / "scripts/process_rss.sh",
        compiler / "scripts/elisac_stage1_seed.sh",
        compiler / "scripts/assert_stage1_fresh.sh",
        compiler / "scripts/stage1_provenance.py",
        project / "scripts/package_studio_app.sh",
        ui / "src/platform/appkit/appkit_canvas_shim.m",
        *(engine / "native" / name for name in (
            "viewport_metal.m", "file_panel_appkit.m", "file_trash_appkit.m",
            "file_path.c", "file_path_namespace_appkit.m",
            "workspace_root_appkit.m", "storage_manifest_lock.c",
            "elisa_native_fallbacks.cpp"))))
    native_tools = {}
    for name in ("clang", "clang++", "ld"):
        selected = subprocess.check_output(["xcrun", "--find", name], text=True).strip()
        native_tools[name] = selected
        paths.append(selected)
        command = shutil.which(name)
        if command is None:
            raise ValueError("missing native tool: " + name)
        paths.append(command)
    headers = re.compile(rb'^\s*#\s*(?:include|import)\s*"([^"]+)"')
    pending = list(paths)
    files = {}
    while pending:
        path = Path(pending.pop()).resolve(strict=True)
        if str(path) in files:
            continue
        files[str(path)] = digest(path)
        if path.suffix == ".elisa":
            for number, line in enumerate(path.read_bytes().split(b"\n"), 1):
                if re.match(rb"^\s*include(?:\s|$)", line) and include_target(line) is None:
                    raise ValueError(f"unrecognized include directive: {path}:{number}")
        if path.suffix in (".c", ".cpp", ".m", ".h", ".hpp"):
            for line in path.read_bytes().splitlines():
                match = headers.match(line)
                if match:
                    pending.append(path.parent / match[1].decode("utf-8"))
    return {"schema": "mocap-studio-inputs-v2", "files": files,
            "build_environment_sha256": build_environment_digest(),
            "native_tools": native_tools,
            "sdk": subprocess.check_output(["xcrun", "--show-sdk-path"], text=True).strip(),
            "sdk_version": subprocess.check_output(["xcrun", "--show-sdk-version"], text=True).strip()}


mode = "generate"
arguments = sys.argv[1:]
if arguments and arguments[0] in ("--snapshot", "--check-snapshot", "--seal-product"):
    mode = arguments.pop(0)
project, engine, ui, compiler, output = (path.resolve() for path in map(Path, arguments))
# Elisa imports currently name these sibling checkouts directly. An environment
# override must not silently link another checkout's native implementation.
for label, selected, sibling in (
        ("engine", engine, project.parent / "elisa-engine-mocap"),
        ("UI", ui, project.parent / "elisa-ui")):
    if selected != sibling.resolve(strict=True):
        raise SystemExit(f"Selected {label} checkout differs from the fixed Elisa include root: {sibling}")
subprocess.run([sys.executable, str(compiler / "scripts/stage1_provenance.py"),
                "check", str(compiler), str(compiler / "bin/elisac-stage1")],
               check=True)
runtime_source = (compiler / "elisacore_std/elisacore_runtime.elisa").resolve(strict=True)
runtime_bridge = project / "build/generated/studio_runtime.elisa"
runtime_text = "# Generated runtime declarations from the selected compiler.\n"
runtime_text += f"include {json.dumps(str(runtime_source))}\n"
if mode != "generate":
    if not runtime_bridge.is_file() or runtime_bridge.read_text() != runtime_text:
        raise SystemExit("Studio runtime selection differs from this compiler; regenerate the build identity first")
    current = snapshot(project, engine, ui, compiler)
    if mode == "--snapshot":
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
    else:
        recorded = json.loads(output.read_text())
        product = recorded.pop("product", None)
        if recorded != current:
            raise SystemExit("Studio source or link inputs changed during the build; refusing publication")
        if mode == "--seal-product":
            current["product"] = {"filename": "mocap_studio",
                                  "sha256": digest(output.parent / "mocap_studio")}
            output.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        elif product is not None:
            if product.get("filename") != "mocap_studio" or product.get("sha256") != digest(output.parent / "mocap_studio"):
                raise SystemExit("Studio executable differs from its sealed input record")
    raise SystemExit(0)
runtime_bridge.parent.mkdir(parents=True, exist_ok=True)
runtime_temporary = runtime_bridge.with_suffix(".tmp")
runtime_temporary.write_text(runtime_text)
runtime_temporary.replace(runtime_bridge)
values = []
for label, root in (("PROJECT", project), ("ENGINE", engine),
                    ("UI", ui), ("COMPILER", compiler)):
    values.extend(fields(label, root))
values.extend([
    ("COMPILER_SHA256", digest(compiler / "bin/elisac-stage1")),
    ("RUNTIME_SHA256", digest(compiler / "build/runtime/elisacore_runtime.o"))])
text = "# Generated build-input identity; dirty revisions are not exact source identities.\n"
text += "module StudioBuildIdentity:\n    public:\n        const module Inputs:\n"
text += "".join(f'            {name}: sview = "{value}"\n' for name, value in values)
output.parent.mkdir(parents=True, exist_ok=True)
temporary = output.with_suffix(".tmp")
temporary.write_text(text)
temporary.replace(output)
