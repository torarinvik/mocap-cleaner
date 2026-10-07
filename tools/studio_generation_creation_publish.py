"""Publish a sealed executable while retaining both exclusive generation locks."""
import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
from pathlib import Path

from studio_generation_contents import DIRECTORY_FLAGS, FILE_FLAGS, Limits, identity, open_artifact, owned, require, version
from studio_generation_creation import Journal, publish_initial
from studio_generation_creation_start import Event, read_record, read_started
from studio_generation_creation_seal import Seal, verify_build_seal
from studio_generation_lock import verified_lock


class Publication:
    phase = "published"
    revision = 4
    suffix = ".revision-4.json"
    temporary = "current-executable"
    destination = "mocap_studio"


def publish(project, artifact, artifact_id):
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", artifact_id), "invalid artifact ID")
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    parent = root = lease = -1
    namespace_published = False
    temporary_facts = None
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
                    (initial[prefix + "_device"], initial[prefix + "_inode"]) == identity(facts), "artifact identity differs")
        lease = os.open(".studio-generation.lease", FILE_FLAGS, dir_fd=root)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(type(initial["lease_device"]) is int and type(initial["lease_inode"]) is int and
                (initial["lease_device"], initial["lease_inode"]) == identity(lease_facts), "lease identity differs")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sealed = verify_build_seal(project, artifact, artifact_id, root)
        require(version(lease_facts) == version(sealed[5]), "lease changed during verification")
        seal_record, seal_payload, seal_facts = read_record(parent, artifact_id + Seal.suffix)
        expected = dict(initial, phase=Seal.phase, revision=Seal.revision, previous_revision=Event.revision,
                        previous_sha256=hashlib.sha256(started_payload).hexdigest(), executable_sha256=sealed[0],
                        contents_inventory_sha256=sealed[1], input_record_sha256=hashlib.sha256(sealed[2]).hexdigest(),
                        lease_record_sha256=hashlib.sha256(sealed[4]).hexdigest())
        require(seal_record == expected and type(seal_record.get("revision")) is int and
                type(seal_record.get("previous_revision")) is int, "sealed event differs")
        prior = ((artifact_id + ".json", initial_payload, initial_facts),
                 (artifact_id + Event.suffix, started_payload, started_facts),
                 (artifact_id + Seal.suffix, seal_payload, seal_facts))
        target = artifact + "/mocap_studio"

        def revalidate():
            verified_lock(project, os.environ)
            require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) == identity(parent_facts),
                    "creation directory replaced")
            for filename, expected_payload, expected_facts in prior:
                _, payload, facts = read_record(parent, filename)
                require(payload == expected_payload and version(facts) == version(expected_facts), "prior event changed")
            rebound = open_artifact(build, artifact)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "artifact replaced")
            finally:
                os.close(rebound)
            current = verify_build_seal(project, artifact, artifact_id, root)
            require(current[:3] == sealed[:3] and version(current[3]) == version(sealed[3]) and
                    current[4] == sealed[4] and version(current[5]) == version(sealed[5]) and
                    version(os.fstat(lease)) == version(lease_facts), "sealed product changed")
            if namespace_published:
                facts = os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
                require(version(facts) == version(temporary_facts) and stat.S_ISLNK(facts.st_mode) and
                        os.readlink(Publication.destination, dir_fd=build) == target, "published pointer changed")

        revalidate()
        try:
            previous = os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
        except FileNotFoundError:
            previous = None
        if previous is not None:
            require(previous.st_uid == os.getuid() and previous.st_nlink == 1 and
                    (stat.S_ISLNK(previous.st_mode) or stat.S_ISREG(previous.st_mode)), "unsupported existing output")
            if stat.S_ISREG(previous.st_mode):
                owned(previous)
        os.symlink(target, Publication.temporary, dir_fd=root)
        temporary_facts = os.stat(Publication.temporary, dir_fd=root, follow_symlinks=False)
        try:
            current_previous = os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
        except FileNotFoundError:
            current_previous = None
        require((previous is None and current_previous is None) or
                (previous is not None and current_previous is not None and version(previous) == version(current_previous)),
                "existing output changed before publication")
        require(identity(os.stat(Publication.temporary, dir_fd=root, follow_symlinks=False)) == identity(temporary_facts),
                "temporary pointer replaced")
        os.replace(Publication.temporary, Publication.destination, src_dir_fd=root, dst_dir_fd=build)
        namespace_published = True
        # Rename may change ctime; capture the destination and verify its original inode.
        published_facts = os.stat(Publication.destination, dir_fd=build, follow_symlinks=False)
        require(identity(published_facts) == identity(temporary_facts), "published pointer identity differs")
        temporary_facts = published_facts
        os.fsync(root)
        os.fsync(build)
        revalidate()
        record = dict(seal_record, phase=Publication.phase, revision=Publication.revision,
                      previous_revision=Seal.revision, previous_sha256=hashlib.sha256(seal_payload).hexdigest(),
                      current_relative_path=Publication.destination)
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "publication event size exceeded")
        publish_initial(build, payload, artifact_id + Publication.suffix, revalidate)
    except (OSError, ValueError, KeyError, TypeError) as error:
        state = "publication uncertain; retain current pointer and generation" if namespace_published else "publication not recorded; retain generation"
        raise ValueError(state + ": " + str(error)) from error
    finally:
        # Never remove a replaced temporary pointer or roll back a published result.
        if temporary_facts is not None and not namespace_published and root >= 0:
            try:
                facts = os.stat(Publication.temporary, dir_fd=root, follow_symlinks=False)
                if identity(facts) == identity(temporary_facts):
                    os.unlink(Publication.temporary, dir_fd=root)
                    os.fsync(root)
            except OSError:
                pass
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
        publish(args.project.absolute(), args.artifact, args.artifact_id)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit("Studio generation publication: " + str(error)) from error
