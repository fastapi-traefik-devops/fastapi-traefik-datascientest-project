# Jenkins recovery report — bounded host CI

2026-10-09 UTC. **Jenkins is online outside kind at http://127.0.0.1:8085/. One agent/executor. Smoke build #4 and controlled app-ci/main #1 succeeded. DEV, STAGE and monitoring remain Synced/Healthy.** No Kubernetes writes, project commit/push, registry publication, public exposure, PROD or legacy dev creation.

## Architecture decision and why Jenkins was offline

The old controller was a Minikube StatefulSet with an 8Gi local PVC. Minikube was deleted manually; no Jenkins controller, service, PVC, namespace or Helm release existed in kind, and no host Jenkins service/home was found. There was no failing pod to repair. Jenkins previously stayed offline because its old controller/agent allowances exceeded physical host headroom. Historical ENOSPC was an earlier issue, not the current absence.

Jenkins now uses three Docker containers on Ubuntu: host-jenkins, host-jenkins-agent and host-jenkins-docker. Kind retains only the application platform. No Kubernetes agents/clouds/RBAC are installed. The controller has zero executors; the single dedicated agent has one, enforcing one running build globally. This follows [official Jenkins Docker guidance](https://github.com/jenkinsci/docker/blob/master/README.md) for controller isolation and WebSocket agents. The user's initial one-executor requirement is satisfied by the worker, rather than executing repository code on the controller.

Container installation was chosen over a host Java/package service because JVM, agent and nested builds can all have explicit cgroup CPU/RAM/swap limits. Docker Compose is absent; the reproducible installer uses Docker CLI, without installing additional Ubuntu packages. No host Docker socket, kubeconfig or application secrets are mounted. The agent talks to a separate TLS Docker-in-Docker daemon, whose private cgroup namespace contains its build descendants. The daemon has no published ports. Privileged DinD is appropriate only for this administrator-controlled development CI; it is not a hostile-code security boundary.

## Recovery evidence and persistent data

Recovered originals remain unchanged: /home/root-admin/jenkins-values.yaml (238 bytes) and /home/root-admin/.cache/helm/repository/jenkins-5.9.56.tgz (85033 bytes). Private copies are in ignored .migration-backup/jenkins, directory 0700/files 0600. The cached chart identifies appVersion 2.568.3, but is not definitive proof of the exact last live release. Chart SHA256: f4377bbf9b99723ae69c778fcc69104cda27854f66e6a61a6c800ea94db54f3e.

No old Jenkins home, credentials/encryption files, account store, job definitions, plugin inventory, history or archive was recovered. **This is a fresh controller reconstructed from source, not a restoration of old persistent state.** Old job history and credentials remain unrecovered. The previous report is retained privately as JENKINS_RECOVERY_REPORT.before-host.md. Existing Sealed Secrets recovery material was untouched and cannot substitute for Jenkins' own encryption files.

Recovered values used NodePort and Kubernetes cloud/namespace jenkins-publish; these were inspected but deliberately not installed. Git supplies application/trusted pipeline logic and CI scripts; the newly added configuration supplies the host controller, plugin locks, single node and manual jobs.

Persistent named volumes, independent of kind:

- host-jenkins-home: configuration, users, encryption files, jobs, plugins, build history and artifacts.
- host-jenkins-plugins: reproducible plugin installation cache.
- host-jenkins-work: worker workspace/remoting state; job workspaces are cleaned after builds.
- host-jenkins-docker: disposable image/build cache; no application database data.
- host-jenkins-client-certs and host-jenkins-server-certs: Docker TLS material.

No Jenkins PVC is expected outside Kubernetes. Docker named volumes have no size quota. Host disk free space stayed above 21Gi during validation; the guard stops CI below 5Gi. The original application PostgreSQL data and all kind PVCs were untouched. No volumes were deleted. Only the newly created worker container was replaced to correct its TLS endpoint, retaining its workspace volume; old recovered files and all controller history were preserved.

For a consistent backup, disable/quiet jobs, wait for active builds, stop host-jenkins, archive the entire home volume with numeric ownership (including credentials.xml and matching secrets/master.key/hudson.util.Secret), encrypt and store off-host, then restart. Preserve private bootstrap passwords, TLS material and configuration/locks separately. Never repair startup by deleting the home volume.

## Resource budget reviewed before installation

Host: 7941Mi RAM, four CPUs. Immediately before installation: 4216Mi available; Docker kind working-memory display 3.887GiB; swap 66Mi. A previous safety snapshot had node 4079Mi, monitoring 608Mi and kind about 3.99GiB. Values are timestamped observations, not a fixed reservation.

Old Kubernetes CI templates:

| Container | Memory request | Memory limit | CPU request / limit |
| --- | --- | --- | --- |
| Python tester | 256Mi | 1024Mi | 250m / 1 |
| Node tester | 256Mi | 1024Mi | 250m / 1 |
| BuildKit | 512Mi | 2048Mi | 250m / 2 |
| Disposable PostgreSQL | 256Mi | 1024Mi | 250m / 1 |
| Inbound agent chart default | 512Mi | 512Mi | inherited default |
| Controller chart default | 256Mi | 4096Mi | 50m / 2 |
| Separate publisher | 256Mi | 1024Mi | 250m / 1, plus inbound agent |

The four CI containers alone allowed 5120Mi simultaneously; inbound agent made approximately 5632Mi before controller. Per-job disableConcurrentBuilds did not prevent different branches/jobs or the asynchronous publisher overlapping. Those old values are not used by host CI.

Proposed host values were shown before implementation:

| Host component | Hard memory limit | JVM heap / expected use | CPU cap |
| --- | --- | --- | --- |
| Controller | 768Mi | heap 384Mi; expected ~400–600Mi working use | 0.5 |
| One inbound agent | 256Mi | heap 128Mi; expected ~80–150Mi including Git/CLI | 0.25 |
| Docker daemon and all descendants | 1536Mi | tools + daemon + charged filesystem cache | 1.25 |
| Aggregate additional CI allowance | **2560Mi / 2.5Gi** | Includes build containers below | **2 cores** |

All three set memory-swap equal to memory, allowing no swap for CI containers. Startup checks remaining unused CI allowance plus a 1Gi host reserve; a fresh stack therefore needs at least 3.5Gi available. Plugin installation is separately capped at 768Mi and completes before controller startup; plugin changes require the controller stopped.

Tools are created sequentially, not kept concurrently alive:

| Tool | Hard RAM / CPU cap | Coexisting tool data |
| --- | --- | --- |
| Python tests | 512Mi / 1 core | Disposable PostgreSQL 128Mi / 0.25 core only during backend tests |
| Frontend/manifest checks | 640Mi / 1 core | NODE_OPTIONS heap 384Mi |
| BuildKit archives | 1024Mi / 1 core | max-parallelism=1; backend then frontend |

Docker tooling has no Kubernetes memory requests. All inner processes share the outer 1536Mi/1.25-core cap; their individual limits are **not added** to the 2.5Gi total. Existing healthy kind usage remains unchanged by configuration. At the pre-installation observation, 4216Mi available minus 2560Mi additional allowance left 1656Mi, exceeding the approximately 1Gi reserve. Higher future platform demand still requires a fresh check.

## Installation, plugins, jobs and credentials

Reused controller candidate jenkins/jenkins:2.568.3-jdk21, digest sha256:c1e4c349365f6d16d88595b2c5f7e8ff39b8ae1d061f62420bac193b4b9616d0. Build daemon docker:29.1.3-dind, digest sha256:173f284a4299164772a90f52b373e73e087583c0963f1334c9995f190ef6f3f5. Agent uses the same Java image and remoting jar from the running controller; Docker/Buildx clients come from the pinned daemon image.

Recovered applicable plugin pins retained: workflow-aggregator 608.v67378e9d3db_1, git 5.10.1, configuration-as-code 2121.v86fe99d4b_b_a_b_. Kubernetes plugin/cloud are not required outside kind. Added compatible plugins required by existing pipeline steps/bootstrap: Job DSL, Credentials Binding, JUnit, Pipeline Utility Steps, HTTP Request, Copy Artifact, Lockable Resources, GitHub Branch Source, Pipeline Build Step and Basic Branch Build Strategies. **83/83 installed plugins active**, including dependencies. Direct pins and the complete resolved lock are in infra/jenkins-host; this is a reconstructed plugin set, not a recovered inventory.

JCasC defines one fresh admin, signups disabled, no anonymous read, no controller executors and one exclusive host-ci worker. No other users exist; multiuser/folder authorization requires review before opening CI to others. Admin password is generated once into ignored .jenkins-host/secrets/jenkins-admin-password (0600), mounted as a file and resolved using [JCasC SecretSource](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/secrets.adoc). Agent authentication uses another private file and -secret @file; no authentication value is printed or embedded in process arguments/configuration source.

Manual jobs:

- host-smoke: checkout, shell, Docker info, tiny FROM scratch image build/remove and workspace cleanup.
- app-ci/main: local host variant of Jenkinsfile, preserving checks, GitOps-only skip behavior, immutable source SHA and artifacts. **Disabled by default and again after guarded validation.** No publisher trigger.
- trusted/publish: **disabled recovery placeholder**, not a claimed restoration of the credential-bearing publisher.

Existing Jenkinsfile/Jenkinsfile.promote and CI scripts are unchanged. The host variant uses public main checkout and reviewed local source because new configuration is uncommitted/unpublished. No webhooks, branch scans or automatic triggers are enabled. Existing trusted publishing must remain separate from reusable application workers.

Public repository checkout works without a GitHub credential. Missing original credential IDs: ghcr-write (registry write identity/token), gitops-app (Git write identity satisfying the existing Username/Password binding/App strategy), ci-read (restricted Jenkins API identity). No old credential store was found. Host registry pull access is not proof of approved Jenkins write access; no credentials were fabricated/imported blindly and no real registry/Git publication was tested. Supply these securely through Jenkins and review a separate trusted agent before enabling publisher. A push would require separate user approval in this session.

## Validation and capacity results

Login page HTTP **200**; authenticated API succeeds; anonymous API returns **403**. Only published Jenkins listener is **127.0.0.1:8085 -> 8080**; no ingress/public DNS/TLS/agent port was added. Controller running, host-ci online, controller executors=0 and worker executors=1. All three Docker restart counters zero, OOMKilled false; cgroup oom/oom_kill counters zero. Daemon max counter=1 reflects hitting/reclaiming at its cap, not an OOM kill. Kind OOM counters/restart count remain zero. Historical Kubernetes scheduler/controller-manager restarts from initial platform bootstrap remain historical.

Initial setup checks found a Docker TLS alias mismatch and a smoke Groovy quoting error; fixed both before successful validation. Jenkins' own declarative validator accepts both host pipelines. Bootstrap rerun preserves the same controller and volumes.

**host-smoke #4: SUCCESS**, roughly 180s including first compilation/checkout. Checkout revision cb1bb5617741cd5b68d36b9d419b6014226b6751; workspace/shell passed; Docker 29.1.3 worked over TLS; scratch image built and removed; workspace and temporary runtime containers cleaned. Sampled controller peak 514Mi, agent 134.5Mi; minimum available host memory **3498.7Mi**. This proves image-build capability, not application image-build peak.

**app-ci/main #1: SUCCESS**, guarded observation ~515s. Three overlays each validated 13/13 resources, zero invalid/errors; **12 CI unit tests passed** (213.712s). Tests create/delete isolated /tmp Git fixtures and write only to their temporary local remotes, not the project remote. Production manifests were rendered for existing source validation only; no PROD resources/Application were created. The checked-out main commit changed only documentation/argocd/deploy files, so the original GitOps-only logic skipped backend checks, frontend application build and image archives. **Do not interpret this as a measured full application build.** No real registry publication or project commit/push occurred.

Measured controlled-CI peaks: controller **565.8Mi**, agent **130.7Mi**, daemon working-memory Docker display **224.4Mi**. A sampled inner validation container used **51.17Mi / 640Mi** and ~0.98 CPU core. Daemon cgroup memory.current was approximately **1426Mi**, largely image filesystem cache, under its **1536Mi memory.max**; memory.swap.max=0. Docker working-memory display excludes some cache, so it must not be mistaken for total cgroup charge. CPU was throttled by the configured limits; brief sampled percentages can differ from quota-period averages.

Host available RAM never below **3430Mi / 3.35Gi** in controlled CI. Swap rose from **208.7Mi to 303.7Mi** over ~8.6 minutes; maximum observed increase within 60s was **40.1Mi**, below the 256Mi/min abort threshold. Startup/idle image pulls also increased swap relative to the initial 66Mi; it was not unchanged. No kind/API/application readiness degradation was observed.

Final snapshot 16:15:19 UTC:

| Measurement | Value |
| --- | --- |
| Host total / available | 7941Mi / 3555Mi |
| kind Docker working memory / cgroup charge | 3.25Gi / 3945Mi |
| Kubernetes node memory / CPU | 3321Mi / 1326m |
| DEV / STAGE | 129Mi / 129Mi |
| Argo CD / Traefik | 516Mi / 22Mi |
| Monitoring | 546Mi / 101m |
| Jenkins controller typical warm idle | ~528Mi, usually <0.02 core after initialization |
| Agent typical warm idle | ~120Mi, usually <0.02 core |
| Docker daemon warm cache display | ~217Mi, usually <0.01 core; reclaimable cache additional |
| Host disk available at CI finish | 21.55Gi |

Snapshots have different sampling times and cache accounting; before/after are not proof that installing Jenkins reduced kind demand. Available memory fell roughly 0.65Gi from the pre-install observation to the final snapshot, while platform usage varied. The physical host remains shared.

**Conclusion:** kind platform plus bounded idle Jenkins, smoke build and GitOps/CI checks fit with a large measured reserve. Jenkins should stay outside kind on this host. One normal application build is bounded by the reviewed caps and must run through the guard; its successful completion/actual peak remains unverified. Do not enable automatic/full or trusted publishing jobs yet. No monitoring or application resources were reduced to fit Jenkins.

## Guard, remaining risks and next steps

The verifier requires 2.5Gi available before submitting a job and checks kind API, required Argo apps, node pressure/readiness and platform pods. During CI it stops only the agent and daemon if available RAM <1Gi, swap growth >256Mi within about a minute, disk free <5Gi, API instability or readiness degradation. It disables app-ci/main in finally, including submission failure. It never stops kind or deletes persistence. Do not bypass it with an unguarded full UI build.

Remaining gaps: full backend tests/frontend/image-archive peaks and push credentials unverified; old state unavailable; privileged DinD/shared worker unsuitable for untrusted forks; single-host CPU/cache/disk contention; artifact/cache growth (host artifacts retained for two builds, five build records); no Jenkins metrics plugin or FastAPI instrumentation added. Jenkins monitoring remains a gap and the monitoring deployment was unchanged. Existing Kubernetes Jenkinsfiles still need separate capacity if used elsewhere; host jobs use only the bounded host variant.

Next: supply recovered old Jenkins home if found; supply write credentials securely only when publishing is needed; run a guarded application-changing revision or explicitly reviewed full-check test to measure Python/Postgres/frontend/BuildKit peaks; keep limits unchanged unless actual failures justify a new budget review. Configure isolated trusted publication and multiuser authorization before enabling publishing. For larger tests/images or concurrent/fork builds, use a separate CI build host with more RAM/CPU, retaining this controller and Argo CD GitOps. Do not increase concurrency or return agents to kind. PROD stays on its future separate cluster after environment/security/release review.

## Files and exact rebuild/access commands

Added infra/jenkins-host/{jenkins.yaml,jobs.groovy,plugins.txt,plugins.lock.txt,images.lock.json,Jenkinsfile.smoke,Jenkinsfile.host,run-tool.sh,buildkit.toml,README.md}; scripts/bootstrap-jenkins-host.py, sync-jenkins-host-jobs.py, verify-jenkins-host.py. Updated .gitignore for private .jenkins-host and this report. Existing application/monitoring/Traefik/Argo configuration and original Jenkinsfiles were not edited. Other earlier migration changes remain uncommitted; DEV_SETUP_REPORT.md already had a user change.

```bash
# Rebuild on this Ubuntu amd64 host; requires Docker, Python3 and read-only host kubectl access.
python3 scripts/bootstrap-jenkins-host.py
python3 scripts/sync-jenkins-host-jobs.py
python3 scripts/verify-jenkins-host.py --check-only
python3 scripts/verify-jenkins-host.py
# Only after reviewing budget/results; no publisher trigger:
python3 scripts/verify-jenkins-host.py app-ci/main
# Local UI:
# http://127.0.0.1:8085/ — admin; read stored password privately, never print it into logs.
# From another workstation:
ssh -L 8085:127.0.0.1:8085 root-admin@YOUR_UBUNTU_HOST
```

Exact operational commands used (bootstrap contains the full Docker arguments and limits):

```bash
docker pull jenkins/jenkins:2.568.3-jdk21
docker pull docker:29.1.3-dind
python3 scripts/bootstrap-jenkins-host.py > .tools/jenkins-host-bootstrap.log 2>&1
# TLS-only correction of newly created agent, retaining every volume:
docker network disconnect host-jenkins-build host-jenkins-docker
docker network connect --alias docker host-jenkins-build host-jenkins-docker
docker stop host-jenkins-agent
docker rm host-jenkins-agent
python3 scripts/bootstrap-jenkins-host.py > .tools/jenkins-host-bootstrap-retry.log 2>&1
# Buildx client copied from pinned image; subsequent fresh agents mount it via bootstrap:
docker cp host-jenkins-docker:/usr/local/libexec/docker/cli-plugins/docker-buildx .jenkins-host/docker-buildx
docker exec --user 0 host-jenkins-agent mkdir -p /usr/local/libexec/docker/cli-plugins
docker cp .jenkins-host/docker-buildx host-jenkins-agent:/usr/local/libexec/docker/cli-plugins/docker-buildx
docker exec host-jenkins-agent docker buildx version
python3 scripts/sync-jenkins-host-jobs.py
python3 scripts/verify-jenkins-host.py > .tools/jenkins-host-smoke-success.log 2>&1
python3 scripts/verify-jenkins-host.py app-ci/main > .tools/jenkins-host-full-validation.log 2>&1
python3 scripts/bootstrap-jenkins-host.py > .tools/jenkins-host-idempotent.log 2>&1
python3 scripts/capture-kind-capacity.py .tools/capacity-host-jenkins-final.json
docker exec host-jenkins-docker cat /sys/fs/cgroup/memory.max
docker exec host-jenkins-docker cat /sys/fs/cgroup/memory.swap.max
docker exec host-jenkins-docker cat /sys/fs/cgroup/memory.events
curl -sS -o /dev/null -w 'Jenkins login HTTP %{http_code}\n' http://127.0.0.1:8085/login
free -h
docker stats --no-stream
ps aux --sort=-%mem | head
kubectl --context kind-fastapi-dev top nodes
kubectl --context kind-fastapi-dev top pods -A
kubectl --context kind-fastapi-dev get applications -n argocd
kubectl --context kind-fastapi-dev get pods -A
git diff --check
git diff
git status --short
```

Private diagnostic logs/capacity/health JSONs are in ignored .tools. Script syntax compilation, shell syntax and git diff whitespace checks passed. Final check-only preflight passed with node pressure/readiness, Argo applications, pods and parent cgroup checks; no additional build was submitted. No commit or push.
# Historical report: the active Phase 1 setup is documented in
# [infra/jenkins-host/README.md](infra/jenkins-host/README.md).
