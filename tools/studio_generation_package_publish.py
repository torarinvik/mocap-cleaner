"""Publish a current package under retained global and artifact locks.

After a namespace move, failures preserve both generations for reconciliation.
The Published event is emitted only after the new bundle and parents are durable.
"""
import argparse
import ctypes
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
from studio_generation_package_seal import verify_package_seal
from studio_generation_lock import verified_lock


class Publication:
    phase = "published"
    revision = 4
    suffix = ".revision-4.json"
    destination = "MocapStudio.app"
    backup = "previous.app"
    intent_suffix = ".publication-intent.json"
    fields = ("executable_sha256", "contents_inventory_sha256", "package_record_sha256",
              "input_record_sha256", "lease_record_sha256", "build_generation_id")
    facts = ("metadata_facts", "inputs_facts", "lease_facts")
    rename_exclusive = 0x00000004


def rename_exclusive(source_parent, source, destination_parent, destination):
    # Darwin sys/stdio.h: RENAME_EXCL refuses every preexisting destination.
    # There is no check-then-overwrite fallback on unsupported hosts/filesystems.
    library = ctypes.CDLL(None, use_errno=True)
    function = getattr(library, "renameatx_np", None)
    require(function is not None, "exclusive package rename is unavailable")
    function.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    function.restype = ctypes.c_int
    if function(source_parent, os.fsencode(source), destination_parent,
                os.fsencode(destination), Publication.rename_exclusive) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), destination)


def publish_package(project, artifact, artifact_id):
    require(re.fullmatch(r"studio-package\.[A-Za-z0-9_-]+", artifact_id), "invalid package ID")
    require(artifact == artifact_id + "/MocapStudio.app", "unsupported original package path")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = pending = root = resources = lease = old_root = old_resources = old_lease = -1
    namespace_changed = False
    current_path = artifact
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build directory replaced")
        parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation directory is not private")
        initial, initial_payload, initial_facts, started_payload, started_facts = read_started(parent, artifact_id)
        require(initial["artifact_kind"] == "studio-package" and initial["original_relative_path"] == artifact,
                "not the original package")
        pending = open_artifact(build, artifact_id)
        pending_facts = os.fstat(pending)
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        for prefix, facts in (("build_root", locked_build), ("root", root_facts)):
            require(type(initial[prefix + "_device"]) is int and type(initial[prefix + "_inode"]) is int and
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts), "package root differs")
        resources = open_artifact(root, "Contents/Resources")
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=resources)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(lease_facts), "package lease differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sealed = verify_package_seal(project, artifact, artifact_id, root)
        require(version(lease_facts) == version(sealed["lease_facts"]), "package lease changed")
        seal_record, seal_payload, seal_facts = read_record(parent, artifact_id + Seal.suffix)
        expected = dict(initial, phase=Seal.phase, revision=Seal.revision, previous_revision=Event.revision,
                        previous_sha256=hashlib.sha256(started_payload).hexdigest())
        for key in Publication.fields:
            expected[key] = sealed[key]
        require(seal_record == expected and type(seal_record.get("revision")) is int and
                type(seal_record.get("previous_revision")) is int, "package sealed event differs")
        try:
            os.stat(artifact_id + Publication.suffix, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("Published event already exists; reconcile before retry")
        try:
            os.stat(artifact_id + Publication.intent_suffix, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("publication intent already exists; reconcile before retry")
        try:
            os.stat(Publication.backup, dir_fd=pending, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("backup already exists; reconcile interrupted publication")
        prior = ((artifact_id + ".json", initial_payload, initial_facts),
                 (artifact_id + Event.suffix, started_payload, started_facts),
                 (artifact_id + Seal.suffix, seal_payload, seal_facts))

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) == identity(parent_facts),
                    "creation directory replaced")
            require(identity(os.stat(artifact_id, dir_fd=build, follow_symlinks=False)) == identity(pending_facts),
                    "pending directory replaced")
            for filename, payload_expected, facts_expected in prior:
                _, payload, facts = read_record(parent, filename)
                require(payload == payload_expected and version(facts) == version(facts_expected), "prior event changed")
            rebound = open_artifact(build, current_path)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "published package replaced")
            finally:
                os.close(rebound)
            current = verify_package_seal(project, current_path, artifact_id, root)
            for key in Publication.fields + ("resource_identity",):
                require(current[key] == sealed[key], "package seal changed")
            for key in Publication.facts:
                require(version(current[key]) == version(sealed[key]), "package controls changed")
            require(version(os.fstat(lease)) == version(lease_facts), "held package lease changed")
            if old_root >= 0:
                old_parent = pending if namespace_changed else build
                old_name = Publication.backup if namespace_changed else Publication.destination
                require(identity(os.stat(old_name, dir_fd=old_parent, follow_symlinks=False)) ==
                        identity(os.fstat(old_root)), "previous package binding replaced")
                rebound_old_resources = open_artifact(old_root, "Contents/Resources")
                try:
                    require(identity(os.fstat(rebound_old_resources)) == identity(old_resources_facts) and
                            version(os.stat(".studio-generation.lease", dir_fd=rebound_old_resources,
                            follow_symlinks=False)) == version(old_facts) and
                            version(os.fstat(old_lease)) == version(old_facts), "previous package lease replaced")
                finally:
                    os.close(rebound_old_resources)
                old_path = artifact_id + "/" + Publication.backup if namespace_changed else Publication.destination
                current_old = verify_package_seal(project, old_path, old_id, old_root)
                for key in Publication.fields + ("resource_identity",):
                    require(current_old[key] == old_sealed[key], "previous package seal changed")
                for key in Publication.facts:
                    require(version(current_old[key]) == version(old_sealed[key]), "previous package controls changed")


        revalidate()
        try:
            previous = os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
        except FileNotFoundError:
            previous = None
        if previous is not None:
            owned(previous, directory=True)
            require(identity(previous) != identity(root_facts), "package is already current; reconcile")
            old_root = open_artifact(build, Publication.destination)
            require(identity(os.fstat(old_root)) == identity(previous), "previous package replaced")
            old_resources = open_artifact(old_root, "Contents/Resources")
            old_resources_facts = os.fstat(old_resources)
            old_lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=old_resources)
            old_facts = os.fstat(old_lease)
            owned(old_facts)
            require(not old_facts.st_mode & 0o222 and old_facts.st_size > 0, "previous package lease is unsealed")
            fcntl.flock(old_lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            old_metadata, _, _ = read_record(old_resources, "PACKAGE-GENERATION.json", private=False)
            require(isinstance(old_metadata, dict) and isinstance(old_metadata.get("package_generation_id"), str) and
                    re.fullmatch(r"studio-package\.[A-Za-z0-9_-]+", old_metadata["package_generation_id"]),
                    "previous package generation identity is unavailable")
            old_id = old_metadata["package_generation_id"]
            old_sealed = verify_package_seal(project, Publication.destination, old_id, old_root)
            require(version(os.stat(".studio-generation.lease", dir_fd=old_resources, follow_symlinks=False)) ==
                    version(old_facts) and identity(os.stat(Publication.destination, dir_fd=build,
                    follow_symlinks=False)) == identity(previous), "previous package binding changed")
        intent = dict(seal_record, phase="publication-intent", revision=Publication.revision,
                      previous_revision=Seal.revision, previous_sha256=hashlib.sha256(seal_payload).hexdigest(),
                      current_relative_path=Publication.destination)
        if previous is not None:
            intent.update(previous_root_device=previous.st_dev, previous_root_inode=previous.st_ino,
                          previous_relative_path=artifact_id + "/" + Publication.backup,
                          previous_lease_device=old_facts.st_dev, previous_lease_inode=old_facts.st_ino)
            intent["previous_package_generation_id"] = old_id
            for key in Publication.fields:
                intent["previous_" + key] = old_sealed[key]
        intent_payload = (json.dumps(intent, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(intent_payload) <= Limits.json_bytes, "publication intent size exceeded")
        publish_initial(build, intent_payload, artifact_id + Publication.intent_suffix, revalidate)
        intent_record, durable_intent_payload, intent_facts = read_record(parent, artifact_id + Publication.intent_suffix)
        require(intent_record == intent and durable_intent_payload == intent_payload, "durable intent differs")
        prior += ((artifact_id + Publication.intent_suffix, intent_payload, intent_facts),)
        revalidate()
        if previous is not None:
            require(identity(os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)) == identity(previous) and
                    version(os.fstat(old_lease)) == version(old_facts), "previous bundle changed before move")
            rename_exclusive(build, Publication.destination, pending, Publication.backup)
            namespace_changed = True
            os.fsync(pending)
            os.fsync(build)
        else:
            require(not os.path.lexists(project / "build" / Publication.destination), "current package appeared")
        # The global lock serializes cooperating builders. Never overwrite an
        # observed replacement target, even if it is an empty directory.
        try:
            os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("current package appeared before rename")
        require(identity(os.stat("MocapStudio.app", dir_fd=pending, follow_symlinks=False)) == identity(root_facts),
                "pending package replaced")
        rename_exclusive(pending, "MocapStudio.app", build, Publication.destination)
        namespace_changed = True
        current_path = Publication.destination
        os.fsync(pending)
        os.fsync(build)
        revalidate()
        record = dict(seal_record, phase=Publication.phase, revision=Publication.revision,
                      previous_revision=Seal.revision, previous_sha256=hashlib.sha256(seal_payload).hexdigest(),
                      current_relative_path=Publication.destination,
                      publication_intent_sha256=hashlib.sha256(intent_payload).hexdigest())
        if previous is not None:
            record.update(previous_root_device=previous.st_dev, previous_root_inode=previous.st_ino,
                          previous_relative_path=artifact_id + "/" + Publication.backup)
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "Published event size exceeded")
        publish_initial(build, payload, artifact_id + Publication.suffix, revalidate)
    except (OSError, ValueError, KeyError, TypeError) as error:
        state = "package publication uncertain; retain current and backup for reconciliation" if namespace_changed else "package publication refused; retain generation"
        # Only undo the first namespace move. Once the new bundle became
        # current, preserve both generations for explicit reconciliation.
        if namespace_changed and current_path == artifact and old_root >= 0:
            try:
                revalidate()
                try:
                    os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise ValueError("current destination occupied; previous package cannot be restored")
                rename_exclusive(pending, Publication.backup, build, Publication.destination)
                namespace_changed = False
                os.fsync(pending)
                os.fsync(build)
                revalidate()
                state = "publication interrupted; verified previous package restored, new generation retained for reconciliation"
            except (OSError, ValueError, KeyError, TypeError) as rollback_error:
                state = "publication and previous-package restoration require reconciliation: " + str(rollback_error)
        raise ValueError(state + ": " + str(error)) from error
    finally:
        for fd in (old_lease, old_resources, old_root, lease, resources, root, pending, parent, build):
            if fd >= 0:
                os.close(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    try:
        publish_package(args.project.absolute(), args.artifact, args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio package publication: " + str(error)) from error
