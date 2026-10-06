"""Generate constant build-input provenance; never query Git during export."""
import hashlib
import re
import subprocess
import sys
from pathlib import Path


def fields(label, root):
    revision = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("invalid Git revision")
    dirty = bool(subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True).strip())
    return [(label + "_REVISION", revision),
            (label + "_DIRTY", str(dirty).lower())]


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


project, engine, ui, compiler, output = map(Path, sys.argv[1:])
subprocess.run([sys.executable, str(compiler / "scripts/stage1_provenance.py"),
                "check", str(compiler), str(compiler / "bin/elisac-stage1")],
               check=True)
values = []
for label, root in (("PROJECT", project), ("ENGINE", engine),
                    ("UI", ui), ("COMPILER", compiler)):
    values.extend(fields(label, root))
values.extend([
    ("COMPILER_SHA256", digest(compiler / "bin/elisac-stage1")),
    ("RUNTIME_SHA256", digest(compiler / "build/runtime/elisacore_runtime.o"))])
text = "# Generated build-input identity; dirty revisions are not exact source identities.\n"
text += "module StudioBuildIdentity:\n    public:\n        const module Inputs:\n"
text += "".join(f'            {name}: sview = "{value}"\n' for name, value in values)
output.parent.mkdir(parents=True, exist_ok=True)
temporary = output.with_suffix(".tmp")
temporary.write_text(text)
temporary.replace(output)
