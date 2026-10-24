#!/usr/bin/env python3
"""Offline integrity checks for API collections, examples and genuine evidence."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def require(ok,message):
    if not ok:raise RuntimeError(message)


def main():
    files=[p for p in ROOT.rglob('*') if p.is_file()]
    for p in files:
        require(not p.is_symlink(),'Symlink rejected')
        if p.suffix=='.json':json.loads(p.read_text())
        elif p.suffix=='.py':ast.parse(p.read_text(),filename=p.name)
        elif p.suffix=='.cjs':subprocess.run(['node','--check',str(p)],check=True,capture_output=True)
        elif p.suffix=='.md':
            for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' not in url and not url.startswith('#'):
                    require((p.parent/unquote(url.split('#')[0])).exists(),'Broken link: '+url)
    readonly=json.loads((ROOT/'collections/liora-readonly.postman_collection.json').read_text())
    requests=readonly['item'][0]['item'];require(len(requests)==9,'Read-only coverage changed')
    require(all(r['request']['method']=='GET' for r in requests),'Live mutation request found')
    require(all(r['request']['auth']['type']=='noauth' for r in requests),'Unexpected live credential binding')
    require(all(len(r.get('response',[]))==1 for r in requests),'Captured examples missing')
    spec=json.loads((ROOT/'openapi.dev.json').read_text())
    operations={(m.upper(),p) for p,ops in spec['paths'].items() for m in ops if m in ['get','post','put','patch','delete']}
    examples=json.loads((ROOT/'collections/liora-backend-examples.postman_collection.json').read_text())
    names={(i['request']['method'],i['name'].split(' — ')[0].split(' ',1)[1]) for f in examples['item'] for i in f['item']}
    require(names==operations and len(names)==22,'Full examples differ from actual OpenAPI operations')
    variables={v['key']:v['value'] for v in examples['variable']}
    require(variables['example_base_url']=='https://example.invalid','Examples must not default to a live write target')
    require(not variables['access_token'] and not variables['reset_token'],'Secret token found')
    passed=failed=assertions=0
    for p in sorted((ROOT/'evidence/results').glob('*-private.json'))+sorted((ROOT/'evidence/results').glob('*-public.json')):
        data=json.loads(p.read_text());require(data['tls_verification'] is True,'TLS verification disabled')
        require(len(data['executions'])==9,'Execution count mismatch')
        for e in data['executions']:require(e['method']=='GET','Recorded mutation found')
        if data['failure_count']==0:
            passed+=1;assertions+=data['stats']['assertions']['total']
            require(all(all(a['passed'] for a in e['assertions']) for e in data['executions']),'False passing run')
            require(data['executions'][0]['http_status']==200 and data['executions'][0]['response_body']=='true','Health evidence mismatch')
            require(data['executions'][2]['http_status']==401,'Authentication evidence mismatch')
            require(data['executions'][7]['http_status']==403,'Invalid-token evidence mismatch')
            require(data['executions'][1]['openapi_response_sha256']==hashlib.sha256((ROOT/data['executions'][1]['openapi_capture_path']).read_bytes()).hexdigest(),'OpenAPI response differs from its captured contract')
        else:
            failed+=1;require(data['route']=='public' and data['environment'] in ['dev','stage'],'Unexpected failed route')
            require(all(not e['http_status'] and e['transport_error'] for e in data['executions']),'Expected TLS transport failure missing')
    require((passed,failed,assertions)==(4,2,108),'Aggregate counts mismatch')
    provenance=json.loads((ROOT/'evidence/provenance.json').read_text());images=list((ROOT/'evidence/screenshots').glob('*.jpg'))
    require(len(images)==8,'Screenshot count mismatch')
    hashes=set()
    for image in images:
        with Image.open(image) as im:require(im.format=='JPEG','Not a JPEG');im.verify()
        hashes.add(hashlib.sha256(image.read_bytes()).hexdigest())
    require(len(hashes)==8,'Duplicate screenshots')
    for shot in provenance['screenshots']:
        require(hashlib.sha256((ROOT/shot['path']).read_bytes()).hexdigest()==shot['sha256'],'Screenshot hash mismatch')
    patterns=[rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{40,}',rb'AKIA[0-9A-Z]{16}',rb'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}']
    for p in files:
        require(p.suffix not in ['.dump','.tfstate','.zip','.tar','.gz'] and p.name!='kubeconfig','Sensitive/unnecessary artifact')
        require(not any(re.search(pattern,p.read_bytes()) for pattern in patterns),'Credential pattern in '+p.name)
    return {'status':'PASS','files_checked':len(files),'example_operations':len(operations),'unique_genuine_screenshots':len(images),
            'passing_newman_runs':passed,'public_tls_failed_runs':failed,'passing_assertions':assertions,
            'syntax_links_provenance_and_credential_pattern_checks':'PASS','scope':'Offline evidence validation; no live API request'}


if __name__=='__main__':print(json.dumps(main(),indent=2))
