"""Verify the exact engine-pinned FBX parser inputs before compiling Studio."""
import hashlib
import runpy
import sys
from pathlib import Path

engine = Path(sys.argv[1]).resolve(strict=True)
pins = runpy.run_path(str(engine / 'scripts/fetch_dependencies.py'))['PINNED']
for name in ('ufbx_source', 'ufbx_header'):
    revision, url, expected, relative = pins[name]
    path = engine / 'dependencies' / relative
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f'Missing regular pinned parser input: {path}')
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != expected:
        raise SystemExit(f'Pinned parser input changed: {path}')
print('Studio FBX parser inputs match engine pins')
