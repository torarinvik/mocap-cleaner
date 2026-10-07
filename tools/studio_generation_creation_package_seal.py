"""Append Building -> Sealed after verifying the complete current package seal.

This event does not establish current publication, inactivity or cleanup
eligibility. Both exclusive locks remain held through durable publication.
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path

from studio_generation_contents import (
    DIRECTORY_FLAGS, FILE_FLAGS, Limits, hash_file, identity, open_artifact,
    owned, require, verify_record, version,
)
from studio_generation_creation import Journal, publish_initial
from studio_generation_creation_start import Event, read_record, read_started
from studio_generation_lock import verified_lock
from studio_generation_package_seal import verify_package_seal


class Seal:
    phase = "sealed"
    revision = 3
    suffix = ".revision-3.json"
    lease_protocol = 1


def record_package_seal(project, artifact, artifact_id):
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", artifact_id), "invalid artifact ID")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = root = resources = lease = -1
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build directory replaced")
        parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation directory is not private")
        initial, initial_payload, initial_facts, started_payload, started_facts = read_started(parent, artifact_id)
        require(initial["artifact_kind"] == "studio-package" and initial["original_relative_path"] == artifact,
                "not the original package artifact")
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(initial[prefix + "_device"]) is int and type(initial[prefix + "_inode"]) is int and
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts),
                    "seal artifact root identity differs")
        resources = open_artifact(root, "Contents/Resources")
        resources_facts = os.fstat(resources)
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=resources)
        opened_lease = os.fstat(lease)
        owned(opened_lease)
        require(type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(opened_lease),
                "seal lease identity differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sealed = verify_package_seal(project, artifact, artifact_id, root)
        require(version(opened_lease) == version(sealed["lease_facts"]), "lease changed during seal validation")
        os.fsync(parent)
        os.fsync(build)

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) ==
                    identity(parent_facts), "creation journal directory replaced")
            for filename, expected_payload, expected_facts in (
                    (artifact_id + ".json", initial_payload, initial_facts),
                    (artifact_id + Event.suffix, started_payload, started_facts)):
                _, payload, facts = read_record(parent, filename)
                require(payload == expected_payload and version(facts) == version(expected_facts),
                        "prior creation event changed")
            rebound = open_artifact(build, artifact)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "seal artifact replaced")
            finally:
                os.close(rebound)
            current = verify_package_seal(project, artifact, artifact_id, root)
            for key in ("executable_sha256", "contents_inventory_sha256", "package_record_sha256",
                        "input_record_sha256", "lease_record_sha256", "build_generation_id", "resource_identity"):
                require(current[key] == sealed[key], "package seal changed during event publication")
            for key in ("metadata_facts", "inputs_facts", "lease_facts"):
                require(version(current[key]) == version(sealed[key]), "package control changed during event publication")
            require(identity(os.fstat(resources)) == identity(resources_facts) and
                    version(os.fstat(lease)) == version(opened_lease), "held package lease changed")

        record = dict(initial, phase=Seal.phase, revision=Seal.revision,
                      previous_revision=Event.revision,
                      previous_sha256=hashlib.sha256(started_payload).hexdigest())
        for key in ("executable_sha256", "contents_inventory_sha256", "package_record_sha256",
                    "input_record_sha256", "lease_record_sha256", "build_generation_id"):
            record[key] = sealed[key]
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "seal event size exceeded")
        publish_initial(build, payload, artifact_id + Seal.suffix, revalidate)
    finally:
        for fd in (lease, resources, root, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    try:
        record_package_seal(args.project.absolute(), args.artifact, args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio package creation seal is unverified; retain generation: " + str(error)) from error
