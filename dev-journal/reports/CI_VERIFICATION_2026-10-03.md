# Local verification — 2026-10-03

No changes were pushed, no release/tag/PR was created on GitHub, and no real
Kubernetes or Argo resources were applied. Existing application workloads were
not touched. The pre-existing untracked `.swp` was left untouched.

## Executed checks

| Check | Result |
| --- | --- |
| Kustomize 5.6.0 render, dev/stage/prod | PASS |
| kubeconform 0.6.7, strict Kubernetes 1.31 schemas | PASS: 13 resources/environment, 39 total, no skips |
| YAML parsing | PASS: deployment/Argo/RBAC files and both embedded Jenkins Pod templates |
| Argo AppProject/ApplicationSet schema validation | PASS against official Argo CD v2.13.3 CRD schemas, downloaded to /tmp; not a claim about installed Argo version |
| Jenkinsfiles | PASS offline Groovy 4.0.24 parse through CONVERSION; actual Jenkins Declarative validation not available |
| Shell scripts and embedded pipeline shells | PASS `sh -n` |
| Promotion safety suite | PASS: 12 tests, real temporary local Git remotes and mocked registry; covers CAS retry, stale stage rejection, release ancestry/history/digest checks, review-branch-only writes, idempotence, write-once tags, auth failure |
| Backend mypy/Ruff/format | PASS using uv 0.5.11, frozen lock |
| Backend migrations/pytest | PASS: 55 tests, two SQLAlchemy warnings; disposable PostgreSQL 16, loopback-only, no host ports, stopped afterward |
| Backend JUnit/coverage | Generated `backend/test-results.xml`, `backend/coverage.xml`; 94% coverage (existing scope includes tests) |
| Frontend npm ci / TypeScript / Vite | PASS with Node 20.18.1; sourcemap and large-chunk warnings |
| Dockerfiles | PASS for backend and frontend with local Docker BuildKit; no registry push |
| BuildKit archive / publisher compatibility | PASS: frontend Docker-format export parsed by crane digest without loading/running the image |
| Frontend image | nginx configuration and environment-independent API URL checked locally |
| Diff whitespace / credential review | PASS; no new real plaintext secrets detected; existing .env sensitive keys are placeholders, existing sealed secrets remain encrypted |

Frontend installation reports **61 vulnerabilities: 4 moderate, 54 high, 3 critical**
in the existing dependency tree. These require a separate dependency remediation
review before production; no automatic breaking upgrades were performed. Versions
are pinned for repeatability, not asserted to be current/security-supported.

Local logs are under `/tmp/gitops-*-check.log`, `/tmp/gitops-*-build.log`,
`/tmp/gitops-promotion-tests.log`, `/tmp/gitops-groovy-check.log`, and
`/tmp/gitops-archive-check.log`. Verification images use the local tags
`fastapi-gitops-local/backend:verification` and
`fastapi-gitops-local/frontend:verification`. They were not published. Build cache
and local verification outputs remain available; no shared Docker cache was pruned.

## Not tested end to end

Actual Jenkins plugin/Declarative compatibility, job ACLs/credentials, Kubernetes
cloud scheduling/admission isolation, GitHub webhooks/tag discovery/status checks,
GHCR authentication/uploads/retagging, real GitHub fast-forward pushes/ruleset
bypass, Argo reconciliation, real TLS/ingress/storage, and production health were
not tested. GitHub PR creation is deliberately manual. No credentials were read
from a live Kubernetes Secret. Cluster version was not queried. A controlled
non-production acceptance run is required after the documented setup.

## Final architecture review

| Question | Finding |
| --- | --- |
| Can Jenkins deploy app workloads directly? | Neither pipeline has kubectl/helm/Argo deployment calls or an app kubeconfig. Operator must revoke pre-existing live workload RBAC; repository edits cannot prove existing live permissions are gone. |
| Is Git desired state for all environments? | Yes: main, deploy/overlays/dev, stage, prod; Argo tracks these paths. |
| Are images immutable and commit-tied? | SHA tags are write-once by publisher policy; actual workload images are digest-pinned after promotion. Initial zero-SHA placeholders intentionally do not deploy. |
| Is the same artifact promoted? | Yes: CI archives are copied to GHCR; release only checks/retags recorded digests. No build command in publisher/release code. |
| Can untrusted PRs obtain write credentials? | CI receives none; trusted folder and restricted cloud/node/admission configuration are mandatory. This boundary has not been tested live. |
| Can GitOps commits recurse forever? | No: changed-path filtering validates GitOps-only commits but does not archive/publish/trigger promotion. |
| Can promotions overwrite each other? | Global lock plus one publisher build at a time; fast-forward Git retry; stage freshness/ancestry checks. Prod changes require up-to-date reviewed PRs. Tested locally for Git races. |
| Can prod change without approval? | Release code writes a review branch only after Jenkins approval. Main protections and code-owner reviews must cover shared base/Argo/pipeline paths too. A compromised bypass bot remains a documented GitHub permission limitation. |
| Do all overlays render and validate? | Yes, 39 strict resource schema checks passed without skips. |
| Any real secrets in the change? | None detected; no new plaintext Secret manifests. Historical Git objects were not audited. |
| Does documentation match implementation? | Current guide describes the two-job trust boundary, asynchronous publisher, manual PR, tag discovery/manual fallback, SHA selection, recursion, validation, prerequisites and limitations. Historical guides are marked accordingly. |
