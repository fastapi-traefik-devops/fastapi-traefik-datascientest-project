#!/usr/bin/env python3
"""Explicit operator action: create fresh STAGE credentials and save only ciphertext.

Existing encrypted files are reused; existing live credentials are never overwritten.
Secrets are distinct from DEV, and backend/database passwords match.
"""
import base64,json,os,secrets,subprocess,tempfile
from pathlib import Path
import yaml
root=Path(__file__).resolve().parent.parent
out=root/'infra/kind/secrets/app-stage'
files=[out/f'{name}-secrets.yaml' for name in ('backend','db')]
if all(p.exists() for p in files):
    print('Existing encrypted STAGE credentials retained; no rotation performed')
    raise SystemExit(0)
if any(p.exists() for p in files): raise SystemExit('Partial encrypted STAGE backup: resolve before creating credentials')
ctx='kind-fastapi-dev'
live=json.loads(subprocess.check_output(['kubectl','--context',ctx,'get','secrets','-n','app-stage','-o','json']))
if any(s['metadata']['name'] in ('backend-secrets','db-secrets') for s in live['items']):
    raise SystemExit('Existing live STAGE credentials found; recover/seal them rather than replace')
backup=Path(os.environ.get('SEALED_SECRETS_KEY_BACKUP',root/'sealed-secrets-key-backup.yaml'))
b=yaml.safe_load(backup.read_text()); key=b.get('items',[b])[0]
password=secrets.token_urlsafe(36)
values={'backend':{'SECRET_KEY':secrets.token_urlsafe(48),'FIRST_SUPERUSER_PASSWORD':secrets.token_urlsafe(24),'POSTGRES_PASSWORD':password},'db':{'POSTGRES_PASSWORD':password}}
sealed={}
with tempfile.TemporaryDirectory(prefix='stage-seal-') as tmp:
    cert=Path(tmp)/'cert.pem'; cert.write_bytes(base64.b64decode(key['data']['tls.crt']));cert.chmod(0o600)
    for name,data in values.items():
        secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':f'{name}-secrets','namespace':'app-stage'},'type':'Opaque','stringData':data}
        result=subprocess.run(['kubeseal','--cert',str(cert),'--format','yaml'],input=json.dumps(secret).encode(),capture_output=True)
        if result.returncode: raise SystemExit(f'Sealing failed for {name}; no credentials printed')
        sealed[name]=result.stdout
out.mkdir(parents=True,exist_ok=True)
for name,data in sealed.items():
    (out/f'{name}-secrets.yaml').write_bytes(data)
    print(f'Created encrypted app-stage/{name}-secrets; plaintext stayed in memory')
