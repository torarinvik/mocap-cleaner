#!/usr/bin/env python3
"""Require a matching current prover product for checked qualification."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_sha(root):
    digest = hashlib.sha256()
    for directory, children, files in os.walk(root):
        children.sort()
        for name in sorted(files):
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            digest.update(relative.encode() + b"\0")
            digest.update(bytes.fromhex(sha(path)))
    return digest.hexdigest()


def main():
    if len(sys.argv) != 4:
        raise ValueError("usage: check_prover_freshness.py PROVER PROOF_ROOT COMPILER_ROOT")
    prover, proof_root, compiler_root = map(lambda p: Path(p).resolve(), sys.argv[1:])
    manifest = json.loads(Path(str(prover) + ".manifest.json").read_text())
    if not isinstance(manifest, dict) or manifest.get("schema") != "elisa-proof-build-manifest-v1":
        raise ValueError("unsupported prover manifest")
    if manifest["binary"]["sha256"] != sha(prover):
        raise ValueError("prover manifest does not match the selected binary")
    if os.environ.get("MOCAP_PROOF_COMPARISON") == "1":
        raise ValueError("comparison mode cannot pass current qualification; run the selected prover directly and label its evidence as comparison")
    head = subprocess.check_output(["git", "-C", str(proof_root), "rev-parse", "HEAD"], text=True).strip()
    if manifest["proof"]["head"] != head or manifest["proof"]["source_tree_sha256"] != tree_sha(proof_root / "src"):
        raise ValueError("selected prover is stale relative to current proof source; rebuild and qualify it")
    subprocess.run([sys.executable, str(compiler_root / "scripts/stage1_provenance.py"),
                    "check", str(compiler_root), str(compiler_root / "bin/elisac-stage1")], check=True)
    compiler = json.loads((compiler_root / "bin/elisac-stage1.provenance.json").read_text())
    revision = compiler["source_revision"]
    if manifest["frontend"]["revision"] != revision or manifest["compiler"]["source_revision"] != revision:
        raise ValueError("prover frontend/compiler is stale relative to current Stage1; rebuild and qualify it")
    linked_compiler = manifest["compiler"]
    for field in ("source_tree_sha256", "build_recipe_sha256"):
        if linked_compiler[field] != compiler[field]:
            raise ValueError(f"prover compiler {field} differs from current Stage1; rebuild and qualify it")
    if linked_compiler["product"]["sha256"] != compiler["product_sha256"]:
        raise ValueError("prover was linked with a different Stage1 product; rebuild and qualify it")
    frontend_tree = subprocess.check_output(
        ["git", "-C", str(compiler_root), "rev-parse", revision + "^{tree}"], text=True).strip()
    if manifest["frontend"]["tree"] != frontend_tree:
        raise ValueError("prover frontend tree does not match its compiler revision")
    if manifest["runtime"]["sha256"] != sha(compiler_root / "build/runtime/elisacore_runtime.o"):
        raise ValueError("prover runtime does not match current compiler runtime")
    print("prover freshness: current source, frontend, compiler and runtime")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f"prover freshness: {error}", file=sys.stderr)
        sys.exit(2)
