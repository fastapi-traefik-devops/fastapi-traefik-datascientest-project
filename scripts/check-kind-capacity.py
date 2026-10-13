#!/usr/bin/env python3
"""Conservative local monitoring gate; idle measurements cannot prove CI peak safety."""
import json, subprocess

def run(*args):
    return subprocess.check_output(args, text=True)

available = int(next(x.split()[1] for x in open('/proc/meminfo') if x.startswith('MemAvailable:'))) / 1024
node = json.loads(run('kubectl', '--context', 'kind-fastapi-dev', 'get', 'nodes', '-o', 'json'))['items'][0]
conditions = {c['type']: c['status'] for c in node['status']['conditions']}
for condition in ['MemoryPressure', 'DiskPressure', 'PIDPressure']:
    if conditions.get(condition) != 'False':
        raise SystemExit(f'Capacity gate failed: {condition}')
run('kubectl', '--context', 'kind-fastapi-dev', 'top', 'nodes')
run('kubectl', '--context', 'kind-fastapi-dev', 'top', 'pods', '-A')
# Monitoring requests ~1Gi; retain 2Gi host/CI margin, alongside reviewed CI peak.
if available < 3072:
    raise SystemExit(f'Capacity gate failed: host MemAvailable {available:.0f}Mi < 3072Mi')
container = 'fastapi-dev-control-plane'
limit = int(run('docker', 'inspect', container, '--format', '{{.HostConfig.Memory}}'))
current = int(run('docker', 'exec', container, 'cat', '/sys/fs/cgroup/memory.current'))
maximum = run('docker', 'exec', container, 'cat', '/sys/fs/cgroup/memory.max').strip()
limits = [x for x in [limit, int(maximum) if maximum != 'max' else 0] if x]
if limits and min(limits) - current < 1536 * 1024**2:
    raise SystemExit('Capacity gate failed: kind cgroup has less than 1536Mi headroom')
print(f'Idle capacity gate passed: host available {available:.0f}Mi; CI peak review still required.')
