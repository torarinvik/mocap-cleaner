#!/usr/bin/env python3
"""Check the known FBX converter ABI before compiling Studio.

This narrow source check covers the converter's rate type, not arbitrary FFI.
"""
from pathlib import Path
import re
import sys


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: studio_verify_fbx_abi.py PROJECT ENGINE")
    project, engine = map(Path, sys.argv[1:])
    native = (engine / "native/fbx_to_glb.c").read_text()
    worker = (project / "src/studio/fbx_import_worker.elisa").read_text()
    native_signature = r"int64_t\s+elisa_fbx_to_glb\s*\(\s*const\s+char\s*\*\s*input\s*,\s*const\s+char\s*\*\s*output\s*,\s*double\s+rate\s*\)"
    worker_signature = r'@link_name\("elisa_fbx_to_glb"\)\s+extern\s+convert\(source:\s*cstr,\s*destination:\s*cstr,\s*rate:\s*f64\)\s*->\s*i64'
    if not re.search(native_signature, native):
        raise SystemExit("Studio FBX ABI: expected native double rate declaration; review the adapter")
    if not re.search(worker_signature, worker):
        raise SystemExit("Studio FBX ABI: Elisa converter must declare an f64 rate")
    print("Studio FBX converter rate ABI matches (double/f64)")


if __name__ == "__main__":
    main()
