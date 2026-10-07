"""Durably seal existing controls while preserving artifact lease inodes."""
import os
import stat


def seal_control(path, text, readonly=False):
    """Flush an existing control record without replacing its lock inode."""
    parent = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    fd = -1
    try:
        parent_facts = os.fstat(parent)
        if parent_facts.st_uid != os.getuid() or parent_facts.st_mode & 0o022:
            raise ValueError("control directory is foreign or writable")
        fd = os.open(path.name, os.O_WRONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     dir_fd=parent)
        facts = os.fstat(fd)
        named = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if (not stat.S_ISREG(facts.st_mode) or facts.st_uid != os.getuid() or
                facts.st_nlink != 1 or facts.st_mode & 0o022 or
                (facts.st_dev, facts.st_ino) != (named.st_dev, named.st_ino)):
            raise ValueError("control record is foreign, linked, writable or replaced")
        os.ftruncate(fd, 0)
        payload = memoryview(text.encode("utf-8"))
        while payload:
            written = os.write(fd, payload)
            if written <= 0:
                raise OSError("control record write made no progress")
            payload = payload[written:]
        if readonly:
            os.fchmod(fd, 0o444)
        os.fsync(fd)
        named = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        after = os.fstat(fd)
        if ((facts.st_dev, facts.st_ino) != (named.st_dev, named.st_ino) or
                after.st_nlink != 1 or after.st_uid != os.getuid() or
                after.st_mode & 0o022):
            raise ValueError("control record identity changed during sealing")
        parent_named = os.stat(path.parent, follow_symlinks=False)
        if (parent_facts.st_dev, parent_facts.st_ino) != (parent_named.st_dev, parent_named.st_ino):
            raise ValueError("control directory changed during sealing")
        os.fsync(parent)
    finally:
        if fd >= 0:
            os.close(fd)
        os.close(parent)
