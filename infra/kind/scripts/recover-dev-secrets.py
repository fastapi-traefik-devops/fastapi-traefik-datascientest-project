#!/usr/bin/env python3
"""Reseal recoverable DEV credentials; never creates the legacy dev namespace.

Run after base bootstrap. Plaintext remains in memory; key/cert temp files are 0600.
STAGE, registry credentials and TLS require their own backups/manual provisioning.
"""
import base64, json, os, subprocess, tempfile
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[3]
backup = Path(os.environ.get('SEALED_SECRETS_KEY_BACKUP', root / 'sealed-secrets-key-backup.yaml'))
doc = yaml.safe_load(backup.read_text())
keys = doc.get('items', [doc])
out = root / 'infra/kind/secrets/app-dev'
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='sealed-recovery-') as tmp:
    private = []
    for i, item in enumerate(keys):
        p = Path(tmp) / f'key-{i}.pem'
        p.write_bytes(base64.b64decode(item['data']['tls.key']))
        p.chmod(0o600)
        private.append(str(p))
    cert = Path(tmp) / 'cert.pem'
    cert.write_bytes(base64.b64decode(keys[0]['data']['tls.crt']))
    cert.chmod(0o600)
    recovered = {}
    for name in ('backend', 'db'):
        source = root / f'k8s/overlays/dev/sealed-secret-{name}.yaml'
        r = subprocess.run(['kubeseal', '--recovery-unseal', '--recovery-private-key', ','.join(private)], input=source.read_bytes(), capture_output=True)
        if r.returncode:
            raise SystemExit(f'Offline decryption failed: {name}')
        secret = yaml.safe_load(r.stdout)
        secret['metadata'] = {'name': f'{name}-secrets', 'namespace': 'app-dev'}
        recovered[name] = secret
    if recovered['backend']['data']['POSTGRES_PASSWORD'] != recovered['db']['data']['POSTGRES_PASSWORD']:
        raise SystemExit('Recovered database passwords differ')
    for name, secret in recovered.items():
        r = subprocess.run(['kubeseal', '--cert', str(cert), '--format', 'yaml'], input=json.dumps(secret).encode(), capture_output=True)
        if r.returncode:
            raise SystemExit(f'Resealing failed: {name}')
        (out / f'{name}-secrets.yaml').write_bytes(r.stdout)
        print(f'Resealed app-dev/{name}-secrets; no plaintext emitted')
