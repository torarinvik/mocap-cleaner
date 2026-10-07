"""Fingerprint build-affecting settings without publishing their values."""
import hashlib
import json
import os


def build_environment_digest():
    # Retain identity without writing arbitrary environment values into a
    # distributable manifest. Tool lookup, SDK/header selection and semantic
    # compiler settings can change output even when source bytes are stable.
    names = {
        "PATH", "HOME", "TMPDIR", "SDKROOT", "DEVELOPER_DIR", "TOOLCHAINS",
        "MACOSX_DEPLOYMENT_TARGET", "CC", "CXX", "CPP", "AR", "AS", "LD",
        "CFLAGS", "CPPFLAGS", "CXXFLAGS", "OBJCFLAGS", "OBJCXXFLAGS", "LDFLAGS",
        "CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "OBJC_INCLUDE_PATH",
        "LIBRARY_PATH", "COMPILER_PATH", "SOURCE_DATE_EPOCH", "ZERO_AR_DATE",
        "LANG", "LC_ALL", "PYTHON_BIN", "PYTHON_CONFIG", "LLVM_CONFIG",
    }
    excluded = {"ELISA_STAGE1_MAX_RSS_KB", "ELISA_PROOF_JOBS",
                "ELISA_PROOF_HEAVY_JOBS", "ELISA_PROOF_BUILD_JOBS",
                "ELISA_PROOF_OBJECT_CACHE", "ELISA_PROOF_REPORT_CACHE"}
    selected = {name: value for name, value in os.environ.items()
                if name not in excluded and
                (name in names or name.startswith(("ELISA_", "LLVM_", "CLANG_",
                                                  "LD_", "DYLD_", "LC_")))}
    payload = json.dumps(selected, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


