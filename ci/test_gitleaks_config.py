"""Exercise the real scanner against narrow checksum allowances and negative fixtures."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get('GITLEAKS_BINARY') or shutil.which('gitleaks')
PROVENANCE = 'docs/backend-api-evidence-2026-10-24/evidence/provenance.json'
DIGEST = hashlib.sha256(b'public OpenAPI fixture').hexdigest()


@unittest.skipUnless(BINARY, 'Gitleaks binary required; set GITLEAKS_BINARY or use the CI agent')
class EvidenceAllowlistTests(unittest.TestCase):
    def scan(self, relative, text, *, defaults=False, history=False):
        with tempfile.TemporaryDirectory(prefix='gitleaks-policy-test-') as temp:
            temp = Path(temp)
            source = temp / 'source'
            source.mkdir()
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            config = ROOT / '.gitleaks.toml'
            if defaults:
                config = temp / 'defaults.toml'
                config.write_text('[extend]\nuseDefault = true\n')
            if history:
                for args in [
                    ['git', 'init', '--quiet', str(source)],
                    ['git', '-C', str(source), 'add', '.'],
                    ['git', '-C', str(source), '-c', 'user.name=Fixture',
                     '-c', 'user.email=fixture@example.invalid', 'commit', '--quiet', '-m', 'Public fixture'],
                ]:
                    subprocess.run(args, check=True, capture_output=True)
            report = temp / 'report.json'
            result = subprocess.run([
                BINARY, 'git' if history else 'dir', str(source), '--redact=100',
                '--no-banner', '--ignore-gitleaks-allow', '--config', str(config),
                '--report-format', 'json', '--report-path', str(report),
            ], cwd=ROOT, capture_output=True, text=True)
            self.assertIn(result.returncode, (0, 1), 'Scanner failed: ' + result.stderr)
            findings = json.loads(report.read_text())
            return result.returncode, findings

    def fixture(self, key, value=DIGEST):
        return json.dumps({key: value}, indent=2) + '\n'

    def test_default_rule_reproduces_the_hash_false_positive(self):
        code, findings = self.scan(PROVENANCE, self.fixture('openapi.dev.json'), defaults=True)
        self.assertEqual(code, 1)
        self.assertIn('generic-api-key', {f['RuleID'] for f in findings})

    def test_both_exact_openapi_capture_keys_are_allowed(self):
        for key in ('openapi.dev.json', 'openapi.stage-prod.json'):
            with self.subTest(key=key):
                self.assertEqual(self.scan(PROVENANCE, self.fixture(key)), (0, []))

    def test_existing_response_digest_field_is_allowed(self):
        path = 'docs/backend-api-evidence-2026-10-24/evidence/results/dev-private.json'
        self.assertEqual(self.scan(path, self.fixture('openapi_response_sha256')), (0, []))

    def test_unrelated_file_remains_scanned(self):
        code, _ = self.scan('docs/unrelated.json', self.fixture('openapi.dev.json'))
        self.assertEqual(code, 1)

    def test_filename_key_not_allowed_in_other_evidence_files(self):
        path = 'docs/backend-api-evidence-2026-10-24/evidence/access-policy.json'
        code, _ = self.scan(path, self.fixture('openapi.dev.json'))
        self.assertEqual(code, 1)

    def test_other_key_is_not_exempted_in_provenance(self):
        value = base64.b64encode(hashlib.sha256(b'non-secret regression fixture').digest()).decode()
        code, _ = self.scan(PROVENANCE, self.fixture('api_key', value))
        self.assertEqual(code, 1)

    def test_secret_shaped_value_is_not_exempted_by_capture_key(self):
        # Generated nonfunctional fixture, never an issued credential.
        value = 'gh' + 'p_' + hashlib.sha256(b'not-an-issued-token').hexdigest()[:36]
        code, findings = self.scan(PROVENANCE, self.fixture('openapi.dev.json', value))
        self.assertEqual(code, 1)
        self.assertIn('github-pat', {f['RuleID'] for f in findings})

    def test_same_line_extra_secret_remains_scanned(self):
        value = base64.b64encode(hashlib.sha256(b'inline regression fixture').digest()).decode()
        text = '{"openapi.dev.json": "' + DIGEST + '", "api_key": "' + value + '"}\n'
        code, _ = self.scan(PROVENANCE, text)
        self.assertEqual(code, 1)

    def test_history_scan_accepts_the_same_exact_digest_line(self):
        self.assertEqual(self.scan(PROVENANCE, self.fixture('openapi.dev.json'), history=True), (0, []))


if __name__ == '__main__':
    unittest.main(verbosity=2)
