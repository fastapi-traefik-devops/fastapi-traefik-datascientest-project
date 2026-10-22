#!/usr/bin/env python3
"""Read-only STAGE observer. No GitHub, registry, database or Kubernetes write access."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import ssl
import time
import urllib.request

COMPONENTS = ('backend', 'frontend')
REPO = 'https://github.com/fastapi-traefik-devops/fastapi-traefik-liora-infrastructure'
REGISTRY = 'ghcr.io/fastapi-traefik-devops/fastapi-'


def inspect(request, application, deployments, pods):
    source = application.get('spec', {}).get('source', {})
    status = application.get('status', {})
    argo = (source.get('repoURL', '').removesuffix('.git') == REPO
            and source.get('path') == 'kubernetes/apps/liora/overlays/stage'
            and source.get('targetRevision') == 'main'
            and application.get('spec', {}).get('destination', {}).get('namespace') == 'app-stage'
            and status.get('sync', {}).get('status') == 'Synced'
            and status.get('health', {}).get('status') == 'Healthy'
            and bool(re.fullmatch(r'[0-9a-f]{40}', status.get('sync', {}).get('revision', ''))))
    running = True
    evidence = []
    for name in COMPONENTS:
        deployment = deployments[name]
        spec, state = deployment['spec'], deployment.get('status', {})
        count = spec.get('replicas', 1)
        running &= (count > 0 and state.get('observedGeneration', 0) >= deployment['metadata']['generation']
                    and state.get('updatedReplicas', 0) == count and state.get('availableReplicas', 0) == count
                    and state.get('replicas', 0) == count)
        selector = spec['selector']['matchLabels']
        selected = [p for p in pods['items'] if not p['metadata'].get('deletionTimestamp')
                    and all(p['metadata'].get('labels', {}).get(k) == v for k, v in selector.items())]
        running &= len(selected) == count
        expected = REGISTRY + name + ':sha-' + request['sha'] + '@' + request['digests'][name]
        template = spec['template']['spec']['containers']
        running &= any(c['name'] == name and c['image'] == expected for c in template)
        for pod in selected:
            state = pod.get('status', {})
            ready = any(c.get('type') == 'Ready' and c.get('status') == 'True' for c in state.get('conditions', []))
            containers = {c['name']: c for c in pod['spec']['containers']}
            statuses = {c['name']: c for c in state.get('containerStatuses', [])}
            image_id = statuses.get(name, {}).get('imageID', '')
            # K3s exposes pullable repo@sha256 manifest IDs; config IDs alone do not qualify.
            running &= (ready and state.get('phase') == 'Running' and name in containers
                        and containers[name]['image'] == expected and statuses.get(name, {}).get('ready') is True
                        and image_id.rsplit('@', 1)[-1] == request['digests'][name])
            evidence.append({'component': name, 'uid': pod['metadata']['uid'], 'image_id': image_id})
    return {'argo': bool(argo), 'running_images': bool(running)}, status.get('sync', {}).get('revision', ''), evidence


def smoke(fetch):
    # Check expected application responses, not merely HTTP 200 (e.g. a login interstitial).
    root = fetch('https://stage.liora.aprt.info/').decode()
    health = json.loads(fetch('https://stage.liora.aprt.info/api/v1/utils/health-check/'))
    return ('id="root"' in root or "id='root'" in root) and health is True


def observe(request, get, fetch, timeout=900, interval=10):
    deadline = time.monotonic() + timeout
    record = {'version': 1, 'status': 'failed', 'sha': request['sha'], 'digests': request['digests'],
              'infrastructure_commit': request['infrastructure_commit'],
              'argo_revision': '', 'checks': {'argo': False, 'running_images': False, 'url': False}}
    while True:
        try:
            checks, revision, pods = inspect(request, get('/apis/argoproj.io/v1alpha1/namespaces/argocd/applications/app-stage'),
                {n: get('/apis/apps/v1/namespaces/app-stage/deployments/' + n) for n in COMPONENTS},
                get('/api/v1/namespaces/app-stage/pods'))
            checks['url'] = bool(smoke(fetch)) if all(checks.values()) else False
            record.update(checks=checks, argo_revision=revision, pods=pods)
            if all(checks.values()):
                record['status'] = 'accepted'
                break
        except Exception:
            # No response bodies, tokens or exception details in evidence/logs.
            record['checks'] = {'argo': False, 'running_images': False, 'url': False}
        if time.monotonic() >= deadline:
            break
        time.sleep(min(interval, max(0, deadline - time.monotonic())))
    record['observed_at'] = datetime.now(timezone.utc).isoformat()
    return record


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--request', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=900)
    args = p.parse_args()
    request = json.loads(args.request.read_text())
    if (request.get('status') != 'promoted' or not re.fullmatch(r'[0-9a-f]{40}', request.get('sha', ''))
            or not re.fullmatch(r'[0-9a-f]{40}', request.get('infrastructure_commit', ''))
            or set(request.get('digests', {})) != set(COMPONENTS)
            or not all(re.fullmatch(r'sha256:[0-9a-f]{64}', d) for d in request['digests'].values())):
        p.error('Valid promoted STAGE request required')
    sa = Path('/var/run/secrets/kubernetes.io/serviceaccount')
    context = ssl.create_default_context(cafile=str(sa / 'ca.crt'))
    token = (sa / 'token').read_text().strip()
    def get(path):
        req = urllib.request.Request('https://kubernetes.default.svc' + path,
                                     headers={'Authorization': 'Bearer ' + token})
        with urllib.request.urlopen(req, context=context, timeout=20) as response:
            return json.load(response)
    def fetch(url):
        with urllib.request.urlopen(url, timeout=20) as response:
            if response.status != 200 or response.geturl() != url:
                raise ValueError('Unexpected STAGE HTTP response')
            return response.read(1024 * 1024)
    record = observe(request, get, fetch, args.timeout)
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    return 0 if record['status'] == 'accepted' else 1


if __name__ == '__main__':
    raise SystemExit(main())
