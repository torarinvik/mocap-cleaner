"""Register an explicitly declared Studio product tree under the build lock.

The external record survives quarantine. Control records are verified separately
by cleanup; excluding them avoids a digest cycle when the generation is sealed.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import stat
from pathlib import Path

from studio_generation_lock import verified_lock


class Limits:
    entries = 4096
    depth = 32
    path_bytes = 4095
    json_bytes = 1048576
    file_bytes = 10**15


CONTROLS = {
    "studio-build": {"inputs.json", ".studio-generation.lease"},
    "studio-package": {
        "Contents/Resources/PACKAGE-GENERATION.json",
        "Contents/Resources/BUILD-INPUTS.json",
        "Contents/Resources/.studio-generation.lease",
    },
}
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(facts):
    return facts.st_dev, facts.st_ino


def version(facts):
    return identity(facts), facts.st_size, facts.st_mtime_ns, facts.st_ctime_ns


def relative_path(value):
    parts = value.split("/")
    require(value and len(value.encode("utf-8")) <= Limits.path_bytes,
            "invalid relative path length")
    require(len(parts) <= Limits.depth and all(p not in ("", ".", "..") for p in parts),
            "invalid relative path components")
    require("\x00" not in value, "NUL in relative path")
    return parts


def owned(facts, directory=False):
    require(facts.st_uid == os.getuid(), "foreign owner")
    require(stat.S_ISDIR(facts.st_mode) if directory else stat.S_ISREG(facts.st_mode),
            "unsupported filesystem entry")
    if not directory:
        require(facts.st_nlink == 1, "hard-linked file")


def hash_file(parent, name, facts):
    fd = os.open(name, FILE_FLAGS, dir_fd=parent)
    try:
        opened = os.fstat(fd)
        owned(opened)
        require(version(opened) == version(facts), "file replaced before read")
        digest = hashlib.sha256()
        count = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            require(count <= facts.st_size, "file grew during read")
            digest.update(chunk)
        require(count == facts.st_size and version(os.fstat(fd)) == version(facts),
                "file changed during read")
        require(version(os.stat(name, dir_fd=parent, follow_symlinks=False)) == version(facts),
                "file binding changed during read")
        return digest.hexdigest()
    finally:
        os.close(fd)


def scan(root_fd, controls):
    entries = []
    total = 0

    def walk(fd, prefix, depth):
        nonlocal total
        require(depth <= Limits.depth, "directory depth exceeded")
        before = os.fstat(fd)
        owned(before, directory=True)
        names = sorted(os.listdir(fd))
        require(len(names) <= Limits.entries + len(controls), "directory entry count exceeded")
        for name in names:
            path = prefix + name
            relative_path(path)
            facts = os.stat(name, dir_fd=fd, follow_symlinks=False)
            directory = stat.S_ISDIR(facts.st_mode)
            owned(facts, directory=directory)
            if path in controls:
                require(not directory, "control record is a directory")
                continue
            require(len(entries) < Limits.entries, "entry count exceeded")
            entry = {"path": path, "kind": "directory" if directory else "regular_file"}
            entries.append(entry)
            if directory:
                child = os.open(name, DIRECTORY_FLAGS, dir_fd=fd)
                try:
                    require(identity(os.fstat(child)) == identity(facts), "directory replaced")
                    walk(child, path + "/", depth + 1)
                    require(identity(os.stat(name, dir_fd=fd, follow_symlinks=False)) == identity(facts),
                            "directory binding replaced")
                finally:
                    os.close(child)
            else:
                total += facts.st_size
                require(total <= Limits.file_bytes, "total file size exceeded")
                entry.update(size_bytes=facts.st_size, sha256=hash_file(fd, name, facts))
        require(names == sorted(os.listdir(fd)) and version(before) == version(os.fstat(fd)),
                "directory changed during inventory")

    walk(root_fd, "", 0)
    return sorted(entries, key=lambda entry: entry["path"])


def declared_entries(files, directories, controls):
    expected = {}
    for kind, paths in (("regular_file", files), ("directory", directories)):
        for path in paths:
            relative_path(path)
            require(path not in controls and path not in expected, "duplicate or control declaration")
            expected[path] = kind
    require(len(expected) <= Limits.entries, "too many declared entries")
    return expected


def open_artifact(build_fd, relative):
    current = os.dup(build_fd)
    try:
        for component in relative_path(relative):
            child = os.open(component, DIRECTORY_FLAGS, dir_fd=current)
            os.close(current)
            current = child
            owned(os.fstat(current), directory=True)
        return current
    except BaseException:
        os.close(current)
        raise


def publish(build_fd, filename, payload):
    name = ".studio-generation-inventory"
    try:
        os.mkdir(name, 0o700, dir_fd=build_fd)
        os.fsync(build_fd)
    except FileExistsError:
        pass
    parent = os.open(name, DIRECTORY_FLAGS, dir_fd=build_fd)
    temporary = ".pending-" + secrets.token_hex(16)
    try:
        facts = os.fstat(parent)
        owned(facts, directory=True)
        require(not facts.st_mode & 0o077, "inventory directory permissions are not private")
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(fd)
        finally:
            os.close(fd)
        require(identity(os.stat(name, dir_fd=build_fd, follow_symlinks=False)) == identity(facts),
                "inventory directory replaced")
        os.link(temporary, filename, src_dir_fd=parent, dst_dir_fd=parent,
                follow_symlinks=False)
        os.unlink(temporary, dir_fd=parent)
        os.fsync(parent)
    finally:
        try:
            os.unlink(temporary, dir_fd=parent)
        except FileNotFoundError:
            pass
        os.close(parent)


def verify_record(project, artifact, artifact_id, kind):
    """Verify the external record and return its digest before sealing."""
    _, locked_build, _ = verified_lock(project, os.environ)
    build_fd = os.open(project / "build", DIRECTORY_FLAGS)
    root_fd = parent = fd = -1
    try:
        require(identity(os.fstat(build_fd)) == identity(locked_build), "build directory replaced")
        root_fd = open_artifact(build_fd, artifact)
        root = os.fstat(root_fd)
        parent = os.open(".studio-generation-inventory", DIRECTORY_FLAGS, dir_fd=build_fd)
        owned(os.fstat(parent), directory=True)
        fd = os.open(artifact_id + ".json", FILE_FLAGS, dir_fd=parent)
        facts = os.fstat(fd)
        owned(facts)
        require(facts.st_size <= Limits.json_bytes, "inventory JSON limit exceeded")
        payload = bytearray()
        while len(payload) <= Limits.json_bytes:
            chunk = os.read(fd, min(65536, Limits.json_bytes + 1 - len(payload)))
            if not chunk:
                break
            payload.extend(chunk)
        require(len(payload) == facts.st_size and version(os.fstat(fd)) == version(facts),
                "inventory changed during read")
        record = json.loads(payload)
        expected = {
            "schema": "mocap-studio-generation-inventory-v1",
            "artifact_id": artifact_id, "artifact_kind": kind,
            "root_device": root.st_dev, "root_inode": root.st_ino,
            "build_root_device": locked_build.st_dev, "build_root_inode": locked_build.st_ino,
            "entries": scan(root_fd, CONTROLS[kind]),
        }
        require(record == expected, "inventory differs from current artifact")
        require(version(os.stat(artifact_id + ".json", dir_fd=parent,
                                follow_symlinks=False)) == version(facts), "inventory replaced")
        rebound = open_artifact(build_fd, artifact)
        try:
            require(identity(os.fstat(rebound)) == identity(root), "artifact replaced")
        finally:
            os.close(rebound)
        verified_lock(project, os.environ)
        return hashlib.sha256(payload).hexdigest()
    finally:
        for opened in (fd, parent, root_fd, build_fd):
            if opened >= 0:
                os.close(opened)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--artifact", required=True, help="directory relative to build/")
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--kind", choices=CONTROLS, required=True)
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--directory", action="append", default=[])
    args = parser.parse_args()
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", args.artifact_id),
            "invalid artifact ID")
    project = args.project.absolute()
    _, locked_build, _ = verified_lock(project, os.environ)
    expected = declared_entries(args.file, args.directory, CONTROLS[args.kind])
    build_fd = os.open(project / "build", DIRECTORY_FLAGS)
    root_fd = -1
    try:
        require(identity(os.fstat(build_fd)) == identity(locked_build), "build directory replaced")
        root_fd = open_artifact(build_fd, args.artifact)
        root = os.fstat(root_fd)
        entries = scan(root_fd, CONTROLS[args.kind])
        require({e["path"]: e["kind"] for e in entries} == expected,
                "tree differs from explicitly declared product paths")
        record = {
            "schema": "mocap-studio-generation-inventory-v1",
            "artifact_id": args.artifact_id, "artifact_kind": args.kind,
            "root_device": root.st_dev, "root_inode": root.st_ino,
            "build_root_device": locked_build.st_dev, "build_root_inode": locked_build.st_ino,
            "entries": entries,
        }
        payload = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        require(len(payload) <= Limits.json_bytes, "inventory JSON limit exceeded")
        rebound = open_artifact(build_fd, args.artifact)
        try:
            require(identity(os.fstat(rebound)) == identity(root), "artifact path replaced")
        finally:
            os.close(rebound)
        require(scan(root_fd, CONTROLS[args.kind]) == entries, "tree changed before publication")
        verified_lock(project, os.environ)
        publish(build_fd, args.artifact_id + ".json", payload)
        print(hashlib.sha256(payload).hexdigest())
    finally:
        if root_fd >= 0:
            os.close(root_fd)
        os.close(build_fd)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit("Studio contents inventory: " + str(error)) from error
