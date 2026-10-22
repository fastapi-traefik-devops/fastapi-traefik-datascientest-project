import copy
import unittest
from unittest.mock import patch
import stage_acceptance as observer


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.request = {'status': 'promoted', 'sha': 'a' * 40, 'digests': {'backend': 'sha256:' + 'b' * 64, 'frontend': 'sha256:' + 'c' * 64}, 'infrastructure_commit': 'd' * 40}
        self.app = {'spec': {'source': {'repoURL': observer.REPO + '.git', 'path': 'kubernetes/apps/liora/overlays/stage', 'targetRevision': 'main'}, 'destination': {'namespace': 'app-stage'}}, 'status': {'sync': {'status': 'Synced', 'revision': 'e' * 40}, 'health': {'status': 'Healthy'}}}
        self.deployments, self.pods = {}, {'items': []}
        for n in observer.COMPONENTS:
            image = observer.REGISTRY + n + ':sha-' + self.request['sha'] + '@' + self.request['digests'][n]
            self.deployments[n] = {'metadata': {'generation': 2}, 'spec': {'replicas': 1, 'selector': {'matchLabels': {'app': n}}, 'template': {'spec': {'containers': [{'name': n, 'image': image}]}}}, 'status': {'observedGeneration': 2, 'updatedReplicas': 1, 'availableReplicas': 1, 'replicas': 1}}
            self.pods['items'].append({'metadata': {'uid': n, 'labels': {'app': n}}, 'spec': {'containers': [{'name': n, 'image': image}]}, 'status': {'phase': 'Running', 'conditions': [{'type': 'Ready', 'status': 'True'}], 'containerStatuses': [{'name': n, 'ready': True, 'imageID': observer.REGISTRY + n + '@' + self.request['digests'][n]}]}})

    def inspect(self):
        return observer.inspect(self.request, self.app, self.deployments, self.pods)[0]

    def test_checks_running_ids_not_only_desired_images(self):
        self.assertTrue(all(self.inspect().values()))
        self.pods['items'][0]['status']['containerStatuses'][0]['imageID'] = 'sha256:' + 'f' * 64
        self.assertFalse(self.inspect()['running_images'])

    def test_unready_extra_or_old_replica_blocks_acceptance(self):
        for mutation in ('unready', 'extra', 'old-generation'):
            with self.subTest(mutation=mutation):
                original = copy.deepcopy((self.pods, self.deployments))
                if mutation == 'unready': self.pods['items'][0]['status']['containerStatuses'][0]['ready'] = False
                elif mutation == 'extra': self.pods['items'].append(copy.deepcopy(self.pods['items'][0]))
                else: self.deployments['backend']['status']['observedGeneration'] = 1
                self.assertFalse(self.inspect()['running_images'])
                self.pods, self.deployments = original

    def test_wrong_argo_source_or_health_blocks_acceptance(self):
        self.app['status']['health']['status'] = 'Progressing'
        self.assertFalse(self.inspect()['argo'])
        self.app['status']['health']['status'] = 'Healthy'
        self.app['spec']['source']['path'] = 'legacy/stage'
        self.assertFalse(self.inspect()['argo'])

    def get(self, path):
        if 'applications/' in path: return self.app
        if 'deployments/' in path: return self.deployments[path.rsplit('/', 1)[-1]]
        return self.pods

    def test_complete_acceptance_and_interstitial_rejection(self):
        fetch = lambda url: b'<html><div id="root"></div></html>' if url.endswith('/') and 'health-check' not in url else b'true'
        result = observer.observe(self.request, self.get, fetch, timeout=0)
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(result['sha'], self.request['sha'])
        result = observer.observe(self.request, self.get, lambda url: b'Access login', timeout=0)
        self.assertEqual(result['status'], 'failed')

    def test_timeout_and_error_do_not_leak_tokens_or_bodies(self):
        def failed(path): raise RuntimeError('fixture-secret-token')
        result = observer.observe(self.request, failed, failed, timeout=0)
        self.assertEqual(result['status'], 'failed')
        self.assertNotIn('fixture-secret-token', str(result))


if __name__ == '__main__':
    unittest.main()
