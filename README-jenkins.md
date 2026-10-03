# Jenkins CI

This repository uses the root [Jenkinsfile](Jenkinsfile) to check the backend,
compile the frontend, and build both container images. Jenkins creates a temporary
Kubernetes agent Pod in the `dev` namespace for each build.

The pipeline is CI-only: it does not push images, apply Kubernetes manifests, or
deploy the application. It does not require registry credentials or run kubectl.

## Prerequisites

- A running Jenkins controller and Kubernetes cluster.
- Jenkins plugins: Pipeline (including Declarative Pipeline), Kubernetes, Git,
  JUnit, and Timestamper, with their dependencies.
- An existing `dev` namespace with enough capacity for the agent Pod.
- Controller credentials with permission to manage agent Pods, read their logs,
  and execute commands in their containers in `dev`.
- Network access for Git checkout, container pulls, Python packages, and npm.
- Cluster admission policy that permits the privileged BuildKit container.

The four containers declared in the Jenkinsfile request a total of 1 CPU and
1.25 GiB of memory. Allow additional capacity for the plugin-provided Jenkins
inbound agent and temporary build files.

Docker does not need to be installed on the controller. Builds use BuildKit
inside the agent Pod.

## Open Jenkins locally

For the current installation, the Jenkins Service is `jenkins` in namespace
`jenkins`, exposing port 8080. Run this on the machine hosting your browser:

```bash
kubectl port-forward -n jenkins service/jenkins 8080:8080 --address 127.0.0.1
```

Open <http://localhost:8080> and sign in with your existing Jenkins account.
Leave the command running; press Ctrl+C to stop forwarding. If port 8080 is
occupied, use `8081:8080` and open <http://localhost:8081>.

If kubectl and the forward run on a remote host, open an SSH tunnel from your
own computer in a separate terminal:

```bash
ssh -N -L 8080:127.0.0.1:8080 <user>@<remote-host>
```

Port forwarding opens the Jenkins interface. It does not start the application.

## Configure the Kubernetes cloud

In **Manage Jenkins**, open **Clouds** and configure a Kubernetes cloud. Use the
cloud name `kubernetes` for the default selection used by this Jenkinsfile.
Configure the Kubernetes connection and test it. Agent Pods must be created in
`dev`, as specified by the pipeline.

For this in-cluster installation, use a controller URL reachable from the agent
Pods, such as:

```text
http://jenkins.jenkins.svc.cluster.local:8080
```

For TCP agent connections, configure the Jenkins tunnel as
`jenkins-agent.jenkins.svc.cluster.local:50000`, and ensure the controller's inbound
agent listener is enabled. Alternatively, configure WebSocket agent connections.
Do not use `http://localhost:8080` as the agent-facing controller URL: localhost
inside the agent Pod refers to that Pod.

The [controller RBAC file](k8s/rbac/jenkins-controller-dev-rbac.yaml) describes
agent-management permissions for the `jenkins` service account in namespace
`jenkins`. Check those identity assumptions against your installation before
using it. The broader [agent RBAC file](k8s/rbac/jenkins-dev-rbac.yaml) grants
application and secret management permissions and is unnecessary for this CI
pipeline. This guide does not require applying either file automatically.

The agent Pod disables Kubernetes service account token mounting. The controller
uses its own credentials to manage the agent; the build containers do not need
Kubernetes API credentials.

See the official [Kubernetes plugin documentation](https://plugins.jenkins.io/kubernetes/)
for cloud configuration and agent connection options.

## Create the pipeline job

1. Select **New Item**, give the job a name, and choose **Pipeline**.
2. Under **Pipeline**, select **Pipeline script from SCM**.
3. Select **Git** and enter this repository's clone URL.
4. For a private repository, select a Jenkins-managed checkout credential with
   read access. Keep tokens and private keys out of repository files.
5. Set the branch specifier to the branch containing the updated Jenkinsfile,
   such as `*/main` or `*/master`, matching your repository.
6. Set **Script Path** to `Jenkinsfile`, save, and select **Build Now**.

An uncommitted local Jenkinsfile change will not be loaded by an SCM job. The job
must check out a revision containing that change. No automatic webhook trigger is
configured in this Jenkinsfile; configure triggers separately if needed.

See [Jenkins Pipeline setup](https://www.jenkins.io/doc/book/pipeline/getting-started/)
for SCM job configuration.

## Pipeline stages

| Stage | What it runs |
| --- | --- |
| Checkout | Checks out the job's configured SCM revision once. |
| Backend Checks and Tests | Installs locked dependencies with `uv sync --frozen`; runs mypy, Ruff lint and format checks; waits for the test database, runs Alembic migrations and initial data setup; executes pytest with coverage. |
| Frontend Check | Runs `npm ci` and `npm run build`, including TypeScript compilation and Vite bundling. |
| Build Container Images | Starts BuildKit, waits up to 60 seconds for readiness, and builds the backend and frontend Dockerfiles into local OCI archives. |

Stages run sequentially. An earlier failure prevents later stages from running.
Concurrent runs of the same job are disabled. The execution timeout is 45 minutes
after the top-level agent is allocated; agent provisioning can take additional time.

The temporary Pod contains:

| Container | Purpose |
| --- | --- |
| `python-tester` | Python 3.10 and uv 0.5.11 for backend checks and tests. |
| `node-tester` | Node.js 20 for frontend installation and compilation. |
| `postgres-test` | PostgreSQL 16 for the isolated `app_ci` test database. |
| `buildkit` | BuildKit v0.24.0 for local image builds. |
| Plugin-provided inbound agent | Connects the Pod to Jenkins and manages the shared workspace. |

## Test configuration and credentials

Backend tests connect to `127.0.0.1:5432`, database `app_ci`, user `postgres`.
PostgreSQL listens only on loopback inside the agent Pod and uses the explicit
test-only password configured in the Jenkinsfile. This password is only for the
disposable CI database and must never be reused for an application database. It has no Service or persistent
volume and does not access the application database.

The backend stage generates a fresh signing key and administrator password for
each run, with shell tracing disabled while generating them. The test
administrator email is `ci-admin@example.com`. These are test credentials, not
Jenkins login credentials.

`ENVIRONMENT=local` enables the application's local test behavior. The frontend
uses `VITE_API_URL=http://localhost:8000` for the compile and image-build checks.
This is a CI build setting, not a deployment URL.

The pipeline mounts neither `ghcr-creds` nor `ghcr-pull-secret`. Git checkout
credentials, when needed, are configured in Jenkins separately.

## Results and cleanup

Open the build's **Console Output** for stage logs and failures. Jenkins publishes
`backend/test-results.xml` through JUnit when pytest produces it and archives
`backend/coverage.xml` when coverage data is available. Coverage generation is attempted even when
pytest fails, and pytest's failure status is preserved. Reports can be absent if setup,
linting, or test collection fails before they are generated; their absence does not make a
failed stage successful.

Image builds write `/tmp/backend-ci.tar` and `/tmp/frontend-ci.tar` inside the
BuildKit container. These archives are not published or archived in Jenkins and
are discarded with the temporary Pod. The pipeline cleans all workspace contents through the Python tool container
before the inbound agent removes the workspace, so root-owned build files do not
block cleanup.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Pipeline does not recognize `kubernetes`, `junit`, or `timestamps` | Required plugins and their dependencies are installed and enabled. |
| Agent stays pending or does not connect | Cloud connection, controller RBAC, `dev` namespace, resource capacity, image pull access, and the agent-facing Jenkins URL/tunnel. |
| Pod is rejected as privileged | The current BuildKit configuration requires privileged containers; use an authorized build environment or change the builder configuration. |
| PostgreSQL connection fails | `postgres-test` startup logs and the test settings above. The prestart script retries database availability before migrating. |
| Backend lint stage fails | Resolve the reported mypy, Ruff lint, or formatting errors; dependency installation alone is not a passing test run. |
| Dependency installation fails | Package registry access and consistency between manifests and lockfiles. |
| BuildKit exits or readiness times out | Daemon output printed in the console, cluster restrictions, and available memory/disk space. |
| Jenkins shows an older pipeline | The job's selected branch and checked-out revision contain the intended Jenkinsfile. |
| Local Jenkins URL stops responding | The port-forward process is still running and the controller Pod is available. Restart forwarding after Pod replacement. |

## Current scope

The pipeline checks backend code, runs backend tests, compiles the frontend, and
checks both Dockerfile builds. It does not run Playwright browser tests, validate
Kubernetes manifests, scan images, promote releases, or deploy workloads.

BuildKit remains privileged, and the agent uses the `dev` namespace. Restrict
which jobs and repository contributors can execute this pipeline. The current
Dockerfiles also retain their existing dependency installation commands; CI
checks do not make those commands fully reproducible.

The Jenkinsfile has passed offline YAML and shell syntax checks, including
report failure handling. Backend mypy, Ruff lint, and formatting checks passed
on 38 source files. Migrations and all 55 backend tests passed locally against a
temporary PostgreSQL 16 database, using the cached backend image dependencies.
Coverage was 94% with test files included. A successful end-to-end Jenkins run,
including frontend compilation and both container builds, has not yet been confirmed.
