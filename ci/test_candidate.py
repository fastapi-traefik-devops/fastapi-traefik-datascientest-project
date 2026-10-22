import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import candidate
import registry
from phase1 import PROFILES, TEST_REPORTS


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.sha = 'a' * 40
        for n in ('backend', 'frontend'):
            (self.directory / f'{n}-ci.tar').write_bytes(n.encode())
        for n in TEST_REPORTS.values():
            (self.directory / n).write_text('<testsuites><testsuite tests="2" failures="0" errors="0"/></testsuites>')
        self.manifest = candidate.write_candidate(self.directory, self.sha, PROFILES['migration'], 'migration-ci', '3')

    def validate(self):
        return candidate.validate_candidate(self.directory, self.sha, 'migration-ci', '3')

    def test_explicit_deferral_is_required(self):
        self.assertFalse(self.validate()['security_scanned'])
        self.assertEqual(len(self.manifest['deferred']), 7)
        with self.assertRaises(FileNotFoundError):
            registry.validate(self.directory, self.sha)
        self.manifest['security_scanned'] = True
        (self.directory / 'candidate.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            self.validate()

    def test_job_and_build_provenance_must_match(self):
        for job, build in [('app-ci/main', '3'), ('migration-ci', '2'), ('untrusted', '3')]:
            with self.assertRaises(ValueError):
                candidate.validate_candidate(self.directory, self.sha, job, build)

    def test_missing_functional_gate_blocks_export(self):
        with self.assertRaises(ValueError):
            candidate.write_candidate(self.directory, self.sha, PROFILES['migration'][:-1], 'migration-ci', '3')

    def test_modified_archive_or_report_fails_before_registry(self):
        for filename in ('frontend-ci.tar', 'backend-unit.xml'):
            original = (self.directory / filename).read_bytes()
            (self.directory / filename).write_bytes(original + b' changed')
            with self.assertRaises(Exception):
                self.validate()
            (self.directory / filename).write_bytes(original)

    def test_failed_or_empty_tests_block_export(self):
        for xml in ('<testsuite tests="0"/>', '<testsuite tests="2" failures="1"/>', '<testsuite tests="2"><error/></testsuite>'):
            (self.directory / 'backend-unit.xml').write_text(xml)
            with self.assertRaises(ValueError):
                candidate.write_candidate(self.directory, self.sha, PROFILES['migration'], 'migration-ci', '3')

    def test_functional_mode_must_be_selected_explicitly(self):
        with patch.object(registry, 'digest', return_value='sha256:' + 'b' * 64), \
             patch.object(registry.subprocess, 'check_output', return_value='sha256:' + 'b' * 64):
            registry.publish(self.directory, self.sha, 'ghcr.io/fixture', mode='functional', source_job='migration-ci', source_build='3')
        self.assertTrue((self.directory / 'published-images.json').exists())


if __name__ == '__main__':
    unittest.main()
