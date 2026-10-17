#!/usr/bin/env python3
"""Validate local Prometheus/Grafana without public exposure; query dashboard expressions."""
import base64,json,math,subprocess,time,urllib.request,urllib.parse
from pathlib import Path
import yaml
ctx='kind-fastapi-dev';processes=[];grafana_auth=None
def request(base,path,body=None):
    headers={'Content-Type':'application/json'} if body else {}
    if base==globals().get('graf') and grafana_auth:
        headers['Authorization']=grafana_auth
    req=urllib.request.Request(base+path,data=json.dumps(body).encode() if body else None,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as r:return r.status,json.load(r)
def query(expr):
    status,obj=request(prom,'/api/v1/query?'+urllib.parse.urlencode({'query':expr}))
    assert status==200 and obj['status']=='success',(expr,obj)
    return obj['data']['result']
try:
    subprocess.run(['kubectl','--context',ctx,'wait','-n','monitoring','pod','--all','--for=condition=Ready','--timeout=180s'],check=True)
    for svc,port,target in [('monitoring-prometheus',19090,9090),('monitoring-grafana',13000,80),('monitoring-alertmanager',19093,9093)]:
        processes.append(subprocess.Popen(['kubectl','--context',ctx,'port-forward','--address=127.0.0.1','-n','monitoring','svc/'+svc,f'{port}:{target}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
    prom='http://127.0.0.1:19090';graf='http://127.0.0.1:13000';am='http://127.0.0.1:19093'
    for attempt in range(30):
        try:
            with urllib.request.urlopen(prom+'/-/ready',timeout=2) as r:assert r.status==200
            break
        except Exception:
            if attempt==29:raise
            time.sleep(1)
    print('Prometheus /-/ready: 200')
    expected=['node-exporter','kube-state-metrics','kubelet','argocd-metrics','argocd-server-metrics','argocd-repo-server','traefik']
    for attempt in range(24):
        _,obj=request(prom,'/api/v1/targets');targets=obj['data']['activeTargets']
        missing=[name for name in expected if not any(name in (t['scrapePool']+' '+json.dumps(t['labels'])) and t['health']=='up' for t in targets)]
        bad=[(t['labels'].get('job'),t['health'],t.get('lastError')) for t in targets if t['health']!='up']
        cpu=query('sum by(namespace,pod) (rate(container_cpu_usage_seconds_total{namespace=~"app-dev|app-stage",container!="",container!="POD"}[5m]))')
        if not missing and not bad and {x['metric'].get('namespace') for x in cpu}>={'app-dev','app-stage'}:break
        if attempt==23:raise AssertionError({'missing_targets':missing,'bad_targets':bad,'cpu_namespaces':list({x['metric'].get('namespace') for x in cpu})})
        time.sleep(10)
    print('Targets API: 200;',len(targets),'targets UP; required exporters and pod CPU samples present')
    for t in targets:print('target',t['scrapePool'],t['labels'].get('job'),t['health'])
    # Produce fresh benign traffic so latency/rate panels can be checked beyond idle NaN values.
    for host in ['dev.example.com','stage.example.com']:
        for _ in range(3):
            for path in ['/','/api/v1/utils/health-check/']:
                with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1'+path,headers={'Host':host}),timeout=10) as response:
                    assert response.status==200
    for attempt in range(12):
        latency=query('histogram_quantile(0.95,sum by(le,entrypoint) (rate(traefik_entrypoint_request_duration_seconds_bucket[5m])))')
        service_latency=query('histogram_quantile(0.95,sum by(le,service) (rate(traefik_service_request_duration_seconds_bucket{service=~"app-(dev|stage)-.*"}[5m])))')
        if any(math.isfinite(float(x['value'][1])) and float(x['value'][1])>0 for x in latency) and service_latency and all(math.isfinite(float(x['value'][1])) and float(x['value'][1])>0 for x in service_latency):break
        if attempt==11:raise AssertionError('No finite Traefik latency after fresh test traffic')
        time.sleep(10)
    print('Fresh DEV/STAGE traffic: 200; finite Traefik p95 latency observed')
    expressions={
      'pod CPU':'sum by(namespace,pod) (rate(container_cpu_usage_seconds_total{namespace=~"app-dev|app-stage",container!="",container!="POD"}[5m]))',
      'pod memory':'sum by(namespace,pod) (container_memory_working_set_bytes{namespace=~"app-dev|app-stage",container!="",container!="POD"})',
      'deployment replicas':'kube_deployment_status_replicas_available{namespace=~"app-dev|app-stage"}',
      'restart counters':'kube_pod_container_status_restarts_total{namespace=~"app-dev|app-stage"}',
    }
    for name,expr in expressions.items():
        result=query(expr);assert {r['metric'].get('namespace') for r in result}>={'app-dev','app-stage'},name
        print(name,len(result),'series; app-dev and app-stage separated')
    for name,expr in {'node memory':'node_memory_MemAvailable_bytes','Argo applications':'argocd_app_info{name=~"app-dev|app-stage"}','Traefik reload':'traefik_config_last_reload_success','Traefik response codes':'traefik_entrypoint_requests_total','Traefik latency':'traefik_entrypoint_request_duration_seconds_bucket','kubelet container data':'container_memory_working_set_bytes{namespace=~"app-dev|app-stage"}'}.items():
        result=query(expr);assert result,name;print(name,len(result),'series')
        if name=='Argo applications':assert {x['metric'].get('name') for x in result}>={'app-dev','app-stage'}
    _,rules=request(prom,'/api/v1/rules')
    wanted={'NodeMemoryPressure','NodeDiskPressure','NodeHighCPU','NodeHighMemory','ApplicationRestartSpike','ApplicationDeploymentUnavailable','ArgoApplicationUnhealthy','ArgoApplicationOutOfSync'}
    matched=[r for g in rules['data']['groups'] for r in g['rules'] if r.get('name') in wanted]
    assert {r['name'] for r in matched}==wanted
    assert all(r['health']=='ok' and not r.get('lastError') for r in matched)
    print('Rules API: 200; eight expected alert rules loaded and evaluating successfully')
    _,status=request(am,'/api/v2/status');config=yaml.safe_load(status['config']['original'])
    assert config['route']['receiver']=='slack'
    receiver=next(r for r in config['receivers'] if r['name']=='slack')
    assert receiver['slack_configs'][0]['send_resolved'] is True
    assert receiver['slack_configs'][0]['api_url_file']=='/etc/alertmanager/secrets/monitoring-slack-webhook/slack-webhook'
    _,alerts=request(am,'/api/v2/alerts')
    _,discovery=request(prom,'/api/v1/alertmanagers')
    assert len(discovery['data']['activeAlertmanagers'])==1
    assert all(float(x['value'][1])==0 for x in query('prometheus_notifications_errors_total'))
    print('Alertmanager API: 200;',len(alerts),'active alerts; one discovered endpoint; zero notification errors; Slack receiver with resolved notifications enabled')
    secret=json.loads(subprocess.check_output(['kubectl','--context',ctx,'get','secret','monitoring-grafana-admin','-n','monitoring','-o','json']))['data']
    user=base64.b64decode(secret['admin-user']).decode()
    password=base64.b64decode(secret['admin-password']).decode()
    grafana_auth='Basic '+base64.b64encode((user+':'+password).encode()).decode()
    del secret,user,password
    assert request(graf,'/api/health')[0]==200
    _,ds=request(graf,'/api/datasources/uid/prometheus');assert ds['uid']=='prometheus'
    _,search=request(graf,'/api/search?type=dash-db')
    docs=yaml.safe_load((Path(__file__).resolve().parent.parent/'monitoring/dashboards/platform.yaml').read_text())['data']
    expected_dashboards=[json.loads(d) for d in docs.values()]
    assert {x['uid'] for x in search}>={d['uid'] for d in expected_dashboards}
    print('Grafana health/datasource/search: 200; four expected dashboard UIDs present')
    for desired in expected_dashboards:
        _,live=request(graf,'/api/dashboards/uid/'+desired['uid']);assert live['meta'].get('provisioned') is True
        panels=live['dashboard']['panels'];checks=0
        assert live['dashboard']['title']==desired['title']
        assert panels==desired['panels'],desired['uid']
        for panel in panels:
            for target in panel.get('targets',[]):
                expr=target.get('expr')
                if not expr:continue
                selections=['app-dev','app-stage'] if '$namespace' in expr else ['']
                for ns in selections:
                    resolved=expr.replace('$namespace',ns)
                    samples=query(resolved)
                    assert samples and any(math.isfinite(float(x['value'][1])) for x in samples),(desired['uid'],panel['title'],ns,'missing/nonfinite data')
                    body={'queries':[{'refId':'A','expr':resolved,'instant':True,'range':False,'datasource':{'uid':'prometheus','type':'prometheus'},'format':'time_series','intervalMs':60000,'maxDataPoints':100}],'from':'now-5m','to':'now'}
                    _,answer=request(graf,'/api/ds/query',body)
                    result=answer['results']['A'];assert not result.get('error'),result
                    assert any(any(values for values in frame.get('data',{}).get('values',[])) for frame in result.get('frames',[])),(desired['uid'],panel['title'])
                    checks+=1
        print('dashboard',desired['uid'],checks,'panel/namespace queries returned real data through Grafana')
    print('Prometheus/Grafana validation PASS')
finally:
    for p in processes:p.terminate()
    for p in processes:
        try:p.wait(timeout=5)
        except subprocess.TimeoutExpired:p.kill();p.wait()
