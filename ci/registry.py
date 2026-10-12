#!/usr/bin/env python3
"""Trusted registry-only writer: successful gates, checked archives, write-once SHA tags."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from phase1 import STEPS, file_sha


def validate(directory: Path, expected_sha: str) -> dict:
    manifest = json.loads((directory / "gates.json").read_text())
    sha = manifest.get("sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha != expected_sha:
        raise ValueError("Artifact SHA does not match verified successful Jenkins SCM revision")
    if (directory / "source-sha.txt").read_text().strip() != sha:
        raise ValueError("Conflicting artifact SHA records")
    required = set(STEPS) - {"attest"}
    if manifest.get("version") != 1 or set(manifest.get("gates", [])) != required:
        raise ValueError("Missing or unexpected CI gates")
    for component in ("backend", "frontend"):
        if manifest.get("archives", {}).get(component) != file_sha(directory / f"{component}-ci.tar"):
            raise ValueError("Image archive integrity check failed")
    return manifest


def digest(crane: str, image: str) -> str | None:
    result = subprocess.run([crane, "digest", image], capture_output=True, text=True)
    if result.returncode == 0:
        value = result.stdout.strip()
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
            raise ValueError("Invalid registry digest")
        return value
    if "MANIFEST_UNKNOWN" in result.stderr or "NAME_UNKNOWN" in result.stderr:
        return None
    # Authentication, network and service failures are never interpreted as missing images.
    raise RuntimeError("Registry lookup failed; refusing to publish")


def publish(directory: Path, expected_sha: str, namespace: str, crane: str = "crane"):
    manifest = validate(directory, expected_sha)
    if not re.fullmatch(r"[a-z0-9.-]+(?::[0-9]+)?/[a-z0-9][a-z0-9_./-]*", namespace):
        raise ValueError("Invalid registry namespace")
    results = {}
    for component in ("backend", "frontend"):
        archive = directory / f"{component}-ci.tar"
        expected = subprocess.check_output([crane, "digest", "--tarball", str(archive)], text=True).strip()
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", expected):
            raise ValueError("Invalid image archive digest")
        image = f"{namespace}/fastapi-{component}:sha-{manifest['sha']}"
        existing = digest(crane, image)
        if existing is None:
            subprocess.run([crane, "push", str(archive), image], check=True)
        elif existing != expected:
            raise RuntimeError("Refusing to overwrite an existing SHA tag with different bytes")
        if digest(crane, image) != expected:
            raise RuntimeError("Published image digest verification failed")
        results[component] = {"image": image, "digest": expected}
        print("Verified immutable registry artifact:", image)
    (directory / "published-images.json").write_text(json.dumps(results, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    sha = os.environ["EXPECTED_SOURCE_SHA"]
    # Fail before binding/using registry credentials for incomplete artifacts.
    validate(args.directory, sha)
    namespace = os.environ.get("REGISTRY_NAMESPACE", "ghcr.io/fastapi-traefik-devops")
    with tempfile.TemporaryDirectory(prefix="phase1-registry-auth-") as auth:
        os.chmod(auth, 0o700)
        old = os.environ.get("DOCKER_CONFIG")
        os.environ["DOCKER_CONFIG"] = auth
        try:
            result = subprocess.run(["crane", "auth", "login", namespace.split("/")[0],
                                     "-u", os.environ["GHCR_USER"], "--password-stdin"],
                                    input=os.environ["GHCR_TOKEN"], text=True, capture_output=True)
            if result.returncode:
                raise SystemExit("Registry authentication failed; no credential output retained")
            config = Path(auth) / "config.json"
            if config.exists():
                config.chmod(0o600)
            publish(args.directory, sha, namespace)
        finally:
            if old is None:
                os.environ.pop("DOCKER_CONFIG", None)
            else:
                os.environ["DOCKER_CONFIG"] = old


if __name__ == "__main__":
    main()
