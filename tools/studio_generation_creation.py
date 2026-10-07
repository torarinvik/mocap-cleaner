"""Register initial generation ownership before any product output is written.

This infrastructure records Created only. Later journal transitions and native
cleanup consumption must be integrated separately; a record is not eligibility.
"""
import argparse
import fcntl
import json
import os
import re
import secrets
from pathlib import Path

from studio_generation_contents import (
    CONTROLS, DIRECTORY_FLAGS, FILE_FLAGS, Limits, identity, open_artifact,
    owned, relative_path, require, scan, version,
)
from studio_generation_lock import verified_lock


class Journal:
    directory = ".studio-generation-creations"
    schema = "mocap-studio-generation-creation-v1"
    phase = "created"
    revision = 1


def declared_plan(files, directories, kind):
    require(len(files) + len(directories) <= Limits.entries, "declared path limit exceeded")
    entries = {}
    for paths, entry_kind in ((directories, "directory"), (files, "regular_file")):
        for path in paths:
            relative_path(path)
            require(path not in entries, "duplicate declared path")
            entries[path] = entry_kind
    for path in entries:
        parts = relative_path(path)
        for count in range(1, len(parts)):
            require(entries.get("/".join(parts[:count])) == "directory",
                    "declared path has an undeclared directory ancestor")
    require(all(entries.get(path) == "regular_file" for path in CONTROLS[kind]),
            "creation plan must declare every generation control")
    return entries


def publish_initial(build, payload, filename, revalidate):
    try:
        os.mkdir(Journal.directory, 0o700, dir_fd=build)
    except FileExistsError:
        pass
    parent = os.open(Journal.directory, DIRECTORY_FLAGS, dir_fd=build)
    temporary = ".pending-" + secrets.token_hex(16)
    linked = False
    temporary_identity = None

    def remove_temporary():
        try:
            named = os.stat(temporary, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return
        require(temporary_identity is not None and identity(named) == temporary_identity,
                "temporary creation journal replaced; preserve unknown entry")
        os.unlink(temporary, dir_fd=parent)

    try:
        parent_facts = os.fstat(parent)
        owned(parent_facts, directory=True)
        require(not parent_facts.st_mode & 0o077, "creation journal directory is not private")
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent)
        temporary_identity = identity(os.fstat(fd))
        try:
            remaining = memoryview(payload)
            while remaining:
                count = os.write(fd, remaining)
                require(count > 0, "creation journal write made no progress")
                remaining = remaining[count:]
            os.fsync(fd)
            written = os.fstat(fd)
        finally:
            os.close(fd)
        revalidate()
        require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) ==
                identity(parent_facts), "creation journal directory replaced")
        os.link(temporary, filename, src_dir_fd=parent, dst_dir_fd=parent,
                follow_symlinks=False)
        linked = True
        named = os.stat(filename, dir_fd=parent, follow_symlinks=False)
        require(identity(named) == identity(written) and named.st_nlink == 2,
                "creation journal replaced during publication")
        remove_temporary()
        named = os.stat(filename, dir_fd=parent, follow_symlinks=False)
        require(identity(named) == identity(written) and named.st_nlink == 1,
                "creation journal replaced after removing temporary link")
        os.fsync(parent)
        os.fsync(build)
        revalidate()
        require(identity(os.stat(Journal.directory, dir_fd=build, follow_symlinks=False)) ==
                identity(parent_facts), "creation journal directory changed after publication")
        require(version(os.stat(filename, dir_fd=parent, follow_symlinks=False)) == version(named),
                "creation journal changed after publication")
    except (OSError, ValueError) as error:
        if linked:
            raise ValueError("creation journal publication is uncertain; retain and inspect " +
                             Journal.directory + "/" + filename) from error
        raise
    finally:
        try:
            remove_temporary()
        finally:
            os.close(parent)


def create_record(project, artifact, artifact_id, kind, files, directories):
    require(kind in CONTROLS, "unknown artifact kind")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", artifact_id),
            "invalid artifact ID")
    plan = declared_plan(files, directories, kind)
    _, locked_build, _ = verified_lock(project, os.environ)
    build = os.open(project / "build", DIRECTORY_FLAGS)
    root = lease_parent = lease = -1
    try:
        require(identity(os.fstat(build)) == identity(locked_build), "build directory replaced")
        root = open_artifact(build, artifact)
        root_facts = os.fstat(root)
        owned(root_facts, directory=True)
        lease_relative = (".studio-generation.lease" if kind == "studio-build" else
                          "Contents/Resources/.studio-generation.lease")
        parent_path, _, lease_name = lease_relative.rpartition("/")
        lease_parent = open_artifact(root, parent_path) if parent_path else os.dup(root)
        lease_parent_facts = os.fstat(lease_parent)
        owned(lease_parent_facts, directory=True)
        lease = os.open(lease_name, FILE_FLAGS, dir_fd=lease_parent)
        lease_facts = os.fstat(lease)
        owned(lease_facts)
        require(lease_facts.st_size == 0 and not lease_facts.st_mode & 0o077,
                "initial lease must be empty and private")
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        initial = scan(root, set(), durable=True)
        require(all(plan.get(entry["path"]) == entry["kind"] for entry in initial),
                "initial tree contains undeclared paths")
        require([entry["path"] for entry in initial if entry["kind"] == "regular_file"] ==
                [lease_relative], "creation registration must precede all product writes")

        def revalidate():
            verified_lock(project, os.environ)
            rebound = open_artifact(build, artifact)
            try:
                require(identity(os.fstat(rebound)) == identity(root_facts), "artifact replaced")
            finally:
                os.close(rebound)
            current_parent = open_artifact(root, parent_path) if parent_path else os.dup(root)
            try:
                require(identity(os.fstat(current_parent)) == identity(lease_parent_facts),
                        "initial lease ancestor replaced")
                require(version(os.stat(lease_name, dir_fd=current_parent, follow_symlinks=False)) ==
                        version(lease_facts), "current initial lease replaced")
            finally:
                os.close(current_parent)
            require(version(os.fstat(lease)) == version(lease_facts), "initial lease changed")
            require(version(os.stat(lease_name, dir_fd=lease_parent, follow_symlinks=False)) ==
                    version(lease_facts), "initial lease replaced")
            require(scan(root, set()) == initial, "initial tree changed during registration")

        record = {
            "schema": Journal.schema, "artifact_id": artifact_id, "artifact_kind": kind,
            "phase": Journal.phase, "revision": Journal.revision,
            "operation_id": secrets.token_hex(16), "original_relative_path": artifact,
            "build_root_device": locked_build.st_dev, "build_root_inode": locked_build.st_ino,
            "root_device": root_facts.st_dev, "root_inode": root_facts.st_ino,
            "lease_device": lease_facts.st_dev, "lease_inode": lease_facts.st_ino,
            "declared_entries": [{"path": path, "kind": plan[path]} for path in sorted(plan)],
        }
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "creation journal JSON limit exceeded")
        publish_initial(build, payload, artifact_id + ".json", revalidate)
    finally:
        for fd in (lease, lease_parent, root, build):
            if fd >= 0:
                os.close(fd)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--kind", choices=CONTROLS, required=True)
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--directory", action="append", default=[])
    args = parser.parse_args()
    create_record(args.project.absolute(), args.artifact, args.artifact_id,
                  args.kind, args.file, args.directory)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit("Studio creation ownership is unverified: " + str(error)) from error
