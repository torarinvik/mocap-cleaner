#!/usr/bin/env python3
"""Run compiled tests with a bounded dynamic worker pool."""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run_one(path):
    name = Path(path).stem
    if (ROOT / "build" / "test" / f"{name}.status").read_text().strip() != "ok":
        return name, None
    output = ROOT / "build" / "test" / f"{name}.run.log"
    with output.open("wb") as log:
        result = subprocess.run(
            [str(ROOT / "build" / "test" / name)], cwd=ROOT,
            stdout=log, stderr=subprocess.STDOUT, check=False
        )
    return name, result.returncode


def main():
    jobs = int(sys.argv[1])
    paths = sys.argv[2:]
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run_one, path): Path(path).stem for path in paths}
        for future in concurrent.futures.as_completed(futures):
            name, code = future.result()
            results[name] = code

    status = 0
    for path in paths:
        name = Path(path).stem
        code = results[name]
        if code is None:
            sys.stdout.buffer.write(
                f"test  {name}: BUILD FAILED (build/test/{name}.log)\n".encode()
            )
            status = 1
            continue
        output = ROOT / "build" / "test" / f"{name}.run.log"
        with output.open("rb") as log:
            while chunk := log.read(65536):
                sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.write(f"test  {name}: rc={code}\n".encode())
        if code != 0:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
