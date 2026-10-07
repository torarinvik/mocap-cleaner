"""Finish only an already-published, exactly identified package after interruption.

No bundle is moved or removed. Pending, conflicting, busy or unknown layouts
refuse. This command requires the verified global build lock wrapper.
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path

from studio_generation_contents import DIRECTORY_FLAGS, FILE_FLAGS, Limits, identity, open_artifact, owned, require, version
from studio_generation_creation import Journal, publish_initial
from studio_generation_creation_start import Event, read_record, read_started
from studio_generation_creation_package_seal import Seal
from studio_generation_package_publish import Publication
from studio_generation_package_seal import verify_package_seal
from studio_generation_lock import verified_lock


class Recovery:
    previous_fields = frozenset(("previous_root_device", "previous_root_inode", "previous_relative_path",
        "previous_lease_device", "previous_lease_inode", "previous_package_generation_id")) | frozenset(
        "previous_" + field for field in Publication.fields)


def reconcile_published(project, artifact_id):
    require(re.fullmatch(r"studio-package\.[A-Za-z0-9_-]+", artifact_id), "invalid package ID")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = pending = root = resources = lease = old_root = old_resources = old_lease = -1
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build root replaced")
        parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation directory is not private")
        initial, initial_payload, initial_facts, started_payload, started_facts = read_started(parent, artifact_id)
        require(initial["artifact_kind"] == "studio-package" and
                initial["original_relative_path"] == artifact_id + "/MocapStudio.app", "unsupported original package")
        pending = open_artifact(build, artifact_id)
        pending_facts = os.fstat(pending)
        root = open_artifact(build, Publication.destination)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(initial[prefix + "_device"]) is int and type(initial[prefix + "_inode"]) is int and
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts), "current package identity differs")
        try:
            os.stat("MocapStudio.app", dir_fd=pending, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("original package path is occupied; reconcile conflicting layout")
        resources = open_artifact(root, "Contents/Resources")
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=resources)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(lease_facts), "current lease identity differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sealed = verify_package_seal(project, Publication.destination, artifact_id, root)
        require(version(lease_facts) == version(sealed["lease_facts"]), "current lease changed")
        seal_record, seal_payload, seal_facts = read_record(parent, artifact_id + Seal.suffix)
        expected_seal = dict(initial, phase=Seal.phase, revision=Seal.revision, previous_revision=Event.revision,
                             previous_sha256=hashlib.sha256(started_payload).hexdigest())
        for key in Publication.fields:
            expected_seal[key] = sealed[key]
        require(seal_record == expected_seal and type(seal_record.get("revision")) is int and
                type(seal_record.get("previous_revision")) is int, "sealed event differs")
        intent, intent_payload, intent_facts = read_record(parent, artifact_id + Publication.intent_suffix)
        require(isinstance(intent, dict), "intent is not an object")
        expected_intent = dict(seal_record, phase="publication-intent", revision=Publication.revision,
                               previous_revision=Seal.revision, previous_sha256=hashlib.sha256(seal_payload).hexdigest(),
                               current_relative_path=Publication.destination)
        has_previous = bool(set(intent) & Recovery.previous_fields)
        if has_previous:
            require(Recovery.previous_fields <= set(intent), "incomplete previous package intent")
            for key in Recovery.previous_fields:
                expected_intent[key] = intent[key]
        require(intent == expected_intent and type(intent.get("revision")) is int and
                type(intent.get("previous_revision")) is int, "unsupported publication intent")
        if has_previous:
            old_path = artifact_id + "/" + Publication.backup
            require(intent["previous_relative_path"] == old_path and
                    isinstance(intent["previous_package_generation_id"], str) and
                    re.fullmatch(r"studio-package\.[A-Za-z0-9_-]+", intent["previous_package_generation_id"]),
                    "unsupported previous package identity")
            old_root = open_artifact(build, old_path)
            old_root_facts = os.fstat(old_root)
            old_resources = open_artifact(old_root, "Contents/Resources")
            old_lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=old_resources)
            old_lease_facts = os.fstat(old_lease)
            owned(old_lease_facts)
            for prefix, facts in (("previous_root", old_root_facts), ("previous_lease", old_lease_facts)):
                require(type(intent[prefix + "_device"]) is int and type(intent[prefix + "_inode"]) is int and
                        (intent[prefix + "_device"], intent[prefix + "_inode"]) == identity(facts), "previous package identity differs")
            fcntl.flock(old_lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            old_sealed = verify_package_seal(project, old_path, intent["previous_package_generation_id"], old_root)
            for key in Publication.fields:
                require(intent["previous_" + key] == old_sealed[key], "previous package seal differs from intent")
            require(version(old_lease_facts) == version(old_sealed["lease_facts"]), "previous lease changed")
        else:
            try:
                os.stat(Publication.backup, dir_fd=pending, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise ValueError("unexpected previous package backup")
        prior = ((artifact_id + ".json", initial_payload, initial_facts),
                 (artifact_id + Event.suffix, started_payload, started_facts),
                 (artifact_id + Seal.suffix, seal_payload, seal_facts),
                 (artifact_id + Publication.intent_suffix, intent_payload, intent_facts))

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) == identity(parent_facts) and
                    identity(os.stat(artifact_id, dir_fd=build, follow_symlinks=False)) == identity(pending_facts),
                    "recovery parent replaced")
            for filename, expected_payload, expected_facts in prior:
                _, payload, facts = read_record(parent, filename)
                require(payload == expected_payload and version(facts) == version(expected_facts), "prior event changed")
            require(identity(os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)) == identity(root_facts),
                    "current package replaced")
            current = verify_package_seal(project, Publication.destination, artifact_id, root)
            for key in Publication.fields + ("resource_identity",):
                require(current[key] == sealed[key], "current seal changed")
            for key in Publication.facts:
                require(version(current[key]) == version(sealed[key]), "current controls changed")
            require(version(os.fstat(lease)) == version(lease_facts), "held current lease changed")
            try:
                os.stat("MocapStudio.app", dir_fd=pending, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise ValueError("original package path became occupied")
            if has_previous:
                current_old = verify_package_seal(project, old_path, intent["previous_package_generation_id"], old_root)
                for key in Publication.fields + ("resource_identity",):
                    require(current_old[key] == old_sealed[key], "previous seal changed")
                for key in Publication.facts:
                    require(version(current_old[key]) == version(old_sealed[key]), "previous controls changed")
                require(version(os.fstat(old_lease)) == version(old_lease_facts), "held previous lease changed")
            else:
                try:
                    os.stat(Publication.backup, dir_fd=pending, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise ValueError("unexpected backup appeared")

        os.fsync(root)
        os.fsync(pending)
        os.fsync(build)
        revalidate()
        record = dict(seal_record, phase=Publication.phase, revision=Publication.revision,
                      previous_revision=Seal.revision, previous_sha256=hashlib.sha256(seal_payload).hexdigest(),
                      current_relative_path=Publication.destination,
                      publication_intent_sha256=hashlib.sha256(intent_payload).hexdigest())
        if has_previous:
            for key in ("previous_root_device", "previous_root_inode", "previous_relative_path"):
                record[key] = intent[key]
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "Published event size exceeded")
        try:
            existing, existing_payload, existing_facts = read_record(parent, artifact_id + Publication.suffix)
        except FileNotFoundError:
            publish_initial(build, payload, artifact_id + Publication.suffix, revalidate)
        else:
            require(existing == record and existing_payload == payload, "existing Published event differs")
            os.fsync(parent)
            os.fsync(build)
            revalidate()
            _, again_payload, again_facts = read_record(parent, artifact_id + Publication.suffix)
            require(again_payload == payload and version(again_facts) == version(existing_facts), "Published event changed")
    finally:
        for fd in (old_lease, old_resources, old_root, lease, resources, root, pending, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    try:
        reconcile_published(args.project.absolute(), args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio package reconciliation unverified; retain all generations: " + str(error)) from error
