#!/usr/bin/env python3
"""Run compiled tests with a bounded dynamic worker pool."""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_one(path, run_directory):
    name = Path(path).stem
    record = {"schema": "mocap-test-execution-v1", "test": name,
              "started_ns": time.time_ns(), "returncode": None}
    if (ROOT / "build" / "test" / f"{name}.status").read_text().strip() not in ("ok", "cached"):
        record["outcome"] = "build-failed"
        record["finished_ns"] = time.time_ns()
        with (run_directory / f"{name}.json").open("x") as output:
            json.dump(record, output, sort_keys=True)
        return name, None
    executable = ROOT / "build" / "test" / name
    record["executable_sha256_before"] = file_digest(executable)
    build_key = ROOT / "build" / "test" / f"{name}.build-key"
    record["build_key_before"] = build_key.read_text().strip()
    output = run_directory / f"{name}.log"
    with output.open("xb") as log:
        result = subprocess.run(
            [str(executable)], cwd=ROOT,
            stdout=log, stderr=subprocess.STDOUT, check=False
        )
    record["returncode"] = result.returncode
    record["finished_ns"] = time.time_ns()
    record["executable_sha256_after"] = file_digest(executable)
    record["build_key_after"] = build_key.read_text().strip()
    record["output_sha256"] = file_digest(output)
    stable = (record["executable_sha256_before"] == record["executable_sha256_after"] and
              record["build_key_before"] == record["build_key_after"])
    record["outcome"] = "completed" if stable else "inputs-changed"
    with (run_directory / f"{name}.json").open("x") as destination:
        json.dump(record, destination, sort_keys=True)
    # Compatibility copy is explicitly replaceable. The run directory owns
    # the evidence used to print and review this execution's result.
    latest = ROOT / "build" / "test" / f"{name}.run.log"
    temporary = latest.with_name(latest.name + "." + run_directory.name)
    with output.open("rb") as source, temporary.open("xb") as destination:
        for chunk in iter(lambda: source.read(65536), b""):
            destination.write(chunk)
    os.replace(temporary, latest)
    if record["outcome"] != "completed":
        raise RuntimeError(f"test inputs changed during execution: {name}; evidence: {run_directory}")
    return name, result.returncode


def main():
    jobs = int(sys.argv[1])
    paths = sys.argv[2:]
    run_directory = ROOT / "build" / "test-runs" / uuid.uuid4().hex
    run_directory.mkdir(parents=True, mode=0o700)
    print(f"test execution evidence: {run_directory}", flush=True)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run_one, path, run_directory): Path(path).stem for path in paths}
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
        output = run_directory / f"{name}.log"
        with output.open("rb") as log:
            while chunk := log.read(65536):
                sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.write(f"test  {name}: rc={code}\n".encode())
        if code != 0:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
