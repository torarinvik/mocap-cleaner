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
    adapter = (project / "src/studio/fbx_import_native.elisa").read_text()
    native_signature = r"int64_t\s+elisa_fbx_to_glb_bounded\s*\(\s*const\s+char\s*\*\s*input\s*,\s*size_t\s+input_length\s*,\s*const\s+char\s*\*\s*output\s*,\s*size_t\s+output_length\s*,\s*double\s+rate\s*\)"
    adapter_signature = (
        r'@link_name\("elisa_fbx_to_glb_bounded"\)\s+@callconv\(c\)\s+'
        r'@bounds\(source,\s*source_length,\s*destination,\s*destination_length\)\s+'
        r'extern\s+raw_convert\(source:\s*u8&,\s*source_length:\s*usize,\s*'
        r'destination:\s*u8&,\s*destination_length:\s*usize,\s*rate:\s*f64\)\s*->\s*i64')
    if not re.search(native_signature, native):
        raise SystemExit("Studio FBX ABI: expected native double rate declaration; review the adapter")
    if not re.search(adapter_signature, adapter):
        raise SystemExit("Studio FBX ABI: Elisa converter must declare an f64 rate")
    print("Studio bounded FBX converter ABI matches (pointer/size_t pairs, double/f64)")


if __name__ == "__main__":
    main()
