#!/usr/bin/env python3
"""Link console tools with the engine's portable filesystem path adapter."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    compiler = os.environ["MOCAP_CLI_COMPILER"]
    args = sys.argv[1:]
    if "-emit" not in args or args[args.index("-emit") + 1] != "exe":
        return subprocess.call([compiler, *args])
    if "-o" not in args:
        print("CLI native linking requires an explicit output path", file=sys.stderr)
        return 2
    output_index = args.index("-o") + 1
    output = Path(args[output_index]).resolve()
    engine = Path(os.environ.get("ELISA_ENGINE_ROOT", root.parent / "elisa-engine-mocap"))
    runtime = Path(os.environ.get("MOCAP_CLI_RUNTIME", root.parent / "Elisa-compiler/build/runtime/elisacore_runtime.o"))
    if not runtime.is_file():
        print(f"Missing Elisa runtime: {runtime}", file=sys.stderr)
        return 2
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
        os.replace(directory / "executable", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
