#!/usr/bin/env python3
"""Check the cleanup exports' declared C widths, pointer shapes and arity.

This source guard does not prove buffer extents, lifetime or native behavior.
Unsupported declarations refuse qualification rather than being skipped.
"""
from pathlib import Path
import re
import sys

PAIRS = (
    ("src/studio/io/build_generation_trash_native.elisa", "studio_build_generation_trash_appkit.h"),
    ("src/studio/io/build_generation_candidate_provider_native.elisa", "studio_build_generation_candidate_provider_appkit.h"),
    ("src/studio/io/build_generation_recovery_discovery.elisa", "studio_build_generation_recovery_discovery_appkit.h"),
)
C_TYPES = {"int32_t": "i32", "uint32_t": "u32", "int64_t": "i64",
           "uint64_t": "u64", "char": "u8", "size_t": "usize"}
ELISA_TYPES = set(C_TYPES.values())


def c_parameter(parameter):
    match = re.fullmatch(r"\s*(const\s+)?(\w+)\s*(\*)?\s*(\w+)\s*", parameter)
    if not match or match[2] not in C_TYPES:
        raise ValueError(f"unsupported C parameter: {parameter}")
    kind = C_TYPES[match[2]]
    if match[3]:
        kind = ("const-pointer:" if match[1] else "pointer:") + kind
    elif match[1]:
        raise ValueError(f"unsupported scalar const qualification: {parameter}")
    return kind


def elisa_parameter(parameter):
    match = re.fullmatch(r"\s*\w+\s*:\s*(mutable\s+)?(\w+)\s*(&)?\s*", parameter)
    if not match:
        raise ValueError(f"unsupported Elisa parameter: {parameter}")
    if match[2] == "cstr" and not match[1] and not match[3]:
        return "const-pointer:u8"
    if match[2] not in ELISA_TYPES:
        raise ValueError(f"unsupported Elisa parameter type: {parameter}")
    if match[3]:
        return ("pointer:" if match[1] else "const-pointer:") + match[2]
    if match[1]:
        raise ValueError(f"unsupported mutable scalar parameter: {parameter}")
    return match[2]


def check(project, engine):
    checked = 0
    for elisa_path, header_path in PAIRS:
        elisa = (project / elisa_path).read_text()
        native = (engine / "native" / header_path).read_text()
        native = re.sub(r"/\*.*?\*/|//[^\n]*", "", native, flags=re.S)
        pattern = (r'@link_name\("([^\"]+)"\)\s+@callconv\(c\)\s+'
                   r'extern\s+(\w+)\s*\((.*?)\)\s*->\s*(\w+)')
        declarations = list(re.finditer(pattern, elisa, re.S))
        links = re.findall(r'@link_name\("([^\"]+)"\)', elisa)
        if len(set(links)) != len(links):
            raise ValueError(f"duplicate foreign symbol declaration: {elisa_path}")
        if len(declarations) != len(links) or not declarations:
            raise ValueError(f"missing C calling convention or unsupported declaration: {elisa_path}")
        for declaration in declarations:
            symbol, local, arguments, result = declaration.groups()
            native_pattern = r"(\w+)\s+" + re.escape(symbol) + r"\s*\((.*?)\)\s*;"
            signatures = list(re.finditer(native_pattern, native, re.S))
            if len(signatures) != 1:
                raise ValueError(f"expected one C prototype for {symbol}")
            signature = signatures[0]
            native_result = C_TYPES.get(signature[1])
            native_arguments = [c_parameter(p) for p in signature[2].split(",")]
            elisa_arguments = [elisa_parameter(p) for p in arguments.split(",")]
            if result != native_result or elisa_arguments != native_arguments:
                raise ValueError(f"cleanup ABI mismatch for {symbol} ({local}): "
                                 f"C {native_arguments} -> {native_result}; "
                                 f"Elisa {elisa_arguments} -> {result}")
            checked += 1
    return checked


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: studio_verify_cleanup_abi.py PROJECT ENGINE")
    try:
        count = check(*map(Path, sys.argv[1:]))
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
    print(f"Studio cleanup C declarations match ({count} exports; extents/lifetime remain separate)")


if __name__ == "__main__":
    main()
