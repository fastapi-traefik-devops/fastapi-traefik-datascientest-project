#!/usr/bin/env bash
# Operator bootstrap only. Never invoked by Jenkins. No Minikube/PROD operations.
set -euo pipefail
set +x
umask 077
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export PATH="$ROOT/.tools:$PATH"
NAME=fastapi-dev
CONTEXT=kind-fastapi-dev
PHASE=${1:-base}
KEY_BACKUP=${SEALED_SECRETS_KEY_BACKUP:-$ROOT/sealed-secrets-key-backup.yaml}
KIND_VERSION=v0.33.0
SEALED_VERSION=v0.39.1
TRAEFIK_CHART=39.0.0
ARGO_VERSION=v3.5.4
METRICS_VERSION=v0.9.0
for tool in kind kubectl helm python3 curl docker; do command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }; done
python3 -c 'import yaml'
k() { kubectl --context "$CONTEXT" --request-timeout=60s "$@"; }
ns() { k create namespace "$1" --dry-run=client -o yaml | k apply -f -; }
wait_app() {
  k wait -n argocd "application/$1" --for=jsonpath='{.status.sync.status}'=Synced --timeout=600s
  k wait -n argocd "application/$1" --for=jsonpath='{.status.health.status}'=Healthy --timeout=600s
}
case "$PHASE" in
base)
  [[ "$(kind version)" == *"$KIND_VERSION"* ]] || { echo "Use kind $KIND_VERSION" >&2; exit 1; }
  [[ -s "$KEY_BACKUP" ]] || { echo 'Provide SEALED_SECRETS_KEY_BACKUP before bootstrap.' >&2; exit 1; }
  if ! kind get clusters | grep -qx "$NAME"; then
    kind create cluster --name "$NAME" --config "$ROOT/infra/kind/kind-config.yaml" --wait 180s
  fi
  k wait node --all --for=condition=Ready --timeout=180s
  k rollout status -n kube-system deployment/coredns --timeout=180s
  # Restore only key Secrets, stripping live metadata; private bytes stay in memory/stdin.
  python3 - "$KEY_BACKUP" "$CONTEXT" <<'PY'
import sys,yaml,subprocess,os
p,ctx=sys.argv[1:]; os.chmod(p,0o600)
d=yaml.safe_load(open(p)); items=d.get('items',[d]); keys=[]
for i in items:
    if i.get('kind')!='Secret' or not {'tls.key','tls.crt'} <= i.get('data',{}).keys():
        raise SystemExit('Backup contains an invalid key object')
    keys.append({'apiVersion':'v1','kind':'Secret','metadata':{'name':i['metadata']['name'],'namespace':'kube-system','labels':{'sealedsecrets.bitnami.com/sealed-secrets-key':'active'}},'type':'kubernetes.io/tls','data':i['data']})
if not keys: raise SystemExit('Empty key backup')
subprocess.run(['kubectl','--context',ctx,'apply','-f','-'],input=yaml.safe_dump({'apiVersion':'v1','kind':'List','items':keys}).encode(),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('Sealed Secrets key restored without printing private material')
PY
  curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://github.com/bitnami/sealed-secrets/releases/download/$SEALED_VERSION/controller.yaml" -o "$ROOT/.tools/sealed-controller.yaml"
  k apply -f "$ROOT/.tools/sealed-controller.yaml"
  k rollout restart -n kube-system deployment/sealed-secrets-controller
  k rollout status -n kube-system deployment/sealed-secrets-controller --timeout=180s
  helm upgrade --install traefik traefik --repo https://traefik.github.io/charts --version "$TRAEFIK_CHART" --namespace traefik --create-namespace --kube-context "$CONTEXT" --values "$ROOT/infra/kind/traefik-values.yaml" --wait --timeout 5m
  ns argocd
  curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://raw.githubusercontent.com/argoproj/argo-cd/$ARGO_VERSION/manifests/install.yaml" -o "$ROOT/.tools/argocd-install.yaml"
  k apply --server-side -n argocd -f "$ROOT/.tools/argocd-install.yaml"
  k wait -n argocd pod --all --for=condition=Ready --timeout=600s
  curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://github.com/kubernetes-sigs/metrics-server/releases/download/$METRICS_VERSION/components.yaml" -o "$ROOT/.tools/metrics-server.yaml"
  # Local kind kubelet certificates are not signed by the metrics-server trust root.
  # Keep this declarative so reruns do not append duplicate arguments.
  python3 - "$ROOT/.tools/metrics-server.yaml" <<'PYMETRICS'
import sys,yaml
p=sys.argv[1]; docs=list(yaml.safe_load_all(open(p)))
for doc in docs:
    if doc.get('kind')=='Deployment' and doc['metadata']['name']=='metrics-server':
        args=doc['spec']['template']['spec']['containers'][0]['args']
        if '--kubelet-insecure-tls' not in args: args.append('--kubelet-insecure-tls')
with open(p,'w') as f: yaml.safe_dump_all(docs,f,sort_keys=False)
PYMETRICS
  k apply -f "$ROOT/.tools/metrics-server.yaml"
  k rollout status deployment/metrics-server -n kube-system --timeout=180s
  k apply -f "$ROOT/infra/kind/project-fastapi.yaml"
  ns app-dev; ns app-stage
  for env in dev stage; do
    if k get -n argocd "application/app-$env" >/dev/null 2>&1; then continue; fi
    # Register desired Git source, but do not reconcile before credentials are provisioned.
    python3 - "$ROOT/argocd/app-$env.yaml" <<'PY' | k apply -f -
import sys,yaml
x=yaml.safe_load(open(sys.argv[1])); x['metadata'].setdefault('annotations',{})['argocd.argoproj.io/skip-reconcile']='true'; x['spec']['syncPolicy']['automated']['enabled']=False
print(yaml.safe_dump(x))
PY
  done
  ns monitoring
  k apply -f "$ROOT/argocd/project-monitoring.yaml"
  # Inline local values preserve unpublished monitoring configuration; Argo owns workloads.
  if ! k get -n argocd application/monitoring >/dev/null 2>&1; then
    python3 "$ROOT/monitoring/bootstrap.py" | k apply -f -
  fi
  k cluster-info; k get nodes -o wide
  echo 'Base installed. Provision namespace-specific credentials before dev/stage phases.'
  ;;
dev|stage)
  ENVIRONMENT_NS="app-$PHASE"
  if [[ -d "$ROOT/infra/kind/secrets/$ENVIRONMENT_NS" ]]; then
    k apply -f "$ROOT/infra/kind/secrets/$ENVIRONMENT_NS"
    for secret in backend-secrets db-secrets; do
      k wait -n "$ENVIRONMENT_NS" "sealedsecret/$secret" --for=condition=Synced --timeout=120s
    done
  fi
  for secret in backend-secrets db-secrets ghcr-pull-secret; do
    k get secret -n "$ENVIRONMENT_NS" "$secret" >/dev/null || { echo "Missing $ENVIRONMENT_NS/$secret; supply or recover it securely." >&2; exit 1; }
  done
  # Ensure only this environment is enabled. Existing ApplicationSet is never applied.
  APP_MANIFEST="$ROOT/argocd/app-$PHASE.yaml"
  if [[ "$PHASE" == stage ]]; then APP_MANIFEST="$ROOT/infra/kind/app-stage-local.yaml"; fi
  k apply -f "$APP_MANIFEST"
  k annotate -n argocd "application/app-$PHASE" argocd.argoproj.io/skip-reconcile-
  k patch -n argocd "application/app-$PHASE" --type=merge -p '{"spec":{"syncPolicy":{"automated":{"enabled":true}}}}'
  wait_app "app-$PHASE"
  for deployment in postgres-deployment backend frontend adminer; do k rollout status -n "$ENVIRONMENT_NS" "deployment/$deployment" --timeout=180s; done
  ;;
monitoring)
  for app in app-dev app-stage; do wait_app "$app"; done
  # Monitoring may run while Jenkins is explicitly kept offline. This does not prove CI peak safety.
  if [[ "${CI_CAPACITY_VERIFIED:-}" != yes ]]; then
    [[ "${CI_DISABLED:-}" == yes ]] || { echo 'Keep CI offline with CI_DISABLED=yes, or verify CI peak capacity with CI_CAPACITY_VERIFIED=yes.' >&2; exit 1; }
    python3 - <<'PYCI'
import json,subprocess
status=subprocess.run(['systemctl','is-active','jenkins'],capture_output=True,text=True)
if status.stdout.strip() in ('active','activating'): raise SystemExit('Jenkins is active; CI peak must be measured')
pods=json.loads(subprocess.check_output(['kubectl','--context','kind-fastapi-dev','get','pods','-A','-o','json']))['items']
for p in pods:
    if p['status'].get('phase') not in ('Succeeded','Failed') and (p['metadata']['namespace'].startswith('jenkins') or any(c['name']=='jnlp' for c in p['spec']['containers'])):
        raise SystemExit('Jenkins workload/agent is active; keep monitoring paused until CI peak is reviewed')
containers=subprocess.check_output(['docker','ps','--format','{{.Image}} {{.Names}}'],text=True)
if 'jenkins' in containers.lower(): raise SystemExit('Docker Jenkins controller is active; measure CI peak first')
print('Local Jenkins controller/agents absent; monitoring budget excludes CI. Keep Jenkins/builds offline.')
PYCI
  fi
  python3 "$ROOT/scripts/check-kind-capacity.py"
  k annotate -n argocd application/monitoring argocd.argoproj.io/skip-reconcile-
  k patch -n argocd application/monitoring --type=merge -p '{"spec":{"syncPolicy":{"automated":{"enabled":true}}}}'
  python3 "$ROOT/scripts/watch-kind-monitoring.py"
  k get pods,pvc -n monitoring
  ;;
*) echo 'Usage: bootstrap-kind.sh {base|dev|stage|monitoring}' >&2; exit 2 ;;
esac
