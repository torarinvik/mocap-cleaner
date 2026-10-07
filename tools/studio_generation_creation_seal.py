"""Append Building -> Sealed after verifying the complete build product seal.

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


class Seal:
    phase = "sealed"
    revision = 3
    suffix = ".revision-3.json"
    lease_protocol = 1


def verify_build_seal(project, artifact, artifact_id, root):
    metadata, metadata_payload, metadata_facts = read_record(root, "inputs.json", private=False)
    require(isinstance(metadata, dict) and metadata.get("schema") == "mocap-studio-inputs-v2",
            "unsupported build input schema")
    generation = metadata.get("generation")
    require(isinstance(generation, dict) and type(generation.get("lease_protocol")) is int,
            "invalid generation protocol type")
    require(generation == {
        "schema": "mocap-studio-generation-v1", "artifact": "studio-build",
        "id": artifact_id, "lease_protocol": Seal.lease_protocol,
    }, "build generation identity differs")
    product = metadata.get("product")
    require(isinstance(product, dict) and set(product) == {"filename", "sha256"} and
            product.get("filename") == "mocap_studio" and
            isinstance(product.get("sha256"), str) and
            re.fullmatch(r"[0-9a-f]{64}", product["sha256"]), "invalid executable seal")
    inventory_sha = verify_record(project, artifact, artifact_id, "studio-build")
    require(metadata.get("contents_inventory_sha256") == inventory_sha,
            "build contents inventory seal differs")
    lease_record, lease_payload, lease_facts = read_record(root, ".studio-generation.lease", private=False)
    require(isinstance(lease_record, dict) and type(lease_record.get("lease_protocol")) is int,
            "invalid lease protocol type")
    require(lease_record == {
        "schema": "mocap-studio-artifact-lease-v1", "lease_protocol": Seal.lease_protocol,
        "artifact": "studio-build", "id": artifact_id,
        "executable_sha256": product["sha256"], "contents_inventory_sha256": inventory_sha,
    } and not lease_facts.st_mode & 0o222, "unsupported or writable sealed lease")
    executable_facts = os.stat("mocap_studio", dir_fd=root, follow_symlinks=False)
    require(hash_file(root, "mocap_studio", executable_facts, durable=True) == product["sha256"],
            "executable differs from the product seal")
    return (product["sha256"], inventory_sha, metadata_payload, metadata_facts,
            lease_payload, lease_facts)


def record_seal(project, artifact, artifact_id):
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
        initial, initial_payload, initial_facts, started_payload, started_facts = read_started(parent, artifact_id)
        require(initial["artifact_kind"] == "studio-build" and initial["original_relative_path"] == artifact,
                "not the original build artifact")
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(initial[prefix + "_device"]) is int and type(initial[prefix + "_inode"]) is int and
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts),
                    "seal artifact root identity differs")
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=root)
        opened_lease = os.fstat(lease)
        owned(opened_lease)
        require(type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(opened_lease),
                "seal lease identity differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sealed = verify_build_seal(project, artifact, artifact_id, root)
        require(version(opened_lease) == version(sealed[5]), "lease changed during seal validation")
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
            current = verify_build_seal(project, artifact, artifact_id, root)
            require(current[:3] == sealed[:3] and version(current[3]) == version(sealed[3]) and
                    current[4] == sealed[4] and version(current[5]) == version(sealed[5]) and
                    version(os.fstat(lease)) == version(opened_lease),
                    "product seal changed during event publication")

        record = dict(initial, phase=Seal.phase, revision=Seal.revision,
                      previous_revision=Event.revision,
                      previous_sha256=hashlib.sha256(started_payload).hexdigest(),
                      executable_sha256=sealed[0], contents_inventory_sha256=sealed[1],
                      input_record_sha256=hashlib.sha256(sealed[2]).hexdigest(),
                      lease_record_sha256=hashlib.sha256(sealed[4]).hexdigest())
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "seal event size exceeded")
        publish_initial(build, payload, artifact_id + Seal.suffix, revalidate)
    finally:
        for fd in (lease, root, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    try:
        record_seal(args.project.absolute(), args.artifact, args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio creation seal is unverified; retain generation: " + str(error)) from error
