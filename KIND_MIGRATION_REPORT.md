# kind migration / clean rebuild report

2026-10-09 UTC. Context `kind-fastapi-dev`. **DEV, STAGE and monitoring are Synced/Healthy and validated. Jenkins remains offline/not restored. This local platform is ready for DEV/STAGE work with CI kept offline until its peak budget is validated.** No commit/push, PROD resource, legacy dev namespace or Minikube recreation occurred.

## A. Previous Minikube architecture

Historical reports describe one Docker-driver Minikube node, Kubernetes v1.35.1, Traefik ClusterIP ingress, Argo CD, app-dev/app-stage, and a separate legacy dev namespace. Jenkins ran as `jenkins-0`, a two-container StatefulSet with local PVC. Its exact installer/chart version and controller settings were not preserved in Git. PostgreSQL also used local PVCs. No PROD Application was installed.

## B. Why Minikube was replaced

The host has about 7.8GiB RAM, but the old Minikube Docker/cgroup limit was only 3GiB. Kubernetes advertised host-like memory, obscuring that limit. Monitoring rollout produced capacity/readiness problems and was paused. The operator manually deleted Minikube before this rebuild; the old live state is gone.

## C. Why kind was chosen

A reproducible Docker-based local cluster matches this development workflow. One node avoids extra kubelet/container/control-plane overhead and leaves more RAM for workloads and CI. kind itself does not create RAM or guarantee CI peak safety; the corrected memory accounting and omitted legacy workloads matter too.

## D. New kind architecture

Ubuntu host -> one Docker container `fastapi-dev-control-plane` -> Kubernetes v1.35.8, kind networking/CoreDNS/local-path storage, Sealed Secrets, Traefik, Argo CD, metrics-server, and app-dev. app-stage and monitoring are deployed and validated, alongside the unchanged app-dev. Jenkins controller is intended to run outside kind, with current pipelines still using Kubernetes agents. PROD remains on a future separate cluster.

## E. Kind cluster configuration

`infra/kind/kind-config.yaml`: kind v0.33.0, one control-plane node, Kubernetes 1.35.8 pinned to digest `07b2536e30b803ed61d1677a79df6115f798ce64c80f9e22f6ed45afd09323c0`. Same Kubernetes minor as the old cluster, with a newer patch. Node label ingress-ready=true. Host 127.0.0.1:80 -> node:80 and 127.0.0.1:443 -> node:443; Traefik hostPorts map to its web/websecure entrypoints. No worker nodes or public exposure configured.

The node is Ready; kindnet and both CoreDNS pods are Ready. Database DNS resolved from the backend pod. API listens on localhost with a dynamically chosen port recorded in kubeconfig. StorageClass standard is now kind local-path, not Minikube's hostPath provisioner. Docker HostConfig.Memory=0 and cgroup memory.max=max: no 3GiB cap; the host remains the shared physical limit. Current system kubectl is v1.37.0; prefer a 1.35.x client for the usual supported minor skew.

Sources: [kind v0.33.0 image digests](https://github.com/kubernetes-sigs/kind/releases/tag/v0.33.0), [kind port mappings](https://kind.sigs.k8s.io/docs/user/configuration/#extra-port-mappings).

## F. Files added / modified

- `.gitignore`: private backups/local tools excluded. Existing DEV_SETUP_REPORT.md changes were present before this rebuild and preserved.
- `infra/kind/kind-config.yaml`, `traefik-values.yaml`, `project-fastapi.yaml`: local cluster/platform configuration; project allows only DEV/STAGE destinations.
- `infra/kind/secrets/app-dev/{backend,db}-secrets.yaml`: encrypted namespace-correct recovery; no plaintext credentials.
- `argocd/app-stage.yaml`: standard stage-only Application. `infra/kind/app-stage-local.yaml`: kind-only HTTP patches; no TLS credential dependency.
- `scripts/bootstrap-kind.sh`: phased idempotent operator bootstrap.
- `scripts/recover-dev-secrets.py`, `restore-kind-registry-auth.py`, `verify-kind-app.py`: recovery and read-only validation helpers.
- `scripts/check-kind-capacity.py`, `watch-kind-monitoring.py`: capacity/startup checks. `capture-kind-capacity.py` records before/after resource observations.
- `scripts/create-stage-secrets.py`: explicit fresh-credential generation, saving ciphertext only. `verify-kind-monitoring.py`: target/query/rule and provisioned dashboard validation.
- `MIGRATION_BACKUP_CHECKLIST.md`, this report, updated `MONITORING_SETUP_REPORT.md`.

Prepared monitoring/ and monitoring Argo files were already untracked at task start and reused. DEV/STAGE overlays, image digest pins, application code, Jenkins pipelines, CI scripts and PROD files were not changed. Existing `argocd/applicationset.yaml` includes PROD and is deliberately never applied by this bootstrap. Existing global project permits PROD; kind uses its own scoped copy instead.

## G. Sealed Secrets recovery

Found `sealed-secrets-key-backup.yaml` with one private key. Restricted permissions to 0600 and excluded it from Git. Offline backend/database decryption passed. The frontend sealed file is empty, so an earlier zero exit on that file did not prove decryption. Active frontend has no frontend-secret dependency.

Bootstrap normalizes the key Secret metadata and restores only keys to kube-system through memory/stdin before installing controller v0.39.1, then restarts/waits for the controller. Original ciphertext is strict to legacy dev; it cannot simply be renamed. Recovery helper decrypts in memory and reseals specifically for app-dev. Both app-dev SealedSecrets report Synced=True and produced Secrets with matching database passwords. Legacy dev is never created.

Existing host Docker GHCR auth was recovered into ghcr-pull-secret for DEV/STAGE using memory/stdin. Only ghcr.io auth was copied, not unrelated registries. Its original permission scope is not established; replace with a package-reader credential for continued use. Anonymous GHCR access returned 401. Private material never entered scripts/reports/Git; no key/secret values printed. See the backup checklist for future key/Jenkins backup procedures.

## H. DEV restore

Argo app-dev tracks Git main revision `cb1bb5617741cd5b68d36b9d419b6014226b6751`, path deploy/overlays/dev. Synced/Healthy; last operation Succeeded. PostgreSQL/adminer/backend/frontend are 1/1 Ready, zero restarts in validation. Migration Sync hook succeeded and was deleted by HookSucceeded policy. New postgres-vol PVC: Bound, 1Gi, RWO, standard.

Backend remains one replica with `fastapi run --workers 1 app/main.py`. Existing backend/frontend digest pins remain unchanged. SQLAlchemy SELECT 1 passed; service DNS resolved. Backend health/OpenAPI/docs returned 200; backend `/` returned expected 404 because there is no backend root route. Frontend and Adminer internal roots returned 200. Traefik DEV host root, health, OpenAPI and docs returned 200; localhost HTTP root/health/docs also returned 200 with Host dev.example.com. `/metrics` returned 404.

## I. STAGE restore

User explicitly authorized new STAGE credentials. Created independent cryptographically random SECRET_KEY, FIRST_SUPERUSER_PASSWORD and POSTGRES_PASSWORD; the database/backend password matches and all differ from DEV. Generated values stayed in memory; only strict namespace-correct SealedSecrets were saved to infra/kind/secrets/app-stage and applied. Existing registry pull credential was retained. SMTP_PASSWORD is optional/unconfigured and was not fabricated.

The first generated admin password was 48 characters, exceeding UserCreate's 40-character maximum. Schema migration/database connectivity succeeded but initial user creation failed. Corrected only that new admin password to 32 random characters, resealed it, and Argo retried successfully; the database password/PVC/data stayed unchanged. Generation helper now respects the schema bound and reuses existing encrypted files instead of rotating on reruns.

STAGE backend/database SealedSecrets are Synced=True, both Secrets exist and passwords match. Argo app-stage: Synced/Healthy; last operation Succeeded; remote main revision cb1bb5617741cd5b68d36b9d419b6014226b6751. PostgreSQL/backend/frontend/Adminer are 1/1 Ready, zero restarts. New 1Gi postgres-vol PVC is Bound. Backend remains one replica with `fastapi run --workers 1 app/main.py` and original image digests.

`infra/kind/app-stage-local.yaml` uses Argo source Kustomize patches against the standard deploy/overlays/stage Git path. It removes spec.tls and changes FRONTEND_HOST/BACKEND_CORS_ORIGINS to http://stage.example.com. Standard STAGE overlay/HTTPS design, hostname, existing routing paths and image pins remain unchanged. No fake production certificates or public DNS/TLS were created. STAGE ingress retains /api to backend and / to frontend; /docs is checked directly at the backend, not added to the ingress.

SQLAlchemy SELECT 1 and service DNS passed. Backend root returned expected 404; health/OpenAPI/docs 200; /metrics 404. Frontend/Adminer roots 200. Internal Traefik and localhost STAGE Host-header root/health/OpenAPI each 200. DEV remained Synced/Healthy and was not redeployed.

[Argo source Kustomize patches](https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/#patches).

## J. Legacy dev namespace decision

Not recreated. Remaining references are retained legacy k8s examples, old RBAC examples and historical reports. Active desired state is deploy/overlays/dev and deploy/overlays/stage, targeting app-dev/app-stage. Neither current pipeline uses legacy dev; pipelines use jenkins-ci/jenkins-publish. Ciphertext recovery does not require a live dev namespace. No need was established to recreate it.

## K. Traefik setup

Helm chart 39.0.0, image v3.6.7, one replica, ClusterIP, metrics enabled with stable labels/named port. Publish actual local ingress status IP 127.0.0.1, because Argo v3.5.4 waits for an ingress address in sync wave -2. This resolved a fresh-install health gate without changing app manifests.

Single-node hostPorts require `maxSurge=0,maxUnavailable=1`. Initial default rolling update stalled because a second pod could not bind ports; corrected chart values and retry succeeded. Brief ingress downtime during replacement is expected locally. HTTP/HTTPS localhost listeners work; unmatched HTTPS returns 404 using Traefik's default certificate. Public DNS/trusted TLS were not configured. Traefik exporter returned 200 with reload/request/response/latency metrics after test traffic. STAGE internal/localhost root, health and OpenAPI routing returned 200 after deployment.

## L. Argo CD setup

Pinned v3.5.4 official install manifests, server-side applied into argocd. All seven pods Ready. Server and controller/server/repo metric Services exist as ClusterIP. Controller, server and repo exporters returned HTTP 200, including app-info and Git-request series. These exporters are now also verified UP in Prometheus (section O).

Applications: app-dev, app-stage and monitoring all active, Synced/Healthy. No ApplicationSet installed, no app-prod Application/namespace. Kind fastapi project permits only app-dev/app-stage; Secrets/Namespaces remain operator-managed. Monitoring uses its existing scoped project. Repository main is accessible without recovered Argo repository credentials.

## M. Jenkins strategy


Jenkins recovery inspection (2026-10-09) found the previous host values file and cached Helm chart 5.9.56/appVersion 2.568.3; private copies are preserved under ignored .migration-backup/jenkins. No old Jenkins home/jobs/credential store was located. Current kind has no Jenkins namespace/release/PVC; host service absent. Recovered values use NodePort and do not contain full JCasC/jobs, so they must not be blindly reapplied. Actual trusted pipeline uses credential ID gitops-app while README lists gitops-write.

At the recovery safety gate, host available 4087Mi; kind 3.989GiB; monitoring 608Mi/77m CPU. Application CI containers permit 5120Mi before inbound agent, and cached controller defaults permit 4096Mi. No safe normal-build peak was established; per the user's explicit stop instruction Jenkins was not recreated. No platform resources/pipelines were changed. See JENKINS_RECOVERY_REPORT.md for evidence, recovered artifacts and the capacity/configuration procedure. Separate build capacity or a reviewed larger host/bounded budget is required before continuing.

Jenkins remains CI. Jenkinsfile uses Kubernetes agents in jenkins-ci, with Python tests, Node build, privileged BuildKit and disposable loopback PostgreSQL. Trusted publisher uses jenkins-publish, copies verified archives, pushes GHCR digests and writes Git promotions; Argo CD consumes Git desired state. Jenkins does not deploy application workloads.

No active host Jenkins service/JENKINS_HOME or old archive found. A host controller can use the same pipelines via Kubernetes plugin/cloud credentials, but jobs/plugins/folder restrictions/credentials must be restored or provisioned as described in README-jenkins.md. Do not automatically deploy Jenkins into kind. Controller relocation does not move Kubernetes build agents out of kind.

For a host controller: install a supported Jenkins/Java LTS combination, configure a persistent host JENKINS_HOME, restore the matching encrypted credential files if available, and configure both Kubernetes clouds against kind. Use a dedicated identity with reviewed agent-only RBAC, not the kind cluster-admin kubeconfig. Adapt the existing CI RoleBinding subject to that identity; do not blindly apply its old jenkins/jenkins ServiceAccount subject. Allow in-cluster agents to reach the host controller (Docker kind network gateway or explicit host address, WebSocket preferred), and restrict controller executors/concurrency. Current CI files require separate trust/isolation controls; a privileged BuildKit pod on a shared single node does not provide production isolation. No plugin, job, credential or Jenkins build was created in this rebuild.

## N. Monitoring setup

Reused chart 92.2.0 and prepared values/rules/monitors/dashboards. Preflight render flattened 44 resources and passed AppProject permission/internal-Service checks. Before enabling, verified both apps, node pressure conditions, API readiness, OOM counters and about 5GiB host available RAM. Local Jenkins/controller/agents are absent; monitoring was enabled using `CI_DISABLED=yes scripts/bootstrap-kind.sh monitoring`. This intentionally permits monitoring with CI offline; it does not claim measured CI peak safety.

Removed live skip-reconcile and enabled automatic sync; prune=false remains. Startup watcher observed memory/API state; no pressure stop was needed. All six monitoring pods are Ready, zero restarts: Operator, Prometheus, Grafana, Alertmanager, kube-state-metrics and node-exporter. Prometheus 2Gi and Alertmanager 256Mi PVCs are Bound. Application Synced/Healthy, no ComparisonError, successful operation.

Live Argo source uses inline Helm values from monitoring/bootstrap.py because the local Git files remain unpublished. No manual Helm monitoring release was installed. Final argocd/app-monitoring.yaml now represents enabled, unpaused Git-backed desired state; do not apply it until these files are published to main. Bootstrap generator always emits a paused Application regardless of the final file's enabled state, so a fresh rebuild must still pass the explicit activation gate. DEV/STAGE application Git paths and immutable digests remain unchanged.

Prometheus/Grafana/Alertmanager Services are internal ClusterIP; no monitoring Ingress, NodePort or LoadBalancer. Grafana remains anonymous Viewer with initial admin creation disabled.

## O. Prometheus validation

Prometheus /-/ready, /api/v1/targets and /api/v1/rules returned 200. All 16 active scrape targets are UP with no scrape errors: node-exporter, kube-state-metrics, three kubelet endpoints (including cAdvisor/container metrics), Argo controller/server/repo, Traefik, API server, Grafana, Operator and Prometheus/Alertmanager/reloader targets. Stable ServiceMonitor/PodMonitor discovery, no hardcoded pod IPs.

CPU, memory, deployment replica and restart queries returned eight series each with app-dev and app-stage separated. Node memory, Argo application state, kubelet container data, Traefik response-code counters, latency buckets and reload success returned nonempty results. Argo sync-rate/reconciliation/Git-request dashboard queries returned data. Additional benign DEV/STAGE traffic is used to verify finite Traefik p95 latency rather than treating an idle NaN as a measured latency. Exact reusable checks are in scripts/verify-kind-monitoring.py; transcript is ignored .tools/verify-monitoring.log.

## P. Grafana validation

Grafana health/datasource/search APIs returned 200. Prometheus datasource UID prometheus exists. Four dashboards are provisioned: platform-nodes, dev-stage-workloads, gitops-argocd, ingress-traefik. Validated every stored panel expression against Prometheus and through Grafana /api/ds/query, with both DEV and STAGE selections for workload panels: 4 node, 12 workload/namespace, 4 Argo and 4 Traefik checks returned data. This verifies API provisioning/query execution; no manual browser visual review is claimed.

The initial verifier opened the Grafana forward before pod readiness, so that forward exited. The verifier now waits for all monitoring pods Ready and the rerun passed. Temporary validation forwards were closed afterwards. Access locally:

```bash
kubectl --context kind-fastapi-dev port-forward --address=127.0.0.1 -n monitoring svc/monitoring-grafana 13000:80
kubectl --context kind-fastapi-dev port-forward --address=127.0.0.1 -n monitoring svc/monitoring-prometheus 19090:9090
```

Run each in its own terminal. Grafana http://127.0.0.1:13000; Prometheus http://127.0.0.1:19090. No public exposure.

## Q. Alerts

All eight expected alert rules loaded and evaluated with health=ok and no lastError: NodeMemoryPressure, NodeDiskPressure, NodeHighCPU, NodeHighMemory, ApplicationRestartSpike, ApplicationDeploymentUnavailable, ArgoApplicationUnhealthy, ArgoApplicationOutOfSync. Alertmanager null receiver retained; no external/production notification routing.

## R. Resource usage

Measurements at 2026-10-09T14:25:33.988650+00:00 and 2026-10-09T14:34:38.874042+00:00; idle/test snapshots, not sustained CI/load guarantees.

| Measurement | Before monitoring (DEV+STAGE) | After monitoring validation |
| --- | --- | --- |
| Host available RAM | 5112Mi | 3987Mi |
| Docker kind memory | 2.216GiB / 7.755GiB | 4.068GiB / 7.755GiB |
| Node memory / CPU | 2273Mi / 920m | 4035Mi / 1215m |
| DEV | 132Mi / 44m | 138Mi / 65m |
| STAGE | 138Mi / 60m | 130Mi / 47m |
| Argo CD | 339Mi / 34m | 413Mi / 42m |
| Traefik | 36Mi / 1m | 31Mi / 1m |
| Monitoring | 0Mi / 0m | 655Mi / 85m |
| cgroup memory.current (includes cache) | 4041Mi | 5453Mi |

Monitoring pods use **655Mi and 85 millicores**, versus configured requests ~1024Mi/280m. The full node/Docker increase also includes control-plane discovery/CRDs, caches and startup effects, not just monitoring pods. Host total 7941Mi; available after validation ~3.9GiB. Swap rose to roughly 67Mi during downloads/startup; no OOMs or pressure conditions. Monitor longer-term trends rather than interpreting one idle sample as a peak budget.

Node allocatable 4 CPU/8131772Ki memory. Pre-monitoring requests 2100m CPU/1706Mi memory, limits 4700m/4948Mi. Monitoring adds requests ~280m/1024Mi; post-monitoring requests 2380m CPU/2730Mi and limits 6350m/7700Mi. Some control-plane/Argo containers are unbounded; those limit sums do not guarantee a safe physical host budget. No new scheduler/controller-manager restarts during this rollout; each retains one historical bootstrap lease-timeout restart. OOM/oom_kill counters remain zero; all pods Ready. Disk free ~26GiB (57% used), compared with 34GiB before image downloads.

**DEV+STAGE+Argo+Traefik+monitoring fit safely for the observed local workload with Jenkins offline.** Retention/load/peak behavior still needs observation. **Jenkins controller may fit outside kind with a reviewed bounded memory budget, but Jenkins restoration/build safety is not validated.** Current CI agent requests ~1280Mi and permits ~5Gi memory limits before inbound agent/controller/publisher demand. Remaining ~3.9GiB cannot guarantee that peak; **CI builds could cause dangerous pressure**. Keep CI offline until concurrency/resource budgets and representative builds are measured (or use separate CI capacity). Controller relocation alone does not move existing Kubernetes agents out of kind. PROD remains a separate cluster.

Final confirmation at 2026-10-09T14:41:04.990251+00:00: all three Applications Synced/Healthy; monitoring 611Mi/89m CPU, kind 3.874GiB / 7.755GiB, node 3978Mi/1449m, host available 4196Mi. No pressure/OOM or new control-plane restarts. Jenkins/CI stays offline.

## S. Remaining gaps

Jenkins home/jobs/plugins/credentials/cloud trust restrictions and representative CI peak budget remain unimplemented. No Jenkins Prometheus plugin installed. FastAPI /metrics still returns 404; application instrumentation was not changed. Local storage remains disposable; protect off-host Sealed Secrets key backups. Future Git publication is needed to replace inline monitoring values with the final multi-source Git Application; no commit/push was performed. Browser appearance, long-running monitoring retention/load, CI isolation and production durability are not validated.

## T. Exact rebuild procedure

Prerequisites: Docker/cgroup v2, kind v0.33.0, compatible kubectl (prefer 1.35.x), Helm, Python3/PyYAML, curl, kubeseal v0.39.1, free localhost ports 80/443, network access. Supply private key backup securely; configure host Docker GHCR access with a package-reader credential. Existing encrypted files are restored, not regenerated on reruns.

```bash
export SEALED_SECRETS_KEY_BACKUP=/private/path/sealed-secrets-keys.yaml
scripts/bootstrap-kind.sh base
python3 scripts/recover-dev-secrets.py
python3 scripts/restore-kind-registry-auth.py
scripts/bootstrap-kind.sh dev
scripts/bootstrap-kind.sh stage
python3 scripts/verify-kind-app.py stage
python3 scripts/capture-kind-capacity.py .tools/capacity-before-monitoring.json
CI_DISABLED=yes scripts/bootstrap-kind.sh monitoring
python3 scripts/verify-kind-monitoring.py
python3 scripts/capture-kind-capacity.py .tools/capacity-after-monitoring.json
```

The existing local encrypted STAGE files are already provisioned and remain uncommitted. If starting without those ciphertext files, `python3 scripts/create-stage-secrets.py` is an explicit operator action to create new values; it refuses to overwrite live Secrets and preserves existing complete ciphertext files. SMTP password is optional/unconfigured. STAGE phase uses local HTTP patches, no app-tls required.

CI_DISABLED requires local Jenkins/controller/agents absent; keep builds offline. Once CI is restored, repeat measured peak review and use CI_CAPACITY_VERIFIED=yes only when that review actually passed. Bootstrap checks memory/node conditions; startup watcher requests pause/termination on pressure/errors without deleting data. API outages can prevent pause requests, so verify state after recovery.

After explicit commit/push approval and publication of monitoring files, apply argocd/app-monitoring.yaml to switch to the final Git-backed sources, then verify targets/dashboard data/capacity again. Do not apply it while remote paths are absent. No bootstrap phase creates PROD/legacy dev/Minikube or deletes clusters/PVCs.

## U. Exact commands run

Key execution commands (no secret payloads included):

```bash
python3 scripts/create-stage-secrets.py
scripts/bootstrap-kind.sh stage
python3 scripts/verify-kind-app.py stage
python3 scripts/check-kind-capacity.py
python3 scripts/capture-kind-capacity.py .tools/capacity-before-monitoring.json
CI_DISABLED=yes scripts/bootstrap-kind.sh monitoring
python3 scripts/verify-kind-monitoring.py
python3 scripts/capture-kind-capacity.py .tools/capacity-after-monitoring.json
kubectl --context kind-fastapi-dev wait -n monitoring pod --all --for=condition=Ready --timeout=180s
kubectl --context kind-fastapi-dev top nodes
kubectl --context kind-fastapi-dev top pods -A
kubectl --context kind-fastapi-dev top pods -n monitoring
kubectl --context kind-fastapi-dev describe nodes
docker stats --no-stream
free -h
```

Recovered key/base/DEV actions and fixed Traefik ingress status/zero-surge rollout are documented in preceding sections. Earlier inspection found Minikube already deleted; it was never recreated. Follow-up stage secret logs were redacted in memory before output. Admin correction resealed only FIRST_SUPERUSER_PASSWORD; Argo retried its hook without deleting data. Monitoring chart 92.2.0 was pulled/rendered locally for preflight; live deployment used Argo, not Helm install. Monitoring validation uses temporary localhost forwards and closes them. Final requested Git/resource/status/report displays were executed. Local diagnostics/capacity JSONs remain ignored under .tools. No registry push, Jenkins build, commit or Git push was run.

## V. Readiness for continued DEV/STAGE work

DEV and STAGE are ready for initial local work, with newly recreated test databases. Both and monitoring are Synced/Healthy and validated. DEV was preserved during STAGE/monitoring rollout. Monitoring is internal only and active. Jenkins/CI remains offline and unvalidated; do not enable builds under the assumption that idle monitoring headroom proves CI safety.

## W. Exact next steps before PROD

STAGE and local monitoring are now validated. Restore/provision Jenkins trust boundaries and validate CI resource peaks without disturbing DEV/STAGE. For PROD, provision a separate adequately sized cluster, durable storage/backups, reviewed environment-specific secrets, DNS/TLS, ingress/authentication, CI isolation and monitored recovery procedures. Review PROD manifests and create PROD resources only after an explicit separate authorization. The current local bootstrap intentionally has no PROD path.
