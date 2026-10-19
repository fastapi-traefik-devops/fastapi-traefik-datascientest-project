"""No network: run the stage promotion wrapper with a fake crane and a fake promote.py."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHA = 'a' * 40


class PromoteStageTests(unittest.TestCase):
    def run_wrapper(self, **overrides):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            crane = root / 'crane'
            crane.write_text('#!/bin/sh\nprintf "%s %s\\n" "$1" "$(cat)" >> "$CALLS"\n')
            crane.chmod(0o700)
            # Records what promote.py would receive, including what Git's askpass would answer.
            promote = root / 'promote.py'
            promote.write_text('''import os, subprocess, sys
askpass = os.environ["GIT_ASKPASS"]
user = subprocess.check_output([askpass, "Username for 'https://github.com': "], text=True).strip()
password = subprocess.check_output([askpass, "Password for 'https://x@github.com': "], text=True).strip()
with open(os.environ["CALLS"], "a") as calls:
    calls.write(f"promote {' '.join(sys.argv[1:])} user={user} password_ok={password == 'git-token'}\\n")
    calls.write(f"docker_config_set={bool(os.environ.get('DOCKER_CONFIG'))}\\n")
''')
            calls = root / 'calls'
            calls.write_text('')
            env = dict(os.environ, PATH=f'{root}:{os.environ["PATH"]}', CALLS=str(calls),
                       PROMOTE_PY=str(promote), EXPECTED_SOURCE_SHA=SHA, GHCR_USER='ghcr-user',
                       GHCR_TOKEN='ghcr-token', GIT_TOKEN='git-token')
            for key, value in overrides.items():
                if value is None:
                    env.pop(key, None)
                else:
                    env[key] = value
            result = subprocess.run(['sh', str(ROOT / 'ci/promote-stage.sh')], env=env,
                                    text=True, capture_output=True, cwd=root)
            output = result.stdout + result.stderr
            self.assertNotIn('ghcr-token', output)
            self.assertNotIn('git-token', output)
            return result.returncode, calls.read_text().splitlines()

    def test_promotes_the_verified_sha_with_registry_and_git_credentials(self):
        status, calls = self.run_wrapper()
        self.assertEqual(status, 0)
        self.assertIn('auth ghcr-token', calls)
        self.assertIn(f'promote stage {SHA} user=x-access-token password_ok=True', calls)
        self.assertIn('docker_config_set=True', calls)

    def test_missing_git_token_fails_before_any_registry_login(self):
        status, calls = self.run_wrapper(GIT_TOKEN=None)
        self.assertNotEqual(status, 0)
        self.assertEqual(calls, [])

    def test_missing_source_sha_fails(self):
        status, calls = self.run_wrapper(EXPECTED_SOURCE_SHA=None)
        self.assertNotEqual(status, 0)
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
