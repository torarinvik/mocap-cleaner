#!/usr/bin/env python3
"""Refuse mixed compiler/runtime source in focused Studio qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("compiler", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    compiler = args.compiler.resolve(strict=True)
    source = args.source.resolve(strict=True)
    product = compiler / "bin/elisac-stage1"
    checked = subprocess.run([sys.executable, str(compiler / "scripts/stage1_provenance.py"),
                              "check", str(compiler), str(product)])
    if checked.returncode:
        raise SystemExit(checked.returncode)
    selected_std = (compiler / "elisacore_std").resolve(strict=True)
    selected_runtime = (selected_std / "elisacore_runtime.elisa").resolve(strict=True)
    project = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project / "scripts"))
    from prove import sources

    paths = []
    sources(str(source), paths)
    entries = []
    found_runtime = False
    for spelling in paths:
        included = Path(spelling).resolve(strict=True)
        if included.name == "elisacore_runtime.elisa":
            if included != selected_runtime:
                raise SystemExit(f"Runtime source differs from selected compiler: {included}")
            found_runtime = True
        if "elisacore_std" in Path(spelling).parts or "elisacore_std" in included.parts:
            if not included.is_relative_to(selected_std):
                raise SystemExit(f"Standard-library source differs from selected compiler: {included}")
        entries.append({"path": str(included),
                        "sha256": hashlib.sha256(included.read_bytes()).hexdigest()})
    if not found_runtime:
        raise SystemExit("Studio qualification source does not include the selected runtime")
    record = {"format": "mocap-studio-focused-source-closure-v1",
              "source": str(source), "compiler": str(compiler),
              "product_sha256": hashlib.sha256(product.read_bytes()).hexdigest(),
              "runtime_source": str(selected_runtime), "ordered_sources": entries}
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(record, indent=2) + "\n")
    print(f"Studio runtime source matches selected compiler ({len(entries)} source files)")


if __name__ == "__main__":
    main()
