"""Exercise credential handling with inert trusted helpers and fake Git/registry."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class PublisherActionTests(unittest.TestCase):
    def invoke(self, action='stage', missing=None, newest='a' * 40):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(Path(__file__).with_name('publisher-action.sh'), root)
            (root / 'registry.py').write_text('import os; print("validated candidate")\n')
            (root / 'promote.py').write_text('''import os, subprocess, sys
assert subprocess.check_output([os.environ['GIT_ASKPASS'], 'Password'], text=True).strip() == 'fixture-git-secret'
print('promote ' + ' '.join(sys.argv[1:]))
''')
            for name, body in [('git', 'printf "%s\\trefs/heads/main\\n" "$NEWEST"'), ('crane', 'cat >/dev/null')]:
                (root / name).write_text('#!/bin/sh\n' + body + '\n')
                (root / name).chmod(0o700)
            env = dict(os.environ, PATH=str(root) + ':' + os.environ['PATH'], NEWEST=newest,
                       ACTION=action, EXPECTED_SOURCE_SHA='a' * 40, GHCR_USER='fake',
                       GHCR_TOKEN='fixture-registry-secret', GIT_TOKEN='fixture-git-secret',
                       SOURCE_JOB='migration-ci', CI_BUILD='3')
            if missing: env.pop(missing, None)
            result = subprocess.run(['sh', str(root / 'publisher-action.sh')], cwd=root, env=env, text=True, capture_output=True)
            output = result.stdout + result.stderr
            self.assertNotIn('fixture-git-secret', output)
            self.assertNotIn('fixture-registry-secret', output)
            return result.returncode, output

    def test_stage_validates_then_promotes(self):
        status, output = self.invoke()
        self.assertEqual(status, 0)
        self.assertLess(output.index('validated candidate'), output.index('promote stage'))

    def test_missing_credentials_fail_before_publication(self):
        for name in ('GIT_TOKEN', 'GHCR_TOKEN', 'EXPECTED_SOURCE_SHA'):
            status, output = self.invoke(missing=name)
            self.assertNotEqual(status, 0)
            self.assertNotIn('validated candidate', output)

    def test_superseded_candidate_is_not_published(self):
        status, output = self.invoke(newest='b' * 40)
        self.assertEqual(status, 0)
        self.assertNotIn('validated candidate', output)
        self.assertNotIn('promote stage', output)

    def test_prod_does_not_publish_or_rebuild(self):
        status, output = self.invoke(action='prod')
        self.assertEqual(status, 0)
        self.assertNotIn('validated candidate', output)
        self.assertIn('promote prod', output)
