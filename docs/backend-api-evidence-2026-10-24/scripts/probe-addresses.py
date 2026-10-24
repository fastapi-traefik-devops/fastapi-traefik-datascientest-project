#!/usr/bin/env python3
"""Read-only HTTPS/IP probes from the current PC. Keeps certificate checks enabled."""
import argparse
import concurrent.futures
import datetime
import json
from pathlib import Path
import socket
import subprocess

HOSTS = {'dev':'dev.liora.aprt.info','stage':'stage.liora.aprt.info','prod':'liora.aprt.info'}


def probe(case):
    environment, host, route, ip, family = case
    args=['curl','--silent','--show-error','--connect-timeout','5','--max-time','12']
    if family:args.append(f'-{family}')
    if ip:args.extend(['--resolve', f'{host}:443:{ip}'])
    args.extend(['--write-out','\n%{json}',f'https://{host}/api/v1/utils/health-check/'])
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(args,capture_output=True,text=True,timeout=15)
    body,_,metrics=p.stdout.rpartition('\n')
    try:data=json.loads(metrics)
    except ValueError:data={}
    return {'environment':environment,'hostname':host,'route':route,'requested_ip':ip,
            'family':family or 'auto','started_utc':start,'exit_code':p.returncode,
            'http_status':data.get('http_code'),'remote_ip':data.get('remote_ip'),
            'ssl_verify_result':data.get('ssl_verify_result'),'response_body':body,
            'error':p.stderr.strip(),'tls_verification_enabled':True}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise SystemExit('Refusing to overwrite prior evidence')
    cases=[];dns={}
    for env,host in HOSTS.items():
        dns[host]=sorted({r[4][0] for r in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)})
        cases.extend([(env,host,'public-dns',None,None),(env,host,'private-haproxy','192.168.77.240',None)])
        if env!='prod':cases.extend((env,host,'public-dns-'+label,None,family) for family,label in [('4','ipv4'),('6','ipv6')])
        cases.append((env,host,'direct-traefik-vip','192.168.77.17' if env=='prod' else '192.168.77.16',None))
    cases.append(('routing-negative','192.168.77.240','bare-ip-no-hostname',None,None))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(probe,cases))
    result={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'origin':'local PC',
            'dns':dns,'probes':results,'note':'No -k or TLS bypass. An IP alone does not provide the application Host/SNI name. Public failures describe this PC/path, not all Internet clients.'}
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps([{'environment':r['environment'],'route':r['route'],'exit':r['exit_code'],'http':r['http_status'],'ip':r['remote_ip']} for r in results],indent=2))


if __name__=='__main__':main()
