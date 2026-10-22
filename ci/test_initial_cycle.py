"""Exercise candidate -> immutable publication -> split-repository STAGE update."""
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import candidate
from phase1 import PROFILES, TEST_REPORTS
import registry
import test_promote as fixtures


class InitialCycleTests(unittest.TestCase):
    def test_initial_cycle_needs_no_observer_and_keeps_prod_blocked(self):
        fixture = fixtures.PromotionTests('test_stage_is_scoped_and_idempotent')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        artifacts = fixture.root / 'artifacts'
        artifacts.mkdir()
        for name in ('backend', 'frontend'):
            (artifacts / f'{name}-ci.tar').write_bytes(('tested-runtime-' + name).encode())
        for filename in TEST_REPORTS.values():
            (artifacts / filename).write_text('<testsuite tests="2" failures="0" errors="0"/>')
        candidate.write_candidate(artifacts, fixture.sha, PROFILES['migration'], 'app-ci/main', '4')
        remote_images = {}
        def archive_digest(args, **kwargs):
            self.assertEqual(args[:3], ['crane', 'digest', '--tarball'])
            name = Path(args[3]).name.removesuffix('-ci.tar')
            return fixture.pair[name] + '\n'
        def command(args, *a, **kwargs):
            if args[0] != 'crane':
                return fixtures.REAL_RUN(args, *a, **kwargs)
            self.assertEqual(args[1], 'push')
            name = Path(args[2]).name.removesuffix('-ci.tar')
            remote_images[args[3]] = fixture.pair[name]
            return subprocess.CompletedProcess(args, 0, '', '')
        with patch.object(registry, 'digest', side_effect=lambda tool, image: remote_images.get(image)), \
             patch.object(registry.subprocess, 'check_output', side_effect=archive_digest), \
             patch.object(registry.subprocess, 'run', side_effect=command):
            registry.publish(artifacts, fixture.sha, 'ghcr.io/fastapi-traefik-devops',
                             mode='functional', source_job='app-ci/main', source_build='4')
            published = json.loads((artifacts / 'published-images.json').read_text())
            self.assertEqual({n: v['digest'] for n, v in published.items()}, fixture.pair)
            result = fixture.invoke('stage')
        self.assertEqual(result['status'], 'promoted')
        recorded = json.loads(fixture.show('kubernetes/apps/liora/overlays/stage/promotion.json'))
        self.assertEqual(recorded['sha'], fixture.sha)
        self.assertEqual(recorded['digests'], fixture.pair)
        files = fixture.show('kubernetes/apps/liora/overlays/stage/kustomization.yaml')
        for digest in fixture.pair.values(): self.assertIn(digest, files)
        # A desired-state update is not accepted-deployment evidence.
        with self.assertRaisesRegex(RuntimeError, 'PROD is blocked'):
            fixture.invoke('prod', release='v1.2.0')
