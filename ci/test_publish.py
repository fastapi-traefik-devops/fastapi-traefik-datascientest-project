"""The obsolete monorepo writer cannot bypass the trusted publisher."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest


class LegacyEntryTests(unittest.TestCase):
    def test_legacy_writer_fails_without_using_or_printing_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(['sh', str(Path(__file__).with_name('publish.sh'))], cwd=directory,
                env=dict(os.environ, GHCR_TOKEN='fixture-ghcr-secret', GIT_TOKEN='fixture-git-secret'),
                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('fixture-ghcr-secret', result.stdout + result.stderr)
        self.assertNotIn('fixture-git-secret', result.stdout + result.stderr)
