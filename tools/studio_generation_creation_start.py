"""Append the Created -> Building creation-journal event before product writes.

Events are create-only records; the original ownership declaration is retained.
No failed/sealed/published outcome or cleanup eligibility is inferred here.
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path

from studio_generation_contents import (
    DIRECTORY_FLAGS, FILE_FLAGS, Limits, identity, open_artifact, owned, require,
    scan, version, bounded_json,
)
from studio_generation_creation import Journal, declared_plan, publish_initial
from studio_generation_lock import verified_lock


class Event:
    phase = "building"
    revision = 2
    suffix = ".revision-2.json"
    initial_keys = frozenset((
        "schema", "artifact_id", "artifact_kind", "phase", "revision",
        "operation_id", "original_relative_path", "build_root_device",
        "build_root_inode", "root_device", "root_inode", "lease_device",
        "lease_inode", "declared_entries",
    ))


def read_record(parent, filename, private=True):
    fd = os.open(filename, FILE_FLAGS, dir_fd=parent)
    try:
        facts = os.fstat(fd)
        owned(facts)
        require((not private or not facts.st_mode & 0o077) and 0 < facts.st_size <= Limits.json_bytes,
                "creation record is not bounded and private")
        payload = bytearray()
        while len(payload) <= facts.st_size:
            chunk = os.read(fd, min(65536, facts.st_size + 1 - len(payload)))
            if not chunk:
                break
            payload.extend(chunk)
        require(len(payload) == facts.st_size and version(os.fstat(fd)) == version(facts),
                "creation record changed during read")
        record = bounded_json(payload)
        os.fsync(fd)
        require(version(os.stat(filename, dir_fd=parent, follow_symlinks=False)) ==
                version(facts), "creation record binding changed")
        return record, bytes(payload), facts
    finally:
        os.close(fd)


def read_initial(parent, artifact_id):
    record, payload, facts = read_record(parent, artifact_id + ".json")
    require(isinstance(record, dict) and set(record) == Event.initial_keys,
            "unsupported initial creation record fields")
    require(record["schema"] == Journal.schema and record["phase"] == Journal.phase and
            type(record["revision"]) is int and record["revision"] == Journal.revision and
            record["artifact_id"] == artifact_id, "unsupported initial creation state")
    require(isinstance(record["operation_id"], str) and
            re.fullmatch(r"[0-9a-f]{32}", record["operation_id"]), "invalid operation identity")
    entries = record["declared_entries"]
    require(isinstance(entries, list) and len(entries) <= Limits.entries, "invalid creation plan")
    files, directories = [], []
    for entry in entries:
        require(isinstance(entry, dict) and set(entry) == {"path", "kind"} and
                isinstance(entry["path"], str), "invalid declared creation entry")
        if entry["kind"] == "regular_file":
            files.append(entry["path"])
        else:
            require(entry["kind"] == "directory", "unsupported creation entry kind")
            directories.append(entry["path"])
    plan = declared_plan(files, directories, record["artifact_kind"])
    require(entries == [{"path": path, "kind": plan[path]} for path in sorted(plan)],
            "noncanonical creation plan")
    return record, payload, facts


def read_started(parent, artifact_id):
    initial, payload, facts = read_initial(parent, artifact_id)
    started, started_payload, started_facts = read_record(parent, artifact_id + Event.suffix)
    expected = dict(initial, phase=Event.phase, revision=Event.revision,
                    previous_revision=Journal.revision,
                    previous_sha256=hashlib.sha256(payload).hexdigest())
    require(started == expected and type(started.get("revision")) is int and
            type(started.get("previous_revision")) is int, "invalid creation start chain")
    return initial, payload, facts, started_payload, started_facts


def start_record(project, artifact, artifact_id):
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", artifact_id), "invalid artifact ID")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = root = lease_parent = lease = -1
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build directory replaced")
        parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation directory is not private")
        record, original, prior = read_initial(parent, artifact_id)
        require(record["original_relative_path"] == artifact, "creation artifact path differs")
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(record[prefix + "_device"]) is int and type(record[prefix + "_inode"]) is int and
                    (record[prefix + "_device"], record[prefix + "_inode"]) == identity(facts),
                    "creation root identity differs")
        lease_path = (".studio-generation.lease" if record["artifact_kind"] == "studio-build" else
                      "Contents/Resources/.studio-generation.lease")
        parent_path, _, name = lease_path.rpartition("/")
        lease_parent = open_artifact(root, parent_path) if parent_path else os.dup(root)
        lease_parent_facts = os.fstat(lease_parent)
        lease = os.open(name, FILE_FLAGS, dir_fd=lease_parent)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(lease_facts.st_size == 0 and not lease_facts.st_mode & 0o077 and
                type(record["lease_device"]) is int and type(record["lease_inode"]) is int and
                (record["lease_device"], record["lease_inode"]) == identity(lease_facts),
                "initial creation lease differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        initial = scan(root, set())
        require([entry["path"] for entry in initial if entry["kind"] == "regular_file"] ==
                [lease_path], "product writes already started")
        plan = {entry["path"]: entry["kind"] for entry in record["declared_entries"]}
        require(all(plan.get(entry["path"]) == entry["kind"] for entry in initial),
                "unknown initial descendant")
        os.fsync(parent)
        os.fsync(build)

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) ==
                    identity(parent_facts), "creation record directory replaced")
            current, payload, facts = read_initial(parent, artifact_id)
            require(current == record and payload == original and version(facts) == version(prior),
                    "prior creation record changed")
            rebound = open_artifact(build, artifact)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "artifact replaced")
            finally:
                os.close(rebound)
            current_parent = open_artifact(root, parent_path) if parent_path else os.dup(root)
            try:
                require(identity(os.fstat(current_parent)) == identity(lease_parent_facts) and
                        version(os.stat(name, dir_fd=current_parent, follow_symlinks=False)) ==
                        version(lease_facts), "creation lease binding changed")
            finally:
                os.close(current_parent)
            require(version(os.fstat(lease)) == version(lease_facts) and scan(root, set()) == initial,
                    "initial creation tree changed")

        successor = dict(record, phase=Event.phase, revision=Event.revision,
                         previous_revision=Journal.revision,
                         previous_sha256=hashlib.sha256(original).hexdigest())
        payload = (json.dumps(successor, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "creation event size exceeded")
        publish_initial(build, payload, artifact_id + Event.suffix, revalidate)
    finally:
        for fd in (lease, lease_parent, root, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    try:
        start_record(args.project.absolute(), args.artifact, args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio creation start is unverified: " + str(error)) from error
