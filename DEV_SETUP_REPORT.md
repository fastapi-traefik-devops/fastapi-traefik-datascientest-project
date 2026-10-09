# DEV setup report

Inspection date: 2026-10-09 UTC. Target: `app-dev`, Argo Application `app-dev`.
Result: local DEV configuration validated; namespace created; live GitOps deployment blocked.
No commit, push, Jenkins build/promotion, image upload, stage deployment, or PROD creation was performed.

## A. What existed before

- Active Kubernetes context: `minikube`; one Ready node, Kubernetes v1.35.1.
- Repository started clean at local commit `11f0b3a`; remote main and Argo stage track `39d2623444c723949afcd3a9843aae835afc1dcd`.
- `deploy/base` and `deploy/overlays/{dev,stage,prod}` are the active Kustomize manifests. `k8s/` is legacy; Helm manages platform components, not this app's desired state.
- `app-stage` existed, Synced/Healthy, with ready backend, frontend, PostgreSQL and Adminer pods. Backend uses one worker and one replica.
- Legacy namespace `dev` existed with four ready application pods and a completed migration job. It uses old v0.1.0 image tags and is not an Argo Application.
- `app-dev` and `app-prod` did not exist. Only Application `app-stage` existed; no ApplicationSet was installed.
- AppProject `fastapi` already permits `app-dev`, `app-stage`, `app-prod`, this repository and the required workload kinds. It intentionally excludes Secrets and Namespaces.
- DEV and PROD overlays contained all-zero SHA image placeholders. DEV already requested one backend replica.
- Traefik uses IngressClass `traefik` and a ClusterIP service, ports 80/443; no external service address. Stage host is `stage.example.com`; legacy dev uses `api.example.com` and `dashboard.example.com`.
- Metrics server now exists and responds; it was already installed when this task began. This task did not install it.

## B. Jenkins CI flow

`Jenkinsfile` runs app-ci multibranch CI: backend lint/types/tests and migrations against disposable PostgreSQL, frontend build, Kustomize/schema validation and promotion tests, then BuildKit archives for backend/frontend.
Successful eligible main builds schedule `trusted/publish` asynchronously. PRs cannot publish; GitOps/docs-only commits validate without rebuilding images.
`Jenkinsfile.promote` loads trusted main, verifies the successful numbered CI build and artifact source SHA, copies archives, and runs `ci/publish.sh` under a global lock.
`ci/publish.sh` uses crane to push missing `sha-<full-SHA>` images to GHCR and preserves existing SHA tags. `ci/promote.py` writes authoritative digest pins plus `promotion.json` in Git.
Main publication automatically updates stage. DEV is a manually selected `MODE=dev` Jenkins run with explicit CI job/build and approval; the approved run automatically writes/pushes DEV Git changes. Production release creates a review branch instead of deploying directly.
No CI redesign, second CI mechanism, or Argo image build was introduced.

Image provenance verified live:
- `app-ci/main` build 5: SUCCESS; source SHA `3303e93b753e8282dc7b461c583fb8ace43574a1`; both image archives and source-sha.txt retained.
- `trusted/publish` build 6: SUCCESS; MODE=publish, CI_JOB=app-ci/main, CI_BUILD=5.
- Backend digest: `sha256:ea2d0aaf163f15f1bf749ee69822ebe33e619d2a00a5813d348732936b56f00b`.
- Frontend digest: `sha256:a8d07b6be8ae8c76cc8133c885ba8ec3c095ded005db251aaf6a190e88426f82`.
- These are the recorded images running in stage and now selected in local DEV configuration. Registry authentication/expiry was not independently tested with a new DEV pull.

## C. Argo CD deployment flow

Prepared `argocd/app-dev.yaml`: project fastapi, same repository as stage, targetRevision main, source path `deploy/overlays/dev`, destination namespace app-dev, same automated prune/selfHeal, retry and PruneLast policy as live stage.
Argo creates config/storage/database at wave -2, runs the migration Sync hook at wave 0, then rolls backend/frontend at wave 1.
Namespace creation is operator bootstrap from its repository manifest because the existing AppProject does not allow Namespace resources. Secrets remain externally provisioned.
Do not apply `argocd/applicationset.yaml` for this DEV-only task: it includes PROD and would also manage stage.
The DEV Application was server-dry-run validated but not created live: remote main still contains placeholder images and the old DEV configuration, and app-dev secrets are missing. Creating an auto-syncing application now would fail against that remote state. Applying local workload manifests directly would bypass the requested GitOps flow.

## D. What changed

- Created only live namespace app-dev from a new repository bootstrap manifest.
- Prepared a DEV-only Argo Application matching stage conventions.
- Pinned local DEV backend/frontend and migration image to the existing Jenkins-produced stage digests; added matching promotion record.
- Preserved one backend and one frontend replica; added explicit one-worker backend command in the DEV overlay.
- Changed DEV frontend/CORS origin to internal-test HTTP; removed DEV TLS dependency. No external Traefik service or public DNS was configured. The host remains the existing `dev.example.com` placeholder and can be selected using an HTTP Host header.
- Added DEV `/docs` ingress routing to backend; existing `/api` backend and `/` frontend routes remain.
- Preserved inherited secret references, PostgreSQL settings, probes, ClusterIP services and storage.
- Stage, PROD, shared base, Jenkins pipelines/scripts, Argo project and ApplicationSet files are unchanged. Legacy dev workloads/data were not adopted, patched or removed.

## E. Files changed

1. `deploy/overlays/dev/kustomization.yaml` (modified).
2. `deploy/overlays/dev/promotion.json` (new).
3. `argocd/bootstrap/dev-namespace.yaml` (new).
4. `argocd/app-dev.yaml` (new).
5. `DEV_SETUP_REPORT.md` (new).

## F. Important commands run

Shell commands were executed outside the sandbox because its startup previously failed with a bwrap operation-not-permitted error. Secret JSON/XML reads were captured and filtered in Python; no secret values were printed or written into this report.

Repository inspection:
```bash
pwd
git status --short
rg --files -g AGENTS.md -g '!node_modules' -g '!.git'
git log -4 --oneline
rg --files deploy argocd ci k8s/rbac
cat Jenkinsfile Jenkinsfile.promote ci/publish.sh ci/promote.py
cat argocd/project.yaml argocd/applicationset.yaml
cat deploy/overlays/dev/kustomization.yaml deploy/overlays/stage/kustomization.yaml deploy/overlays/stage/promotion.json
cat deploy/base/{deployment-backend.yaml,service-backend.yaml,deployment-db.yaml,service-db.yaml,configmap-db.yaml,configmap-backend.yaml,job-prestart.yaml,ingress-app.yaml,pvc-db.yaml,kustomization.yaml}
cat deployment.md backend/app/main.py backend/app/api/main.py
rg -n 'ENVIRONMENT|openapi|docs_url|SECRET_KEY' backend/app/core/config.py
git ls-remote origin HEAD refs/heads/main
```
Ancestor AGENTS.md paths were checked; no applicable instructions were found.
Jenkins metadata was captured through `kubectl exec -n jenkins jenkins-0 -c jenkins -- cat` for controller config, trusted publisher config, main build 5 build.xml, publisher build 6 build.xml. Python printed only cloud names/namespaces/restrictions, resource requests, script paths, credential IDs, build results, source SHA and non-secret promotion parameters. Retained archives were checked with `ls /var/jenkins_home/jobs/app-ci/branches/main/builds/5/archive` in that container.

Cluster inspection:
```bash
kubectl config current-context
kubectl get namespaces
kubectl get applications,applicationsets -n argocd
kubectl get pods -A -o wide
kubectl get services,ingresses -n traefik -o wide
kubectl get ingress -A -o wide
kubectl get appproject fastapi -n argocd -o yaml
kubectl get deployments,services,pvc -n dev -o wide
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp
kubectl get storageclass
kubectl get resourcequota,limitrange -n app-dev
kubectl get rolebindings -n app-dev
df -h /
free -h
```
Stage Application spec/sync/health were read using jsonpath. Secret names/types were listed using custom-columns. Secret JSON for dev/app-stage was parsed in memory to display names/types/key names only; values were never printed.

The only persisted cluster mutation:
```bash
kubectl apply --dry-run=server -f argocd/bootstrap/dev-namespace.yaml
kubectl apply -f argocd/bootstrap/dev-namespace.yaml
```

Validation and final checks:
```bash
kubectl apply --dry-run=server -f argocd/app-dev.yaml
/tmp/ci-bin/kustomize build deploy/overlays/dev
/tmp/ci-bin/kustomize build deploy/overlays/stage
/tmp/ci-bin/kustomize build deploy/overlays/prod
kubectl apply --dry-run=server -f /tmp/dev-setup-audit/dev-rendered.yaml
git diff --check
git diff --exit-code HEAD -- deploy/base deploy/overlays/stage deploy/overlays/prod Jenkinsfile Jenkinsfile.promote ci argocd/project.yaml argocd/applicationset.yaml
kubectl get ingress,endpointslices -n app-dev
kubectl get all -n app-dev
kubectl get application app-dev -n argocd
```
Rendered manifests were passed in memory to `/tmp/ci-bin/kubeconform -strict -summary -kubernetes-version 1.31.0`. All 13 resources/environment passed, 39 total; DEV also passed server admission dry-run against installed Kubernetes v1.35.1. The Argo Application and namespace passed server dry-run.
Python assertions verified DEV replica/worker settings, exact stage digests, migration image consistency, namespace isolation, absence of plaintext Secrets, `/docs` route, absent TLS requirement, ClusterIP-only services and matching promotion record.
Python read-only HTTP checks ran via `kubectl exec -n app-stage deployment/backend -- python -c ...` to legacy dev/stage backend services and Traefik with the appropriate Host header. Backend SQLAlchemy SELECT 1 checks ran via `kubectl exec -n dev deployment/backend -- python -c ...` and the equivalent app-stage command. Recent backend logs were captured with `kubectl logs -n <namespace> deployment/backend --tail=30`; only health/error counts were printed.

Capacity commands (all executed):
```bash
kubectl get nodes -o wide
kubectl top nodes
kubectl top pods -A
kubectl describe nodes
```
Python aggregated live pod resource requests/limits by namespace from captured `kubectl get pods -A -o json`.
Temporary validation/metrics/reference endpoint outputs are under `/tmp/dev-setup-audit`; no credentials are stored there.
Final display commands: `git diff`, `git status --short`, `kubectl get all -n dev`, `kubectl get all -n app-dev`, `kubectl get applications -n argocd`, and `cat DEV_SETUP_REPORT.md`. New manifest contents are shown separately because git diff omits untracked files.

## G. DEV namespace status

`app-dev`: created, Active, empty. No workloads, services, PVC, ingress, or secrets exist there yet.
Legacy `dev`: remains Active and unchanged, with existing data/workloads.
The name app-dev follows the existing GitOps overlay/AppProject convention. The requested `kubectl get all -n dev` output describes legacy dev, not the new GitOps target.

Required externally supplied secrets in app-dev:

| Name | Type / required keys |
| --- | --- |
| backend-secrets | Opaque: SECRET_KEY, FIRST_SUPERUSER_PASSWORD, POSTGRES_PASSWORD; optional SMTP_PASSWORD |
| db-secrets | Opaque: POSTGRES_PASSWORD, matching backend-secrets |
| ghcr-pull-secret | kubernetes.io/dockerconfigjson: .dockerconfigjson with GHCR read access |

All three are missing in app-dev. No secret values were generated, invented, copied across environments, or printed. An approved secret source/provisioning process was requested from the operator and not yet provided.
Stage has all three required names/keys. Legacy dev has backend/db secrets and `ghcr-creds`, but its pods reference missing `ghcr-pull-secret`, causing repeated pull-secret warnings. Its existing secrets were not reused automatically.
app-tls is not required for the prepared DEV HTTP setup. ENVIRONMENT remains staging because the app accepts only local/staging/production and staging preserves non-local secret validation.

## H. Argo CD status

- app-stage: Synced, Healthy; remote revision 39d2623444c723949afcd3a9843aae835afc1dcd.
- app-dev: manifest prepared and server validated; no live Application yet.
- DEV Synced/Healthy validation: BLOCKED by missing secrets and unpublished Git changes.
- No force sync, parameter override, direct workload apply or local-only image override was used.

## I. Kubernetes workload status

New app-dev: no pods/deployments/jobs; live rollout is not tested.
Planned: one backend worker/replica, one frontend, one PostgreSQL using Recreate and a 1Gi RWO default-class PVC, one internal Adminer, and migration Sync hook.
Reference stage and legacy dev each have four ready application pods. Stage backend has zero restarts; legacy backend has nine historical restarts and uses about 415Mi, compared with stage one-worker backend about 91Mi.
No new DEV pod logs or readiness results can exist until the Argo deployment occurs.

## J. Database connectivity result

New app-dev: NOT TESTED; no database/backend exists yet.
Reference stage and legacy dev: backend SQLAlchemy engine connects to its configured DB and executes SELECT 1 successfully, returning 1. This verifies backend-to-database connectivity without exposing credentials.
DEV configuration uses DB service `db:5432`, database app, user postgres. Secret passwords must match before the migration job can succeed.
Inherited backend HTTP health returns true without querying DB; a 200 there alone does not prove database connectivity. PostgreSQL uses pg_isready readiness. Stage recently reported occasional one-second readiness timeouts although it is currently ready.

## K. Traefik result

Prepared DEV ingress: class traefik, host dev.example.com, `/api` -> backend service port 80 -> container 8000, `/docs` -> same backend, `/` -> frontend port 80. Services are ClusterIP.
The route and service port mappings pass rendering/schema/admission checks. No DEV live ingress/endpoints exist yet; actual Traefik-to-DEV backend connectivity is NOT TESTED.
A request to Traefik with Host dev.example.com currently returns 404, as expected before deployment.
Stage Traefik routing for frontend/health/OpenAPI still works. Stage `/docs` through ingress returns 404, while its backend service `/docs` returns 200; the DEV-only docs route addresses this without modifying stage.
No public exposure/DNS/TLS was added. Internal testing can use Traefik's cluster service with Host header, or loopback-only port forwarding. The HTTP route is visible to clients that already have access to the existing Traefik endpoint; this does not add network isolation.

## L. Endpoint test results

| Endpoint / target | New app-dev | Legacy dev backend service | Stage backend service | Stage through Traefik |
| --- | --- | --- | --- | --- |
| / | NOT TESTED | 404 | 404 | 200 (frontend) |
| /api/v1/utils/health-check/ | NOT TESTED | 200 | 200 | 200 |
| /api/v1/openapi.json | NOT TESTED | 200 | 200 | 200 |
| /docs | NOT TESTED | 200 | 200 | 404 |

FastAPI defines no backend root route, so direct backend / returning 404 is expected. Use health/OpenAPI as API checks; the ingress root serves the frontend. No credentials were used for these endpoint tests.
Recent captured backend logs: 27 successful health-check lines in legacy dev, 26 in stage, zero ERROR lines in either 30-line sample. This is a limited sample, not a full historical log audit.

## M. Cluster capacity

Single Ready minikube node: 4 CPU, 8,131,772Ki memory = about 7.76GiB; 110 pod capacity. Allocatable equals reported capacity.
Measured idle-CI snapshot: 1,073m CPU (26%), 2,962Mi memory (37%). No active CI/publisher agents existed at measurement time.
MemoryPressure, DiskPressure and PIDPressure are False. Host filesystem: 61GiB total, 78% used, about 13GiB available. Metrics and pod usage fluctuate and do not describe build peaks.

| Existing namespace | CPU requests | Memory requests MiB | CPU limits | Memory limits MiB |
| --- | --- | --- | --- | --- |
| app-stage | 0.50 | 576 | 2.20 | 2176 |
| legacy dev | 0.50 | 576 | 2.20 | 2176 |
| Jenkins controller | 0.05 | 256 | 2.00 | 4096 |
| kube-system | 0.85 | 370 | 0 | 170 |
| Argo CD | 0 | 0 | 0 | 0 |
| Traefik | 0 | 0 | 0 | 0 |
| Total | 1.90 | 1778 | 6.40 | 8618 |

Argo/Traefik consume measured CPU/memory despite having no requests/limits. The control plane also has unbounded limits in several containers. Current limits already exceed capacity (160% CPU, 108% memory); limits are potential maxima, not actual simultaneous use.
New DEV steady-state requests add 0.50 CPU/576Mi, limits add 2.20 CPU/2176Mi; projected totals 2.40 CPU/2354Mi requests, 8.60 CPU/10794Mi limits. Migration adds temporary 0.10 CPU/128Mi requests, 0.50 CPU/512Mi limits. Rollouts may also briefly add surge pods.
DEV + stage idle operation appears feasible, but DEV + stage + CI on one node has narrow CPU scheduling headroom and unproven peak memory behavior. A controlled build/load observation is required before calling the combination safe. Legacy dev remains in these totals.
Adding PROD now is risky: its two backend/frontend replicas plus DB/Adminer add 0.70 CPU/832Mi requests before hooks/surge, leaving roughly 0.90 CPU for CI after DEV, less than CI's explicit 1 CPU request before the inbound agent. PROD was neither created nor changed.

## N. Jenkins resource impact

The four explicit CI containers together request 1 CPU/1280Mi and have limits of 5 CPU/5120Mi, plus the inbound agent. Cloud default templates specify an agent request of 512m CPU/512Mi; the actual generated agent Pod must be checked during a run to confirm inheritance.
If that agent request applies, DEV + current workloads + one CI agent projects 3.912 CPU/4146Mi requests, near the 4 CPU ceiling. Concurrent migration/rollout or publisher activity can exceed schedulable CPU.
The publisher requests 250m CPU/256Mi plus inbound agent, with publisher limit 1 CPU/1Gi. It can overlap other branch builds; per-job concurrency disabling does not serialize all branch jobs.
BuildKit is privileged, generates substantial image/archive/cache disk I/O, and shares this node with applications. No build was started because an approved DEV promotion writes Git, which is currently prohibited, and a new build would add avoidable pressure.
Measured controller memory was about 904Mi despite requesting only 256Mi. CI peak resource consumption is NOT measured in this task. Dedicated CI capacity/isolation should be addressed before PROD.

## O. Remaining blockers

1. Supply app-dev backend-secrets, db-secrets and ghcr-pull-secret through an approved source. The source is not known; values must remain private and DB passwords consistent.
2. Publish/merge the reviewed local DEV configuration to remote main. The explicit no-commit/no-push instruction prevents Argo from seeing it now. Do not enable the current remote placeholder configuration.
3. Apply the DEV-only Argo Application after those two prerequisites, then let Argo migrate and deploy.
4. Run real app-dev DB, Traefik, endpoint, digest, readiness and Synced/Healthy checks. Current reference passes do not certify new DEV.
5. Observe capacity during one controlled CI run plus DEV/stage load; monitor pending pods, OOM/restarts, DB probe timeouts and image/archive disk growth.

Existing issues outside this DEV-only change: legacy dev's missing pull-secret name; stage's missing TLS secret and placeholder DNS; Jenkins broad authenticated-user permissions/legacy deployment RBAC; privileged CI on the application node; previous dependency vulnerabilities; single-node hostPath DB durability. These were not modified or claimed resolved.

## P. Whether DEV is ready

NO: the new GitOps DEV environment is not deployed and cannot be reported Synced/Healthy.
YES: DEV namespace exists and the local configuration is ready for review, secret provisioning and publication. Schema, server dry-run, replica/worker/image/namespace/routing contract checks passed.
The inability to finish live validation comes from missing operator-supplied secrets and the explicit prohibition on committing/pushing, not from a build-system redesign requirement.

## Q. Exact next steps before PROD

First complete DEV (the following are future instructions, not actions already run):

1. Provision the three required app-dev secrets from the approved secret manager/process. Do not copy stage JWT/admin/database secrets by default.
2. Review the five changed files. After explicit commit/push authorization, publish them through the repository's normal reviewed main flow. Confirm remote DEV pins the tested digest pair and one worker/replica.
3. Bootstrap only DEV:
   `kubectl apply -f argocd/app-dev.yaml`
   Do not apply the existing all-environment ApplicationSet.
4. Confirm migration success and rollout with:
   `kubectl get pods,jobs,deployments,services,ingress,pvc -n app-dev`
   `kubectl logs -n app-dev deployment/backend --tail=50`
   `kubectl get application app-dev -n argocd`
   Compare deployed backend/frontend digests with DEV promotion.json.
5. From the DEV backend, use the existing SQLAlchemy engine for SELECT 1 without printing connection strings. Check pg_isready and the migration result.
6. For local-only ingress checks run:
   `kubectl port-forward --address=127.0.0.1 -n traefik service/traefik 18080:80`
   In another terminal, run `curl -i -H 'Host: dev.example.com' http://127.0.0.1:18080/api/v1/utils/health-check/`, then the equivalent /api/v1/openapi.json, /docs and / paths. Expected statuses: 200. Stop the forward after testing.
7. Require app-dev Synced/Healthy and ready pods, then repeat the four capacity commands during a controlled Jenkins build. Do not trigger trusted/publish MODE=dev until Git writes are explicitly authorized; normal future DEV promotions use app-ci/main build 5 or another successful approved branch build.

Before any separate PROD request: resolve CI capacity/isolation and Jenkins permissions; arrange durable storage and tested backups/restores; verify dependency/image vulnerabilities and GitHub branch/tag protections; configure actual PROD secrets/DNS/TLS; retain appropriate worker/resources; tag the tested application SHA with vX.Y.Z, use approved release mode and a reviewed production PR. Runtime release validation must refer to the actual digest pair tested in stage, not a later GitOps-only commit. No PROD actions are part of this task.
