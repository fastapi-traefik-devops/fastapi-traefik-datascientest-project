"""Exercise Git promotion against a temporary bare remote; never contact GitHub/GHCR."""
import contextlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import promote

REAL_RUN = subprocess.run
ROOT = Path(__file__).resolve().parents[1]


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote.git'
        self.work = self.root / 'work'
        promote.git('init', '--bare', '--initial-branch=main', str(self.remote))
        promote.git('clone', str(self.remote), str(self.work))
        promote.git('config', 'user.email', 'test@example.com', cwd=self.work)
        promote.git('config', 'user.name', 'Test', cwd=self.work)
        shutil.copytree(ROOT / 'deploy', self.work / 'deploy')
        # Fixtures must not inherit real environment promotion history/digests.
        for overlay in (self.work / 'deploy/overlays').iterdir():
            (overlay / 'promotion.json').unlink(missing_ok=True)
            path = overlay / 'kustomization.yaml'
            content = re.sub(r'^  digest: .*\n', '', path.read_text(), flags=re.M)
            content = re.sub(r'^  newTag: .*$', '  newTag: sha-' + '0' * 40, content, flags=re.M)
            path.write_text(content)
        (self.work / 'source.py').write_text('version = 1\n')
        self.sha = self.commit('Initial application')
        self.digests = {n: 'sha256:' + c * 64 for n, c in [('backend', 'a'), ('frontend', 'b')]}
        self.registry = {f'{promote.REGISTRY}{n}:sha-{self.sha}': d for n, d in self.digests.items()}
        self.addCleanup(patch.stopall)
        patch.object(promote, 'REPO', str(self.remote)).start()
        patch.object(promote, 'digest', side_effect=lambda image: self.registry[image]).start()

    def commit(self, message):
        promote.git('add', '.', cwd=self.work)
        promote.git('commit', '-qm', message, cwd=self.work)
        promote.git('push', '-q', 'origin', 'main', cwd=self.work)
        return promote.git('rev-parse', 'HEAD', cwd=self.work)

    def invoke(self, environment, sha=None, release=None):
        argv = ['promote.py', environment, sha or self.sha]
        if release:
            argv += ['--release', release]
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
            promote.main()

    def show(self, branch, path):
        return promote.git('--git-dir', str(self.remote), 'show', f'{branch}:{path}')

    def test_stage_records_exact_pair_and_is_idempotent(self):
        self.invoke('stage')
        path = 'deploy/overlays/stage/promotion.json'
        self.assertEqual(json.loads(self.show('main', path))['digests'], self.digests)
        head = promote.git('--git-dir', str(self.remote), 'rev-parse', 'main')
        self.invoke('stage')
        self.assertEqual(promote.git('--git-dir', str(self.remote), 'rev-parse', 'main'), head)
        overlay = self.show('main', 'deploy/overlays/stage/kustomization.yaml')
        self.assertIn('sha-' + self.sha, overlay)
        self.assertIn(self.digests['backend'], overlay)
        changes = promote.git('--git-dir', str(self.remote), 'diff-tree', '--root', '--first-parent', '-m',
                              '--no-commit-id', '--name-only', '-r', 'main').splitlines()
        self.assertTrue(changes)
        self.assertTrue(all(path.startswith('deploy/') for path in changes))

    def test_stale_stage_build_cannot_overwrite_new_source(self):
        (self.work / 'source.py').write_text('version = 2\n')
        newer = self.commit('New source')
        self.invoke('stage')
        self.assertEqual(promote.git('--git-dir', str(self.remote), 'rev-parse', 'main'), newer)

    def test_unrelated_main_commit_survives_push_retry(self):
        raced = False

        def race(args, *a, **kw):
            nonlocal raced
            if args[:3] == ['git', 'push', 'origin'] and not raced:
                raced = True
                (self.work / 'notes.md').write_text('Concurrent human update\n')
                self.commit('Concurrent documentation')
            return REAL_RUN(args, *a, **kw)

        with patch.object(subprocess, 'run', side_effect=race):
            self.invoke('stage')
        self.assertTrue(raced)
        self.assertEqual(self.show('main', 'notes.md'), 'Concurrent human update')
        self.assertEqual(json.loads(self.show('main', 'deploy/overlays/stage/promotion.json'))['sha'], self.sha)

    def test_missing_images_fail_before_git_write(self):
        self.registry.clear()
        with self.assertRaises(KeyError):
            self.invoke('stage')
        self.assertEqual(promote.git('--git-dir', str(self.remote), 'rev-parse', 'main'), self.sha)

    def test_dev_changes_only_dev(self):
        self.invoke('dev')
        self.assertEqual(json.loads(self.show('main', 'deploy/overlays/dev/promotion.json'))['sha'], self.sha)
        self.assertNotIn('digest:', self.show('main', 'deploy/overlays/prod/kustomization.yaml'))

    def tag(self):
        promote.git('tag', 'v1.2.0', self.sha, cwd=self.work)
        promote.git('push', '-q', 'origin', 'v1.2.0', cwd=self.work)

    def test_release_requires_stage_history(self):
        self.tag()
        with self.assertRaisesRegex(RuntimeError, 'never been promoted to stage'):
            self.invoke('prod', release='v1.2.0')

    def test_release_creates_only_review_branch_and_reuses_digests(self):
        self.invoke('stage')
        self.tag()
        head = promote.git('--git-dir', str(self.remote), 'rev-parse', 'main')
        for name, value in self.digests.items():
            self.registry[f'{promote.REGISTRY}{name}:v1.2.0'] = value

        def registry_read(args, *a, **kw):
            if args[0] == 'crane':
                self.assertEqual(args[1], 'digest')
                return subprocess.CompletedProcess(args, 0, self.registry[args[2]] + '\n', '')
            return REAL_RUN(args, *a, **kw)

        with patch.object(subprocess, 'run', side_effect=registry_read):
            self.invoke('prod', release='v1.2.0')
            self.invoke('prod', release='v1.2.0')
        self.assertEqual(promote.git('--git-dir', str(self.remote), 'rev-parse', 'main'), head)
        record = json.loads(self.show('release/v1.2.0', 'deploy/overlays/prod/promotion.json'))
        self.assertEqual(record['sha'], self.sha)
        self.assertEqual(record['digests'], self.digests)

    def test_release_refuses_moved_registry_tag(self):
        self.invoke('stage')
        self.tag()

        def registry_read(args, *a, **kw):
            if args[0] == 'crane':
                return subprocess.CompletedProcess(args, 0, 'sha256:' + 'c' * 64, '')
            return REAL_RUN(args, *a, **kw)

        with patch.object(subprocess, 'run', side_effect=registry_read), self.assertRaisesRegex(RuntimeError, 'overwrite existing release tag'):
            self.invoke('prod', release='v1.2.0')

    def test_release_rejects_commit_outside_main(self):
        promote.git('checkout', '-qb', 'feature', cwd=self.work)
        (self.work / 'source.py').write_text('not reviewed\n')
        promote.git('add', '.', cwd=self.work)
        promote.git('commit', '-qm', 'Feature only', cwd=self.work)
        sha = promote.git('rev-parse', 'HEAD', cwd=self.work)
        promote.git('push', '-q', 'origin', 'feature', cwd=self.work)
        for name, value in self.digests.items():
            self.registry[f'{promote.REGISTRY}{name}:sha-{sha}'] = value
        with self.assertRaises(subprocess.CalledProcessError):
            self.invoke('prod', sha, 'v1.2.0')


if __name__ == '__main__':
    unittest.main()
