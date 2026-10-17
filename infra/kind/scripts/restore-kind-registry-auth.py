#!/usr/bin/env python3
"""Restore only existing ghcr.io Docker auth into app-dev/app-stage.

Uses host Docker credentials as provided, without printing or writing plaintext YAML.
For a new engineer, configure a package-reader credential with docker login first.
"""
import base64,json,subprocess,sys
from pathlib import Path
namespaces=sys.argv[1:] or ['app-dev','app-stage']
if not set(namespaces) <= {'app-dev','app-stage'}:
    raise SystemExit('Only DEV/STAGE namespaces are supported')
config=json.loads((Path.home()/'.docker/config.json').read_text())
auth=config.get('auths',{}).get('ghcr.io')
if not auth or not auth.get('auth'):
    raise SystemExit('No inline ghcr.io auth found; provision a package-reader credential securely')
encoded=base64.b64encode(json.dumps({'auths':{'ghcr.io':auth}}).encode()).decode()
for ns in namespaces:
    secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':'ghcr-pull-secret','namespace':ns},'type':'kubernetes.io/dockerconfigjson','data':{'.dockerconfigjson':encoded}}
    r=subprocess.run(['kubectl','--context','kind-fastapi-dev','apply','-f','-'],input=json.dumps(secret).encode(),capture_output=True)
    if r.returncode: raise SystemExit(f'Registry auth restore failed in {ns}')
    print(f'Restored {ns}/ghcr-pull-secret from existing host Docker auth')
