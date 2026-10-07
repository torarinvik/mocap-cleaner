#!/usr/bin/env bash
# Reconcile an already-current package without moving or removing bundles.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$#" != 1 ]]; then
  echo "usage: $0 studio-package.GENERATION_ID" >&2
  exit 2
fi
exec python3 "$ROOT/tools/studio_generation_lock.py" run -- \
  python3 "$ROOT/tools/studio_generation_package_reconcile.py" \
  --project "$ROOT" --artifact-id "$1"
