"""Verify exact package control records and contents without following links.

This establishes a product seal, not publication, inactivity, or cleanup
eligibility. Callers retain the global lock and original artifact lease.
"""
import hashlib
import os
import re

from studio_generation_contents import hash_file, identity, open_artifact, require, verify_record
from studio_generation_creation_start import read_record


class PackageSeal:
    schema = "mocap-studio-package-generation-v2"
    lease_schema = "mocap-studio-artifact-lease-v1"
    input_schema = "mocap-studio-inputs-v2"
    protocol = 1
    resources = "Contents/Resources"
    executables = "Contents/MacOS"


def verify_package_seal(project, artifact, artifact_id, root):
    resources = open_artifact(root, PackageSeal.resources)
    executables = -1
    try:
        resources_facts = os.fstat(resources)
        metadata, metadata_payload, metadata_facts = read_record(resources, "PACKAGE-GENERATION.json", private=False)
        require(isinstance(metadata, dict) and set(metadata) == {
            "schema", "lease_protocol", "package_generation_id", "build_generation_id",
            "executable_sha256", "contents_inventory_sha256",
        }, "unsupported package record fields")
        require(metadata["schema"] == PackageSeal.schema and
                type(metadata["lease_protocol"]) is int and metadata["lease_protocol"] == PackageSeal.protocol and
                metadata["package_generation_id"] == artifact_id, "package identity or protocol differs")
        build_id = metadata["build_generation_id"]
        require(isinstance(build_id, str) and re.fullmatch(r"studio-build\.[A-Za-z0-9_-]+", build_id),
                "package has no current build identity")
        executable_sha = metadata["executable_sha256"]
        require(isinstance(executable_sha, str) and re.fullmatch(r"[0-9a-f]{64}", executable_sha),
                "invalid package executable digest")
        inventory_sha = verify_record(project, artifact, artifact_id, "studio-package")
        require(metadata["contents_inventory_sha256"] == inventory_sha, "package contents seal differs")
        inputs, inputs_payload, inputs_facts = read_record(resources, "BUILD-INPUTS.json", private=False)
        require(isinstance(inputs, dict) and inputs.get("schema") == PackageSeal.input_schema,
                "unsupported copied input record")
        require(inputs.get("product") == {"filename": "mocap_studio", "sha256": executable_sha},
                "copied input executable seal differs")
        generation = inputs.get("generation")
        require(isinstance(generation, dict) and type(generation.get("lease_protocol")) is int and generation == {
            "schema": "mocap-studio-generation-v1", "artifact": "studio-build",
            "id": build_id, "lease_protocol": PackageSeal.protocol,
        }, "copied build generation identity differs")
        lease, lease_payload, lease_facts = read_record(resources, ".studio-generation.lease", private=False)
        require(isinstance(lease, dict) and type(lease.get("lease_protocol")) is int and lease == {
            "schema": PackageSeal.lease_schema, "lease_protocol": PackageSeal.protocol,
            "artifact": "studio-package", "id": artifact_id,
            "executable_sha256": executable_sha, "contents_inventory_sha256": inventory_sha,
        } and not lease_facts.st_mode & 0o222, "package lease differs or is writable")
        executables = open_artifact(root, PackageSeal.executables)
        executable_facts = os.stat("MocapStudio", dir_fd=executables, follow_symlinks=False)
        require(hash_file(executables, "MocapStudio", executable_facts, durable=True) == executable_sha,
                "copied executable differs")
        rebound = open_artifact(root, PackageSeal.resources)
        try:
            require(identity(os.fstat(rebound)) == identity(resources_facts), "package resources replaced")
        finally:
            os.close(rebound)
        return {
            "executable_sha256": executable_sha,
            "contents_inventory_sha256": inventory_sha,
            "package_record_sha256": hashlib.sha256(metadata_payload).hexdigest(),
            "input_record_sha256": hashlib.sha256(inputs_payload).hexdigest(),
            "lease_record_sha256": hashlib.sha256(lease_payload).hexdigest(),
            "build_generation_id": build_id,
            "resource_identity": identity(resources_facts),
            "metadata_facts": metadata_facts,
            "inputs_facts": inputs_facts,
            "lease_facts": lease_facts,
        }
    finally:
        for fd in (executables, resources):
            if fd >= 0:
                os.close(fd)
