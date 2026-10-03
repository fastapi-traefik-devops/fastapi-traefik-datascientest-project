"""No network: execute publisher shell with a fake registry client."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublishTests(unittest.TestCase):
    def execute(self, behavior):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / 'crane'
            binary.write_text('''#!/bin/sh
printf '%s\\n' "$1" >> "$CALLS"
case "$1" in
  auth) cat > /dev/null; exit 0 ;;
  digest)
    case "$BEHAVIOR" in
      exists) echo sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
      missing) echo MANIFEST_UNKNOWN >&2; exit 1 ;;
      denied) echo UNAUTHORIZED >&2; exit 1 ;;
    esac ;;
  push) exit 0 ;;
  *) exit 90 ;;
esac
''')
            binary.chmod(0o700)
            calls = root / 'calls'
            env = dict(os.environ, PATH=f'{root}:{os.environ["PATH"]}', CALLS=str(calls),
                       BEHAVIOR=behavior, GHCR_USER='test-user', GHCR_TOKEN='test-token',
                       GIT_USER='test-git', GIT_TOKEN='test-git-token', PROMOTION_MODE='publish',
                       REGISTRY_NAMESPACE='example.invalid', IMAGE_SHA='a' * 40,
                       SOURCE_JOB='app-ci/feature-test')
            result = subprocess.run(['sh', str(ROOT / 'ci/publish.sh')], env=env,
                                    text=True, capture_output=True, cwd=root)
            self.assertNotIn('test-token', result.stdout + result.stderr)
            self.assertNotIn('test-git-token', result.stdout + result.stderr)
            return result.returncode, calls.read_text().splitlines()

    def test_existing_sha_tags_are_never_pushed(self):
        status, calls = self.execute('exists')
        self.assertEqual(status, 0)
        self.assertEqual(calls.count('digest'), 2)
        self.assertNotIn('push', calls)

    def test_missing_tags_copy_both_archives(self):
        status, calls = self.execute('missing')
        self.assertEqual(status, 0)
        self.assertEqual(calls.count('push'), 2)

    def test_auth_error_fails_closed(self):
        status, calls = self.execute('denied')
        self.assertNotEqual(status, 0)
        self.assertNotIn('push', calls)


if __name__ == '__main__':
    unittest.main()
