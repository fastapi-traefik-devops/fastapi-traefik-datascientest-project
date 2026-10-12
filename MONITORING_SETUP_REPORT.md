# Monitoring setup report

Updated 2026-10-09 UTC. Context kind-fastapi-dev, Kubernetes v1.35.8.

**Monitoring is active, Synced/Healthy and validated. DEV and STAGE remain Synced/Healthy. Jenkins and CI are offline.** All six monitoring pods are Ready, zero restarts, and both PVCs are Bound. No public monitoring exposure, PROD, legacy dev or Minikube was created. No commit/push performed.

## Configuration and GitOps

Reused kube-prometheus-stack 92.2.0, prepared monitoring values, monitors, rules and dashboards. Preflight rendered 44 resources and verified AppProject permissions/internal Services. Operator/CRDs v0.94.1; Prometheus v3.15.0-distroless; Alertmanager v0.34.1; Grafana v13.2.3-distroless from the pinned chart. Single replicas, no HA, Prometheus 3d/1500MB retention, 60s scrape/evaluation. Configured total steady requests ~1024Mi/280m CPU.

The live Argo Application uses inline Helm values generated from existing files by monitoring/bootstrap.py because the repository files are still unpublished. Argo deployed the stack; no manual monitoring Helm release. argocd/app-monitoring.yaml now represents enabled/unpaused final Git-backed desired state with conservative prune=false. Apply that source only after monitoring files are published to main; applying it before remote paths exist would fail. Bootstrap generator always emits a paused Application so a fresh rebuild cannot bypass the explicit capacity phase.

Live skip-reconcile was removed and auto-sync deliberately enabled after both app validations and memory/node/API checks. Used `CI_DISABLED=yes scripts/bootstrap-kind.sh monitoring`: local Jenkins/controller/agents are absent, and builds remain offline. This is not a claim of measured CI peak safety. Startup watcher found no pressure stop necessary. No ComparisonError or manifest-generation errors remained.

Existing ServiceMonitor/PodMonitor definitions select Argo Services and Traefik through stable labels/named ports; no pod IP is hardcoded. Monitoring discovery/rules are scoped to the monitoring namespace; workload panels/alerts use app-dev and app-stage, not legacy dev. Prometheus 2Gi and Alertmanager 256Mi local-path PVCs are Bound; pruning/deletion safeguards retained. Grafana storage is ephemeral and dashboards/datasource are reproducible. Local storage is not production durability.

## STAGE prerequisite completed

User authorized fresh STAGE credentials. Generated independent random SECRET_KEY, FIRST_SUPERUSER_PASSWORD and POSTGRES_PASSWORD, matching backend/database passwords; only encrypted SealedSecrets were saved. Initial admin password exceeded the schema's 40-character maximum; corrected only that new password to 32 characters, resealed, and migration retry succeeded without recreating the database.

Local STAGE HTTP Application patches remove TLS and change frontend/CORS origin to HTTP; standard HTTPS overlay remains unchanged. No public TLS certificate required. STAGE PostgreSQL/backend/frontend/Adminer are Ready, backend one replica/worker. SELECT 1, DNS, health/OpenAPI/docs, frontend/Adminer and internal/localhost Traefik checks passed (200, except expected backend root and /metrics 404). DEV was preserved.

## Prometheus validation

/-/ready, /api/v1/targets and /api/v1/rules returned HTTP 200. All **16 active targets UP**, with no lastError:

- node-exporter and kube-state-metrics;
- kubelet metrics, cAdvisor/container metrics and probe endpoint;
- argocd-metrics, argocd-server-metrics, argocd-repo-server;
- Traefik PodMonitor;
- API server, Grafana, Operator, Prometheus/Alertmanager and config reloaders.

CPU, memory, deployment replica and restart queries each returned eight workload series with both app-dev/app-stage separated. Node memory, Argo app state, kubelet container data, Traefik reload/response-code/latency metrics returned nonempty results. Fresh benign requests to both application hosts returned 200 and produced finite Traefik p95 latency. Argo application state, sync-rate, reconcile-duration and Git-request dashboard queries returned data.

## Grafana validation

Grafana health, datasource and search APIs returned HTTP 200. Datasource UID prometheus exists. Four dashboards are provisioned and were checked using their stored expressions, both directly in Prometheus and through Grafana /api/ds/query:

| Dashboard UID | Verified panel/namespace queries |
| --- | --- |
| platform-nodes | 4 |
| dev-stage-workloads | 12 (six panels for each namespace) |
| gitops-argocd | 4 |
| ingress-traefik | 4 |

Every check returned data. This validates provisioning/query execution; no manual browser visual review is claimed. An initial Grafana forward was started before readiness and exited; the verifier now waits for all monitoring pods Ready, and reruns passed. Temporary validation forwards were closed.

## Access, internal only

Run each in a separate terminal:

```bash
kubectl --context kind-fastapi-dev port-forward --address=127.0.0.1 -n monitoring svc/monitoring-grafana 13000:80
kubectl --context kind-fastapi-dev port-forward --address=127.0.0.1 -n monitoring svc/monitoring-prometheus 19090:9090
kubectl --context kind-fastapi-dev port-forward --address=127.0.0.1 -n monitoring svc/monitoring-alertmanager 19093:9093
```

Grafana http://127.0.0.1:13000, Prometheus http://127.0.0.1:19090. Services are ClusterIP; no Ingress, NodePort or LoadBalancer. Grafana requires authentication; anonymous access is disabled and the normal login form is enabled. Sign-up remains disabled. Admin credentials come from the separately provisioned `monitoring-grafana-admin` Kubernetes Secret in namespace `monitoring` (`admin-user` and `admin-password` keys); no credentials are stored in Git or Helm values.

## Alerts

All eight expected rules loaded and evaluated with health=ok and no lastError: NodeMemoryPressure, NodeDiskPressure, NodeHighCPU, NodeHighMemory, ApplicationRestartSpike, ApplicationDeploymentUnavailable, ArgoApplicationUnhealthy, ArgoApplicationOutOfSync. Alertmanager uses a null receiver; no production/external notification routing.

## Resource comparison

Idle/test snapshots at 2026-10-09T14:25:33.988650+00:00 and 2026-10-09T14:34:38.874042+00:00; long-running/load peaks remain unverified.

| Measurement | Before monitoring | After validation |
| --- | --- | --- |
| Host available RAM | 5112Mi | 3987Mi |
| kind Docker memory | 2.216GiB / 7.755GiB | 4.068GiB / 7.755GiB |
| Node memory / CPU | 2273Mi / 920m | 4035Mi / 1215m |
| Monitoring memory / CPU | 0 | 655Mi / 85m |
| DEV memory / CPU | 132Mi / 44m | 138Mi / 65m |
| STAGE memory / CPU | 138Mi / 60m | 130Mi / 47m |

Node requests after monitoring: 2380m CPU/2730Mi; configured limits 6350m CPU/7700Mi. Some control-plane/Argo containers have no memory limits; limit sums are not a safe physical host budget. Total Docker/node growth includes control-plane CRDs/discovery, caches and startup as well as monitoring pods. Host RAM 7941Mi, available after validation ~3.9GiB; disk available ~26GiB. Swap rose to ~67Mi during startup. No OOM/oom_kill or MemoryPressure/DiskPressure/PIDPressure; no new control-plane restarts in this rollout (one historical lease-timeout restart each remains).

**The measured local DEV+STAGE+Argo+Traefik+monitoring platform fits with Jenkins offline.** Monitor retention/query/load trends. A bounded host Jenkins controller may fit, but restoration and build peak safety are unverified. Existing CI pod requests ~1280Mi and allows ~5Gi limits, plus inbound agent/controller/publisher overhead. That peak can exceed remaining headroom and cause dangerous pressure. Keep CI offline until its concurrency/resources and representative build peak are reviewed, or supply separate CI capacity. Moving only the controller outside kind does not relocate Kubernetes build agents.

Final confirmation at 2026-10-09T14:41:04.990251+00:00: all three Applications Synced/Healthy; monitoring 611Mi/89m CPU, kind 3.874GiB / 7.755GiB, node 3978Mi/1449m, host available 4196Mi. No pressure/OOM or new control-plane restarts. Jenkins/CI stays offline.

## Repeatable validation and remaining work

```bash
python3 monitoring/verify-grafana-auth.py
python3 scripts/verify-kind-monitoring.py
python3 scripts/capture-kind-capacity.py .tools/capacity-after-monitoring.json
kubectl --context kind-fastapi-dev top nodes
kubectl --context kind-fastapi-dev top pods -A
kubectl --context kind-fastapi-dev top pods -n monitoring
docker stats --no-stream
free -h
```

Verifier checks required UP targets, DEV/STAGE namespace separation, node/Argo/Traefik series, finite latency after traffic, all eight rules, datasource and every provisioned dashboard panel through Grafana. Diagnostics are in ignored .tools/verify-monitoring.log and capacity JSONs.

FastAPI /metrics still returns 404; no instrumentation added. Future proposal: pinned prometheus-fastapi-instrumentator plus instrument/expose call, backend metrics ServiceMonitor and cardinality/namespace validation. Jenkins metrics remain unavailable: Prometheus plugin/configuration requires separate approval; none installed. Jenkins jobs/plugins/credentials/cloud restrictions and CI peak validation remain work. Final monitoring Git source switch requires approved publication. PROD remains a future separate cluster with durable storage/backups, environment-specific secrets, authentication/DNS/TLS and isolation; no PROD resources created.

## Jenkins recovery inspection update

2026-10-09: Jenkins remains absent/offline. Host values and cached Helm chart were found, but no controller state/credentials/history backup. Memory gate stopped recreation before any runtime or agent was launched: host available 4087Mi; monitoring 608Mi/77m CPU; normal CI containers allow 5120Mi before inbound/controller overhead. Separate build capacity or a reviewed increased host/bounded budget is needed. No Jenkins plugin/scrape target was added, and DEV/STAGE/monitoring were not changed. Details: JENKINS_RECOVERY_REPORT.md.

## Grafana authentication security change

2026-10-09: Disabled `grafana.ini.auth.anonymous.enabled`, enabled the normal login form (`auth.disable_login_form: false`), and removed `GF_SECURITY_DISABLE_INITIAL_ADMIN_CREATION` so Grafana creates its admin account. The pinned chart reads both admin fields through Secret references configured by `grafana.admin.existingSecret`. The password was randomly generated in memory and sent to Kubernetes through stdin; no credential files, command-line password arguments, commits or pushes were used.

Run `python3 monitoring/ensure-grafana-secret.py` before reconciling a fresh installation. It creates the Secret only when absent and preserves existing credentials. The Secret is provisioned separately from Argo CD and must be recreated on a new cluster; it is deliberately absent from Git/Kustomize and Helm-generated resources. Authorized operators can retrieve the password locally with:

```bash
kubectl --context kind-fastapi-dev -n monitoring get secret monitoring-grafana-admin -o jsonpath='{.data.admin-password}' | base64 --decode
```

Username: `admin`. Use the existing loopback-only port-forward and the `/login` page. Grafana still uses ephemeral storage; account changes made only in its database do not survive replacement. Updating the bootstrap Secret alone does not rotate a password in an already initialized Grafana database.

Only Grafana authentication values in the live monitoring Argo CD Application were patched. Argo CD performed the ConfigMap/Deployment reconciliation and rollout; dashboards, providers, datasource and other monitoring values were preserved. The unpublished Git-backed Application source was not activated. `monitoring/values.yaml` carries the same desired settings for eventual publication. No DEV, STAGE, Jenkins or PROD configuration or workload was changed, and verification generates no application traffic.

`monitoring/verify-grafana-auth.py` checks anonymous rejection, dashboard redirection, login form availability, normal `/login` authentication with a session cookie, datasource preservation, dashboard panel equality and all panel queries. It closes its loopback-only port-forward and prints no credentials. The broader existing monitoring verifier now obtains its Grafana authentication from the Secret; it was not run for this security change because it generates DEV/STAGE traffic.

Verified after reconciliation at 2026-10-09 18:29 UTC: monitoring Application **Synced / Healthy**, Argo operation **Succeeded**, Grafana rollout complete. Anonymous search, datasource, dashboard and query APIs each returned **401**; dashboard navigation redirected to `/login`, with the login form enabled. Normal username/password login succeeded and subsequent requests used its session cookie. Prometheus datasource UID/URL and all four dashboards' panel definitions were preserved. Authenticated dashboard queries returned data: `platform-nodes` 4, `dev-stage-workloads` 12, `gitops-argocd` 4, `ingress-traefik` 4 (**24 total**). Service remains **ClusterIP**, has no external IPs, and monitoring has **no Ingress**. No browser visual review is claimed.
