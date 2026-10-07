"""Serialize cooperating Studio build, package and future cleanup clients."""
import fcntl
import os
import stat
import subprocess
import sys
from pathlib import Path


LOCK_NAME = ".studio-generation.lock"
FD_ENV = "MOCAP_STUDIO_GENERATION_LOCK_FD"
LOCK_DEVICE_ENV = "MOCAP_STUDIO_GENERATION_LOCK_DEVICE"
LOCK_INODE_ENV = "MOCAP_STUDIO_GENERATION_LOCK_INODE"
BUILD_DEVICE_ENV = "MOCAP_STUDIO_GENERATION_BUILD_DEVICE"
BUILD_INODE_ENV = "MOCAP_STUDIO_GENERATION_BUILD_INODE"
VERIFIED_ENV = "MOCAP_STUDIO_GENERATION_LOCK_VERIFIED"


def fail(message):
    print("Studio generation lock: " + message, file=sys.stderr)
    raise SystemExit(2)


def same_identity(left, right):
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def open_build_directory(project):
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = -1
    try:
        project_fd = os.open(project, flags)
        try:
            try:
                os.mkdir("build", mode=0o700, dir_fd=project_fd)
            except FileExistsError:
                pass
            fd = os.open("build", flags, dir_fd=project_fd)
        finally:
            os.close(project_fd)
        facts = os.fstat(fd)
        path_facts = os.stat(project / "build", follow_symlinks=False)
    except OSError as error:
        if fd >= 0:
            os.close(fd)
        fail("build directory could not be opened without following symlinks: " + str(error))
    if not stat.S_ISDIR(facts.st_mode) or facts.st_uid != os.getuid() or not same_identity(facts, path_facts):
        os.close(fd)
        fail("build directory identity or owner is not verified")
    return fd, facts


def inspect_lock(fd, project, build_fd, build_facts):
    try:
        facts = os.fstat(fd)
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        path_facts = os.stat(LOCK_NAME, dir_fd=build_fd, follow_symlinks=False)
    except OSError as error:
        fail("lock descriptor or path could not be verified: " + str(error))
    if flags & os.O_ACCMODE != os.O_RDWR:
        fail("lock descriptor is not open read/write")
    if (not stat.S_ISREG(facts.st_mode) or facts.st_uid != os.getuid() or
            facts.st_nlink != 1 or facts.st_mode & 0o077 or
            not same_identity(facts, path_facts)):
        fail("lock file is foreign, linked, writable by others, or replaced")
    try:
        current_build = os.stat(project / "build", follow_symlinks=False)
    except OSError as error:
        fail("build directory path could not be rechecked: " + str(error))
    if not same_identity(build_facts, current_build):
        fail("build directory changed while verifying the lock")
    return facts


def inherited_lock(project, environment):
    try:
        fd = int(environment[FD_ENV], 10)
        expected_lock = (int(environment[LOCK_DEVICE_ENV], 10), int(environment[LOCK_INODE_ENV], 10))
        expected_build = (int(environment[BUILD_DEVICE_ENV], 10), int(environment[BUILD_INODE_ENV], 10))
    except (KeyError, ValueError):
        fail("inherited lock metadata is incomplete or malformed")
    if fd < 0:
        fail("inherited lock descriptor is invalid")
    build_fd, build_facts = open_build_directory(project)
    if (build_facts.st_dev, build_facts.st_ino) != expected_build:
        os.close(build_fd)
        fail("inherited lock belongs to another build directory")
    try:
        facts = inspect_lock(fd, project, build_fd, build_facts)
        if (facts.st_dev, facts.st_ino) != expected_lock:
            fail("inherited lock descriptor belongs to another lock file")
        # The descriptor must carry the exclusive advisory lock. With an
        # inherited descriptor, this succeeds on the same open file
        # description, but refuses a different process's lock holder.
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        inspect_lock(fd, project, build_fd, build_facts)
    except OSError as error:
        fail("inherited descriptor does not hold the exclusive lock: " + str(error))
    finally:
        os.close(build_fd)
    return fd, build_facts, facts


def acquire_lock(project):
    build_fd, build_facts = open_build_directory(project)
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    previous_mask = os.umask(0o077)
    try:
        try:
            fd = os.open(LOCK_NAME, flags, 0o600, dir_fd=build_fd)
        except OSError as error:
            os.close(build_fd)
            fail("lock file could not be created without following symlinks: " + str(error))
    finally:
        os.umask(previous_mask)
    keep_fd = False
    try:
        facts = inspect_lock(fd, project, build_fd, build_facts)
        fcntl.flock(fd, fcntl.LOCK_EX)
        facts = inspect_lock(fd, project, build_fd, build_facts)
        keep_fd = True
        return fd, build_facts, facts
    except OSError as error:
        fail("exclusive lock acquisition failed: " + str(error))
    finally:
        os.close(build_fd)
        if not keep_fd:
            os.close(fd)


def verified_lock(project, environment):
    if environment.get(VERIFIED_ENV) != "1":
        fail("lock descriptor was not passed by the build wrapper")
    return inherited_lock(project, environment)


def run(project, command):
    if not command:
        fail("run requires a command after --")
    inherited_keys = (FD_ENV, LOCK_DEVICE_ENV, LOCK_INODE_ENV, BUILD_DEVICE_ENV, BUILD_INODE_ENV, VERIFIED_ENV)
    if any(key in os.environ for key in inherited_keys):
        if os.environ.get(VERIFIED_ENV) != "1":
            fail("stale or unverified inherited lock metadata")
        fd, build_facts, lock_facts = verified_lock(project, os.environ)
        owns_lock = False
    else:
        fd, build_facts, lock_facts = acquire_lock(project)
        owns_lock = True
    child_environment = os.environ.copy()
    child_environment.update({
        FD_ENV: str(fd),
        LOCK_DEVICE_ENV: str(lock_facts.st_dev),
        LOCK_INODE_ENV: str(lock_facts.st_ino),
        BUILD_DEVICE_ENV: str(build_facts.st_dev),
        BUILD_INODE_ENV: str(build_facts.st_ino),
        VERIFIED_ENV: "1",
    })
    os.set_inheritable(fd, True)
    try:
        completed = subprocess.run(command, env=child_environment, pass_fds=(fd,), check=False)
        return completed.returncode
    finally:
        if owns_lock:
            os.close(fd)


def main(arguments):
    project = Path(__file__).resolve().parent.parent
    if len(arguments) == 1 and arguments[0] == "check":
        verified_lock(project, os.environ)
        return 0
    if len(arguments) >= 3 and arguments[0] == "run" and arguments[1] == "--":
        return run(project, arguments[2:])
    fail("usage: studio_generation_lock.py check | run -- command [args...]")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
