"""Append a durable failure event for an owned, unsealed build generation.

This records builder failure and exact observed descendants, not cleanup
eligibility. Unknown entries, a nonempty lease or uncertain identities refuse.
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
    scan, version,
)
from studio_generation_creation import Journal, publish_initial
from studio_generation_creation_start import Event, read_initial, read_record
from studio_generation_lock import verified_lock


class Failure:
    phase = "failed"
    revision = 3
    suffix = ".revision-3.json"
    max_exit_status = 255


def record_failure(project, artifact, artifact_id, exit_status):
    require(type(exit_status) is int and 0 < exit_status <= Failure.max_exit_status,
            "failure requires a nonzero bounded exit status")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", artifact_id), "invalid artifact ID")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = root = lease = -1
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build directory replaced")
        parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation directory is not private")
        initial, initial_payload, initial_facts = read_initial(parent, artifact_id)
        require(initial["artifact_kind"] == "studio-build" and
                initial["original_relative_path"] == artifact, "not the original build artifact")
        started, started_payload, started_facts = read_record(parent, artifact_id + Event.suffix)
        expected_started = dict(initial, phase=Event.phase, revision=Event.revision,
                                previous_revision=Journal.revision,
                                previous_sha256=hashlib.sha256(initial_payload).hexdigest())
        require(started == expected_started and type(started.get("revision")) is int and
                type(started.get("previous_revision")) is int, "invalid creation start chain")
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(initial[prefix + "_device"]) is int and type(initial[prefix + "_inode"]) is int and
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts),
                    "failure artifact root identity differs")
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=root)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(lease_facts.st_size == 0 and not lease_facts.st_mode & 0o077 and
                type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(lease_facts),
                "failure requires the original unsealed private lease")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        observed = scan(root, set(), durable=True)
        plan = {entry["path"]: entry["kind"] for entry in initial["declared_entries"]}
        require(all(plan.get(entry["path"]) == entry["kind"] for entry in observed),
                "failed tree contains unknown descendants")
        os.fsync(parent)
        os.fsync(build)

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) ==
                    identity(parent_facts), "creation directory replaced")
            for filename, expected_payload, expected_facts in (
                    (artifact_id + ".json", initial_payload, initial_facts),
                    (artifact_id + Event.suffix, started_payload, started_facts)):
                _, payload, facts = read_record(parent, filename)
                require(payload == expected_payload and version(facts) == version(expected_facts),
                        "prior journal event changed")
            rebound = open_artifact(build, artifact)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "failure artifact replaced")
                require(version(os.stat(".studio-generation.lease", dir_fd=rebound,
                                        follow_symlinks=False)) == version(lease_facts),
                        "failure lease binding changed")
            finally:
                os.close(rebound)
            require(version(os.fstat(lease)) == version(lease_facts) and
                    scan(root, set()) == observed, "failed tree changed before event publication")

        event = dict(initial, phase=Failure.phase, revision=Failure.revision,
                     previous_revision=Event.revision,
                     previous_sha256=hashlib.sha256(started_payload).hexdigest(),
                     failure_exit_status=exit_status, observed_entries=observed)
        payload = (json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "failure event size exceeded")
        publish_initial(build, payload, artifact_id + Failure.suffix, revalidate)
    finally:
        for fd in (lease, root, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--failure-status", type=int, required=True)
    args = parser.parse_args()
    try:
        record_failure(args.project.absolute(), args.artifact, args.artifact_id, args.failure_status)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio failure ownership is unverified; retain generation: " + str(error)) from error
