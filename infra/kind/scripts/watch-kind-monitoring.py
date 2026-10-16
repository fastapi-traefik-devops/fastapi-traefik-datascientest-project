#!/usr/bin/env python3
"""Watch monitoring startup and pause reconciliation on memory pressure; no deletions."""
import json,subprocess,time
CTX='kind-fastapi-dev'
def k(*args):
    return subprocess.check_output(['kubectl','--context',CTX,'--request-timeout=15s',*args],text=True)
def stop(reason):
    k('patch','application','monitoring','-n','argocd','--type=merge','-p','{"spec":{"syncPolicy":{"automated":{"enabled":false}}}}')
    k('annotate','application','monitoring','-n','argocd','argocd.argoproj.io/skip-reconcile=true','--overwrite')
    k('patch','application','monitoring','-n','argocd','--type=merge','-p','{"status":{"operationState":{"phase":"Terminating"}}}')
    raise SystemExit('Monitoring paused without deleting workloads/data: '+reason)
for _ in range(60):
    try:
        available=int(next(x.split()[1] for x in open('/proc/meminfo') if x.startswith('MemAvailable:')))/1024
        node=json.loads(k('get','nodes','-o','json'))['items'][0]
        pressure=[c['type'] for c in node['status']['conditions'] if c['type'] in ('MemoryPressure','DiskPressure','PIDPressure') and c['status']!='False']
        if available<1536 or pressure: stop(f'host available {available:.0f}Mi; node pressure {pressure}')
        app=json.loads(k('get','application','monitoring','-n','argocd','-o','json'))
        status=app.get('status',{})
        if status.get('sync',{}).get('status')=='Synced' and status.get('health',{}).get('status')=='Healthy':
            print('Monitoring startup Synced/Healthy; inspect targets/dashboards and continue pressure observation.')
            break
        if any(c['type'] in ('ComparisonError','InvalidSpecError') for c in status.get('conditions',[])):
            stop('Argo comparison/specification error')
    except subprocess.CalledProcessError:
        stop('Kubernetes API unavailable during startup')
    time.sleep(10)
else: stop('Startup did not become Synced/Healthy within ten minutes')
