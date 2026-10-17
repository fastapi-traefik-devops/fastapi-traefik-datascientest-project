#!/usr/bin/env python3
"""Capture namespace and host/container memory observations, without credential data."""
import datetime,json,subprocess,sys
from pathlib import Path
ctx='kind-fastapi-dev'
def k(path):return json.loads(subprocess.check_output(['kubectl','--context',ctx,'--request-timeout=15s','get','--raw='+path]))
def cpu(v):
 if v.endswith('n'):return float(v[:-1])/1e6
 if v.endswith('u'):return float(v[:-1])/1000
 if v.endswith('m'):return float(v[:-1])
 return float(v)*1000
def mem(v):
 for suffix,scale in [('Ki',1/1024),('Mi',1),('Gi',1024)]:
  if v.endswith(suffix):return float(v[:-len(suffix)])*scale
 return float(v)/1024**2
pods=k('/apis/metrics.k8s.io/v1beta1/pods')['items'];nodes=k('/apis/metrics.k8s.io/v1beta1/nodes')['items']
groups={}
for p in pods:
 group=groups.setdefault(p['metadata']['namespace'],{'cpu_m':0,'memory_mi':0})
 for c in p['containers']:
  group['cpu_m']+=cpu(c['usage']['cpu']);group['memory_mi']+=mem(c['usage']['memory'])
host={line.split(':')[0]:int(line.split()[1])/1024 for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemTotal:','MemAvailable:'))}
current=int(subprocess.check_output(['docker','exec','fastapi-dev-control-plane','cat','/sys/fs/cgroup/memory.current']))/1024**2
docker=json.loads(subprocess.check_output(['docker','stats','--no-stream','--format','{{json .}}','fastapi-dev-control-plane']))
record={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host_mi':host,'node':{'cpu_m':cpu(nodes[0]['usage']['cpu']),'memory_mi':mem(nodes[0]['usage']['memory'])},'namespaces':{ns:{k:round(v,2) for k,v in g.items()} for ns,g in groups.items()},'docker':docker,'cgroup_memory_current_mi':round(current,2)}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
