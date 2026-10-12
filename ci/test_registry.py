import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import registry
from phase1 import STEPS, file_sha


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.sha = "a" * 40
        for component in ("backend", "frontend"):
            (self.directory / f"{component}-ci.tar").write_bytes(component.encode())
        self.manifest = {"version": 1, "sha": self.sha, "gates": list(set(STEPS) - {"attest"}),
                         "archives": {name: file_sha(self.directory / f"{name}-ci.tar") for name in ("backend", "frontend")}}
        self.write()
        (self.directory / "source-sha.txt").write_text(self.sha)

    def write(self):
        (self.directory / "gates.json").write_text(json.dumps(self.manifest))

    def test_successful_gates_and_archive_integrity(self):
        self.assertEqual(registry.validate(self.directory, self.sha)["sha"], self.sha)

    def test_missing_security_gate_blocks_publication(self):
        self.manifest["gates"].remove("backend-image-security")
        self.write()
        with self.assertRaisesRegex(ValueError, "CI gates"):
            registry.validate(self.directory, self.sha)

    def test_forged_source_revision_blocks_publication(self):
        with self.assertRaisesRegex(ValueError, "SCM revision"):
            registry.validate(self.directory, "b" * 40)

    def test_modified_archive_blocks_publication(self):
        (self.directory / "backend-ci.tar").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "integrity"):
            registry.validate(self.directory, self.sha)

    def test_registry_authentication_failure_is_not_missing_image(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "UNAUTHORIZED")):
            with self.assertRaisesRegex(RuntimeError, "lookup failed"):
                registry.digest("crane", "example.invalid/image:tag")

    def test_existing_sha_tag_cannot_be_overwritten(self):
        with patch.object(subprocess, "check_output", return_value="sha256:" + "a" * 64), \
             patch.object(registry, "digest", return_value="sha256:" + "b" * 64), \
             patch.object(subprocess, "run") as mutation:
            with self.assertRaisesRegex(RuntimeError, "overwrite"):
                registry.publish(self.directory, self.sha, "example.invalid/team")
            mutation.assert_not_called()

    def test_matching_existing_artifacts_are_idempotent(self):
        with patch.object(subprocess, "check_output", return_value="sha256:" + "a" * 64), \
             patch.object(registry, "digest", return_value="sha256:" + "a" * 64), \
             patch.object(subprocess, "run") as mutation:
            registry.publish(self.directory, self.sha, "example.invalid/team")
            mutation.assert_not_called()


if __name__ == "__main__":
    unittest.main()
