#!/usr/bin/env python3
"""Print a cache key for test executables from source and toolchain state."""
import hashlib
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_SUFFIXES = {".elisa", ".elisai", ".c", ".h", ".m", ".mm", ".cc", ".cpp", ".go", ".py", ".sh"}


def add_file(digest, path):
    path = Path(path)
    digest.update(str(path.resolve()).encode() + b"\0")
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1 << 20), b""):
                digest.update(block)
    except OSError:
        digest.update(b"<missing>")
    digest.update(b"\0")


def add_repo(digest, repo):
    try:
        tracked = subprocess.check_output(
            ["git", "-C", str(repo), "ls-files", "-z"], stderr=subprocess.DEVNULL
        )
        untracked = subprocess.check_output(
            ["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard", "-z"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit(f"test build key: cannot inventory repository {repo.resolve()}")
    digest.update(str(repo.resolve()).encode() + b"\0")
    paths = set(filter(None, tracked.split(b"\0")))
    paths.update(filter(None, untracked.split(b"\0")))
    for raw_path in sorted(paths):
        relative = Path(os.fsdecode(raw_path))
        if relative.suffix not in SOURCE_SUFFIXES:
            continue
        add_file(digest, repo / relative)


def resolve_compiler(selection):
    """Resolve the checkout shared by cache identity and generated declarations."""
    selected_compiler = Path(shutil.which(selection) or selection).resolve()
    configured_root = Path(os.environ["ELISA_STAGE1"]).resolve() if os.environ.get("ELISA_STAGE1") else None
    if selected_compiler.name == "elisac_stage1.sh" and selected_compiler.parent.name == "scripts":
        compiler_root = selected_compiler.parent.parent
    elif selected_compiler.name == "elisac-stage1" and selected_compiler.parent.name == "bin":
        compiler_root = selected_compiler.parent.parent
    else:
        raise SystemExit(
            "test build key: cannot establish compiler checkout from this command; "
            "select CHECKOUT/scripts/elisac_stage1.sh or CHECKOUT/bin/elisac-stage1")
    if configured_root is not None and compiler_root != configured_root:
        raise SystemExit("test build key: selected compiler differs from ELISA_STAGE1 checkout")
    return selected_compiler, compiler_root.resolve()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: test_build_key.py ELISAC")
    selected_compiler, compiler_root = resolve_compiler(sys.argv[1])
    digest = hashlib.sha256(b"mocap-cleaner-test-build-v5\0")
    digest.update(f"{platform.system()}:{platform.machine()}:{sys.version}\0".encode())
    digest.update((sys.argv[1] + "\0-emit exe").encode())
    add_file(digest, selected_compiler)
    sys.path.insert(0, str(ROOT / "tools"))
    from build_environment import build_environment_digest
    digest.update(build_environment_digest().encode() + b"\0")

    # Compiler source changes invalidate cached executables even when the product
    # has not been rebuilt yet. The next compile then reaches the wrapper
    # provenance gate instead of accepting cached results from a stale product.
    for repo in (ROOT, compiler_root, ROOT.parent / "elisa-engine-mocap", ROOT.parent / "elisa-ui"):
        add_repo(digest, repo)

    for name in ("ELISAC", "ELISA_STAGE1_BIN", "ELISA_RUNTIME_OBJ", "ELISA_CLANG", "ELISA_AR", "LLVM_CONFIG"):
        value = os.environ.get(name)
        if value:
            add_file(digest, value)

    add_file(
        digest,
        os.environ.get("ELISA_STAGE1_BIN", compiler_root / "bin" / "elisac-stage1"),
    )
    runtime = os.environ.get("ELISA_RUNTIME_OBJ")
    if runtime and runtime != "none":
        add_file(digest, runtime)
    else:
        add_file(digest, compiler_root / "build" / "runtime" / "elisacore_runtime.o")

    llvm_config = os.environ.get("LLVM_CONFIG", "/opt/homebrew/opt/llvm/bin/llvm-config")
    clang = os.environ.get("ELISA_CLANG") or str(Path(llvm_config).parent / "clang")
    if not Path(clang).is_file():
        clang = shutil.which("clang") or clang
    add_file(digest, clang)
    llvm_ar = os.environ.get("ELISA_AR") or str(Path(llvm_config).parent / "llvm-ar")
    if not Path(llvm_ar).is_file():
        llvm_ar = shutil.which("ar") or llvm_ar
    add_file(digest, llvm_config)
    add_file(digest, llvm_ar)

    add_file(digest, compiler_root / "build" / "compiler-build-manifest.json")
    add_file(digest, ROOT / "build" / "generated" / "studio_icon_paths.elisa")
    print(digest.hexdigest())


if __name__ == "__main__":
    main()
