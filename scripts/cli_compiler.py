#!/usr/bin/env python3
"""Link console tools with the engine's portable filesystem path adapter."""

import os
import hashlib
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile


def selected_toolchain(compiler):
    selected = Path(shutil.which(compiler) or compiler).resolve(strict=True)
    if ((selected.name == "elisac_stage1.sh" and selected.parent.name == "scripts") or
            (selected.name == "elisac-stage1" and selected.parent.name == "bin")):
        compiler_root = selected.parent.parent
    else:
        raise ValueError("CLI compiler must be the selected Stage1 wrapper or product")
    configured = os.environ.get("ELISA_STAGE1")
    if configured and Path(configured).resolve(strict=True) != compiler_root:
        raise ValueError("CLI compiler differs from ELISA_STAGE1 checkout")
    expected_runtime = (compiler_root / "build/runtime/elisacore_runtime.o").resolve()
    runtime = Path(os.environ.get("MOCAP_CLI_RUNTIME", expected_runtime)).resolve()
    if runtime != expected_runtime:
        raise ValueError("CLI runtime must belong to the selected compiler checkout")
    return compiler_root, runtime


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    compiler = os.environ["MOCAP_CLI_COMPILER"]
    args = sys.argv[1:]
    if "-emit" in args and args.index("-emit") + 1 == len(args):
        print("CLI compiler -emit requires a value", file=sys.stderr)
        return 2
    if "-emit" not in args or args[args.index("-emit") + 1] != "exe":
        return subprocess.call([compiler, *args])
    if "-o" not in args or args.index("-o") + 1 == len(args):
        print("CLI native linking requires an explicit output path", file=sys.stderr)
        return 2
    output_index = args.index("-o") + 1
    output = Path(args[output_index]).resolve()
    engine = Path(os.environ.get("ELISA_ENGINE_ROOT", root.parent / "elisa-engine-mocap"))
    try:
        compiler_root, runtime = selected_toolchain(compiler)
    except (OSError, ValueError) as error:
        print(f"CLI toolchain selection: {error}", file=sys.stderr)
        return 2
    provenance_check = [sys.executable, str(compiler_root / "scripts/stage1_provenance.py"),
                        "check", str(compiler_root), str(compiler_root / "bin/elisac-stage1")]
    status = subprocess.call(provenance_check)
    if status:
        return status
    # Object compilation bypasses the Stage1 wrapper's executable-link path.
    # Refresh the exact runtime here so a compiler/source update cannot leave
    # this manual native link using the previous runtime product.
    runtime_environment = os.environ.copy()
    runtime_environment["ELISA_STAGE1_BIN"] = str(compiler_root / "bin/elisac-stage1")
    runtime_environment["ELISA_RUNTIME_OBJ"] = str(runtime)
    status = subprocess.call(
        ["bash", str(compiler_root / "scripts/build_runtime_object.sh")],
        env=runtime_environment,
    )
    if status:
        return status
    runtime_digest = file_digest(runtime)
    output.parent.mkdir(parents=True, exist_ok=True)
    # A failed compile or link leaves the previous executable intact.
    with tempfile.TemporaryDirectory(prefix="cli-link-", dir=output.parent) as temporary:
        directory = Path(temporary)
        args[args.index("-emit") + 1] = "obj"
        args[output_index] = str(directory / "main.o")
        commands = [
            [compiler, *args],
            ["clang", "-std=c11", "-Wall", "-Wextra", "-Werror", "-O2", "-c",
             str(engine / "native/file_path.c"), "-o", str(directory / "file_path.o")],
        ]
        link_inputs = [str(directory / "main.o"), str(directory / "file_path.o"), str(runtime)]
        if sys.platform == "darwin":
            commands.append([
                "clang", "-fobjc-arc", "-Wall", "-Wextra", "-Werror", "-O2", "-c",
                str(engine / "native/file_path_namespace_appkit.m"),
                "-o", str(directory / "file_path_namespace.o"),
            ])
            link_inputs.extend([str(directory / "file_path_namespace.o"), "-framework", "Foundation"])
        commands.append(["clang", *link_inputs, "-lm", "-o", str(directory / "executable")])
        for command in commands:
            status = subprocess.call(command)
            if status:
                return status
        status = subprocess.call(provenance_check)
        if status:
            return status
        if file_digest(runtime) != runtime_digest:
            print("CLI runtime changed during compilation/linking; refusing publication", file=sys.stderr)
            return 2
        os.replace(directory / "executable", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
