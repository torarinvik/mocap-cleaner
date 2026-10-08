#!/usr/bin/env python3
"""Generate test runtime declarations from the same compiler as the cache key."""
import os
from pathlib import Path
import subprocess
import sys

from test_build_key import ROOT, resolve_compiler


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare_test_runtime.py ELISAC")
    _, compiler = resolve_compiler(sys.argv[1])
    engine = Path(os.environ.get("ELISA_ENGINE_ROOT", ROOT.parent / "elisa-engine-mocap"))
    ui = Path(os.environ.get("ELISA_UI_ROOT", ROOT.parent / "elisa-ui"))
    # The canonical generator validates compiler provenance and fixed include
    # roots before atomically replacing declarations. Never copy old std files.
    subprocess.run([sys.executable, str(ROOT / "tools/studio_build_identity.py"),
                    str(ROOT), str(engine), str(ui), str(compiler),
                    str(ROOT / "build/generated/studio_build_identity.elisa")],
                   check=True)


if __name__ == "__main__":
    main()
