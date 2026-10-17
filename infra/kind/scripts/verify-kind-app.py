#!/usr/bin/env python3
"""Read-only DEV/STAGE database, DNS and HTTP checks; no secret values emitted."""
import subprocess,sys
phase=sys.argv[1] if len(sys.argv)>1 else 'dev'
if phase not in ('dev','stage'): raise SystemExit('Use dev or stage')
code='''
import socket,urllib.request,urllib.error
from sqlalchemy import text
from app.core.db import engine
with engine.connect() as connection:
    assert connection.execute(text('SELECT 1')).scalar()==1
print('Database SELECT 1: PASS')
print('CoreDNS service discovery:', bool(socket.getaddrinfo('db',5432)))
def check(url,expected,host=None):
    req=urllib.request.Request(url,headers={'Host':host} if host else {})
    try:
        with urllib.request.urlopen(req,timeout=15) as response: status=response.status
    except urllib.error.HTTPError as error: status=error.code
    print(url,'Host='+host if host else '',status)
    assert status==expected,(url,status,expected)
for path,status in [('/',404),('/api/v1/utils/health-check/',200),('/api/v1/openapi.json',200),('/docs',200),('/metrics',404)]:
    check('http://backend'+path,status)
check('http://frontend/',200)
check('http://adminer/',200)
for path in ['/', '/api/v1/utils/health-check/', '/api/v1/openapi.json']:
    check('http://traefik.traefik.svc.cluster.local'+path,200,HOST)
if HOST.startswith('dev.'):
    check('http://traefik.traefik.svc.cluster.local/docs',200,HOST)
'''.replace('HOST',repr(phase+'.example.com'))
subprocess.run(['kubectl','--context','kind-fastapi-dev','exec','-i','-n','app-'+phase,'deployment/backend','--','python','-'],input=code.encode(),check=True)
