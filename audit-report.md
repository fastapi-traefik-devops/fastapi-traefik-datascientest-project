# Codex conversation

## User

Bitte analysiere mein gesamtes Repository wie ein Senior DevOps / Cloud Engineer und überprüfe, ob mein Projekt alle unten genannten Projektanforderungen erfüllt.

WICHTIG:
- Prüfe tatsächlich die vorhandenen Dateien im Repository.
- Gehe nicht davon aus, dass etwas implementiert ist, nur weil es in der README erwähnt wird.
- Vergleiche Dokumentation und tatsächliche Implementierung.
- Prüfe insbesondere Terraform, Kubernetes, Docker und CI/CD sehr gründlich.
- Ändere zunächst nichts.
- Erstelle zuerst einen vollständigen Audit-Bericht.
- Sage klar, was:
  1. vollständig erfüllt ist,
  2. nur teilweise erfüllt ist,
  3. fehlt,
  4. falsch oder unsicher implementiert ist.

## 1. Repository vollständig analysieren

Untersuche unter anderem:

- Terraform-Dateien (*.tf)
- Dockerfile / Dockerfiles
- docker-compose.yml / compose.yaml
- Kubernetes YAML-Dateien
- Helm Charts, falls vorhanden
- GitHub Actions unter `.github/workflows/`
- GitLab CI / Jenkins, falls vorhanden
- Application Source Code
- Unit Tests
- Integration/API/E2E Tests
- README.md
- Config-Dateien
- `.env.example`
- Monitoring-Konfiguration
- Prometheus
- Grafana
- Trivy / Snyk / Dependabot
- Kubernetes Secrets / Secret Management
- Backup- und Disaster-Recovery-Konfiguration
- Scripts
- Architecture-Dokumentation

Ignoriere generierte Verzeichnisse wie:

- `.terraform/`
- `node_modules/`
- `vendor/`
- Build-Artefakte

## 2. Docker prüfen

Überprüfe:

- Existiert ein funktionierendes Dockerfile?
- Ist der Build reproduzierbar?
- Wird ein Multi-Stage Build verwendet, wenn sinnvoll?
- Läuft die Anwendung als Non-Root User, wenn möglich?
- Gibt es unnötige Dateien im Image?
- Existiert `.dockerignore`?
- Sind Secrets im Image oder Dockerfile enthalten?
- Ist ein Container Registry Workflow vorhanden?
- Wird das Docker Image versioniert/tagged?
- Wird das Image durch CI/CD gebaut und gepusht?

Bewertung:
PASS / PARTIAL / FAIL

## 3. Dev und Prod prüfen

Überprüfe, ob mindestens zwei getrennte Umgebungen vorhanden sind:

- dev
- prod

Prüfe insbesondere:

- unterschiedliche Environment Variables
- unterschiedliche Terraform-Konfigurationen
- tfvars
- Kubernetes Namespaces
- ConfigMaps
- Secrets
- Helm values
- unterschiedliche Deployments
- automatische Dev-Deployments
- kontrollierte/approval-basierte Prod-Deployments

Prüfe außerdem, ob dokumentiert ist, welche Unterschiede zwischen Dev und Prod bestehen.

## 4. Tests prüfen

Suche nach tatsächlichen Tests.

Mindestens erforderlich:

- Unit Tests

Zusätzlich prüfen:

- Integration Tests
- API Tests
- End-to-End Tests

Überprüfe:

- ob die Tests tatsächlich ausführbar sind
- ob CI/CD die Tests ausführt
- ob ein fehlgeschlagener Test die Pipeline stoppt

## 5. Kubernetes prüfen

Überprüfe vorhandene Kubernetes-Ressourcen.

Mindestens erwartet:

- Deployment
- Service
- ConfigMap und/oder Secret

Zusätzlich:

- Ingress
- Namespace
- readinessProbe
- livenessProbe
- resource requests
- resource limits
- replicas
- rolling updates
- Pod Security
- ServiceAccount
- RBAC
- PersistentVolume / PersistentVolumeClaim, falls notwendig

Prüfe auch:

- korrekte Labels und Selectors
- Container Ports
- Service Ports
- Environment Variables
- Image Referenzen
- Secrets
- Production Readiness

Zeige konkrete Fehler mit Dateiname und möglichst Zeilennummer.

## 6. CI/CD prüfen

Prüfe die komplette Pipeline.

Sie sollte mindestens:

1. Source Code auschecken
2. Dependencies installieren
3. Tests ausführen
4. Docker Image bauen
5. Security Scan durchführen
6. Docker Image in Registry pushen
7. Dev deployen
8. Production Deployment ermöglichen

Prüfe zusätzlich:

- main/dev Branch Strategy
- Environment Protection
- Production Approval Gate
- GitHub/GitLab Secrets
- keine hard-coded Credentials
- Image Tagging
- Commit SHA Tags
- Rollback-Möglichkeit
- Terraform Validation
- terraform fmt
- terraform validate
- terraform plan

## 7. Terraform / Infrastructure as Code SEHR GRÜNDLICH prüfen

Analysiere alle Terraform-Dateien vollständig.

Prüfe zuerst die Struktur:

- providers.tf
- versions.tf
- variables.tf
- outputs.tf
- main.tf
- terraform.tfvars
- dev/prod tfvars
- modules/
- backend-Konfiguration

Bewerte dann jede Terraform Resource.

Prüfe insbesondere:

### Terraform Qualität

- `terraform fmt`
- `terraform validate`
- Provider Versions
- required_version
- Variables
- Variable Types
- Variable Validation
- Locals
- Outputs
- Module-Struktur
- Naming
- Tags / Labels
- unnötige Duplikation
- hard-coded Werte

### Terraform State

Prüfe:

- Remote Backend vorhanden?
- State lokal oder remote?
- State Locking?
- Verschlüsselung?
- Sind `.tfstate` Dateien versehentlich im Git Repository?
- Ist `.terraform/` korrekt ignoriert?
- Sind Secrets im Terraform State problematisch?

### Infrastruktur

Je nach verwendeter Cloud prüfe:

- Netzwerk / VPC
- Subnets
- Routing
- Internet/NAT Gateway
- Security Groups / Firewall
- Kubernetes Cluster
- Node Groups
- IAM
- Load Balancer
- DNS
- Storage
- Database
- Container Registry
- Monitoring
- Backup

### Security

Suche besonders nach:

- `0.0.0.0/0`
- öffentlich erreichbaren Datenbanken
- offenen SSH Ports
- Admin-Rechten
- `*` IAM Permissions
- hard-coded Passwords
- Tokens
- API Keys
- Access Keys
- Private Keys
- Secrets in tfvars
- Secrets in outputs

Kennzeichne kritische Findings deutlich.

### Terraform Dev/Prod

Prüfe, ob Dev und Prod sauber getrennt sind.

Bewerte unter anderem:

- State Isolation
- Variable Isolation
- unterschiedliche Konfiguration
- unterschiedliche Namespaces/Cluster/Resources
- versehentliche gemeinsame Ressourcen

### Terraform CI/CD

Prüfe, ob die Pipeline mindestens folgende Befehle berücksichtigt:

```bash
terraform fmt -check -recursive
terraform init
terraform validate
terraform plan
```

Prüfe außerdem, ob `terraform apply` kontrolliert ausgeführt wird und Production nicht versehentlich automatisch zerstört oder verändert werden kann.

Prüfe auf problematische Verwendung von:

```bash
terraform apply -auto-approve
terraform destroy -auto-approve
```

insbesondere in Production.

## 8. Monitoring prüfen

Prüfe, ob tatsächlich Monitoring vorhanden ist.

Erwartet wird z. B.:

- Prometheus
- Grafana

oder:

- Datadog

Überprüfe:

- Metrics
- Scraping
- Dashboards
- Kubernetes Monitoring
- Application Monitoring
- Alerts

Dokumentation alleine zählt nicht als Implementierung.

## 9. DevSecOps / Security prüfen

Mindestens 3 Sicherheitsmaßnahmen sollen vorhanden sein.

Prüfe beispielsweise:

- Trivy
- Snyk
- Dependabot
- Kubernetes Secrets
- Vault
- AWS SSM / Secrets Manager
- GitHub/GitLab Secrets
- HTTPS
- TLS
- cert-manager
- RBAC
- IAM
- Network Policies
- Container läuft als Non-Root
- Security Context

Prüfe außerdem das Repository nach versehentlich eingecheckten Secrets.

Gib niemals gefundene Secrets vollständig aus. Maskiere sie.

## 10. Disaster Recovery prüfen

Überprüfe:

- Datenbank Backup
- Persistent Storage Backup
- Terraform Recovery
- Kubernetes Recovery
- Container Failure Recovery
- Node Failure Recovery
- Rollback
- vorherige Docker Image Version
- Infrastructure Rebuild

Prüfe, ob die README konkret erklärt:

- Was passiert bei Container-Ausfall?
- Was passiert bei Node-Ausfall?
- Wie wird Infrastruktur über Terraform neu aufgebaut?
- Wie wird eine alte App-Version wiederhergestellt?
- Wie werden persistente Daten wiederhergestellt?

## 11. README und Dokumentation prüfen

Die README muss mindestens enthalten:

- Projektübersicht
- Architektur
- Tech Stack
- lokale Setup-Schritte
- Docker-Anleitung
- Dev Deployment
- Prod Deployment
- Terraform Deployment
- Kubernetes Deployment
- CI/CD Erklärung
- Monitoring Erklärung
- Security Erklärung
- Disaster Recovery
- Architecture Diagram

Prüfe, ob die Anleitung tatsächlich mit dem Code übereinstimmt.

## 12. Architecture Diagram prüfen

Überprüfe, ob ein Architekturdiagramm existiert.

Das Diagramm sollte mindestens zeigen:

- Entwickler / Git Repository
- CI/CD
- Tests
- Docker Build
- Container Registry
- Terraform
- Cloud Infrastruktur
- Kubernetes Cluster
- Ingress / Load Balancer
- Application Pods
- Service
- ConfigMap / Secrets
- Datenbank, falls vorhanden
- Prometheus
- Grafana
- Backup / Storage

## 13. Tatsächliche Validierung durchführen

Wenn die benötigten Tools verfügbar sind, führe möglichst read-only bzw. sichere Prüfungen aus.

Zum Beispiel:

```bash
terraform fmt -check -recursive
terraform validate
docker build .
kubectl apply --dry-run=client -f ...
```

Führe vorhandene Unit Tests aus.

Führe vorhandene Linter aus.

Führe Security Scanner aus, falls bereits im Projekt vorhanden.

WICHTIG:

Kein:

```bash
terraform apply
terraform destroy
kubectl delete
```

und keine anderen destruktiven Befehle ausführen.

## 14. Abschlussbericht erstellen

Erstelle am Ende eine Tabelle:

| Bereich | Status | Was vorhanden ist | Was fehlt | Priorität |
|---|---|---|---|---|
| Docker | PASS/PARTIAL/FAIL | ... | ... | ... |
| Dev/Prod | PASS/PARTIAL/FAIL | ... | ... | ... |
| Tests | PASS/PARTIAL/FAIL | ... | ... | ... |
| Kubernetes | PASS/PARTIAL/FAIL | ... | ... | ... |
| CI/CD | PASS/PARTIAL/FAIL | ... | ... | ... |
| Terraform | PASS/PARTIAL/FAIL | ... | ... | ... |
| Monitoring | PASS/PARTIAL/FAIL | ... | ... | ... |
| Security | PASS/PARTIAL/FAIL | ... | ... | ... |
| Disaster Recovery | PASS/PARTIAL/FAIL | ... | ... | ... |
| Documentation | PASS/PARTIAL/FAIL | ... | ... | ... |
| Architecture Diagram | PASS/PARTIAL/FAIL | ... | ... | ... |

Danach erstelle drei Kategorien:

### CRITICAL
Probleme, durch die das Projekt die Pflichtanforderungen wahrscheinlich nicht erfüllt.

### SHOULD FIX
Wichtige Verbesserungen vor der Abgabe.

### NICE TO HAVE
Bonus- und Production-Readiness-Verbesserungen.

Danach gib mir eine priorisierte TODO-Liste in der Reihenfolge, in der ich die Probleme beheben sollte.

Für jedes Problem nenne:

- Datei
- relevante Stelle
- Problem
- warum es problematisch ist
- konkrete Lösung

Am Schluss gib mir eine Gesamtbewertung:

**Project readiness: X / 100**

und schätze ein:

- Welche Pflichtanforderungen sind erfüllt?
- Welche Pflichtanforderungen fehlen noch?
- Was sollte ich unbedingt vor der Abgabe korrigieren?

WICHTIG:
Ändere im ersten Schritt keine Dateien. Führe nur den Audit durch und warte danach auf meine Anweisung, bevor du Änderungen am Repository vornimmst.

## Assistant

Ich prüfe die tatsächlichen Dateien und gleiche sie mit der Dokumentation ab. Anschließend führe ich verfügbare, sichere Validierungen aus und erstelle den Audit-Bericht mit konkreten Fundstellen. Ich ändere keine Projektdateien und führe keine Deployments oder destruktiven Befehle aus.

## Activity

    $ pwd; rg --files --hidden -g '! .git' -g '!.git/**' -g '!node_modules/**' -g '!.terraform/**' -g '!vendor/**' -g '!dist/**' -g '!build/**' -g '!**/.venv/**' -g '!**/node_modules/**' -g '!**/.terraform/**' -g 'AGENTS.md' -g '*.tf' -g '*.tfvars*' -g '*Dockerfile*' -g '*compose*' -g '*.yaml' -g '*.yml' -g '*.md' -g '*test*' -g '*requirements*' -g 'pyproject.toml' -g 'package.json' -g '.dockerignore' -g '.gitignore' -g '*Jenkins*' -g '*.sh' -g '*.py' -g '.env*'
    bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
    ✗ (1) • 33ms

## Activity

    $ pwd; git status --short; for p in /AGENTS.md /home/AGENTS.md /home/root-admin/AGENTS.md; do if [ -f "$p" ]; then cat "$p"; fi; done; rg --files --hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/.terraform/**' -g '!vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.venv/**'
    /home/root-admin/fastapi-traefik-datascientest-project
     M .gitignore
     M DEV_SETUP_REPORT.md
    ?? ALERTING_RUNBOOK.md
    ?? GRAFANA_DASHBOARDS.md
    ?? JENKINS_RECOVERY_REPORT.md
    ?? KIND_MIGRATION_REPORT.md
    ?? MIGRATION_BACKUP_CHECKLIST.md
    ?? MONITORING_SETUP_REPORT.md
    ?? PROMETHEUS_QUERIES.md
    ?? argocd/app-monitoring.yaml
    ?? argocd/app-stage.yaml
    ?? argocd/bootstrap/monitoring-namespace.yaml
    ?? argocd/project-monitoring.yaml
    ?? infra/
    ?? monitoring/
    ?? scripts/bootstrap-jenkins-host.py
    ?? scripts/bootstrap-kind.sh
    ?? scripts/capture-kind-capacity.py
    ?? scripts/check-kind-capacity.py
    ?? scripts/create-stage-secrets.py
    ?? scripts/recover-dev-secrets.py
    ?? scripts/restore-kind-registry-auth.py
    ?? scripts/sync-jenkins-host-jobs.py
    ?? scripts/verify-jenkins-host.py
    ?? scripts/verify-kind-app.py
    ?? scripts/verify-kind-monitoring.py
    ?? scripts/watch-kind-monitoring.py
    MONITORING_SETUP_REPORT.md
    docker-compose.yml
    PROMETHEUS_QUERIES.md
    JENKINS-TROUBLESHOOTING.md
    scripts/generate-client.sh
    scripts/deploy.sh
    scripts/verify-kind-monitoring.py
    scripts/build-push.sh
    scripts/test.sh
    scripts/watch-kind-monitoring.py
    scripts/restore-kind-registry-auth.py
    scripts/bootstrap-kind.sh
    scripts/test-local.sh
    scripts/check-kind-capacity.py
    scripts/verify-jenkins-host.py
    scripts/recover-dev-secrets.py
    scripts/sync-jenkins-host-jobs.py
    scripts/create-stage-secrets.py
    scripts/verify-kind-app.py
    scripts/capture-kind-capacity.py
    scripts/build.sh
    scripts/bootstrap-jenkins-host.py
    GRAFANA_DASHBOARDS.md
    development.md
    KIND_MIGRATION_REPORT.md
    ALERTING_RUNBOOK.md
    get_helm.sh
    Jenkinsfile.promote
    img/dashboard-items.png
    img/dashboard-user-settings.png
    img/dashboard-create.png
    img/github-social-preview.svg
    img/dashboard.png
    img/login.png
    img/github-social-preview.png
    img/dashboard-dark.png
    img/docs.png
    .env
    .pre-commit-config.yaml
    docker-compose.override.yml
    hooks/post_gen_project.py
    argocd/bootstrap/dev-namespace.yaml
    argocd/bootstrap/monitoring-namespace.yaml
    argocd/project.yaml
    argocd/project-monitoring.yaml
    argocd/app-monitoring.yaml
    argocd/app-stage.yaml
    argocd/applicationset.yaml
    argocd/app-dev.yaml
    DEV_SETUP_REPORT.md
    .github/dependabot.yml
    .github/workflows/generate-client.yml
    .github/workflows/test-backend.yml
    .github/workflows/add-to-project.yml
    .github/workflows/deploy-staging.yml.disabled
    .github/workflows/latest-changes.yml
    .github/workflows/lint-backend.yml
    .github/workflows/playwright.yml
    .github/workflows/test-docker-compose.yml
    .github/workflows/deploy-production.yml.disabled
    .github/workflows/issue-manager.yml
    .github/workflows/smokeshow.yml
    .github/workflows/labeler.yml
    .github/DISCUSSION_TEMPLATE/questions.yml
    .github/FUNDING.yml
    .github/ISSUE_TEMPLATE/config.yml
    .github/ISSUE_TEMPLATE/privileged.yml
    .github/labeler.yml
    deploy/base/deployment-db.yaml
    deploy/base/service-db.yaml
    deploy/base/ingress-app.yaml
    deploy/base/deployment-frontend.yaml
    deploy/base/configmap-db.yaml
    deploy/base/deployment-backend.yaml
    deploy/base/deployment-adminer.yaml
    deploy/base/service-frontend.yaml
    deploy/base/job-prestart.yaml
    deploy/base/service-adminer.yaml
    deploy/base/kustomization.yaml
    deploy/base/configmap-backend.yaml
    deploy/base/pvc-db.yaml
    deploy/base/service-backend.yaml
    deploy/overlays/dev/promotion.json
    deploy/overlays/dev/kustomization.yaml
    frontend/package.json
    frontend/tsconfig.node.json
    frontend/.nvmrc
    frontend/openapi-ts.config.ts
    frontend/.dockerignore
    deploy/overlays/stage/promotion.json
    deploy/overlays/stage/kustomization.yaml
    frontend/src/routes/reset-password.tsx
    frontend/src/routes/recover-password.tsx
    frontend/src/routes/__root.tsx
    frontend/src/routes/login.tsx
    frontend/src/routes/signup.tsx
    deploy/overlays/prod/kustomization.yaml
    SECURITY.md
    copier.yml
    .gitignore
    frontend/src/routes/_layout/settings.tsx
    frontend/src/routes/_layout/items.tsx
    frontend/src/routes/_layout/index.tsx
    frontend/src/routes/_layout/admin.tsx
    frontend/src/routes/_layout.tsx
    frontend/src/theme.tsx
    frontend/src/main.tsx
    k8s/base/deployment-db.yaml
    k8s/base/service-db.yaml
    k8s/base/secret-frontend.yaml
    k8s/base/secret-db.yaml
    k8s/base/ingress-app.yaml
    k8s/base/deployment-frontend.yaml
    k8s/base/secret-backend.yaml
    k8s/base/configmap-db.yaml
    k8s/base/deployment-backend.yaml
    k8s/base/deployment-adminer.yaml
    k8s/base/service-frontend.yaml
    k8s/base/job-prestart.yaml
    k8s/base/service-adminer.yaml
    k8s/base/kustomization.yaml
    k8s/base/configmap-backend.yaml
    k8s/base/pvc-db.yaml
    k8s/base/service-backend.yaml
    k8s/base/configmap-frontend.yaml
    k8s/overlays/dev/sealed-secret-backend.yaml
    k8s/overlays/dev/sealed-secret-db.yaml
    k8s/overlays/dev/sealed-secret-frontend.yaml
    k8s/overlays/dev/kustomization.yaml
    k8s/overlays/prod/kustomization.yaml
    frontend/src/theme/button.recipe.ts
    frontend/src/utils.ts
    frontend/src/vite-env.d.ts
    frontend/src/client/types.gen.ts
    frontend/src/client/index.ts
    frontend/src/client/sdk.gen.ts
    frontend/src/client/schemas.gen.ts
    frontend/src/client/core/OpenAPI.ts
    frontend/src/client/core/CancelablePromise.ts
    frontend/src/client/core/ApiRequestOptions.ts
    frontend/src/client/core/ApiResult.ts
    frontend/src/client/core/request.ts
    frontend/src/client/core/ApiError.ts
    ci/publish.sh
    ci/jenkins-controller-rbac.yaml
    ci/validate.sh
    ci/test_promote.py
    ci/tools.sh
    ci/README.md
    ci/test_publish.py
    ci/VERIFICATION.md
    ci/promote.py
    .gitattributes
    frontend/biome.json
    frontend/package-lock.json
    frontend/src/components/Pending/PendingItems.tsx
    frontend/.gitignore
    frontend/index.html
    frontend/nginx.conf
    frontend/playwright.config.ts
    frontend/tsconfig.build.json
    frontend/tsconfig.json
    frontend/src/components/Pending/PendingUsers.tsx
    frontend/src/components/ui/field.tsx
    frontend/src/components/ui/button.tsx
    frontend/src/components/ui/toaster.tsx
    frontend/src/components/ui/radio.tsx
    frontend/src/components/ui/provider.tsx
    frontend/src/components/ui/color-mode.tsx
    frontend/src/components/ui/drawer.tsx
    frontend/src/components/ui/link-button.tsx
    frontend/src/components/ui/menu.tsx
    frontend/src/components/ui/input-group.tsx
    frontend/src/components/ui/checkbox.tsx
    frontend/src/components/ui/close-button.tsx
    frontend/src/components/ui/skeleton.tsx
    frontend/src/components/ui/dialog.tsx
    frontend/src/components/ui/pagination.tsx
    frontend/src/components/ui/password-input.tsx
    frontend/tests/reset-password.spec.ts
    frontend/tests/sign-up.spec.ts
    frontend/tests/user-settings.spec.ts
    frontend/tests/config.ts
    frontend/tests/login.spec.ts
    frontend/tests/utils/privateApi.ts
    frontend/tests/utils/mailcatcher.ts
    frontend/tests/utils/user.ts
    frontend/tests/utils/random.ts
    frontend/tests/auth.setup.ts
    MIGRATION_BACKUP_CHECKLIST.md
    docker-compose.traefik.yml
    JENKINS-INVESTIGATION-REPORT.md
    README-jenkins.md
    README.md
    frontend/src/routeTree.gen.ts
    frontend/src/components/Common/UserActionsMenu.tsx
    frontend/src/components/Common/ItemActionsMenu.tsx
    frontend/src/components/Common/Navbar.tsx
    frontend/src/components/Common/Sidebar.tsx
    frontend/src/components/Common/SidebarItems.tsx
    frontend/src/components/Common/UserMenu.tsx
    frontend/src/components/Common/NotFound.tsx
    frontend/src/components/UserSettings/ChangePassword.tsx
    frontend/src/components/UserSettings/UserInformation.tsx
    frontend/src/components/UserSettings/DeleteConfirmation.tsx
    frontend/src/components/UserSettings/DeleteAccount.tsx
    frontend/src/components/UserSettings/Appearance.tsx
    frontend/src/components/Admin/EditUser.tsx
    frontend/src/components/Admin/DeleteUser.tsx
    frontend/src/components/Admin/AddUser.tsx
    frontend/src/components/Items/AddItem.tsx
    frontend/src/components/Items/DeleteItem.tsx
    frontend/src/components/Items/EditItem.tsx
    frontend/src/hooks/useAuth.ts
    frontend/src/hooks/useCustomToast.ts
    frontend/.env
    frontend/Dockerfile.playwright
    frontend/vite.config.ts
    backend/scripts/lint.sh
    backend/scripts/prestart.sh
    backend/scripts/test.sh
    backend/scripts/tests-start.sh
    backend/scripts/format.sh
    backend/.dockerignore
    backend/Dockerfile
    frontend/public/assets/images/favicon.png
    frontend/public/assets/images/fastapi-logo.svg
    frontend/Dockerfile
    frontend/README.md
    frontend/nginx-backend-not-found.conf
    backend/alembic.ini
    backend/app/utils.py
    backend/app/crud.py
    backend/app/backend_pre_start.py
    backend/app/initial_data.py
    backend/app/main.py
    k8s/rbac/jenkins-dev-rbac.yaml
    k8s/rbac/jenkins-controller-dev-rbac.yaml
    backend/app/api/deps.py
    backend/app/api/routes/utils.py
    backend/app/api/routes/items.py
    backend/app/api/routes/__init__.py
    backend/app/api/routes/users.py
    backend/app/api/routes/login.py
    backend/app/api/routes/private.py
    backend/app/api/main.py
    backend/app/api/__init__.py
    backend/app/models.py
    backend/app/tests/crud/__init__.py
    backend/app/tests/crud/test_user.py
    backend/app/tests/scripts/test_test_pre_start.py
    backend/app/tests/scripts/test_backend_pre_start.py
    backend/app/tests/scripts/__init__.py
    backend/app/tests/conftest.py
    backend/app/tests/__init__.py
    backend/app/tests/api/routes/test_users.py
    backend/app/tests/api/routes/test_items.py
    backend/app/tests/api/routes/__init__.py
    backend/app/tests/api/routes/test_private.py
    backend/app/tests/api/routes/test_login.py
    backend/app/tests/api/__init__.py
    .copier/.copier-answers.yml.jinja
    .copier/update_dotenv.py
    deployment.md
    LICENSE
    backend/app/tests/utils/utils.py
    backend/app/tests/utils/user.py
    backend/app/tests/utils/__init__.py
    backend/app/tests/utils/item.py
    backend/app/core/security.py
    backend/app/core/db.py
    backend/app/core/config.py
    backend/app/core/__init__.py
    monitoring/verify-grafana-auth.py
    backend/app/email-templates/src/reset_password.mjml
    backend/app/email-templates/src/new_account.mjml
    backend/app/email-templates/src/test_email.mjml
    backend/pyproject.toml
    backend/README.md
    backend/app/alembic/versions/1a31ce608336_add_cascade_delete_relationships.py
    backend/app/alembic/versions/d98dd8ec85a3_edit_replace_id_integers_in_all_models_.py
    backend/app/alembic/versions/9c0a54914c78_add_max_length_for_string_varchar_.py
    backend/app/alembic/versions/e2412789c190_initialize_models.py
    backend/app/alembic/versions/.keep
    backend/app/alembic/README
    backend/app/alembic/env.py
    backend/app/alembic/script.py.mako
    backend/app/__init__.py
    backend/app/tests_pre_start.py
    infra/jenkins-host/jobs.groovy
    infra/jenkins-host/buildkit.toml
    infra/jenkins-host/Jenkinsfile.host
    infra/jenkins-host/README.md
    infra/jenkins-host/run-tool.sh
    infra/jenkins-host/plugins.txt
    infra/jenkins-host/Jenkinsfile.smoke
    infra/jenkins-host/jenkins.yaml
    infra/jenkins-host/images.lock.json
    infra/jenkins-host/plugins.lock.txt
    Jenkinsfile
    release-notes.md
    JENKINS_RECOVERY_REPORT.md
    infra/kind/app-stage-local.yaml
    infra/kind/project-fastapi.yaml
    infra/kind/kind-config.yaml
    infra/kind/traefik-values.yaml
    monitoring/values.yaml
    backend/.gitignore
    backend/uv.lock
    monitoring/monitors/argocd.yaml
    monitoring/monitors/traefik.yaml
    monitoring/kustomization.yaml
    monitoring/ensure-grafana-secret.py
    monitoring/test-alert-rules.py
    monitoring/bootstrap.py
    monitoring/rules/dev-stage.yaml
    infra/kind/secrets/app-stage/backend-secrets.yaml
    infra/kind/secrets/app-stage/db-secrets.yaml
    monitoring/dashboards/platform.yaml
    infra/kind/secrets/app-dev/backend-secrets.yaml
    infra/kind/secrets/app-dev/db-secrets.yaml
    ✓ • 351ms

## Activity

    $ rg --files --hidden -g AGENTS.md -g '*.tf' -g '*.tfvars*' -g '*.tfstate*' -g '!.git/**' -g '!**/node_modules/**' -g '!**/.terraform/**'; git ls-files '*.tf' '*.tfstate*' '*secret*' '.env*' 'infra/*' 'monitoring/*'; cat Jenkinsfile Jenkinsfile.promote ci/validate.sh ci/publish.sh ci/tools.sh; cat backend/Dockerfile frontend/Dockerfile frontend/Dockerfile.playwright backend/.dockerignore frontend/.dockerignore .gitignore
    .env
    k8s/base/secret-backend.yaml
    k8s/base/secret-db.yaml
    k8s/base/secret-frontend.yaml
    k8s/overlays/dev/sealed-secret-backend.yaml
    k8s/overlays/dev/sealed-secret-db.yaml
    k8s/overlays/dev/sealed-secret-frontend.yaml
    pipeline {
        agent {
            kubernetes {
                namespace 'jenkins-ci'
                yaml '''
    apiVersion: v1
    kind: Pod
    metadata:
      labels:
        component: jenkins-agent
    spec:
      automountServiceAccountToken: false
      containers:
      - name: python-tester
        image: ghcr.io/astral-sh/uv:0.5.11-python3.10-bookworm-slim
        command:
          - /bin/sh
          - -c
          - sleep infinity
        tty: true
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: "1"
            memory: 1Gi

      - name: node-tester
        image: node:20.18.1
        command:
          - /bin/sh
          - -c
          - sleep infinity
        tty: true
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: "1"
            memory: 1Gi

      - name: buildkit
        image: moby/buildkit:v0.24.0
        command:
          - /bin/sh
          - -c
          - sleep infinity
        tty: true
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: "2"
            memory: 2Gi
        securityContext:
          privileged: true

      # Disposable database: loopback-only, no Service or persistent volume.
      - name: postgres-test
        image: postgres:16.6
        args: ["-c", "listen_addresses=127.0.0.1"]
        env:
        - name: POSTGRES_DB
          value: app_ci
        # Disposable CI password, never used for an application database.
        - name: POSTGRES_PASSWORD
          value: ci-only-postgres-password
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: "1"
            memory: 1Gi
    '''
            }
        }

        options {
            skipDefaultCheckout(true)
            timeout(time: 45, unit: 'MINUTES')
            disableConcurrentBuilds()
            buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        }

        environment {
            REGISTRY_NAMESPACE = 'ghcr.io/fastapi-traefik-devops'
            CI = 'true'
            // Test-only settings. PostgreSQL is isolated inside this agent Pod.
            ENVIRONMENT = 'local'
            PROJECT_NAME = 'FastAPI CI'
            POSTGRES_SERVER = '127.0.0.1'
            POSTGRES_PORT = '5432'
            POSTGRES_DB = 'app_ci'
            POSTGRES_USER = 'postgres'
            POSTGRES_PASSWORD = 'ci-only-postgres-password'
            FIRST_SUPERUSER = 'ci-admin@example.com'
            EMAIL_TEST_USER = 'test@example.com'
            EMAILS_FROM_EMAIL = 'ci@example.com'
            EMAILS_FROM_NAME = 'ci@example.com'
            SMTP_HOST = '127.0.0.1'
            SMTP_PORT = '1025'
            SMTP_TLS = 'false'
            SMTP_SSL = 'false'
            BACKEND_CORS_ORIGINS = 'http://localhost:5173'
            FRONTEND_HOST = 'http://localhost:5173'
            VITE_API_URL = ''
        }

        stages {

            stage('Checkout') {
                steps {
                    script {
                        def revision = checkout scm
                        env.IMAGE_SHA = revision.GIT_COMMIT
                        if (!(env.IMAGE_SHA ==~ /[0-9a-f]{40}/)) { error('Expected full Git SHA') }
                        if (!env.BRANCH_NAME) { error('Configure a GitHub multibranch job') }
                        env.SKIP_BUILD = env.TAG_NAME ? 'true' : 'false'
                        // GitOps-only changes validate, but never create application artifacts.
                        def changes = sh(returnStdout: true, script: 'git diff-tree --root --first-parent -m --no-commit-id --name-only -r HEAD').trim().readLines()
                        if (changes && changes.every { it.startsWith('deploy/') || it.startsWith('argocd/') || it.endsWith('.md') }) {
                            env.SKIP_BUILD = 'true'
                        }
                        writeFile file: 'source-sha.txt', text: env.IMAGE_SHA + '\n'

                    }
                }
            }

            stage('Backend Checks and Tests') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    container('python-tester') {
                        sh '''
                            set -eu
                            # Jenkins sh normally enables tracing; keep ephemeral keys out of logs.
                            set +x
                            cd backend
                            uv sync --frozen
                            SECRET_KEY="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(32))')"
                            FIRST_SUPERUSER_PASSWORD="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(24))')"
                            export SECRET_KEY FIRST_SUPERUSER_PASSWORD
                            uv run --frozen bash scripts/lint.sh
                            uv run --frozen bash scripts/prestart.sh
                            test_status=0
                            uv run --frozen coverage run --source=app -m pytest --junitxml=test-results.xml || test_status=$?
                            # Preserve reports on test failure without hiding pytest's exit status.
                            report_status=0
                            uv run --frozen coverage report --show-missing || report_status=$?
                            uv run --frozen coverage xml -o coverage.xml || report_status=$?
                            if [ "$test_status" -ne 0 ]; then
                                exit "$test_status"
                            fi
                            exit "$report_status"
                        '''
                    }
                }
                post {
                    always {
                        junit testResults: 'backend/test-results.xml', allowEmptyResults: true
                        archiveArtifacts artifacts: 'backend/coverage.xml', allowEmptyArchive: true
                    }
                }
            }

            stage('Frontend Check') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    container('node-tester') {
                        sh '''
                            set -eu
                            echo "--- Verifying Frontend Dependencies ---"
                            cd frontend
                            npm ci
                            npm run build
                        '''
                    }
                }
            }

            stage('Validate all overlays') {
                steps {
                    container('node-tester') {
                        sh 'sh ci/tools.sh && PATH=/tmp/ci-bin:$PATH sh ci/validate.sh && PATH=/tmp/ci-bin:$PATH python3 -m unittest discover -s ci -p "test_*.py"'
                    }
                }
            }

            stage('Build image archives') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    container('buildkit') {
                        sh '''
                            set -eu
                            buildkitd --addr unix:///tmp/buildkitd.sock > /tmp/buildkitd.log 2>&1 &
                            BUILDKIT_PID=$!
                            trap 'kill "${BUILDKIT_PID}" 2>/dev/null || true; wait "${BUILDKIT_PID}" 2>/dev/null || true' EXIT

                            ready=false
                            for i in $(seq 1 60); do
                                if buildctl --addr unix:///tmp/buildkitd.sock debug workers > /dev/null 2>&1; then
                                    ready=true
                                    break
                                fi
                                if ! kill -0 "${BUILDKIT_PID}" 2>/dev/null; then
                                    cat /tmp/buildkitd.log
                                    exit 1
                                fi
                                sleep 1
                            done
                            if [ "$ready" != true ]; then
                                cat /tmp/buildkitd.log
                                echo "BuildKit did not become ready within 60 seconds"
                                exit 1
                            fi

                            # Verify both image builds before any registry writes.
                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/backend" \
                              --local dockerfile="${WORKSPACE}/backend" \
                              --output type=docker,dest=${WORKSPACE}/backend-ci.tar \
                              --progress=plain

                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/frontend" \
                              --local dockerfile="${WORKSPACE}/frontend" \
                              --opt "build-arg:VITE_API_URL=${VITE_API_URL:-}" \
                              --output type=docker,dest=${WORKSPACE}/frontend-ci.tar \
                              --progress=plain

                        '''
                    }
                }
            }
            stage('Archive checked images') {
                when { expression { env.SKIP_BUILD != 'true' && !env.CHANGE_ID } }
                steps {
                    archiveArtifacts artifacts: '*-ci.tar,source-sha.txt', fingerprint: true
                }
            }

        }

        post {
            success {
                script {
                    if (env.SKIP_BUILD != 'true' && !env.CHANGE_ID && env.BRANCH_NAME == 'main') {
                        build job: '/trusted/publish', wait: false, quietPeriod: 10,
                            parameters: [string(name: 'MODE', value: 'publish'),
                                         string(name: 'CI_JOB', value: env.JOB_NAME),
                                         string(name: 'CI_BUILD', value: env.BUILD_NUMBER)]
                    } else if (env.TAG_NAME) {
                        build job: '/trusted/publish', wait: false, quietPeriod: 10,
                            parameters: [string(name: 'MODE', value: 'release'),
                                         string(name: 'RELEASE_TAG', value: env.TAG_NAME)]
                    }
                }
            }
            always {
                // Tool containers create root-owned files; clean them in the same
                // container before the inbound agent removes the workspace.
                container('python-tester') {
                    sh '''
                        set -eu
                        test -n "${WORKSPACE}"
                        test "${WORKSPACE}" != /
                        cd "${WORKSPACE}"
                        find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
                    '''
                }
                deleteDir()
            }
        }
    }
    // TRUSTED standalone Pipeline: load this file ONLY from protected main.
    // Never configure this job as a branch/PR-controlled Pipeline.
    pipeline {
        agent {
            kubernetes {
                cloud 'trusted-kubernetes'
                namespace 'jenkins-publish'
                yaml '''
    apiVersion: v1
    kind: Pod
    spec:
      automountServiceAccountToken: false
      containers:
      - name: publisher
        image: python:3.10.16-bookworm
        command: [sh, -c, sleep infinity]
        resources:
          requests: {cpu: 250m, memory: 256Mi}
          limits: {cpu: '1', memory: 1Gi}
    '''
            }
        }
        options {
            skipDefaultCheckout(true)
            disableConcurrentBuilds()
            timeout(time: 60, unit: 'MINUTES')
            buildDiscarder(logRotator(numToKeepStr: '100'))
        }
        parameters {
            choice(name: 'MODE', choices: ['publish', 'dev', 'release'], description: 'publish: archive to GHCR and main to stage; dev: approved selected CI build; release: existing stage artifact only')
            string(name: 'CI_JOB', defaultValue: 'app-ci/main', description: 'Exact branch job under app-ci; PR jobs are rejected')
            string(name: 'CI_BUILD', defaultValue: '', description: 'Exact successful CI build number (unused for release)')
            string(name: 'RELEASE_TAG', defaultValue: '', description: 'Existing vX.Y.Z tag, for release mode only')
        }
        environment {
            PATH = "/tmp/ci-bin:${env.PATH}"
            REGISTRY_NAMESPACE = 'ghcr.io/fastapi-traefik-devops'
            JENKINS_API_URL = 'http://jenkins.jenkins.svc.cluster.local:8080/'
        }
        stages {
            stage('Trusted implementation') {
                steps {
                    checkout scm
                    container('publisher') { sh 'sh ci/tools.sh' }
                    script {
                        if (!(params.MODE in ['publish', 'dev', 'release'])) {
                            error('Invalid mode')
                        }

                        if (params.MODE == 'release') {
                            if (!(params.RELEASE_TAG ==~ /v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)/)) {
                                error('Expected vX.Y.Z')
                            }
                        } else {
                            if (!(params.CI_BUILD ==~ /[1-9][0-9]*/)) {
                                error('Exact CI build number required')
                            }

                            if (params.MODE == 'publish' && params.CI_JOB != 'app-ci/main') {
                                error('Automatic publish is allowed only from app-ci/main')
                            }

                            if (params.MODE == 'dev' &&
                                (!(params.CI_JOB ==~ /app-ci\/[A-Za-z0-9_.%\-]+/) ||
                                params.CI_JOB.startsWith('app-ci/PR-'))) {
                                error('Dev promotion requires a repository branch job under app-ci; PR jobs are rejected')
                            }
                        }
                    }
                }
            }
            stage('Verify successful CI and copy artifacts') {
                when { expression { params.MODE != 'release' } }
                steps {
                    script {
                        def jobPath = params.CI_JOB.split('/').collect { 'job/' + java.net.URLEncoder.encode(it, 'UTF-8') }.join('/')
                        def data
                        timeout(time: 10, unit: 'MINUTES') {
                            waitUntil(initialRecurrencePeriod: 5000) {
                                def response = httpRequest authentication: 'ci-read', quiet: true,
                                    url: "${env.JENKINS_API_URL}${jobPath}/${params.CI_BUILD}/api/json?tree=result,building,actions[lastBuiltRevision[SHA1],remoteUrls]"
                                data = readJSON text: response.content, returnPojo: true
                                return !data.building
                            }
                        }
                        if (data.result != 'SUCCESS') { error('Source CI build must be SUCCESS') }
                        def revisions = data.actions.findAll { it.lastBuiltRevision }.collect { it.lastBuiltRevision.SHA1 }.unique()
                        if (revisions.size() != 1 || !(revisions[0] ==~ /[0-9a-f]{40}/)) { error('Ambiguous or missing Git plugin revision') }
                        env.IMAGE_SHA = revisions[0]
                        copyArtifacts projectName: params.CI_JOB, selector: specific(params.CI_BUILD),
                            filter: '*-ci.tar,source-sha.txt', target: 'artifacts', fingerprintArtifacts: true
                        if (readFile('artifacts/source-sha.txt').trim() != env.IMAGE_SHA) { error('Artifact SHA disagrees with Jenkins SCM revision') }
                    }
                }
            }
            stage('Explicit promotion approval') {
                when { expression { params.MODE in ['dev', 'release'] } }
                steps {
                    input message: "Approve ${params.MODE}: ${params.MODE == 'release' ? params.RELEASE_TAG : env.IMAGE_SHA}. For a release, confirm this tag's digest pair ran successfully in stage (Argo health and smoke tests). Production still requires a reviewed Git PR.", submitter: 'admin'
                }
            }
            stage('Publish or promote under global lock') {
                steps {
                    lock(resource: 'fastapi-ghcr-gitops') {
                        container('publisher') {
                            withCredentials([
                                usernamePassword(credentialsId: 'ghcr-write', usernameVariable: 'GHCR_USER', passwordVariable: 'GHCR_TOKEN'),
                                usernamePassword(credentialsId: 'gitops-app', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')
                            ]) {
                                withEnv(["PROMOTION_MODE=${params.MODE}", "SOURCE_JOB=${params.CI_JOB}", "RELEASE_TAG=${params.RELEASE_TAG}"]) {
                                    sh 'sh ci/publish.sh'
                                }
                            }
                        }
                    }
                }
            }
        }
        post {
            always {
                container('publisher') { sh 'find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +' }
                deleteDir()
            }
        }
    }
    #!/bin/sh
    set -eu
    mkdir -p rendered /tmp/kubeconform-cache
    for environment in dev stage prod; do
      kustomize build "deploy/overlays/$environment" > "rendered/$environment.yaml"
      kubeconform -cache /tmp/kubeconform-cache -strict -summary -kubernetes-version 1.31.0 "rendered/$environment.yaml"
    done
    #!/bin/sh
    # Executes only in the trusted publisher, never in an application build Pod.
    set -eu
    set +x
    credential_dir=$(mktemp -d)
    trap 'rm -rf "$credential_dir"' EXIT HUP INT TERM
    export DOCKER_CONFIG="$credential_dir/docker"
    mkdir -p "$DOCKER_CONFIG"
    printf '%s' "$GHCR_TOKEN" | crane auth login ghcr.io -u "$GHCR_USER" --password-stdin
    cat > "$credential_dir/askpass" <<'ASKPASS'
    #!/bin/sh
    case "$1" in
      *Username*) printf '%s\n' "$GIT_USER" ;;
      *Password*) printf '%s\n' "$GIT_TOKEN" ;;
    esac
    ASKPASS
    chmod 700 "$credential_dir/askpass"
    export GIT_ASKPASS="$credential_dir/askpass" GIT_TERMINAL_PROMPT=0
    repo=https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
    if [ "$PROMOTION_MODE" = release ]; then
      # Resolve annotated/lightweight tag in a separate data-only clone.
      git clone --quiet --no-checkout "$repo" "$credential_dir/source"
      IMAGE_SHA=$(git -C "$credential_dir/source" rev-parse "refs/tags/$RELEASE_TAG^{commit}")
      git -C "$credential_dir/source" merge-base --is-ancestor "$IMAGE_SHA" origin/main
      export IMAGE_SHA
      # promote.py fails closed for missing images, checks stage evidence, never builds.
      python3 ci/promote.py prod "$IMAGE_SHA" --release "$RELEASE_TAG"
      exit
    fi
    # Existing SHA tags are NEVER overwritten. Partial publication is retryable.
    # Re-running CI may produce different bytes; retain the original successful image.
    for component in backend frontend; do
      image="$REGISTRY_NAMESPACE/fastapi-$component:sha-$IMAGE_SHA"
      if crane digest "$image" > "$credential_dir/digest" 2> "$credential_dir/error"; then
        echo "Retaining existing immutable $component image for $IMAGE_SHA"
      elif grep -Eq 'MANIFEST_UNKNOWN|NAME_UNKNOWN' "$credential_dir/error"; then
        crane push "artifacts/$component-ci.tar" "$image"
      else
        echo 'Registry lookup failed; refusing to treat it as a missing image' >&2
        exit 1
      fi
    done
    if [ "$PROMOTION_MODE" = dev ]; then
      python3 ci/promote.py dev "$IMAGE_SHA"
    elif [ "$SOURCE_JOB" = app-ci/main ]; then
      python3 ci/promote.py stage "$IMAGE_SHA"
    fi
    #!/bin/sh
    # Used only on disposable amd64 Linux agents. Versions are deliberately explicit.
    set -eu
    mkdir -p /tmp/ci-bin
    fetch() {
      url=$1; file=$2
      curl --fail --silent --show-error --location --retry 3 "$url" -o "$file"
    }
    fetch https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v5.6.0/kustomize_v5.6.0_linux_amd64.tar.gz /tmp/kustomize.tar.gz
    echo "54e4031ddc4e7fc59e408da29e7c646e8e57b8088c51b84b3df0864f47b5148f  /tmp/kustomize.tar.gz" | sha256sum -c -
    tar xzf /tmp/kustomize.tar.gz -C /tmp/ci-bin kustomize
    fetch https://github.com/yannh/kubeconform/releases/download/v0.6.7/kubeconform-linux-amd64.tar.gz /tmp/kubeconform.tar.gz
    echo "95f14e87aa28c09d5941f11bd024c1d02fdc0303ccaa23f61cef67bc92619d73  /tmp/kubeconform.tar.gz" | sha256sum -c -
    tar xzf /tmp/kubeconform.tar.gz -C /tmp/ci-bin kubeconform
    fetch https://github.com/google/go-containerregistry/releases/download/v0.20.3/go-containerregistry_Linux_x86_64.tar.gz /tmp/crane.tar.gz
    echo "36c67a932f489b3f2724b64af90b599a8ef2aa7b004872597373c0ad694dc059  /tmp/crane.tar.gz" | sha256sum -c -
    tar xzf /tmp/crane.tar.gz -C /tmp/ci-bin crane
    FROM python:3.10.16-bookworm

    ENV PYTHONUNBUFFERED=1

    WORKDIR /app/

    # Install uv
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
    COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

    # Place executables in the environment at the front of the path
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
    ENV PATH="/app/.venv/bin:$PATH"

    # Compile bytecode
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
    ENV UV_COMPILE_BYTECODE=1

    # uv Cache
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
    ENV UV_LINK_MODE=copy

    # Install dependencies
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
    RUN --mount=type=cache,target=/root/.cache/uv \
        --mount=type=bind,source=uv.lock,target=uv.lock \
        --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
        uv sync --frozen --no-install-project

    ENV PYTHONPATH=/app

    COPY ./scripts /app/scripts

    COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

    COPY ./app /app/app

    # Sync the project
    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
    RUN --mount=type=cache,target=/root/.cache/uv \
        uv sync --frozen

    CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
    # Stage 0, "build-stage", based on Node.js, to build and compile the frontend
    FROM node:20.18.1 AS build-stage

    WORKDIR /app

    COPY package*.json /app/

    RUN npm ci

    COPY ./ /app/

    ARG VITE_API_URL=""
    ENV VITE_API_URL=${VITE_API_URL}

    RUN npm run build


    # Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
    FROM nginx:1.27.3

    COPY --from=build-stage /app/dist/ /usr/share/nginx/html

    COPY ./nginx.conf /etc/nginx/conf.d/default.conf
    COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
    FROM node:20

    WORKDIR /app

    COPY package*.json /app/

    RUN npm install

    RUN npx -y playwright install --with-deps

    COPY ./ /app/

    ARG VITE_API_URL=${VITE_API_URL}
    # Python
    __pycache__
    app.egg-info
    *.pyc
    .mypy_cache
    .coverage
    htmlcov
    .venv
    node_modules
    dist
    .vscode
    node_modules/
    /test-results/
    /playwright-report/
    /blob-report/
    /playwright/.cache/

    # Local secrets and CI output (tracked template .env remains placeholders only)
    .env.*.local
    *.local.env
    rendered/
    *-ci.tar
    backend/test-results.xml
    backend/coverage.xml
    __pycache__/

    # Python cache
    __pycache__/
    *.py[cod]

    # Private recovery material and local kind tooling
    .migration-backup/
    sealed-secrets-key-backup.yaml
    .tools/

    # Private host Jenkins bootstrap state
    .jenkins-host/
    ✓ • 0ms

## Activity

    $ for f in deploy/base/*.yaml deploy/overlays/*/kustomization.yaml argocd/*.yaml argocd/bootstrap/*.yaml k8s/base/kustomization.yaml k8s/overlays/*/kustomization.yaml k8s/rbac/*.yaml ci/jenkins-controller-rbac.yaml; do echo "FILE $f"; nl -ba "$f"; done
    FILE deploy/base/configmap-backend.yaml
         1    apiVersion: v1
         2    kind: ConfigMap
         3    metadata:
         4      name: backend-config
         5      annotations:
         6        argocd.argoproj.io/sync-wave: '-2'
         7    data:
         8      DOMAIN: localhost
         9      FRONTEND_HOST: http://localhost:5173
        10      ENVIRONMENT: local
        11      PROJECT_NAME: Full Stack FastAPI Project
        12      BACKEND_CORS_ORIGINS: http://localhost,http://localhost:5173,https://localhost,https://localhost:5173
        13      FIRST_SUPERUSER: admin@example.com
        14      EMAILS_FROM_EMAIL: info@example.com
        15      SMTP_HOST: ''
        16      SMTP_USER: ''
        17      SMTP_TLS: 'True'
        18      SMTP_SSL: 'False'
        19      SMTP_PORT: '587'
        20      POSTGRES_SERVER: db
        21      POSTGRES_PORT: '5432'
        22      POSTGRES_DB: app
        23      POSTGRES_USER: postgres
        24      SENTRY_DSN: ''
    FILE deploy/base/configmap-db.yaml
         1    apiVersion: v1
         2    kind: ConfigMap
         3    metadata:
         4      name: db-config
         5      annotations:
         6        argocd.argoproj.io/sync-wave: '-2'
         7    data:
         8      PGDATA: /var/lib/postgresql/data/pgdata
         9      POSTGRES_DB: app
        10      POSTGRES_USER: postgres
    FILE deploy/base/deployment-adminer.yaml
         1    apiVersion: apps/v1
         2    kind: Deployment
         3    metadata:
         4      name: adminer
         5      labels:
         6        app: adminer
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      replicas: 1
        11      selector:
        12        matchLabels:
        13          app: adminer
        14      template:
        15        metadata:
        16          labels:
        17            app: adminer
        18        spec:
        19          containers:
        20          - name: adminer
        21            image: adminer:4.8.1
        22            ports:
        23            - containerPort: 8080
        24            env:
        25            - name: ADMINER_DESIGN
        26              value: pepa-linha-dark
        27            resources:
        28              requests:
        29                cpu: 50m
        30                memory: 64Mi
        31              limits:
        32                cpu: 200m
        33                memory: 128Mi
        34          automountServiceAccountToken: false
    FILE deploy/base/deployment-backend.yaml
         1    apiVersion: apps/v1
         2    kind: Deployment
         3    metadata:
         4      name: backend
         5      labels:
         6        app: backend
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '1'
         9    spec:
        10      replicas: 1
        11      selector:
        12        matchLabels:
        13          app: backend
        14      template:
        15        metadata:
        16          labels:
        17            app: backend
        18        spec:
        19          imagePullSecrets:
        20          - name: ghcr-pull-secret
        21          containers:
        22          - name: backend
        23            image: backend:unconfigured
        24            ports:
        25            - containerPort: 8000
        26            envFrom:
        27            - configMapRef:
        28                name: backend-config
        29            - secretRef:
        30                name: backend-secrets
        31            startupProbe:
        32              httpGet:
        33                path: /api/v1/utils/health-check/
        34                port: 8000
        35              periodSeconds: 5
        36              failureThreshold: 30
        37            readinessProbe:
        38              httpGet:
        39                path: /api/v1/utils/health-check/
        40                port: 8000
        41              initialDelaySeconds: 5
        42              periodSeconds: 10
        43            livenessProbe:
        44              httpGet:
        45                path: /api/v1/utils/health-check/
        46                port: 8000
        47              initialDelaySeconds: 15
        48              periodSeconds: 20
        49            resources:
        50              requests:
        51                cpu: 100m
        52                memory: 128Mi
        53              limits:
        54                cpu: 500m
        55                memory: 512Mi
        56          automountServiceAccountToken: false
    FILE deploy/base/deployment-db.yaml
         1    apiVersion: apps/v1
         2    kind: Deployment
         3    metadata:
         4      name: postgres-deployment
         5      labels:
         6        app: postgres
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      replicas: 1
        11      selector:
        12        matchLabels:
        13          app: postgres
        14      template:
        15        metadata:
        16          labels:
        17            app: postgres
        18        spec:
        19          containers:
        20          - name: postgres
        21            image: postgres:16.6
        22            ports:
        23            - containerPort: 5432
        24            envFrom:
        25            - configMapRef:
        26                name: db-config
        27            - secretRef:
        28                name: db-secrets
        29            volumeMounts:
        30            - mountPath: /var/lib/postgresql/data
        31              name: postgres-vol
        32            resources:
        33              requests:
        34                cpu: 250m
        35                memory: 256Mi
        36              limits:
        37                cpu: '1'
        38                memory: 1Gi
        39            readinessProbe:
        40              exec:
        41                command:
        42                - sh
        43                - -c
        44                - pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"
        45              periodSeconds: 5
        46            livenessProbe:
        47              tcpSocket:
        48                port: 5432
        49              initialDelaySeconds: 30
        50              periodSeconds: 20
        51          volumes:
        52          - name: postgres-vol
        53            persistentVolumeClaim:
        54              claimName: postgres-vol
        55          automountServiceAccountToken: false
        56      strategy:
        57        type: Recreate
    FILE deploy/base/deployment-frontend.yaml
         1    apiVersion: apps/v1
         2    kind: Deployment
         3    metadata:
         4      name: frontend
         5      labels:
         6        app: frontend
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '1'
         9    spec:
        10      replicas: 1
        11      selector:
        12        matchLabels:
        13          app: frontend
        14      template:
        15        metadata:
        16          labels:
        17            app: frontend
        18        spec:
        19          imagePullSecrets:
        20          - name: ghcr-pull-secret
        21          containers:
        22          - name: frontend
        23            image: frontend:unconfigured
        24            ports:
        25            - containerPort: 80
        26            resources:
        27              requests:
        28                cpu: 100m
        29                memory: 128Mi
        30              limits:
        31                cpu: 500m
        32                memory: 512Mi
        33            readinessProbe:
        34              httpGet:
        35                path: /
        36                port: 80
        37              periodSeconds: 10
        38              failureThreshold: 3
        39            livenessProbe:
        40              httpGet:
        41                path: /
        42                port: 80
        43              periodSeconds: 10
        44              failureThreshold: 3
        45          automountServiceAccountToken: false
    FILE deploy/base/ingress-app.yaml
         1    apiVersion: networking.k8s.io/v1
         2    kind: Ingress
         3    metadata:
         4      name: app-ingress
         5      annotations:
         6        argocd.argoproj.io/sync-wave: '-2'
         7    spec:
         8      ingressClassName: traefik
         9      rules:
        10      - host: app.example.com
        11        http:
        12          paths:
        13          - path: /api
        14            pathType: Prefix
        15            backend:
        16              service:
        17                name: backend
        18                port:
        19                  number: 80
        20          - path: /
        21            pathType: Prefix
        22            backend:
        23              service:
        24                name: frontend
        25                port:
        26                  number: 80
        27      tls:
        28      - hosts:
        29        - app.example.com
        30        secretName: app-tls
    FILE deploy/base/job-prestart.yaml
         1    apiVersion: batch/v1
         2    kind: Job
         3    metadata:
         4      name: prestart
         5      annotations:
         6        argocd.argoproj.io/sync-wave: '0'
         7        argocd.argoproj.io/hook: Sync
         8        argocd.argoproj.io/hook-delete-policy: BeforeHookCreation,HookSucceeded
         9    spec:
        10      backoffLimit: 3
        11      template:
        12        spec:
        13          restartPolicy: Never
        14          imagePullSecrets:
        15          - name: ghcr-pull-secret
        16          containers:
        17          - name: prestart
        18            image: backend:unconfigured
        19            command:
        20            - bash
        21            - scripts/prestart.sh
        22            envFrom:
        23            - configMapRef:
        24                name: backend-config
        25            - secretRef:
        26                name: backend-secrets
        27            resources:
        28              requests:
        29                cpu: 100m
        30                memory: 128Mi
        31              limits:
        32                cpu: 500m
        33                memory: 512Mi
        34          automountServiceAccountToken: false
        35      activeDeadlineSeconds: 600
    FILE deploy/base/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3    resources:
         4    - configmap-backend.yaml
         5    - configmap-db.yaml
         6    - pvc-db.yaml
         7    - deployment-backend.yaml
         8    - service-backend.yaml
         9    - deployment-db.yaml
        10    - service-db.yaml
        11    - deployment-frontend.yaml
        12    - service-frontend.yaml
        13    - deployment-adminer.yaml
        14    - service-adminer.yaml
        15    - job-prestart.yaml
        16    - ingress-app.yaml
    FILE deploy/base/pvc-db.yaml
         1    apiVersion: v1
         2    kind: PersistentVolumeClaim
         3    metadata:
         4      name: postgres-vol
         5      annotations:
         6        argocd.argoproj.io/sync-wave: '-2'
         7        argocd.argoproj.io/sync-options: Prune=false,Delete=false
         8    spec:
         9      accessModes:
        10      - ReadWriteOnce
        11      resources:
        12        requests:
        13          storage: 1Gi
        14      volumeMode: Filesystem
    FILE deploy/base/service-adminer.yaml
         1    apiVersion: v1
         2    kind: Service
         3    metadata:
         4      name: adminer
         5      labels:
         6        app: adminer
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      selector:
        11        app: adminer
        12      ports:
        13      - port: 80
        14        targetPort: 8080
    FILE deploy/base/service-backend.yaml
         1    apiVersion: v1
         2    kind: Service
         3    metadata:
         4      name: backend
         5      labels:
         6        app: backend
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      selector:
        11        app: backend
        12      ports:
        13      - port: 80
        14        targetPort: 8000
    FILE deploy/base/service-db.yaml
         1    apiVersion: v1
         2    kind: Service
         3    metadata:
         4      name: db
         5      labels:
         6        app: postgres
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      selector:
        11        app: postgres
        12      ports:
        13      - port: 5432
        14        targetPort: 5432
    FILE deploy/base/service-frontend.yaml
         1    apiVersion: v1
         2    kind: Service
         3    metadata:
         4      name: frontend
         5      labels:
         6        app: frontend
         7      annotations:
         8        argocd.argoproj.io/sync-wave: '-2'
         9    spec:
        10      selector:
        11        app: frontend
        12      ports:
        13      - port: 80
        14        targetPort: 80
    FILE deploy/overlays/dev/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3    namespace: app-dev
         4    resources:
         5    - ../../base
         6    images:
         7    - name: backend
         8      newName: ghcr.io/fastapi-traefik-devops/fastapi-backend
         9      newTag: sha-3303e93b753e8282dc7b461c583fb8ace43574a1
        10      digest: sha256:ea2d0aaf163f15f1bf749ee69822ebe33e619d2a00a5813d348732936b56f00b
        11    - name: frontend
        12      newName: ghcr.io/fastapi-traefik-devops/fastapi-frontend
        13      newTag: sha-3303e93b753e8282dc7b461c583fb8ace43574a1
        14      digest: sha256:a8d07b6be8ae8c76cc8133c885ba8ec3c095ded005db251aaf6a190e88426f82
        15    replicas:
        16    - name: backend
        17      count: 1
        18    - name: frontend
        19      count: 1
        20    patches:
        21    - target:
        22        kind: ConfigMap
        23        name: backend-config
        24      patch: |
        25        apiVersion: v1
        26        kind: ConfigMap
        27        metadata:
        28          name: backend-config
        29        data:
        30          BACKEND_CORS_ORIGINS: http://dev.example.com
        31          DOMAIN: dev.example.com
        32          ENVIRONMENT: staging
        33          FRONTEND_HOST: http://dev.example.com
        34    - target:
        35        kind: Ingress
        36        name: app-ingress
        37      patch: |
        38        - op: replace
        39          path: /spec/rules/0/host
        40          value: dev.example.com
        41        - op: remove
        42          path: /spec/tls
        43        - op: add
        44          path: /spec/rules/0/http/paths/-
        45          value:
        46            path: /docs
        47            pathType: Prefix
        48            backend:
        49              service:
        50                name: backend
        51                port:
        52                  number: 80
        53    - target:
        54        kind: Deployment
        55        name: backend
        56      patch: |
        57        - op: add
        58          path: /spec/template/spec/containers/0/command
        59          value: ["fastapi", "run", "--workers", "1", "app/main.py"]
    FILE deploy/overlays/prod/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3    namespace: app-prod
         4    resources:
         5    - ../../base
         6    images:
         7    - name: backend
         8      newName: ghcr.io/fastapi-traefik-devops/fastapi-backend
         9      newTag: sha-0000000000000000000000000000000000000000
        10    - name: frontend
        11      newName: ghcr.io/fastapi-traefik-devops/fastapi-frontend
        12      newTag: sha-0000000000000000000000000000000000000000
        13    replicas:
        14    - name: backend
        15      count: 2
        16    - name: frontend
        17      count: 2
        18    patches:
        19    - target:
        20        kind: ConfigMap
        21        name: backend-config
        22      patch: "apiVersion: v1\ndata:\n  BACKEND_CORS_ORIGINS: https://prod.example.com\n\
        23        \  DOMAIN: prod.example.com\n  ENVIRONMENT: production\n  FRONTEND_HOST: https://prod.example.com\n\
        24        kind: ConfigMap\nmetadata:\n  name: backend-config\n"
        25    - target:
        26        kind: Ingress
        27        name: app-ingress
        28      patch: "- op: replace\n  path: /spec/rules/0/host\n  value: prod.example.com\n-\
        29        \ op: replace\n  path: /spec/tls/0/hosts/0\n  value: prod.example.com\n"
    FILE deploy/overlays/stage/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3    namespace: app-stage
         4    resources:
         5    - ../../base
         6    images:
         7    - name: backend
         8      newName: ghcr.io/fastapi-traefik-devops/fastapi-backend
         9      newTag: sha-3303e93b753e8282dc7b461c583fb8ace43574a1
        10      digest: sha256:ea2d0aaf163f15f1bf749ee69822ebe33e619d2a00a5813d348732936b56f00b
        11    - name: frontend
        12      newName: ghcr.io/fastapi-traefik-devops/fastapi-frontend
        13      newTag: sha-3303e93b753e8282dc7b461c583fb8ace43574a1
        14      digest: sha256:a8d07b6be8ae8c76cc8133c885ba8ec3c095ded005db251aaf6a190e88426f82
        15    replicas:
        16    - name: backend
        17      count: 1
        18    - name: frontend
        19      count: 1
        20    patches:
        21    - target:
        22        kind: ConfigMap
        23        name: backend-config
        24      patch: "apiVersion: v1\ndata:\n  BACKEND_CORS_ORIGINS: https://stage.example.com\n\
        25        \  DOMAIN: stage.example.com\n  ENVIRONMENT: staging\n  FRONTEND_HOST: https://stage.example.com\n\
        26        kind: ConfigMap\nmetadata:\n  name: backend-config\n"
        27    - target:
        28        kind: Ingress
        29        name: app-ingress
        30      patch: "- op: replace\n  path: /spec/rules/0/host\n  value: stage.example.com\n\
        31        - op: replace\n  path: /spec/tls/0/hosts/0\n  value: stage.example.com\n"
        32    - target:
        33        kind: Deployment
        34        name: backend
        35      patch: |
        36        - op: add
        37          path: /spec/template/spec/containers/0/command
        38          value: ["fastapi", "run", "--workers", "1", "app/main.py"]
    FILE argocd/app-dev.yaml
         1    # Bootstrap only after the DEV overlay is on remote main and secrets are ready.
         2    # Apply this DEV-only Application; the existing ApplicationSet also enables PROD.
         3    apiVersion: argoproj.io/v1alpha1
         4    kind: Application
         5    metadata:
         6      name: app-dev
         7      namespace: argocd
         8    spec:
         9      project: fastapi
        10      source:
        11        repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        12        targetRevision: main
        13        path: deploy/overlays/dev
        14      destination:
        15        server: https://kubernetes.default.svc
        16        namespace: app-dev
        17      syncPolicy:
        18        automated:
        19          prune: true
        20          selfHeal: true
        21        retry:
        22          limit: 5
        23          backoff:
        24            duration: 5s
        25            factor: 2
        26            maxDuration: 3m
        27        syncOptions:
        28          - PruneLast=true
    FILE argocd/app-monitoring.yaml
         1    # kind DEV/STAGE monitoring: capacity and runtime validated with Jenkins offline.
         2    # Apply this Git-backed source only after monitoring files are published to main.
         3    apiVersion: argoproj.io/v1alpha1
         4    kind: Application
         5    metadata:
         6      name: monitoring
         7      namespace: argocd
         8    spec:
         9      project: monitoring
        10      sources:
        11      - repoURL: https://prometheus-community.github.io/helm-charts
        12        chart: kube-prometheus-stack
        13        targetRevision: 92.2.0
        14        helm:
        15          releaseName: monitoring
        16          valueFiles:
        17          - $values/monitoring/values.yaml
        18      - repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        19        targetRevision: main
        20        ref: values
        21      - repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        22        targetRevision: main
        23        path: monitoring
        24      destination:
        25        server: https://kubernetes.default.svc
        26        namespace: monitoring
        27      syncPolicy:
        28        automated:
        29          prune: false
        30          selfHeal: true
        31          allowEmpty: false
        32          enabled: true
        33        retry:
        34          limit: 3
        35          backoff:
        36            duration: 10s
        37            factor: 2
        38            maxDuration: 1m
        39        syncOptions:
        40        - ServerSideApply=true
        41        - SkipDryRunOnMissingResource=true
        42        - PruneLast=true
    FILE argocd/app-stage.yaml
         1    apiVersion: argoproj.io/v1alpha1
         2    kind: Application
         3    metadata:
         4      name: app-stage
         5      namespace: argocd
         6    spec:
         7      project: fastapi
         8      source:
         9        repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        10        targetRevision: main
        11        path: deploy/overlays/stage
        12      destination:
        13        server: https://kubernetes.default.svc
        14        namespace: app-stage
        15      syncPolicy:
        16        automated:
        17          prune: true
        18          selfHeal: true
        19        retry:
        20          limit: 5
        21          backoff:
        22            duration: 5s
        23            factor: 2
        24            maxDuration: 3m
        25        syncOptions:
        26        - PruneLast=true
    FILE argocd/applicationset.yaml
         1    apiVersion: argoproj.io/v1alpha1
         2    kind: ApplicationSet
         3    metadata:
         4      name: fastapi
         5      namespace: argocd
         6    spec:
         7      generators:
         8        - list:
         9            elements:
        10              - environment: dev
        11              - environment: stage
        12              - environment: prod
        13      template:
        14        metadata:
        15          name: 'app-{{environment}}'
        16        spec:
        17          project: fastapi
        18          source:
        19            repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        20            targetRevision: main
        21            path: 'deploy/overlays/{{environment}}'
        22          destination:
        23            server: https://kubernetes.default.svc
        24            namespace: 'app-{{environment}}'
        25          syncPolicy:
        26            automated:
        27              prune: true
        28              selfHeal: true
        29              allowEmpty: false
        30            retry:
        31              limit: 5
        32              backoff:
        33                duration: 5s
        34                factor: 2
        35                maxDuration: 3m
        36            syncOptions:
        37              - PruneLast=true
    FILE argocd/project-monitoring.yaml
         1    apiVersion: argoproj.io/v1alpha1
         2    kind: AppProject
         3    metadata:
         4      name: monitoring
         5      namespace: argocd
         6    spec:
         7      description: DEV/STAGE monitoring platform; no production destinations
         8      sourceRepos:
         9      - https://prometheus-community.github.io/helm-charts
        10      - https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        11      destinations:
        12      - namespace: monitoring
        13        server: https://kubernetes.default.svc
        14      clusterResourceWhitelist:
        15      - group: apiextensions.k8s.io
        16        kind: CustomResourceDefinition
        17      - group: rbac.authorization.k8s.io
        18        kind: ClusterRole
        19      - group: rbac.authorization.k8s.io
        20        kind: ClusterRoleBinding
        21      namespaceResourceWhitelist:
        22      - group: ''
        23        kind: ConfigMap
        24      - group: ''
        25        kind: Secret
        26      - group: ''
        27        kind: Service
        28      - group: ''
        29        kind: ServiceAccount
        30      - group: ''
        31        kind: PersistentVolumeClaim
        32      - group: apps
        33        kind: Deployment
        34      - group: apps
        35        kind: DaemonSet
        36      - group: apps
        37        kind: StatefulSet
        38      - group: rbac.authorization.k8s.io
        39        kind: Role
        40      - group: rbac.authorization.k8s.io
        41        kind: RoleBinding
        42      - group: monitoring.coreos.com
        43        kind: Prometheus
        44      - group: monitoring.coreos.com
        45        kind: Alertmanager
        46      - group: monitoring.coreos.com
        47        kind: ServiceMonitor
        48      - group: monitoring.coreos.com
        49        kind: PodMonitor
        50      - group: monitoring.coreos.com
        51        kind: PrometheusRule
    FILE argocd/project.yaml
         1    apiVersion: argoproj.io/v1alpha1
         2    kind: AppProject
         3    metadata:
         4      name: fastapi
         5      namespace: argocd
         6    spec:
         7      description: FastAPI GitOps environments
         8      sourceRepos:
         9        - https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        10      destinations:
        11        - server: https://kubernetes.default.svc
        12          namespace: app-dev
        13        - server: https://kubernetes.default.svc
        14          namespace: app-stage
        15        - server: https://kubernetes.default.svc
        16          namespace: app-prod
        17      clusterResourceWhitelist: []
        18      namespaceResourceWhitelist:
        19        - group: ''
        20          kind: ConfigMap
        21        - group: ''
        22          kind: Service
        23        - group: ''
        24          kind: PersistentVolumeClaim
        25        - group: apps
        26          kind: Deployment
        27        - group: batch
        28          kind: Job
        29        - group: networking.k8s.io
        30          kind: Ingress
    FILE argocd/bootstrap/dev-namespace.yaml
         1    # Operator bootstrap: fastapi AppProject intentionally cannot create Namespaces.
         2    apiVersion: v1
         3    kind: Namespace
         4    metadata:
         5      name: app-dev
    FILE argocd/bootstrap/monitoring-namespace.yaml
         1    apiVersion: v1
         2    kind: Namespace
         3    metadata:
         4      name: monitoring
    FILE k8s/base/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3
         4    resources:
         5      - configmap-backend.yaml
         6      - configmap-db.yaml
         7      - configmap-frontend.yaml
         8      - secret-backend.yaml
         9      - secret-db.yaml
        10      - secret-frontend.yaml
        11      - pvc-db.yaml
        12      - deployment-backend.yaml
        13      - service-backend.yaml
        14      - deployment-db.yaml
        15      - service-db.yaml
        16      - deployment-frontend.yaml
        17      - service-frontend.yaml
        18      - deployment-adminer.yaml
        19      - service-adminer.yaml
        20      - job-prestart.yaml
        21      - ingress-app.yaml
        22
        23    images:
        24      - name: backend
        25        newName: ghcr.io/fastapi-traefik-devops/fastapi-backend
        26        newTag: v0.1.0
        27      - name: frontend
        28        newName: ghcr.io/fastapi-traefik-devops/fastapi-frontend
        29        newTag: v0.1.0
    FILE k8s/overlays/dev/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3
         4    namespace: dev
         5
         6    resources:
         7      - ../../base
    FILE k8s/overlays/prod/kustomization.yaml
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3
         4    namespace: prod
         5
         6    resources:
         7      - ../../base
         8
         9    patches:
        10      - target:
        11          kind: Deployment
        12          name: backend
        13        patch: |-
        14          - op: replace
        15            path: /spec/replicas
        16            value: 2
        17      - target:
        18          kind: Deployment
        19          name: frontend
        20        patch: |-
        21          - op: replace
        22            path: /spec/replicas
        23            value: 2
        24      - target:
        25          kind: Ingress
        26          name: app-ingress
        27        patch: |-
        28          - op: replace
        29            path: /spec/rules/0/host
        30            value: api.yourdomain.com
        31          - op: replace
        32            path: /spec/rules/1/host
        33            value: dashboard.yourdomain.com
    FILE k8s/rbac/jenkins-controller-dev-rbac.yaml
         1    # Legacy controller access to the application namespace is retired.
         2    # Operator must apply/revoke the existing live role during migration.
         3    apiVersion: rbac.authorization.k8s.io/v1
         4    kind: Role
         5    metadata:
         6      name: jenkins-controller-agent-manager
         7      namespace: dev
         8    rules: []
    FILE k8s/rbac/jenkins-dev-rbac.yaml
         1    # Legacy role intentionally grants no permissions. See README-jenkins.md.
         2    # Existing cluster bindings must be revoked by an administrator during migration.
         3    apiVersion: rbac.authorization.k8s.io/v1
         4    kind: Role
         5    metadata:
         6      name: jenkins-agent
         7      namespace: dev
         8    rules: []
    FILE ci/jenkins-controller-rbac.yaml
         1    # Apply only during operator-led bootstrap; never from Jenkins pipelines.
         2    apiVersion: rbac.authorization.k8s.io/v1
         3    kind: Role
         4    metadata:
         5      name: jenkins-agent-manager
         6      namespace: jenkins-ci
         7    rules:
         8      - apiGroups: ['']
         9        resources: [pods, pods/log, pods/exec]
        10        verbs: [get, list, watch, create, delete, patch, update]
        11    ---
        12    apiVersion: rbac.authorization.k8s.io/v1
        13    kind: RoleBinding
        14    metadata:
        15      name: jenkins-agent-manager
        16      namespace: jenkins-ci
        17    subjects:
        18      - kind: ServiceAccount
        19        name: jenkins
        20        namespace: jenkins
        21    roleRef:
        22      kind: Role
        23      name: jenkins-agent-manager
        24      apiGroup: rbac.authorization.k8s.io
        25    ---
        26    apiVersion: rbac.authorization.k8s.io/v1
        27    kind: Role
        28    metadata:
        29      name: jenkins-agent-manager
        30      namespace: jenkins-publish
        31    rules:
        32      - apiGroups: ['']
        33        resources: [pods, pods/log, pods/exec]
        34        verbs: [get, list, watch, create, delete, patch, update]
        35    ---
        36    apiVersion: rbac.authorization.k8s.io/v1
        37    kind: RoleBinding
        38    metadata:
        39      name: jenkins-agent-manager
        40      namespace: jenkins-publish
        41    subjects:
        42      - kind: ServiceAccount
        43        name: jenkins
        44        namespace: jenkins
        45    roleRef:
        46      kind: Role
        47      name: jenkins-agent-manager
        48      apiGroup: rbac.authorization.k8s.io
    ✓ • 380ms

## Activity

    $ for f in README.md ci/README.md ci/VERIFICATION.md deployment.md development.md docker-compose.yml docker-compose.override.yml docker-compose.traefik.yml .github/workflows/test-backend.yml .github/workflows/lint-backend.yml .github/workflows/playwright.yml .github/workflows/test-docker-compose.yml .github/dependabot.yml; do echo "FILE $f"; nl -ba "$f"; done
    FILE README.md
         1    # Full Stack FastAPI Template
         2
         3    <a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test/badge.svg" alt="Test"></a>
         4    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/full-stack-fastapi-template.svg" alt="Coverage"></a>
         5
         6    ## Technology Stack and Features
         7
         8    - ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
         9        - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
        10        - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
        11        - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
        12    - 🚀 [React](https://react.dev) for the frontend.
        13        - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
        14        - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
        15        - 🤖 An automatically generated frontend client.
        16        - 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
        17        - 🦇 Dark mode support.
        18    - 🐋 [Docker Compose](https://www.docker.com) for development and production.
        19    - 🔒 Secure password hashing by default.
        20    - 🔑 JWT (JSON Web Token) authentication.
        21    - 📫 Email based password recovery.
        22    - ✅ Tests with [Pytest](https://pytest.org).
        23    - 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
        24    - 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
        25    - 🏭 CI/CD using GitHub Flow, Jenkins, GHCR and Argo CD; see [the operating guide](README-jenkins.md).
        26
        27    ### Dashboard Login
        28
        29    [![API docs](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)
        30
        31    ### Dashboard - Admin
        32
        33    [![API docs](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)
        34
        35    ### Dashboard - Create User
        36
        37    [![API docs](img/dashboard-create.png)](https://github.com/fastapi/full-stack-fastapi-template)
        38
        39    ### Dashboard - Items
        40
        41    [![API docs](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)
        42
        43    ### Dashboard - User Settings
        44
        45    [![API docs](img/dashboard-user-settings.png)](https://github.com/fastapi/full-stack-fastapi-template)
        46
        47    ### Dashboard - Dark Mode
        48
        49    [![API docs](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)
        50
        51    ### Interactive API Documentation
        52
        53    [![API docs](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)
        54
        55    ## How To Use It
        56
        57    You can **just fork or clone** this repository and use it as is.
        58
        59    ✨ It just works. ✨
        60
        61    ### How to Use a Private Repository
        62
        63    If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.
        64
        65    But you can do the following:
        66
        67    - Create a new GitHub repo, for example `my-full-stack`.
        68    - Clone this repository manually, set the name with the name of the project you want to use, for example `my-full-stack`:
        69
        70    ```bash
        71    git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
        72    ```
        73
        74    - Enter into the new directory:
        75
        76    ```bash
        77    cd my-full-stack
        78    ```
        79
        80    - Set the new origin to your new repository, copy it from the GitHub interface, for example:
        81
        82    ```bash
        83    git remote set-url origin git@github.com:octocat/my-full-stack.git
        84    ```
        85
        86    - Add this repo as another "remote" to allow you to get updates later:
        87
        88    ```bash
        89    git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
        90    ```
        91
        92    - Push the code to your new repository:
        93
        94    ```bash
        95    git push -u origin master
        96    ```
        97
        98    ### Update From the Original Template
        99
       100    After cloning the repository, and after doing changes, you might want to get the latest changes from this original template.
       101
       102    - Make sure you added the original repository as a remote, you can check it with:
       103
       104    ```bash
       105    git remote -v
       106
       107    origin    git@github.com:octocat/my-full-stack.git (fetch)
       108    origin    git@github.com:octocat/my-full-stack.git (push)
       109    upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)
       110    upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
       111    ```
       112
       113    - Pull the latest changes without merging:
       114
       115    ```bash
       116    git pull --no-commit upstream master
       117    ```
       118
       119    This will download the latest changes from this template without committing them, that way you can check everything is right before committing.
       120
       121    - If there are conflicts, solve them in your editor.
       122
       123    - Once you are done, commit the changes:
       124
       125    ```bash
       126    git merge --continue
       127    ```
       128
       129    ### Configure
       130
       131    You can then update configs in the `.env` files to customize your configurations.
       132
       133    Before deploying it, make sure you change at least the values for:
       134
       135    - `SECRET_KEY`
       136    - `FIRST_SUPERUSER_PASSWORD`
       137    - `POSTGRES_PASSWORD`
       138
       139    You can (and should) pass these as environment variables from secrets.
       140
       141    Read the [deployment.md](./deployment.md) docs for more details.
       142
       143    ### Generate Secret Keys
       144
       145    Some environment variables in the `.env` file have a default value of `changethis`.
       146
       147    You have to change them with a secret key, to generate secret keys you can run the following command:
       148
       149    ```bash
       150    python -c "import secrets; print(secrets.token_urlsafe(32))"
       151    ```
       152
       153    Copy the content and use that as password / secret key. And run that again to generate another secure key.
       154
       155    ## How To Use It - Alternative With Copier
       156
       157    This repository also supports generating a new project using [Copier](https://copier.readthedocs.io).
       158
       159    It will copy all the files, ask you configuration questions, and update the `.env` files with your answers.
       160
       161    ### Install Copier
       162
       163    You can install Copier with:
       164
       165    ```bash
       166    pip install copier
       167    ```
       168
       169    Or better, if you have [`pipx`](https://pipx.pypa.io/), you can run it with:
       170
       171    ```bash
       172    pipx install copier
       173    ```
       174
       175    **Note**: If you have `pipx`, installing copier is optional, you could run it directly.
       176
       177    ### Generate a Project With Copier
       178
       179    Decide a name for your new project's directory, you will use it below. For example, `my-awesome-project`.
       180
       181    Go to the directory that will be the parent of your project, and run the command with your project's name:
       182
       183    ```bash
       184    copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
       185    ```
       186
       187    If you have `pipx` and you didn't install `copier`, you can run it directly:
       188
       189    ```bash
       190    pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
       191    ```
       192
       193    **Note** the `--trust` option is necessary to be able to execute a [post-creation script](https://github.com/fastapi/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py) that updates your `.env` files.
       194
       195    ### Input Variables
       196
       197    Copier will ask you for some data, you might want to have at hand before generating the project.
       198
       199    But don't worry, you can just update any of that in the `.env` files afterwards.
       200
       201    The input variables, with their default values (some auto generated) are:
       202
       203    - `project_name`: (default: `"FastAPI Project"`) The name of the project, shown to API users (in .env).
       204    - `stack_name`: (default: `"fastapi-project"`) The name of the stack used for Docker Compose labels and project name (no spaces, no periods) (in .env).
       205    - `secret_key`: (default: `"changethis"`) The secret key for the project, used for security, stored in .env, you can generate one with the method above.
       206    - `first_superuser`: (default: `"admin@example.com"`) The email of the first superuser (in .env).
       207    - `first_superuser_password`: (default: `"changethis"`) The password of the first superuser (in .env).
       208    - `smtp_host`: (default: "") The SMTP server host to send emails, you can set it later in .env.
       209    - `smtp_user`: (default: "") The SMTP server user to send emails, you can set it later in .env.
       210    - `smtp_password`: (default: "") The SMTP server password to send emails, you can set it later in .env.
       211    - `emails_from_email`: (default: `"info@example.com"`) The email account to send emails from, you can set it later in .env.
       212    - `postgres_password`: (default: `"changethis"`) The password for the PostgreSQL database, stored in .env, you can generate one with the method above.
       213    - `sentry_dsn`: (default: "") The DSN for Sentry, if you are using it, you can set it later in .env.
       214
       215    ## Backend Development
       216
       217    Backend docs: [backend/README.md](./backend/README.md).
       218
       219    ## Frontend Development
       220
       221    Frontend docs: [frontend/README.md](./frontend/README.md).
       222
       223    ## Jenkins CI
       224
       225    Jenkins setup, local access, pipeline stages, and troubleshooting: [README-jenkins.md](./README-jenkins.md).
       226
       227    ## Deployment
       228
       229    Deployment docs: [deployment.md](./deployment.md).
       230
       231    ## Kubernetes GitOps
       232
       233    Active manifests live in `deploy/base` and `deploy/overlays/{dev,stage,prod}`.
       234    Argo CD owns application deployment; Jenkins builds images and modifies Git.
       235    See [Jenkins setup and release procedures](README-jenkins.md) and
       236    [Argo bootstrap and rollback](deployment.md).
       237
       238    `k8s/` is retained for historical/local reference. Do not apply it alongside the
       239    active GitOps applications. Its old sealed secrets belong to their original
       240    namespace/cluster. Production uses externally provisioned secrets.
    FILE ci/README.md
         1    # CI implementation
         2
         3    See [the operating guide](../README-jenkins.md). Scripts in this directory are
         4    executed by Jenkins; only the trusted promotion job receives write credentials.
    FILE ci/VERIFICATION.md
         1    # Local verification — 2026-10-03
         2
         3    No changes were pushed, no release/tag/PR was created on GitHub, and no real
         4    Kubernetes or Argo resources were applied. Existing application workloads were
         5    not touched. The pre-existing untracked `.swp` was left untouched.
         6
         7    ## Executed checks
         8
         9    | Check | Result |
        10    | --- | --- |
        11    | Kustomize 5.6.0 render, dev/stage/prod | PASS |
        12    | kubeconform 0.6.7, strict Kubernetes 1.31 schemas | PASS: 13 resources/environment, 39 total, no skips |
        13    | YAML parsing | PASS: deployment/Argo/RBAC files and both embedded Jenkins Pod templates |
        14    | Argo AppProject/ApplicationSet schema validation | PASS against official Argo CD v2.13.3 CRD schemas, downloaded to /tmp; not a claim about installed Argo version |
        15    | Jenkinsfiles | PASS offline Groovy 4.0.24 parse through CONVERSION; actual Jenkins Declarative validation not available |
        16    | Shell scripts and embedded pipeline shells | PASS `sh -n` |
        17    | Promotion safety suite | PASS: 12 tests, real temporary local Git remotes and mocked registry; covers CAS retry, stale stage rejection, release ancestry/history/digest checks, review-branch-only writes, idempotence, write-once tags, auth failure |
        18    | Backend mypy/Ruff/format | PASS using uv 0.5.11, frozen lock |
        19    | Backend migrations/pytest | PASS: 55 tests, two SQLAlchemy warnings; disposable PostgreSQL 16, loopback-only, no host ports, stopped afterward |
        20    | Backend JUnit/coverage | Generated `backend/test-results.xml`, `backend/coverage.xml`; 94% coverage (existing scope includes tests) |
        21    | Frontend npm ci / TypeScript / Vite | PASS with Node 20.18.1; sourcemap and large-chunk warnings |
        22    | Dockerfiles | PASS for backend and frontend with local Docker BuildKit; no registry push |
        23    | BuildKit archive / publisher compatibility | PASS: frontend Docker-format export parsed by crane digest without loading/running the image |
        24    | Frontend image | nginx configuration and environment-independent API URL checked locally |
        25    | Diff whitespace / credential review | PASS; no new real plaintext secrets detected; existing .env sensitive keys are placeholders, existing sealed secrets remain encrypted |
        26
        27    Frontend installation reports **61 vulnerabilities: 4 moderate, 54 high, 3 critical**
        28    in the existing dependency tree. These require a separate dependency remediation
        29    review before production; no automatic breaking upgrades were performed. Versions
        30    are pinned for repeatability, not asserted to be current/security-supported.
        31
        32    Local logs are under `/tmp/gitops-*-check.log`, `/tmp/gitops-*-build.log`,
        33    `/tmp/gitops-promotion-tests.log`, `/tmp/gitops-groovy-check.log`, and
        34    `/tmp/gitops-archive-check.log`. Verification images use the local tags
        35    `fastapi-gitops-local/backend:verification` and
        36    `fastapi-gitops-local/frontend:verification`. They were not published. Build cache
        37    and local verification outputs remain available; no shared Docker cache was pruned.
        38
        39    ## Not tested end to end
        40
        41    Actual Jenkins plugin/Declarative compatibility, job ACLs/credentials, Kubernetes
        42    cloud scheduling/admission isolation, GitHub webhooks/tag discovery/status checks,
        43    GHCR authentication/uploads/retagging, real GitHub fast-forward pushes/ruleset
        44    bypass, Argo reconciliation, real TLS/ingress/storage, and production health were
        45    not tested. GitHub PR creation is deliberately manual. No credentials were read
        46    from a live Kubernetes Secret. Cluster version was not queried. A controlled
        47    non-production acceptance run is required after the documented setup.
        48
        49    ## Final architecture review
        50
        51    | Question | Finding |
        52    | --- | --- |
        53    | Can Jenkins deploy app workloads directly? | Neither pipeline has kubectl/helm/Argo deployment calls or an app kubeconfig. Operator must revoke pre-existing live workload RBAC; repository edits cannot prove existing live permissions are gone. |
        54    | Is Git desired state for all environments? | Yes: main, deploy/overlays/dev, stage, prod; Argo tracks these paths. |
        55    | Are images immutable and commit-tied? | SHA tags are write-once by publisher policy; actual workload images are digest-pinned after promotion. Initial zero-SHA placeholders intentionally do not deploy. |
        56    | Is the same artifact promoted? | Yes: CI archives are copied to GHCR; release only checks/retags recorded digests. No build command in publisher/release code. |
        57    | Can untrusted PRs obtain write credentials? | CI receives none; trusted folder and restricted cloud/node/admission configuration are mandatory. This boundary has not been tested live. |
        58    | Can GitOps commits recurse forever? | No: changed-path filtering validates GitOps-only commits but does not archive/publish/trigger promotion. |
        59    | Can promotions overwrite each other? | Global lock plus one publisher build at a time; fast-forward Git retry; stage freshness/ancestry checks. Prod changes require up-to-date reviewed PRs. Tested locally for Git races. |
        60    | Can prod change without approval? | Release code writes a review branch only after Jenkins approval. Main protections and code-owner reviews must cover shared base/Argo/pipeline paths too. A compromised bypass bot remains a documented GitHub permission limitation. |
        61    | Do all overlays render and validate? | Yes, 39 strict resource schema checks passed without skips. |
        62    | Any real secrets in the change? | None detected; no new plaintext Secret manifests. Historical Git objects were not audited. |
        63    | Does documentation match implementation? | Current guide describes the two-job trust boundary, asynchronous publisher, manual PR, tag discovery/manual fallback, SHA selection, recursion, validation, prerequisites and limitations. Historical guides are marked accordingly. |
    FILE deployment.md
         1    # Argo CD deployment
         2
         3    The production path is [GitHub Flow + Jenkins + GHCR + Argo CD](README-jenkins.md).
         4    Jenkins never applies application resources. Git `main`, `deploy/overlays/{dev,stage,prod}`,
         5    is desired state. `k8s/` is a retained legacy example, not an active deployment root.
         6    Do not apply both manifest trees to the same workload. Compose remains a separate
         7    local development tool, not this project's production CD system.
         8
         9    ## One-time operator bootstrap
        10
        11    Do not run these steps until the changes have been reviewed/merged, Jenkins trust
        12    boundaries configured, and real hostnames/secrets/storage prepared. These commands
        13    are instructions only; no real cluster was changed during implementation.
        14
        15    1. Install a supported, organization-approved Argo CD version, including its
        16       ApplicationSet controller, or connect to your existing installation. Download
        17       and review the exact release manifests (never an unpinned `stable` URL), e.g.:
        18
        19       ```bash
        20       export ARGOCD_VERSION='<approved-version>'
        21       curl -fL "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml" -o /tmp/argocd-install.yaml
        22       # Review the downloaded manifest before the next commands.
        23       kubectl create namespace argocd
        24       kubectl apply -n argocd -f /tmp/argocd-install.yaml
        25       ```
        26
        27       Skip installation if Argo already exists. Configure SSO/RBAC and restrict
        28       Application/AppProject writes and sync overrides to platform administrators.
        29       Ordinary users must not override main, image parameters or the production
        30       source path. Register a read-only repository credential in Argo for private Git.
        31    2. Create `app-dev`, `app-stage`, `app-prod` namespaces outside the ApplicationSet:
        32
        33       ```bash
        34       kubectl create namespace app-dev
        35       kubectl create namespace app-stage
        36       kubectl create namespace app-prod
        37       ```
        38
        39       Provision `backend-secrets`, `db-secrets`, `ghcr-pull-secret`, and `app-tls`
        40       securely in each namespace. See the exact key/permission table in
        41       README-jenkins.md. Use an external secret manager or newly sealed namespace-
        42       specific secrets; never commit generated plaintext YAML. Configure Traefik,
        43       DNS and valid TLS certificates for real hosts replacing `*.example.com` in
        44       overlays. The AppProject cannot create Namespaces, Secrets or cluster RBAC.
        45    3. Choose the cluster's storage class and capacity, backup/restore and database
        46       ownership. The base retains a 1Gi default-class RWO PVC and a single PostgreSQL
        47       Deployment using Recreate to avoid concurrent writers. PVC deletion/pruning
        48       is disabled in Argo annotations; do not assume this substitutes for backups.
        49       Migrating existing `dev` data into `app-dev` requires an explicit operator data
        50       migration plan. No existing namespace/data is adopted or deleted automatically.
        51    4. Complete the Jenkins setup, publish real images, and promote dev/stage. Initial
        52       overlay tags are deliberately all-zero SHA placeholders and will not pull.
        53       Before enabling each Argo application, replace that environment's placeholder
        54       through its normal promotion flow; production still needs a reviewed release.
        55       For phased bootstrap, temporarily list only provisioned environments in the
        56       ApplicationSet through a reviewed Git change, adding prod after approval.
        57    5. Review and apply the AppProject/ApplicationSet as an administrator:
        58
        59       ```bash
        60       kubectl apply -f argocd/project.yaml
        61       kubectl apply -f argocd/applicationset.yaml
        62       ```
        63
        64       They define `app-dev`, `app-stage`, `app-prod` against the in-cluster API,
        65       tracking only this repository's main. All automatically sync, prune and
        66       self-heal **after** Git approval. For an external cluster update both
        67       destination definitions and register that cluster with Argo first.
        68    6. Verify actual Argo sync/health, image digests and migrations in dev/stage before
        69       production. Set up alerting for failed hooks, sync failures and missing Secrets.
        70       Normal subsequent application deployment requires only Git changes.
        71
        72    ## Rollback
        73
        74    Revert the offending overlay promotion commit in a reviewed PR, restoring both
        75    `kustomization.yaml` SHA/digests and `promotion.json` together, or explicitly set
        76    both to a previously recorded artifact pair. Merge to main; Argo detects the
        77    reverted desired state and reconciles it. No image rebuild or Jenkins cluster
        78    command is needed. A new main build can subsequently advance stage again.
        79
        80    For production, review the rollback PR under the same rules as a release. Avoid
        81    Argo UI rollback/parameter overrides while auto-sync is enabled: Git would restore
        82    the declared state. Database migrations are not automatically reversible; verify
        83    schema compatibility before reverting application images and use your separately
        84    approved restore/migration procedure when necessary. Keep old image digests in GHCR.
        85
        86    ## References
        87
        88    - [Argo sync phases/waves and hooks](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
        89    - [Jenkins credentials and untrusted pipelines](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
        90    - [GHCR digest-based pulls](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
    FILE development.md
         1    > Production deployment now uses [Jenkins and Argo CD](README-jenkins.md).
         2    > The Compose/subdomain examples below describe local or standalone development;
         3    > GitOps environments use one origin with `/api` ingress routing.
         4
         5    # FastAPI Project - Development
         6
         7    ## Docker Compose
         8
         9    * Start the local stack with Docker Compose:
        10
        11    ```bash
        12    docker compose watch
        13    ```
        14
        15    * Now you can open your browser and interact with these URLs:
        16
        17    Frontend, built with Docker, with routes handled based on the path: http://localhost:5173
        18
        19    Backend, JSON based web API based on OpenAPI: http://localhost:8000
        20
        21    Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs
        22
        23    Adminer, database web administration: http://localhost:8080
        24
        25    Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090
        26
        27    **Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.
        28
        29    To check the logs, run (in another terminal):
        30
        31    ```bash
        32    docker compose logs
        33    ```
        34
        35    To check the logs of a specific service, add the name of the service, e.g.:
        36
        37    ```bash
        38    docker compose logs backend
        39    ```
        40
        41    ## Local Development
        42
        43    The Docker Compose files are configured so that each of the services is available in a different port in `localhost`.
        44
        45    For the backend and frontend, they use the same port that would be used by their local development server, so, the backend is at `http://localhost:8000` and the frontend at `http://localhost:5173`.
        46
        47    This way, you could turn off a Docker Compose service and start its local development service, and everything would keep working, because it all uses the same ports.
        48
        49    For example, you can stop that `frontend` service in the Docker Compose, in another terminal, run:
        50
        51    ```bash
        52    docker compose stop frontend
        53    ```
        54
        55    And then start the local frontend development server:
        56
        57    ```bash
        58    cd frontend
        59    npm run dev
        60    ```
        61
        62    Or you could stop the `backend` Docker Compose service:
        63
        64    ```bash
        65    docker compose stop backend
        66    ```
        67
        68    And then you can run the local development server for the backend:
        69
        70    ```bash
        71    cd backend
        72    fastapi dev app/main.py
        73    ```
        74
        75    ## Docker Compose in `localhost.tiangolo.com`
        76
        77    When you start the Docker Compose stack, it uses `localhost` by default, with different ports for each service (backend, frontend, adminer, etc).
        78
        79    When you deploy it to production (or staging), it will deploy each service in a different subdomain, like `api.example.com` for the backend and `dashboard.example.com` for the frontend.
        80
        81    In the guide about [deployment](deployment.md) you can read about Traefik, the configured proxy. That's the component in charge of transmitting traffic to each service based on the subdomain.
        82
        83    If you want to test that it's all working locally, you can edit the local `.env` file, and change:
        84
        85    ```dotenv
        86    DOMAIN=localhost.tiangolo.com
        87    ```
        88
        89    That will be used by the Docker Compose files to configure the base domain for the services.
        90
        91    Traefik will use this to transmit traffic at `api.localhost.tiangolo.com` to the backend, and traffic at `dashboard.localhost.tiangolo.com` to the frontend.
        92
        93    The domain `localhost.tiangolo.com` is a special domain that is configured (with all its subdomains) to point to `127.0.0.1`. This way you can use that for your local development.
        94
        95    After you update it, run again:
        96
        97    ```bash
        98    docker compose watch
        99    ```
       100
       101    When deploying, for example in production, the main Traefik is configured outside of the Docker Compose files. For local development, there's an included Traefik in `docker-compose.override.yml`, just to let you test that the domains work as expected, for example with `api.localhost.tiangolo.com` and `dashboard.localhost.tiangolo.com`.
       102
       103    ## Docker Compose files and env vars
       104
       105    There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.
       106
       107    And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker compose` to apply overrides on top of `docker-compose.yml`.
       108
       109    These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.
       110
       111    They also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.
       112
       113    After changing variables, make sure you restart the stack:
       114
       115    ```bash
       116    docker compose watch
       117    ```
       118
       119    ## The .env file
       120
       121    The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.
       122
       123    Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.
       124
       125    One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.
       126
       127    ## Pre-commits and code linting
       128
       129    we are using a tool called [pre-commit](https://pre-commit.com/) for code linting and formatting.
       130
       131    When you install it, it runs right before making a commit in git. This way it ensures that the code is consistent and formatted even before it is committed.
       132
       133    You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.
       134
       135    #### Install pre-commit to run automatically
       136
       137    `pre-commit` is already part of the dependencies of the project, but you could also install it globally if you prefer to, following [the official pre-commit docs](https://pre-commit.com/).
       138
       139    After having the `pre-commit` tool installed and available, you need to "install" it in the local repository, so that it runs automatically before each commit.
       140
       141    Using `uv`, you could do it with:
       142
       143    ```bash
       144    ❯ uv run pre-commit install
       145    pre-commit installed at .git/hooks/pre-commit
       146    ```
       147
       148    Now whenever you try to commit, e.g. with:
       149
       150    ```bash
       151    git commit
       152    ```
       153
       154    ...pre-commit will run and check and format the code you are about to commit, and will ask you to add that code (stage it) with git again before committing.
       155
       156    Then you can `git add` the modified/fixed files again and now you can commit.
       157
       158    #### Running pre-commit hooks manually
       159
       160    you can also run `pre-commit` manually on all the files, you can do it using `uv` with:
       161
       162    ```bash
       163    ❯ uv run pre-commit run --all-files
       164    check for added large files..............................................Passed
       165    check toml...............................................................Passed
       166    check yaml...............................................................Passed
       167    ruff.....................................................................Passed
       168    ruff-format..............................................................Passed
       169    eslint...................................................................Passed
       170    prettier.................................................................Passed
       171    ```
       172
       173    ## URLs
       174
       175    The production or staging URLs would use these same paths, but with your own domain.
       176
       177    ### Development URLs
       178
       179    Development URLs, for local development.
       180
       181    Frontend: http://localhost:5173
       182
       183    Backend: http://localhost:8000
       184
       185    Automatic Interactive Docs (Swagger UI): http://localhost:8000/docs
       186
       187    Automatic Alternative Docs (ReDoc): http://localhost:8000/redoc
       188
       189    Adminer: http://localhost:8080
       190
       191    Traefik UI: http://localhost:8090
       192
       193    MailCatcher: http://localhost:1080
       194
       195    ### Development URLs with `localhost.tiangolo.com` Configured
       196
       197    Development URLs, for local development.
       198
       199    Frontend: http://dashboard.localhost.tiangolo.com
       200
       201    Backend: http://api.localhost.tiangolo.com
       202
       203    Automatic Interactive Docs (Swagger UI): http://api.localhost.tiangolo.com/docs
       204
       205    Automatic Alternative Docs (ReDoc): http://api.localhost.tiangolo.com/redoc
       206
       207    Adminer: http://localhost.tiangolo.com:8080
       208
       209    Traefik UI: http://localhost.tiangolo.com:8090
       210
       211    MailCatcher: http://localhost.tiangolo.com:1080
    FILE docker-compose.yml
         1    services:
         2
         3      db:
         4        image: postgres:12
         5        restart: always
         6        healthcheck:
         7          test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
         8          interval: 10s
         9          retries: 5
        10          start_period: 30s
        11          timeout: 10s
        12        volumes:
        13          - app-db-data:/var/lib/postgresql/data/pgdata
        14        env_file:
        15          - .env
        16        environment:
        17          - PGDATA=/var/lib/postgresql/data/pgdata
        18          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
        19          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
        20          - POSTGRES_DB=${POSTGRES_DB?Variable not set}
        21
        22      adminer:
        23        image: adminer
        24        restart: always
        25        networks:
        26          - traefik-public
        27          - default
        28        depends_on:
        29          - db
        30        environment:
        31          - ADMINER_DESIGN=pepa-linha-dark
        32        labels:
        33          - traefik.enable=true
        34          - traefik.docker.network=traefik-public
        35          - traefik.constraint-label=traefik-public
        36          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.rule=Host(`adminer.${DOMAIN?Variable not set}`)
        37          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.entrypoints=http
        38          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.middlewares=https-redirect
        39          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.rule=Host(`adminer.${DOMAIN?Variable not set}`)
        40          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.entrypoints=https
        41          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.tls=true
        42          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.tls.certresolver=le
        43          - traefik.http.services.${STACK_NAME?Variable not set}-adminer.loadbalancer.server.port=8080
        44
        45      prestart:
        46        image: '${DOCKER_IMAGE_BACKEND?Variable not set}:${TAG-latest}'
        47        build:
        48          context: ./backend
        49        networks:
        50          - traefik-public
        51          - default
        52        depends_on:
        53          db:
        54            condition: service_healthy
        55            restart: true
        56        command: bash scripts/prestart.sh
        57        env_file:
        58          - .env
        59        environment:
        60          - DOMAIN=${DOMAIN}
        61          - FRONTEND_HOST=${FRONTEND_HOST?Variable not set}
        62          - ENVIRONMENT=${ENVIRONMENT}
        63          - BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS}
        64          - SECRET_KEY=${SECRET_KEY?Variable not set}
        65          - FIRST_SUPERUSER=${FIRST_SUPERUSER?Variable not set}
        66          - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD?Variable not set}
        67          - SMTP_HOST=${SMTP_HOST}
        68          - SMTP_USER=${SMTP_USER}
        69          - SMTP_PASSWORD=${SMTP_PASSWORD}
        70          - EMAILS_FROM_EMAIL=${EMAILS_FROM_EMAIL}
        71          - POSTGRES_SERVER=db
        72          - POSTGRES_PORT=${POSTGRES_PORT}
        73          - POSTGRES_DB=${POSTGRES_DB}
        74          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
        75          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
        76          - SENTRY_DSN=${SENTRY_DSN}
        77
        78      backend:
        79        image: '${DOCKER_IMAGE_BACKEND?Variable not set}:${TAG-latest}'
        80        restart: always
        81        networks:
        82          - traefik-public
        83          - default
        84        depends_on:
        85          db:
        86            condition: service_healthy
        87            restart: true
        88          prestart:
        89            condition: service_completed_successfully
        90        env_file:
        91          - .env
        92        environment:
        93          - DOMAIN=${DOMAIN}
        94          - FRONTEND_HOST=${FRONTEND_HOST?Variable not set}
        95          - ENVIRONMENT=${ENVIRONMENT}
        96          - BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS}
        97          - SECRET_KEY=${SECRET_KEY?Variable not set}
        98          - FIRST_SUPERUSER=${FIRST_SUPERUSER?Variable not set}
        99          - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD?Variable not set}
       100          - SMTP_HOST=${SMTP_HOST}
       101          - SMTP_USER=${SMTP_USER}
       102          - SMTP_PASSWORD=${SMTP_PASSWORD}
       103          - EMAILS_FROM_EMAIL=${EMAILS_FROM_EMAIL}
       104          - POSTGRES_SERVER=db
       105          - POSTGRES_PORT=${POSTGRES_PORT}
       106          - POSTGRES_DB=${POSTGRES_DB}
       107          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
       108          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
       109          - SENTRY_DSN=${SENTRY_DSN}
       110
       111        healthcheck:
       112          test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/utils/health-check/"]
       113          interval: 10s
       114          timeout: 5s
       115          retries: 5
       116
       117        build:
       118          context: ./backend
       119        labels:
       120          - traefik.enable=true
       121          - traefik.docker.network=traefik-public
       122          - traefik.constraint-label=traefik-public
       123
       124          - traefik.http.services.${STACK_NAME?Variable not set}-backend.loadbalancer.server.port=8000
       125
       126          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.rule=Host(`api.${DOMAIN?Variable not set}`)
       127          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.entrypoints=http
       128
       129          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.rule=Host(`api.${DOMAIN?Variable not set}`)
       130          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.entrypoints=https
       131          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.tls=true
       132          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.tls.certresolver=le
       133
       134          # Enable redirection for HTTP and HTTPS
       135          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.middlewares=https-redirect
       136
       137      frontend:
       138        image: '${DOCKER_IMAGE_FRONTEND?Variable not set}:${TAG-latest}'
       139        restart: always
       140        networks:
       141          - traefik-public
       142          - default
       143        build:
       144          context: ./frontend
       145          args:
       146            - VITE_API_URL=https://api.${DOMAIN?Variable not set}
       147            - NODE_ENV=production
       148        labels:
       149          - traefik.enable=true
       150          - traefik.docker.network=traefik-public
       151          - traefik.constraint-label=traefik-public
       152
       153          - traefik.http.services.${STACK_NAME?Variable not set}-frontend.loadbalancer.server.port=80
       154
       155          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-http.rule=Host(`dashboard.${DOMAIN?Variable not set}`)
       156          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-http.entrypoints=http
       157
       158          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-https.rule=Host(`dashboard.${DOMAIN?Variable not set}`)
       159          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-https.entrypoints=https
       160          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-https.tls=true
       161          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-https.tls.certresolver=le
       162
       163          # Enable redirection for HTTP and HTTPS
       164          - traefik.http.routers.${STACK_NAME?Variable not set}-frontend-http.middlewares=https-redirect
       165    volumes:
       166      app-db-data:
       167
       168    networks:
       169      traefik-public:
       170        # Allow setting it to false for testing
       171        external: true
    FILE docker-compose.override.yml
         1    services:
         2
         3      # Local services are available on their ports, but also available on:
         4      # http://api.localhost.tiangolo.com: backend
         5      # http://dashboard.localhost.tiangolo.com: frontend
         6      # etc. To enable it, update .env, set:
         7      # DOMAIN=localhost.tiangolo.com
         8      proxy:
         9        image: traefik:3.0
        10        volumes:
        11          - /var/run/docker.sock:/var/run/docker.sock
        12        ports:
        13          - "80:80"
        14          - "8090:8080"
        15        # Duplicate the command from docker-compose.yml to add --api.insecure=true
        16        command:
        17          # Enable Docker in Traefik, so that it reads labels from Docker services
        18          - --providers.docker
        19          # Add a constraint to only use services with the label for this stack
        20          - --providers.docker.constraints=Label(`traefik.constraint-label`, `traefik-public`)
        21          # Do not expose all Docker services, only the ones explicitly exposed
        22          - --providers.docker.exposedbydefault=false
        23          # Create an entrypoint "http" listening on port 80
        24          - --entrypoints.http.address=:80
        25          # Create an entrypoint "https" listening on port 443
        26          - --entrypoints.https.address=:443
        27          # Enable the access log, with HTTP requests
        28          - --accesslog
        29          # Enable the Traefik log, for configurations and errors
        30          - --log
        31          # Enable debug logging for local development
        32          - --log.level=DEBUG
        33          # Enable the Dashboard and API
        34          - --api
        35          # Enable the Dashboard and API in insecure mode for local development
        36          - --api.insecure=true
        37        labels:
        38          # Enable Traefik for this service, to make it available in the public network
        39          - traefik.enable=true
        40          - traefik.constraint-label=traefik-public
        41          # Dummy https-redirect middleware that doesn't really redirect, only to
        42          # allow running it locally
        43          - traefik.http.middlewares.https-redirect.contenttype.autodetect=false
        44        networks:
        45          - traefik-public
        46          - default
        47
        48      db:
        49        restart: "no"
        50        ports:
        51          - "5432:5432"
        52
        53      adminer:
        54        restart: "no"
        55        ports:
        56          - "8080:8080"
        57
        58      backend:
        59        restart: "no"
        60        ports:
        61          - "8000:8000"
        62        build:
        63          context: ./backend
        64        # command: sleep infinity  # Infinite loop to keep container alive doing nothing
        65        command:
        66          - fastapi
        67          - run
        68          - --reload
        69          - "app/main.py"
        70        develop:
        71          watch:
        72            - path: ./backend
        73              action: sync
        74              target: /app
        75              ignore:
        76                - ./backend/.venv
        77                - .venv
        78            - path: ./backend/pyproject.toml
        79              action: rebuild
        80        # TODO: remove once coverage is done locally
        81        volumes:
        82          - ./backend/htmlcov:/app/htmlcov
        83        environment:
        84          SMTP_HOST: "mailcatcher"
        85          SMTP_PORT: "1025"
        86          SMTP_TLS: "false"
        87          EMAILS_FROM_EMAIL: "noreply@example.com"
        88
        89      mailcatcher:
        90        image: schickling/mailcatcher
        91        ports:
        92          - "1080:1080"
        93          - "1025:1025"
        94
        95      frontend:
        96        restart: "no"
        97        ports:
        98          - "5173:80"
        99        build:
       100          context: ./frontend
       101          args:
       102            - VITE_API_URL=http://localhost:8000
       103            - NODE_ENV=development
       104
       105      playwright:
       106        build:
       107          context: ./frontend
       108          dockerfile: Dockerfile.playwright
       109          args:
       110            - VITE_API_URL=http://backend:8000
       111            - NODE_ENV=production
       112        ipc: host
       113        depends_on:
       114          - backend
       115          - mailcatcher
       116        env_file:
       117          - .env
       118        environment:
       119          - VITE_API_URL=http://backend:8000
       120          - MAILCATCHER_HOST=http://mailcatcher:1080
       121          # For the reports when run locally
       122          - PLAYWRIGHT_HTML_HOST=0.0.0.0
       123          - CI=${CI}
       124        volumes:
       125          - ./frontend/blob-report:/app/blob-report
       126          - ./frontend/test-results:/app/test-results
       127        ports:
       128          - 9323:9323
       129
       130    networks:
       131      traefik-public:
       132        # For local dev, don't expect an external Traefik network
       133        external: false
    FILE docker-compose.traefik.yml
         1    services:
         2      traefik:
         3        image: traefik:3.0
         4        ports:
         5          # Listen on port 80, default for HTTP, necessary to redirect to HTTPS
         6          - 80:80
         7          # Listen on port 443, default for HTTPS
         8          - 443:443
         9        restart: always
        10        labels:
        11          # Enable Traefik for this service, to make it available in the public network
        12          - traefik.enable=true
        13          # Use the traefik-public network (declared below)
        14          - traefik.docker.network=traefik-public
        15          # Define the port inside of the Docker service to use
        16          - traefik.http.services.traefik-dashboard.loadbalancer.server.port=8080
        17          # Make Traefik use this domain (from an environment variable) in HTTP
        18          - traefik.http.routers.traefik-dashboard-http.entrypoints=http
        19          - traefik.http.routers.traefik-dashboard-http.rule=Host(`traefik.${DOMAIN?Variable not set}`)
        20          # traefik-https the actual router using HTTPS
        21          - traefik.http.routers.traefik-dashboard-https.entrypoints=https
        22          - traefik.http.routers.traefik-dashboard-https.rule=Host(`traefik.${DOMAIN?Variable not set}`)
        23          - traefik.http.routers.traefik-dashboard-https.tls=true
        24          # Use the "le" (Let's Encrypt) resolver created below
        25          - traefik.http.routers.traefik-dashboard-https.tls.certresolver=le
        26          # Use the special Traefik service api@internal with the web UI/Dashboard
        27          - traefik.http.routers.traefik-dashboard-https.service=api@internal
        28          # https-redirect middleware to redirect HTTP to HTTPS
        29          - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
        30          - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
        31          # traefik-http set up only to use the middleware to redirect to https
        32          - traefik.http.routers.traefik-dashboard-http.middlewares=https-redirect
        33          # admin-auth middleware with HTTP Basic auth
        34          # Using the environment variables USERNAME and HASHED_PASSWORD
        35          - traefik.http.middlewares.admin-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}
        36          # Enable HTTP Basic auth, using the middleware created above
        37          - traefik.http.routers.traefik-dashboard-https.middlewares=admin-auth
        38        volumes:
        39          # Add Docker as a mounted volume, so that Traefik can read the labels of other services
        40          - /var/run/docker.sock:/var/run/docker.sock:ro
        41          # Mount the volume to store the certificates
        42          - traefik-public-certificates:/certificates
        43        command:
        44          # Enable Docker in Traefik, so that it reads labels from Docker services
        45          - --providers.docker
        46          # Do not expose all Docker services, only the ones explicitly exposed
        47          - --providers.docker.exposedbydefault=false
        48          # Create an entrypoint "http" listening on port 80
        49          - --entrypoints.http.address=:80
        50          # Create an entrypoint "https" listening on port 443
        51          - --entrypoints.https.address=:443
        52          # Create the certificate resolver "le" for Let's Encrypt, uses the environment variable EMAIL
        53          - --certificatesresolvers.le.acme.email=${EMAIL?Variable not set}
        54          # Store the Let's Encrypt certificates in the mounted volume
        55          - --certificatesresolvers.le.acme.storage=/certificates/acme.json
        56          # Use the TLS Challenge for Let's Encrypt
        57          - --certificatesresolvers.le.acme.tlschallenge=true
        58          # Enable the access log, with HTTP requests
        59          - --accesslog
        60          # Enable the Traefik log, for configurations and errors
        61          - --log
        62          # Enable the Dashboard and API
        63          - --api
        64        networks:
        65          # Use the public network created to be shared between Traefik and
        66          # any other service that needs to be publicly available with HTTPS
        67          - traefik-public
        68
        69    volumes:
        70      # Create a volume to store the certificates, even if the container is recreated
        71      traefik-public-certificates:
        72
        73    networks:
        74      # Use the previously created public network "traefik-public", shared with other
        75      # services that need to be publicly available via this Traefik
        76      traefik-public:
        77        external: true
    FILE .github/workflows/test-backend.yml
         1    name: Test Backend
         2
         3    on:
         4      push:
         5        branches:
         6          - master
         7      pull_request:
         8        types:
         9          - opened
        10          - synchronize
        11
        12    jobs:
        13      test-backend:
        14        runs-on: ubuntu-latest
        15        steps:
        16          - name: Checkout
        17            uses: actions/checkout@v4
        18          - name: Set up Python
        19            uses: actions/setup-python@v5
        20            with:
        21              python-version: "3.10"
        22          - name: Install uv
        23            uses: astral-sh/setup-uv@v5
        24            with:
        25              version: "0.4.15"
        26              enable-cache: true
        27          - run: docker compose down -v --remove-orphans
        28          - run: docker compose up -d db mailcatcher
        29          - name: Migrate DB
        30            run: uv run bash scripts/prestart.sh
        31            working-directory: backend
        32          - name: Run tests
        33            run: uv run bash scripts/tests-start.sh "Coverage for ${{ github.sha }}"
        34            working-directory: backend
        35          - run: docker compose down -v --remove-orphans
        36          - name: Store coverage files
        37            uses: actions/upload-artifact@v4
        38            with:
        39              name: coverage-html
        40              path: backend/htmlcov
        41              include-hidden-files: true
    FILE .github/workflows/lint-backend.yml
         1    name: Lint Backend
         2
         3    on:
         4      push:
         5        branches:
         6          - master
         7      pull_request:
         8        types:
         9          - opened
        10          - synchronize
        11
        12    jobs:
        13      lint-backend:
        14        runs-on: ubuntu-latest
        15        steps:
        16          - name: Checkout
        17            uses: actions/checkout@v4
        18          - name: Set up Python
        19            uses: actions/setup-python@v5
        20            with:
        21              python-version: "3.10"
        22          - name: Install uv
        23            uses: astral-sh/setup-uv@v5
        24            with:
        25              version: "0.4.15"
        26              enable-cache: true
        27          - run: uv run bash scripts/lint.sh
        28            working-directory: backend
    FILE .github/workflows/playwright.yml
         1    name: Playwright Tests
         2
         3    on:
         4      push:
         5        branches:
         6        - master
         7      pull_request:
         8        types:
         9        - opened
        10        - synchronize
        11      workflow_dispatch:
        12        inputs:
        13          debug_enabled:
        14            description: 'Run the build with tmate debugging enabled (https://github.com/marketplace/actions/debugging-with-tmate)'
        15            required: false
        16            default: 'false'
        17
        18    jobs:
        19      changes:
        20        runs-on: ubuntu-latest
        21        # Set job outputs to values from filter step
        22        outputs:
        23          changed: ${{ steps.filter.outputs.changed }}
        24        steps:
        25        - uses: actions/checkout@v4
        26        # For pull requests it's not necessary to checkout the code but for the main branch it is
        27        - uses: dorny/paths-filter@v3
        28          id: filter
        29          with:
        30            filters: |
        31              changed:
        32                - backend/**
        33                - frontend/**
        34                - .env
        35                - docker-compose*.yml
        36                - .github/workflows/playwright.yml
        37
        38      test-playwright:
        39        needs:
        40          - changes
        41        if: ${{ needs.changes.outputs.changed == 'true' }}
        42        timeout-minutes: 60
        43        runs-on: ubuntu-latest
        44        strategy:
        45          matrix:
        46            shardIndex: [1, 2, 3, 4]
        47            shardTotal: [4]
        48          fail-fast: false
        49        steps:
        50        - uses: actions/checkout@v4
        51        - uses: actions/setup-node@v4
        52          with:
        53            node-version: lts/*
        54        - uses: actions/setup-python@v5
        55          with:
        56            python-version: '3.10'
        57        - name: Setup tmate session
        58          uses: mxschmitt/action-tmate@v3
        59          if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.debug_enabled == 'true' }}
        60          with:
        61            limit-access-to-actor: true
        62        - name: Install uv
        63          uses: astral-sh/setup-uv@v5
        64          with:
        65            version: "0.4.15"
        66            enable-cache: true
        67        - run: uv sync
        68          working-directory: backend
        69        - run: npm ci
        70          working-directory: frontend
        71        - run: uv run bash scripts/generate-client.sh
        72          env:
        73            VIRTUAL_ENV: backend/.venv
        74        - run: docker compose build
        75        - run: docker compose down -v --remove-orphans
        76        - name: Run Playwright tests
        77          run: docker compose run --rm playwright npx playwright test --fail-on-flaky-tests --trace=retain-on-failure --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
        78        - run: docker compose down -v --remove-orphans
        79        - name: Upload blob report to GitHub Actions Artifacts
        80          if: ${{ !cancelled() }}
        81          uses: actions/upload-artifact@v4
        82          with:
        83            name: blob-report-${{ matrix.shardIndex }}
        84            path: frontend/blob-report
        85            include-hidden-files: true
        86            retention-days: 1
        87
        88      merge-playwright-reports:
        89        needs:
        90          - test-playwright
        91          - changes
        92        # Merge reports after playwright-tests, even if some shards have failed
        93        if: ${{ !cancelled() && needs.changes.outputs.changed == 'true' }}
        94        runs-on: ubuntu-latest
        95        steps:
        96        - uses: actions/checkout@v4
        97        - uses: actions/setup-node@v4
        98          with:
        99            node-version: 20
       100        - name: Install dependencies
       101          run: npm ci
       102          working-directory: frontend
       103        - name: Download blob reports from GitHub Actions Artifacts
       104          uses: actions/download-artifact@v4
       105          with:
       106            path: frontend/all-blob-reports
       107            pattern: blob-report-*
       108            merge-multiple: true
       109        - name: Merge into HTML Report
       110          run: npx playwright merge-reports --reporter html ./all-blob-reports
       111          working-directory: frontend
       112        - name: Upload HTML report
       113          uses: actions/upload-artifact@v4
       114          with:
       115            name: html-report--attempt-${{ github.run_attempt }}
       116            path: frontend/playwright-report
       117            retention-days: 30
       118            include-hidden-files: true
       119
       120      # https://github.com/marketplace/actions/alls-green#why
       121      alls-green-playwright:  # This job does nothing and is only used for the branch protection
       122        if: always()
       123        needs:
       124          - test-playwright
       125        runs-on: ubuntu-latest
       126        steps:
       127          - name: Decide whether the needed jobs succeeded or failed
       128            uses: re-actors/alls-green@release/v1
       129            with:
       130              jobs: ${{ toJSON(needs) }}
       131              allowed-skips: test-playwright
    FILE .github/workflows/test-docker-compose.yml
         1    name: Test Docker Compose
         2
         3    on:
         4      push:
         5        branches:
         6          - master
         7      pull_request:
         8        types:
         9          - opened
        10          - synchronize
        11
        12    jobs:
        13
        14      test-docker-compose:
        15        runs-on: ubuntu-latest
        16        steps:
        17          - name: Checkout
        18            uses: actions/checkout@v4
        19          - run: docker compose build
        20          - run: docker compose down -v --remove-orphans
        21          - run: docker compose up -d --wait backend frontend adminer
        22          - name: Test backend is up
        23            run: curl http://localhost:8000/api/v1/utils/health-check
        24          - name: Test frontend is up
        25            run: curl http://localhost:5173
        26          - run: docker compose down -v --remove-orphans
    FILE .github/dependabot.yml
         1    version: 2
         2    updates:
         3      # GitHub Actions
         4      - package-ecosystem: github-actions
         5        directory: /
         6        schedule:
         7          interval: daily
         8        commit-message:
         9          prefix: ⬆
        10      # Python
        11      - package-ecosystem: pip
        12        directory: /
        13        schedule:
        14          interval: daily
        15        commit-message:
        16          prefix: ⬆
        17      # npm
        18      - package-ecosystem: npm
        19        directory: /
        20        schedule:
        21          interval: daily
        22        commit-message:
        23          prefix: ⬆
        24      # Docker
        25      - package-ecosystem: docker
        26        directory: /
        27        schedule:
        28          interval: weekly
        29        commit-message:
        30          prefix: ⬆
    ✓ • 42ms

## Activity

    $ cat README.md ci/README.md ci/VERIFICATION.md; cat argocd/applicationset.yaml argocd/project.yaml argocd/project-monitoring.yaml infra/kind/kind-config.yaml infra/kind/app-stage-local.yaml infra/kind/project-fastapi.yaml infra/kind/traefik-values.yaml; cat backend/pyproject.toml frontend/package.json frontend/playwright.config.ts
    # Full Stack FastAPI Template

    <a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test/badge.svg" alt="Test"></a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/full-stack-fastapi-template.svg" alt="Coverage"></a>

    ## Technology Stack and Features

    - ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
        - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
        - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
        - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
    - 🚀 [React](https://react.dev) for the frontend.
        - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
        - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
        - 🤖 An automatically generated frontend client.
        - 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
        - 🦇 Dark mode support.
    - 🐋 [Docker Compose](https://www.docker.com) for development and production.
    - 🔒 Secure password hashing by default.
    - 🔑 JWT (JSON Web Token) authentication.
    - 📫 Email based password recovery.
    - ✅ Tests with [Pytest](https://pytest.org).
    - 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
    - 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
    - 🏭 CI/CD using GitHub Flow, Jenkins, GHCR and Argo CD; see [the operating guide](README-jenkins.md).

    ### Dashboard Login

    [![API docs](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Dashboard - Admin

    [![API docs](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Dashboard - Create User

    [![API docs](img/dashboard-create.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Dashboard - Items

    [![API docs](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Dashboard - User Settings

    [![API docs](img/dashboard-user-settings.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Dashboard - Dark Mode

    [![API docs](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ### Interactive API Documentation

    [![API docs](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)

    ## How To Use It

    You can **just fork or clone** this repository and use it as is.

    ✨ It just works. ✨

    ### How to Use a Private Repository

    If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.

    But you can do the following:

    - Create a new GitHub repo, for example `my-full-stack`.
    - Clone this repository manually, set the name with the name of the project you want to use, for example `my-full-stack`:

    ```bash
    git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
    ```

    - Enter into the new directory:

    ```bash
    cd my-full-stack
    ```

    - Set the new origin to your new repository, copy it from the GitHub interface, for example:

    ```bash
    git remote set-url origin git@github.com:octocat/my-full-stack.git
    ```

    - Add this repo as another "remote" to allow you to get updates later:

    ```bash
    git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
    ```

    - Push the code to your new repository:

    ```bash
    git push -u origin master
    ```

    ### Update From the Original Template

    After cloning the repository, and after doing changes, you might want to get the latest changes from this original template.

    - Make sure you added the original repository as a remote, you can check it with:

    ```bash
    git remote -v

    origin    git@github.com:octocat/my-full-stack.git (fetch)
    origin    git@github.com:octocat/my-full-stack.git (push)
    upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)
    upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
    ```

    - Pull the latest changes without merging:

    ```bash
    git pull --no-commit upstream master
    ```

    This will download the latest changes from this template without committing them, that way you can check everything is right before committing.

    - If there are conflicts, solve them in your editor.

    - Once you are done, commit the changes:

    ```bash
    git merge --continue
    ```

    ### Configure

    You can then update configs in the `.env` files to customize your configurations.

    Before deploying it, make sure you change at least the values for:

    - `SECRET_KEY`
    - `FIRST_SUPERUSER_PASSWORD`
    - `POSTGRES_PASSWORD`

    You can (and should) pass these as environment variables from secrets.

    Read the [deployment.md](./deployment.md) docs for more details.

    ### Generate Secret Keys

    Some environment variables in the `.env` file have a default value of `changethis`.

    You have to change them with a secret key, to generate secret keys you can run the following command:

    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

    Copy the content and use that as password / secret key. And run that again to generate another secure key.

    ## How To Use It - Alternative With Copier

    This repository also supports generating a new project using [Copier](https://copier.readthedocs.io).

    It will copy all the files, ask you configuration questions, and update the `.env` files with your answers.

    ### Install Copier

    You can install Copier with:

    ```bash
    pip install copier
    ```

    Or better, if you have [`pipx`](https://pipx.pypa.io/), you can run it with:

    ```bash
    pipx install copier
    ```

    **Note**: If you have `pipx`, installing copier is optional, you could run it directly.

    ### Generate a Project With Copier

    Decide a name for your new project's directory, you will use it below. For example, `my-awesome-project`.

    Go to the directory that will be the parent of your project, and run the command with your project's name:

    ```bash
    copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
    ```

    If you have `pipx` and you didn't install `copier`, you can run it directly:

    ```bash
    pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
    ```

    **Note** the `--trust` option is necessary to be able to execute a [post-creation script](https://github.com/fastapi/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py) that updates your `.env` files.

    ### Input Variables

    Copier will ask you for some data, you might want to have at hand before generating the project.

    But don't worry, you can just update any of that in the `.env` files afterwards.

    The input variables, with their default values (some auto generated) are:

    - `project_name`: (default: `"FastAPI Project"`) The name of the project, shown to API users (in .env).
    - `stack_name`: (default: `"fastapi-project"`) The name of the stack used for Docker Compose labels and project name (no spaces, no periods) (in .env).
    - `secret_key`: (default: `"changethis"`) The secret key for the project, used for security, stored in .env, you can generate one with the method above.
    - `first_superuser`: (default: `"admin@example.com"`) The email of the first superuser (in .env).
    - `first_superuser_password`: (default: `"changethis"`) The password of the first superuser (in .env).
    - `smtp_host`: (default: "") The SMTP server host to send emails, you can set it later in .env.
    - `smtp_user`: (default: "") The SMTP server user to send emails, you can set it later in .env.
    - `smtp_password`: (default: "") The SMTP server password to send emails, you can set it later in .env.
    - `emails_from_email`: (default: `"info@example.com"`) The email account to send emails from, you can set it later in .env.
    - `postgres_password`: (default: `"changethis"`) The password for the PostgreSQL database, stored in .env, you can generate one with the method above.
    - `sentry_dsn`: (default: "") The DSN for Sentry, if you are using it, you can set it later in .env.

    ## Backend Development

    Backend docs: [backend/README.md](./backend/README.md).

    ## Frontend Development

    Frontend docs: [frontend/README.md](./frontend/README.md).

    ## Jenkins CI

    Jenkins setup, local access, pipeline stages, and troubleshooting: [README-jenkins.md](./README-jenkins.md).

    ## Deployment

    Deployment docs: [deployment.md](./deployment.md).

    ## Kubernetes GitOps

    Active manifests live in `deploy/base` and `deploy/overlays/{dev,stage,prod}`.
    Argo CD owns application deployment; Jenkins builds images and modifies Git.
    See [Jenkins setup and release procedures](README-jenkins.md) and
    [Argo bootstrap and rollback](deployment.md).

    `k8s/` is retained for historical/local reference. Do not apply it alongside the
    active GitOps applications. Its old sealed secrets belong to their original
    namespace/cluster. Production uses externally provisioned secrets.
    # CI implementation

    See [the operating guide](../README-jenkins.md). Scripts in this directory are
    executed by Jenkins; only the trusted promotion job receives write credentials.
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
    apiVersion: argoproj.io/v1alpha1
    kind: ApplicationSet
    metadata:
      name: fastapi
      namespace: argocd
    spec:
      generators:
        - list:
            elements:
              - environment: dev
              - environment: stage
              - environment: prod
      template:
        metadata:
          name: 'app-{{environment}}'
        spec:
          project: fastapi
          source:
            repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
            targetRevision: main
            path: 'deploy/overlays/{{environment}}'
          destination:
            server: https://kubernetes.default.svc
            namespace: 'app-{{environment}}'
          syncPolicy:
            automated:
              prune: true
              selfHeal: true
              allowEmpty: false
            retry:
              limit: 5
              backoff:
                duration: 5s
                factor: 2
                maxDuration: 3m
            syncOptions:
              - PruneLast=true
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: fastapi
      namespace: argocd
    spec:
      description: FastAPI GitOps environments
      sourceRepos:
        - https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
      destinations:
        - server: https://kubernetes.default.svc
          namespace: app-dev
        - server: https://kubernetes.default.svc
          namespace: app-stage
        - server: https://kubernetes.default.svc
          namespace: app-prod
      clusterResourceWhitelist: []
      namespaceResourceWhitelist:
        - group: ''
          kind: ConfigMap
        - group: ''
          kind: Service
        - group: ''
          kind: PersistentVolumeClaim
        - group: apps
          kind: Deployment
        - group: batch
          kind: Job
        - group: networking.k8s.io
          kind: Ingress
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: monitoring
      namespace: argocd
    spec:
      description: DEV/STAGE monitoring platform; no production destinations
      sourceRepos:
      - https://prometheus-community.github.io/helm-charts
      - https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
      destinations:
      - namespace: monitoring
        server: https://kubernetes.default.svc
      clusterResourceWhitelist:
      - group: apiextensions.k8s.io
        kind: CustomResourceDefinition
      - group: rbac.authorization.k8s.io
        kind: ClusterRole
      - group: rbac.authorization.k8s.io
        kind: ClusterRoleBinding
      namespaceResourceWhitelist:
      - group: ''
        kind: ConfigMap
      - group: ''
        kind: Secret
      - group: ''
        kind: Service
      - group: ''
        kind: ServiceAccount
      - group: ''
        kind: PersistentVolumeClaim
      - group: apps
        kind: Deployment
      - group: apps
        kind: DaemonSet
      - group: apps
        kind: StatefulSet
      - group: rbac.authorization.k8s.io
        kind: Role
      - group: rbac.authorization.k8s.io
        kind: RoleBinding
      - group: monitoring.coreos.com
        kind: Prometheus
      - group: monitoring.coreos.com
        kind: Alertmanager
      - group: monitoring.coreos.com
        kind: ServiceMonitor
      - group: monitoring.coreos.com
        kind: PodMonitor
      - group: monitoring.coreos.com
        kind: PrometheusRule
    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    name: fastapi-dev
    nodes:
      - role: control-plane
        image: kindest/node:v1.35.8@sha256:07b2536e30b803ed61d1677a79df6115f798ce64c80f9e22f6ed45afd09323c0
        labels:
          ingress-ready: "true"
        extraPortMappings:
          - containerPort: 80
            hostPort: 80
            listenAddress: "127.0.0.1"
            protocol: TCP
          - containerPort: 443
            hostPort: 443
            listenAddress: "127.0.0.1"
            protocol: TCP
    # Local kind HTTP only; standard STAGE overlay retains HTTPS/TLS.
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: app-stage
      namespace: argocd
      annotations:
        argocd.argoproj.io/skip-reconcile: 'true'
    spec:
      project: fastapi
      source:
        repoURL: https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
        targetRevision: main
        path: deploy/overlays/stage
        kustomize:
          patches:
          - target:
              kind: Ingress
              name: app-ingress
            patch: "- op: remove\n  path: /spec/tls\n"
          - target:
              kind: ConfigMap
              name: backend-config
            patch: "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: backend-config\n\
              data:\n  FRONTEND_HOST: http://stage.example.com\n  BACKEND_CORS_ORIGINS:\
              \ http://stage.example.com\n"
      destination:
        server: https://kubernetes.default.svc
        namespace: app-stage
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
          enabled: false
        retry:
          limit: 5
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 3m
        syncOptions:
        - PruneLast=true
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: fastapi
      namespace: argocd
    spec:
      description: FastAPI GitOps environments
      sourceRepos:
      - https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
      destinations:
      - server: https://kubernetes.default.svc
        namespace: app-dev
      - server: https://kubernetes.default.svc
        namespace: app-stage
      clusterResourceWhitelist: []
      namespaceResourceWhitelist:
      - group: ''
        kind: ConfigMap
      - group: ''
        kind: Service
      - group: ''
        kind: PersistentVolumeClaim
      - group: apps
        kind: Deployment
      - group: batch
        kind: Job
      - group: networking.k8s.io
        kind: Ingress
    deployment:
      replicas: 1
    service:
      type: ClusterIP
    ports:
      web:
        hostPort: 80
      websecure:
        hostPort: 443
    metrics:
      prometheus:
        addEntryPointsLabels: true
        addServicesLabels: true
        entryPoint: metrics
    nodeSelector:
      ingress-ready: "true"
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 300m
        memory: 256Mi
    # ClusterIP has no load balancer address; publish the actual local host endpoint.
    providers:
      kubernetesIngress:
        publishedService:
          enabled: false
    additionalArguments:
      - --providers.kubernetesingress.ingressendpoint.ip=127.0.0.1
    # One node binds each host port once; replace without a surge pod.
    updateStrategy:
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 1
        maxSurge: 0
    [project]
    name = "app"
    version = "0.1.0"
    description = ""
    requires-python = ">=3.10,<4.0"
    dependencies = [
        "fastapi[standard]<1.0.0,>=0.114.2",
        "python-multipart<1.0.0,>=0.0.7",
        "email-validator<3.0.0.0,>=2.1.0.post1",
        "passlib[bcrypt]<2.0.0,>=1.7.4",
        "tenacity<9.0.0,>=8.2.3",
        "pydantic>2.0",
        "emails<1.0,>=0.6",
        "jinja2<4.0.0,>=3.1.4",
        "alembic<2.0.0,>=1.12.1",
        "httpx<1.0.0,>=0.25.1",
        "psycopg[binary]<4.0.0,>=3.1.13",
        "sqlmodel<1.0.0,>=0.0.21",
        # Pin bcrypt until passlib supports the latest
        "bcrypt==4.0.1",
        "pydantic-settings<3.0.0,>=2.2.1",
        "sentry-sdk[fastapi]<2.0.0,>=1.40.6",
        "pyjwt<3.0.0,>=2.8.0",
    ]

    [tool.uv]
    dev-dependencies = [
        "pytest<8.0.0,>=7.4.3",
        "mypy<2.0.0,>=1.8.0",
        "ruff<1.0.0,>=0.2.2",
        "pre-commit<4.0.0,>=3.6.2",
        "types-passlib<2.0.0.0,>=1.7.7.20240106",
        "coverage<8.0.0,>=7.4.3",
    ]

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [tool.mypy]
    strict = true
    exclude = ["venv", ".venv", "alembic"]

    [tool.ruff]
    target-version = "py310"
    exclude = ["alembic"]

    [tool.ruff.lint]
    select = [
        "E",  # pycodestyle errors
        "W",  # pycodestyle warnings
        "F",  # pyflakes
        "I",  # isort
        "B",  # flake8-bugbear
        "C4",  # flake8-comprehensions
        "UP",  # pyupgrade
        "ARG001", # unused arguments in functions
    ]
    ignore = [
        "E501",  # line too long, handled by black
        "B008",  # do not perform function calls in argument defaults
        "W191",  # indentation contains tabs
        "B904",  # Allow raising exceptions without from e, for HTTPException
    ]

    [tool.ruff.lint.pyupgrade]
    # Preserve types, even if a file imports `from __future__ import annotations`.
    keep-runtime-typing = true
    {
      "name": "frontend",
      "private": true,
      "version": "0.0.0",
      "type": "module",
      "scripts": {
        "dev": "vite",
        "build": "tsc -p tsconfig.build.json && vite build",
        "lint": "biome check --apply-unsafe --no-errors-on-unmatched --files-ignore-unknown=true ./",
        "preview": "vite preview",
        "generate-client": "openapi-ts"
      },
      "dependencies": {
        "@chakra-ui/react": "^3.8.0",
        "@emotion/react": "^11.14.0",
        "@tanstack/react-query": "^5.28.14",
        "@tanstack/react-query-devtools": "^5.28.14",
        "@tanstack/react-router": "1.19.1",
        "axios": "1.7.4",
        "form-data": "4.0.0",
        "next-themes": "^0.4.4",
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-error-boundary": "^4.0.13",
        "react-hook-form": "7.49.3",
        "react-icons": "^5.4.0"
      },
      "devDependencies": {
        "@biomejs/biome": "1.6.1",
        "@hey-api/openapi-ts": "^0.57.0",
        "@playwright/test": "^1.45.2",
        "@tanstack/router-devtools": "1.19.1",
        "@tanstack/router-vite-plugin": "1.19.0",
        "@types/node": "^20.10.5",
        "@types/react": "^18.2.37",
        "@types/react-dom": "^18.2.15",
        "@vitejs/plugin-react-swc": "^3.5.0",
        "dotenv": "^16.4.5",
        "typescript": "^5.2.2",
        "vite": "^5.4.14"
      }
    }
    import { defineConfig, devices } from '@playwright/test';
    import 'dotenv/config'

    /**
     * Read environment variables from file.
     * https://github.com/motdotla/dotenv
     */

    /**
     * See https://playwright.dev/docs/test-configuration.
     */
    export default defineConfig({
      testDir: './tests',
      /* Run tests in files in parallel */
      fullyParallel: true,
      /* Fail the build on CI if you accidentally left test.only in the source code. */
      forbidOnly: !!process.env.CI,
      /* Retry on CI only */
      retries: process.env.CI ? 2 : 0,
      /* Opt out of parallel tests on CI. */
      workers: process.env.CI ? 1 : undefined,
      /* Reporter to use. See https://playwright.dev/docs/test-reporters */
      reporter: process.env.CI ? 'blob' : 'html',
      /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
      use: {
        /* Base URL to use in actions like `await page.goto('/')`. */
        baseURL: 'http://localhost:5173',

        /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
        trace: 'on-first-retry',
      },

      /* Configure projects for major browsers */
      projects: [
        { name: 'setup', testMatch: /.*\.setup\.ts/ },

        {
          name: 'chromium',
          use: {
            ...devices['Desktop Chrome'],
            storageState: 'playwright/.auth/user.json',
          },
          dependencies: ['setup'],
        },

        // {
        //   name: 'firefox',
        //   use: {
        //     ...devices['Desktop Firefox'],
        //     storageState: 'playwright/.auth/user.json',
        //   },
        //   dependencies: ['setup'],
        // },

        // {
        //   name: 'webkit',
        //   use: {
        //     ...devices['Desktop Safari'],
        //     storageState: 'playwright/.auth/user.json',
        //   },
        //   dependencies: ['setup'],
        // },

        /* Test against mobile viewports. */
        // {
        //   name: 'Mobile Chrome',
        //   use: { ...devices['Pixel 5'] },
        // },
        // {
        //   name: 'Mobile Safari',
        //   use: { ...devices['iPhone 12'] },
        // },

        /* Test against branded browsers. */
        // {
        //   name: 'Microsoft Edge',
        //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
        // },
        // {
        //   name: 'Google Chrome',
        //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
        // },
      ],

      /* Run your local dev server before starting the tests */
      webServer: {
        command: 'npm run dev',
        url: 'http://localhost:5173',
        reuseExistingServer: !process.env.CI,
      },
    });
    ✓ • 0ms

## Assistant

Der erste wesentliche Befund: Im Repository gibt es keine Terraform-Dateien. Kubernetes und die Jenkins/GitOps-Pipeline sind vorhanden, aber Prod verwendet noch Platzhalter-Images. Außerdem liegen neue Monitoring- und Infrastrukturdateien nur lokal und unversioniert vor; ich unterscheide deshalb zwischen dem aktuellen Arbeitsverzeichnis und einem reproduzierbaren Checkout.

## Activity

    $ cat monitoring/values.yaml monitoring/monitors/*.yaml monitoring/rules/dev-stage.yaml monitoring/kustomization.yaml; cat monitoring/test-alert-rules.py; rg -n '^(#|```)|backup|restore|rollback|Terraform|terraform|approval|protect|stage|prod|mermaid|graph|flowchart' README-jenkins.md deployment.md DEV_SETUP_REPORT.md KIND_MIGRATION_REPORT.md MONITORING_SETUP_REPORT.md MIGRATION_BACKUP_CHECKLIST.md ALERTING_RUNBOOK.md infra/jenkins-host/README.md; cat backend/app/core/config.py backend/app/core/security.py backend/app/api/deps.py backend/app/main.py backend/app/api/main.py backend/app/api/routes/private.py backend/app/api/routes/utils.py backend/app/tests/conftest.py backend/scripts/lint.sh backend/scripts/test.sh
    fullnameOverride: monitoring
    defaultRules:
      create: false
    kubeControllerManager:
      enabled: false
    kubeScheduler:
      enabled: false
    kubeEtcd:
      enabled: false
    kubeProxy:
      enabled: false
    crds:
      enabled: true
      upgradeJob:
        enabled: false
    prometheusOperator:
      admissionWebhooks:
        enabled: false
      tls:
        enabled: false
      resources:
        requests:
          cpu: 40m
          memory: 128Mi
        limits:
          cpu: 200m
          memory: 256Mi
      prometheusConfigReloader:
        resources:
          requests:
            cpu: 5m
            memory: 32Mi
          limits:
            cpu: 100m
            memory: 64Mi
    prometheus:
      ingress:
        enabled: false
      prometheusSpec:
        replicas: 1
        retention: 3d
        retentionSize: 1500MB
        scrapeInterval: 60s
        evaluationInterval: 60s
        resources:
          requests:
            cpu: 100m
            memory: 512Mi
          limits:
            cpu: 500m
            memory: 1536Mi
        serviceMonitorSelectorNilUsesHelmValues: false
        serviceMonitorSelector:
          matchLabels:
            release: monitoring
        serviceMonitorNamespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: monitoring
        podMonitorSelectorNilUsesHelmValues: false
        podMonitorSelector:
          matchLabels:
            release: monitoring
        podMonitorNamespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: monitoring
        ruleSelectorNilUsesHelmValues: false
        ruleSelector:
          matchLabels:
            release: monitoring
        ruleNamespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: monitoring
        storageSpec:
          volumeClaimTemplate:
            metadata:
              annotations:
                argocd.argoproj.io/sync-options: Prune=false,Delete=false
            spec:
              storageClassName: standard
              accessModes:
              - ReadWriteOnce
              resources:
                requests:
                  storage: 2Gi
    alertmanager:
      ingress:
        enabled: false
      config:
        global:
          resolve_timeout: 5m
        route:
          receiver: 'null'
          group_by:
          - alertname
          - namespace
          group_wait: 1m
          group_interval: 5m
          repeat_interval: 12h
        receivers:
        - name: 'null'
      alertmanagerSpec:
        replicas: 1
        resources:
          requests:
            cpu: 20m
            memory: 64Mi
          limits:
            cpu: 100m
            memory: 128Mi
        storage:
          volumeClaimTemplate:
            metadata:
              annotations:
                argocd.argoproj.io/sync-options: Prune=false,Delete=false
            spec:
              storageClassName: standard
              accessModes:
              - ReadWriteOnce
              resources:
                requests:
                  storage: 256Mi
    kube-state-metrics:
      resources:
        requests:
          cpu: 30m
          memory: 64Mi
        limits:
          cpu: 150m
          memory: 128Mi
    prometheus-node-exporter:
      hostNetwork: false
      service:
        enableHostPort: false
      resources:
        requests:
          cpu: 20m
          memory: 32Mi
        limits:
          cpu: 100m
          memory: 64Mi
    grafana:
      replicas: 1
      defaultDashboardsEnabled: false
      ingress:
        enabled: false
      service:
        type: ClusterIP
      resources:
        requests:
          cpu: 50m
          memory: 128Mi
        limits:
          cpu: 300m
          memory: 384Mi
      persistence:
        enabled: false
      # Provision separately; credentials never enter Helm values or Git.
      admin:
        existingSecret: monitoring-grafana-admin
        userKey: admin-user
        passwordKey: admin-password
      grafana.ini:
        auth:
          disable_login_form: false
        auth.anonymous:
          enabled: false
        users:
          allow_sign_up: false
        analytics:
          reporting_enabled: false
          check_for_updates: false
      sidecar:
        resources:
          requests:
            cpu: 10m
            memory: 32Mi
          limits:
            cpu: 100m
            memory: 128Mi
        datasources:
          enabled: false
        dashboards:
          enabled: true
          searchNamespace: monitoring
          skipReload: true
          initDashboards: false
          provider:
            allowUiUpdates: false
            disableDelete: true
            updateIntervalSeconds: 30
      datasources:
        datasources.yaml:
          apiVersion: 1
          datasources:
          - name: Prometheus
            uid: prometheus
            type: prometheus
            url: http://monitoring-prometheus.monitoring.svc.cluster.local:9090
            access: proxy
            isDefault: true
            editable: false
      testFramework:
        enabled: false
    coreDns:
      enabled: false
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-metrics
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-metrics
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-server-metrics
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-server-metrics
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-repo-server
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-repo-server
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    apiVersion: monitoring.coreos.com/v1
    kind: PodMonitor
    metadata:
      name: traefik
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - traefik
      selector:
        matchLabels:
          app.kubernetes.io/name: traefik
          app.kubernetes.io/instance: traefik-traefik
      podMetricsEndpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
      name: dev-stage-platform
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      groups:
      - name: dev-stage-platform
        rules:
        - alert: NodeMemoryPressure
          expr: kube_node_status_condition{condition="MemoryPressure",status="true"} ==
            1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: Node has sustained Kubernetes memory pressure
        - alert: NodeDiskPressure
          expr: kube_node_status_condition{condition="DiskPressure",status="true"} ==
            1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: Node has sustained Kubernetes disk pressure
        - alert: NodeHighCPU
          expr: (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
            > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: Node CPU usage sustained above 85 percent
        - alert: NodeHighMemory
          expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.90
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: Node memory usage sustained above 90 percent
        - alert: ApplicationRestartSpike
          expr: sum by(namespace,pod,container) (increase(kube_pod_container_status_restarts_total{namespace=~"app-dev|app-stage"}[15m]))
            >= 3
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: DEV or STAGE container restarted at least three times in 15 minutes
        - alert: ApplicationDeploymentUnavailable
          expr: kube_deployment_status_replicas_available{namespace=~"app-dev|app-stage"}
            < kube_deployment_spec_replicas{namespace=~"app-dev|app-stage"}
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: DEV or STAGE deployment has fewer available replicas than desired
        - alert: ArgoApplicationUnhealthy
          expr: argocd_app_info{name=~"app-dev|app-stage",health_status!="Healthy"} ==
            1
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: DEV or STAGE Argo Application is unhealthy
        - alert: ArgoApplicationOutOfSync
          expr: argocd_app_info{name=~"app-dev|app-stage",sync_status!="Synced"} == 1
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: DEV or STAGE Argo Application is out of sync
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    namespace: monitoring
    resources:
    - monitors/argocd.yaml
    - monitors/traefik.yaml
    - rules/dev-stage.yaml
    - dashboards/platform.yaml
    #!/usr/bin/env python3
    """Test loaded rules with synthetic samples; never inject alerts or stress workloads.

    Requires a loopback Prometheus forward on 19090 and PyYAML.
    Uses .tools/promtool (copied from the installed image) and matching local rules.
    """
    import json
    import re
    from pathlib import Path
    import subprocess
    import tempfile
    import urllib.request
    import urllib.parse
    import yaml

    rules = yaml.safe_load((Path(__file__).parent / 'rules/dev-stage.yaml').read_text())['spec']['groups'][0]['rules']
    loaded = json.load(urllib.request.urlopen('http://127.0.0.1:19090/api/v1/rules', timeout=20))['data']['groups']
    group = next(g for g in loaded if g['name'] == 'dev-stage-platform')
    for rule in rules:
        live = next(r for r in group['rules'] if r['name'] == rule['alert'])
        canonical = json.load(urllib.request.urlopen('http://127.0.0.1:19090/api/v1/format_query?' + urllib.parse.urlencode({'query': rule['expr']}), timeout=20))['data']
        assert re.sub(r'\s+', '', live['query']) == re.sub(r'\s+', '', canonical) and live['duration'] == {'5m': 300, '10m': 600, '15m': 900}[rule['for']], rule['alert']
        assert live['annotations'] == rule['annotations'] and live['labels'] == rule['labels'], rule['alert']
        assert live['health'] == 'ok' and not live.get('lastError'), rule['alert']

    def sample(metric, labels, values):
        return {'series': metric + '{' + ','.join(f'{k}="{v}"' for k, v in labels.items()) + '}', 'values': values}

    cases = {
        'NodeMemoryPressure': ([sample('kube_node_status_condition', {'node': 'test', 'condition': 'MemoryPressure', 'status': 'true'}, '1+0x24 0+0x25')], {'node': 'test', 'condition': 'MemoryPressure', 'status': 'true'}, 5),
        'NodeDiskPressure': ([sample('kube_node_status_condition', {'node': 'test', 'condition': 'DiskPressure', 'status': 'true'}, '1+0x24 0+0x25')], {'node': 'test', 'condition': 'DiskPressure', 'status': 'true'}, 5),
        'NodeHighCPU': ([sample('node_cpu_seconds_total', {'instance': 'test', 'mode': 'idle'}, '0+5x24 180+60x25')], {'instance': 'test'}, 16),
        'NodeHighMemory': ([sample('node_memory_MemAvailable_bytes', {'instance': 'test'}, '5+0x24 50+0x25'), sample('node_memory_MemTotal_bytes', {'instance': 'test'}, '100+0x50')], {'instance': 'test'}, 15),
        'ApplicationRestartSpike': ([sample('kube_pod_container_status_restarts_total', {'namespace': 'app-dev', 'pod': 'test', 'container': 'backend'}, '0 3+0x49')], {'namespace': 'app-dev', 'pod': 'test', 'container': 'backend'}, 6),
        'ApplicationDeploymentUnavailable': ([sample('kube_deployment_status_replicas_available', {'namespace': 'app-stage', 'deployment': 'backend'}, '0+0x24 1+0x25'), sample('kube_deployment_spec_replicas', {'namespace': 'app-stage', 'deployment': 'backend'}, '1+0x50')], {'namespace': 'app-stage', 'deployment': 'backend'}, 10),
        'ArgoApplicationUnhealthy': ([sample('argocd_app_info', {'name': 'app-dev', 'health_status': 'Degraded', 'sync_status': 'Synced'}, '1+0x24 0+0x25')], {'name': 'app-dev', 'health_status': 'Degraded', 'sync_status': 'Synced'}, 10),
        'ArgoApplicationOutOfSync': ([sample('argocd_app_info', {'name': 'app-stage', 'health_status': 'Healthy', 'sync_status': 'OutOfSync'}, '1+0x24 0+0x25')], {'name': 'app-stage', 'health_status': 'Healthy', 'sync_status': 'OutOfSync'}, 10),
    }
    tests = []
    for rule in rules:
        samples, labels, fires = cases[rule['alert']]
        tests.append({'name': rule['alert'] + ' pending/firing/recovered', 'interval': '1m', 'input_series': samples, 'alert_rule_test': [
            {'eval_time': f'{fires-1}m', 'alertname': rule['alert'], 'exp_alerts': []},
            {'eval_time': f'{fires}m', 'alertname': rule['alert'], 'exp_alerts': [{'exp_labels': {**labels, **rule['labels']}, 'exp_annotations': rule['annotations']}]},
            {'eval_time': '45m', 'alertname': rule['alert'], 'exp_alerts': []},
        ]})
    # Threshold boundaries are healthy: CPU=85%, memory=90%, restarts<3,
    # equal available/desired, normal node conditions and Healthy/Synced apps.
    healthy = [sample('node_cpu_seconds_total', {'instance': 'test', 'mode': 'idle'}, '0+9x50'), sample('node_memory_MemAvailable_bytes', {'instance': 'test'}, '10+0x50'), sample('node_memory_MemTotal_bytes', {'instance': 'test'}, '100+0x50')]
    for condition in ['MemoryPressure', 'DiskPressure']:
        healthy.append(sample('kube_node_status_condition', {'node': 'test', 'condition': condition, 'status': 'true'}, '0+0x50'))
    for ns in ['app-dev', 'app-stage']:
        healthy.extend([sample('kube_pod_container_status_restarts_total', {'namespace': ns, 'pod': 'test', 'container': 'backend'}, '0 2+0x49'), sample('kube_deployment_status_replicas_available', {'namespace': ns, 'deployment': 'backend'}, '1+0x50'), sample('kube_deployment_spec_replicas', {'namespace': ns, 'deployment': 'backend'}, '1+0x50'), sample('argocd_app_info', {'name': ns, 'health_status': 'Healthy', 'sync_status': 'Synced'}, '1+0x50')])
    # Unhealthy synthetic PROD samples must never match application rules.
    healthy.extend([sample('kube_pod_container_status_restarts_total', {'namespace': 'app-prod', 'pod': 'test', 'container': 'backend'}, '0+10x50'), sample('kube_deployment_status_replicas_available', {'namespace': 'app-prod', 'deployment': 'backend'}, '0+0x50'), sample('kube_deployment_spec_replicas', {'namespace': 'app-prod', 'deployment': 'backend'}, '1+0x50'), sample('argocd_app_info', {'name': 'app-prod', 'health_status': 'Degraded', 'sync_status': 'OutOfSync'}, '1+0x50')])
    tests.append({'name': 'Healthy boundaries and environment isolation', 'interval': '1m', 'input_series': healthy, 'alert_rule_test': [{'eval_time': t, 'alertname': r['alert'], 'exp_alerts': []} for r in rules for t in ['6m', '30m']]})
    with tempfile.TemporaryDirectory(prefix='monitoring-alert-tests-') as directory:
        rulefile = Path(directory) / 'rules.yaml'
        rulefile.write_text(yaml.safe_dump({'groups': [{'name': 'dev-stage-platform', 'rules': rules}]}))
        testfile = Path(directory) / 'tests.yaml'
        testfile.write_text(yaml.safe_dump({'rule_files': [str(rulefile)], 'evaluation_interval': '1m', 'tests': tests}))
        promtool = Path(__file__).resolve().parent.parent / '.tools/promtool'
        subprocess.run([str(promtool), 'test', 'rules', str(testfile)], check=True)
    print('Eight live rules match local definitions; pending/firing/recovery and healthy boundary/isolation tests PASS')
    DEV_SETUP_REPORT.md:1:# DEV setup report
    DEV_SETUP_REPORT.md:3:## Live completion update — 2026-10-09 UTC
    DEV_SETUP_REPORT.md:13:- Backend, frontend, PostgreSQL and Adminer: **1/1 ready**, zero restarts in the completion check. Backend has one replica and the explicit one-worker command. Backend/frontend/migration digest pins match the Jenkins-produced pair recorded in DEV promotion.json.
    DEV_SETUP_REPORT.md:18:### Current capacity and remaining limits
    DEV_SETUP_REPORT.md:24:### Commands used for completion
    DEV_SETUP_REPORT.md:40:## Original inspection snapshot — before the merge and secret approval
    DEV_SETUP_REPORT.md:44:No commit, push, Jenkins build/promotion, image upload, stage deployment, or PROD creation was performed.
    DEV_SETUP_REPORT.md:46:## A. What existed before
    DEV_SETUP_REPORT.md:49:- Repository started clean at local commit `11f0b3a`; remote main and Argo stage track `39d2623444c723949afcd3a9843aae835afc1dcd`.
    DEV_SETUP_REPORT.md:50:- `deploy/base` and `deploy/overlays/{dev,stage,prod}` are the active Kustomize manifests. `k8s/` is legacy; Helm manages platform components, not this app's desired state.
    DEV_SETUP_REPORT.md:51:- `app-stage` existed, Synced/Healthy, with ready backend, frontend, PostgreSQL and Adminer pods. Backend uses one worker and one replica.
    DEV_SETUP_REPORT.md:53:- `app-dev` and `app-prod` did not exist. Only Application `app-stage` existed; no ApplicationSet was installed.
    DEV_SETUP_REPORT.md:54:- AppProject `fastapi` already permits `app-dev`, `app-stage`, `app-prod`, this repository and the required workload kinds. It intentionally excludes Secrets and Namespaces.
    DEV_SETUP_REPORT.md:56:- Traefik uses IngressClass `traefik` and a ClusterIP service, ports 80/443; no external service address. Stage host is `stage.example.com`; legacy dev uses `api.example.com` and `dashboard.example.com`.
    DEV_SETUP_REPORT.md:59:## B. Jenkins CI flow
    DEV_SETUP_REPORT.md:65:Main publication automatically updates stage. DEV is a manually selected `MODE=dev` Jenkins run with explicit CI job/build and approval; the approved run automatically writes/pushes DEV Git changes. Production release creates a review branch instead of deploying directly.
    DEV_SETUP_REPORT.md:73:- These are the recorded images running in stage and now selected in local DEV configuration. Registry authentication/expiry was not independently tested with a new DEV pull.
    DEV_SETUP_REPORT.md:75:## C. Argo CD deployment flow
    DEV_SETUP_REPORT.md:77:Prepared `argocd/app-dev.yaml`: project fastapi, same repository as stage, targetRevision main, source path `deploy/overlays/dev`, destination namespace app-dev, same automated prune/selfHeal, retry and PruneLast policy as live stage.
    DEV_SETUP_REPORT.md:80:Do not apply `argocd/applicationset.yaml` for this DEV-only task: it includes PROD and would also manage stage.
    DEV_SETUP_REPORT.md:83:## D. What changed
    DEV_SETUP_REPORT.md:86:- Prepared a DEV-only Argo Application matching stage conventions.
    DEV_SETUP_REPORT.md:87:- Pinned local DEV backend/frontend and migration image to the existing Jenkins-produced stage digests; added matching promotion record.
    DEV_SETUP_REPORT.md:94:## E. Files changed
    DEV_SETUP_REPORT.md:102:## F. Important commands run
    DEV_SETUP_REPORT.md:107:```bash
    DEV_SETUP_REPORT.md:115:cat deploy/overlays/dev/kustomization.yaml deploy/overlays/stage/kustomization.yaml deploy/overlays/stage/promotion.json
    DEV_SETUP_REPORT.md:120:```
    DEV_SETUP_REPORT.md:125:```bash
    DEV_SETUP_REPORT.md:140:```
    DEV_SETUP_REPORT.md:141:Stage Application spec/sync/health were read using jsonpath. Secret names/types were listed using custom-columns. Secret JSON for dev/app-stage was parsed in memory to display names/types/key names only; values were never printed.
    DEV_SETUP_REPORT.md:144:```bash
    DEV_SETUP_REPORT.md:147:```
    DEV_SETUP_REPORT.md:150:```bash
    DEV_SETUP_REPORT.md:153:/tmp/ci-bin/kustomize build deploy/overlays/stage
    DEV_SETUP_REPORT.md:154:/tmp/ci-bin/kustomize build deploy/overlays/prod
    DEV_SETUP_REPORT.md:157:git diff --exit-code HEAD -- deploy/base deploy/overlays/stage deploy/overlays/prod Jenkinsfile Jenkinsfile.promote ci argocd/project.yaml argocd/applicationset.yaml
    DEV_SETUP_REPORT.md:161:```
    DEV_SETUP_REPORT.md:163:Python assertions verified DEV replica/worker settings, exact stage digests, migration image consistency, namespace isolation, absence of plaintext Secrets, `/docs` route, absent TLS requirement, ClusterIP-only services and matching promotion record.
    DEV_SETUP_REPORT.md:164:Python read-only HTTP checks ran via `kubectl exec -n app-stage deployment/backend -- python -c ...` to legacy dev/stage backend services and Traefik with the appropriate Host header. Backend SQLAlchemy SELECT 1 checks ran via `kubectl exec -n dev deployment/backend -- python -c ...` and the equivalent app-stage command. Recent backend logs were captured with `kubectl logs -n <namespace> deployment/backend --tail=30`; only health/error counts were printed.
    DEV_SETUP_REPORT.md:167:```bash
    DEV_SETUP_REPORT.md:172:```
    DEV_SETUP_REPORT.md:177:## G. DEV namespace status
    DEV_SETUP_REPORT.md:193:app-tls is not required for the prepared DEV HTTP setup. ENVIRONMENT remains staging because the app accepts only local/staging/production and staging preserves non-local secret validation.
    DEV_SETUP_REPORT.md:195:## H. Argo CD status
    DEV_SETUP_REPORT.md:197:- app-stage: Synced, Healthy; remote revision 39d2623444c723949afcd3a9843aae835afc1dcd.
    DEV_SETUP_REPORT.md:202:## I. Kubernetes workload status
    DEV_SETUP_REPORT.md:206:Reference stage and legacy dev each have four ready application pods. Stage backend has zero restarts; legacy backend has nine historical restarts and uses about 415Mi, compared with stage one-worker backend about 91Mi.
    DEV_SETUP_REPORT.md:209:## J. Database connectivity result
    DEV_SETUP_REPORT.md:212:Reference stage and legacy dev: backend SQLAlchemy engine connects to its configured DB and executes SELECT 1 successfully, returning 1. This verifies backend-to-database connectivity without exposing credentials.
    DEV_SETUP_REPORT.md:216:## K. Traefik result
    DEV_SETUP_REPORT.md:221:Stage Traefik routing for frontend/health/OpenAPI still works. Stage `/docs` through ingress returns 404, while its backend service `/docs` returns 200; the DEV-only docs route addresses this without modifying stage.
    DEV_SETUP_REPORT.md:224:## L. Endpoint test results
    DEV_SETUP_REPORT.md:234:Recent captured backend logs: 27 successful health-check lines in legacy dev, 26 in stage, zero ERROR lines in either 30-line sample. This is a limited sample, not a full historical log audit.
    DEV_SETUP_REPORT.md:236:## M. Cluster capacity
    DEV_SETUP_REPORT.md:244:| app-stage | 0.50 | 576 | 2.20 | 2176 |
    DEV_SETUP_REPORT.md:254:DEV + stage idle operation appears feasible, but DEV + stage + CI on one node has narrow CPU scheduling headroom and unproven peak memory behavior. A controlled build/load observation is required before calling the combination safe. Legacy dev remains in these totals.
    DEV_SETUP_REPORT.md:257:## N. Jenkins resource impact
    DEV_SETUP_REPORT.md:265:## O. Remaining blockers
    DEV_SETUP_REPORT.md:271:5. Observe capacity during one controlled CI run plus DEV/stage load; monitor pending pods, OOM/restarts, DB probe timeouts and image/archive disk growth.
    DEV_SETUP_REPORT.md:273:Existing issues outside this DEV-only change: legacy dev's missing pull-secret name; stage's missing TLS secret and placeholder DNS; Jenkins broad authenticated-user permissions/legacy deployment RBAC; privileged CI on the application node; previous dependency vulnerabilities; single-node hostPath DB durability. These were not modified or claimed resolved.
    DEV_SETUP_REPORT.md:275:## P. Whether DEV is ready
    DEV_SETUP_REPORT.md:281:## Q. Exact next steps before PROD
    DEV_SETUP_REPORT.md:285:1. Provision the three required app-dev secrets from the approved secret manager/process. Do not copy stage JWT/admin/database secrets by default.
    DEV_SETUP_REPORT.md:301:Before any separate PROD request: resolve CI capacity/isolation and Jenkins permissions; arrange durable storage and tested backups/restores; verify dependency/image vulnerabilities and GitHub branch/tag protections; configure actual PROD secrets/DNS/TLS; retain appropriate worker/resources; tag the tested application SHA with vX.Y.Z, use approved release mode and a reviewed production PR. Runtime release validation must refer to the actual digest pair tested in stage, not a later GitOps-only commit. No PROD actions are part of this task.
    README-jenkins.md:1:# GitHub Flow + Jenkins + GHCR + Argo CD
    README-jenkins.md:8:```mermaid
    README-jenkins.md:9:flowchart TD
    README-jenkins.md:14:  P -->|main only| S[stage overlay Git commit]
    README-jenkins.md:15:  SHA -->|selected successful build + approval| D[dev overlay Git commit]
    README-jenkins.md:16:  T[vX.Y.Z tag] --> R[Trusted release: approval, main ancestry, existing SHA digests, stage history]
    README-jenkins.md:18:  V --> PR[prod review branch and human PR]
    README-jenkins.md:23:  A --> E[app-dev / app-stage / app-prod]
    README-jenkins.md:24:```
    README-jenkins.md:26:## Layout and trust boundary
    README-jenkins.md:31:| `Jenkinsfile.promote` | Separate trusted standalone job loaded ONLY from protected main; successful-build verification, publishing, Git-only promotions |
    README-jenkins.md:38:| `deploy/overlays/stage` | Latest eligible successful main SHA/digests and stage configuration |
    README-jenkins.md:39:| `deploy/overlays/prod` | Reviewed release SHA/digests and production configuration |
    README-jenkins.md:51:## Jenkins setup (required before enabling webhooks)
    README-jenkins.md:76:   with no production workloads or credentials; privileged build containers can
    README-jenkins.md:114:### Credentials and external secrets
    README-jenkins.md:119:| `gitops-write` in trusted | Username/password: separate GitHub account/token, fine-grained token restricted to this repository, Contents read/write (and implicit Metadata read). Writes stage/dev commits and `release/*` branches; does not merge prod. No Actions, administration or package permissions. |
    README-jenkins.md:136:## Environments and immutable artifacts
    README-jenkins.md:146:  and writes its exact SHA/digests to stage. A superseded build cannot roll stage
    README-jenkins.md:151:  gate confirms that the digest pair actually ran successfully in stage. Jenkins
    README-jenkins.md:152:  verifies main ancestry, both SHA images and matching stage Git history, retags
    README-jenkins.md:161:image reference. Release tags may exist before the production PR is approved;
    README-jenkins.md:175:is not HA; arrange backups/restore and appropriate storage before production.
    README-jenkins.md:178:### Recursion and concurrency
    README-jenkins.md:183:promotion commits and reviewed production overlay changes. Mixed source changes
    README-jenkins.md:185:SHA image; release the recorded stage application SHA, not the subsequent bot SHA.
    README-jenkins.md:197:## Release procedure
    README-jenkins.md:199:Tag the actual built application commit recorded by stage. A plain tag of main's
    README-jenkins.md:202:```bash
    README-jenkins.md:205:release_sha=$(python3 -c 'import json; print(json.load(open("deploy/overlays/stage/promotion.json"))["sha"])')
    README-jenkins.md:208:```
    README-jenkins.md:211:only after checking Argo `app-stage` is Healthy/Synced at the recorded digest pair
    README-jenkins.md:214:start release mode manually. Missing images or absent stage history fail closed.
    README-jenkins.md:216:PR and review the exact production digest/config diff. Do not merge an older
    README-jenkins.md:219:## GitHub rules required
    README-jenkins.md:221:Protect main: require PR review, code-owner review, dismiss stale approvals,
    README-jenkins.md:222:require approval of the last push, require the Jenkins CI status and up-to-date
    README-jenkins.md:225:`.github/`, and especially all production-affecting shared base resources. No
    README-jenkins.md:227:Changes to the shared base affect prod immediately after merge and require the
    README-jenkins.md:228:same production review as the prod overlay. Limit ruleset bypass to the dedicated
    README-jenkins.md:229:GitOps machine account needed for automatic stage/dev commits; no human/developer
    README-jenkins.md:232:can change prod or pipeline code. If this residual risk is unacceptable, use a
    README-jenkins.md:233:separate stage/dev GitOps repository or an independently enforcing GitHub App
    README-jenkins.md:244:## Argo CD bootstrap and rollback
    README-jenkins.md:247:rollbacks and legacy-manifest migration. No bootstrap command is run by Jenkins.
    README-jenkins.md:249:## Verification and operating limits
    README-jenkins.md:253:a non-production acceptance exercise covering: PR credential denial, feature
    README-jenkins.md:255:main builds, missing-image release failure, release approval and prod PR review.
    deployment.md:1:# Argo CD deployment
    deployment.md:3:The production path is [GitHub Flow + Jenkins + GHCR + Argo CD](README-jenkins.md).
    deployment.md:4:Jenkins never applies application resources. Git `main`, `deploy/overlays/{dev,stage,prod}`,
    deployment.md:7:local development tool, not this project's production CD system.
    deployment.md:9:## One-time operator bootstrap
    deployment.md:29:   Ordinary users must not override main, image parameters or the production
    deployment.md:31:2. Create `app-dev`, `app-stage`, `app-prod` namespaces outside the ApplicationSet:
    deployment.md:35:   kubectl create namespace app-stage
    deployment.md:36:   kubectl create namespace app-prod
    deployment.md:45:3. Choose the cluster's storage class and capacity, backup/restore and database
    deployment.md:48:   is disabled in Argo annotations; do not assume this substitutes for backups.
    deployment.md:51:4. Complete the Jenkins setup, publish real images, and promote dev/stage. Initial
    deployment.md:54:   through its normal promotion flow; production still needs a reviewed release.
    deployment.md:56:   ApplicationSet through a reviewed Git change, adding prod after approval.
    deployment.md:64:   They define `app-dev`, `app-stage`, `app-prod` against the in-cluster API,
    deployment.md:66:   self-heal **after** Git approval. For an external cluster update both
    deployment.md:68:6. Verify actual Argo sync/health, image digests and migrations in dev/stage before
    deployment.md:69:   production. Set up alerting for failed hooks, sync failures and missing Secrets.
    deployment.md:72:## Rollback
    deployment.md:78:command is needed. A new main build can subsequently advance stage again.
    deployment.md:80:For production, review the rollback PR under the same rules as a release. Avoid
    deployment.md:81:Argo UI rollback/parameter overrides while auto-sync is enabled: Git would restore
    deployment.md:84:approved restore/migration procedure when necessary. Keep old image digests in GHCR.
    deployment.md:86:## References
    MONITORING_SETUP_REPORT.md:1:# Monitoring setup report
    MONITORING_SETUP_REPORT.md:7:## Configuration and GitOps
    MONITORING_SETUP_REPORT.md:15:Existing ServiceMonitor/PodMonitor definitions select Argo Services and Traefik through stable labels/named ports; no pod IP is hardcoded. Monitoring discovery/rules are scoped to the monitoring namespace; workload panels/alerts use app-dev and app-stage, not legacy dev. Prometheus 2Gi and Alertmanager 256Mi local-path PVCs are Bound; pruning/deletion safeguards retained. Grafana storage is ephemeral and dashboards/datasource are reproducible. Local storage is not production durability.
    MONITORING_SETUP_REPORT.md:17:## STAGE prerequisite completed
    MONITORING_SETUP_REPORT.md:23:## Prometheus validation
    MONITORING_SETUP_REPORT.md:33:CPU, memory, deployment replica and restart queries each returned eight workload series with both app-dev/app-stage separated. Node memory, Argo app state, kubelet container data, Traefik reload/response-code/latency metrics returned nonempty results. Fresh benign requests to both application hosts returned 200 and produced finite Traefik p95 latency. Argo application state, sync-rate, reconcile-duration and Git-request dashboard queries returned data.
    MONITORING_SETUP_REPORT.md:35:## Grafana validation
    MONITORING_SETUP_REPORT.md:42:| dev-stage-workloads | 12 (six panels for each namespace) |
    MONITORING_SETUP_REPORT.md:48:## Access, internal only
    MONITORING_SETUP_REPORT.md:52:```bash
    MONITORING_SETUP_REPORT.md:56:```
    MONITORING_SETUP_REPORT.md:60:## Alerts
    MONITORING_SETUP_REPORT.md:62:All eight expected rules loaded and evaluated with health=ok and no lastError: NodeMemoryPressure, NodeDiskPressure, NodeHighCPU, NodeHighMemory, ApplicationRestartSpike, ApplicationDeploymentUnavailable, ArgoApplicationUnhealthy, ArgoApplicationOutOfSync. Alertmanager uses a null receiver; no production/external notification routing.
    MONITORING_SETUP_REPORT.md:64:## Resource comparison
    MONITORING_SETUP_REPORT.md:83:## Repeatable validation and remaining work
    MONITORING_SETUP_REPORT.md:85:```bash
    MONITORING_SETUP_REPORT.md:94:```
    MONITORING_SETUP_REPORT.md:98:FastAPI /metrics still returns 404; no instrumentation added. Future proposal: pinned prometheus-fastapi-instrumentator plus instrument/expose call, backend metrics ServiceMonitor and cardinality/namespace validation. Jenkins metrics remain unavailable: Prometheus plugin/configuration requires separate approval; none installed. Jenkins jobs/plugins/credentials/cloud restrictions and CI peak validation remain work. Final monitoring Git source switch requires approved publication. PROD remains a future separate cluster with durable storage/backups, environment-specific secrets, authentication/DNS/TLS and isolation; no PROD resources created.
    MONITORING_SETUP_REPORT.md:100:## Jenkins recovery inspection update
    MONITORING_SETUP_REPORT.md:102:2026-10-09: Jenkins remains absent/offline. Host values and cached Helm chart were found, but no controlle
    ... command output truncated for persistence ...
    0600 files). These recover partial install settings/chart, not JENKINS_HOME, jobs/history/plugin inventory or encrypted credentials. The remaining Docker volume belongs to current kind and was left untouched. See JENKINS_RECOVERY_REPORT.md.
    KIND_MIGRATION_REPORT.md:1:# kind migration / clean rebuild report
    KIND_MIGRATION_REPORT.md:3:2026-10-09 UTC. Context `kind-fastapi-dev`. **DEV, STAGE and monitoring are Synced/Healthy and validated. Jenkins remains offline/not restored. This local platform is ready for DEV/STAGE work with CI kept offline until its peak budget is validated.** No commit/push, PROD resource, legacy dev namespace or Minikube recreation occurred.
    KIND_MIGRATION_REPORT.md:5:## A. Previous Minikube architecture
    KIND_MIGRATION_REPORT.md:7:Historical reports describe one Docker-driver Minikube node, Kubernetes v1.35.1, Traefik ClusterIP ingress, Argo CD, app-dev/app-stage, and a separate legacy dev namespace. Jenkins ran as `jenkins-0`, a two-container StatefulSet with local PVC. Its exact installer/chart version and controller settings were not preserved in Git. PostgreSQL also used local PVCs. No PROD Application was installed.
    KIND_MIGRATION_REPORT.md:9:## B. Why Minikube was replaced
    KIND_MIGRATION_REPORT.md:11:The host has about 7.8GiB RAM, but the old Minikube Docker/cgroup limit was only 3GiB. Kubernetes advertised host-like memory, obscuring that limit. Monitoring rollout produced capacity/readiness problems and was paused. The operator manually deleted Minikube before this rebuild; the old live state is gone.
    KIND_MIGRATION_REPORT.md:13:## C. Why kind was chosen
    KIND_MIGRATION_REPORT.md:15:A reproducible Docker-based local cluster matches this development workflow. One node avoids extra kubelet/container/control-plane overhead and leaves more RAM for workloads and CI. kind itself does not create RAM or guarantee CI peak safety; the corrected memory accounting and omitted legacy workloads matter too.
    KIND_MIGRATION_REPORT.md:17:## D. New kind architecture
    KIND_MIGRATION_REPORT.md:19:Ubuntu host -> one Docker container `fastapi-dev-control-plane` -> Kubernetes v1.35.8, kind networking/CoreDNS/local-path storage, Sealed Secrets, Traefik, Argo CD, metrics-server, and app-dev. app-stage and monitoring are deployed and validated, alongside the unchanged app-dev. Jenkins controller is intended to run outside kind, with current pipelines still using Kubernetes agents. PROD remains on a future separate cluster.
    KIND_MIGRATION_REPORT.md:21:## E. Kind cluster configuration
    KIND_MIGRATION_REPORT.md:29:## F. Files added / modified
    KIND_MIGRATION_REPORT.md:31:- `.gitignore`: private backups/local tools excluded. Existing DEV_SETUP_REPORT.md changes were present before this rebuild and preserved.
    KIND_MIGRATION_REPORT.md:34:- `argocd/app-stage.yaml`: standard stage-only Application. `infra/kind/app-stage-local.yaml`: kind-only HTTP patches; no TLS credential dependency.
    KIND_MIGRATION_REPORT.md:36:- `scripts/recover-dev-secrets.py`, `restore-kind-registry-auth.py`, `verify-kind-app.py`: recovery and read-only validation helpers.
    KIND_MIGRATION_REPORT.md:38:- `scripts/create-stage-secrets.py`: explicit fresh-credential generation, saving ciphertext only. `verify-kind-monitoring.py`: target/query/rule and provisioned dashboard validation.
    KIND_MIGRATION_REPORT.md:43:## G. Sealed Secrets recovery
    KIND_MIGRATION_REPORT.md:45:Found `sealed-secrets-key-backup.yaml` with one private key. Restricted permissions to 0600 and excluded it from Git. Offline backend/database decryption passed. The frontend sealed file is empty, so an earlier zero exit on that file did not prove decryption. Active frontend has no frontend-secret dependency.
    KIND_MIGRATION_REPORT.md:47:Bootstrap normalizes the key Secret metadata and restores only keys to kube-system through memory/stdin before installing controller v0.39.1, then restarts/waits for the controller. Original ciphertext is strict to legacy dev; it cannot simply be renamed. Recovery helper decrypts in memory and reseals specifically for app-dev. Both app-dev SealedSecrets report Synced=True and produced Secrets with matching database passwords. Legacy dev is never created.
    KIND_MIGRATION_REPORT.md:49:Existing host Docker GHCR auth was recovered into ghcr-pull-secret for DEV/STAGE using memory/stdin. Only ghcr.io auth was copied, not unrelated registries. Its original permission scope is not established; replace with a package-reader credential for continued use. Anonymous GHCR access returned 401. Private material never entered scripts/reports/Git; no key/secret values printed. See the backup checklist for future key/Jenkins backup procedures.
    KIND_MIGRATION_REPORT.md:51:## H. DEV restore
    KIND_MIGRATION_REPORT.md:57:## I. STAGE restore
    KIND_MIGRATION_REPORT.md:59:User explicitly authorized new STAGE credentials. Created independent cryptographically random SECRET_KEY, FIRST_SUPERUSER_PASSWORD and POSTGRES_PASSWORD; the database/backend password matches and all differ from DEV. Generated values stayed in memory; only strict namespace-correct SealedSecrets were saved to infra/kind/secrets/app-stage and applied. Existing registry pull credential was retained. SMTP_PASSWORD is optional/unconfigured and was not fabricated.
    KIND_MIGRATION_REPORT.md:63:STAGE backend/database SealedSecrets are Synced=True, both Secrets exist and passwords match. Argo app-stage: Synced/Healthy; last operation Succeeded; remote main revision cb1bb5617741cd5b68d36b9d419b6014226b6751. PostgreSQL/backend/frontend/Adminer are 1/1 Ready, zero restarts. New 1Gi postgres-vol PVC is Bound. Backend remains one replica with `fastapi run --workers 1 app/main.py` and original image digests.
    KIND_MIGRATION_REPORT.md:65:`infra/kind/app-stage-local.yaml` uses Argo source Kustomize patches against the standard deploy/overlays/stage Git path. It removes spec.tls and changes FRONTEND_HOST/BACKEND_CORS_ORIGINS to http://stage.example.com. Standard STAGE overlay/HTTPS design, hostname, existing routing paths and image pins remain unchanged. No fake production certificates or public DNS/TLS were created. STAGE ingress retains /api to backend and / to frontend; /docs is checked directly at the backend, not added to the ingress.
    KIND_MIGRATION_REPORT.md:71:## J. Legacy dev namespace decision
    KIND_MIGRATION_REPORT.md:73:Not recreated. Remaining references are retained legacy k8s examples, old RBAC examples and historical reports. Active desired state is deploy/overlays/dev and deploy/overlays/stage, targeting app-dev/app-stage. Neither current pipeline uses legacy dev; pipelines use jenkins-ci/jenkins-publish. Ciphertext recovery does not require a live dev namespace. No need was established to recreate it.
    KIND_MIGRATION_REPORT.md:75:## K. Traefik setup
    KIND_MIGRATION_REPORT.md:81:## L. Argo CD setup
    KIND_MIGRATION_REPORT.md:85:Applications: app-dev, app-stage and monitoring all active, Synced/Healthy. No ApplicationSet installed, no app-prod Application/namespace. Kind fastapi project permits only app-dev/app-stage; Secrets/Namespaces remain operator-managed. Monitoring uses its existing scoped project. Repository main is accessible without recovered Argo repository credentials.
    KIND_MIGRATION_REPORT.md:87:## M. Jenkins strategy
    KIND_MIGRATION_REPORT.md:90:Jenkins recovery inspection (2026-10-09) found the previous host values file and cached Helm chart 5.9.56/appVersion 2.568.3; private copies are preserved under ignored .migration-backup/jenkins. No old Jenkins home/jobs/credential store was located. Current kind has no Jenkins namespace/release/PVC; host service absent. Recovered values use NodePort and do not contain full JCasC/jobs, so they must not be blindly reapplied. Actual trusted pipeline uses credential ID gitops-app while README lists gitops-write.
    KIND_MIGRATION_REPORT.md:96:No active host Jenkins service/JENKINS_HOME or old archive found. A host controller can use the same pipelines via Kubernetes plugin/cloud credentials, but jobs/plugins/folder restrictions/credentials must be restored or provisioned as described in README-jenkins.md. Do not automatically deploy Jenkins into kind. Controller relocation does not move Kubernetes build agents out of kind.
    KIND_MIGRATION_REPORT.md:98:For a host controller: install a supported Jenkins/Java LTS combination, configure a persistent host JENKINS_HOME, restore the matching encrypted credential files if available, and configure both Kubernetes clouds against kind. Use a dedicated identity with reviewed agent-only RBAC, not the kind cluster-admin kubeconfig. Adapt the existing CI RoleBinding subject to that identity; do not blindly apply its old jenkins/jenkins ServiceAccount subject. Allow in-cluster agents to reach the host controller (Docker kind network gateway or explicit host address, WebSocket preferred), and restrict controller executors/concurrency. Current CI files require separate trust/isolation controls; a privileged BuildKit pod on a shared single node does not provide production isolation. No plugin, job, credential or Jenkins build was created in this rebuild.
    KIND_MIGRATION_REPORT.md:100:## N. Monitoring setup
    KIND_MIGRATION_REPORT.md:110:## O. Prometheus validation
    KIND_MIGRATION_REPORT.md:114:CPU, memory, deployment replica and restart queries returned eight series each with app-dev and app-stage separated. Node memory, Argo application state, kubelet container data, Traefik response-code counters, latency buckets and reload success returned nonempty results. Argo sync-rate/reconciliation/Git-request dashboard queries returned data. Additional benign DEV/STAGE traffic is used to verify finite Traefik p95 latency rather than treating an idle NaN as a measured latency. Exact reusable checks are in scripts/verify-kind-monitoring.py; transcript is ignored .tools/verify-monitoring.log.
    KIND_MIGRATION_REPORT.md:116:## P. Grafana validation
    KIND_MIGRATION_REPORT.md:118:Grafana health/datasource/search APIs returned 200. Prometheus datasource UID prometheus exists. Four dashboards are provisioned: platform-nodes, dev-stage-workloads, gitops-argocd, ingress-traefik. Validated every stored panel expression against Prometheus and through Grafana /api/ds/query, with both DEV and STAGE selections for workload panels: 4 node, 12 workload/namespace, 4 Argo and 4 Traefik checks returned data. This verifies API provisioning/query execution; no manual browser visual review is claimed.
    KIND_MIGRATION_REPORT.md:122:```bash
    KIND_MIGRATION_REPORT.md:125:```
    KIND_MIGRATION_REPORT.md:129:## Q. Alerts
    KIND_MIGRATION_REPORT.md:131:All eight expected alert rules loaded and evaluated with health=ok and no lastError: NodeMemoryPressure, NodeDiskPressure, NodeHighCPU, NodeHighMemory, ApplicationRestartSpike, ApplicationDeploymentUnavailable, ArgoApplicationUnhealthy, ArgoApplicationOutOfSync. Alertmanager null receiver retained; no external/production notification routing.
    KIND_MIGRATION_REPORT.md:133:## R. Resource usage
    KIND_MIGRATION_REPORT.md:157:## S. Remaining gaps
    KIND_MIGRATION_REPORT.md:159:Jenkins home/jobs/plugins/credentials/cloud trust restrictions and representative CI peak budget remain unimplemented. No Jenkins Prometheus plugin installed. FastAPI /metrics still returns 404; application instrumentation was not changed. Local storage remains disposable; protect off-host Sealed Secrets key backups. Future Git publication is needed to replace inline monitoring values with the final multi-source Git Application; no commit/push was performed. Browser appearance, long-running monitoring retention/load, CI isolation and production durability are not validated.
    KIND_MIGRATION_REPORT.md:161:## T. Exact rebuild procedure
    KIND_MIGRATION_REPORT.md:163:Prerequisites: Docker/cgroup v2, kind v0.33.0, compatible kubectl (prefer 1.35.x), Helm, Python3/PyYAML, curl, kubeseal v0.39.1, free localhost ports 80/443, network access. Supply private key backup securely; configure host Docker GHCR access with a package-reader credential. Existing encrypted files are restored, not regenerated on reruns.
    KIND_MIGRATION_REPORT.md:165:```bash
    KIND_MIGRATION_REPORT.md:169:python3 scripts/restore-kind-registry-auth.py
    KIND_MIGRATION_REPORT.md:171:scripts/bootstrap-kind.sh stage
    KIND_MIGRATION_REPORT.md:172:python3 scripts/verify-kind-app.py stage
    KIND_MIGRATION_REPORT.md:177:```
    KIND_MIGRATION_REPORT.md:179:The existing local encrypted STAGE files are already provisioned and remain uncommitted. If starting without those ciphertext files, `python3 scripts/create-stage-secrets.py` is an explicit operator action to create new values; it refuses to overwrite live Secrets and preserves existing complete ciphertext files. SMTP password is optional/unconfigured. STAGE phase uses local HTTP patches, no app-tls required.
    KIND_MIGRATION_REPORT.md:181:CI_DISABLED requires local Jenkins/controller/agents absent; keep builds offline. Once CI is restored, repeat measured peak review and use CI_CAPACITY_VERIFIED=yes only when that review actually passed. Bootstrap checks memory/node conditions; startup watcher requests pause/termination on pressure/errors without deleting data. API outages can prevent pause requests, so verify state after recovery.
    KIND_MIGRATION_REPORT.md:183:After explicit commit/push approval and publication of monitoring files, apply argocd/app-monitoring.yaml to switch to the final Git-backed sources, then verify targets/dashboard data/capacity again. Do not apply it while remote paths are absent. No bootstrap phase creates PROD/legacy dev/Minikube or deletes clusters/PVCs.
    KIND_MIGRATION_REPORT.md:185:## U. Exact commands run
    KIND_MIGRATION_REPORT.md:189:```bash
    KIND_MIGRATION_REPORT.md:190:python3 scripts/create-stage-secrets.py
    KIND_MIGRATION_REPORT.md:191:scripts/bootstrap-kind.sh stage
    KIND_MIGRATION_REPORT.md:192:python3 scripts/verify-kind-app.py stage
    KIND_MIGRATION_REPORT.md:205:```
    KIND_MIGRATION_REPORT.md:207:Recovered key/base/DEV actions and fixed Traefik ingress status/zero-surge rollout are documented in preceding sections. Earlier inspection found Minikube already deleted; it was never recreated. Follow-up stage secret logs were redacted in memory before output. Admin correction resealed only FIRST_SUPERUSER_PASSWORD; Argo retried its hook without deleting data. Monitoring chart 92.2.0 was pulled/rendered locally for preflight; live deployment used Argo, not Helm install. Monitoring validation uses temporary localhost forwards and closes them. Final requested Git/resource/status/report displays were executed. Local diagnostics/capacity JSONs remain ignored under .tools. No registry push, Jenkins build, commit or Git push was run.
    KIND_MIGRATION_REPORT.md:209:## V. Readiness for continued DEV/STAGE work
    KIND_MIGRATION_REPORT.md:213:## W. Exact next steps before PROD
    KIND_MIGRATION_REPORT.md:215:STAGE and local monitoring are now validated. Restore/provision Jenkins trust boundaries and validate CI resource peaks without disturbing DEV/STAGE. For PROD, provision a separate adequately sized cluster, durable storage/backups, reviewed environment-specific secrets, DNS/TLS, ingress/authentication, CI isolation and monitored recovery procedures. Review PROD manifests and create PROD resources only after an explicit separate authorization. The current local bootstrap intentionally has no PROD path.
    ALERTING_RUNBOOK.md:1:# Alerting runbook
    ALERTING_RUNBOOK.md:3:Scope: existing `kind-fastapi-dev` monitoring with DEV and STAGE application alerts. Node alerts cover the shared local node. Rules are in [monitoring/rules/dev-stage.yaml](monitoring/rules/dev-stage.yaml); thresholds and durations were preserved. All eight have severity `warning`.
    ALERTING_RUNBOOK.md:5:## Alert lifecycle and notification limits
    ALERTING_RUNBOOK.md:13:These eight rules do not alert on exporter disappearance, missing applications, TLS expiry, backups or application-specific request errors. The Platform Overview `up` panel requires attention when telemetry fails. FastAPI currently has no native request metrics. Default kube-prometheus rules are disabled. Additional coverage should be a deliberate follow-up rather than assumed to exist.
    ALERTING_RUNBOOK.md:15:## Alerts
    ALERTING_RUNBOOK.md:17:### NodeMemoryPressure
    ALERTING_RUNBOOK.md:19:```promql
    ALERTING_RUNBOOK.md:21:```
    ALERTING_RUNBOOK.md:31:### NodeDiskPressure
    ALERTING_RUNBOOK.md:33:```promql
    ALERTING_RUNBOOK.md:35:```
    ALERTING_RUNBOOK.md:45:### NodeHighCPU
    ALERTING_RUNBOOK.md:47:```promql
    ALERTING_RUNBOOK.md:49:```
    ALERTING_RUNBOOK.md:59:### NodeHighMemory
    ALERTING_RUNBOOK.md:61:```promql
    ALERTING_RUNBOOK.md:63:```
    ALERTING_RUNBOOK.md:73:### ApplicationRestartSpike
    ALERTING_RUNBOOK.md:75:```promql
    ALERTING_RUNBOOK.md:76:sum by(namespace,pod,container) (increase(kube_pod_container_status_restarts_total{namespace=~"app-dev|app-stage"}[15m])) >= 3
    ALERTING_RUNBOOK.md:77:```
    ALERTING_RUNBOOK.md:87:### ApplicationDeploymentUnavailable
    ALERTING_RUNBOOK.md:89:```promql
    ALERTING_RUNBOOK.md:90:kube_deployment_status_replicas_available{namespace=~"app-dev|app-stage"} < kube_deployment_spec_replicas{namespace=~"app-dev|app-stage"}
    ALERTING_RUNBOOK.md:91:```
    ALERTING_RUNBOOK.md:101:### ArgoApplicationUnhealthy
    ALERTING_RUNBOOK.md:103:```promql
    ALERTING_RUNBOOK.md:104:argocd_app_info{name=~"app-dev|app-stage",health_status!="Healthy"} == 1
    ALERTING_RUNBOOK.md:105:```
    ALERTING_RUNBOOK.md:107:Measures / why it matters: Argo app-dev/app-stage health is anything other than Healthy; captures Degraded, Progressing, Missing, Unknown and other nonhealthy states.
    ALERTING_RUNBOOK.md:115:### ArgoApplicationOutOfSync
    ALERTING_RUNBOOK.md:117:```promql
    ALERTING_RUNBOOK.md:118:argocd_app_info{name=~"app-dev|app-stage",sync_status!="Synced"} == 1
    ALERTING_RUNBOOK.md:119:```
    ALERTING_RUNBOOK.md:121:Measures / why it matters: Argo app-dev/app-stage sync state is anything other than Synced; catches drift or comparison problems.
    ALERTING_RUNBOOK.md:129:## Safe investigation commands
    ALERTING_RUNBOOK.md:131:Replace `app-dev` with `app-stage` when indicated by the alert. Replace POD/DEPLOYMENT/NODE with the actual names; do not substitute exporter IPs for node names.
    ALERTING_RUNBOOK.md:133:```bash
    ALERTING_RUNBOOK.md:142:```
    ALERTING_RUNBOOK.md:146:## Inspect and validate alert plumbing
    ALERTING_RUNBOOK.md:150:```bash
    ALERTING_RUNBOOK.md:153:```
    ALERTING_RUNBOOK.md:157:```promql
    ALERTING_RUNBOOK.md:160:```
    ALERTING_RUNBOOK.md:162:The first counts discovered receivers (healthy=1 here; unhealthy=0); restore Service/endpoints/discovery if absent. The second counts failed Prometheus sends (healthy=0; unhealthy=increasing); inspect notification logs and Alertmanager connectivity. Neither establishes external delivery with a null receiver. Full panel/target validation: `python3 scripts/verify-kind-monitoring.py` (close existing forwards first).
    ALERTING_RUNBOOK.md:166:## FastAPI instrumentation assessment — proposal only
    ALERTING_RUNBOOK.md:174:```toml
    ALERTING_RUNBOOK.md:176:```
    ALERTING_RUNBOOK.md:182:```python
    ALERTING_RUNBOOK.md:185:```
    ALERTING_RUNBOOK.md:189:```python
    ALERTING_RUNBOOK.md:198:```
    ALERTING_RUNBOOK.md:204:```yaml
    ALERTING_RUNBOOK.md:208:  name: fastapi-dev-stage
    ALERTING_RUNBOOK.md:214:    matchNames: [app-dev, app-stage]
    ALERTING_RUNBOOK.md:223:```
    ALERTING_RUNBOOK.md:227:Validate in DEV first: disabled flag preserves `/metrics` 404, enabled route returns Prometheus content, OpenAPI generation remains valid, auth/CORS/errors/streaming behavior and existing backend tests pass, request counters/histograms advance after known traffic, route cardinality remains bounded, each replica has an UP target, and CPU/memory/latency overhead fits capacity. Rebuild and deploy the immutable DEV image, then STAGE after validation. Tests should use isolated registries/app construction to avoid duplicate collector registration. Rollback: disable the DEV/STAGE flag or restore prior image and remove/disable its proposed ServiceMonitor; leave existing infrastructure monitoring intact.
    ALERTING_RUNBOOK.md:229:## Validation record
    ALERTING_RUNBOOK.md:234:- All 29 dashboard expressions returned live series; Workloads was checked for both namespaces. Some idle latency series correctly remained NaN; benign DEV/STAGE requests produced finite HTTP entrypoint and all four DEV/STAGE service p95 measurements.
    ALERTING_RUNBOOK.md:238:- Argo monitoring/app-dev/app-stage all Synced/Healthy, operations Succeeded. All six monitoring pods Ready with zero restarts. Dashboard-only change caused the expected Grafana rollout; other monitoring Application spec values were compared before/after and preserved.
    infra/jenkins-host/README.md:1:# Local Jenkins outside kind
    infra/jenkins-host/README.md:16:```bash
    infra/jenkins-host/README.md:21:# Full no-push validation only after reviewing the smoke measurements and margin:
    infra/jenkins-host/README.md:23:```
    infra/jenkins-host/README.md:27:```bash
    infra/jenkins-host/README.md:29:```
    infra/jenkins-host/README.md:33:`host-smoke` is manual and admin-only. `app-ci/main` is disabled by default; the verifier enables it only for a guarded validation and disables it afterwards. Both load the reviewed local pipeline source, because these uncommitted files are not on remote main. Checkout still uses the real public repository main. No branch scans, webhooks or automatic publication are enabled. Do not accept untrusted PR jobs on this shared worker: DinD is privileged, and a persistent worker is not a hostile-code security boundary. `trusted/publish` is a disabled recovery placeholder; restore `ghcr-write`, `gitops-app`, `ci-read` and an isolated trusted execution strategy before converting it to the protected original pipeline.
    infra/jenkins-host/README.md:41:Back up consistently: disable/quiet jobs, wait for completion, stop `host-jenkins`, then archive the entire `host-jenkins-home` with ownership and encryption files using a read-only helper mount. Encrypt and copy off-host; restart the controller afterwards. Preserve `.jenkins-host/secrets` separately and the checked-in configuration/image/plugin locks. Never delete volumes to repair startup. Old Minikube Jenkins history and credentials are unrecovered, not restored by this setup.
    import secrets
    import warnings
    from typing import Annotated, Any, Literal

    from pydantic import (
        AnyUrl,
        BeforeValidator,
        EmailStr,
        HttpUrl,
        PostgresDsn,
        computed_field,
        model_validator,
    )
    from pydantic_core import MultiHostUrl
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from typing_extensions import Self


    def parse_cors(v: Any) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)


    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            # Use top level .env file (one level above ./backend/)
            env_file="../.env",
            env_ignore_empty=True,
            extra="ignore",
        )
        API_V1_STR: str = "/api/v1"
        SECRET_KEY: str = secrets.token_urlsafe(32)
        # 60 minutes * 24 hours * 8 days = 8 days
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
        FRONTEND_HOST: str = "http://localhost:5173"
        ENVIRONMENT: Literal["local", "staging", "production"] = "local"

        BACKEND_CORS_ORIGINS: Annotated[
            list[AnyUrl] | str, BeforeValidator(parse_cors)
        ] = []

        @computed_field  # type: ignore[prop-decorator]
        @property
        def all_cors_origins(self) -> list[str]:
            return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
                self.FRONTEND_HOST
            ]

        PROJECT_NAME: str
        SENTRY_DSN: HttpUrl | None = None
        POSTGRES_SERVER: str
        POSTGRES_PORT: int = 5432
        POSTGRES_USER: str
        POSTGRES_PASSWORD: str = ""
        POSTGRES_DB: str = ""

        @computed_field  # type: ignore[prop-decorator]
        @property
        def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
            return MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )

        SMTP_TLS: bool = True
        SMTP_SSL: bool = False
        SMTP_PORT: int = 587
        SMTP_HOST: str | None = None
        SMTP_USER: str | None = None
        SMTP_PASSWORD: str | None = None
        EMAILS_FROM_EMAIL: EmailStr | None = None
        EMAILS_FROM_NAME: EmailStr | None = None

        @model_validator(mode="after")
        def _set_default_emails_from(self) -> Self:
            if not self.EMAILS_FROM_NAME:
                self.EMAILS_FROM_NAME = self.PROJECT_NAME
            return self

        EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

        @computed_field  # type: ignore[prop-decorator]
        @property
        def emails_enabled(self) -> bool:
            return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

        EMAIL_TEST_USER: EmailStr = "test@example.com"
        FIRST_SUPERUSER: EmailStr
        FIRST_SUPERUSER_PASSWORD: str

        def _check_default_secret(self, var_name: str, value: str | None) -> None:
            if value == "changethis":
                message = (
                    f'The value of {var_name} is "changethis", '
                    "for security, please change it, at least for deployments."
                )
                if self.ENVIRONMENT == "local":
                    warnings.warn(message, stacklevel=1)
                else:
                    raise ValueError(message)

        @model_validator(mode="after")
        def _enforce_non_default_secrets(self) -> Self:
            self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
            self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
            self._check_default_secret(
                "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
            )

            return self


    settings = Settings()  # type: ignore
    from datetime import datetime, timedelta, timezone
    from typing import Any

    import jwt
    from passlib.context import CryptContext

    from app.core.config import settings

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    ALGORITHM = "HS256"


    def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    from collections.abc import Generator
    from typing import Annotated

    import jwt
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from jwt.exceptions import InvalidTokenError
    from pydantic import ValidationError
    from sqlmodel import Session

    from app.core import security
    from app.core.config import settings
    from app.core.db import engine
    from app.models import TokenPayload, User

    reusable_oauth2 = OAuth2PasswordBearer(
        tokenUrl=f"{settings.API_V1_STR}/login/access-token"
    )


    def get_db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session


    SessionDep = Annotated[Session, Depends(get_db)]
    TokenDep = Annotated[str, Depends(reusable_oauth2)]


    def get_current_user(session: SessionDep, token: TokenDep) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (InvalidTokenError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user = session.get(User, token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user


    CurrentUser = Annotated[User, Depends(get_current_user)]


    def get_current_active_superuser(current_user: CurrentUser) -> User:
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )
        return current_user
    import sentry_sdk
    from fastapi import FastAPI
    from fastapi.routing import APIRoute
    from starlette.middleware.cors import CORSMiddleware

    from app.api.main import api_router
    from app.core.config import settings


    def custom_generate_unique_id(route: APIRoute) -> str:
        return f"{route.tags[0]}-{route.name}"


    if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
        sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
    )

    # Set all CORS enabled origins
    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    from fastapi import APIRouter

    from app.api.routes import items, login, private, users, utils
    from app.core.config import settings

    api_router = APIRouter()
    api_router.include_router(login.router)
    api_router.include_router(users.router)
    api_router.include_router(utils.router)
    api_router.include_router(items.router)


    if settings.ENVIRONMENT == "local":
        api_router.include_router(private.router)
    from typing import Any

    from fastapi import APIRouter
    from pydantic import BaseModel

    from app.api.deps import SessionDep
    from app.core.security import get_password_hash
    from app.models import (
        User,
        UserPublic,
    )

    router = APIRouter(tags=["private"], prefix="/private")


    class PrivateUserCreate(BaseModel):
        email: str
        password: str
        full_name: str
        is_verified: bool = False


    @router.post("/users/", response_model=UserPublic)
    def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
        """
        Create a new user.
        """

        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
        )

        session.add(user)
        session.commit()

        return user
    from fastapi import APIRouter, Depends
    from pydantic.networks import EmailStr

    from app.api.deps import get_current_active_superuser
    from app.models import Message
    from app.utils import generate_test_email, send_email

    router = APIRouter(prefix="/utils", tags=["utils"])


    @router.post(
        "/test-email/",
        dependencies=[Depends(get_current_active_superuser)],
        status_code=201,
    )
    def test_email(email_to: EmailStr) -> Message:
        """
        Test emails.
        """
        email_data = generate_test_email(email_to=email_to)
        send_email(
            email_to=email_to,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
        return Message(message="Test email sent")


    @router.get("/health-check/")
    async def health_check() -> bool:
        return True
    from collections.abc import Generator

    import pytest
    from fastapi.testclient import TestClient
    from sqlmodel import Session, delete

    from app.core.config import settings
    from app.core.db import engine, init_db
    from app.main import app
    from app.models import Item, User
    from app.tests.utils.user import authentication_token_from_email
    from app.tests.utils.utils import get_superuser_token_headers


    @pytest.fixture(scope="session", autouse=True)
    def db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            init_db(session)
            yield session
            statement = delete(Item)
            session.execute(statement)
            statement = delete(User)
            session.execute(statement)
            session.commit()


    @pytest.fixture(scope="module")
    def client() -> Generator[TestClient, None, None]:
        with TestClient(app) as c:
            yield c


    @pytest.fixture(scope="module")
    def superuser_token_headers(client: TestClient) -> dict[str, str]:
        return get_superuser_token_headers(client)


    @pytest.fixture(scope="module")
    def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
        return authentication_token_from_email(
            client=client, email=settings.EMAIL_TEST_USER, db=db
        )
    #!/usr/bin/env bash

    set -e
    set -x

    mypy app
    ruff check app
    ruff format app --check
    #!/usr/bin/env bash

    set -e
    set -x

    coverage run --source=app -m pytest
    coverage report --show-missing
    coverage html --title "${@-coverage}"
    ✓ • 151ms

## Activity

    $ command -v terraform docker kubectl kustomize kubeconform helm uv python3 node npm trivy snyk gitleaks actionlint shellcheck; ls -ld backend/.venv frontend/node_modules /tmp/ci-bin /tmp/gitops* 2>/dev/null; git ls-files | wc -l; rg -n --hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/.venv/**' -g '!**/uv.lock' -g '!**/package-lock.json' -g '!**/src/client/**' -g '!.tools/**' -g '!.migration-backup/**' -g '!.jenkins-host/**' 'terraform|trivy|snyk|NetworkPolicy|PodDisruptionBudget|CronJob|VolumeSnapshot|cert-manager|ClusterIssuer|ServiceMonitor|/metrics|mermaid|flowchart|graph TD' .
    /usr/bin/docker
    /usr/bin/kubectl
    /usr/local/bin/helm
    /usr/bin/python3
    drwxrwxr-x   2 root-admin root-admin 4096 Oct  5 08:18 /tmp/ci-bin
    drwxr-xr-x   5 root       root       4096 Oct  3 11:31 backend/.venv
    drwxr-xr-x 145 root       root       4096 Oct  3 11:40 frontend/node_modules
    274
    ./MONITORING_SETUP_REPORT.md:15:Existing ServiceMonitor/PodMonitor definitions select Argo Services and Traefik through stable labels/named ports; no pod IP is hardcoded. Monitoring discovery/rules are scoped to the monitoring namespace; workload panels/alerts use app-dev and app-stage, not legacy dev. Prometheus 2Gi and Alertmanager 256Mi local-path PVCs are Bound; pruning/deletion safeguards retained. Grafana storage is ephemeral and dashboards/datasource are reproducible. Local storage is not production durability.
    ./MONITORING_SETUP_REPORT.md:21:Local STAGE HTTP Application patches remove TLS and change frontend/CORS origin to HTTP; standard HTTPS overlay remains unchanged. No public TLS certificate required. STAGE PostgreSQL/backend/frontend/Adminer are Ready, backend one replica/worker. SELECT 1, DNS, health/OpenAPI/docs, frontend/Adminer and internal/localhost Traefik checks passed (200, except expected backend root and /metrics 404). DEV was preserved.
    ./MONITORING_SETUP_REPORT.md:98:FastAPI /metrics still returns 404; no instrumentation added. Future proposal: pinned prometheus-fastapi-instrumentator plus instrument/expose call, backend metrics ServiceMonitor and cardinality/namespace validation. Jenkins metrics remain unavailable: Prometheus plugin/configuration requires separate approval; none installed. Jenkins jobs/plugins/credentials/cloud restrictions and CI peak validation remain work. Final monitoring Git source switch requires approved publication. PROD remains a future separate cluster with durable storage/backups, environment-specific secrets, authentication/DNS/TLS and isolation; no PROD resources created.
    ./monitoring/bootstrap.py:19:values['prometheus']['additionalServiceMonitors'] = [
    ./monitoring/monitors/argocd.yaml:2:kind: ServiceMonitor
    ./monitoring/monitors/argocd.yaml:17:    path: /metrics
    ./monitoring/monitors/argocd.yaml:22:kind: ServiceMonitor
    ./monitoring/monitors/argocd.yaml:37:    path: /metrics
    ./monitoring/monitors/argocd.yaml:42:kind: ServiceMonitor
    ./monitoring/monitors/argocd.yaml:57:    path: /metrics
    ./monitoring/monitors/traefik.yaml:18:    path: /metrics
    ./argocd/project-monitoring.yaml:47:    kind: ServiceMonitor
    ./scripts/bootstrap-kind.sh:56:  curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://github.com/kubernetes-sigs/metrics-server/releases/download/$METRICS_VERSION/components.yaml" -o "$ROOT/.tools/metrics-server.yaml"
    ./scripts/bootstrap-kind.sh:59:  python3 - "$ROOT/.tools/metrics-server.yaml" <<'PYMETRICS'
    ./scripts/bootstrap-kind.sh:68:  k apply -f "$ROOT/.tools/metrics-server.yaml"
    ./scripts/bootstrap-kind.sh:69:  k rollout status deployment/metrics-server -n kube-system --timeout=180s
    ./DEV_SETUP_REPORT.md:174:Temporary validation/metrics/reference endpoint outputs are under `/tmp/dev-setup-audit`; no credentials are stored there.
    ./scripts/verify-kind-app.py:21:for path,status in [('/',404),('/api/v1/utils/health-check/',200),('/api/v1/openapi.json',200),('/docs',200),('/metrics',404)]:
    ./scripts/capture-kind-capacity.py:16:pods=k('/apis/metrics.k8s.io/v1beta1/pods')['items'];nodes=k('/apis/metrics.k8s.io/v1beta1/nodes')['items']
    ./KIND_MIGRATION_REPORT.md:55:Backend remains one replica with `fastapi run --workers 1 app/main.py`. Existing backend/frontend digest pins remain unchanged. SQLAlchemy SELECT 1 passed; service DNS resolved. Backend health/OpenAPI/docs returned 200; backend `/` returned expected 404 because there is no backend root route. Frontend and Adminer internal roots returned 200. Traefik DEV host root, health, OpenAPI and docs returned 200; localhost HTTP root/health/docs also returned 200 with Host dev.example.com. `/metrics` returned 404.
    ./KIND_MIGRATION_REPORT.md:67:SQLAlchemy SELECT 1 and service DNS passed. Backend root returned expected 404; health/OpenAPI/docs 200; /metrics 404. Frontend/Adminer roots 200. Internal Traefik and localhost STAGE Host-header root/health/OpenAPI each 200. DEV remained Synced/Healthy and was not redeployed.
    ./KIND_MIGRATION_REPORT.md:112:Prometheus /-/ready, /api/v1/targets and /api/v1/rules returned 200. All 16 active scrape targets are UP with no scrape errors: node-exporter, kube-state-metrics, three kubelet endpoints (including cAdvisor/container metrics), Argo controller/server/repo, Traefik, API server, Grafana, Operator and Prometheus/Alertmanager/reloader targets. Stable ServiceMonitor/PodMonitor discovery, no hardcoded pod IPs.
    ./KIND_MIGRATION_REPORT.md:159:Jenkins home/jobs/plugins/credentials/cloud trust restrictions and representative CI peak budget remain unimplemented. No Jenkins Prometheus plugin installed. FastAPI /metrics still returns 404; application instrumentation was not changed. Local storage remains disposable; protect off-host Sealed Secrets key backups. Future Git publication is needed to replace inline monitoring values with the final multi-source Git Application; no commit/push was performed. Browser appearance, long-running monitoring retention/load, CI isolation and production durability are not validated.
    ./ALERTING_RUNBOOK.md:168:No Prometheus dependency/import or route is present in `backend/pyproject.toml` or `backend/app/main.py`; native `/metrics` currently returns 404. Existing pod metrics and Traefik metrics work without application changes, but cannot expose route-template app duration or app-specific business metrics.
    ./ALERTING_RUNBOOK.md:170:A bounded, opt-in middleware is reasonable for DEV/STAGE's current one-worker execution, subject to dependency resolution, tests and overhead measurement. Compatibility is plausible from the declared Starlette/Python constraints; it is not a tested lockfile resolution. The Dockerfile default is **four workers**. A plain process-local registry with four workers would report whichever worker handled each scrape. Keep one worker for this proposal; do not enable it in multiworker environments without a tested multiprocess registry/directory lifecycle. No backend, dependency, lockfile, image, ServiceMonitor or ingress change has been implemented.
    ./ALERTING_RUNBOOK.md:194:        excluded_handlers=[r"^/metrics$", r"^/api/v1/utils/health-check/$"],
    ./ALERTING_RUNBOOK.md:196:        app, endpoint="/metrics", include_in_schema=False
    ./ALERTING_RUNBOOK.md:202:Proposed scraping: avoid altering the shared base Service or public ingress. Add a **new internal-only backend-metrics Service in each DEV/STAGE overlay**, with metadata labels `app: backend-metrics`, selector `app: backend`, port `name: metrics`, `port: 8000`, `targetPort: 8000`. Then add this ServiceMonitor under `monitoring` and include it in the active inline source as well as local Kustomize/bootstrap definitions:
    ./ALERTING_RUNBOOK.md:206:kind: ServiceMonitor
    ./ALERTING_RUNBOOK.md:220:    path: /metrics
    ./ALERTING_RUNBOOK.md:225:Existing app ingress uses `/` on the API host, so exposing `/metrics` on port 8000 would also make it routable there. **Before enabling**, add a DEV/STAGE-specific Traefik restriction for the exact `/metrics` path (including `/metrics/` redirect variant), using an IP allowlist middleware/route that denies external access while direct internal metrics Service scraping remains allowed; or implement a dedicated private metrics listener. Confirm external requests are rejected and internal scraping succeeds. Simply omitting an explicit metrics ingress is insufficient with the existing catch-all route. Do not modify the PROD/shared ingress.
    ./ALERTING_RUNBOOK.md:227:Validate in DEV first: disabled flag preserves `/metrics` 404, enabled route returns Prometheus content, OpenAPI generation remains valid, auth/CORS/errors/streaming behavior and existing backend tests pass, request counters/histograms advance after known traffic, route cardinality remains bounded, each replica has an UP target, and CPU/memory/latency overhead fits capacity. Rebuild and deploy the immutable DEV image, then STAGE after validation. Tests should use isolated registries/app construction to avoid duplicate collector registration. Rollback: disable the DEV/STAGE flag or restore prior image and remove/disable its proposed ServiceMonitor; leave existing infrastructure monitoring intact.
    ./README-jenkins.md:8:```mermaid
    ./README-jenkins.md:9:flowchart TD
    ✓ • 498ms

## Activity

    $ nl -ba ci/promote.py; cat infra/jenkins-host/Jenkinsfile.host infra/jenkins-host/Jenkinsfile.smoke infra/jenkins-host/jenkins.yaml infra/jenkins-host/jobs.groovy infra/jenkins-host/run-tool.sh
         1    #!/usr/bin/env python3
         2    """Trusted Git writer. Never execute code from a selected application revision."""
         3    import argparse
         4    import json
         5    from pathlib import Path
         6    import re
         7    import subprocess
         8    import tempfile
         9
        10    REPO = 'https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git'
        11    REGISTRY = 'ghcr.io/fastapi-traefik-devops/fastapi-'
        12
        13
        14    def run(*args, cwd=None):
        15        return subprocess.check_output(args, cwd=cwd, text=True).strip()
        16
        17
        18    def git(*args, cwd=None):
        19        return run('git', *args, cwd=cwd)
        20
        21
        22    def digest(image):
        23        return run('crane', 'digest', image)
        24
        25
        26    def set_images(path, sha, digests):
        27        # Deliberately edit only image fields; preserve human-maintained overlay YAML.
        28        text = path.read_text()
        29        for name in ('backend', 'frontend'):
        30            pattern = rf'(  newName: {REGISTRY}{name}\n)  newTag: [^\n]+(?:\n  digest: [^\n]+)?'
        31            text, count = re.subn(pattern, rf'\g<1>  newTag: sha-{sha}\n  digest: {digests[name]}', text)
        32            if count != 1:
        33                raise RuntimeError(f'Expected exactly one {name} image entry in {path}')
        34        path.write_text(text)
        35
        36
        37    def main():
        38        p = argparse.ArgumentParser()
        39        p.add_argument('environment', choices=['dev', 'stage', 'prod'])
        40        p.add_argument('sha')
        41        p.add_argument('--release', default='')
        42        args = p.parse_args()
        43        if not re.fullmatch(r'[0-9a-f]{40}', args.sha):
        44            p.error('full SHA required')
        45        if args.environment == 'prod' and not re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', args.release):
        46            p.error('production requires vX.Y.Z')
        47        digests = {n: digest(f'{REGISTRY}{n}:sha-{args.sha}') for n in ('backend', 'frontend')}
        48        if not all(re.fullmatch(r'sha256:[0-9a-f]{64}', d) for d in digests.values()):
        49            raise RuntimeError('Unexpected registry digest')
        50        # A fixed trusted implementation is used; the target checkout is data only.
        51        with tempfile.TemporaryDirectory(prefix='gitops-') as directory:
        52            git('clone', '--quiet', '--no-checkout', REPO, directory)
        53            git('checkout', '--quiet', '-B', 'promotion', 'origin/main', cwd=directory)
        54            if args.environment != 'dev':
        55                git('merge-base', '--is-ancestor', args.sha, 'origin/main', cwd=directory)
        56            if args.environment == 'prod':
        57                git('fetch', '--quiet', 'origin', f'refs/tags/{args.release}:refs/tags/{args.release}', cwd=directory)
        58                if git('rev-parse', f'{args.release}^{{commit}}', cwd=directory) != args.sha:
        59                    raise RuntimeError('Release tag moved or disagrees with selected SHA')
        60                # Evidence that this exact digest pair was recorded in stage Git history.
        61                # Human approval additionally verifies Argo health/smoke tests; Jenkins has no cluster access.
        62                found = False
        63                for commit in git('log', '--format=%H', 'origin/main', '--', 'deploy/overlays/stage/promotion.json', cwd=directory).splitlines():
        64                    record = json.loads(git('show', f'{commit}:deploy/overlays/stage/promotion.json', cwd=directory))
        65                    if record['sha'] == args.sha and record['digests'] == digests:
        66                        found = True
        67                        break
        68                if not found:
        69                    raise RuntimeError('This digest pair has never been promoted to stage')
        70                for name, expected in digests.items():
        71                    target = f'{REGISTRY}{name}:{args.release}'
        72                    existing = subprocess.run(['crane', 'digest', target], text=True, capture_output=True)
        73                    if existing.returncode == 0:
        74                        if existing.stdout.strip() != expected:
        75                            raise RuntimeError('Refusing to overwrite existing release tag')
        76                    elif 'MANIFEST_UNKNOWN' in existing.stderr or 'NAME_UNKNOWN' in existing.stderr:
        77                        run('crane', 'tag', f'{REGISTRY}{name}@{expected}', args.release)
        78                    else:
        79                        raise RuntimeError('Registry lookup failed; refusing to treat it as missing')
        80                    if digest(target) != expected:
        81                        raise RuntimeError('Release digest mismatch')
        82            for attempt in range(5):
        83                git('fetch', '--quiet', 'origin', 'main', cwd=directory)
        84                git('reset', '--hard', 'origin/main', cwd=directory)
        85                overlay = Path(directory) / 'deploy' / 'overlays' / args.environment
        86                record_path = overlay / 'promotion.json'
        87                if args.environment == 'stage':
        88                    # Reject delayed builds when newer application/CI changes have reached main.
        89                    changed = git('diff', '--name-only', args.sha, 'origin/main', cwd=directory).splitlines()
        90                    if any(not (f.startswith(('deploy/', 'argocd/')) or f.endswith('.md')) for f in changed):
        91                        print('Stage promotion superseded by newer source on main')
        92                        return
        93                    if record_path.exists():
        94                        old = json.loads(record_path.read_text())['sha']
        95                        if old != args.sha:
        96                            git('merge-base', '--is-ancestor', old, args.sha, cwd=directory)
        97                set_images(overlay / 'kustomization.yaml', args.sha, digests)
        98                record_path.write_text(json.dumps({'sha': args.sha, 'digests': digests, 'release': args.release}, indent=2) + '\n')
        99                # Run the original trusted validator, never scripts from the data checkout.
       100                run('sh', str(Path(__file__).resolve().parent / 'validate.sh'), cwd=directory)
       101                git('add', f'deploy/overlays/{args.environment}', cwd=directory)
       102                if not git('diff', '--cached', '--name-only', cwd=directory):
       103                    print('Desired state already matches')
       104                    return
       105                if args.environment == 'prod':
       106                    branch = f'release/{args.release}'
       107                    ref = f'refs/remotes/origin/{branch}'
       108                    exists = subprocess.run(['git', 'show-ref', '--verify', '--quiet', ref], cwd=directory)
       109                    if exists.returncode == 0:
       110                        for filename in ('promotion.json', 'kustomization.yaml'):
       111                            existing = git('show', f'{ref}:deploy/overlays/prod/{filename}', cwd=directory)
       112                            if existing != (overlay / filename).read_text().strip():
       113                                raise RuntimeError('Existing release branch differs; review it manually, never overwrite')
       114                        print(f'Existing review branch: {branch}')
       115                        return
       116                git('-c', 'user.name=Jenkins GitOps', '-c', 'user.email=jenkins-gitops@users.noreply.github.com',
       117                    'commit', '-m', f'gitops({args.environment}): promote {args.sha} {args.release}'.strip(), cwd=directory)
       118                if args.environment == 'prod':
       119                    branch = f'release/{args.release}'
       120                    # Never force-push or merge. A human opens/reviews the PR.
       121                    git('push', 'origin', f'HEAD:refs/heads/{branch}', cwd=directory)
       122                    print(f'Open reviewed PR: {REPO.removesuffix(".git")}/compare/main...{branch}')
       123                    return
       124                result = subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/main'], cwd=directory)
       125                if result.returncode == 0:
       126                    return
       127            raise RuntimeError('Main advanced repeatedly; rerun promotion')
       128
       129
       130    if __name__ == '__main__':
       131        main()
    // Admin-controlled host variant of Jenkinsfile. No publication or Kubernetes agents.
    def shHost(String body) {
        writeFile file: '.host-step.sh', text: '#!/bin/sh\n' + body
        sh '/opt/host-ci/run-tool.sh "$HOST_TOOL" "$WORKSPACE/.host-step.sh"'
    }
    pipeline {
        agent { label 'host-ci' }

        options {
            skipDefaultCheckout(true)
            timeout(time: 45, unit: 'MINUTES')
            disableConcurrentBuilds()
            buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '2'))
        }

        environment {
            REGISTRY_NAMESPACE = 'ghcr.io/fastapi-traefik-devops'
            CI = 'true'
            // Test-only settings. PostgreSQL is isolated inside this agent Pod.
            ENVIRONMENT = 'local'
            PROJECT_NAME = 'FastAPI CI'
            POSTGRES_SERVER = 'postgres-test'
            POSTGRES_PORT = '5432'
            POSTGRES_DB = 'app_ci'
            POSTGRES_USER = 'postgres'
            POSTGRES_PASSWORD = 'ci-only-postgres-password'
            FIRST_SUPERUSER = 'ci-admin@example.com'
            EMAIL_TEST_USER = 'test@example.com'
            EMAILS_FROM_EMAIL = 'ci@example.com'
            EMAILS_FROM_NAME = 'ci@example.com'
            SMTP_HOST = '127.0.0.1'
            SMTP_PORT = '1025'
            SMTP_TLS = 'false'
            SMTP_SSL = 'false'
            BACKEND_CORS_ORIGINS = 'http://localhost:5173'
            FRONTEND_HOST = 'http://localhost:5173'
            VITE_API_URL = ''
        }

        stages {

            stage('Checkout') {
                steps {
                    script {
                        def revision = checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: 'https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git']]])
                        env.BRANCH_NAME = 'main'
                        env.IMAGE_SHA = revision.GIT_COMMIT
                        if (!(env.IMAGE_SHA ==~ /[0-9a-f]{40}/)) { error('Expected full Git SHA') }
                        if (!env.BRANCH_NAME) { error('Configure a GitHub multibranch job') }
                        env.SKIP_BUILD = env.TAG_NAME ? 'true' : 'false'
                        // GitOps-only changes validate, but never create application artifacts.
                        def changes = sh(returnStdout: true, script: 'git diff-tree --root --first-parent -m --no-commit-id --name-only -r HEAD').trim().readLines()
                        if (changes && changes.every { it.startsWith('deploy/') || it.startsWith('argocd/') || it.endsWith('.md') }) {
                            env.SKIP_BUILD = 'true'
                        }
                        writeFile file: 'source-sha.txt', text: env.IMAGE_SHA + '\n'

                    }
                }
            }

            stage('Backend Checks and Tests') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    withEnv(['HOST_TOOL=python']) {
                        shHost '''
                            set -eu
                            # Jenkins sh normally enables tracing; keep ephemeral keys out of logs.
                            set +x
                            cd backend
                            uv sync --frozen
                            SECRET_KEY="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(32))')"
                            FIRST_SUPERUSER_PASSWORD="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(24))')"
                            export SECRET_KEY FIRST_SUPERUSER_PASSWORD
                            uv run --frozen bash scripts/lint.sh
                            uv run --frozen bash scripts/prestart.sh
                            test_status=0
                            uv run --frozen coverage run --source=app -m pytest --junitxml=test-results.xml || test_status=$?
                            # Preserve reports on test failure without hiding pytest's exit status.
                            report_status=0
                            uv run --frozen coverage report --show-missing || report_status=$?
                            uv run --frozen coverage xml -o coverage.xml || report_status=$?
                            if [ "$test_status" -ne 0 ]; then
                                exit "$test_status"
                            fi
                            exit "$report_status"
                        '''
                    }
                }
                post {
                    always {
                        junit testResults: 'backend/test-results.xml', allowEmptyResults: true
                        archiveArtifacts artifacts: 'backend/coverage.xml', allowEmptyArchive: true
                    }
                }
            }

            stage('Frontend Check') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    withEnv(['HOST_TOOL=node']) {
                        shHost '''
                            set -eu
                            echo "--- Verifying Frontend Dependencies ---"
                            cd frontend
                            npm ci
                            npm run build
                        '''
                    }
                }
            }

            stage('Validate all overlays') {
                steps {
                    withEnv(['HOST_TOOL=node']) {
                        withEnv(['HOST_TOOL=node']) { shHost 'sh ci/tools.sh && PATH=/tmp/ci-bin:$PATH sh ci/validate.sh && PATH=/tmp/ci-bin:$PATH python3 -m unittest discover -s ci -p "test_*.py"' }
                    }
                }
            }

            stage('Build image archives') {
                when { expression { env.SKIP_BUILD != 'true' } }
                steps {
                    withEnv(['HOST_TOOL=buildkit']) {
                        shHost '''
                            set -eu
                            buildkitd --config /etc/buildkit/host.toml --addr unix:///tmp/buildkitd.sock > /tmp/buildkitd.log 2>&1 &
                            BUILDKIT_PID=$!
                            trap 'kill "${BUILDKIT_PID}" 2>/dev/null || true; wait "${BUILDKIT_PID}" 2>/dev/null || true' EXIT

                            ready=false
                            for i in $(seq 1 60); do
                                if buildctl --addr unix:///tmp/buildkitd.sock debug workers > /dev/null 2>&1; then
                                    ready=true
                                    break
                                fi
                                if ! kill -0 "${BUILDKIT_PID}" 2>/dev/null; then
                                    cat /tmp/buildkitd.log
                                    exit 1
                                fi
                                sleep 1
                            done
                            if [ "$ready" != true ]; then
                                cat /tmp/buildkitd.log
                                echo "BuildKit did not become ready within 60 seconds"
                                exit 1
                            fi

                            # Verify both image builds before any registry writes.
                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/backend" \
                              --local dockerfile="${WORKSPACE}/backend" \
                              --output type=docker,dest=${WORKSPACE}/backend-ci.tar \
                              --progress=plain

                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/frontend" \
                              --local dockerfile="${WORKSPACE}/frontend" \
                              --opt "build-arg:VITE_API_URL=${VITE_API_URL:-}" \
                              --output type=docker,dest=${WORKSPACE}/frontend-ci.tar \
                              --progress=plain

                        '''
                    }
                }
            }
            stage('Archive checked images') {
                when { expression { env.SKIP_BUILD != 'true' && !env.CHANGE_ID } }
                steps {
                    archiveArtifacts artifacts: '*-ci.tar,source-sha.txt', fingerprint: true
                }
            }

        }

        post {
            always {
                // Tool containers create root-owned files; clean them in the same
                // container before the inbound agent removes the workspace.
                withEnv(['HOST_TOOL=python']) {
                    shHost '''
                        set -eu
                        test -n "${WORKSPACE}"
                        test "${WORKSPACE}" != /
                        cd "${WORKSPACE}"
                        find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
                    '''
                }
                deleteDir()
            }
        }
    }
    pipeline {
      agent { label 'host-ci' }
      options { disableConcurrentBuilds(); timeout(time: 10, unit: 'MINUTES'); buildDiscarder(logRotator(numToKeepStr: '5')) }
      stages {
        stage('Checkout') {
          steps { git branch: 'main', url: 'https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git' }
        }
        stage('Shell and Docker') {
          steps {
            sh '''
              set -eu
              test -f Jenkinsfile
              git rev-parse --verify HEAD
              printf 'Jenkins workspace and shell OK\n'
              docker info --format '{{.ServerVersion}}'
              mkdir -p .host-smoke
              printf 'host-ci smoke\n' > .host-smoke/probe
              printf 'FROM scratch\nCOPY probe /probe\n' > .host-smoke/Dockerfile
              docker build --network=none --tag host-ci-smoke:local .host-smoke
              test "$(docker image inspect host-ci-smoke:local --format '{{.Id}}')" != ''
              docker image rm host-ci-smoke:local
            '''
          }
        }
      }
      post { always { deleteDir() } }
    }
    jenkins:
      systemMessage: "Local bounded CI; GitOps remains in Argo CD. Publication disabled."
      numExecutors: 0
      mode: EXCLUSIVE
      securityRealm:
        local:
          allowsSignup: false
          users:
            - id: admin
              password: "${jenkins-admin-password}"
      authorizationStrategy:
        loggedInUsersCanDoAnything:
          allowAnonymousRead: false
      nodes:
        - permanent:
            name: host-ci
            remoteFS: /home/jenkins/agent
            labelString: host-ci
            numExecutors: 1
            mode: EXCLUSIVE
            launcher:
              inbound:
                workDirSettings:
                  disabled: false
                  workDirPath: /home/jenkins/agent
      remotingSecurity:
        enabled: true
    unclassified:
      location:
        url: http://127.0.0.1:8085/
    jobs:
      - file: /bootstrap/jobs.groovy
    // Admin-controlled local pipeline source, never an untrusted PR definition.
    pipelineJob('host-smoke') {
      description('Manual checkout/shell/isolated Docker smoke test; no registry or Git writes.')
      definition { cps { script(new File('/bootstrap/Jenkinsfile.smoke').text); sandbox() } }
    }
    folder('app-ci')
    pipelineJob('app-ci/main') {
      description('Manual host CI. Disabled pending measured smoke-test capacity review. No publisher trigger.')
      disabled(true)
      definition { cps { script(new File('/bootstrap/Jenkinsfile.host').text); sandbox() } }
    }
    folder('trusted')
    pipelineJob('trusted/publish') {
      description('Recovery placeholder: DISABLED. Missing ghcr-write, gitops-app, ci-read and isolated trusted agent. Original Jenkinsfile.promote retained in Git.')
      disabled(true)
      definition { cps { script("error('Publishing is disabled until credentials and trust isolation are reviewed')"); sandbox() } }
    }
    #!/bin/sh
    # Sequential disposable tools, entirely within the bounded DinD parent cgroup.
    set -eu
    kind=$1
    step=$2
    run_id=$(printf '%s' "${BUILD_TAG:-local}" | tr -c 'a-zA-Z0-9_.-' '-')
    network="ci-$run_id"
    name="tool-$run_id"
    cleanup() {
      docker rm -f "$name" postgres-test >/dev/null 2>&1 || true
      docker network rm "$network" >/dev/null 2>&1 || true
    }
    trap cleanup EXIT INT TERM
    limit=512m
    image=ghcr.io/astral-sh/uv:0.5.11-python3.10-bookworm-slim
    case "$kind" in
      python) ;;
      node) image=node:20.18.1; limit=640m ;;
      buildkit) image=moby/buildkit:v0.24.0; limit=1024m ;;
      *) echo 'Unknown CI tool' >&2; exit 2 ;;
    esac
    docker network create "$network" >/dev/null
    # Only the backend test step needs a database; credentials are disposable CI settings.
    if [ "$kind" = python ] && grep -q 'scripts/prestart.sh' "$step"; then
      docker run -d --name postgres-test --network "$network" --memory=128m --memory-swap=128m --cpus=0.25 \
        -e POSTGRES_DB=app_ci -e POSTGRES_PASSWORD=ci-only-postgres-password postgres:16.6 >/dev/null
      ready=false
      for i in $(seq 1 60); do
        if docker exec postgres-test pg_isready -U postgres -d app_ci >/dev/null 2>&1; then ready=true; break; fi
        sleep 1
      done
      test "$ready" = true
    fi
    set -- docker run --rm --name "$name" --network "$network" --memory="$limit" --memory-swap="$limit" --cpus=1 \
      --user=0 -v "$WORKSPACE:$WORKSPACE" -w "$WORKSPACE" \
      -e NODE_OPTIONS=--max-old-space-size=384 -e CI=true \
      -e WORKSPACE -e REGISTRY_NAMESPACE -e IMAGE_SHA -e VITE_API_URL \
      -e ENVIRONMENT -e PROJECT_NAME -e POSTGRES_SERVER -e POSTGRES_PORT -e POSTGRES_DB -e POSTGRES_USER -e POSTGRES_PASSWORD \
      -e FIRST_SUPERUSER -e EMAIL_TEST_USER -e EMAILS_FROM_EMAIL -e EMAILS_FROM_NAME \
      -e SMTP_HOST -e SMTP_PORT -e SMTP_TLS -e SMTP_SSL -e BACKEND_CORS_ORIGINS -e FRONTEND_HOST
    if [ "$kind" = buildkit ]; then
      set -- "$@" --privileged -v /opt/host-ci/buildkit.toml:/etc/buildkit/host.toml:ro --entrypoint=sh
    fi
    if [ "$kind" = buildkit ]; then "$@" "$image" "$step"; else "$@" "$image" sh "$step"; fi
    ✓ • 0ms

## Activity

    $ nl -ba monitoring/values.yaml; nl -ba monitoring/rules/dev-stage.yaml; cat monitoring/monitors/*.yaml; cat monitoring/test-alert-rules.py; nl -ba infra/jenkins-host/jobs.groovy; nl -ba infra/jenkins-host/run-tool.sh
         1    fullnameOverride: monitoring
         2    defaultRules:
         3      create: false
         4    kubeControllerManager:
         5      enabled: false
         6    kubeScheduler:
         7      enabled: false
         8    kubeEtcd:
         9      enabled: false
        10    kubeProxy:
        11      enabled: false
        12    crds:
        13      enabled: true
        14      upgradeJob:
        15        enabled: false
        16    prometheusOperator:
        17      admissionWebhooks:
        18        enabled: false
        19      tls:
        20        enabled: false
        21      resources:
        22        requests:
        23          cpu: 40m
        24          memory: 128Mi
        25        limits:
        26          cpu: 200m
        27          memory: 256Mi
        28      prometheusConfigReloader:
        29        resources:
        30          requests:
        31            cpu: 5m
        32            memory: 32Mi
        33          limits:
        34            cpu: 100m
        35            memory: 64Mi
        36    prometheus:
        37      ingress:
        38        enabled: false
        39      prometheusSpec:
        40        replicas: 1
        41        retention: 3d
        42        retentionSize: 1500MB
        43        scrapeInterval: 60s
        44        evaluationInterval: 60s
        45        resources:
        46          requests:
        47            cpu: 100m
        48            memory: 512Mi
        49          limits:
        50            cpu: 500m
        51            memory: 1536Mi
        52        serviceMonitorSelectorNilUsesHelmValues: false
        53        serviceMonitorSelector:
        54          matchLabels:
        55            release: monitoring
        56        serviceMonitorNamespaceSelector:
        57          matchLabels:
        58            kubernetes.io/metadata.name: monitoring
        59        podMonitorSelectorNilUsesHelmValues: false
        60        podMonitorSelector:
        61          matchLabels:
        62            release: monitoring
        63        podMonitorNamespaceSelector:
        64          matchLabels:
        65            kubernetes.io/metadata.name: monitoring
        66        ruleSelectorNilUsesHelmValues: false
        67        ruleSelector:
        68          matchLabels:
        69            release: monitoring
        70        ruleNamespaceSelector:
        71          matchLabels:
        72            kubernetes.io/metadata.name: monitoring
        73        storageSpec:
        74          volumeClaimTemplate:
        75            metadata:
        76              annotations:
        77                argocd.argoproj.io/sync-options: Prune=false,Delete=false
        78            spec:
        79              storageClassName: standard
        80              accessModes:
        81              - ReadWriteOnce
        82              resources:
        83                requests:
        84                  storage: 2Gi
        85    alertmanager:
        86      ingress:
        87        enabled: false
        88      config:
        89        global:
        90          resolve_timeout: 5m
        91        route:
        92          receiver: 'null'
        93          group_by:
        94          - alertname
        95          - namespace
        96          group_wait: 1m
        97          group_interval: 5m
        98          repeat_interval: 12h
        99        receivers:
       100        - name: 'null'
       101      alertmanagerSpec:
       102        replicas: 1
       103        resources:
       104          requests:
       105            cpu: 20m
       106            memory: 64Mi
       107          limits:
       108            cpu: 100m
       109            memory: 128Mi
       110        storage:
       111          volumeClaimTemplate:
       112            metadata:
       113              annotations:
       114                argocd.argoproj.io/sync-options: Prune=false,Delete=false
       115            spec:
       116              storageClassName: standard
       117              accessModes:
       118              - ReadWriteOnce
       119              resources:
       120                requests:
       121                  storage: 256Mi
       122    kube-state-metrics:
       123      resources:
       124        requests:
       125          cpu: 30m
       126          memory: 64Mi
       127        limits:
       128          cpu: 150m
       129          memory: 128Mi
       130    prometheus-node-exporter:
       131      hostNetwork: false
       132      service:
       133        enableHostPort: false
       134      resources:
       135        requests:
       136          cpu: 20m
       137          memory: 32Mi
       138        limits:
       139          cpu: 100m
       140          memory: 64Mi
       141    grafana:
       142      replicas: 1
       143      defaultDashboardsEnabled: false
       144      ingress:
       145        enabled: false
       146      service:
       147        type: ClusterIP
       148      resources:
       149        requests:
       150          cpu: 50m
       151          memory: 128Mi
       152        limits:
       153          cpu: 300m
       154          memory: 384Mi
       155      persistence:
       156        enabled: false
       157      # Provision separately; credentials never enter Helm values or Git.
       158      admin:
       159        existingSecret: monitoring-grafana-admin
       160        userKey: admin-user
       161        passwordKey: admin-password
       162      grafana.ini:
       163        auth:
       164          disable_login_form: false
       165        auth.anonymous:
       166          enabled: false
       167        users:
       168          allow_sign_up: false
       169        analytics:
       170          reporting_enabled: false
       171          check_for_updates: false
       172      sidecar:
       173        resources:
       174          requests:
       175            cpu: 10m
       176            memory: 32Mi
       177          limits:
       178            cpu: 100m
       179            memory: 128Mi
       180        datasources:
       181          enabled: false
       182        dashboards:
       183          enabled: true
       184          searchNamespace: monitoring
       185          skipReload: true
       186          initDashboards: false
       187          provider:
       188            allowUiUpdates: false
       189            disableDelete: true
       190            updateIntervalSeconds: 30
       191      datasources:
       192        datasources.yaml:
       193          apiVersion: 1
       194          datasources:
       195          - name: Prometheus
       196            uid: prometheus
       197            type: prometheus
       198            url: http://monitoring-prometheus.monitoring.svc.cluster.local:9090
       199            access: proxy
       200            isDefault: true
       201            editable: false
       202      testFramework:
       203        enabled: false
       204    coreDns:
       205      enabled: false
         1    apiVersion: monitoring.coreos.com/v1
         2    kind: PrometheusRule
         3    metadata:
         4      name: dev-stage-platform
         5      namespace: monitoring
         6      labels:
         7        release: monitoring
         8    spec:
         9      groups:
        10      - name: dev-stage-platform
        11        rules:
        12        - alert: NodeMemoryPressure
        13          expr: kube_node_status_condition{condition="MemoryPressure",status="true"} ==
        14            1
        15          for: 5m
        16          labels:
        17            severity: warning
        18          annotations:
        19            summary: Node has sustained Kubernetes memory pressure
        20        - alert: NodeDiskPressure
        21          expr: kube_node_status_condition{condition="DiskPressure",status="true"} ==
        22            1
        23          for: 5m
        24          labels:
        25            severity: warning
        26          annotations:
        27            summary: Node has sustained Kubernetes disk pressure
        28        - alert: NodeHighCPU
        29          expr: (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
        30            > 0.85
        31          for: 15m
        32          labels:
        33            severity: warning
        34          annotations:
        35            summary: Node CPU usage sustained above 85 percent
        36        - alert: NodeHighMemory
        37          expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.90
        38          for: 15m
        39          labels:
        40            severity: warning
        41          annotations:
        42            summary: Node memory usage sustained above 90 percent
        43        - alert: ApplicationRestartSpike
        44          expr: sum by(namespace,pod,container) (increase(kube_pod_container_status_restarts_total{namespace=~"app-dev|app-stage"}[15m]))
        45            >= 3
        46          for: 5m
        47          labels:
        48            severity: warning
        49          annotations:
        50            summary: DEV or STAGE container restarted at least three times in 15 minutes
        51        - alert: ApplicationDeploymentUnavailable
        52          expr: kube_deployment_status_replicas_available{namespace=~"app-dev|app-stage"}
        53            < kube_deployment_spec_replicas{namespace=~"app-dev|app-stage"}
        54          for: 10m
        55          labels:
        56            severity: warning
        57          annotations:
        58            summary: DEV or STAGE deployment has fewer available replicas than desired
        59        - alert: ArgoApplicationUnhealthy
        60          expr: argocd_app_info{name=~"app-dev|app-stage",health_status!="Healthy"} ==
        61            1
        62          for: 10m
        63          labels:
        64            severity: warning
        65          annotations:
        66            summary: DEV or STAGE Argo Application is unhealthy
        67        - alert: ArgoApplicationOutOfSync
        68          expr: argocd_app_info{name=~"app-dev|app-stage",sync_status!="Synced"} == 1
        69          for: 10m
        70          labels:
        71            severity: warning
        72          annotations:
        73            summary: DEV or STAGE Argo Application is out of sync
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-metrics
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-metrics
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-server-metrics
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-server-metrics
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: argocd-repo-server
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - argocd
      selector:
        matchLabels:
          app.kubernetes.io/name: argocd-repo-server
      endpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    apiVersion: monitoring.coreos.com/v1
    kind: PodMonitor
    metadata:
      name: traefik
      namespace: monitoring
      labels:
        release: monitoring
    spec:
      namespaceSelector:
        matchNames:
        - traefik
      selector:
        matchLabels:
          app.kubernetes.io/name: traefik
          app.kubernetes.io/instance: traefik-traefik
      podMetricsEndpoints:
      - port: metrics
        path: /metrics
        interval: 60s
        scrapeTimeout: 10s
    #!/usr/bin/env python3
    """Test loaded rules with synthetic samples; never inject alerts or stress workloads.

    Requires a loopback Prometheus forward on 19090 and PyYAML.
    Uses .tools/promtool (copied from the installed image) and matching local rules.
    """
    import json
    import re
    from pathlib import Path
    import subprocess
    import tempfile
    import urllib.request
    import urllib.parse
    import yaml

    rules = yaml.safe_load((Path(__file__).parent / 'rules/dev-stage.yaml').read_text())['spec']['groups'][0]['rules']
    loaded = json.load(urllib.request.urlopen('http://127.0.0.1:19090/api/v1/rules', timeout=20))['data']['groups']
    group = next(g for g in loaded if g['name'] == 'dev-stage-platform')
    for rule in rules:
        live = next(r for r in group['rules'] if r['name'] == rule['alert'])
        canonical = json.load(urllib.request.urlopen('http://127.0.0.1:19090/api/v1/format_query?' + urllib.parse.urlencode({'query': rule['expr']}), timeout=20))['data']
        assert re.sub(r'\s+', '', live['query']) == re.sub(r'\s+', '', canonical) and live['duration'] == {'5m': 300, '10m': 600, '15m': 900}[rule['for']], rule['alert']
        assert live['annotations'] == rule['annotations'] and live['labels'] == rule['labels'], rule['alert']
        assert live['health'] == 'ok' and not live.get('lastError'), rule['alert']

    def sample(metric, labels, values):
        return {'series': metric + '{' + ','.join(f'{k}="{v}"' for k, v in labels.items()) + '}', 'values': values}

    cases = {
        'NodeMemoryPressure': ([sample('kube_node_status_condition', {'node': 'test', 'condition': 'MemoryPressure', 'status': 'true'}, '1+0x24 0+0x25')], {'node': 'test', 'condition': 'MemoryPressure', 'status': 'true'}, 5),
        'NodeDiskPressure': ([sample('kube_node_status_condition', {'node': 'test', 'condition': 'DiskPressure', 'status': 'true'}, '1+0x24 0+0x25')], {'node': 'test', 'condition': 'DiskPressure', 'status': 'true'}, 5),
        'NodeHighCPU': ([sample('node_cpu_seconds_total', {'instance': 'test', 'mode': 'idle'}, '0+5x24 180+60x25')], {'instance': 'test'}, 16),
        'NodeHighMemory': ([sample('node_memory_MemAvailable_bytes', {'instance': 'test'}, '5+0x24 50+0x25'), sample('node_memory_MemTotal_bytes', {'instance': 'test'}, '100+0x50')], {'instance': 'test'}, 15),
        'ApplicationRestartSpike': ([sample('kube_pod_container_status_restarts_total', {'namespace': 'app-dev', 'pod': 'test', 'container': 'backend'}, '0 3+0x49')], {'namespace': 'app-dev', 'pod': 'test', 'container': 'backend'}, 6),
        'ApplicationDeploymentUnavailable': ([sample('kube_deployment_status_replicas_available', {'namespace': 'app-stage', 'deployment': 'backend'}, '0+0x24 1+0x25'), sample('kube_deployment_spec_replicas', {'namespace': 'app-stage', 'deployment': 'backend'}, '1+0x50')], {'namespace': 'app-stage', 'deployment': 'backend'}, 10),
        'ArgoApplicationUnhealthy': ([sample('argocd_app_info', {'name': 'app-dev', 'health_status': 'Degraded', 'sync_status': 'Synced'}, '1+0x24 0+0x25')], {'name': 'app-dev', 'health_status': 'Degraded', 'sync_status': 'Synced'}, 10),
        'ArgoApplicationOutOfSync': ([sample('argocd_app_info', {'name': 'app-stage', 'health_status': 'Healthy', 'sync_status': 'OutOfSync'}, '1+0x24 0+0x25')], {'name': 'app-stage', 'health_status': 'Healthy', 'sync_status': 'OutOfSync'}, 10),
    }
    tests = []
    for rule in rules:
        samples, labels, fires = cases[rule['alert']]
        tests.append({'name': rule['alert'] + ' pending/firing/recovered', 'interval': '1m', 'input_series': samples, 'alert_rule_test': [
            {'eval_time': f'{fires-1}m', 'alertname': rule['alert'], 'exp_alerts': []},
            {'eval_time': f'{fires}m', 'alertname': rule['alert'], 'exp_alerts': [{'exp_labels': {**labels, **rule['labels']}, 'exp_annotations': rule['annotations']}]},
            {'eval_time': '45m', 'alertname': rule['alert'], 'exp_alerts': []},
        ]})
    # Threshold boundaries are healthy: CPU=85%, memory=90%, restarts<3,
    # equal available/desired, normal node conditions and Healthy/Synced apps.
    healthy = [sample('node_cpu_seconds_total', {'instance': 'test', 'mode': 'idle'}, '0+9x50'), sample('node_memory_MemAvailable_bytes', {'instance': 'test'}, '10+0x50'), sample('node_memory_MemTotal_bytes', {'instance': 'test'}, '100+0x50')]
    for condition in ['MemoryPressure', 'DiskPressure']:
        healthy.append(sample('kube_node_status_condition', {'node': 'test', 'condition': condition, 'status': 'true'}, '0+0x50'))
    for ns in ['app-dev', 'app-stage']:
        healthy.extend([sample('kube_pod_container_status_restarts_total', {'namespace': ns, 'pod': 'test', 'container': 'backend'}, '0 2+0x49'), sample('kube_deployment_status_replicas_available', {'namespace': ns, 'deployment': 'backend'}, '1+0x50'), sample('kube_deployment_spec_replicas', {'namespace': ns, 'deployment': 'backend'}, '1+0x50'), sample('argocd_app_info', {'name': ns, 'health_status': 'Healthy', 'sync_status': 'Synced'}, '1+0x50')])
    # Unhealthy synthetic PROD samples must never match application rules.
    healthy.extend([sample('kube_pod_container_status_restarts_total', {'namespace': 'app-prod', 'pod': 'test', 'container': 'backend'}, '0+10x50'), sample('kube_deployment_status_replicas_available', {'namespace': 'app-prod', 'deployment': 'backend'}, '0+0x50'), sample('kube_deployment_spec_replicas', {'namespace': 'app-prod', 'deployment': 'backend'}, '1+0x50'), sample('argocd_app_info', {'name': 'app-prod', 'health_status': 'Degraded', 'sync_status': 'OutOfSync'}, '1+0x50')])
    tests.append({'name': 'Healthy boundaries and environment isolation', 'interval': '1m', 'input_series': healthy, 'alert_rule_test': [{'eval_time': t, 'alertname': r['alert'], 'exp_alerts': []} for r in rules for t in ['6m', '30m']]})
    with tempfile.TemporaryDirectory(prefix='monitoring-alert-tests-') as directory:
        rulefile = Path(directory) / 'rules.yaml'
        rulefile.write_text(yaml.safe_dump({'groups': [{'name': 'dev-stage-platform', 'rules': rules}]}))
        testfile = Path(directory) / 'tests.yaml'
        testfile.write_text(yaml.safe_dump({'rule_files': [str(rulefile)], 'evaluation_interval': '1m', 'tests': tests}))
        promtool = Path(__file__).resolve().parent.parent / '.tools/promtool'
        subprocess.run([str(promtool), 'test', 'rules', str(testfile)], check=True)
    print('Eight live rules match local definitions; pending/firing/recovery and healthy boundary/isolation tests PASS')
         1    // Admin-controlled local pipeline source, never an untrusted PR definition.
         2    pipelineJob('host-smoke') {
         3      description('Manual checkout/shell/isolated Docker smoke test; no registry or Git writes.')
         4      definition { cps { script(new File('/bootstrap/Jenkinsfile.smoke').text); sandbox() } }
         5    }
         6    folder('app-ci')
         7    pipelineJob('app-ci/main') {
         8      description('Manual host CI. Disabled pending measured smoke-test capacity review. No publisher trigger.')
         9      disabled(true)
        10      definition { cps { script(new File('/bootstrap/Jenkinsfile.host').text); sandbox() } }
        11    }
        12    folder('trusted')
        13    pipelineJob('trusted/publish') {
        14      description('Recovery placeholder: DISABLED. Missing ghcr-write, gitops-app, ci-read and isolated trusted agent. Original Jenkinsfile.promote retained in Git.')
        15      disabled(true)
        16      definition { cps { script("error('Publishing is disabled until credentials and trust isolation are reviewed')"); sandbox() } }
        17    }
         1    #!/bin/sh
         2    # Sequential disposable tools, entirely within the bounded DinD parent cgroup.
         3    set -eu
         4    kind=$1
         5    step=$2
         6    run_id=$(printf '%s' "${BUILD_TAG:-local}" | tr -c 'a-zA-Z0-9_.-' '-')
         7    network="ci-$run_id"
         8    name="tool-$run_id"
         9    cleanup() {
        10      docker rm -f "$name" postgres-test >/dev/null 2>&1 || true
        11      docker network rm "$network" >/dev/null 2>&1 || true
        12    }
        13    trap cleanup EXIT INT TERM
        14    limit=512m
        15    image=ghcr.io/astral-sh/uv:0.5.11-python3.10-bookworm-slim
        16    case "$kind" in
        17      python) ;;
        18      node) image=node:20.18.1; limit=640m ;;
        19      buildkit) image=moby/buildkit:v0.24.0; limit=1024m ;;
        20      *) echo 'Unknown CI tool' >&2; exit 2 ;;
        21    esac
        22    docker network create "$network" >/dev/null
        23    # Only the backend test step needs a database; credentials are disposable CI settings.
        24    if [ "$kind" = python ] && grep -q 'scripts/prestart.sh' "$step"; then
        25      docker run -d --name postgres-test --network "$network" --memory=128m --memory-swap=128m --cpus=0.25 \
        26        -e POSTGRES_DB=app_ci -e POSTGRES_PASSWORD=ci-only-postgres-password postgres:16.6 >/dev/null
        27      ready=false
        28      for i in $(seq 1 60); do
        29        if docker exec postgres-test pg_isready -U postgres -d app_ci >/dev/null 2>&1; then ready=true; break; fi
        30        sleep 1
        31      done
        32      test "$ready" = true
        33    fi
        34    set -- docker run --rm --name "$name" --network "$network" --memory="$limit" --memory-swap="$limit" --cpus=1 \
        35      --user=0 -v "$WORKSPACE:$WORKSPACE" -w "$WORKSPACE" \
        36      -e NODE_OPTIONS=--max-old-space-size=384 -e CI=true \
        37      -e WORKSPACE -e REGISTRY_NAMESPACE -e IMAGE_SHA -e VITE_API_URL \
        38      -e ENVIRONMENT -e PROJECT_NAME -e POSTGRES_SERVER -e POSTGRES_PORT -e POSTGRES_DB -e POSTGRES_USER -e POSTGRES_PASSWORD \
        39      -e FIRST_SUPERUSER -e EMAIL_TEST_USER -e EMAILS_FROM_EMAIL -e EMAILS_FROM_NAME \
        40      -e SMTP_HOST -e SMTP_PORT -e SMTP_TLS -e SMTP_SSL -e BACKEND_CORS_ORIGINS -e FRONTEND_HOST
        41    if [ "$kind" = buildkit ]; then
        42      set -- "$@" --privileged -v /opt/host-ci/buildkit.toml:/etc/buildkit/host.toml:ro --entrypoint=sh
        43    fi
        44    if [ "$kind" = buildkit ]; then "$@" "$image" "$step"; else "$@" "$image" sh "$step"; fi
    ✓ • 0ms

## Activity

    $ nl -ba README-jenkins.md; nl -ba deployment.md | tail -135; nl -ba MIGRATION_BACKUP_CHECKLIST.md; cat scripts/build.sh scripts/build-push.sh scripts/deploy.sh scripts/test.sh scripts/test-local.sh; cat k8s/rbac/*.yaml ci/jenkins-controller-rbac.yaml; cat monitoring/bootstrap.py monitoring/ensure-grafana-secret.py monitoring/verify-grafana-auth.py
         1    # GitHub Flow + Jenkins + GHCR + Argo CD
         2
         3    `main` is the only long-lived branch. Use short-lived feature branches and reviewed
         4    pull requests. Jenkins checks/builds artifacts and writes Git; Argo CD reconciles
         5    application resources. Jenkins has no application deployment commands or cluster
         6    credentials. Existing Compose files remain useful for local development.
         7
         8    ```mermaid
         9    flowchart TD
        10      F[Feature branch or PR] --> CI[Jenkins app-ci multibranch: checks and image archives]
        11      CI -->|successful repository branch only| P[Trusted Jenkins publisher]
        12      P --> SHA[GHCR sha-full-commit-SHA images]
        13      M[main] --> CI
        14      P -->|main only| S[stage overlay Git commit]
        15      SHA -->|selected successful build + approval| D[dev overlay Git commit]
        16      T[vX.Y.Z tag] --> R[Trusted release: approval, main ancestry, existing SHA digests, stage history]
        17      R --> V[Retag existing images; never build]
        18      V --> PR[prod review branch and human PR]
        19      PR -->|approved merge| G[main desired state]
        20      S --> G
        21      D --> G
        22      G --> A[Argo CD]
        23      A --> E[app-dev / app-stage / app-prod]
        24    ```
        25
        26    ## Layout and trust boundary
        27
        28    | Path | Purpose |
        29    | --- | --- |
        30    | `Jenkinsfile` | Credential-free multibranch CI; backend mypy/Ruff/tests, JUnit/coverage, frontend TypeScript/Vite, all overlay validation/promotion safety tests, BuildKit image archives |
        31    | `Jenkinsfile.promote` | Separate trusted standalone job loaded ONLY from protected main; successful-build verification, publishing, Git-only promotions |
        32    | `ci/tools.sh` | Version/checksum-pinned amd64 Kustomize 5.6.0, kubeconform 0.6.7, crane 0.20.3 |
        33    | `ci/validate.sh` | Render and strictly schema-check all overlays against Kubernetes 1.31 |
        34    | `ci/publish.sh`, `ci/promote.py` | Registry operations and Git writer; no execution of selected source revision |
        35    | `ci/jenkins-controller-rbac.yaml` | Bootstrap-only agent Pod management in dedicated CI namespaces |
        36    | `deploy/base` | Shared Deployments, Services, ConfigMaps, migration Job, PVC and Ingress; no plaintext Secrets |
        37    | `deploy/overlays/dev` | Selected development SHA/digests and dev configuration |
        38    | `deploy/overlays/stage` | Latest eligible successful main SHA/digests and stage configuration |
        39    | `deploy/overlays/prod` | Reviewed release SHA/digests and production configuration |
        40    | `argocd/project.yaml` | Restricts repository, three namespaces and namespaced resource kinds |
        41    | `argocd/applicationset.yaml` | Three applications tracking main, automatic prune/selfHeal |
        42
        43    The two-job split is intentional: a `when` condition in a branch-controlled
        44    Jenkinsfile is **not** a credentials security boundary. Branch authors can edit
        45    that file. Only the `trusted` folder holds write credentials. The publisher copies
        46    image archives as data and never runs branch scripts or Dockerfiles. It verifies
        47    that the exact numbered CI build finished SUCCESS and that artifact SHA matches
        48    the Jenkins Git plugin revision. PR jobs are rejected and do not archive images.
        49    Do not allow users to create arbitrary jobs under `app-ci` or change the trusted job.
        50
        51    ## Jenkins setup (required before enabling webhooks)
        52
        53    1. Install Pipeline/Declarative, Git, GitHub Branch Source, Kubernetes,
        54       Credentials Binding, JUnit, Timestamper, Pipeline Utility Steps, HTTP Request,
        55       Copy Artifact, Pipeline Build Step, Basic Branch Build Strategies (for tags),
        56       Lockable Resources, and an authorization
        57       plugin (Role Strategy or equivalent). Use supported plugin versions and test
        58       the Declarative linter on your controller. Coverage XML is archived; a coverage
        59       visualization plugin is optional. Configure GitHub status reporting through
        60       Branch Source; require the actual emitted Jenkins context in GitHub rules.
        61    2. Create namespaces `jenkins-ci` and `jenkins-publish`. Configure cloud
        62       `kubernetes` for CI and `trusted-kubernetes` for the publisher. Use
        63       `ci/jenkins-controller-rbac.yaml` as an operator-reviewed starting point.
        64       Agent service accounts need **no RBAC** and do not mount API tokens. Revoke
        65       pre-existing Jenkins workload permissions in `dev` (including the historical
        66       `jenkins-agent` RoleBinding); changing a file does not revoke live RBAC.
        67       `k8s/rbac/jenkins-dev-rbac.yaml` and the old controller-dev RBAC file now define empty legacy Roles. Remove any other broad pre-existing controller grants too.
        68    3. Restrict the trusted cloud to the `trusted` folder using Kubernetes plugin
        69       cloud restrictions. Enforce admission restrictions on CI Pod creation:
        70       fixed CI namespace/node pool, no hostPath/host networking, no Secret mounts,
        71       no service-account token mounts, and no selection of privileged service
        72       accounts. Do not place application secrets in CI namespaces. Folder-scoped
        73       credentials alone do not secure a controller that can be tricked into creating
        74       arbitrary Pods in the publisher namespace. Test these denials explicitly.
        75    4. BuildKit remains privileged. Run CI on dedicated disposable worker nodes
        76       with no production workloads or credentials; privileged build containers can
        77       compromise their node. For hostile public PRs use a separate isolated build
        78       cluster/controller or do not enable fork PR execution until this boundary
        79       is in place. The publisher is unprivileged and must run on separate trusted
        80       nodes. Configure node scheduling through restricted cloud Pod templates and
        81       admission policy. Network-isolate workers from application databases and
        82       controller administration endpoints while allowing required agent traffic.
        83    5. Configure agent URL, e.g. `http://jenkins.jenkins.svc.cluster.local:8080`, and
        84       WebSocket or port 50000 connectivity. Set the controller's `JENKINS_URL` to an
        85       address reachable by its HTTP Request plugin. Both clouds require amd64 nodes.
        86       Python and Node containers have limits; BuildKit is limited to 2 CPU/2 GiB;
        87       isolated PostgreSQL 16 is loopback-only, without a Service, host port or PVC.
        88       Allow additional resources for the inbound agent and large image archives.
        89    6. Create multibranch job **`app-ci`** using GitHub Branch Source and script path
        90       `Jenkinsfile`. Discover repository branches, PRs (untrusted fork strategy),
        91       and tags. Enable the tag build strategy; tag discovery alone may not build
        92       tags. Use full checkout history, no shallow clone. Configure the GitHub webhook
        93       for push/PR/tag events and periodic indexing as a fallback. Checkout/scan
        94       credentials must be read-only; never global registry/Git write credentials.
        95    7. Create folder **`trusted`** and standalone Pipeline **`trusted/publish`**,
        96       Pipeline from SCM, branch `*/main`, script `Jenkinsfile.promote`, full clone.
        97       Restrict Configure/Replay/credential administration to CI administrators.
        98       It must never load its Jenkinsfile or helper scripts from a parameter, PR or
        99       release tag. Restrict Build permissions to the CI execution identity and
       100       operators. The CI job schedules this job asynchronously after success; the
       101       publisher waits for CI completion and fails unless its result is SUCCESS.
       102       Monitor the publisher job separately: a successful CI status does not prove
       103       publication or promotion succeeded. Retry with the original job/build number.
       104    8. Give the publisher Copy Artifact read access to `app-ci/*` through plugin
       105       permissions and Jenkins Job/Read + Job/Discover + artifact access. Configure
       106       authorization so build parameters cannot select jobs outside `app-ci`.
       107       PR names must retain the GitHub Branch Source `PR-<number>` convention.
       108    9. Create the credentials below **inside `trusted` only**. Configure Jenkins group
       109       `release-managers` for the input gate (or replace the submitter with your exact
       110       approved user/group IDs). Configure lock resource `fastapi-ghcr-gitops`; all
       111       publishers must share this resource and controller. No separate script may
       112       write these image tags or promote these overlays concurrently.
       113
       114    ### Credentials and external secrets
       115
       116    | ID/location | Type and exact purpose |
       117    | --- | --- |
       118    | `ghcr-write` in trusted | Username/password: GitHub machine account + PAT classic with `write:packages` (includes package read), authorized for the organization/SSO and both GHCR packages. No delete/admin permission. Avoid repository scope if your account setup permits; associate packages with the repository. |
       119    | `gitops-write` in trusted | Username/password: separate GitHub account/token, fine-grained token restricted to this repository, Contents read/write (and implicit Metadata read). Writes stage/dev commits and `release/*` branches; does not merge prod. No Actions, administration or package permissions. |
       120    | `ci-read` in trusted | Username/password: Jenkins service user/API token; Overall/Read, Job/Read/Discover on app-ci and artifact read only. HTTP Request uses it to verify build status/revision. No Build/Configure/admin permission is needed for this user. |
       121    | SCM discovery/checkout | Separate read-only GitHub credential; private repository contents read and discovery metadata. GitHub status reporting needs Commit statuses write or appropriate GitHub App Checks permission; do not reuse GitOps credentials. |
       122    | Optional future PR automation | Separate GitHub App installation/fine-grained token: this repository Pull requests read/write and Contents read. No credential is used by current code for PR creation; open the printed compare link manually. |
       123    | Argo repository access | Read-only deploy key or GitHub App credential in Argo CD if the repository is private. |
       124    | `ghcr-pull-secret`, each app namespace | Kubernetes dockerconfigjson with a distinct package-reader credential (`read:packages`), no push permission. |
       125    | `backend-secrets`, each app namespace | `SECRET_KEY`, `FIRST_SUPERUSER_PASSWORD`, `POSTGRES_PASSWORD`, optional `SMTP_PASSWORD`; unique strong values per environment. |
       126    | `db-secrets`, each app namespace | `POSTGRES_PASSWORD`, matching that environment's backend secret. |
       127    | `app-tls`, each app namespace | TLS certificate/key for the actual ingress hostname, issued by your certificate management system. |
       128
       129    The old `ghcr-creds` mounted Kubernetes Secret is not used by either pipeline.
       130    Only its manifest reference was inspected; no live Secret was read. Provision
       131    Jenkins credentials from your secret manager. Never paste real values into Git,
       132    job parameters, shell tracing, or documentation. Out-of-band app Secrets are
       133    intentionally outside Argo's managed/pruned resource set. The old sealed secrets
       134    are namespace/cluster-specific and cannot be reused in `app-*` unchanged.
       135
       136    ## Environments and immutable artifacts
       137
       138    - **Feature branches:** run all checks, build both image archives, publish through
       139      the trusted job to `sha-<40-character-SHA>`. No deployment by default. PR builds
       140      run checks/build validation with no publishing or write credentials.
       141    - **Dev:** run `trusted/publish`, `MODE=dev`, exact `CI_JOB` and `CI_BUILD` from a
       142      successful repository-branch build. An authorized release manager approves.
       143      Existing images are reused; missing images are copied from retained checked
       144      archives. Git changes only; Argo deploys. Retain archives until published.
       145    - **Stage:** a successful application-changing main build automatically publishes
       146      and writes its exact SHA/digests to stage. A superseded build cannot roll stage
       147      back. Argo deploys the Git change. Failed publish/promotion can be retried with
       148      the same numbered CI build; no image rebuild is needed.
       149    - **Prod:** discovered version tags schedule release mode; alternatively run
       150      `trusted/publish` with `MODE=release`, `RELEASE_TAG=vX.Y.Z`. An authorized input
       151      gate confirms that the digest pair actually ran successfully in stage. Jenkins
       152      verifies main ancestry, both SHA images and matching stage Git history, retags
       153      the existing digests, and pushes only `release/vX.Y.Z`. Open the printed compare
       154      link as a PR, obtain review, then merge. Argo automatically syncs after merge.
       155
       156    SHA tags are write-once **by publisher policy**, not a registry immutability
       157    feature. Existing tags are never overwritten, even on a repeated CI build. Both
       158    images are built before either is published. A partially completed upload is
       159    retryable; no environment changes until both images resolve. Kubernetes overlays
       160    record SHA tags **and digests**; Kustomize renders the digest as the authoritative
       161    image reference. Release tags may exist before the production PR is approved;
       162    creating a registry tag does not deploy it. Restrict GHCR writers and retention
       163    so deployed digests cannot be deleted. Digests prevent tag movement changing Pods.
       164
       165    Frontend images use an empty `VITE_API_URL`, so browser requests use the current
       166    origin. Ingress routes `/api` to FastAPI and `/` to nginx. Build-time hostnames
       167    must not vary by environment. Local Compose can still supply its API build arg.
       168    Backend probes use the existing `/api/v1/utils/health-check/`; it is a process
       169    health check, not a database readiness check. PostgreSQL has a readiness check.
       170    Argo sync waves create config/storage/database at -2, run the migration Sync hook
       171    at 0, and roll out backend/frontend at 1. A Sync hook allows first installation
       172    with database resources in earlier waves; a PreSync hook would run too soon.
       173    Migration failures block rollout. Use backwards-compatible migrations: old Pods
       174    remain serving during migrations. The retained single-instance PostgreSQL design
       175    is not HA; arrange backups/restore and appropriate storage before production.
       176    Adminer is preserved as an internal Service, without public ingress.
       177
       178    ### Recursion and concurrency
       179
       180    CI inspects the actual changed paths, not just `[skip ci]` text or author identity.
       181    Commits changing only `deploy/`, `argocd/` or Markdown render/validate overlays but
       182    skip application tests/build/archive/publication. This includes generated
       183    promotion commits and reviewed production overlay changes. Mixed source changes
       184    still build. Version tags never rebuild. Such GitOps/docs-only commits have no
       185    SHA image; release the recorded stage application SHA, not the subsequent bot SHA.
       186
       187    Both jobs disable concurrent builds per job. The publisher also takes a global
       188    lock for all registry and Git writes. Stage checks source freshness and monotonic
       189    Git ancestry, so a delayed older build cannot overwrite a newer promotion.
       190    Git writes use normal fast-forward pushes (no force) and retry after fetching
       191    and regenerating only the selected overlay, so unrelated concurrent main changes
       192    are preserved. Dev selection is explicit and serialized. Production uses a
       193    version-specific branch and GitHub review; require an up-to-date branch before
       194    merging, and reject obsolete release PRs. Historical promotion records remain in
       195    Git; `promotion.json` records SHA, digest pair and optional release version.
       196
       197    ## Release procedure
       198
       199    Tag the actual built application commit recorded by stage. A plain tag of main's
       200    latest bot commit intentionally fails because that commit has no built images.
       201
       202    ```bash
       203    git checkout main
       204    git pull --ff-only
       205    release_sha=$(python3 -c 'import json; print(json.load(open("deploy/overlays/stage/promotion.json"))["sha"])')
       206    git tag v1.2.0 "$release_sha"
       207    git push origin v1.2.0
       208    ```
       209
       210    Tag discovery schedules the trusted release process; approve its Jenkins input
       211    only after checking Argo `app-stage` is Healthy/Synced at the recorded digest pair
       212    and running the appropriate smoke tests. Jenkins deliberately has no Argo/cluster
       213    access and cannot verify runtime health itself. If discovery is unavailable,
       214    start release mode manually. Missing images or absent stage history fail closed.
       215    Jenkins opens no PR itself: follow its printed GitHub comparison link, create the
       216    PR and review the exact production digest/config diff. Do not merge an older
       217    release PR after a newer release. No image rebuild occurs during this procedure.
       218
       219    ## GitHub rules required
       220
       221    Protect main: require PR review, code-owner review, dismiss stale approvals,
       222    require approval of the last push, require the Jenkins CI status and up-to-date
       223    branches; prohibit force push and deletion. Add your real infrastructure/release
       224    team to CODEOWNERS for `Jenkinsfile*`, `ci/`, `deploy/`, `argocd/`, Dockerfiles,
       225    `.github/`, and especially all production-affecting shared base resources. No
       226    placeholder CODEOWNERS is supplied because the actual authorized team is unknown.
       227    Changes to the shared base affect prod immediately after merge and require the
       228    same production review as the prod overlay. Limit ruleset bypass to the dedicated
       229    GitOps machine account needed for automatic stage/dev commits; no human/developer
       230    bypass. That account's trusted code writes only the intended overlay. GitHub does
       231    not provide a path-scoped Contents-write token: compromise of this bypass account
       232    can change prod or pipeline code. If this residual risk is unacceptable, use a
       233    separate stage/dev GitOps repository or an independently enforcing GitHub App
       234    before enabling automatic direct commits. Restrict token access and audit usage.
       235
       236    Protect `v*` tags with rulesets: only release managers may create them; forbid
       237    updates/deletion. Allow the GitOps writer to create short-lived `release/*`
       238    branches, but never auto-merge them. Configure webhooks and required status names
       239    from an observed Jenkins run. Old GitHub Actions deployment workflows are renamed
       240    `.yml.disabled`; other template maintenance/test workflows remain supplemental,
       241    not the deployment authority. Review their secrets separately, especially the
       242    legacy generated-client workflow's write token. Jenkins remains required CI.
       243
       244    ## Argo CD bootstrap and rollback
       245
       246    See [deployment.md](deployment.md) for operator-only bootstrap, prerequisites,
       247    rollbacks and legacy-manifest migration. No bootstrap command is run by Jenkins.
       248
       249    ## Verification and operating limits
       250
       251    Local results are recorded in [ci/VERIFICATION.md](ci/VERIFICATION.md). Before live
       252    use, validate both pipelines with your controller's Declarative linter, then run
       253    a non-production acceptance exercise covering: PR credential denial, feature
       254    publish, repeated SHA publication, main promotion, GitOps recursion, overlapping
       255    main builds, missing-image release failure, release approval and prod PR review.
       256    Use a registry read/write sandbox for this exercise. Monitor both CI and publisher
       257    jobs plus Argo application health. Jenkins build retention is 30 CI builds/10
       258    archive sets and 100 publisher builds; configure adequate artifact storage.
       259
       260    Tools are downloaded from fixed upstream releases with fixed archive SHA256s;
       261    kubeconform also needs access to its upstream Kubernetes schema repository. For
       262    fully offline validation, mirror schemas/tools internally and pin that mirror.
       263    Base/agent images use explicit versions but are not digest pinned, and their age
       264    is not a security-support guarantee; maintain reviewed updates and scan images.
       265    No image signing or vulnerability gate has been added in this change.
         1    # Argo CD deployment
         2
         3    The production path is [GitHub Flow + Jenkins + GHCR + Argo CD](README-jenkins.md).
         4    Jenkins never applies application resources. Git `main`, `deploy/overlays/{dev,stage,prod}`,
         5    is desired state. `k8s/` is a retained legacy example, not an active deployment root.
         6    Do not apply both manifest trees to the same workload. Compose remains a separate
         7    local development tool, not this project's production CD system.
         8
         9    ## One-time operator bootstrap
        10
        11    Do not run these steps until the changes have been reviewed/merged, Jenkins trust
        12    boundaries configured, and real hostnames/secrets/storage prepared. These commands
        13    are instructions only; no real cluster was changed during implementation.
        14
        15    1. Install a supported, organization-approved Argo CD version, including its
        16       ApplicationSet controller, or connect to your existing installation. Download
        17       and review the exact release manifests (never an unpinned `stable` URL), e.g.:
        18
        19       ```bash
        20       export ARGOCD_VERSION='<approved-version>'
        21       curl -fL "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml" -o /tmp/argocd-install.yaml
        22       # Review the downloaded manifest before the next commands.
        23       kubectl create namespace argocd
        24       kubectl apply -n argocd -f /tmp/argocd-install.yaml
        25       ```
        26
        27       Skip installation if Argo already exists. Configure SSO/RBAC and restrict
        28       Application/AppProject writes and sync overrides to platform administrators.
        29       Ordinary users must not override main, image parameters or the production
        30       source path. Register a read-only repository credential in Argo for private Git.
        31    2. Create `app-dev`, `app-stage`, `app-prod` namespaces outside the ApplicationSet:
        32
        33       ```bash
        34       kubectl create namespace app-dev
        35       kubectl create namespace app-stage
        36       kubectl create namespace app-prod
        37       ```
        38
        39       Provision `backend-secrets`, `db-secrets`, `ghcr-pull-secret`, and `app-tls`
        40       securely in each namespace. See the exact key/permission table in
        41       README-jenkins.md. Use an external secret manager or newly sealed namespace-
        42       specific secrets; never commit generated plaintext YAML. Configure Traefik,
        43       DNS and valid TLS certificates for real hosts replacing `*.example.com` in
        44       overlays. The AppProject cannot create Namespaces, Secrets or cluster RBAC.
        45    3. Choose the cluster's storage class and capacity, backup/restore and database
        46       ownership. The base retains a 1Gi default-class RWO PVC and a single PostgreSQL
        47       Deployment using Recreate to avoid concurrent writers. PVC deletion/pruning
        48       is disabled in Argo annotations; do not assume this substitutes for backups.
        49       Migrating existing `dev` data into `app-dev` requires an explicit operator data
        50       migration plan. No existing namespace/data is adopted or deleted automatically.
        51    4. Complete the Jenkins setup, publish real images, and promote dev/stage. Initial
        52       overlay tags are deliberately all-zero SHA placeholders and will not pull.
        53       Before enabling each Argo application, replace that environment's placeholder
        54       through its normal promotion flow; production still needs a reviewed release.
        55       For phased bootstrap, temporarily list only provisioned environments in the
        56       ApplicationSet through a reviewed Git change, adding prod after approval.
        57    5. Review and apply the AppProject/ApplicationSet as an administrator:
        58
        59       ```bash
        60       kubectl apply -f argocd/project.yaml
        61       kubectl apply -f argocd/applicationset.yaml
        62       ```
        63
        64       They define `app-dev`, `app-stage`, `app-prod` against the in-cluster API,
        65       tracking only this repository's main. All automatically sync, prune and
        66       self-heal **after** Git approval. For an external cluster update both
        67       destination definitions and register that cluster with Argo first.
        68    6. Verify actual Argo sync/health, image digests and migrations in dev/stage before
        69       production. Set up alerting for failed hooks, sync failures and missing Secrets.
        70       Normal subsequent application deployment requires only Git changes.
        71
        72    ## Rollback
        73
        74    Revert the offending overlay promotion commit in a reviewed PR, restoring both
        75    `kustomization.yaml` SHA/digests and `promotion.json` together, or explicitly set
        76    both to a previously recorded artifact pair. Merge to main; Argo detects the
        77    reverted desired state and reconciles it. No image rebuild or Jenkins cluster
        78    command is needed. A new main build can subsequently advance stage again.
        79
        80    For production, review the rollback PR under the same rules as a release. Avoid
        81    Argo UI rollback/parameter overrides while auto-sync is enabled: Git would restore
        82    the declared state. Database migrations are not automatically reversible; verify
        83    schema compatibility before reverting application images and use your separately
        84    approved restore/migration procedure when necessary. Keep old image digests in GHCR.
        85
        86    ## References
        87
        88    - [Argo sync phases/waves and hooks](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
        89    - [Jenkins credentials and untrusted pipelines](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
        90    - [GHCR digest-based pulls](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
         1    # Recovery and backup checklist
         2
         3    2026-10-09 UTC. Minikube was deleted by the operator before this rebuild. Do not recreate it.
         4
         5    | Item | Found / recoverable | Action |
         6    | --- | --- | --- |
         7    | Sealed Secrets private key | `sealed-secrets-key-backup.yaml`, one kube-system key Secret | Restricted to 0600, excluded from Git; restored into kind before controller startup |
         8    | Key validation | Certificate SHA256 `0B:89:57:D5:50:6D:48:76:16:B6:FD:8A:2D:74:D8:9A:49:12:59:95:4A:6D:57:C9:AB:18:0D:A8:0C:E2:22:7B` | Offline recovery of backend/database ciphertext succeeded; live app-dev decryption succeeded |
         9    | Legacy encrypted backend/database secrets | `k8s/overlays/dev/sealed-secret-{backend,db}.yaml` | Recovered only in memory; resealed for app-dev in `infra/kind/secrets/app-dev/` |
        10    | Legacy frontend SealedSecret | Empty file | No encrypted content; initial kubeseal success on empty input was not a meaningful test. Active frontend has no frontend Secret dependency |
        11    | GHCR access | Existing host `~/.docker/config.json` contains ghcr.io auth | Only that registry entry restored to app-dev/app-stage; no credentials printed or committed. Anonymous access is unauthorized |
        12    | STAGE backend/database secrets | Fresh credentials created with explicit user authorization | Encrypted SealedSecrets saved in infra/kind/secrets/app-stage; passwords match and differ from DEV. Admin password fits the application 40-character maximum. No plaintext files or values printed |
        13    | STAGE TLS | No backup identified; standard overlay references app-tls | Local kind HTTP override removes this dependency; preserve HTTPS/TLS design for later proper certificate provisioning |
        14    | Argo repository credentials | No backup identified | Public Git repository main is accessible; supply read-only access if made private |
        15    | Jenkins home | No archive identified; host Jenkins inactive/not installed | Old controller jobs/plugins/credentials/build history cannot be recovered from Git alone |
        16    | PostgreSQL data | Old PVC data gone, no dump identified | Intentionally disposable: new PVCs/init/migrations recreate test databases; old rows are not restored |
        17    | Monitoring data | Previous rollout paused; no monitoring PVC observed in historical report | Recreate short-retention history when rollout is safe |
        18
        19    Do not commit private material. `.migration-backup/`, `.tools/`, and `sealed-secrets-key-backup.yaml` are ignored. Existing private PEM in `.migration-backup/` is 0600 within a 0700 directory. Store an additional encrypted/off-host copy of the key; the ignored working copy alone is not disaster recovery. No private key or plaintext secret values were printed.
        20
        21    For another engineer, securely supply the key backup, package-reader registry access and namespace-specific application secrets. Run `scripts/recover-dev-secrets.py` to regenerate encrypted app-dev Secrets from the old ciphertext/key. Restoring the key alone cannot recreate live-only STAGE/registry/TLS credentials.
        22
        23    Future key export (run against kind, outside a build log):
        24
        25    ```bash
        26    umask 077
        27    mkdir -p .migration-backup
        28    chmod 700 .migration-backup
        29    kubectl --context kind-fastapi-dev get secret -n kube-system \
        30      -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml \
        31      > .migration-backup/sealed-secrets-keys.yaml
        32    chmod 600 .migration-backup/sealed-secrets-keys.yaml
        33    ```
        34
        35    Export every key after rotation; retain older keys needed by ciphertext. Do not print/cat these files.
        36
        37    Future Jenkins backup: put the controller in quiet mode, wait for running builds, stop the controller for a consistent backup, and archive all of `JENKINS_HOME` (jobs, plugins, credentials.xml, secrets/master.key, secrets/hudson.util.Secret, users, config.xml, build archives). Encrypt the archive and preserve ownership. Credentials require the matching Jenkins encryption files. Restart after backup. No such old backup was found; none was fabricated.
        38
        39    Jenkins follow-up: discovered /home/root-admin/jenkins-values.yaml and cached jenkins-5.9.56.tgz. Preserved copies under ignored .migration-backup/jenkins (0700 directory/0600 files). These recover partial install settings/chart, not JENKINS_HOME, jobs/history/plugin inventory or encrypted credentials. The remaining Docker volume belongs to current kind and was left untouched. See JENKINS_RECOVERY_REPORT.md.
    #! /usr/bin/env sh

    # Exit in case of error
    set -e

    TAG=${TAG?Variable not set} \
    FRONTEND_ENV=${FRONTEND_ENV-production} \
    docker-compose \
    -f docker-compose.yml \
    build
    #! /usr/bin/env sh

    # Exit in case of error
    set -e

    TAG=${TAG?Variable not set} \
    FRONTEND_ENV=${FRONTEND_ENV-production} \
    sh ./scripts/build.sh

    docker-compose -f docker-compose.yml push
    #! /usr/bin/env sh

    # Exit in case of error
    set -e

    DOMAIN=${DOMAIN?Variable not set} \
    STACK_NAME=${STACK_NAME?Variable not set} \
    TAG=${TAG?Variable not set} \
    docker-compose \
    -f docker-compose.yml \
    config > docker-stack.yml

    docker-auto-labels docker-stack.yml

    docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
    #! /usr/bin/env sh

    # Exit in case of error
    set -e
    set -x

    docker compose build
    docker compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
    docker compose up -d
    docker compose exec -T backend bash scripts/tests-start.sh "$@"
    docker compose down -v --remove-orphans
    #! /usr/bin/env bash

    # Exit in case of error
    set -e

    docker-compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

    if [ $(uname -s) = "Linux" ]; then
        echo "Remove __pycache__ files"
        sudo find . -type d -name __pycache__ -exec rm -r {} \+
    fi

    docker-compose build
    docker-compose up -d
    docker-compose exec -T backend bash scripts/tests-start.sh "$@"
    # Legacy controller access to the application namespace is retired.
    # Operator must apply/revoke the existing live role during migration.
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: jenkins-controller-agent-manager
      namespace: dev
    rules: []
    # Legacy role intentionally grants no permissions. See README-jenkins.md.
    # Existing cluster bindings must be revoked by an administrator during migration.
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: jenkins-agent
      namespace: dev
    rules: []
    # Apply only during operator-led bootstrap; never from Jenkins pipelines.
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: jenkins-agent-manager
      namespace: jenkins-ci
    rules:
      - apiGroups: ['']
        resources: [pods, pods/log, pods/exec]
        verbs: [get, list, watch, create, delete, patch, update]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: jenkins-agent-manager
      namespace: jenkins-ci
    subjects:
      - kind: ServiceAccount
        name: jenkins
        namespace: jenkins
    roleRef:
      kind: Role
      name: jenkins-agent-manager
      apiGroup: rbac.authorization.k8s.io
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: jenkins-agent-manager
      namespace: jenkins-publish
    rules:
      - apiGroups: ['']
        resources: [pods, pods/log, pods/exec]
        verbs: [get, list, watch, create, delete, patch, update]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: jenkins-agent-manager
      namespace: jenkins-publish
    subjects:
      - kind: ServiceAccount
        name: jenkins
        namespace: jenkins
    roleRef:
      kind: Role
      name: jenkins-agent-manager
      apiGroup: rbac.authorization.k8s.io
    #!/usr/bin/env python3
    """Render an Argo Helm bootstrap while monitoring Git files remain unpublished.

    Requires PyYAML. Writes only a credential-free Application to stdout.
    After the reviewed Git merge, apply argocd/app-monitoring.yaml instead.
    This is an operator bootstrap helper, not a CI pipeline or Helm installer.
    """
    import copy
    from pathlib import Path
    import yaml

    root = Path(__file__).resolve().parent.parent

    def load(relative):
        return yaml.safe_load((root / relative).read_text())

    app = load('argocd/app-monitoring.yaml')
    values = load('monitoring/values.yaml')
    values['prometheus']['additionalServiceMonitors'] = [
        {'name': item['metadata']['name'], **item['spec']}
        for item in yaml.safe_load_all((root / 'monitoring/monitors/argocd.yaml').read_text())
    ]
    monitor = load('monitoring/monitors/traefik.yaml')
    values['prometheus']['additionalPodMonitors'] = [
        {'name': monitor['metadata']['name'], **monitor['spec']}
    ]
    rule = load('monitoring/rules/dev-stage.yaml')
    values['additionalPrometheusRulesMap'] = {rule['metadata']['name']: rule['spec']}
    dashboard = load('monitoring/dashboards/platform.yaml')
    values['grafana']['dashboards'] = {
        'default': {
            name.removesuffix('.json'): {'json': contents}
            for name, contents in dashboard['data'].items()
        }
    }
    values['grafana']['dashboardProviders'] = {
        'dashboardproviders.yaml': {
            'apiVersion': 1,
            'providers': [{
                'name': 'bootstrap', 'orgId': 1, 'folder': 'DEV-STAGE',
                'type': 'file', 'disableDeletion': True, 'editable': False,
                'options': {'path': '/var/lib/grafana/dashboards/default'},
            }],
        }
    }
    source = copy.deepcopy(app['spec'].pop('sources')[0])
    source['helm'].pop('valueFiles')
    source['helm']['valuesObject'] = values
    app['spec']['source'] = source
    # A fresh bootstrap always pauses; activation requires the explicit capacity phase.
    app['metadata'].setdefault('annotations', {})['argocd.argoproj.io/skip-reconcile'] = 'true'
    app['spec']['syncPolicy']['automated']['enabled'] = False
    print(yaml.safe_dump(app, sort_keys=False), end='')
    #!/usr/bin/env python3
    """Create the monitoring admin Secret if absent; never print or persist credentials."""
    import json
    import secrets
    import subprocess

    kubectl = ['kubectl', '--context', 'kind-fastapi-dev', '-n', 'monitoring']
    name = 'monitoring-grafana-admin'
    result = subprocess.run(kubectl + ['get', 'secret', name, '--ignore-not-found', '-o', 'json'],
                            check=True, capture_output=True, text=True)
    if result.stdout.strip():
        data = json.loads(result.stdout).get('data', {})
        if not all(data.get(key) for key in ('admin-user', 'admin-password')):
            raise SystemExit('Existing Grafana Secret lacks required keys; left unchanged.')
        print('Existing Grafana admin Secret preserved.')
    else:
        secret = {'apiVersion': 'v1', 'kind': 'Secret', 'type': 'Opaque',
                  'metadata': {'name': name, 'namespace': 'monitoring'},
                  'stringData': {'admin-user': 'admin', 'admin-password': secrets.token_urlsafe(32)}}
        # stdin avoids exposing the password through process arguments or files.
        result = subprocess.run(kubectl + ['create', '-f', '-'], input=json.dumps(secret),
                                capture_output=True, text=True)
        if result.returncode:
            raise SystemExit('Grafana Secret creation failed; no credential output retained.')
        print('Grafana admin Secret created; credentials stored only in Kubernetes.')
    #!/usr/bin/env python3
    """Verify login and all provisioned dashboard queries using a normal login session."""
    import base64
    import http.cookiejar
    import json
    from pathlib import Path
    import subprocess
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    import yaml

    kubectl = ['kubectl', '--context', 'kind-fastapi-dev', '-n', 'monitoring']
    base = 'http://127.0.0.1:13001'

    def request(opener, path, body=None):
        req = urllib.request.Request(base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={'Content-Type': 'application/json'} if body is not None else {})
        return opener.open(req, timeout=30)

    def get_json(opener, path, body=None):
        with request(opener, path, body) as response:
            assert response.status == 200
            return json.load(response)

    service = json.loads(subprocess.check_output(kubectl + ['get', 'svc', 'monitoring-grafana', '-o', 'json']))
    assert service['spec']['type'] == 'ClusterIP'
    assert not service['spec'].get('externalIPs')
    ingresses = json.loads(subprocess.check_output(kubectl + ['get', 'ingress', '-o', 'json']))
    assert not ingresses['items'], 'Unexpected monitoring ingress'
    subprocess.run(kubectl + ['rollout', 'status', 'deployment/monitoring-grafana', '--timeout=180s'], check=True)
    secret = json.loads(subprocess.check_output(kubectl + ['get', 'secret', 'monitoring-grafana-admin', '-o', 'json']))['data']
    credentials = {key: base64.b64decode(secret[field]).decode() for key, field in
                   [('user', 'admin-user'), ('password', 'admin-password')]}
    forward = subprocess.Popen(kubectl + ['port-forward', '--address=127.0.0.1',
                               'svc/monitoring-grafana', '13001:80'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        anonymous = urllib.request.build_opener()
        for attempt in range(30):
            try:
                get_json(anonymous, '/api/health')
                break
            except (OSError, urllib.error.URLError):
                if attempt == 29:
                    raise
                time.sleep(1)
        docs = yaml.safe_load((Path(__file__).parent / 'dashboards/platform.yaml').read_text())['data']
        dashboards = [json.loads(contents) for contents in docs.values()]
        for path in ['/api/search?type=dash-db', '/api/datasources/uid/prometheus',
                     '/api/dashboards/uid/' + dashboards[0]['uid'], '/api/ds/query']:
            try:
                request(anonymous, path, {'queries': []} if path == '/api/ds/query' else None)
            except urllib.error.HTTPError as error:
                assert error.code == 401, (path, error.code)
            else:
                raise AssertionError('Anonymous access permitted: ' + path)
        with request(anonymous, '/d/' + dashboards[0]['uid']) as response:
            assert urllib.parse.urlparse(response.url).path == '/login'
        with request(anonymous, '/login') as response:
            page = response.read().decode()
            assert '"disableLoginForm":false' in page.replace(' ', '')
        print('Anonymous APIs: 401; dashboard redirects to /login; login form enabled.')
        session = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        get_json(session, '/login', credentials)
        assert get_json(session, '/api/user')['login'] == credentials['user']
        del credentials, secret
        datasource = get_json(session, '/api/datasources/uid/prometheus')
        assert datasource['uid'] == 'prometheus'
        assert datasource['url'] == 'http://monitoring-prometheus.monitoring.svc.cluster.local:9090'
        search = get_json(session, '/api/search?type=dash-db')
        assert {item['uid'] for item in search} >= {item['uid'] for item in dashboards}
        for desired in dashboards:
            live = get_json(session, '/api/dashboards/uid/' + desired['uid'])
            assert live['meta']['provisioned'] is True
            assert live['dashboard']['panels'] == desired['panels']
            checks = 0
            for panel in live['dashboard']['panels']:
                for target in panel.get('targets', []):
                    expr = target.get('expr')
                    if not expr:
                        continue
                    for namespace in (['app-dev', 'app-stage'] if '$namespace' in expr else ['']):
                        body = {'queries': [{'refId': 'A', 'expr': expr.replace('$namespace', namespace),
                            'instant': True, 'range': False, 'datasource': {'uid': 'prometheus', 'type': 'prometheus'},
                            'format': 'time_series', 'intervalMs': 60000, 'maxDataPoints': 100}],
                            'from': 'now-5m', 'to': 'now'}
                        result = get_json(session, '/api/ds/query', body)['results']['A']
                        assert not result.get('error'), (desired['uid'], panel['title'])
                        assert any(any(values for values in frame.get('data', {}).get('values', []))
                                   for frame in result.get('frames', [])), (desired['uid'], panel['title'])
                        checks += 1
            print('Authenticated dashboard', desired['uid'], checks, 'queries returned data; panels preserved.')
        print('PASS: normal login session, Prometheus datasource, four dashboards; ClusterIP, no ingress.')
    finally:
        forward.terminate()
        try:
            forward.wait(timeout=5)
        except subprocess.TimeoutExpired:
            forward.kill()
            forward.wait()
    ✓ • 0ms

## Activity

    $ docker info --format '{{.ServerVersion}}'; docker ps --format '{{.Names}} {{.Status}}'; docker image ls --format '{{.Repository}}:{{.Tag}}'; kubectl config current-context; kubectl --context kind-fastapi-dev --request-timeout=15s get pods,pvc -A; kubectl --context kind-fastapi-dev --request-timeout=15s get applications -n argocd; ls -l /tmp/ci-bin .tools/kustomize .tools/kubeconform .tools/promtool backend/.venv/bin/python 2>/dev/null; backend/.venv/bin/python -c 'import pytest,yaml; print("pytest",pytest.__version__)'
    29.1.3
    host-jenkins-agent Up 2 days
    host-jenkins-docker Up 2 days
    host-jenkins Up 2 days
    fastapi-dev-control-plane Up 2 days
    fastapi-gitops-local/frontend:verification
    fastapi-gitops-local/backend:verification
    postgres:16
    jenkins/jenkins:2.568.3-jdk21
    kindest/node:<none>
    ghcr.io/fastapi-traefik-devops/fastapi-frontend:v0.1.0
    ghcr.io/fastapi-traefik-devops/fastapi-backend:v0.1.0
    python:3.10
    gcr.io/k8s-minikube/kicbase:v0.0.50
    gcr.io/k8s-minikube/kicbase:<none>
    docker:29.1.3-dind
    ghcr.io/astral-sh/uv:0.5.11-python3.10-bookworm-slim
    ghcr.io/astral-sh/uv:0.5.11
    node:20.18.1
    groovy:4.0.24-jdk17
    kind-fastapi-dev
    NAMESPACE            NAME                                                    READY   STATUS    RESTARTS        AGE
    app-dev              pod/adminer-7cb5cfdc97-smhcd                            1/1     Running   0               2d17h
    app-dev              pod/backend-86c5779498-8vb78                            1/1     Running   0               2d17h
    app-dev              pod/frontend-b5ffb8544-7hbbg                            1/1     Running   0               2d17h
    app-dev              pod/postgres-deployment-5bb8bcc84b-qhxpq                1/1     Running   0               2d17h
    app-stage            pod/adminer-7cb5cfdc97-cmv2p                            1/1     Running   0               2d17h
    app-stage            pod/backend-86c5779498-s68k6                            1/1     Running   0               2d17h
    app-stage            pod/frontend-b5ffb8544-h4l4b                            1/1     Running   0               2d17h
    app-stage            pod/postgres-deployment-5bb8bcc84b-8pshh                1/1     Running   0               2d17h
    argocd               pod/argocd-application-controller-0                     1/1     Running   0               2d18h
    argocd               pod/argocd-applicationset-controller-5c66f59556-9zlfz   1/1     Running   0               2d18h
    argocd               pod/argocd-dex-server-64cc54b998-cmzzc                  1/1     Running   0               2d18h
    argocd               pod/argocd-notifications-controller-68d59788b7-2jv6m    1/1     Running   0               2d18h
    argocd               pod/argocd-redis-7f877d46b7-42f8g                       1/1     Running   0               2d18h
    argocd               pod/argocd-repo-server-7bc46c4ddf-4x7t7                 1/1     Running   0               2d18h
    argocd               pod/argocd-server-57bf79bfcc-zf9vd                      1/1     Running   0               2d18h
    kube-system          pod/coredns-7d764666f9-62vgl                            1/1     Running   0               2d18h
    kube-system          pod/coredns-7d764666f9-cjxww                            1/1     Running   0               2d18h
    kube-system          pod/etcd-fastapi-dev-control-plane                      1/1     Running   0               2d18h
    kube-system          pod/kindnet-mrlqc                                       1/1     Running   0               2d18h
    kube-system          pod/kube-apiserver-fastapi-dev-control-plane            1/1     Running   0               2d18h
    kube-system          pod/kube-controller-manager-fastapi-dev-control-plane   1/1     Running   1 (2d17h ago)   2d18h
    kube-system          pod/kube-proxy-g297s                                    1/1     Running   0               2d18h
    kube-system          pod/kube-scheduler-fastapi-dev-control-plane            1/1     Running   1 (2d17h ago)   2d18h
    kube-system          pod/metrics-server-67cbccccd9-q9h25                     1/1     Running   0               2d18h
    kube-system          pod/sealed-secrets-controller-54d84bf77c-hjvpm          1/1     Running   0               2d17h
    local-path-storage   pod/local-path-provisioner-67b778fdf6-pjsgw             1/1     Running   0               2d18h
    monitoring           pod/alertmanager-monitoring-alertmanager-0              2/2     Running   0               2d17h
    monitoring           pod/monitoring-grafana-55bc98bcf-479t8                  2/2     Running   0               2d12h
    monitoring           pod/monitoring-kube-state-metrics-94cb77c4-lcjk9        1/1     Running   0               2d17h
    monitoring           pod/monitoring-operator-56747f885c-lkwdt                1/1     Running   0               2d17h
    monitoring           pod/monitoring-prometheus-node-exporter-wlxvs           1/1     Running   0               2d17h
    monitoring           pod/prometheus-monitoring-prometheus-0                  2/2     Running   0               2d17h
    traefik              pod/traefik-6cbd84cf4d-v9fwt                            1/1     Running   0               2d17h

    NAMESPACE    NAME                                                                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
    app-dev      persistentvolumeclaim/postgres-vol                                                                     Bound    pvc-5f34e36a-4091-410c-8fe8-c3a51f78acb2   1Gi        RWO            standard       <unset>                 2d17h
    app-stage    persistentvolumeclaim/postgres-vol                                                                     Bound    pvc-a98c3ace-963e-4845-893b-0cc291e32b0d   1Gi        RWO            standard       <unset>                 2d17h
    monitoring   persistentvolumeclaim/alertmanager-monitoring-alertmanager-db-alertmanager-monitoring-alertmanager-0   Bound    pvc-dd437321-80eb-44da-a707-34bbe2db8b37   256Mi      RWO            standard       <unset>                 2d17h
    monitoring   persistentvolumeclaim/prometheus-monitoring-prometheus-db-prometheus-monitoring-prometheus-0           Bound    pvc-aa651d39-fb03-4c52-917e-2ecb37d09472   2Gi        RWO            standard       <unset>                 2d17h
    NAME         SYNC STATUS   HEALTH STATUS
    app-dev      Synced        Healthy
    app-stage    Synced        Healthy
    monitoring   Synced        Healthy
    -rwxr-xr-x 1 root-admin root-admin 119146763 Oct  9 18:53 .tools/promtool
    lrwxrwxrwx 1 root       root              22 Oct  3 11:30 backend/.venv/bin/python -> /usr/local/bin/python3

    /tmp/ci-bin:
    total 35572
    -rwxr-xr-x 1 root-admin root-admin 10838168 Jan 15  2025 crane
    -rwxr-xr-x 1 root-admin root-admin 11163270 Jul 30  2024 kubeconform
    -rwxr-xr-x 1 root-admin root-admin 14413976 Jan 14  2025 kustomize
    /bin/bash: line 1: backend/.venv/bin/python: No such file or directory
    ✗ (127) • 11.64s

## Assistant

Die Implementierung enthält brauchbare Probes, Ressourcenlimits, getrennte Namespaces und digestgebundene Dev-/Stage-Images. Die größten bisherigen Lücken sind Terraform, ein ausführbarer Prod-Aufbau, automatisches Dev-Deployment und Datenbank-Backups. Bei CI/CD fällt zusätzlich auf: Die lokale Jenkins-Wiederherstellung konfiguriert die eigentlichen Build- und Publish-Jobs ausdrücklich als deaktiviert.

## Activity

    $ kubectl config current-context; kubectl --context kind-fastapi-dev --request-timeout=10s get pods,pvc -A; kubectl --context kind-fastapi-dev --request-timeout=10s get applications -n argocd; ls -l /tmp/ci-bin .tools/kustomize .tools/kubeconform .tools/promtool backend/.venv/bin/python 2>/dev/null; backend/.venv/bin/python -c 'import pytest; print(pytest.__version__)'; python3 -c 'import yaml; print(yaml.__version__)'
    kind-fastapi-dev
    NAMESPACE            NAME                                                    READY   STATUS    RESTARTS        AGE
    app-dev              pod/adminer-7cb5cfdc97-smhcd                            1/1     Running   0               2d17h
    app-dev              pod/backend-86c5779498-8vb78                            1/1     Running   0               2d17h
    app-dev              pod/frontend-b5ffb8544-7hbbg                            1/1     Running   0               2d17h
    app-dev              pod/postgres-deployment-5bb8bcc84b-qhxpq                1/1     Running   0               2d17h
    app-stage            pod/adminer-7cb5cfdc97-cmv2p                            1/1     Running   0               2d17h
    app-stage            pod/backend-86c5779498-s68k6                            1/1     Running   0               2d17h
    app-stage            pod/frontend-b5ffb8544-h4l4b                            1/1     Running   0               2d17h
    app-stage            pod/postgres-deployment-5bb8bcc84b-8pshh                1/1     Running   0               2d17h
    argocd               pod/argocd-application-controller-0                     1/1     Running   0               2d18h
    argocd               pod/argocd-applicationset-controller-5c66f59556-9zlfz   1/1     Running   0               2d18h
    argocd               pod/argocd-dex-server-64cc54b998-cmzzc                  1/1     Running   0               2d18h
    argocd               pod/argocd-notifications-controller-68d59788b7-2jv6m    1/1     Running   0               2d18h
    argocd               pod/argocd-redis-7f877d46b7-42f8g                       1/1     Running   0               2d18h
    argocd               pod/argocd-repo-server-7bc46c4ddf-4x7t7                 1/1     Running   0               2d18h
    argocd               pod/argocd-server-57bf79bfcc-zf9vd                      1/1     Running   0               2d18h
    kube-system          pod/coredns-7d764666f9-62vgl                            1/1     Running   0               2d18h
    kube-system          pod/coredns-7d764666f9-cjxww                            1/1     Running   0               2d18h
    kube-system          pod/etcd-fastapi-dev-control-plane                      1/1     Running   0               2d18h
    kube-system          pod/kindnet-mrlqc                                       1/1     Running   0               2d18h
    kube-system          pod/kube-apiserver-fastapi-dev-control-plane            1/1     Running   0               2d18h
    kube-system          pod/kube-controller-manager-fastapi-dev-control-plane   1/1     Running   1 (2d17h ago)   2d18h
    kube-system          pod/kube-proxy-g297s                                    1/1     Running   0               2d18h
    kube-system          pod/kube-scheduler-fastapi-dev-control-plane            1/1     Running   1 (2d17h ago)   2d18h
    kube-system          pod/metrics-server-67cbccccd9-q9h25                     1/1     Running   0               2d18h
    kube-system          pod/sealed-secrets-controller-54d84bf77c-hjvpm          1/1     Running   0               2d17h
    local-path-storage   pod/local-path-provisioner-67b778fdf6-pjsgw             1/1     Running   0               2d18h
    monitoring           pod/alertmanager-monitoring-alertmanager-0              2/2     Running   0               2d17h
    monitoring           pod/monitoring-grafana-55bc98bcf-479t8                  2/2     Running   0               2d12h
    monitoring           pod/monitoring-kube-state-metrics-94cb77c4-lcjk9        1/1     Running   0               2d17h
    monitoring           pod/monitoring-operator-56747f885c-lkwdt                1/1     Running   0               2d17h
    monitoring           pod/monitoring-prometheus-node-exporter-wlxvs           1/1     Running   0               2d17h
    monitoring           pod/prometheus-monitoring-prometheus-0                  2/2     Running   0               2d17h
    traefik              pod/traefik-6cbd84cf4d-v9fwt                            1/1     Running   0               2d17h

    NAMESPACE    NAME                                                                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
    app-dev      persistentvolumeclaim/postgres-vol                                                                     Bound    pvc-5f34e36a-4091-410c-8fe8-c3a51f78acb2   1Gi        RWO            standard       <unset>                 2d17h
    app-stage    persistentvolumeclaim/postgres-vol                                                                     Bound    pvc-a98c3ace-963e-4845-893b-0cc291e32b0d   1Gi        RWO            standard       <unset>                 2d17h
    monitoring   persistentvolumeclaim/alertmanager-monitoring-alertmanager-db-alertmanager-monitoring-alertmanager-0   Bound    pvc-dd437321-80eb-44da-a707-34bbe2db8b37   256Mi      RWO            standard       <unset>                 2d17h
    monitoring   persistentvolumeclaim/prometheus-monitoring-prometheus-db-prometheus-monitoring-prometheus-0           Bound    pvc-aa651d39-fb03-4c52-917e-2ecb37d09472   2Gi        RWO            standard       <unset>                 2d17h
    NAME         SYNC STATUS   HEALTH STATUS
    app-dev      Synced        Healthy
    app-stage    Synced        Healthy
    monitoring   Synced        Healthy
    -rwxr-xr-x 1 root-admin root-admin 119146763 Oct  9 18:53 .tools/promtool
    lrwxrwxrwx 1 root       root              22 Oct  3 11:30 backend/.venv/bin/python -> /usr/local/bin/python3

    /tmp/ci-bin:
    total 35572
    -rwxr-xr-x 1 root-admin root-admin 10838168 Jan 15  2025 crane
    -rwxr-xr-x 1 root-admin root-admin 11163270 Jul 30  2024 kubeconform
    -rwxr-xr-x 1 root-admin root-admin 14413976 Jan 14  2025 kustomize
    /bin/bash: line 1: backend/.venv/bin/python: No such file or directory
    6.0.1
    ✓ • 973ms

## Activity

    $ python3 - <<'PY'
        from pathlib import Path
        import subprocess,re,yaml,base64
        files=subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines()
        for name in dict.fromkeys(files):
         p=Path(name)
         if not p.is_file() or p.suffix in ['.png','.lock'] or name.endswith('package-lock.json'): continue
         text=p.read_text(errors='replace')
         if name in ['.env','frontend/.env'] or ('secret' in name and p.suffix in ['.yaml','.yml']):
          print('SECRET FILE',name,'tracked=',subprocess.run(['git','ls-files','--error-unmatch',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0)
          if name.endswith('.env'):
           for i,line in enumerate(text.splitlines(),1):
            if '=' in line and not line.startswith('#'):
             k,v=line.split('=',1)
             print(i,k, '<masked; '+('empty' if not v else 'placeholder' if v in ['changethis',''] else 'configured')+'>')
          else:
           for obj in yaml.safe_load_all(text):
            if not isinstance(obj,dict): continue
            print('kind=',obj.get('kind'),'name=',obj.get('metadata',{}).get('name'))
            for section in ['data','stringData']:
             for k,v in (obj.get(section) or {}).items():
              if section=='data':
               try: v=base64.b64decode(str(v)).decode()
               except Exception: v='binary'
              print(section,k,'<masked; '+('placeholder' if v=='changethis' else 'empty' if not v else 'configured')+'>')
         for i,line in enumerate(text.splitlines(),1):
          if re.search(r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}',line):print('POTENTIAL CREDENTIAL',name,i,'<masked>')
        print('TF inventory', [p for p in files if re.search(r'\.tf(?:vars|state)?(?:\.|$)',p)])
        PY
        nl -ba docker-compose.yml | head -140; cat frontend/nginx.conf frontend/nginx-backend-not-found.conf; nl -ba .github/workflows/generate-client.yml; cat .pre-commit-config.yaml; nl -ba deployment.md | head -48; nl -ba scripts/bootstrap-kind.sh | head -155; cat infra/jenkins-host/README.md
    SECRET FILE infra/kind/secrets/app-dev/backend-secrets.yaml tracked= False
    kind= SealedSecret name= backend-secrets
    SECRET FILE infra/kind/secrets/app-dev/db-secrets.yaml tracked= False
    kind= SealedSecret name= db-secrets
    SECRET FILE infra/kind/secrets/app-stage/backend-secrets.yaml tracked= False
    kind= SealedSecret name= backend-secrets
    SECRET FILE infra/kind/secrets/app-stage/db-secrets.yaml tracked= False
    kind= SealedSecret name= db-secrets
    SECRET FILE .env tracked= True
    4 DOMAIN <masked; configured>
    9 FRONTEND_HOST <masked; configured>
    14 ENVIRONMENT <masked; configured>
    16 PROJECT_NAME <masked; configured>
    17 STACK_NAME <masked; configured>
    20 BACKEND_CORS_ORIGINS <masked; configured>
    21 SECRET_KEY <masked; placeholder>
    22 FIRST_SUPERUSER <masked; configured>
    23 FIRST_SUPERUSER_PASSWORD <masked; placeholder>
    26 SMTP_HOST <masked; empty>
    27 SMTP_USER <masked; empty>
    28 SMTP_PASSWORD <masked; empty>
    29 EMAILS_FROM_EMAIL <masked; configured>
    30 SMTP_TLS <masked; configured>
    31 SMTP_SSL <masked; configured>
    32 SMTP_PORT <masked; configured>
    35 POSTGRES_SERVER <masked; configured>
    36 POSTGRES_PORT <masked; configured>
    37 POSTGRES_DB <masked; configured>
    38 POSTGRES_USER <masked; configured>
    39 POSTGRES_PASSWORD <masked; placeholder>
    41 SENTRY_DSN <masked; empty>
    44 DOCKER_IMAGE_BACKEND <masked; configured>
    45 DOCKER_IMAGE_FRONTEND <masked; configured>
    SECRET FILE frontend/.env tracked= True
    1 VITE_API_URL <masked; configured>
    2 MAILCATCHER_HOST <masked; configured>
    SECRET FILE k8s/base/secret-backend.yaml tracked= True
    kind= Secret name= backend-secrets
    stringData SECRET_KEY <masked; placeholder>
    stringData FIRST_SUPERUSER_PASSWORD <masked; placeholder>
    stringData SMTP_PASSWORD <masked; empty>
    stringData POSTGRES_PASSWORD <masked; placeholder>
    SECRET FILE k8s/base/secret-db.yaml tracked= True
    kind= Secret name= db-secrets
    stringData POSTGRES_PASSWORD <masked; placeholder>
    SECRET FILE k8s/base/secret-frontend.yaml tracked= True
    kind= Secret name= frontend-secrets
    SECRET FILE k8s/overlays/dev/sealed-secret-backend.yaml tracked= True
    kind= SealedSecret name= backend-secrets
    SECRET FILE k8s/overlays/dev/sealed-secret-db.yaml tracked= True
    kind= SealedSecret name= db-secrets
    SECRET FILE k8s/overlays/dev/sealed-secret-frontend.yaml tracked= True
    TF inventory []
         1    services:
         2
         3      db:
         4        image: postgres:12
         5        restart: always
         6        healthcheck:
         7          test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
         8          interval: 10s
         9          retries: 5
        10          start_period: 30s
        11          timeout: 10s
        12        volumes:
        13          - app-db-data:/var/lib/postgresql/data/pgdata
        14        env_file:
        15          - .env
        16        environment:
        17          - PGDATA=/var/lib/postgresql/data/pgdata
        18          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
        19          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
        20          - POSTGRES_DB=${POSTGRES_DB?Variable not set}
        21
        22      adminer:
        23        image: adminer
        24        restart: always
        25        networks:
        26          - traefik-public
        27          - default
        28        depends_on:
        29          - db
        30        environment:
        31          - ADMINER_DESIGN=pepa-linha-dark
        32        labels:
        33          - traefik.enable=true
        34          - traefik.docker.network=traefik-public
        35          - traefik.constraint-label=traefik-public
        36          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.rule=Host(`adminer.${DOMAIN?Variable not set}`)
        37          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.entrypoints=http
        38          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-http.middlewares=https-redirect
        39          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.rule=Host(`adminer.${DOMAIN?Variable not set}`)
        40          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.entrypoints=https
        41          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.tls=true
        42          - traefik.http.routers.${STACK_NAME?Variable not set}-adminer-https.tls.certresolver=le
        43          - traefik.http.services.${STACK_NAME?Variable not set}-adminer.loadbalancer.server.port=8080
        44
        45      prestart:
        46        image: '${DOCKER_IMAGE_BACKEND?Variable not set}:${TAG-latest}'
        47        build:
        48          context: ./backend
        49        networks:
        50          - traefik-public
        51          - default
        52        depends_on:
        53          db:
        54            condition: service_healthy
        55            restart: true
        56        command: bash scripts/prestart.sh
        57        env_file:
        58          - .env
        59        environment:
        60          - DOMAIN=${DOMAIN}
        61          - FRONTEND_HOST=${FRONTEND_HOST?Variable not set}
        62          - ENVIRONMENT=${ENVIRONMENT}
        63          - BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS}
        64          - SECRET_KEY=${SECRET_KEY?Variable not set}
        65          - FIRST_SUPERUSER=${FIRST_SUPERUSER?Variable not set}
        66          - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD?Variable not set}
        67          - SMTP_HOST=${SMTP_HOST}
        68          - SMTP_USER=${SMTP_USER}
        69          - SMTP_PASSWORD=${SMTP_PASSWORD}
        70          - EMAILS_FROM_EMAIL=${EMAILS_FROM_EMAIL}
        71          - POSTGRES_SERVER=db
        72          - POSTGRES_PORT=${POSTGRES_PORT}
        73          - POSTGRES_DB=${POSTGRES_DB}
        74          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
        75          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
        76          - SENTRY_DSN=${SENTRY_DSN}
        77
        78      backend:
        79        image: '${DOCKER_IMAGE_BACKEND?Variable not set}:${TAG-latest}'
        80        restart: always
        81        networks:
        82          - traefik-public
        83          - default
        84        depends_on:
        85          db:
        86            condition: service_healthy
        87            restart: true
        88          prestart:
        89            condition: service_completed_successfully
        90        env_file:
        91          - .env
        92        environment:
        93          - DOMAIN=${DOMAIN}
        94          - FRONTEND_HOST=${FRONTEND_HOST?Variable not set}
        95          - ENVIRONMENT=${ENVIRONMENT}
        96          - BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS}
        97          - SECRET_KEY=${SECRET_KEY?Variable not set}
        98          - FIRST_SUPERUSER=${FIRST_SUPERUSER?Variable not set}
        99          - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD?Variable not set}
       100          - SMTP_HOST=${SMTP_HOST}
       101          - SMTP_USER=${SMTP_USER}
       102          - SMTP_PASSWORD=${SMTP_PASSWORD}
       103          - EMAILS_FROM_EMAIL=${EMAILS_FROM_EMAIL}
       104          - POSTGRES_SERVER=db
       105          - POSTGRES_PORT=${POSTGRES_PORT}
       106          - POSTGRES_DB=${POSTGRES_DB}
       107          - POSTGRES_USER=${POSTGRES_USER?Variable not set}
       108          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD?Variable not set}
       109          - SENTRY_DSN=${SENTRY_DSN}
       110
       111        healthcheck:
       112          test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/utils/health-check/"]
       113          interval: 10s
       114          timeout: 5s
       115          retries: 5
       116
       117        build:
       118          context: ./backend
       119        labels:
       120          - traefik.enable=true
       121          - traefik.docker.network=traefik-public
       122          - traefik.constraint-label=traefik-public
       123
       124          - traefik.http.services.${STACK_NAME?Variable not set}-backend.loadbalancer.server.port=8000
       125
       126          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.rule=Host(`api.${DOMAIN?Variable not set}`)
       127          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.entrypoints=http
       128
       129          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.rule=Host(`api.${DOMAIN?Variable not set}`)
       130          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.entrypoints=https
       131          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.tls=true
       132          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-https.tls.certresolver=le
       133
       134          # Enable redirection for HTTP and HTTPS
       135          - traefik.http.routers.${STACK_NAME?Variable not set}-backend-http.middlewares=https-redirect
       136
       137      frontend:
       138        image: '${DOCKER_IMAGE_FRONTEND?Variable not set}:${TAG-latest}'
       139        restart: always
       140        networks:
    server {
      listen 80;

      location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri /index.html =404;
      }

      include /etc/nginx/extra-conf.d/*.conf;
    }
    location /api {
        return 404;
    }
    location /docs {
        return 404;
    }
    location /redoc {
        return 404;
    }
         1    name: Generate Client
         2
         3    on:
         4      pull_request:
         5        types:
         6        - opened
         7        - synchronize
         8
         9    jobs:
        10      generate-client:
        11        permissions:
        12          contents: write
        13        runs-on: ubuntu-latest
        14        steps:
        15        # For PRs from forks
        16        - uses: actions/checkout@v4
        17        # For PRs from the same repo
        18        - uses: actions/checkout@v4
        19          if: ( github.event_name != 'pull_request' || github.secret_source == 'Actions' )
        20          with:
        21            ref: ${{ github.head_ref }}
        22            token: ${{ secrets.FULL_STACK_FASTAPI_TEMPLATE_REPO_TOKEN }}
        23        - uses: actions/setup-node@v4
        24          with:
        25            node-version: lts/*
        26        - uses: actions/setup-python@v5
        27          with:
        28            python-version: "3.10"
        29        - name: Install uv
        30          uses: astral-sh/setup-uv@v5
        31          with:
        32            version: "0.4.15"
        33            enable-cache: true
        34        - name: Install dependencies
        35          run: npm ci
        36          working-directory: frontend
        37        - run: uv sync
        38          working-directory: backend
        39        - run: uv run bash scripts/generate-client.sh
        40          env:
        41            VIRTUAL_ENV: backend/.venv
        42            ENVIRONMENT: production
        43            SECRET_KEY: just-for-generating-client
        44            POSTGRES_PASSWORD: just-for-generating-client
        45            FIRST_SUPERUSER_PASSWORD: just-for-generating-client
        46        - name: Add changes to git
        47          run: |
        48            git config --local user.email "github-actions@github.com"
        49            git config --local user.name "github-actions"
        50            git add frontend/src/client
        51        # Same repo PRs
        52        - name: Push changes
        53          if: ( github.event_name != 'pull_request' || github.secret_source == 'Actions' )
        54          run: |
        55            git diff --staged --quiet || git commit -m "✨ Autogenerate frontend client"
        56            git push
        57        # Fork PRs
        58        - name: Check changes
        59          if: ( github.event_name == 'pull_request' && github.secret_source != 'Actions' )
        60          run: |
        61            git diff --staged --quiet || (echo "Changes detected in generated client, run scripts/generate-client.sh and commit the changes" && exit 1)
    # See https://pre-commit.com for more information
    # See https://pre-commit.com/hooks.html for more hooks
    repos:
      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.4.0
        hooks:
          - id: check-added-large-files
          - id: check-toml
          - id: check-yaml
            args:
              - --unsafe
          - id: end-of-file-fixer
            exclude: |
                (?x)^(
                    frontend/src/client/.*|
                    backend/app/email-templates/build/.*
                )$
          - id: trailing-whitespace
            exclude: ^frontend/src/client/.*
      - repo: https://github.com/charliermarsh/ruff-pre-commit
        rev: v0.2.2
        hooks:
          - id: ruff
            args:
              - --fix
          - id: ruff-format

    ci:
      autofix_commit_msg: 🎨 [pre-commit.ci] Auto format from pre-commit.com hooks
      autoupdate_commit_msg: ⬆ [pre-commit.ci] pre-commit autoupdate
         1    # Argo CD deployment
         2
         3    The production path is [GitHub Flow + Jenkins + GHCR + Argo CD](README-jenkins.md).
         4    Jenkins never applies application resources. Git `main`, `deploy/overlays/{dev,stage,prod}`,
         5    is desired state. `k8s/` is a retained legacy example, not an active deployment root.
         6    Do not apply both manifest trees to the same workload. Compose remains a separate
         7    local development tool, not this project's production CD system.
         8
         9    ## One-time operator bootstrap
        10
        11    Do not run these steps until the changes have been reviewed/merged, Jenkins trust
        12    boundaries configured, and real hostnames/secrets/storage prepared. These commands
        13    are instructions only; no real cluster was changed during implementation.
        14
        15    1. Install a supported, organization-approved Argo CD version, including its
        16       ApplicationSet controller, or connect to your existing installation. Download
        17       and review the exact release manifests (never an unpinned `stable` URL), e.g.:
        18
        19       ```bash
        20       export ARGOCD_VERSION='<approved-version>'
        21       curl -fL "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml" -o /tmp/argocd-install.yaml
        22       # Review the downloaded manifest before the next commands.
        23       kubectl create namespace argocd
        24       kubectl apply -n argocd -f /tmp/argocd-install.yaml
        25       ```
        26
        27       Skip installation if Argo already exists. Configure SSO/RBAC and restrict
        28       Application/AppProject writes and sync overrides to platform administrators.
        29       Ordinary users must not override main, image parameters or the production
        30       source path. Register a read-only repository credential in Argo for private Git.
        31    2. Create `app-dev`, `app-stage`, `app-prod` namespaces outside the ApplicationSet:
        32
        33       ```bash
        34       kubectl create namespace app-dev
        35       kubectl create namespace app-stage
        36       kubectl create namespace app-prod
        37       ```
        38
        39       Provision `backend-secrets`, `db-secrets`, `ghcr-pull-secret`, and `app-tls`
        40       securely in each namespace. See the exact key/permission table in
        41       README-jenkins.md. Use an external secret manager or newly sealed namespace-
        42       specific secrets; never commit generated plaintext YAML. Configure Traefik,
        43       DNS and valid TLS certificates for real hosts replacing `*.example.com` in
        44       overlays. The AppProject cannot create Namespaces, Secrets or cluster RBAC.
        45    3. Choose the cluster's storage class and capacity, backup/restore and database
        46       ownership. The base retains a 1Gi default-class RWO PVC and a single PostgreSQL
        47       Deployment using Recreate to avoid concurrent writers. PVC deletion/pruning
        48       is disabled in Argo annotations; do not assume this substitutes for backups.
         1    #!/usr/bin/env bash
         2    # Operator bootstrap only. Never invoked by Jenkins. No Minikube/PROD operations.
         3    set -euo pipefail
         4    set +x
         5    umask 077
         6    ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
         7    export PATH="$ROOT/.tools:$PATH"
         8    NAME=fastapi-dev
         9    CONTEXT=kind-fastapi-dev
        10    PHASE=${1:-base}
        11    KEY_BACKUP=${SEALED_SECRETS_KEY_BACKUP:-$ROOT/sealed-secrets-key-backup.yaml}
        12    KIND_VERSION=v0.33.0
        13    SEALED_VERSION=v0.39.1
        14    TRAEFIK_CHART=39.0.0
        15    ARGO_VERSION=v3.5.4
        16    METRICS_VERSION=v0.9.0
        17    for tool in kind kubectl helm python3 curl docker; do command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }; done
        18    python3 -c 'import yaml'
        19    k() { kubectl --context "$CONTEXT" --request-timeout=60s "$@"; }
        20    ns() { k create namespace "$1" --dry-run=client -o yaml | k apply -f -; }
        21    wait_app() {
        22      k wait -n argocd "application/$1" --for=jsonpath='{.status.sync.status}'=Synced --timeout=600s
        23      k wait -n argocd "application/$1" --for=jsonpath='{.status.health.status}'=Healthy --timeout=600s
        24    }
        25    case "$PHASE" in
        26    base)
        27      [[ "$(kind version)" == *"$KIND_VERSION"* ]] || { echo "Use kind $KIND_VERSION" >&2; exit 1; }
        28      [[ -s "$KEY_BACKUP" ]] || { echo 'Provide SEALED_SECRETS_KEY_BACKUP before bootstrap.' >&2; exit 1; }
        29      if ! kind get clusters | grep -qx "$NAME"; then
        30        kind create cluster --name "$NAME" --config "$ROOT/infra/kind/kind-config.yaml" --wait 180s
        31      fi
        32      k wait node --all --for=condition=Ready --timeout=180s
        33      k rollout status -n kube-system deployment/coredns --timeout=180s
        34      # Restore only key Secrets, stripping live metadata; private bytes stay in memory/stdin.
        35      python3 - "$KEY_BACKUP" "$CONTEXT" <<'PY'
        36    import sys,yaml,subprocess,os
        37    p,ctx=sys.argv[1:]; os.chmod(p,0o600)
        38    d=yaml.safe_load(open(p)); items=d.get('items',[d]); keys=[]
        39    for i in items:
        40        if i.get('kind')!='Secret' or not {'tls.key','tls.crt'} <= i.get('data',{}).keys():
        41            raise SystemExit('Backup contains an invalid key object')
        42        keys.append({'apiVersion':'v1','kind':'Secret','metadata':{'name':i['metadata']['name'],'namespace':'kube-system','labels':{'sealedsecrets.bitnami.com/sealed-secrets-key':'active'}},'type':'kubernetes.io/tls','data':i['data']})
        43    if not keys: raise SystemExit('Empty key backup')
        44    subprocess.run(['kubectl','--context',ctx,'apply','-f','-'],input=yaml.safe_dump({'apiVersion':'v1','kind':'List','items':keys}).encode(),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        45    print('Sealed Secrets key restored without printing private material')
        46    PY
        47      curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://github.com/bitnami/sealed-secrets/releases/download/$SEALED_VERSION/controller.yaml" -o "$ROOT/.tools/sealed-controller.yaml"
        48      k apply -f "$ROOT/.tools/sealed-controller.yaml"
        49      k rollout restart -n kube-system deployment/sealed-secrets-controller
        50      k rollout status -n kube-system deployment/sealed-secrets-controller --timeout=180s
        51      helm upgrade --install traefik traefik --repo https://traefik.github.io/charts --version "$TRAEFIK_CHART" --namespace traefik --create-namespace --kube-context "$CONTEXT" --values "$ROOT/infra/kind/traefik-values.yaml" --wait --timeout 5m
        52      ns argocd
        53      curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://raw.githubusercontent.com/argoproj/argo-cd/$ARGO_VERSION/manifests/install.yaml" -o "$ROOT/.tools/argocd-install.yaml"
        54      k apply --server-side -n argocd -f "$ROOT/.tools/argocd-install.yaml"
        55      k wait -n argocd pod --all --for=condition=Ready --timeout=600s
        56      curl -fsSL --connect-timeout 10 --max-time 120 --retry 3 "https://github.com/kubernetes-sigs/metrics-server/releases/download/$METRICS_VERSION/components.yaml" -o "$ROOT/.tools/metrics-server.yaml"
        57      # Local kind kubelet certificates are not signed by the metrics-server trust root.
        58      # Keep this declarative so reruns do not append duplicate arguments.
        59      python3 - "$ROOT/.tools/metrics-server.yaml" <<'PYMETRICS'
        60    import sys,yaml
        61    p=sys.argv[1]; docs=list(yaml.safe_load_all(open(p)))
        62    for doc in docs:
        63        if doc.get('kind')=='Deployment' and doc['metadata']['name']=='metrics-server':
        64            args=doc['spec']['template']['spec']['containers'][0]['args']
        65            if '--kubelet-insecure-tls' not in args: args.append('--kubelet-insecure-tls')
        66    with open(p,'w') as f: yaml.safe_dump_all(docs,f,sort_keys=False)
        67    PYMETRICS
        68      k apply -f "$ROOT/.tools/metrics-server.yaml"
        69      k rollout status deployment/metrics-server -n kube-system --timeout=180s
        70      k apply -f "$ROOT/infra/kind/project-fastapi.yaml"
        71      ns app-dev; ns app-stage
        72      for env in dev stage; do
        73        if k get -n argocd "application/app-$env" >/dev/null 2>&1; then continue; fi
        74        # Register desired Git source, but do not reconcile before credentials are provisioned.
        75        python3 - "$ROOT/argocd/app-$env.yaml" <<'PY' | k apply -f -
        76    import sys,yaml
        77    x=yaml.safe_load(open(sys.argv[1])); x['metadata'].setdefault('annotations',{})['argocd.argoproj.io/skip-reconcile']='true'; x['spec']['syncPolicy']['automated']['enabled']=False
        78    print(yaml.safe_dump(x))
        79    PY
        80      done
        81      ns monitoring
        82      k apply -f "$ROOT/argocd/project-monitoring.yaml"
        83      # Inline local values preserve unpublished monitoring configuration; Argo owns workloads.
        84      if ! k get -n argocd application/monitoring >/dev/null 2>&1; then
        85        python3 "$ROOT/monitoring/bootstrap.py" | k apply -f -
        86      fi
        87      k cluster-info; k get nodes -o wide
        88      echo 'Base installed. Provision namespace-specific credentials before dev/stage phases.'
        89      ;;
        90    dev|stage)
        91      ENVIRONMENT_NS="app-$PHASE"
        92      if [[ -d "$ROOT/infra/kind/secrets/$ENVIRONMENT_NS" ]]; then
        93        k apply -f "$ROOT/infra/kind/secrets/$ENVIRONMENT_NS"
        94        for secret in backend-secrets db-secrets; do
        95          k wait -n "$ENVIRONMENT_NS" "sealedsecret/$secret" --for=condition=Synced --timeout=120s
        96        done
        97      fi
        98      for secret in backend-secrets db-secrets ghcr-pull-secret; do
        99        k get secret -n "$ENVIRONMENT_NS" "$secret" >/dev/null || { echo "Missing $ENVIRONMENT_NS/$secret; supply or recover it securely." >&2; exit 1; }
       100      done
       101      # Ensure only this environment is enabled. Existing ApplicationSet is never applied.
       102      APP_MANIFEST="$ROOT/argocd/app-$PHASE.yaml"
       103      if [[ "$PHASE" == stage ]]; then APP_MANIFEST="$ROOT/infra/kind/app-stage-local.yaml"; fi
       104      k apply -f "$APP_MANIFEST"
       105      k annotate -n argocd "application/app-$PHASE" argocd.argoproj.io/skip-reconcile-
       106      k patch -n argocd "application/app-$PHASE" --type=merge -p '{"spec":{"syncPolicy":{"automated":{"enabled":true}}}}'
       107      wait_app "app-$PHASE"
       108      for deployment in postgres-deployment backend frontend adminer; do k rollout status -n "$ENVIRONMENT_NS" "deployment/$deployment" --timeout=180s; done
       109      ;;
       110    monitoring)
       111      for app in app-dev app-stage; do wait_app "$app"; done
       112      # Monitoring may run while Jenkins is explicitly kept offline. This does not prove CI peak safety.
       113      if [[ "${CI_CAPACITY_VERIFIED:-}" != yes ]]; then
       114        [[ "${CI_DISABLED:-}" == yes ]] || { echo 'Keep CI offline with CI_DISABLED=yes, or verify CI peak capacity with CI_CAPACITY_VERIFIED=yes.' >&2; exit 1; }
       115        python3 - <<'PYCI'
       116    import json,subprocess
       117    status=subprocess.run(['systemctl','is-active','jenkins'],capture_output=True,text=True)
       118    if status.stdout.strip() in ('active','activating'): raise SystemExit('Jenkins is active; CI peak must be measured')
       119    pods=json.loads(subprocess.check_output(['kubectl','--context','kind-fastapi-dev','get','pods','-A','-o','json']))['items']
       120    for p in pods:
       121        if p['status'].get('phase') not in ('Succeeded','Failed') and (p['metadata']['namespace'].startswith('jenkins') or any(c['name']=='jnlp' for c in p['spec']['containers'])):
       122            raise SystemExit('Jenkins workload/agent is active; keep monitoring paused until CI peak is reviewed')
       123    containers=subprocess.check_output(['docker','ps','--format','{{.Image}} {{.Names}}'],text=True)
       124    if 'jenkins' in containers.lower(): raise SystemExit('Docker Jenkins controller is active; measure CI peak first')
       125    print('Local Jenkins controller/agents absent; monitoring budget excludes CI. Keep Jenkins/builds offline.')
       126    PYCI
       127      fi
       128      python3 "$ROOT/scripts/check-kind-capacity.py"
       129      k annotate -n argocd application/monitoring argocd.argoproj.io/skip-reconcile-
       130      k patch -n argocd application/monitoring --type=merge -p '{"spec":{"syncPolicy":{"automated":{"enabled":true}}}}'
       131      python3 "$ROOT/scripts/watch-kind-monitoring.py"
       132      k get pods,pvc -n monitoring
       133      ;;
       134    *) echo 'Usage: bootstrap-kind.sh {base|dev|stage|monitoring}' >&2; exit 2 ;;
       135    esac
    # Local Jenkins outside kind

    This installation uses Docker CLI rather than an Ubuntu package: the JVM, agent and all nested Docker builds have hard cgroup limits and persistence independent of kind. Docker Compose is not installed on this host, so no extra host package is required. No host Docker socket, kubeconfig or application secrets are mounted. It does not install any Kubernetes resources.

    | Component | Hard RAM cap | CPU cap | Notes |
    | --- | --- | --- | --- |
    | Controller | 768 MiB | 0.5 | JVM heap 384 MiB; no executors |
    | Inbound agent | 256 MiB | 0.25 | JVM heap 128 MiB; exactly one executor |
    | Docker-in-Docker daemon and its descendants | 1536 MiB | 1.25 | TLS; no host-published Docker port; swap disabled |
    | Total additional allowance | 2560 MiB | 2 | Includes tool containers; not added to them |

    Sequential tool limits: Python 512 MiB + disposable PostgreSQL 128 MiB only during backend testing; Node 640 MiB (V8 heap 384 MiB); BuildKit 1024 MiB, one worker task at a time. Containerized tooling has no Kubernetes-style memory requests. Only a single host-ci executor exists, across all jobs. No publisher agent is provisioned. The existing Kubernetes Jenkinsfiles are preserved; the separately maintained host variant has no publication trigger.

    Run from the repository root:

    ```bash
    python3 scripts/bootstrap-jenkins-host.py
    python3 scripts/sync-jenkins-host-jobs.py
    python3 scripts/verify-jenkins-host.py --check-only
    python3 scripts/verify-jenkins-host.py
    # Full no-push validation only after reviewing the smoke measurements and margin:
    python3 scripts/verify-jenkins-host.py app-ci/main
    ```

    UI: http://127.0.0.1:8085/ . For a remote workstation:

    ```bash
    ssh -L 8085:127.0.0.1:8085 root-admin@YOUR_UBUNTU_HOST
    ```

    Fresh account: admin. Password is in ignored `.jenkins-host/secrets/jenkins-admin-password`, mode 0600; read it privately, never paste it into logs or Git. Agent authentication is read from a separate private file, never passed as a plaintext process argument. No GitHub/registry credentials are invented or imported from the host Docker login.

    `host-smoke` is manual and admin-only. `app-ci/main` is disabled by default; the verifier enables it only for a guarded validation and disables it afterwards. Both load the reviewed local pipeline source, because these uncommitted files are not on remote main. Checkout still uses the real public repository main. No branch scans, webhooks or automatic publication are enabled. Do not accept untrusted PR jobs on this shared worker: DinD is privileged, and a persistent worker is not a hostile-code security boundary. `trusted/publish` is a disabled recovery placeholder; restore `ghcr-write`, `gitops-app`, `ci-read` and an isolated trusted execution strategy before converting it to the protected original pipeline.

    The verifier requires at least 2.5 GiB available before a build and continuously checks memory, swap, kind API, application health and platform pod readiness. It stops only the host agent/build daemon if available RAM falls below 1 GiB, swap rises over 256 MiB within a minute, or the platform degrades; it also stops CI if host disk free space falls below 5 GiB. It never stops kind. Do not bypass it to run full CI from the UI. CPU/image-pull/build-cache pressure also needs observation; memory limits alone do not guarantee performance.

    Images are digest-pinned in `images.lock.json`; direct plugin pins originate from the recovered chart where possible, with compatible required pipeline plugins added. `plugins.lock.txt` records the complete resolved dependency set. The installer never deletes persistent volumes or replaces existing containers blindly. Configuration changes require a reviewed stop/recreate of controller/agent while retaining their volumes.

    Persistent volumes: `host-jenkins-home` (users, encryption keys, jobs, plugins, history/artifacts), `host-jenkins-plugins`, `host-jenkins-work`, `host-jenkins-docker` (disposable CI cache), and two TLS certificate volumes. Docker volumes have no filesystem quota: monitor host disk. Removing kind does not remove these named volumes.

    Back up consistently: disable/quiet jobs, wait for completion, stop `host-jenkins`, then archive the entire `host-jenkins-home` with ownership and encryption files using a read-only helper mount. Encrypt and copy off-host; restart the controller afterwards. Preserve `.jenkins-host/secrets` separately and the checked-in configuration/image/plugin locks. Never delete volumes to repair startup. Old Minikube Jenkins history and credentials are unrecovered, not restored by this setup.
    ✓ • 871ms

## Activity

    $ docker build --progress=plain -t fastapi-repo-audit/frontend:20261012 frontend
    #0 building with "default" instance using docker driver

    #1 [internal] load build definition from Dockerfile
    #1 transferring dockerfile:
    #1 transferring dockerfile: 591B 0.1s done
    #1 DONE 0.4s

    #2 [internal] load metadata for docker.io/library/node:20.18.1
    #2 DONE 1.4s

    #3 [internal] load metadata for docker.io/library/nginx:1.27.3
    #3 DONE 1.7s

    #4 [internal] load .dockerignore
    #4 transferring context: 58B 0.0s done
    #4 DONE 0.0s

    #5 [internal] load build context
    #5 transferring context: 5.58kB 0.1s done
    #5 DONE 0.1s

    #6 [stage-1 1/4] FROM docker.io/library/nginx:1.27.3@sha256:bc2f6a7c8ddbccf55bdb19659ce3b0a92ca6559e86d42677a5a02ef6bda2fcef
    #6 resolve docker.io/library/nginx:1.27.3@sha256:bc2f6a7c8ddbccf55bdb19659ce3b0a92ca6559e86d42677a5a02ef6bda2fcef 0.2s done
    #6 DONE 0.3s

    #7 [build-stage 1/6] FROM docker.io/library/node:20.18.1@sha256:968ca0550acc7589a8b1324401ec6e39ace53b2c82d2aed3a278e9ff491c2b1c
    #7 resolve docker.io/library/node:20.18.1@sha256:968ca0550acc7589a8b1324401ec6e39ace53b2c82d2aed3a278e9ff491c2b1c
    #7 resolve docker.io/library/node:20.18.1@sha256:968ca0550acc7589a8b1324401ec6e39ace53b2c82d2aed3a278e9ff491c2b1c 0.2s done
    #7 DONE 0.3s

    #8 [build-stage 5/6] COPY ./ /app/
    #8 CACHED

    #9 [build-stage 6/6] RUN npm run build
    #9 CACHED

    #10 [stage-1 2/4] COPY --from=build-stage /app/dist/ /usr/share/nginx/html
    #10 CACHED

    #11 [stage-1 3/4] COPY ./nginx.conf /etc/nginx/conf.d/default.conf
    #11 CACHED

    #12 [build-stage 2/6] WORKDIR /app
    #12 CACHED

    #13 [build-stage 3/6] COPY package*.json /app/
    #13 CACHED

    #14 [build-stage 4/6] RUN npm ci
    #14 CACHED

    #15 [stage-1 4/4] COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
    #15 CACHED

    #16 exporting to image
    #16 exporting layers 0.0s done
    #16 exporting manifest sha256:3cbb757a252a75077f68f25b947a191238c7509f5a61759327f00b74e33fad41 0.0s done
    #16 exporting config sha256:597883eded055bf99668da853996f57efbdfe7dbd3b419ab404b74839fc04c38
    #16 exporting config sha256:597883eded055bf99668da853996f57efbdfe7dbd3b419ab404b74839fc04c38 0.1s done
    #16 exporting attestation manifest sha256:d3f5891aea67087376c1eaabb755a6f878872bb78463ae45748b3645dd374726
    #16 exporting attestation manifest sha256:d3f5891aea67087376c1eaabb755a6f878872bb78463ae45748b3645dd374726 0.3s done
    #16 exporting manifest list sha256:fb394d76398a4aeb2dcb13f67013c36586d463c720a37e2797cc3fab4c33dc03
    #16 exporting manifest list sha256:fb394d76398a4aeb2dcb13f67013c36586d463c720a37e2797cc3fab4c33dc03 0.4s done
    #16 naming to docker.io/fastapi-repo-audit/frontend:20261012
    #16 naming to docker.io/fastapi-repo-audit/frontend:20261012 0.0s done
    #16 unpacking to docker.io/fastapi-repo-audit/frontend:20261012 0.1s done
    #16 DONE 1.4s
    ✓ • 8.50s

## Activity

    $ docker build --progress=plain -t fastapi-repo-audit/backend:20261012 backend
    #0 building with "default" instance using docker driver

    #1 [internal] load build definition from Dockerfile
    #1 transferring dockerfile:
    #1 transferring dockerfile: 1.32kB 0.1s done
    #1 DONE 0.4s

    #2 [internal] load metadata for ghcr.io/astral-sh/uv:0.5.11
    #2 DONE 1.4s

    #3 [internal] load metadata for docker.io/library/python:3.10.16-bookworm
    #3 DONE 1.6s

    #4 [internal] load .dockerignore
    #4 transferring context: 116B done
    #4 DONE 0.0s

    #5 [internal] load build context
    #5 DONE 0.0s

    #6 FROM ghcr.io/astral-sh/uv:0.5.11@sha256:0ac957607303916420297a4c9c213bb33fbd3c888f9cd7f4f7273596ebf42b85
    #6 resolve ghcr.io/astral-sh/uv:0.5.11@sha256:0ac957607303916420297a4c9c213bb33fbd3c888f9cd7f4f7273596ebf42b85
    #6 resolve ghcr.io/astral-sh/uv:0.5.11@sha256:0ac957607303916420297a4c9c213bb33fbd3c888f9cd7f4f7273596ebf42b85 0.2s done
    #6 DONE 0.2s

    #7 [stage-0 1/8] FROM docker.io/library/python:3.10.16-bookworm@sha256:b240c5813c2fa23506dc314bb370da0e890dadce666c7886780757976dc3b54b
    #7 resolve docker.io/library/python:3.10.16-bookworm@sha256:b240c5813c2fa23506dc314bb370da0e890dadce666c7886780757976dc3b54b 0.2s done
    #7 DONE 0.2s

    #5 [internal] load build context
    #5 transferring context: 114.09kB 0.4s done
    #5 DONE 0.5s

    #8 [stage-0 2/8] WORKDIR /app/
    #8 CACHED

    #9 [stage-0 3/8] COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
    #9 CACHED

    #10 [stage-0 4/8] RUN --mount=type=cache,target=/root/.cache/uv     --mount=type=bind,source=uv.lock,target=uv.lock     --mount=type=bind,source=pyproject.toml,target=pyproject.toml     uv sync --frozen --no-install-project
    #10 CACHED

    #11 [stage-0 5/8] COPY ./scripts /app/scripts
    #11 CACHED

    #12 [stage-0 6/8] COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
    #12 CACHED

    #13 [stage-0 7/8] COPY ./app /app/app
    #13 DONE 1.4s

    #14 [stage-0 8/8] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen
    #14 7.665 Installed 1 package in 97ms
    #14 12.83 Bytecode compiled 2809 files in 5.16s
    #14 12.83  + app==0.1.0 (from file:///app)
    #14 DONE 13.3s

    #15 exporting to image
    #15 exporting layers
    #15 exporting layers 0.8s done
    #15 exporting manifest sha256:61eefe161776e5e7e46328588a96b01753ddc18da4999de5330419cc0270efd3 0.1s done
    #15 exporting config sha256:0894ec117d95ec79ce587f3173c84d42791ec37b0daca2921f0d4120f119b3b8 0.1s done
    #15 exporting attestation manifest sha256:6c3562e13f504f237fc145e6bd19b2da005e67defda0b35eded8c8ddc4ca2680 0.1s done
    #15 exporting manifest list sha256:86b7e6f6f96bb98211f9cc858a1628f3bb3ebd53cd96083bcc240c79ba1ddc7e
    #15 exporting manifest list sha256:86b7e6f6f96bb98211f9cc858a1628f3bb3ebd53cd96083bcc240c79ba1ddc7e 0.0s done
    #15 naming to docker.io/fastapi-repo-audit/backend:20261012 done
    #15 unpacking to docker.io/fastapi-repo-audit/backend:20261012
    #15 unpacking to docker.io/fastapi-repo-audit/backend:20261012 0.6s done
    #15 DONE 1.9s
    ✓ • 25.09s

## Activity

    $ ps -eo pid,etime,args | rg 'repo-audit|unittest|kubeconform|docker build|kustomize' | head -20; ls -dt /tmp/repo-audit-* 2>/dev/null | head -3; git status --short
     950574       00:33 /bin/bash -c python3 - <<'PY' from pathlib import Path import subprocess,tempfile,os,yaml,json root=Path.cwd(); audit=Path(tempfile.mkdtemp(prefix='repo-audit-'));print('AUDIT_TMP',audit) os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['PATH']='/tmp/ci-bin:'+os.environ['PATH'] r=subprocess.run(['python3','-B','-m','unittest','discover','-s','ci','-p','test_*.py'],env=os.environ);print('CI_TEST_EXIT',r.returncode) for env in ['dev','stage','prod']:  r=subprocess.run(['/tmp/ci-bin/kustomize','build',f'deploy/overlays/{env}'],capture_output=True,text=True)  p=audit/f'{env}.yaml';p.write_text(r.stdout)  print('RENDER',env,r.returncode)  if r.returncode:print(r.stderr);continue  r=subprocess.run(['/tmp/ci-bin/kubeconform','-strict','-summary','-kubernetes-version','1.31.0',str(p)]);print('SCHEMA',env,r.returncode)  r=subprocess.run(['kubectl','--context','kind-fastapi-dev','--request-timeout=10s','apply','--dry-run=client','-f',str(p)],capture_output=True,text=True); print('CLIENT_DRY_RUN',env,r.returncode,r.stdout,r.stderr) for env in ['dev','prod']:  r=subprocess.run(['/tmp/ci-bin/kustomize','build',f'k8s/overlays/{env}'],capture_output=True,text=True);print('LEGACY_RENDER',env,r.returncode,r.stderr[:1800]) files=subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines();count=0 for f in dict.fromkeys(files):  p=Path(f)  if p.suffix not in ['.yaml','.yml'] or not p.is_file():continue  try:list(yaml.safe_load_all(p.read_text()));count+=1  except Exception as e:print('YAML_ERROR',f,str(e)[:500]) print('YAML_PARSED',count) for f in [*Path('scripts').glob('*.sh'),*Path('ci').glob('*.sh'),*Path('backend/scripts').glob('*.sh'),Path('infra/jenkins-host/run-tool.sh')]:  shell='bash' if 'bash' in f.read_text().splitlines()[0] else 'sh'  r=subprocess.run([shell,'-n',str(f)],capture_output=True,text=True)  print('SHELL',f,r.returncode,r.stderr.strip()) for f in Path('monitoring/dashboards').glob('*.yaml'):  obj=yaml.safe_load(f.read_text())  for k,v in obj.get('data',{}).items():   d=json.loads(v);print('DASHBOARD_JSON',k,'panels',len(d['panels'])) PY
     950576       00:32 python3 -B -m unittest discover -s ci -p test_*.py
     951389       00:00 kustomize build deploy/overlays/dev
     951394       00:00 /bin/bash -c ps -eo pid,etime,args | rg 'repo-audit|unittest|kubeconform|docker build|kustomize' | head -20; ls -dt /tmp/repo-audit-* 2>/dev/null | head -3; git status --short
     951397       00:00 rg repo-audit|unittest|kubeconform|docker build|kustomize
    /tmp/repo-audit-36bzshc0
     M .gitignore
     M DEV_SETUP_REPORT.md
    ?? ALERTING_RUNBOOK.md
    ?? GRAFANA_DASHBOARDS.md
    ?? JENKINS_RECOVERY_REPORT.md
    ?? KIND_MIGRATION_REPORT.md
    ?? MIGRATION_BACKUP_CHECKLIST.md
    ?? MONITORING_SETUP_REPORT.md
    ?? PROMETHEUS_QUERIES.md
    ?? argocd/app-monitoring.yaml
    ?? argocd/app-stage.yaml
    ?? argocd/bootstrap/monitoring-namespace.yaml
    ?? argocd/project-monitoring.yaml
    ?? infra/
    ?? monitoring/
    ?? scripts/bootstrap-jenkins-host.py
    ?? scripts/bootstrap-kind.sh
    ?? scripts/capture-kind-capacity.py
    ?? scripts/check-kind-capacity.py
    ?? scripts/create-stage-secrets.py
    ?? scripts/recover-dev-secrets.py
    ?? scripts/restore-kind-registry-auth.py
    ?? scripts/sync-jenkins-host-jobs.py
    ?? scripts/verify-jenkins-host.py
    ?? scripts/verify-kind-app.py
    ?? scripts/verify-kind-monitoring.py
    ?? scripts/watch-kind-monitoring.py
    ✓ • 232ms

## Activity

    $ python3 - <<'PY'
        from pathlib import Path
        import subprocess,tempfile,os,yaml,json
        root=Path.cwd(); audit=Path(tempfile.mkdtemp(prefix='repo-audit-'));print('AUDIT_TMP',audit)
        os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['PATH']='/tmp/ci-bin:'+os.environ['PATH']
        r=subprocess.run(['python3','-B','-m','unittest','discover','-s','ci','-p','test_*.py'],env=os.environ);print('CI_TEST_EXIT',r.returncode)
        for env in ['dev','stage','prod']:
         r=subprocess.run(['/tmp/ci-bin/kustomize','build',f'deploy/overlays/{env}'],capture_output=True,text=True)
         p=audit/f'{env}.yaml';p.write_text(r.stdout)
         print('RENDER',env,r.returncode)
         if r.returncode:print(r.stderr);continue
         r=subprocess.run(['/tmp/ci-bin/kubeconform','-strict','-summary','-kubernetes-version','1.31.0',str(p)]);print('SCHEMA',env,r.returncode)
         r=subprocess.run(['kubectl','--context','kind-fastapi-dev','--request-timeout=10s','apply','--dry-run=client','-f',str(p)],capture_output=True,text=True); print('CLIENT_DRY_RUN',env,r.returncode,r.stdout,r.stderr)
        for env in ['dev','prod']:
         r=subprocess.run(['/tmp/ci-bin/kustomize','build',f'k8s/overlays/{env}'],capture_output=True,text=True);print('LEGACY_RENDER',env,r.returncode,r.stderr[:1800])
        files=subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines();count=0
        for f in dict.fromkeys(files):
         p=Path(f)
         if p.suffix not in ['.yaml','.yml'] or not p.is_file():continue
         try:list(yaml.safe_load_all(p.read_text()));count+=1
         except Exception as e:print('YAML_ERROR',f,str(e)[:500])
        print('YAML_PARSED',count)
        for f in [*Path('scripts').glob('*.sh'),*Path('ci').glob('*.sh'),*Path('backend/scripts').glob('*.sh'),Path('infra/jenkins-host/run-tool.sh')]:
         shell='bash' if 'bash' in f.read_text().splitlines()[0] else 'sh'
         r=subprocess.run([shell,'-n',str(f)],capture_output=True,text=True)
         print('SHELL',f,r.returncode,r.stderr.strip())
        for f in Path('monitoring/dashboards').glob('*.yaml'):
         obj=yaml.safe_load(f.read_text())
         for k,v in obj.get('data',{}).items():
          d=json.loads(v);print('DASHBOARD_JSON',k,'panels',len(d['panels']))
        PY
    Cloning into '/tmp/tmpgom2j85t/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpgom2j85t/remote.git
       5ef9b74..f470ef3  HEAD -> main
    .Cloning into '/tmp/tmp0zlcttbc/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmpcr0iuy_3/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpcr0iuy_3/remote.git
       ab7742e..73b3a2d  HEAD -> main
    To /tmp/tmpcr0iuy_3/remote.git
     * [new branch]      HEAD -> release/v1.2.0
    .Cloning into '/tmp/tmpx6zp9w05/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpx6zp9w05/remote.git
       033ba34..e2ecd46  HEAD -> main
    .Cloning into '/tmp/tmpamn3_icb/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmp8mhb_9wm/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmp_7ct589k/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmp_7ct589k/remote.git
       b316085..1caa3f4  HEAD -> main
    .Cloning into '/tmp/tmpu48xzvwb/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmpn1m24_9x/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpn1m24_9x/remote.git
     ! [rejected]        HEAD -> main (fetch first)
    error: failed to push some refs to '/tmp/tmpn1m24_9x/remote.git'
    hint: Updates were rejected because the remote contains work that you do not
    hint: have locally. This is usually caused by another repository pushing to
    hint: the same ref. If you want to integrate the remote changes, use
    hint: 'git pull' before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.
    To /tmp/tmpn1m24_9x/remote.git
       892ccb7..36f2adc  HEAD -> main
    ....
    ----------------------------------------------------------------------
    Ran 12 tests in 93.883s

    OK
    Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0
    Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0
    Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0
    AUDIT_TMP /tmp/repo-audit-36bzshc0
    CI_TEST_EXIT 0
    RENDER dev 0
    SCHEMA dev 0
    CLIENT_DRY_RUN dev 0 configmap/backend-config configured (dry run)
    configmap/db-config configured (dry run)
    service/adminer configured (dry run)
    service/backend configured (dry run)
    service/db configured (dry run)
    service/frontend configured (dry run)
    persistentvolumeclaim/postgres-vol configured (dry run)
    deployment.apps/adminer configured (dry run)
    deployment.apps/backend configured (dry run)
    deployment.apps/frontend configured (dry run)
    deployment.apps/postgres-deployment configured (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress configured (dry run)

    RENDER stage 0
    SCHEMA stage 0
    CLIENT_DRY_RUN stage 0 configmap/backend-config configured (dry run)
    configmap/db-config configured (dry run)
    service/adminer configured (dry run)
    service/backend configured (dry run)
    service/db configured (dry run)
    service/frontend configured (dry run)
    persistentvolumeclaim/postgres-vol configured (dry run)
    deployment.apps/adminer configured (dry run)
    deployment.apps/backend configured (dry run)
    deployment.apps/frontend configured (dry run)
    deployment.apps/postgres-deployment configured (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress configured (dry run)

    RENDER prod 0
    SCHEMA prod 0
    CLIENT_DRY_RUN prod 0 configmap/backend-config created (dry run)
    configmap/db-config created (dry run)
    service/adminer created (dry run)
    service/backend created (dry run)
    service/db created (dry run)
    service/frontend created (dry run)
    persistentvolumeclaim/postgres-vol created (dry run)
    deployment.apps/adminer created (dry run)
    deployment.apps/backend created (dry run)
    deployment.apps/frontend created (dry run)
    deployment.apps/postgres-deployment created (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress created (dry run)

    LEGACY_RENDER dev 0
    LEGACY_RENDER prod 0
    YAML_PARSED 87
    SHELL scripts/build.sh 0
    SHELL scripts/test-local.sh 0
    SHELL scripts/bootstrap-kind.sh 0
    SHELL scripts/test.sh 0
    SHELL scripts/build-push.sh 0
    SHELL scripts/deploy.sh 0
    SHELL scripts/generate-client.sh 0
    SHELL ci/tools.sh 0
    SHELL ci/validate.sh 0
    SHELL ci/publish.sh 0
    SHELL backend/scripts/format.sh 0
    SHELL backend/scripts/tests-start.sh 0
    SHELL backend/scripts/test.sh 0
    SHELL backend/scripts/prestart.sh 0
    SHELL backend/scripts/lint.sh 0
    SHELL infra/jenkins-host/run-tool.sh 0
    DASHBOARD_JSON platform-nodes.json panels 8
    DASHBOARD_JSON dev-stage-workloads.json panels 8
    DASHBOARD_JSON gitops-argocd.json panels 6
    DASHBOARD_JSON ingress-traefik.json panels 7
    ✓ • 1m 59s

## Activity

    $ python3 -u - <<'PY'
        import subprocess,time,secrets,os
        image='fastapi-repo-audit/backend:20261012'; name='repo-audit-pg-'+secrets.token_hex(4)
        subprocess.run(['docker','run','--rm','-d','--name',name,'--network','none','--memory=256m','-e','POSTGRES_PASSWORD=audit-test-only','-e','POSTGRES_DB=app_audit','postgres:16'],check=True,stdout=subprocess.DEVNULL)
        try:
         for _ in range(40):
          if subprocess.run(['docker','exec',name,'pg_isready','-U','postgres','-d','app_audit'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
          time.sleep(1)
         else:raise RuntimeError('audit database not ready')
         env={'ENVIRONMENT':'local','PROJECT_NAME':'Repository Audit','POSTGRES_SERVER':'127.0.0.1','POSTGRES_DB':'app_audit','POSTGRES_USER':'postgres','POSTGRES_PASSWORD':'audit-test-only','FIRST_SUPERUSER':'audit@example.com','FIRST_SUPERUSER_PASSWORD':secrets.token_urlsafe(20),'SECRET_KEY':secrets.token_urlsafe(32),'EMAILS_FROM_EMAIL':'audit@example.com','EMAILS_FROM_NAME':'audit@example.com','SMTP_HOST':'127.0.0.1','SMTP_PORT':'1025','SMTP_TLS':'false','SMTP_SSL':'false'}
         cmd=['docker','run','--rm','--network','container:'+name,'--memory=768m']
         for k,v in env.items():cmd+=['-e',k+'='+v]
         cmd += [image,'bash','-c','bash scripts/lint.sh && bash scripts/prestart.sh && pytest -p no:cacheprovider']
         result=subprocess.run(cmd);print('BACKEND_LINT_MIGRATION_TEST_EXIT',result.returncode)
        finally:subprocess.run(['docker','stop','-t','5',name],stdout=subprocess.DEVNULL,check=True)
        PY
    + mypy app
    Success: no issues found in 38 source files
    + ruff check app
    All checks passed!
    + ruff format app --check
    38 files already formatted
    + python app/backend_pre_start.py
    INFO:__main__:Initializing service
    INFO:__main__:Starting call to '__main__.init', this is the 1st time calling it.
    INFO:__main__:Service finished initializing
    + alembic upgrade head
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> e2412789c190, Initialize models
    INFO  [alembic.runtime.migration] Running upgrade e2412789c190 -> 9c0a54914c78, Add max length for string(varchar) fields in User and Items models
    INFO  [alembic.runtime.migration] Running upgrade 9c0a54914c78 -> d98dd8ec85a3, Edit replace id integers in all models to use UUID instead
    INFO  [alembic.runtime.migration] Running upgrade d98dd8ec85a3 -> 1a31ce608336, Add cascade delete relationships
    + python app/initial_data.py
    INFO:__main__:Creating initial data
    INFO:__main__:Initial data created
    ============================= test session starts ==============================
    platform linux -- Python 3.10.16, pytest-7.4.4, pluggy-1.5.0
    rootdir: /app
    plugins: anyio-4.6.0
    collected 55 items

    app/tests/api/routes/test_items.py ...........                           [ 20%]
    app/tests/api/routes/test_login.py .......                               [ 32%]
    app/tests/api/routes/test_private.py .                                   [ 34%]
    app/tests/api/routes/test_users.py .........................             [ 80%]
    app/tests/crud/test_user.py .........                                    [ 96%]
    app/tests/scripts/test_backend_pre_start.py .                            [ 98%]
    app/tests/scripts/test_test_pre_start.py .                               [100%]

    =============================== warnings summary ===============================
    app/tests/scripts/test_backend_pre_start.py::test_init_successful_connection
    app/tests/scripts/test_test_pre_start.py::test_init_successful_connection
      /app/.venv/lib/python3.10/site-packages/sqlmodel/orm/session.py:66: SAWarning: The engine provided as bind produced a connection that is already in a transaction. This is usually caused by a core event, such as 'engine_connect', that has left a transaction open. The effective join transaction mode used by this session is 'create_savepoint'. To silence this warning, do not leave transactions open
        results = super().execute(

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    ======================= 55 passed, 2 warnings in 38.38s ========================
    BACKEND_LINT_MIGRATION_TEST_EXIT 0
    ✓ • 3m 38s

## Assistant

Beide Dockerfiles lassen sich lokal bauen. Dev, Stage und der Monitoring-Stack laufen im vorhandenen kind-Cluster und melden sich bei Argo CD als Healthy/Synced. Das belegt die lokale Laufzeitfunktion, aber noch keine vollständige Pipeline: Ich prüfe gerade Tests, Jenkins-Aktivierung und den Unterschied zwischen lokalem Bootstrap und Git-gesteuerter Bereitstellung.

## Activity

    $ python3 -u - <<'PY'
        import subprocess,json,pathlib
        base=['kubectl','--context','kind-fastapi-dev','--request-timeout=10s']
        for resource in ['nodes','namespaces','storageclasses','networkpolicies','poddisruptionbudgets','cronjobs','ingress','sealedsecrets']:
         r=subprocess.run(base+['get',resource,'-A'],capture_output=True,text=True);print(resource,r.stdout,r.stderr[:500])
        a=json.loads(subprocess.check_output(base+['get','applications','-n','argocd','-o','json']))
        for item in a['items']:
         s=item['spec']; print('ARGO',item['metadata']['name'],'path',s.get('source',{}).get('path'),'inlineHelm',bool(s.get('source',{}).get('helm',{}).get('valuesObject')),'patches',s.get('source',{}).get('kustomize',{}).get('patches'),'auto',s.get('syncPolicy',{}).get('automated'))
        for ns in ['app-dev','app-stage','monitoring']:
         r=subprocess.run(base+['get','secrets','-n',ns,'-o','custom-columns=NAME:.metadata.name,TYPE:.type'],capture_output=True,text=True);print('SECRET_METADATA',ns,r.stdout)
        for host in ['dev.example.com','stage.example.com']:
         for path in ['/','/api/v1/utils/health-check/','/api/v1/openapi.json','/docs','/metrics']:
          r=subprocess.run(['curl','-sS','--max-time','10','-o','/dev/null','-w','%{http_code}','-H','Host: '+host,'http://127.0.0.1'+path],capture_output=True,text=True);print('HTTP',host,path,r.returncode,r.stdout)
        for c in ['host-jenkins']:
         for job in ['app-ci/jobs/main','trusted/jobs/publish']:
          r=subprocess.run(['docker','exec',c,'cat','/var/jenkins_home/jobs/'+job+'/config.xml'],capture_output=True,text=True)
          print('LIVE_JOB',job,'readExit',r.returncode,'disabledTrue','<disabled>true</disabled>' in r.stdout,'disabledFalse','<disabled>false</disabled>' in r.stdout)
        PY
    nodes NAME                        STATUS   ROLES           AGE     VERSION
    fastapi-dev-control-plane   Ready    control-plane   2d18h   v1.35.8

    namespaces NAME                 STATUS   AGE
    app-dev              Active   2d18h
    app-stage            Active   2d18h
    argocd               Active   2d18h
    default              Active   2d18h
    kube-node-lease      Active   2d18h
    kube-public          Active   2d18h
    kube-system          Active   2d18h
    local-path-storage   Active   2d18h
    monitoring           Active   2d18h
    traefik              Active   2d18h

    storageclasses NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
    standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  2d18h

    networkpolicies NAMESPACE   NAME                                              POD-SELECTOR                                              AGE
    argocd      argocd-application-controller-network-policy      app.kubernetes.io/name=argocd-application-controller      2d18h
    argocd      argocd-applicationset-controller-network-policy   app.kubernetes.io/name=argocd-applicationset-controller   2d18h
    argocd      argocd-dex-server-network-policy                  app.kubernetes.io/name=argocd-dex-server                  2d18h
    argocd      argocd-notifications-controller-network-policy    app.kubernetes.io/name=argocd-notifications-controller    2d18h
    argocd      argocd-redis-network-policy                       app.kubernetes.io/name=argocd-redis                       2d18h
    argocd      argocd-repo-server-network-policy                 app.kubernetes.io/name=argocd-repo-server                 2d18h
    argocd      argocd-server-network-policy                      app.kubernetes.io/name=argocd-server                      2d18h

    poddisruptionbudgets  No resources found

    cronjobs  No resources found

    ingress NAMESPACE   NAME          CLASS     HOSTS               ADDRESS     PORTS   AGE
    app-dev     app-ingress   traefik   dev.example.com     127.0.0.1   80      2d18h
    app-stage   app-ingress   traefik   stage.example.com   127.0.0.1   80      2d17h

    sealedsecrets NAMESPACE   NAME              AGE
    app-dev     backend-secrets   2d18h
    app-dev     db-secrets        2d18h
    app-stage   backend-secrets   2d17h
    app-stage   db-secrets        2d17h

    ARGO app-dev path deploy/overlays/dev inlineHelm False patches None auto {'enabled': True, 'prune': True, 'selfHeal': True}
    ARGO app-stage path deploy/overlays/stage inlineHelm False patches [{'patch': '- op: remove\n  path: /spec/tls\n', 'target': {'kind': 'Ingress', 'name': 'app-ingress'}}, {'patch': 'apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: backend-config\ndata:\n  FRONTEND_HOST: http://stage.example.com\n  BACKEND_CORS_ORIGINS: http://stage.example.com\n', 'target': {'kind': 'ConfigMap', 'name': 'backend-config'}}] auto {'enabled': True, 'prune': True, 'selfHeal': True}
    ARGO monitoring path None inlineHelm True patches None auto {'allowEmpty': False, 'enabled': True, 'prune': False, 'selfHeal': True}
    SECRET_METADATA app-dev NAME               TYPE
    backend-secrets    Opaque
    db-secrets         Opaque
    ghcr-pull-secret   kubernetes.io/dockerconfigjson

    SECRET_METADATA app-stage NAME               TYPE
    backend-secrets    Opaque
    db-secrets         Opaque
    ghcr-pull-secret   kubernetes.io/dockerconfigjson

    SECRET_METADATA monitoring NAME                                                                  TYPE
    alertmanager-monitoring-alertmanager                                  Opaque
    alertmanager-monitoring-alertmanager-cluster-tls-config               Opaque
    alertmanager-monitoring-alertmanager-generated                        Opaque
    alertmanager-monitoring-alertmanager-tls-assets-0                     Opaque
    alertmanager-monitoring-alertmanager-web-config                       Opaque
    monitoring-grafana-admin                                              Opaque
    monitoring-prometheus-token                                           kubernetes.io/service-account-token
    prometheus-monitoring-prometheus                                      Opaque
    prometheus-monitoring-prometheus-thanos-prometheus-http-client-file   Opaque
    prometheus-monitoring-prometheus-tls-assets-0                         Opaque
    prometheus-monitoring-prometheus-web-config                           Opaque

    HTTP dev.example.com / 0 200
    HTTP dev.example.com /api/v1/utils/health-check/ 0 200
    HTTP dev.example.com /api/v1/openapi.json 0 200
    HTTP dev.example.com /docs 0 200
    HTTP dev.example.com /metrics 0 200
    HTTP stage.example.com / 0 200
    HTTP stage.example.com /api/v1/utils/health-check/ 0 200
    HTTP stage.example.com /api/v1/openapi.json 0 200
    HTTP stage.example.com /docs 0 404
    HTTP stage.example.com /metrics 0 200
    LIVE_JOB app-ci/jobs/main readExit 0 disabledTrue True disabledFalse False
    LIVE_JOB trusted/jobs/publish readExit 0 disabledTrue True disabledFalse False
    ✓ • 11.48s

## Activity

    $ cat scripts/generate-client.sh frontend/tests/config.ts frontend/tests/utils/privateApi.ts frontend/openapi-ts.config.ts frontend/biome.json; free -m; cat scripts/check-kind-capacity.py; nl -ba backend/app/api/routes/users.py; nl -ba backend/app/api/routes/items.py; nl -ba backend/app/api/routes/login.py; cat backend/app/models.py backend/app/crud.py backend/app/utils.py
    #! /usr/bin/env bash

    set -e
    set -x

    cd backend
    python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
    cd ..
    mv openapi.json frontend/
    cd frontend
    npm run generate-client
    npx biome format --write ./src/client
    import path from "node:path"
    import { fileURLToPath } from "node:url"
    import dotenv from "dotenv"

    const __filename = fileURLToPath(import.meta.url)
    const __dirname = path.dirname(__filename)

    dotenv.config({ path: path.join(__dirname, "../../.env") })

    const { FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD } = process.env

    if (typeof FIRST_SUPERUSER !== "string") {
      throw new Error("Environment variable FIRST_SUPERUSER is undefined")
    }

    if (typeof FIRST_SUPERUSER_PASSWORD !== "string") {
      throw new Error("Environment variable FIRST_SUPERUSER_PASSWORD is undefined")
    }

    export const firstSuperuser = FIRST_SUPERUSER as string
    export const firstSuperuserPassword = FIRST_SUPERUSER_PASSWORD as string
    // Note: the `PrivateService` is only available when generating the client
    // for local environments
    import { OpenAPI, PrivateService } from "../../src/client"

    OpenAPI.BASE = `${process.env.VITE_API_URL}`

    export const createUser = async ({
      email,
      password,
    }: {
      email: string
      password: string
    }) => {
      return await PrivateService.createUser({
        requestBody: {
          email,
          password,
          is_verified: true,
          full_name: "Test User",
        },
      })
    }
    import { defineConfig } from "@hey-api/openapi-ts"

    export default defineConfig({
      client: "legacy/axios",
      input: "./openapi.json",
      output: "./src/client",
      // exportSchemas: true,
      plugins: [
        {
          name: "@hey-api/sdk",
          // NOTE: this doesn't allow tree-shaking
          asClass: true,
          operationId: true,
          methodNameBuilder: (operation) => {
            // @ts-ignore
            let name: string = operation.name
            // @ts-ignore
            const service: string = operation.service

            if (service && name.toLowerCase().startsWith(service.toLowerCase())) {
              name = name.slice(service.length)
            }

            return name.charAt(0).toLowerCase() + name.slice(1)
          },
        },
      ],
    })
    {
      "$schema": "https://biomejs.dev/schemas/1.6.1/schema.json",
      "organizeImports": {
        "enabled": true
      },
      "files": {
        "ignore": [
          "node_modules",
          "src/routeTree.gen.ts",
          "playwright.config.ts",
          "playwright-report"
        ]
      },
      "linter": {
        "enabled": true,
        "rules": {
          "recommended": true,
          "suspicious": {
            "noExplicitAny": "off",
            "noArrayIndexKey": "off"
          },
          "style": {
            "noNonNullAssertion": "off"
          }
        }
      },
      "formatter": {
        "indentStyle": "space"
      },
      "javascript": {
        "formatter": {
          "quoteStyle": "double",
          "semicolons": "asNeeded"
        }
      }
    }
                   total        used        free      shared  buff/cache   available
    Mem:            7941        4637         691          44        2964        3303
    Swap:           3251         117        3134
    #!/usr/bin/env python3
    """Conservative local monitoring gate; idle measurements cannot prove CI peak safety."""
    import json, subprocess

    def run(*args):
        return subprocess.check_output(args, text=True)

    available = int(next(x.split()[1] for x in open('/proc/meminfo') if x.startswith('MemAvailable:'))) / 1024
    node = json.loads(run('kubectl', '--context', 'kind-fastapi-dev', 'get', 'nodes', '-o', 'json'))['items'][0]
    conditions = {c['type']: c['status'] for c in node['status']['conditions']}
    for condition in ['MemoryPressure', 'DiskPressure', 'PIDPressure']:
        if conditions.get(condition) != 'False':
            raise SystemExit(f'Capacity gate failed: {condition}')
    run('kubectl', '--context', 'kind-fastapi-dev', 'top', 'nodes')
    run('kubectl', '--context', 'kind-fastapi-dev', 'top', 'pods', '-A')
    # Monitoring requests ~1Gi; retain 2Gi host/CI margin, alongside reviewed CI peak.
    if available < 3072:
        raise SystemExit(f'Capacity gate failed: host MemAvailable {available:.0f}Mi < 3072Mi')
    container = 'fastapi-dev-control-plane'
    limit = int(run('docker', 'inspect', container, '--format', '{{.HostConfig.Memory}}'))
    current = int(run('docker', 'exec', container, 'cat', '/sys/fs/cgroup/memory.current'))
    maximum = run('docker', 'exec', container, 'cat', '/sys/fs/cgroup/memory.max').strip()
    limits = [x for x in [limit, int(maximum) if maximum != 'max' else 0] if x]
    if limits and min(limits) - current < 1536 * 1024**2:
        raise SystemExit('Capacity gate failed: kind cgroup has less than 1536Mi headroom')
    print(f'Idle capacity gate passed: host available {available:.0f}Mi; CI peak review still required.')
         1    import uuid
         2    from typing import Any
         3
         4    from fastapi import APIRouter, Depends, HTTPException
         5    from sqlmodel import col, delete, func, select
         6
         7    from app import crud
         8    from app.api.deps import (
         9        CurrentUser,
        10        SessionDep,
        11        get_current_active_superuser,
        12    )
        13    from app.core.config import settings
        14    from app.core.security import get_password_hash, verify_password
        15    from app.models import (
        16        Item,
        17        Message,
        18        UpdatePassword,
        19        User,
        20        UserCreate,
        21        UserPublic,
        22        UserRegister,
        23        UsersPublic,
        24        UserUpdate,
        25        UserUpdateMe,
        26    )
        27    from app.utils import generate_new_account_email, send_email
        28
        29    router = APIRouter(prefix="/users", tags=["users"])
        30
        31
        32    @router.get(
        33        "/",
        34        dependencies=[Depends(get_current_active_superuser)],
        35        response_model=UsersPublic,
        36    )
        37    def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
        38        """
        39        Retrieve users.
        40        """
        41
        42        count_statement = select(func.count()).select_from(User)
        43        count = session.exec(count_statement).one()
        44
        45        statement = select(User).offset(skip).limit(limit)
        46        users = session.exec(statement).all()
        47
        48        return UsersPublic(data=users, count=count)
        49
        50
        51    @router.post(
        52        "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
        53    )
        54    def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
        55        """
        56        Create new user.
        57        """
        58        user = crud.get_user_by_email(session=session, email=user_in.email)
        59        if user:
        60            raise HTTPException(
        61                status_code=400,
        62                detail="The user with this email already exists in the system.",
        63            )
        64
        65        user = crud.create_user(session=session, user_create=user_in)
        66        if settings.emails_enabled and user_in.email:
        67            email_data = generate_new_account_email(
        68                email_to=user_in.email, username=user_in.email, password=user_in.password
        69            )
        70            send_email(
        71                email_to=user_in.email,
        72                subject=email_data.subject,
        73                html_content=email_data.html_content,
        74            )
        75        return user
        76
        77
        78    @router.patch("/me", response_model=UserPublic)
        79    def update_user_me(
        80        *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
        81    ) -> Any:
        82        """
        83        Update own user.
        84        """
        85
        86        if user_in.email:
        87            existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        88            if existing_user and existing_user.id != current_user.id:
        89                raise HTTPException(
        90                    status_code=409, detail="User with this email already exists"
        91                )
        92        user_data = user_in.model_dump(exclude_unset=True)
        93        current_user.sqlmodel_update(user_data)
        94        session.add(current_user)
        95        session.commit()
        96        session.refresh(current_user)
        97        return current_user
        98
        99
       100    @router.patch("/me/password", response_model=Message)
       101    def update_password_me(
       102        *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
       103    ) -> Any:
       104        """
       105        Update own password.
       106        """
       107        if not verify_password(body.current_password, current_user.hashed_password):
       108            raise HTTPException(status_code=400, detail="Incorrect password")
       109        if body.current_password == body.new_password:
       110            raise HTTPException(
       111                status_code=400, detail="New password cannot be the same as the current one"
       112            )
       113        hashed_password = get_password_hash(body.new_password)
       114        current_user.hashed_password = hashed_password
       115        session.add(current_user)
       116        session.commit()
       117        return Message(message="Password updated successfully")
       118
       119
       120    @router.get("/me", response_model=UserPublic)
       121    def read_user_me(current_user: CurrentUser) -> Any:
       122        """
       123        Get current user.
       124        """
       125        return current_user
       126
       127
       128    @router.delete("/me", response_model=Message)
       129    def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
       130        """
       131        Delete own user.
       132        """
       133        if current_user.is_superuser:
       134            raise HTTPException(
       135                status_code=403, detail="Super users are not allowed to delete themselves"
       136            )
       137        session.delete(current_user)
       138        session.commit()
       139        return Message(message="User deleted successfully")
       140
       141
       142    @router.post("/signup", response_model=UserPublic)
       143    def register_user(session: SessionDep, user_in: UserRegister) -> Any:
       144        """
       145        Create new user without the need to be logged in.
       146        """
       147        user = crud.get_user_by_email(session=session, email=user_in.email)
       148        if user:
       149            raise HTTPException(
       150                status_code=400,
       151                detail="The user with this email already exists in the system",
       152            )
       153        user_create = UserCreate.model_validate(user_in)
       154        user = crud.create_user(session=session, user_create=user_create)
       155        return user
       156
       157
       158    @router.get("/{user_id}", response_model=UserPublic)
       159    def read_user_by_id(
       160        user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
       161    ) -> Any:
       162        """
       163        Get a specific user by id.
       164        """
       165        user = session.get(User, user_id)
       166        if user == current_user:
       167            return user
       168        if not current_user.is_superuser:
       169            raise HTTPException(
       170                status_code=403,
       171                detail="The user doesn't have enough privileges",
       172            )
       173        return user
       174
       175
       176    @router.patch(
       177        "/{user_id}",
       178        dependencies=[Depends(get_current_active_superuser)],
       179        response_model=UserPublic,
       180    )
       181    def update_user(
       182        *,
       183        session: SessionDep,
       184        user_id: uuid.UUID,
       185        user_in: UserUpdate,
       186    ) -> Any:
       187        """
       188        Update a user.
       189        """
       190
       191        db_user = session.get(User, user_id)
       192        if not db_user:
       193            raise HTTPException(
       194                status_code=404,
       195                detail="The user with this id does not exist in the system",
       196            )
       197        if user_in.email:
       198            existing_user = crud.get_user_by_email(session=session, email=user_in.email)
       199            if existing_user and existing_user.id != user_id:
       200                raise HTTPException(
       201                    status_code=409, detail="User with this email already exists"
       202                )
       203
       204        db_user = crud.update_user(session=session, db_user=db_user, user_in=user_in)
       205        return db_user
       206
       207
       208    @router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
       209    def delete_user(
       210        session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
       211    ) -> Message:
       212        """
       213        Delete a user.
       214        """
       215        user = session.get(User, user_id)
       216        if not user:
       217            raise HTTPException(status_code=404, detail="User not found")
       218        if user == current_user:
       219            raise HTTPException(
       220                status_code=403, detail="Super users are not allowed to delete themselves"
       221            )
       222        statement = delete(Item).where(col(Item.owner_id) == user_id)
       223        session.exec(statement)  # type: ignore
       224        session.delete(user)
       225        session.commit()
       226        return Message(message="User deleted successfully")
         1    import uuid
         2    from typing import Any
         3
         4    from fastapi import APIRouter, HTTPException
         5    from sqlmodel import func, select
         6
         7    from app.api.deps import CurrentUser, SessionDep
         8    from app.models import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate, Message
         9
        10    router = APIRouter(prefix="/items", tags=["items"])
        11
        12
        13    @router.get("/", response_model=ItemsPublic)
        14    def read_items(
        15        session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
        16    ) -> Any:
        17        """
        18        Retrieve items.
        19        """
        20
        21        if current_user.is_superuser:
        22            count_statement = select(func.count()).select_from(Item)
        23            count = session.exec(count_statement).one()
        24            statement = select(Item).offset(skip).limit(limit)
        25            items = session.exec(statement).all()
        26        else:
        27            count_statement = (
        28                select(func.count())
        29                .select_from(Item)
        30                .where(Item.owner_id == current_user.id)
        31            )
        32            count = session.exec(count_statement).one()
        33            statement = (
        34                select(Item)
        35                .where(Item.owner_id == current_user.id)
        36                .offset(skip)
        37                .limit(limit)
        38            )
        39            items = session.exec(statement).all()
        40
        41        return ItemsPublic(data=items, count=count)
        42
        43
        44    @router.get("/{id}", response_model=ItemPublic)
        45    def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
        46        """
        47        Get item by ID.
        48        """
        49        item = session.get(Item, id)
        50        if not item:
        51            raise HTTPException(status_code=404, detail="Item not found")
        52        if not current_user.is_superuser and (item.owner_id != current_user.id):
        53            raise HTTPException(status_code=400, detail="Not enough permissions")
        54        return item
        55
        56
        57    @router.post("/", response_model=ItemPublic)
        58    def create_item(
        59        *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
        60    ) -> Any:
        61        """
        62        Create new item.
        63        """
        64        item = Item.model_validate(item_in, update={"owner_id": current_user.id})
        65        session.add(item)
        66        session.commit()
        67        session.refresh(item)
        68        return item
        69
        70
        71    @router.put("/{id}", response_model=ItemPublic)
        72    def update_item(
        73        *,
        74        session: SessionDep,
        75        current_user: CurrentUser,
        76        id: uuid.UUID,
        77        item_in: ItemUpdate,
        78    ) -> Any:
        79        """
        80        Update an item.
        81        """
        82        item = session.get(Item, id)
        83        if not item:
        84            raise HTTPException(status_code=404, detail="Item not found")
        85        if not current_user.is_superuser and (item.owner_id != current_user.id):
        86            raise HTTPException(status_code=400, detail="Not enough permissions")
        87        update_dict = item_in.model_dump(exclude_unset=True)
        88        item.sqlmodel_update(update_dict)
        89        session.add(item)
        90        session.commit()
        91        session.refresh(item)
        92        return item
        93
        94
        95    @router.delete("/{id}")
        96    def delete_item(
        97        session: SessionDep, current_user: CurrentUser, id: uuid.UUID
        98    ) -> Message:
        99        """
       100        Delete an item.
       101        """
       102        item = session.get(Item, id)
       103        if not item:
       104            raise HTTPException(status_code=404, detail="Item not found")
       105        if not current_user.is_superuser and (item.owner_id != current_user.id):
       106            raise HTTPException(status_code=400, detail="Not enough permissions")
       107        session.delete(item)
       108        session.commit()
       109        return Message(message="Item deleted successfully")
         1    from datetime import timedelta
         2    from typing import Annotated, Any
         3
         4    from fastapi import APIRouter, Depends, HTTPException
         5    from fastapi.responses import HTMLResponse
         6    from fastapi.security import OAuth2PasswordRequestForm
         7
         8    from app import crud
         9    from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
        10    from app.core import security
        11    from app.core.config import settings
        12    from app.core.security import get_password_hash
        13    from app.models import Message, NewPassword, Token, UserPublic
        14    from app.utils import (
        15        generate_password_reset_token,
        16        generate_reset_password_email,
        17        send_email,
        18        verify_password_reset_token,
        19    )
        20
        21    router = APIRouter(tags=["login"])
        22
        23
        24    @router.post("/login/access-token")
        25    def login_access_token(
        26        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        27    ) -> Token:
        28        """
        29        OAuth2 compatible token login, get an access token for future requests
        30        """
        31        user = crud.authenticate(
        32            session=session, email=form_data.username, password=form_data.password
        33        )
        34        if not user:
        35            raise HTTPException(status_code=400, detail="Incorrect email or password")
        36        elif not user.is_active:
        37            raise HTTPException(status_code=400, detail="Inactive user")
        38        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        39        return Token(
        40            access_token=security.create_access_token(
        41                user.id, expires_delta=access_token_expires
        42            )
        43        )
        44
        45
        46    @router.post("/login/test-token", response_model=UserPublic)
        47    def test_token(current_user: CurrentUser) -> Any:
        48        """
        49        Test access token
        50        """
        51        return current_user
        52
        53
        54    @router.post("/password-recovery/{email}")
        55    def recover_password(email: str, session: SessionDep) -> Message:
        56        """
        57        Password Recovery
        58        """
        59        user = crud.get_user_by_email(session=session, email=email)
        60
        61        if not user:
        62            raise HTTPException(
        63                status_code=404,
        64                detail="The user with this email does not exist in the system.",
        65            )
        66        password_reset_token = generate_password_reset_token(email=email)
        67        email_data = generate_reset_password_email(
        68            email_to=user.email, email=email, token=password_reset_token
        69        )
        70        send_email(
        71            email_to=user.email,
        72            subject=email_data.subject,
        73            html_content=email_data.html_content,
        74        )
        75        return Message(message="Password recovery email sent")
        76
        77
        78    @router.post("/reset-password/")
        79    def reset_password(session: SessionDep, body: NewPassword) -> Message:
        80        """
        81        Reset password
        82        """
        83        email = verify_password_reset_token(token=body.token)
        84        if not email:
        85            raise HTTPException(status_code=400, detail="Invalid token")
        86        user = crud.get_user_by_email(session=session, email=email)
        87        if not user:
        88            raise HTTPException(
        89                status_code=404,
        90                detail="The user with this email does not exist in the system.",
        91            )
        92        elif not user.is_active:
        93            raise HTTPException(status_code=400, detail="Inactive user")
        94        hashed_password = get_password_hash(password=body.new_password)
        95        user.hashed_password = hashed_password
        96        session.add(user)
        97        session.commit()
        98        return Message(message="Password updated successfully")
        99
       100
       101    @router.post(
       102        "/password-recovery-html-content/{email}",
       103        dependencies=[Depends(get_current_active_superuser)],
       104        response_class=HTMLResponse,
       105    )
       106    def recover_password_html_content(email: str, session: SessionDep) -> Any:
       107        """
       108        HTML Content for Password Recovery
       109        """
       110        user = crud.get_user_by_email(session=session, email=email)
       111
       112        if not user:
       113            raise HTTPException(
       114                status_code=404,
       115                detail="The user with this username does not exist in the system.",
       116            )
       117        password_reset_token = generate_password_reset_token(email=email)
       118        email_data = generate_reset_password_email(
       119            email_to=user.email, email=email, token=password_reset_token
       120        )
       121
       122        return HTMLResponse(
       123            content=email_data.html_content, headers={"subject:": email_data.subject}
       124        )
    import uuid

    from pydantic import EmailStr
    from sqlmodel import Field, Relationship, SQLModel


    # Shared properties
    class UserBase(SQLModel):
        email: EmailStr = Field(unique=True, index=True, max_length=255)
        is_active: bool = True
        is_superuser: bool = False
        full_name: str | None = Field(default=None, max_length=255)


    # Properties to receive via API on creation
    class UserCreate(UserBase):
        password: str = Field(min_length=8, max_length=40)


    class UserRegister(SQLModel):
        email: EmailStr = Field(max_length=255)
        password: str = Field(min_length=8, max_length=40)
        full_name: str | None = Field(default=None, max_length=255)


    # Properties to receive via API on update, all are optional
    class UserUpdate(UserBase):
        email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
        password: str | None = Field(default=None, min_length=8, max_length=40)


    class UserUpdateMe(SQLModel):
        full_name: str | None = Field(default=None, max_length=255)
        email: EmailStr | None = Field(default=None, max_length=255)


    class UpdatePassword(SQLModel):
        current_password: str = Field(min_length=8, max_length=40)
        new_password: str = Field(min_length=8, max_length=40)


    # Database model, database table inferred from class name
    class User(UserBase, table=True):
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        hashed_password: str
        items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


    # Properties to return via API, id is always required
    class UserPublic(UserBase):
        id: uuid.UUID


    class UsersPublic(SQLModel):
        data: list[UserPublic]
        count: int


    # Shared properties
    class ItemBase(SQLModel):
        title: str = Field(min_length=1, max_length=255)
        description: str | None = Field(default=None, max_length=255)


    # Properties to receive on item creation
    class ItemCreate(ItemBase):
        pass


    # Properties to receive on item update
    class ItemUpdate(ItemBase):
        title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


    # Database model, database table inferred from class name
    class Item(ItemBase, table=True):
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        owner_id: uuid.UUID = Field(
            foreign_key="user.id", nullable=False, ondelete="CASCADE"
        )
        owner: User | None = Relationship(back_populates="items")


    # Properties to return via API, id is always required
    class ItemPublic(ItemBase):
        id: uuid.UUID
        owner_id: uuid.UUID


    class ItemsPublic(SQLModel):
        data: list[ItemPublic]
        count: int


    # Generic message
    class Message(SQLModel):
        message: str


    # JSON payload containing access token
    class Token(SQLModel):
        access_token: str
        token_type: str = "bearer"


    # Contents of JWT token
    class TokenPayload(SQLModel):
        sub: str | None = None


    class NewPassword(SQLModel):
        token: str
        new_password: str = Field(min_length=8, max_length=40)
    import uuid
    from typing import Any

    from sqlmodel import Session, select

    from app.core.security import get_password_hash, verify_password
    from app.models import Item, ItemCreate, User, UserCreate, UserUpdate


    def create_user(*, session: Session, user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


    def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        db_user.sqlmodel_update(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


    def get_user_by_email(*, session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = session.exec(statement).first()
        return session_user


    def authenticate(*, session: Session, email: str, password: str) -> User | None:
        db_user = get_user_by_email(session=session, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user


    def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
        db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    import logging
    from dataclasses import dataclass
    from datetime import datetime, timedelta, timezone
    from pathlib import Path
    from typing import Any

    import emails  # type: ignore
    import jwt
    from jinja2 import Template
    from jwt.exceptions import InvalidTokenError

    from app.core import security
    from app.core.config import settings

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    @dataclass
    class EmailData:
        html_content: str
        subject: str


    def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
        template_str = (
            Path(__file__).parent / "email-templates" / "build" / template_name
        ).read_text()
        html_content = Template(template_str).render(context)
        return html_content


    def send_email(
        *,
        email_to: str,
        subject: str = "",
        html_content: str = "",
    ) -> None:
        assert settings.emails_enabled, "no provided configuration for email variables"
        message = emails.Message(
            subject=subject,
            html=html_content,
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
        if settings.SMTP_TLS:
            smtp_options["tls"] = True
        elif settings.SMTP_SSL:
            smtp_options["ssl"] = True
        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER
        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD
        response = message.send(to=email_to, smtp=smtp_options)
        logger.info(f"send email result: {response}")


    def generate_test_email(email_to: str) -> EmailData:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Test email"
        html_content = render_email_template(
            template_name="test_email.html",
            context={"project_name": settings.PROJECT_NAME, "email": email_to},
        )
        return EmailData(html_content=html_content, subject=subject)


    def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Password recovery for user {email}"
        link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"
        html_content = render_email_template(
            template_name="reset_password.html",
            context={
                "project_name": settings.PROJECT_NAME,
                "username": email,
                "email": email_to,
                "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
                "link": link,
            },
        )
        return EmailData(html_content=html_content, subject=subject)


    def generate_new_account_email(
        email_to: str, username: str, password: str
    ) -> EmailData:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - New account for user {username}"
        html_content = render_email_template(
            template_name="new_account.html",
            context={
                "project_name": settings.PROJECT_NAME,
                "username": username,
                "password": password,
                "email": email_to,
                "link": settings.FRONTEND_HOST,
            },
        )
        return EmailData(html_content=html_content, subject=subject)


    def generate_password_reset_token(email: str) -> str:
        delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        now = datetime.now(timezone.utc)
        expires = now + delta
        exp = expires.timestamp()
        encoded_jwt = jwt.encode(
            {"exp": exp, "nbf": now, "sub": email},
            settings.SECRET_KEY,
            algorithm=security.ALGORITHM,
        )
        return encoded_jwt


    def verify_password_reset_token(token: str) -> str | None:
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            return str(decoded_token["sub"])
        except InvalidTokenError:
            return None
    ✓ • 4ms

## Activity

    $ python3 -u - <<'PY'
        import pathlib,tempfile,subprocess,shutil,json
        root=pathlib.Path.cwd();tmp=pathlib.Path(tempfile.mkdtemp(prefix='frontend-audit-'))
        shutil.copytree(root/'frontend',tmp/'frontend',ignore=shutil.ignore_patterns('node_modules','dist','.git'))
        cmd=['docker','run','--rm','--memory=768m','-v',str(tmp/'frontend')+':/app','-v',str(root/'frontend/node_modules')+':/app/node_modules:ro','-w','/app','node:20.18.1']
        for step in [['npm','run','build'],['./node_modules/.bin/biome','check','--no-errors-on-unmatched','--files-ignore-unknown=true','./'],['npx','--no-install','playwright','test','--list']]:
         r=subprocess.run(cmd+step);print('FRONTEND_CHECK',step,'EXIT',r.returncode,flush=True)
        r=subprocess.run(cmd+['npm','audit','--json'],capture_output=True,text=True)
        (tmp/'npm-audit.json').write_text(r.stdout)
        try:
         d=json.loads(r.stdout); print('NPM_AUDIT',d.get('metadata',{}).get('vulnerabilities'),d.get('error'))
         for name,v in d.get('vulnerabilities',{}).items():
          if v['severity']=='critical':print('CRITICAL_PACKAGE',name,'direct',v.get('isDirect'),'fixAvailable',v.get('fixAvailable'))
        except Exception:print('NPM_AUDIT_PARSE_FAILED',r.returncode,r.stderr[:400])
        print('FRONTEND_TMP',tmp)
        PY

    > frontend@0.0.0 build
    > tsc -p tsconfig.build.json && vite build


    <--- Last few GCs --->

    [19:0x1df33ee0]    84061 ms: Mark-Compact (reduce) 382.9 (393.6) -> 381.8 (391.6) MB, 277.62 / 0.04 ms  (+ 157.7 ms in 24 steps since start of marking, biggest step 12.7 ms, walltime since start of marking 1064 ms) (average mu = 0.738, current mu = 0.679)[19:0x1df33ee0]    85085 ms: Mark-Compact (reduce) 382.8 (391.6) -> 381.7 (391.8) MB, 882.82 / 0.00 ms  (average mu = 0.491, current mu = 0.138) allocation failure; scavenge might not succeed


    <--- JS stacktrace --->

    FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
    ----- Native stack trace -----

     1: 0xb8d0a3 node::OOMErrorHandler(char const*, v8::OOMDetails const&) [node]
     2: 0xf06250 v8::Utils::ReportOOMFailure(v8::internal::Isolate*, char const*, v8::OOMDetails const&) [node]
     3: 0xf06537 v8::internal::V8::FatalProcessOutOfMemory(v8::internal::Isolate*, char const*, v8::OOMDetails const&) [node]
     4: 0x11180d5  [node]
     5: 0x112ff58 v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) [node]
     6: 0x1106071 v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) [node]
     7: 0x1107205 v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) [node]
     8: 0x10e3926 v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment) [node]
     9: 0x10d509c v8::internal::FactoryBase<v8::internal::Factory>::AllocateRawArray(int, v8::internal::AllocationType) [node]
    10: 0x10d5204 v8::internal::FactoryBase<v8::internal::Factory>::NewFixedArrayWithFiller(v8::internal::Handle<v8::internal::Map>, int, v8::internal::Handle<v8::internal::Oddball>, v8::internal::AllocationType) [node]
    11: 0x1404fbd v8::internal::OrderedHashTable<v8::internal::OrderedHashMap, 2>::Allocate(v8::internal::Isolate*, int, v8::internal::AllocationType) [node]
    12: 0x1405063 v8::internal::OrderedHashTable<v8::internal::OrderedHashMap, 2>::Rehash(v8::internal::Isolate*, v8::internal::Handle<v8::internal::OrderedHashMap>, int) [node]
    13: 0x1535c73 v8::internal::Runtime_MapGrow(int, unsigned long*, v8::internal::Isolate*) [node]
    14: 0x1979ef6  [node]
    Aborted (core dumped)
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice
    FRONTEND_CHECK ['npm', 'run', 'build'] EXIT 134
    ./src/client/sdk.gen.ts:49:8 lint/complexity/noStaticOnlyClass ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Avoid classes that contain only static members.

         47 │ } from "./types.gen"
         48 │
       > 49 │ export class ItemsService {
            │        ^^^^^^^^^^^^^^^^^^^^
       > 50 │   /**
             ...
      > 167 │   }
      > 168 │ }
            │ ^
        169 │
        170 │ export class LoginService {

      i Prefer using simple functions instead of classes with only static members.


    ./src/client/sdk.gen.ts:170:8 lint/complexity/noStaticOnlyClass ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Avoid classes that contain only static members.

        168 │ }
        169 │
      > 170 │ export class LoginService {
            │        ^^^^^^^^^^^^^^^^^^^^
      > 171 │   /**
             ...
      > 272 │   }
      > 273 │ }
            │ ^
        274 │
        275 │ export class UsersService {

      i Prefer using simple functions instead of classes with only static members.


    ./src/client/sdk.gen.ts:275:8 lint/complexity/noStaticOnlyClass ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Avoid classes that contain only static members.

        273 │ }
        274 │
      > 275 │ export class UsersService {
            │        ^^^^^^^^^^^^^^^^^^^^
      > 276 │   /**
             ...
      > 485 │   }
      > 486 │ }
            │ ^
        487 │
        488 │ export class UtilsService {

      i Prefer using simple functions instead of classes with only static members.


    ./src/client/sdk.gen.ts:488:8 lint/complexity/noStaticOnlyClass ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Avoid classes that contain only static members.

        486 │ }
        487 │
      > 488 │ export class UtilsService {
            │        ^^^^^^^^^^^^^^^^^^^^
      > 489 │   /**
             ...
      > 521 │     })
      > 522 │   }
      > 523 │ }
            │ ^
        524 │

      i Prefer using simple functions instead of classes with only static members.


    ./src/client/sdk.gen.ts organizeImports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      i Import statements could be sorted:

          5   5 │   import { request as __request } from "./core/request"
          6   6 │   import type {
          7     │ - ··ItemsReadItemsData,
          8     │ - ··ItemsReadItemsResponse,
          9     │ - ··ItemsCreateItemData,
         10     │ - ··ItemsCreateItemResponse,
              7 │ + ··ItemsCreateItemData,
              8 │ + ··ItemsCreateItemResponse,
              9 │ + ··ItemsDeleteItemData,
             10 │ + ··ItemsDeleteItemResponse,
         11  11 │     ItemsReadItemData,
         12  12 │     ItemsReadItemResponse,
         13     │ - ··ItemsUpdateItemData,
         14     │ - ··ItemsUpdateItemResponse,
         15     │ - ··ItemsDeleteItemData,
         16     │ - ··ItemsDeleteItemResponse,
             13 │ + ··ItemsReadItemsData,
             14 │ + ··ItemsReadItemsResponse,
             15 │ + ··ItemsUpdateItemData,
             16 │ + ··ItemsUpdateItemResponse,
         17  17 │     LoginLoginAccessTokenData,
         18  18 │     LoginLoginAccessTokenResponse,
         19     │ - ··LoginTestTokenResponse,
         20     │ - ··LoginRecoverPasswordData,
             19 │ + ··LoginRecoverPasswordData,
             20 │ + ··LoginRecoverPasswordHtmlContentData,
             21 │ + ··LoginRecoverPasswordHtmlContentResponse,
         21  22 │     LoginRecoverPasswordResponse,
         22  23 │     LoginResetPasswordData,
         23  24 │     LoginResetPasswordResponse,
         24     │ - ··LoginRecoverPasswordHtmlContentData,
         25     │ - ··LoginRecoverPasswordHtmlContentResponse,
         26     │ - ··UsersReadUsersData,
         27     │ - ··UsersReadUsersResponse,
         28     │ - ··UsersCreateUserData,
         29     │ - ··UsersCreateUserResponse,
         30     │ - ··UsersReadUserMeResponse,
         31     │ - ··UsersDeleteUserMeResponse,
         32     │ - ··UsersUpdateUserMeData,
         33     │ - ··UsersUpdateUserMeResponse,
         34     │ - ··UsersUpdatePasswordMeData,
         35     │ - ··UsersUpdatePasswordMeResponse,
             25 │ + ··LoginTestTokenResponse,
             26 │ + ··UsersCreateUserData,
             27 │ + ··UsersCreateUserResponse,
             28 │ + ··UsersDeleteUserData,
             29 │ + ··UsersDeleteUserMeResponse,
             30 │ + ··UsersDeleteUserResponse,
             31 │ + ··UsersReadUserByIdData,
             32 │ + ··UsersReadUserByIdResponse,
             33 │ + ··UsersReadUserMeResponse,
             34 │ + ··UsersReadUsersData,
             35 │ + ··UsersReadUsersResponse,
         36  36 │     UsersRegisterUserData,
         37  37 │     UsersRegisterUserResponse,
         38     │ - ··UsersReadUserByIdData,
         39     │ - ··UsersReadUserByIdResponse,
             38 │ + ··UsersUpdatePasswordMeData,
             39 │ + ··UsersUpdatePasswordMeResponse,
         40  40 │     UsersUpdateUserData,
         41     │ - ··UsersUpdateUserResponse,
         42     │ - ··UsersDeleteUserData,
         43     │ - ··UsersDeleteUserResponse,
         44     │ - ··UtilsTestEmailData,
         45     │ - ··UtilsTestEmailResponse,
         46     │ - ··UtilsHealthCheckResponse,
             41 │ + ··UsersUpdateUserMeData,
             42 │ + ··UsersUpdateUserMeResponse,
             43 │ + ··UsersUpdateUserResponse,
             44 │ + ··UtilsHealthCheckResponse,
             45 │ + ··UtilsTestEmailData,
             46 │ + ··UtilsTestEmailResponse,
         47  47 │   } from "./types.gen"
         48  48 │


    ./src/client/core/CancelablePromise.ts:87:10 lint/suspicious/noThenProperty ━━━━━━━━━━━━━━━━━━━━━━━━

      × Do not add then to a class.

        85 │   }
        86 │
      > 87 │   public then<TResult1 = T, TResult2 = never>(
           │          ^^^^
        88 │     onFulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | null,
        89 │     onRejected?: ((reason: unknown) => TResult2 | PromiseLike<TResult2>) | null,


    ./src/client/core/request.ts:60:7 lint/complexity/noForEach ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Prefer for...of instead of forEach.

        58 │       append(key, value.toISOString())
        59 │     } else if (Array.isArray(value)) {
      > 60 │       value.forEach((v) => encodePair(key, v))
           │       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        61 │     } else if (typeof value === "object") {
        62 │       Object.entries(value).forEach(([k, v]) => encodePair(`${key}[${k}]`, v))

      i forEach may lead to performance issues when working with large arrays. When combined with functions like filter or map, this causes multiple iterations over the same type.


    ./src/client/core/request.ts:62:7 lint/complexity/noForEach ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Prefer for...of instead of forEach.

        60 │       value.forEach((v) => encodePair(key, v))
        61 │     } else if (typeof value === "object") {
      > 62 │       Object.entries(value).forEach(([k, v]) => encodePair(`${key}[${k}]`, v))
           │       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        63 │     } else {
        64 │       append(key, value)

      i forEach may lead to performance issues when working with large arrays. When combined with functions like filter or map, this causes multiple iterations over the same type.


    ./src/client/core/request.ts:68:3 lint/complexity/noForEach ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Prefer for...of instead of forEach.

        66 │   }
        67 │
      > 68 │   Object.entries(params).forEach(([key, value]) => encodePair(key, value))
           │   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        69 │
        70 │   return qs.length ? `?${qs.join("&")}` : ""

      i forEach may lead to performance issues when working with large arrays. When combined with functions like filter or map, this causes multiple iterations over the same type.


    ./src/client/core/request.ts:79:25 lint/suspicious/noPrototypeBuiltins ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Do not access Object.prototype method 'hasOwnProperty' from target object.

        77 │     .replace("{api-version}", config.VERSION)
        78 │     .replace(/{(.*?)}/g, (substring: string, group: string) => {
      > 79 │       if (options.path?.hasOwnProperty(group)) {
           │                         ^^^^^^^^^^^^^^
        80 │         return encoder(String(options.path[group]))
        81 │       }

      i It's recommended using Object.hasOwn() instead of using Object.hasOwnProperty().

      i See MDN web docs for more details.


    ./src/client/core/request.ts:103:5 lint/complexity/noForEach ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Prefer for...of instead of forEach.

        101 │     }
        102 │
      > 103 │     Object.entries(options.formData)
            │     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      > 104 │       .filter(([, value]) => value !== undefined && value !== null)
             ...
      > 110 │         }
      > 111 │       })
            │       ^^
        112 │
        113 │     return formData

      i forEach may lead to performance issues when working with large arrays. When combined with functions like filter or map, this causes multiple iterations over the same type.


    ./src/client/core/request.ts:107:11 lint/complexity/noForEach ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Prefer for...of instead of forEach.

        105 │       .forEach(([key, value]) => {
        106 │         if (Array.isArray(value)) {
      > 107 │           value.forEach((v) => process(key, v))
            │           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        108 │         } else {
        109 │           process(key, value)

      i forEach may lead to performance issues when working with large arrays. When combined with functions like filter or map, this causes multiple iterations over the same type.


    ./src/client/core/request.ts:160:13 lint/complexity/useLiteralKeys  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━

      × The computed expression can be simplified without the use of a string literal.

        159 │   if (isStringWithValue(token)) {
      > 160 │     headers["Authorization"] = `Bearer ${token}`
            │             ^^^^^^^^^^^^^^^
        161 │   }
        162 │

      i Unsafe fix: Use a literal key instead.

        158 158 │
        159 159 │     if (isStringWithValue(token)) {
        160     │ - ····headers["Authorization"]·=·`Bearer·${token}`
            160 │ + ····headers.Authorization·=·`Bearer·${token}`
        161 161 │     }
        162 162 │


    ./src/client/core/request.ts:165:13 lint/complexity/useLiteralKeys  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━

      × The computed expression can be simplified without the use of a string literal.

        163 │   if (isStringWithValue(username) && isStringWithValue(password)) {
        164 │     const credentials = base64(`${username}:${password}`)
      > 165 │     headers["Authorization"] = `Basic ${credentials}`
            │             ^^^^^^^^^^^^^^^
        166 │   }
        167 │

      i Unsafe fix: Use a literal key instead.

        163 163 │     if (isStringWithValue(username) && isStringWithValue(password)) {
        164 164 │       const credentials = base64(`${username}:${password}`)
        165     │ - ····headers["Authorization"]·=·`Basic·${credentials}`
            165 │ + ····headers.Authorization·=·`Basic·${credentials}`
        166 166 │     }
        167 167 │


    ./src/client/core/request.ts:153:9 lint/performance/noAccumulatingSpread ━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Avoid the use of spread (`...`) syntax on accumulators.

        151 │     .reduce(
        152 │       (headers, [key, value]) => ({
      > 153 │         ...headers,
            │         ^^^^^^^^^^
        154 │         [key]: String(value),
        155 │       }),

      i Spread syntax should be avoided on accumulators (like those in `.reduce`) because it causes a time complexity of `O(n^2)`.

      i Consider methods such as .splice or .push instead.


    ./src/client/core/request.ts organizeImports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      i Import statements could be sorted:

          2   2 │   import type {
          3   3 │     AxiosError,
          4     │ - ··AxiosRequestConfig,
          5     │ - ··AxiosResponse,
          6     │ - ··AxiosInstance,
              4 │ + ··AxiosInstance,
              5 │ + ··AxiosRequestConfig,
              6 │ + ··AxiosResponse,
          7   7 │   } from "axios"
          8   8 │


    Checked 80 files in 547ms. No fixes needed.
    Found 22 errors.
    check ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      × Some errors were emitted while running checks.


    FRONTEND_CHECK ['./node_modules/.bin/biome', 'check', '--no-errors-on-unmatched', '--files-ignore-unknown=true', './'] EXIT 1

    Error: Environment variable FIRST_SUPERUSER is undefined

       at config.ts:13

      11 |
      12 | if (typeof FIRST_SUPERUSER !== "string") {
    > 13 |   throw new Error("Environment variable FIRST_SUPERUSER is undefined")
         |         ^
      14 | }
      15 |
      16 | if (typeof FIRST_SUPERUSER_PASSWORD !== "string") {

        at /app/tests/config.ts:13:9

    Error: Environment variable FIRST_SUPERUSER is undefined

       at config.ts:13

      11 |
      12 | if (typeof FIRST_SUPERUSER !== "string") {
    > 13 |   throw new Error("Environment variable FIRST_SUPERUSER is undefined")
         |         ^
      14 | }
      15 |
      16 | if (typeof FIRST_SUPERUSER_PASSWORD !== "string") {

        at /app/tests/config.ts:13:9

    SyntaxError: The requested module '../../src/client' does not provide an export named 'PrivateService'
    Listing tests:
    Total: 0 tests in 0 files
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice
    FRONTEND_CHECK ['npx', '--no-install', 'playwright', 'test', '--list'] EXIT 1
    NPM_AUDIT {'info': 0, 'low': 0, 'moderate': 4, 'high': 55, 'critical': 3, 'total': 62} None
    CRITICAL_PACKAGE form-data direct True fixAvailable {'name': 'form-data', 'version': '4.0.6', 'isSemVerMajor': False}
    CRITICAL_PACKAGE handlebars direct False fixAvailable {'name': '@hey-api/openapi-ts', 'version': '0.99.0', 'isSemVerMajor': True}
    CRITICAL_PACKAGE tar direct False fixAvailable {'name': '@hey-api/openapi-ts', 'version': '0.99.0', 'isSemVerMajor': True}
    FRONTEND_TMP /tmp/frontend-audit-4ne54tvs
    ✓ • 4m 24s

## Activity

    $ python3 -u - <<'PY'
        import subprocess,os,tempfile,pathlib,yaml,json
        os.environ['PATH']='/tmp/ci-bin:'+os.environ['PATH'];os.environ['PYTHONDONTWRITEBYTECODE']='1'
        tmp=pathlib.Path(tempfile.mkdtemp(prefix='audit-validation-'));print('OUTPUT',tmp,flush=True)
        commands=[['python3','-B','-m','unittest','discover','-s','ci','-p','test_*.py']]
        for i,cmd in enumerate(commands):
         r=subprocess.run(cmd,capture_output=True,text=True);(tmp/f'check-{i}.log').write_text(r.stdout+r.stderr); print('TEST',r.returncode,(r.stdout+r.stderr)[-1200:],flush=True)
        for env in ['dev','stage','prod']:
         r=subprocess.run(['kustomize','build',f'deploy/overlays/{env}'],capture_output=True,text=True);p=tmp/f'{env}.yaml';p.write_text(r.stdout);print('RENDER',env,r.returncode,flush=True)
         for cmd in [['kubeconform','-strict','-summary','-kubernetes-version','1.31.0',str(p)],['kubectl','--context','kind-fastapi-dev','--request-timeout=10s','apply','--dry-run=client','-f',str(p)]]:
          r=subprocess.run(cmd,capture_output=True,text=True);print(cmd[0],env,r.returncode,r.stdout,r.stderr[-600:],flush=True)
        for env in ['dev','prod']:
         r=subprocess.run(['kustomize','build',f'k8s/overlays/{env}'],capture_output=True,text=True);print('LEGACY',env,r.returncode,r.stderr[-900:],flush=True)
        count=0
        for f in dict.fromkeys(subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines()):
         p=pathlib.Path(f)
         if p.suffix in ['.yaml','.yml'] and p.is_file():
          try:list(yaml.safe_load_all(p.read_text()));count+=1
          except Exception as e:print('YAML_ERROR',f,str(e)[:200])
        print('YAML',count)
        for f in [*pathlib.Path('scripts').glob('*.sh'),*pathlib.Path('ci').glob('*.sh'),*pathlib.Path('backend/scripts').glob('*.sh'),pathlib.Path('infra/jenkins-host/run-tool.sh')]:
         shell='bash' if 'bash' in f.read_text().splitlines()[0] else 'sh';r=subprocess.run([shell,'-n',str(f)],capture_output=True,text=True)
         print('SHELL',f,r.returncode,r.stderr[:200])
        PY
    OUTPUT /tmp/audit-validation-083f83p4
    TEST 0 m1/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmp4nbduu3d/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmpqq5z3do4/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpqq5z3do4/remote.git
       00ad7e4..ff6dd78  HEAD -> main
    .Cloning into '/tmp/tmp5q2rwgvr/work'...
    warning: You appear to have cloned an empty repository.
    done.
    .Cloning into '/tmp/tmpan9dmtfq/work'...
    warning: You appear to have cloned an empty repository.
    done.
    To /tmp/tmpan9dmtfq/remote.git
     ! [rejected]        HEAD -> main (fetch first)
    error: failed to push some refs to '/tmp/tmpan9dmtfq/remote.git'
    hint: Updates were rejected because the remote contains work that you do not
    hint: have locally. This is usually caused by another repository pushing to
    hint: the same ref. If you want to integrate the remote changes, use
    hint: 'git pull' before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.
    To /tmp/tmpan9dmtfq/remote.git
       36e4e6f..3ea27a5  HEAD -> main
    ....
    ----------------------------------------------------------------------
    Ran 12 tests in 96.646s

    OK

    RENDER dev 0
    kubeconform dev 0 Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0

    kubectl dev 0 configmap/backend-config configured (dry run)
    configmap/db-config configured (dry run)
    service/adminer configured (dry run)
    service/backend configured (dry run)
    service/db configured (dry run)
    service/frontend configured (dry run)
    persistentvolumeclaim/postgres-vol configured (dry run)
    deployment.apps/adminer configured (dry run)
    deployment.apps/backend configured (dry run)
    deployment.apps/frontend configured (dry run)
    deployment.apps/postgres-deployment configured (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress configured (dry run)

    RENDER stage 0
    kubeconform stage 0 Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0

    kubectl stage 0 configmap/backend-config configured (dry run)
    configmap/db-config configured (dry run)
    service/adminer configured (dry run)
    service/backend configured (dry run)
    service/db configured (dry run)
    service/frontend configured (dry run)
    persistentvolumeclaim/postgres-vol configured (dry run)
    deployment.apps/adminer configured (dry run)
    deployment.apps/backend configured (dry run)
    deployment.apps/frontend configured (dry run)
    deployment.apps/postgres-deployment configured (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress configured (dry run)

    RENDER prod 0
    kubeconform prod 0 Summary: 13 resources found in 1 file - Valid: 13, Invalid: 0, Errors: 0, Skipped: 0

    kubectl prod 0 configmap/backend-config created (dry run)
    configmap/db-config created (dry run)
    service/adminer created (dry run)
    service/backend created (dry run)
    service/db created (dry run)
    service/frontend created (dry run)
    persistentvolumeclaim/postgres-vol created (dry run)
    deployment.apps/adminer created (dry run)
    deployment.apps/backend created (dry run)
    deployment.apps/frontend created (dry run)
    deployment.apps/postgres-deployment created (dry run)
    job.batch/prestart created (dry run)
    ingress.networking.k8s.io/app-ingress created (dry run)

    LEGACY dev 0
    LEGACY prod 0
    YAML 87
    SHELL scripts/build.sh 0
    SHELL scripts/test-local.sh 0
    SHELL scripts/bootstrap-kind.sh 0
    SHELL scripts/test.sh 0
    SHELL scripts/build-push.sh 0
    SHELL scripts/deploy.sh 0
    SHELL scripts/generate-client.sh 0
    SHELL ci/tools.sh 0
    SHELL ci/validate.sh 0
    SHELL ci/publish.sh 0
    SHELL backend/scripts/format.sh 0
    SHELL backend/scripts/tests-start.sh 0
    SHELL backend/scripts/test.sh 0
    SHELL backend/scripts/prestart.sh 0
    SHELL backend/scripts/lint.sh 0
    SHELL infra/jenkins-host/run-tool.sh 0
    ✓ • 1m 59s

## Activity

    $ python3 -u - <<'PY'
        import pathlib,subprocess
        p=sorted(pathlib.Path('/tmp').glob('frontend-audit-*'),key=lambda p:p.stat().st_mtime)[-1]/'frontend'
        cmd=['docker','run','--rm','--memory=2g','--cpus=1','-e','NODE_OPTIONS=--max-old-space-size=1536','-e','FIRST_SUPERUSER=audit@example.com','-e','FIRST_SUPERUSER_PASSWORD=audit-test-only','-e','VITE_API_URL=http://backend:8000','-v',str(p)+':/app','-v',str(pathlib.Path.cwd()/'frontend/node_modules')+':/app/node_modules:ro','-w','/app','node:20.18.1']
        for step in [['npm','run','build'],['npx','--no-install','playwright','test','--list']]:
         r=subprocess.run(cmd+step,capture_output=True,text=True);(p.parent/('build-recheck.log' if step[0]=='npm' else 'playwright-list.log')).write_text(r.stdout+r.stderr);print('RECHECK',step,r.returncode,(r.stdout+r.stderr)[-2000:],flush=True)
        PY
    RECHECK ['npm', 'run', 'build'] 0
    > frontend@0.0.0 build
    > tsc -p tsconfig.build.json && vite build


    ♻️  Generating routes...
    ✅ Processed routes in 2070ms
    vite v5.4.14 building for production...
    transforming...
    ✓ 1385 modules transformed.
    rendering chunks...
    computing gzip size...
    dist/index.html                  0.48 kB │ gzip:   0.31 kB
    dist/assets/index-jgUzIW1W.js  825.87 kB │ gzip: 242.16 kB
    ✓ built in 56.94s
    src/components/ui/provider.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/toaster.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/color-mode.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/password-input.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/hooks/useCustomToast.ts (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/pagination.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/menu.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.
    src/components/ui/link-button.tsx (1:0): Error when using sourcemap for reporting an error: Can't resolve original location of error.

    (!) Some chunks are larger than 500 kB after minification. Consider:
    - Using dynamic import() to code-split the application
    - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
    - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice

    RECHECK ['npx', '--no-install', 'playwright', 'test', '--list'] 1 Listing tests:
    Total: 0 tests in 0 files

    SyntaxError: The requested module '../../src/client' does not provide an export named 'PrivateService'
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice

    ✓ • 2m 48s

## Activity

    $ python3 - <<'PY'
        from pathlib import Path
        import subprocess,json
        root=Path.cwd();files=subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines()
        print('File categories:')
        for prefix in ['backend/app/','frontend/src/','frontend/tests/','scripts/','ci/','infra/','monitoring/','.github/workflows/']:
         selected=[p for p in dict.fromkeys(files) if p.startswith(prefix) and Path(p).is_file()]
         print(prefix,len(selected))
         for p in selected:
          if p.endswith(('.py','.sh','.groovy','.yaml','.yml','.tsx','.ts','.toml','.json')) and not ('client/' in p or p.endswith('package-lock.json')):
           text=Path(p).read_text(errors='replace')
           if prefix in ['scripts/','infra/']:
            for i,line in enumerate(text.splitlines(),1):
             if any(s in line for s in ['privileged','0.0.0.0','password','chmod','requests.','verify=False','http://','disabled','docker.sock']):
              if any(s in line.lower() for s in ['password','token','secret','auth']):continue
              print(p,i,line.strip()[:180])
        PY
        nl -ba k8s/overlays/dev/kustomization.yaml; nl -ba k8s/overlays/prod/kustomization.yaml; nl -ba backend/Dockerfile; nl -ba frontend/Dockerfile; nl -ba frontend/.dockerignore; nl -ba backend/.dockerignore; nl -ba .gitignore; nl -ba argocd/bootstrap/dev-namespace.yaml
    File categories:
    backend/app/ 52
    frontend/src/ 64
    frontend/tests/ 10
    scripts/ 18
    scripts/bootstrap-jenkins-host.py 25 req=urllib.request.Request('http://127.0.0.1:8085'+path,data=data,headers=headers)
    scripts/bootstrap-jenkins-host.py 100 agent_path.chmod(0o600)
    scripts/bootstrap-jenkins-host.py 108 cli.chmod(0o755)
    scripts/bootstrap-jenkins-host.py 113 buildx.chmod(0o755)
    scripts/bootstrap-jenkins-host.py 117 '--restart','unless-stopped','--privileged','--cgroupns=private','--memory=1536m','--memory-swap=1536m','--cpus=1.25',
    scripts/bootstrap-kind.sh 37 p,ctx=sys.argv[1:]; os.chmod(p,0o600)
    scripts/create-stage-secrets.py 27 cert=Path(tmp)/'cert.pem'; cert.write_bytes(base64.b64decode(key['data']['tls.crt']));cert.chmod(0o600)
    scripts/recover-dev-secrets.py 22 p.chmod(0o600)
    scripts/recover-dev-secrets.py 26 cert.chmod(0o600)
    scripts/sync-jenkins-host-jobs.py 15 print('Updated local job definitions; history, disabled flags and credentials unchanged.')
    scripts/verify-kind-app.py 22 check('http://backend'+path,status)
    scripts/verify-kind-app.py 23 check('http://frontend/',200)
    scripts/verify-kind-app.py 24 check('http://adminer/',200)
    scripts/verify-kind-app.py 26 check('http://traefik.traefik.svc.cluster.local'+path,200,HOST)
    scripts/verify-kind-app.py 28 check('http://traefik.traefik.svc.cluster.local/docs',200,HOST)
    scripts/verify-kind-monitoring.py 21 prom='http://127.0.0.1:19090';graf='http://127.0.0.1:13000';am='http://127.0.0.1:19093'
    scripts/verify-kind-monitoring.py 45 with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1'+path,headers={'Host':host}),timeout=10) as response:
    ci/ 9
    infra/ 18
    infra/jenkins-host/jenkins.yaml 2 systemMessage: "Local bounded CI; GitOps remains in Argo CD. Publication disabled."
    infra/jenkins-host/jenkins.yaml 24 disabled: false
    infra/jenkins-host/jenkins.yaml 30 url: http://127.0.0.1:8085/
    infra/jenkins-host/jobs.groovy 9 disabled(true)
    infra/jenkins-host/jobs.groovy 15 disabled(true)
    infra/jenkins-host/jobs.groovy 16 definition { cps { script("error('Publishing is disabled until credentials and trust isolation are reviewed')"); sandbox() } }
    infra/jenkins-host/run-tool.sh 42 set -- "$@" --privileged -v /opt/host-ci/buildkit.toml:/etc/buildkit/host.toml:ro --entrypoint=sh
    infra/kind/app-stage-local.yaml 25 data:\n  FRONTEND_HOST: http://stage.example.com\n  BACKEND_CORS_ORIGINS:\
    infra/kind/app-stage-local.yaml 26 \ http://stage.example.com\n"
    monitoring/ 10
    .github/workflows/ 12
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3
         4    namespace: dev
         5
         6    resources:
         7      - ../../base
         1    apiVersion: kustomize.config.k8s.io/v1beta1
         2    kind: Kustomization
         3
         4    namespace: prod
         5
         6    resources:
         7      - ../../base
         8
         9    patches:
        10      - target:
        11          kind: Deployment
        12          name: backend
        13        patch: |-
        14          - op: replace
        15            path: /spec/replicas
        16            value: 2
        17      - target:
        18          kind: Deployment
        19          name: frontend
        20        patch: |-
        21          - op: replace
        22            path: /spec/replicas
        23            value: 2
        24      - target:
        25          kind: Ingress
        26          name: app-ingress
        27        patch: |-
        28          - op: replace
        29            path: /spec/rules/0/host
        30            value: api.yourdomain.com
        31          - op: replace
        32            path: /spec/rules/1/host
        33            value: dashboard.yourdomain.com
         1    FROM python:3.10.16-bookworm
         2
         3    ENV PYTHONUNBUFFERED=1
         4
         5    WORKDIR /app/
         6
         7    # Install uv
         8    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
         9    COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
        10
        11    # Place executables in the environment at the front of the path
        12    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
        13    ENV PATH="/app/.venv/bin:$PATH"
        14
        15    # Compile bytecode
        16    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
        17    ENV UV_COMPILE_BYTECODE=1
        18
        19    # uv Cache
        20    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
        21    ENV UV_LINK_MODE=copy
        22
        23    # Install dependencies
        24    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
        25    RUN --mount=type=cache,target=/root/.cache/uv \
        26        --mount=type=bind,source=uv.lock,target=uv.lock \
        27        --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
        28        uv sync --frozen --no-install-project
        29
        30    ENV PYTHONPATH=/app
        31
        32    COPY ./scripts /app/scripts
        33
        34    COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
        35
        36    COPY ./app /app/app
        37
        38    # Sync the project
        39    # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
        40    RUN --mount=type=cache,target=/root/.cache/uv \
        41        uv sync --frozen
        42
        43    CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
         1    # Stage 0, "build-stage", based on Node.js, to build and compile the frontend
         2    FROM node:20.18.1 AS build-stage
         3
         4    WORKDIR /app
         5
         6    COPY package*.json /app/
         7
         8    RUN npm ci
         9
        10    COPY ./ /app/
        11
        12    ARG VITE_API_URL=""
        13    ENV VITE_API_URL=${VITE_API_URL}
        14
        15    RUN npm run build
        16
        17
        18    # Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
        19    FROM nginx:1.27.3
        20
        21    COPY --from=build-stage /app/dist/ /usr/share/nginx/html
        22
        23    COPY ./nginx.conf /etc/nginx/conf.d/default.conf
        24    COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
         1    node_modules
         2    dist
         1    # Python
         2    __pycache__
         3    app.egg-info
         4    *.pyc
         5    .mypy_cache
         6    .coverage
         7    htmlcov
         8    .venv
         1    .vscode
         2    node_modules/
         3    /test-results/
         4    /playwright-report/
         5    /blob-report/
         6    /playwright/.cache/
         7
         8    # Local secrets and CI output (tracked template .env remains placeholders only)
         9    .env.*.local
        10    *.local.env
        11    rendered/
        12    *-ci.tar
        13    backend/test-results.xml
        14    backend/coverage.xml
        15    __pycache__/
        16
        17    # Python cache
        18    __pycache__/
        19    *.py[cod]
        20
        21    # Private recovery material and local kind tooling
        22    .migration-backup/
        23    sealed-secrets-key-backup.yaml
        24    .tools/
        25
        26    # Private host Jenkins bootstrap state
        27    .jenkins-host/
         1    # Operator bootstrap: fastapi AppProject intentionally cannot create Namespaces.
         2    apiVersion: v1
         3    kind: Namespace
         4    metadata:
         5      name: app-dev
    ✓ • 218ms

## Activity

    $ python3 -u - <<'PY'
        import subprocess,time,json,urllib.request,os
        base=['kubectl','--context','kind-fastapi-dev','--request-timeout=10s']
        p=subprocess.Popen(base+['-n','monitoring','port-forward','--address=127.0.0.1','svc/monitoring-prometheus','19090:9090'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
         for i in range(30):
          try:
           with urllib.request.urlopen('http://127.0.0.1:19090/-/ready',timeout=2) as r:print('PROMETHEUS_READY',r.status);break
          except Exception:
           if p.poll() is not None:raise RuntimeError('port forward unavailable')
           time.sleep(1)
         with urllib.request.urlopen('http://127.0.0.1:19090/api/v1/targets',timeout=10) as r:
          targets=json.load(r)['data']['activeTargets'];print('SCRAPE_TARGETS',len(targets),'UP',sum(t['health']=='up' for t in targets))
          for t in targets:
           if t['health']!='up':print('DOWN_TARGET',t['labels'].get('job'),t.get('lastError'))
         r=subprocess.run(['python3','-B','monitoring/test-alert-rules.py'],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=90);print('ALERT_TEST',r.returncode,r.stdout,r.stderr[-1500:])
        finally:
         p.terminate()
         try:p.wait(timeout=5)
         except subprocess.TimeoutExpired:p.kill();p.wait()
        PY
    PROMETHEUS_READY 200
    SCRAPE_TARGETS 16 UP 16
    ALERT_TEST 0   SUCCESS

    Eight live rules match local definitions; pending/firing/recovery and healthy boundary/isolation tests PASS

    ✓ • 9.93s

## Activity

    $ docker image inspect fastapi-repo-audit/backend:20261012 fastapi-repo-audit/frontend:20261012 --format '{{.RepoTags}} user={{json .Config.User}} size={{.Size}}'; docker compose version; git rev-list --all --count; nl -ba ci/test_publish.py | head -65; rg -n 'def test_' ci/test_promote.py ci/test_publish.py; rg -n '^(#|##)|pytest|generate-client|playwright|docker|backup|restore|terraform' backend/README.md frontend/README.md development.md SECURITY.md; nl -ba Jenkinsfile | tail -50; nl -ba Jenkinsfile.promote | tail -55; nl -ba scripts/verify-kind-app.py | tail -18
    [fastapi-repo-audit/backend:20261012] user="" size=459520290
    [fastapi-repo-audit/frontend:20261012] user="" size=72324679
    docker: unknown command: docker compose

    Run 'docker --help' for more information
    843
         1    """No network: execute publisher shell with a fake registry client."""
         2    import os
         3    from pathlib import Path
         4    import subprocess
         5    import tempfile
         6    import unittest
         7
         8    ROOT = Path(__file__).resolve().parents[1]
         9
        10
        11    class PublishTests(unittest.TestCase):
        12        def execute(self, behavior):
        13            with tempfile.TemporaryDirectory() as directory:
        14                root = Path(directory)
        15                binary = root / 'crane'
        16                binary.write_text('''#!/bin/sh
        17    printf '%s\\n' "$1" >> "$CALLS"
        18    case "$1" in
        19      auth) cat > /dev/null; exit 0 ;;
        20      digest)
        21        case "$BEHAVIOR" in
        22          exists) echo sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
        23          missing) echo MANIFEST_UNKNOWN >&2; exit 1 ;;
        24          denied) echo UNAUTHORIZED >&2; exit 1 ;;
        25        esac ;;
        26      push) exit 0 ;;
        27      *) exit 90 ;;
        28    esac
        29    ''')
        30                binary.chmod(0o700)
        31                calls = root / 'calls'
        32                env = dict(os.environ, PATH=f'{root}:{os.environ["PATH"]}', CALLS=str(calls),
        33                           BEHAVIOR=behavior, GHCR_USER='test-user', GHCR_TOKEN='test-token',
        34                           GIT_USER='test-git', GIT_TOKEN='test-git-token', PROMOTION_MODE='publish',
        35                           REGISTRY_NAMESPACE='example.invalid', IMAGE_SHA='a' * 40,
        36                           SOURCE_JOB='app-ci/feature-test')
        37                result = subprocess.run(['sh', str(ROOT / 'ci/publish.sh')], env=env,
        38                                        text=True, capture_output=True, cwd=root)
        39                self.assertNotIn('test-token', result.stdout + result.stderr)
        40                self.assertNotIn('test-git-token', result.stdout + result.stderr)
        41                return result.returncode, calls.read_text().splitlines()
        42
        43        def test_existing_sha_tags_are_never_pushed(self):
        44            status, calls = self.execute('exists')
        45            self.assertEqual(status, 0)
        46            self.assertEqual(calls.count('digest'), 2)
        47            self.assertNotIn('push', calls)
        48
        49        def test_missing_tags_copy_both_archives(self):
        50            status, calls = self.execute('missing')
        51            self.assertEqual(status, 0)
        52            self.assertEqual(calls.count('push'), 2)
        53
        54        def test_auth_error_fails_closed(self):
        55            status, calls = self.execute('denied')
        56            self.assertNotEqual(status, 0)
        57            self.assertNotIn('push', calls)
        58
        59
        60    if __name__ == '__main__':
        61        unittest.main()
    ci/test_publish.py:43:    def test_existing_sha_tags_are_never_pushed(self):
    ci/test_publish.py:49:    def test_missing_tags_copy_both_archives(self):
    ci/test_publish.py:54:    def test_auth_error_fails_closed(self):
    ci/test_promote.py:63:    def test_stage_records_exact_pair_and_is_idempotent(self):
    ci/test_promote.py:78:    def test_stale_stage_build_cannot_overwrite_new_source(self):
    ci/test_promote.py:84:    def test_unrelated_main_commit_survives_push_retry(self):
    ci/test_promote.py:101:    def test_missing_images_fail_before_git_write(self):
    ci/test_promote.py:107:    def test_dev_changes_only_dev(self):
    ci/test_promote.py:116:    def test_release_requires_stage_history(self):
    ci/test_promote.py:121:    def test_release_creates_only_review_branch_and_reuses_digests(self):
    ci/test_promote.py:142:    def test_release_refuses_moved_registry_tag(self):
    ci/test_promote.py:154:    def test_release_rejects_commit_outside_main(self):
    SECURITY.md:1:# Security Policy
    SECURITY.md:7:## Versions
    SECURITY.md:13:## Reporting a Vulnerability
    SECURITY.md:19:## Public Discussions
    backend/README.md:1:# FastAPI Project - Backend
    backend/README.md:3:## Requirements
    backend/README.md:5:* [Docker](https://www.docker.com/).
    backend/README.md:8:## Docker Compose
    backend/README.md:12:## General Workflow
    backend/README.md:32:## VS Code
    backend/README.md:38:## Docker Compose Override
    backend/README.md:40:During development, you can change Docker Compose settings that will only affect the local development environment in the file `docker-compose.override.yml`.
    backend/README.md:49:$ docker compose watch
    backend/README.md:57:$ docker compose watch
    backend/README.md:63:$ docker compose exec backend bash
    backend/README.md:92:## Backend tests
    backend/README.md:104:### Test running stack
    backend/README.md:109:docker compose exec backend bash scripts/tests-start.sh
    backend/README.md:112:That `/app/scripts/tests-start.sh` script just calls `pytest` after making sure that the rest of the stack is running. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.
    backend/README.md:117:docker compose exec backend bash scripts/tests-start.sh -x
    backend/README.md:120:### Test Coverage
    backend/README.md:124:## Migrations
    backend/README.md:133:$ docker compose exec backend bash
    backend/README.md:166:## Email Templates
    frontend/README.md:1:# FastAPI Project - Frontend
    frontend/README.md:5:## Frontend development
    frontend/README.md:19:# If using fnm
    frontend/README.md:22:# If using nvm
    frontend/README.md:29:# If using fnm
    frontend/README.md:32:# If using nvm
    frontend/README.md:54:### Removing the frontend
    frontend/README.md:60:* In the `docker-compose.yml` file, remove the whole service / section `frontend`.
    frontend/README.md:62:* In the `docker-compose.override.yml` file, remove the whole service / section `frontend` and `playwright`.
    frontend/README.md:75:## Generate Client
    frontend/README.md:77:### Automatically
    frontend/README.md:83:./scripts/generate-client.sh
    frontend/README.md:88:### Manually
    frontend/README.md:97:npm run generate-client
    frontend/README.md:104:## Using a Remote API
    frontend/README.md:114:## Code Structure
    frontend/README.md:126:## End-to-End Testing with Playwright
    frontend/README.md:131:docker compose up -d --wait backend
    frontend/README.md:137:npx playwright test
    frontend/README.md:143:npx playwright test --ui
    frontend/README.md:149:docker compose down -v
    frontend/README.md:154:For more information on writing and running Playwright tests, refer to the official [Playwright documentation](https://playwright.dev/docs/intro).
    development.md:5:# FastAPI Project - Development
    development.md:7:## Docker Compose
    development.md:12:docker compose watch
    development.md:32:docker compose logs
    development.md:38:docker compose logs backend
    development.md:41:## Local Development
    development.md:52:docker compose stop frontend
    development.md:65:docker compose stop backend
    development.md:75:## Docker Compose in `localhost.tiangolo.com`
    development.md:98:docker compose watch
    development.md:101:When deploying, for example in production, the main Traefik is configured outside of the Docker Compose files. For local development, there's an included Traefik in `docker-compose.override.yml`, just to let you test that the domains work as expected, for example with `api.localhost.tiangolo.com` and `dashboard.localhost.tiangolo.com`.
    development.md:103:## Docker Compose files and env vars
    development.md:105:There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.
    development.md:107:And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker compose` to apply overrides on top of `docker-compose.yml`.
    development.md:111:They also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.
    development.md:116:docker compose watch
    development.md:119:## The .env file
    development.md:125:One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.
    development.md:127:## Pre-commits and code linting
    development.md:135:#### Install pre-commit to run automatically
    development.md:158:#### Running pre-commit hooks manually
    development.md:173:## URLs
    development.md:177:### Development URLs
    development.md:195:### Development URLs with `localhost.tiangolo.com` Configured
       231                              --local context="${WORKSPACE}/frontend" \
       232                              --local dockerfile="${WORKSPACE}/frontend" \
       233                              --opt "build-arg:VITE_API_URL=${VITE_API_URL:-}" \
       234                              --output type=docker,dest=${WORKSPACE}/frontend-ci.tar \
       235                              --progress=plain
       236
       237                        '''
       238                    }
       239                }
       240            }
       241            stage('Archive checked images') {
       242                when { expression { env.SKIP_BUILD != 'true' && !env.CHANGE_ID } }
       243                steps {
       244                    archiveArtifacts artifacts: '*-ci.tar,source-sha.txt', fingerprint: true
       245                }
       246            }
       247
       248        }
       249
       250        post {
       251            success {
       252                script {
       253                    if (env.SKIP_BUILD != 'true' && !env.CHANGE_ID && env.BRANCH_NAME == 'main') {
       254                        build job: '/trusted/publish', wait: false, quietPeriod: 10,
       255                            parameters: [string(name: 'MODE', value: 'publish'),
       256                                         string(name: 'CI_JOB', value: env.JOB_NAME),
       257                                         string(name: 'CI_BUILD', value: env.BUILD_NUMBER)]
       258                    } else if (env.TAG_NAME) {
       259                        build job: '/trusted/publish', wait: false, quietPeriod: 10,
       260                            parameters: [string(name: 'MODE', value: 'release'),
       261                                         string(name: 'RELEASE_TAG', value: env.TAG_NAME)]
       262                    }
       263                }
       264            }
       265            always {
       266                // Tool containers create root-owned files; clean them in the same
       267                // container before the inbound agent removes the workspace.
       268                container('python-tester') {
       269                    sh '''
       270                        set -eu
       271                        test -n "${WORKSPACE}"
       272                        test "${WORKSPACE}" != /
       273                        cd "${WORKSPACE}"
       274                        find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
       275                    '''
       276                }
       277                deleteDir()
       278            }
       279        }
       280    }
        71            }
        72            stage('Verify successful CI and copy artifacts') {
        73                when { expression { params.MODE != 'release' } }
        74                steps {
        75                    script {
        76                        def jobPath = params.CI_JOB.split('/').collect { 'job/' + java.net.URLEncoder.encode(it, 'UTF-8') }.join('/')
        77                        def data
        78                        timeout(time: 10, unit: 'MINUTES') {
        79                            waitUntil(initialRecurrencePeriod: 5000) {
        80                                def response = httpRequest authentication: 'ci-read', quiet: true,
        81                                    url: "${env.JENKINS_API_URL}${jobPath}/${params.CI_BUILD}/api/json?tree=result,building,actions[lastBuiltRevision[SHA1],remoteUrls]"
        82                                data = readJSON text: response.content, returnPojo: true
        83                                return !data.building
        84                            }
        85                        }
        86                        if (data.result != 'SUCCESS') { error('Source CI build must be SUCCESS') }
        87                        def revisions = data.actions.findAll { it.lastBuiltRevision }.collect { it.lastBuiltRevision.SHA1 }.unique()
        88                        if (revisions.size() != 1 || !(revisions[0] ==~ /[0-9a-f]{40}/)) { error('Ambiguous or missing Git plugin revision') }
        89                        env.IMAGE_SHA = revisions[0]
        90                        copyArtifacts projectName: params.CI_JOB, selector: specific(params.CI_BUILD),
        91                            filter: '*-ci.tar,source-sha.txt', target: 'artifacts', fingerprintArtifacts: true
        92                        if (readFile('artifacts/source-sha.txt').trim() != env.IMAGE_SHA) { error('Artifact SHA disagrees with Jenkins SCM revision') }
        93                    }
        94                }
        95            }
        96            stage('Explicit promotion approval') {
        97                when { expression { params.MODE in ['dev', 'release'] } }
        98                steps {
        99                    input message: "Approve ${params.MODE}: ${params.MODE == 'release' ? params.RELEASE_TAG : env.IMAGE_SHA}. For a release, confirm this tag's digest pair ran successfully in stage (Argo health and smoke tests). Production still requires a reviewed Git PR.", submitter: 'admin'
       100                }
       101            }
       102            stage('Publish or promote under global lock') {
       103                steps {
       104                    lock(resource: 'fastapi-ghcr-gitops') {
       105                        container('publisher') {
       106                            withCredentials([
       107                                usernamePassword(credentialsId: 'ghcr-write', usernameVariable: 'GHCR_USER', passwordVariable: 'GHCR_TOKEN'),
       108                                usernamePassword(credentialsId: 'gitops-app', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')
       109                            ]) {
       110                                withEnv(["PROMOTION_MODE=${params.MODE}", "SOURCE_JOB=${params.CI_JOB}", "RELEASE_TAG=${params.RELEASE_TAG}"]) {
       111                                    sh 'sh ci/publish.sh'
       112                                }
       113                            }
       114                        }
       115                    }
       116                }
       117            }
       118        }
       119        post {
       120            always {
       121                container('publisher') { sh 'find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +' }
       122                deleteDir()
       123            }
       124        }
       125    }
        13    print('CoreDNS service discovery:', bool(socket.getaddrinfo('db',5432)))
        14    def check(url,expected,host=None):
        15        req=urllib.request.Request(url,headers={'Host':host} if host else {})
        16        try:
        17            with urllib.request.urlopen(req,timeout=15) as response: status=response.status
        18        except urllib.error.HTTPError as error: status=error.code
        19        print(url,'Host='+host if host else '',status)
        20        assert status==expected,(url,status,expected)
        21    for path,status in [('/',404),('/api/v1/utils/health-check/',200),('/api/v1/openapi.json',200),('/docs',200),('/metrics',404)]:
        22        check('http://backend'+path,status)
        23    check('http://frontend/',200)
        24    check('http://adminer/',200)
        25    for path in ['/', '/api/v1/utils/health-check/', '/api/v1/openapi.json']:
        26        check('http://traefik.traefik.svc.cluster.local'+path,200,HOST)
        27    if HOST.startswith('dev.'):
        28        check('http://traefik.traefik.svc.cluster.local/docs',200,HOST)
        29    '''.replace('HOST',repr(phase+'.example.com'))
        30    subprocess.run(['kubectl','--context','kind-fastapi-dev','exec','-i','-n','app-'+phase,'deployment/backend','--','python','-'],input=code.encode(),check=True)
    ✓ • 1.00s

## Assistant

Die Backend-Prüfungen sind erfolgreich: 55 Tests, Migrationen, mypy und Ruff. Auch alle drei aktiven Kubernetes-Overlays bestehen Schemaprüfung und Client-Dry-Run; 16 Prometheus-Ziele sind UP und die acht Alert-Regeln bestehen ihre Tests.

Der aktuelle Security-Scan meldet dagegen 62 npm-Schwachstellen, darunter drei kritische. Die Frontend-Prüfung zeigt außerdem Lintfehler und eine E2E-Voraussetzung, die im eingecheckten Client fehlt. Ich prüfe noch, ob der dokumentierte Generierungsschritt diese Voraussetzung zuverlässig herstellt.

## Activity

    $ python3 -u - <<'PY'
        import subprocess,re,pathlib
        pattern=re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}')
        p=subprocess.Popen(['git','log','--all','--format=COMMIT:%H','--patch','--no-ext-diff'],stdout=subprocess.PIPE,text=True,errors='replace');path='';commit='';hits=0;changed=set()
        for line in p.stdout:
         if line.startswith('COMMIT:'):commit=line.strip()[7:]
         if line.startswith('+++ b/'):path=line.strip()[6:]
         if not line.startswith('+') or line.startswith('+++'):continue
         if pattern.search(line):print('HISTORY_PATTERN_HIT',commit[:12],path,'<masked>');hits+=1
         if path=='.env' and re.match(r'\+(SECRET_KEY|FIRST_SUPERUSER_PASSWORD|POSTGRES_PASSWORD)=',line):
          k,v=line[1:].strip().split('=',1)
          if v and v.strip('"\'')!='changethis':changed.add((commit[:12],k))
        print('HISTORY_PATTERN_SCAN_EXIT',p.wait(),'HITS',hits,'ENV_NONPLACEHOLDER_ADDITIONS',len(changed))
        for c,k in sorted(changed):print('HISTORY_ENV_CHECK',c,k,'<masked>')
        PY
        kubectl --context kind-fastapi-dev --request-timeout=10s get namespaces -L pod-security.kubernetes.io/enforce; git check-ignore --no-index .terraform/a terraform.tfstate terraform.tfvars; docker run --rm --network none --entrypoint docker -v /home/root-admin/fastapi-traefik-datascientest-project:/work:ro -w /work docker:29.1.3-dind compose config --quiet
    HISTORY_PATTERN_SCAN_EXIT 0 HITS 0 ENV_NONPLACEHOLDER_ADDITIONS 0
    NAME                 STATUS   AGE     ENFORCE
    app-dev              Active   2d18h
    app-stage            Active   2d18h
    argocd               Active   2d18h
    default              Active   2d18h
    kube-node-lease      Active   2d18h
    kube-public          Active   2d18h
    kube-system          Active   2d18h
    local-path-storage   Active   2d18h
    monitoring           Active   2d18h
    traefik              Active   2d18h
    time="2026-10-12T07:41:17Z" level=warning msg="The \"CI\" variable is not set. Defaulting to a blank string."
    ✓ • 11.56s

## Activity

    $ python3 - <<'PY'
        from pathlib import Path
        import ast,subprocess,json
        files=subprocess.check_output(['git','ls-files','-co','--exclude-standard'],text=True).splitlines(); py=[];bad=[]
        for f in dict.fromkeys(files):
         p=Path(f)
         if p.is_file() and p.suffix=='.py':
          try:ast.parse(p.read_text());py.append(f)
          except Exception as e:bad.append((f,str(e)))
        print('PYTHON_AST',len(py),'errors',bad)
        p=sorted(Path('/tmp').glob('frontend-audit-*'),key=lambda p:p.stat().st_mtime)[-1]/'npm-audit.json';d=json.loads(p.read_text())
        print('AUDIT_LOCK_COUNTS',d['metadata']['vulnerabilities'])
        for key in ['form-data','handlebars','tar','axios']:
         v=d['vulnerabilities'].get(key,{})
         print('PACKAGE',key,'severity',v.get('severity'),'range',v.get('range'),'fix',v.get('fixAvailable'))
         for a in v.get('via',[]):
          if isinstance(a,dict): print('ADVISORY',a.get('title'),a.get('url'),a.get('range'))
        print('Source files checked; project outputs remain under /tmp.')
        PY
        nl -ba scripts/bootstrap-jenkins-host.py | sed -n '115,160p'; nl -ba frontend/package.json | head -54; nl -ba .github/dependabot.yml; nl -ba .github/workflows/test-docker-compose.yml | tail -12; cat backend/scripts/tests-start.sh; git status --short
    PYTHON_AST 63 errors []
    AUDIT_LOCK_COUNTS {'info': 0, 'low': 0, 'moderate': 4, 'high': 55, 'critical': 3, 'total': 62}
    PACKAGE form-data severity critical range 4.0.0 - 4.0.5 fix {'name': 'form-data', 'version': '4.0.6', 'isSemVerMajor': False}
    ADVISORY form-data uses unsafe random function in form-data for choosing boundary https://github.com/advisories/GHSA-fjxv-7rqg-78g4 >=4.0.0 <4.0.4
    ADVISORY form-data: CRLF injection in form-data via unescaped multipart field names and filenames https://github.com/advisories/GHSA-hmw2-7cc7-3qxx >=4.0.0 <4.0.6
    PACKAGE handlebars severity critical range 4.0.0 - 4.7.9 fix {'name': '@hey-api/openapi-ts', 'version': '0.99.0', 'isSemVerMajor': True}
    ADVISORY Handlebars.js has JavaScript Injection via AST Type Confusion by tampering @partial-block https://github.com/advisories/GHSA-3mfm-83xf-c92r >=4.0.0 <=4.7.8
    ADVISORY Handlebars.js has JavaScript Injection via AST Type Confusion https://github.com/advisories/GHSA-2w6w-674q-4c4q >=4.0.0 <=4.7.8
    ADVISORY Handlebars.js has Prototype Pollution Leading to XSS through Partial Template Injection https://github.com/advisories/GHSA-2qvq-rjwj-gvw9 >=4.0.0 <4.7.9
    ADVISORY Handlebars.js has a Prototype Method Access Control Gap via Missing __lookupSetter__ Blocklist Entry https://github.com/advisories/GHSA-7rx3-28cr-v5wh >=4.6.0 <=4.7.8
    ADVISORY Handlebars.js has a Property Access Validation Bypass in container.lookup https://github.com/advisories/GHSA-442j-39wm-28r2 >=4.0.0 <=4.7.8
    ADVISORY Handlebars.js has JavaScript Injection via AST Type Confusion when passing an object as dynamic partial https://github.com/advisories/GHSA-xhpv-hc6g-r9c6 >=4.0.0 <=4.7.8
    ADVISORY Handlebars.js has Denial of Service via Malformed Decorator Syntax in Template Compilation https://github.com/advisories/GHSA-9cx6-37pm-9jff >=4.0.0 <=4.7.8
    ADVISORY Handlebars.js has JavaScript Injection in CLI Precompiler via Unescaped Names and Options https://github.com/advisories/GHSA-xjpj-3mr7-gcpf >=4.0.0 <=4.7.8
    ADVISORY Handlebars: JavaScript Injection via Unsafe Inline Embedding of Precompiled Templates https://github.com/advisories/GHSA-xw65-4hp5-5hc7 >=4.0.0 <=4.7.9
    ADVISORY Handlebars: JavaScript Injection via AST Type Confusion in compile (bypass of CVE-2026-33937) https://github.com/advisories/GHSA-8r5x-fm3f-whwj >=4.0.0 <=4.7.9
    ADVISORY Handlebars: JavaScript Injection via Own Property Check Bypass https://github.com/advisories/GHSA-p8wg-vrv2-v86f >=4.0.0 <=4.7.9
    PACKAGE tar severity critical range <=7.5.20 fix {'name': '@hey-api/openapi-ts', 'version': '0.99.0', 'isSemVerMajor': True}
    ADVISORY node-tar Vulnerable to Arbitrary File Creation/Overwrite via Hardlink Path Traversal https://github.com/advisories/GHSA-34x7-hfp2-rc4v <7.5.7
    ADVISORY node-tar is Vulnerable to Arbitrary File Overwrite and Symlink Poisoning via Insufficient Path Sanitization https://github.com/advisories/GHSA-8qq5-rm4j-mr97 <=7.5.2
    ADVISORY Arbitrary File Read/Write via Hardlink Target Escape Through Symlink Chain in node-tar Extraction https://github.com/advisories/GHSA-83g3-92jg-28cx <7.5.8
    ADVISORY tar has Hardlink Path Traversal via Drive-Relative Linkpath https://github.com/advisories/GHSA-qffp-2rhf-9h96 <=7.5.9
    ADVISORY node-tar Symlink Path Traversal via Drive-Relative Linkpath https://github.com/advisories/GHSA-9ppj-qmqm-q256 <=7.5.10
    ADVISORY Race Condition in node-tar Path Reservations via Unicode Ligature Collisions on macOS APFS https://github.com/advisories/GHSA-r6q2-hw4h-h46w <=7.5.3
    ADVISORY node-tar applies PAX size override to intermediary GNU long-name/long-link headers, causing tar parser interpretation differential (file smuggling) https://github.com/advisories/GHSA-vmf3-w455-68vh <=7.5.15
    ADVISORY node-tar: Process crash via PAX numeric path type confusion https://github.com/advisories/GHSA-w8wr-v893-vjvp <=7.5.17
    ADVISORY node-tar: Decompression/parse DoS via unlimited input https://github.com/advisories/GHSA-23hp-3jrh-7fpw <=7.5.18
    ADVISORY node-tar: Negative tar entry size causes infinite loop in archive replace https://github.com/advisories/GHSA-8x88-c5mf-7j5w <=7.5.17
    ADVISORY node-tar: Uncaught Exception DoS via NUL byte in PAX path/linkpath records https://github.com/advisories/GHSA-gvwx-54wh-qm9j <=7.5.16
    ADVISORY node-tar: Uncontrolled recursion in mapHas/filesFilter allows uncatchable stack-overflow DoS via crafted long-path tar with member selection https://github.com/advisories/GHSA-r292-9mhp-454m <=7.5.20
    PACKAGE axios severity high range 1.0.0 - 1.19.0 fix {'name': 'axios', 'version': '1.20.0', 'isSemVerMajor': False}
    ADVISORY axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL https://github.com/advisories/GHSA-jr5f-v2jv-69x6 >=1.0.0 <1.8.2
    ADVISORY Axios is vulnerable to DoS attack through lack of data size check https://github.com/advisories/GHSA-4hjh-wcwx-xvwj >=1.0.0 <1.12.0
    ADVISORY Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF https://github.com/advisories/GHSA-3p68-rc4w-qgx5 >=1.0.0 <1.15.0
    ADVISORY Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy https://github.com/advisories/GHSA-w9j2-pvgh-6h63 >=1.0.0 <1.15.1
    ADVISORY Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0 https://github.com/advisories/GHSA-pmwg-cvhr-8vh7 >=1.0.0 <1.15.1
    ADVISORY Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver` https://github.com/advisories/GHSA-3w6x-2g7m-8v23 >=1.0.0 <1.15.2
    ADVISORY Axios: Null Byte Injection via Reverse-Encoding in AxiosURLSearchParams https://github.com/advisories/GHSA-xhjh-pmcv-23jw >=1.0.0 <1.15.1
    ADVISORY Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream https://github.com/advisories/GHSA-445q-vr5w-6q77 >=1.0.0 <1.15.1
    ADVISORY Axios: no_proxy bypass via IP alias allows SSRF https://github.com/advisories/GHSA-m7pr-hjqh-92cm >=1.0.0 <1.15.1
    ADVISORY Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0 https://github.com/advisories/GHSA-5c9x-8gcm-mpgx >=1.0.0 <1.15.1
    ADVISORY Axios: HTTP adapter streamed responses bypass maxContentLength https://github.com/advisories/GHSA-vf2m-468p-8v99 >=1.0.0 <1.15.1
    ADVISORY Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking https://github.com/advisories/GHSA-pf86-5x62-jrwf >=1.0.0 <1.15.1
    ADVISORY Axios: Header Injection via Prototype Pollution https://github.com/advisories/GHSA-6chq-wfr3-2hj9 >=1.0.0 <1.15.1
    ADVISORY Axios: XSRF Token Cross-Origin Leakage via Prototype Pollution Gadget in `withXSRFToken` Boolean Coercion https://github.com/advisories/GHSA-xx6v-rp6x-q39c >=1.0.0 <1.15.1
    ADVISORY Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig https://github.com/advisories/GHSA-43fc-jf86-j433 >=1.0.0 <=1.13.4
    ADVISORY Axios has prototype pollution read-side gadgets in HTTP adapter that allow credential injection and request hijacking https://github.com/advisories/GHSA-q8qp-cvcw-x6jj >=1.0.0 <1.15.2
    ADVISORY Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain https://github.com/advisories/GHSA-fvcv-3m26-pcqx >=1.0.0 <1.15.0
    ADVISORY Axios: unbounded recursion in toFormData causes DoS via deeply nested request data https://github.com/advisories/GHSA-62hf-57xw-28j9 >=1.0.0 <1.15.1
    ADVISORY Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection https://github.com/advisories/GHSA-hfxv-24rg-xrqf >=1.0.0 <1.16.0
    ADVISORY Allocation of Resources Without Limits or Throttling in Axios https://github.com/advisories/GHSA-777c-7fjr-54vf >=1.7.0 <1.16.0
    ADVISORY Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter https://github.com/advisories/GHSA-p92q-9vqr-4j8v >=1.0.0 <1.16.0
    ADVISORY Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection https://github.com/advisories/GHSA-j5f8-grm9-p9fc >=1.0.0 <1.16.0
    ADVISORY axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge https://github.com/advisories/GHSA-3g43-6gmg-66jw >=1.0.0 <1.15.2
    ADVISORY axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy` https://github.com/advisories/GHSA-35jp-ww65-95wh >=1.0.0 <1.16.0
    ADVISORY axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions https://github.com/advisories/GHSA-898c-q2cr-xwhg >=1.0.0 <1.16.0
    ADVISORY Axios: Prototype pollution gadgets can alter axios request construction https://github.com/advisories/GHSA-mmx7-hfxf-jppx >=1.0.0 <1.18.0
    ADVISORY Axios: Deep formToJSON Key Recursion Can Cause Denial of Service https://github.com/advisories/GHSA-pmv8-rq9r-6j72 >=1.0.0 <1.18.0
    ADVISORY Axios: Nested axios option objects can consume polluted prototype values https://github.com/advisories/GHSA-7q8q-rj6j-mhjq >=1.0.0 <1.18.0
    ADVISORY Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength` https://github.com/advisories/GHSA-jqh4-m9w3-8hp9 >=1.7.0 <1.18.0
    ADVISORY Axios: Excessive recursion in formDataToJSON can cause denial of service https://github.com/advisories/GHSA-42h9-826w-cgv3 >=1.0.0 <1.18.0
    ADVISORY Axios: Prototype pollution gadget in fetch adapter can alter outbound requests https://github.com/advisories/GHSA-vh66-26gq-q6x8 >=1.7.0 <1.20.0
    ADVISORY Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method https://github.com/advisories/GHSA-9fr6-4gfg-395g >=1.0.0 <1.20.0
    ADVISORY Axios: Header Injection via Inherited headers After Minimal Interceptor https://github.com/advisories/GHSA-j8rh-479h-cp32 >=1.0.0 <1.20.0
    Source files checked; project outputs remain under /tmp.
       115        if not exists('container','host-jenkins-docker'):
       116            run('docker','run','-d','--name','host-jenkins-docker','--network','host-jenkins-build','--network-alias','docker',
       117                '--restart','unless-stopped','--privileged','--cgroupns=private','--memory=1536m','--memory-swap=1536m','--cpus=1.25',
       118                '-e','DOCKER_TLS_CERTDIR=/certs','-v','host-jenkins-docker:/var/lib/docker',
       119                '-v','host-jenkins-client-certs:/certs/client','-v','host-jenkins-server-certs:/certs/server',
       120                '-v','host-jenkins-work:/home/jenkins/agent','-v',str(CONFIG)+':/opt/host-ci:ro',daemon)
       121        else:run('docker','start','host-jenkins-docker')
       122        if not exists('container','host-jenkins-agent'):
       123            run('docker','create','--name','host-jenkins-agent','--network','host-jenkins-management','--restart','unless-stopped',
       124                '--memory=256m','--memory-swap=256m','--cpus=0.25','-e','DOCKER_HOST=tcp://docker:2376',
       125                '-e','DOCKER_TLS_VERIFY=1','-e','DOCKER_CERT_PATH=/certs/client',
       126                '-v','host-jenkins-client-certs:/certs/client:ro','-v','host-jenkins-work:/home/jenkins/agent',
       127                '-v',str(agent_file)+':/run/secrets/agent-secret:ro','-v',str(cli)+':/usr/local/bin/docker:ro','-v',str(buildx)+':/usr/local/libexec/docker/cli-plugins/docker-buildx:ro',
       128                '-v',str(CONFIG)+':/opt/host-ci:ro','--entrypoint','bash',jenkins,'-ec',
       129                'curl --fail --retry 30 --retry-delay 2 http://jenkins:8080/jnlpJars/agent.jar -o /tmp/agent.jar; exec java -Xms32m -Xmx128m -jar /tmp/agent.jar -url http://jenkins:8080/ -name host-ci -secret @/run/secrets/agent-secret -webSocket -workDir /home/jenkins/agent')
       130            run('docker','network','connect','host-jenkins-build','host-jenkins-agent')
       131        run('docker','start','host-jenkins-agent')
       132        for _ in range(60):
       133            node=json.loads(api('/computer/host-ci/api/json?tree=offline,numExecutors'))
       134            if not node['offline']:break
       135            time.sleep(2)
       136        else:raise SystemExit('Agent not online; no builds started.')
       137        print('Jenkins online at http://127.0.0.1:8085/; admin password stored privately, not printed. One executor; publisher disabled.')
       138
       139    if __name__=='__main__':
       140        up()
         1    {
         2      "name": "frontend",
         3      "private": true,
         4      "version": "0.0.0",
         5      "type": "module",
         6      "scripts": {
         7        "dev": "vite",
         8        "build": "tsc -p tsconfig.build.json && vite build",
         9        "lint": "biome check --apply-unsafe --no-errors-on-unmatched --files-ignore-unknown=true ./",
        10        "preview": "vite preview",
        11        "generate-client": "openapi-ts"
        12      },
        13      "dependencies": {
        14        "@chakra-ui/react": "^3.8.0",
        15        "@emotion/react": "^11.14.0",
        16        "@tanstack/react-query": "^5.28.14",
        17        "@tanstack/react-query-devtools": "^5.28.14",
        18        "@tanstack/react-router": "1.19.1",
        19        "axios": "1.7.4",
        20        "form-data": "4.0.0",
        21        "next-themes": "^0.4.4",
        22        "react": "^18.2.0",
        23        "react-dom": "^18.2.0",
        24        "react-error-boundary": "^4.0.13",
        25        "react-hook-form": "7.49.3",
        26        "react-icons": "^5.4.0"
        27      },
        28      "devDependencies": {
        29        "@biomejs/biome": "1.6.1",
        30        "@hey-api/openapi-ts": "^0.57.0",
        31        "@playwright/test": "^1.45.2",
        32        "@tanstack/router-devtools": "1.19.1",
        33        "@tanstack/router-vite-plugin": "1.19.0",
        34        "@types/node": "^20.10.5",
        35        "@types/react": "^18.2.37",
        36        "@types/react-dom": "^18.2.15",
        37        "@vitejs/plugin-react-swc": "^3.5.0",
        38        "dotenv": "^16.4.5",
        39        "typescript": "^5.2.2",
        40        "vite": "^5.4.14"
        41      }
        42    }
         1    version: 2
         2    updates:
         3      # GitHub Actions
         4      - package-ecosystem: github-actions
         5        directory: /
         6        schedule:
         7          interval: daily
         8        commit-message:
         9          prefix: ⬆
        10      # Python
        11      - package-ecosystem: pip
        12        directory: /
        13        schedule:
        14          interval: daily
        15        commit-message:
        16          prefix: ⬆
        17      # npm
        18      - package-ecosystem: npm
        19        directory: /
        20        schedule:
        21          interval: daily
        22        commit-message:
        23          prefix: ⬆
        24      # Docker
        25      - package-ecosystem: docker
        26        directory: /
        27        schedule:
        28          interval: weekly
        29        commit-message:
        30          prefix: ⬆
        15        runs-on: ubuntu-latest
        16        steps:
        17          - name: Checkout
        18            uses: actions/checkout@v4
        19          - run: docker compose build
        20          - run: docker compose down -v --remove-orphans
        21          - run: docker compose up -d --wait backend frontend adminer
        22          - name: Test backend is up
        23            run: curl http://localhost:8000/api/v1/utils/health-check
        24          - name: Test frontend is up
        25            run: curl http://localhost:5173
        26          - run: docker compose down -v --remove-orphans
    #! /usr/bin/env bash
    set -e
    set -x

    python app/tests_pre_start.py

    bash scripts/test.sh "$@"
     M .gitignore
     M DEV_SETUP_REPORT.md
    ?? ALERTING_RUNBOOK.md
    ?? GRAFANA_DASHBOARDS.md
    ?? JENKINS_RECOVERY_REPORT.md
    ?? KIND_MIGRATION_REPORT.md
    ?? MIGRATION_BACKUP_CHECKLIST.md
    ?? MONITORING_SETUP_REPORT.md
    ?? PROMETHEUS_QUERIES.md
    ?? argocd/app-monitoring.yaml
    ?? argocd/app-stage.yaml
    ?? argocd/bootstrap/monitoring-namespace.yaml
    ?? argocd/project-monitoring.yaml
    ?? infra/
    ?? monitoring/
    ?? scripts/bootstrap-jenkins-host.py
    ?? scripts/bootstrap-kind.sh
    ?? scripts/capture-kind-capacity.py
    ?? scripts/check-kind-capacity.py
    ?? scripts/create-stage-secrets.py
    ?? scripts/recover-dev-secrets.py
    ?? scripts/restore-kind-registry-auth.py
    ?? scripts/sync-jenkins-host-jobs.py
    ?? scripts/verify-jenkins-host.py
    ?? scripts/verify-kind-app.py
    ?? scripts/verify-kind-monitoring.py
    ?? scripts/watch-kind-monitoring.py
    ✓ • 403ms

## Activity

    $ python3 -u - <<'PY'
        import pathlib,subprocess,os,json,secrets
        root=pathlib.Path.cwd();tmp=sorted(pathlib.Path('/tmp').glob('frontend-audit-*'),key=lambda p:p.stat().st_mtime)[-1];frontend=tmp/'frontend'
        env={'ENVIRONMENT':'local','PROJECT_NAME':'Audit','POSTGRES_SERVER':'unused','POSTGRES_USER':'postgres','FIRST_SUPERUSER':'audit@example.com','FIRST_SUPERUSER_PASSWORD':'audit-test-only','SECRET_KEY':secrets.token_urlsafe(32),'POSTGRES_PASSWORD':'audit-test-only'}
        cmd=['docker','run','--rm','--network','none']
        for k,v in env.items():cmd+=['-e',k+'='+v]
        r=subprocess.run(cmd+['fastapi-repo-audit/backend:20261012','python','-c','import json; from app.main import app; print(json.dumps(app.openapi()))'],capture_output=True,text=True,timeout=30)
        print('LOCAL_OPENAPI',r.returncode);(frontend/'openapi.json').write_text(r.stdout)
        cmd=['docker','run','--rm','--memory=768m','-e','FIRST_SUPERUSER=audit@example.com','-e','FIRST_SUPERUSER_PASSWORD=audit-test-only','-e','VITE_API_URL=http://backend:8000','-v',str(frontend)+':/app','-v',str(root/'frontend/node_modules')+':/app/node_modules:ro','-w','/app','node:20.18.1']
        for step in [['npm','run','generate-client'],['npx','--no-install','playwright','test','--list']]:
         r=subprocess.run(cmd+step,capture_output=True,text=True,timeout=90);print('AFTER_REGEN',step,r.returncode,(r.stdout+r.stderr)[-1200:],flush=True)
         (tmp/('generate-check.log' if step[0]=='npm' else 'playwright-regenerated-list.log')).write_text(r.stdout+r.stderr)
        PY
    LOCAL_OPENAPI 0
    AFTER_REGEN ['npm', 'run', 'generate-client'] 0
    > frontend@0.0.0 generate-client
    > openapi-ts

    ✨ Creating Axios client
    ✨ Done! Your client is located in: /app/src/client
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice

    AFTER_REGEN ['npx', '--no-install', 'playwright', 'test', '--list'] 0 ser-settings.spec.ts:94:3 › Edit user with invalid data › Cancel edit action restores original name
      [chromium] › user-settings.spec.ts:116:3 › Edit user with invalid data › Cancel edit action restores original email
      [chromium] › user-settings.spec.ts:142:3 › Change password successfully › Update password successfully
      [chromium] › user-settings.spec.ts:170:3 › Change password with invalid data › Update password with weak passwords
      [chromium] › user-settings.spec.ts:190:3 › Change password with invalid data › New password and confirmation password do not match
      [chromium] › user-settings.spec.ts:212:3 › Change password with invalid data › Current password and new password are the same
      [chromium] › user-settings.spec.ts:235:1 › Appearance tab is visible
      [chromium] › user-settings.spec.ts:241:1 › User can switch from light mode to dark mode and vice versa
      [chromium] › user-settings.spec.ts:289:1 › Selected mode is preserved across sessions
    Total: 41 tests in 5 files
    npm notice
    npm notice New major version of npm available! 10.8.2 -> 12.2.0
    npm notice Changelog: https://github.com/npm/cli/releases/tag/v12.2.0
    npm notice To update run: npm install -g npm@12.2.0
    npm notice

    ✓ • 34.80s

## Activity

    $ PYTHONDONTWRITEBYTECODE=1 python3 -B monitoring/verify-grafana-auth.py
    deployment "monitoring-grafana" successfully rolled out
    Anonymous APIs: 401; dashboard redirects to /login; login form enabled.
    Authenticated dashboard platform-nodes 8 queries returned data; panels preserved.
    Authenticated dashboard dev-stage-workloads 16 queries returned data; panels preserved.
    Authenticated dashboard gitops-argocd 6 queries returned data; panels preserved.
    Authenticated dashboard ingress-traefik 7 queries returned data; panels preserved.
    PASS: normal login session, Prometheus datasource, four dashboards; ClusterIP, no ingress.
    ✓ • 10.92s

## Assistant

Die abschließenden Prüfungen bestätigen vier funktionierende Grafana-Dashboards mit geschütztem Zugriff. Nach der lokalen OpenAPI-Client-Generierung lassen sich auch die 41 Playwright-Tests auflisten; einen vollständigen Browser-Testlauf habe ich nicht durchgeführt.

Ich habe keine Projektdateien geändert. Der Bericht unterscheidet nun geprüfte Funktion, vorhandene Konfiguration, fehlende Umsetzung und nicht nachgewiesene externe Einstellungen wie GitHub-Branch-Schutz.

## Assistant

**Dein Projekt erfüllt die Anforderungen derzeit nur teilweise.** Die Anwendung, Docker-Builds, Kubernetes-Grundressourcen, Backend-Tests und das lokale Monitoring funktionieren. Die größten Abgabelücken sind **fehlendes Terraform, deaktiviertes CI/CD, eine noch nicht betriebsfähige Prod-Umgebung, fehlendes automatisches Dev-Deployment und fehlende Datenbank-Backups**.

**Project readiness: 53 / 100**

Diese Bewertung bezieht sich auf deine vollständige Anforderungsliste, einschließlich tatsächlich ausführbarer Bereitstellung und Recovery.

## 1. Prüfgrundlage

Ich habe die vorhandenen Implementierungen untersucht: Dockerfiles, Compose, beide Kubernetes-Verzeichnisbäume, Argo CD, Jenkins, GitHub Actions, Anwendungscode, Tests, Monitoring, Skripte und Dokumentation.

Dabei habe ich unterschieden zwischen:

- **Versioniertem Repository:** 274 getrackte Dateien.
- **Zusätzlichen lokalen Dateien:** insbesondere `infra/`, `monitoring/` und neue Betriebsberichte.
- **Tatsächlichem Betrieb:** vorhandener Docker-/kind-Cluster und lokale Jenkins-Installation.

Generierte Verzeichnisse wurden nicht als Implementierungsnachweis gewertet. Bereits installierte Abhängigkeiten wurden für Prüfungen verwendet.

**Keine Projektdateien wurden geändert.** Bestehende lokale Änderungen blieben erhalten. Prüfdateien entstanden unter `/tmp`; zusätzlich wurden zwei lokale Docker-Prüfimages gebaut. Es gab keine Registry-Pushes, Deployments, Terraform-Änderungen oder Eingriffe in bestehende Anwendungsdatenbanken.

## 2. Tatsächlich ausgeführte Validierungen

| Prüfung | Ergebnis |
|---|---|
| Backend-Docker-Build | **PASS** |
| Frontend-Docker-Build | **PASS**, vorhandener Build-Cache wurde genutzt |
| Backend mypy | **PASS**, 38 geprüfte Quelldateien |
| Backend Ruff / Formatprüfung | **PASS** |
| Alembic-Migrationen auf neuer Testdatenbank | **PASS** |
| Backend Pytest | **PASS**, 55 Tests, zwei SQLAlchemy-Warnungen |
| CI-Publisher-/Promotion-Tests | **PASS**, 12 Tests |
| Kustomize: aktive Dev-/Stage-/Prod-Overlays | **PASS** |
| kubeconform, Kubernetes-1.31-Schemas | **PASS**, 39 Ressourcen, keine übersprungen |
| Kubernetes Client-Dry-Run | **PASS**, alle drei aktiven Overlays |
| Legacy-Kustomize-Overlays | Dev und Prod rendern erfolgreich |
| YAML-Parsing | **PASS**, 87 Dateien |
| Python-Syntaxprüfung | **PASS**, 63 Dateien |
| Shell-Syntaxprüfung | **PASS**, 16 Skripte |
| Separater Frontend-TypeScript-/Vite-Build | **PASS** mit ausreichendem Speicher |
| Frontend-Linter ohne Auto-Fixes | **FAIL**, 22 Fehler |
| Playwright-Testauflistung mit eingechecktem Client | **FAIL**, fehlender `PrivateService` |
| Playwright-Testauflistung nach lokaler Client-Generierung | **PASS**, 41 Tests in fünf Dateien |
| Vollständiger Playwright-Browserlauf | **Nicht durchgeführt** |
| Compose-Konfigurationsprüfung | **PASS** über vorhandenes Docker-CLI-Image |
| npm Security Audit | **FAIL**, 62 Findings: 3 critical, 55 high, 4 moderate |
| Prometheus | **PASS**, 16 von 16 Scrape-Zielen UP |
| Alert-Regeln | **PASS**, acht Regeln einschließlich synthetischer Tests |
| Grafana | **PASS**, vier Dashboards und 37 erfolgreiche Dashboard-Abfragen |
| Grafana-Zugriffsschutz | **PASS**, anonyme APIs verweigert, Anmeldung funktioniert |
| Terraform-Prüfungen | **Nicht möglich:** keine Terraform-Dateien, kein Terraform-Binary |

**Wichtig:** Ein erfolgreicher Client-Dry-Run prüft keine Image-Verfügbarkeit, fehlenden Secrets, tatsächlichen Namespace-Aufbau oder erfolgreiche Produktionseinführung.

Die Backend-Tests liefen ausschließlich gegen eine neue, isolierte Wegwerf-Datenbank. Das war notwendig, weil die vorhandene Test-Fixture Tabelleninhalte löscht.

## 3. Docker — PARTIAL

**Vollständig vorhanden und geprüft:**

- Funktionierende Backend- und Frontend-Dockerfiles.
- Lockfiles und Installation über `uv sync --frozen` beziehungsweise `npm ci`.
- Frontend mit sinnvollem Multi-Stage-Build.
- `.dockerignore` für beide Komponenten.
- Jenkins-Code für Image-Builds, Archivierung und GHCR-Publishing.
- Commit-SHA-Tags und digestgebundene Dev-/Stage-Deployments.

**Teilweise erfüllt oder problematisch:**

| Fundstelle | Befund | Auswirkung |
|---|---|---|
| [backend/Dockerfile:1](/home/root-admin/fastapi-traefik-datascientest-project/backend/Dockerfile:1) | Kein `USER`; Laufzeit verwendet standardmäßig root | Unnötig hohe Rechte |
| [frontend/Dockerfile:19](/home/root-admin/fastapi-traefik-datascientest-project/frontend/Dockerfile:19) | Standard-nginx ohne festgelegten Non-Root-Start | nginx-Master startet standardmäßig als root |
| [backend/Dockerfile:28](/home/root-admin/fastapi-traefik-datascientest-project/backend/Dockerfile:28) | Dev-Abhängigkeiten werden mitinstalliert | Tests, Linter und zusätzliche Pakete im Runtime-Image |
| [backend/Dockerfile:36](/home/root-admin/fastapi-traefik-datascientest-project/backend/Dockerfile:36) | Gesamtes `app/` einschließlich Tests wird kopiert | Unnötige Runtime-Dateien |
| [frontend/Dockerfile.playwright:1](/home/root-admin/fastapi-traefik-datascientest-project/frontend/Dockerfile.playwright:1) | `node:20`, `npm install`, unversionierter Playwright-Installationsaufruf | Testimage weniger reproduzierbar |
| [frontend/.dockerignore:1](/home/root-admin/fastapi-traefik-datascientest-project/frontend/.dockerignore:1) | Nur `node_modules` und `dist` ausgeschlossen | Tests, Reports und `.env` können in den Build-Kontext gelangen |

Die normalen Dockerfiles verwenden Versions-Tags, aber keine festgeschriebenen Basisimage-Digests. Damit sind sie **abhängigkeitsseitig weitgehend reproduzierbar**, aber nicht vollständig gegen Änderungen der Basisimages abgesichert.

**Secrets:** In den untersuchten Dockerfiles wurden keine echten Zugangsdaten gefunden. Die vorhandene Frontend-`.env` enthält öffentliche Konfiguration. Die aktuelle Backend-Kopie übernimmt die Repository-Root-`.env` nicht.

**Registry:** Publishing ist implementiert, im aktuellen lokalen Jenkins aber deaktiviert. SHA-Tags sind durch Publisher-Code gegen Überschreiben geschützt; das ist keine nachgewiesene Registry-Immutability-Einstellung.

## 4. Dev und Prod — PARTIAL

Die aktiven Umgebungen liegen unter `deploy/overlays/{dev,stage,prod}`.

| Merkmal | Dev | Stage | Prod |
|---|---|---|---|
| Namespace | `app-dev` | `app-stage` | `app-prod` konfiguriert, live nicht vorhanden |
| Anwendung live vorhanden | Ja | Ja | Nein |
| Backend-Konfiguration | `staging`, HTTP | `staging`, lokal HTTP-Override | `production`, HTTPS vorgesehen |
| Backend-/Frontend-Replikate | 1 / 1 | 1 / 1 | 2 / 2 vorgesehen |
| Image-Digests | Vorhanden | Vorhanden | Fehlen |
| Image-Tags | Echter SHA | Echter SHA | Null-SHA-Platzhalter |
| Neue Version automatisch promoviert | Nein, manuelle Freigabe | Im ursprünglichen Pipeline-Code vorgesehen | Freigabe und reviewed PR vorgesehen |

Dev nutzt `ENVIRONMENT=staging`, weil die Anwendung nur `local`, `staging` und `production` erlaubt. Das ist funktional nachvollziehbar und verhindert die lokalen Test-API-Routen.

**Die automatische Argo-Synchronisierung von Dev erfüllt allein nicht dein gefordertes automatisches Dev-Deployment:** Die Auswahl und Promotion eines neuen Dev-Artefakts erfordert derzeit einen manuellen Publisher-Aufruf und eine Freigabe.

**Prod ist ein vorbereiteter Overlay, keine fertig bereitgestellte Umgebung.** Beide Image-Tags sind Platzhalter in [deploy/overlays/prod/kustomization.yaml:9](/home/root-admin/fastapi-traefik-datascientest-project/deploy/overlays/prod/kustomization.yaml:9).

Terraform-Konfigurationen, tfvars und Terraform-State-Isolation fehlen vollständig.

Die Unterschiede sind im Jenkins-Betriebshandbuch beschrieben. Allerdings unterscheiden sich das ursprüngliche GitOps-Zielbild und der aktuelle lokale Wiederherstellungsbetrieb erheblich.

## 5. Tests — PARTIAL; Unit-Test-Pflicht erfüllt

**Tatsächliche Tests sind vorhanden und ausführbar:**

- Backend-API-Tests für Benutzer, Login und Items.
- Datenbank-/CRUD-Tests.
- Tests mit gemockten Verbindungen für Startskripte.
- Zwölf CI-Publisher-/Promotion-Tests.
- Playwright-E2E-Tests für Login, Registrierung, Passwort-Reset und Einstellungen.

Die Backend-Suite ist überwiegend eine Kombination aus API- und Datenbank-Integrationstests. Die isolierten Startskript- und CI-Tests erfüllen zusätzlich die Unit-Test-Anforderung.

**Pipeline-Verhalten:** Im ursprünglichen Jenkinsfile brechen fehlgeschlagene Tests die Pipeline ab. Der Publisher akzeptiert nur einen erfolgreichen Quellbuild. Das ist korrekt implementiert.

**Lücken:**

- Jenkins führt keine Playwright-E2E-Tests aus.
- Die ergänzenden GitHub-Testworkflows hören bei Push auf `master`, während GitOps und Jenkins `main` verwenden.
- Ein erfolgreicher Jenkins-Publisherlauf hängt nicht nachweislich vom Playwright-Ergebnis ab.
- Der eingecheckte Frontend-Client enthält keinen `PrivateService`. E2E-Tests benötigen zuerst die Client-Generierung mit `ENVIRONMENT=local`.
- Nach dieser Generierung wurden 41 Tests erfolgreich erkannt; ihre vollständige Browserausführung ist nicht nachgewiesen.
- Der Frontend-Linter meldet 22 Fehler, unter anderem in generiertem Client-Code. Jenkins führt diesen Linter nicht aus.

**Zusätzlicher Dokumentationsfehler:** [backend/README.md:112](/home/root-admin/fastapi-traefik-datascientest-project/backend/README.md:112) behauptet, zusätzliche Argumente würden an pytest weitergereicht. Tatsächlich nutzt `backend/scripts/test.sh` sie als Coverage-Titel; der pytest-Aufruf erhält sie nicht.

## 6. Kubernetes — PARTIAL

**Die Mindestanforderungen sind erfüllt:**

- Deployments.
- Services.
- ConfigMaps und Secret-Referenzen.
- Ingress.
- PVC.
- Namespace-Bootstrap für Dev.
- Backend-/Frontend-/Datenbank-Probes.
- Requests und Limits.
- Separate Umgebungs-Namespaces.
- Argo-Sync-Waves und Migration-Job.
- Deaktiviertes automatisches Mounten von ServiceAccount-Tokens.

Labels, Selektoren und Portzuordnungen sind im aktiven Manifestbaum konsistent:

| Komponente | Service-Port | Container-Port |
|---|---:|---:|
| Backend | 80 | 8000 |
| Frontend | 80 | 80 |
| PostgreSQL | 5432 | 5432 |
| Adminer | 80 | 8080 |

Backend und Frontend verwenden ohne explizite Strategie die Kubernetes-Standardstrategie `RollingUpdate`. PostgreSQL verwendet sinnvollerweise `Recreate`, um gleichzeitige Datenbankwriter zu vermeiden.

**Production-Readiness-Lücken:**

1. **Keine Security Contexts für die aktiven App-Workloads.**
   Es fehlen unter anderem `runAsNonRoot`, `allowPrivilegeEscalation: false`, Capability-Drops und ein Seccomp-Profil.

2. **Keine Pod-Security-Enforcement-Labels.**
   Das wurde auch an den vorhandenen Namespaces geprüft.

3. **Keine NetworkPolicies für App- oder CI-Namespaces.**
   Im Cluster existieren Argo-NetworkPolicies; daraus folgt keine Isolation der Anwendung oder des Buildsystems.

4. **Keine PodDisruptionBudgets oder Verteilungsvorgaben.**
   Zwei Prod-Replikate garantieren ohne Node-/Zonenverteilung keine Ausfallsicherheit.

5. **Single-Node-Cluster und lokaler Storage.**
   Der laufende Cluster hat einen Node. Die StorageClass verwendet `local-path`, `reclaimPolicy: Delete` und keine Volume-Erweiterung.

6. **Single-Instance-PostgreSQL ohne Backup oder HA.**
   Ein PVC schützt nicht vor Node-/Host-Verlust.

7. **Backend-Readiness prüft nur den Prozess.**
   [backend/app/api/routes/utils.py:34](/home/root-admin/fastapi-traefik-datascientest-project/backend/app/api/routes/utils.py:34) liefert unabhängig vom Datenbankzustand `True`. Liveness ist damit brauchbar; Readiness erkennt Datenbankausfälle nicht.

8. **Adminer hat keine Probes und bleibt auch im Prod-Overlay enthalten.**

9. **TLS ist in Stage/Prod referenziert, aber nicht vollständig provisioniert.**
   Der lokale Stage-Bootstrap entfernt TLS ausdrücklich. Ein produktiver Zertifikatsprozess ist nicht implementiert.

**Ingress-/Dokumentationsbefund:** Dev `/docs` liefert 200; Stage `/docs` liefert 404. Stage routet `/docs` nicht zum Backend. Ein HTTP-200 bei `/metrics` am öffentlichen Host stammt vom Frontend-SPA-Fallback und ist **kein Nachweis für Prometheus-Anwendungsmetriken**.

Die App nutzt den Default-ServiceAccount ohne API-Token. Ein eigener App-ServiceAccount ist daher derzeit kein Pflichtfehler, wäre aber eine klare Grundlage für spätere Berechtigungen.

## 7. CI/CD — PARTIAL

| Erwarteter Schritt | Implementierung | Aktueller Nachweis |
|---|---|---|
| Checkout | Vorhanden | Code vorhanden |
| Dependencies installieren | `uv sync --frozen`, `npm ci` | Lokal geprüft |
| Tests ausführen | Backend und Promotion-Tests | Erfolgreich geprüft |
| Docker bauen | BuildKit-Archive | Dockerfiles lokal erfolgreich |
| Security Scan | **Fehlt** | Kein entsprechendes Gate |
| Registry-Push | Separater trusted Publisher | Aktuell deaktiviert |
| Dev automatisch deployen | **Nicht implementiert wie gefordert** | Dev-Promotion manuell |
| Prod ermöglichen | Approval und Release-Reviewbranch | Vorbereitung vorhanden, Prod nicht betriebsfähig |

**Positive Implementierungsdetails:**

- CI und Publisher getrennt.
- PR-Builds erhalten keine Registry-/Git-Schreibcredentials.
- Publisher prüft Quellbuild-Erfolg und SHA.
- Digestbasierte Promotion ohne Neubuild.
- Freigabe vor Release.
- Prod wird über einen Reviewbranch vorbereitet.
- Globaler Lock und Schutz gegen veraltete Stage-Promotions.
- Rollback über Git dokumentiert.
- GitOps-Commits lösen keine endlose Image-Publishing-Schleife aus.

**Entscheidender Laufzeitbefund:**
In [infra/jenkins-host/jobs.groovy:9](/home/root-admin/fastapi-traefik-datascientest-project/infra/jenkins-host/jobs.groovy:9) und Zeile 15 sind Build- und Publisherjob deaktiviert. Die live gelesenen Jobkonfigurationen bestätigen jeweils `disabled=true`. Der Publisher ist ein Fehler ausgebender Wiederherstellungsplatzhalter.

Damit ist die vollständige Pipeline aktuell **nicht als laufendes CI/CD-System erfüllt**.

**Weitere konkrete Probleme:**

- GitHub-Push-Trigger verwenden `master` statt `main`.
- Keine Terraform-Validierung oder Terraform-Planung.
- Keine nachgewiesenen GitHub-Environment-Protection-Einstellungen.
- Branch-/Tag-Schutz wird dokumentiert, aber nicht durch Repository-Dateien bewiesen.
- `CODEOWNERS` fehlt.
- Der BuildKit-Container ist privilegiert.
- Die dokumentierte Isolation privilegierter CI-Nodes ist nicht implementiert oder live nachgewiesen.
- Der Generate-Client-Workflow führt PR-Code mit einem Schreibtoken bei internen PRs aus.
- Die Dokumentation nennt `gitops-write`, der Publisher erwartet `gitops-app`.
- Der dokumentierte Release-Manager-Kreis stimmt nicht mit `submitter: 'admin'` überein.
- Die Dokumentation beschreibt Feature-Branch-Publishing großzügiger als der automatische Trigger tatsächlich implementiert.

Die deaktivierten GitHub-Deploymentdateien mit `.yml.disabled` sind **keine aktiven Deployment-Workflows**.

## 8. Terraform / Infrastructure as Code — FAIL

**Es existieren keine Terraform-Dateien im untersuchten Repository.** Shell-/kind-Bootstrap und Kubernetes-Manifeste ersetzen die ausdrücklich geforderte Terraform-Implementierung nicht.

| Prüffeld | Ergebnis |
|---|---|
| `main.tf`, `providers.tf`, `versions.tf` | Fehlen |
| `variables.tf`, Typen und Validierungen | Fehlen |
| `outputs.tf`, Locals und Module | Fehlen |
| Dev-/Prod-tfvars | Fehlen |
| Provider-Versionen / `required_version` | Fehlen |
| Remote Backend | Fehlt |
| State Locking / Verschlüsselung | Nicht konfiguriert |
| State-Isolation Dev/Prod | Fehlt |
| Terraform-Netzwerk und Cluster | Fehlen |
| Terraform-IAM, Registry, DNS, Storage | Fehlen |
| Terraform-Datenbank und Backup | Fehlen |
| `fmt`, `init`, `validate`, `plan` in CI | Fehlen |
| Kontrollierter Apply-Prozess | Fehlt |

**State und Security:**

- Keine getrackten Terraform-State-Dateien gefunden.
- Keine Terraform-Secrets in tfvars oder Outputs gefunden, weil diese Dateien fehlen.
- `.terraform/`, `*.tfstate*` und entsprechende tfvars-Regeln fehlen in der Root-`.gitignore`.
- Keine Terraform-Verwendung von `apply -auto-approve` oder `destroy -auto-approve` gefunden.

Das bedeutet **nicht**, dass Terraform sicher implementiert ist. Es ist überhaupt nicht implementiert. VPC, Subnets, Routing, NAT, Security Groups, IAM-Wildcards, öffentliche Datenbanken und Cloud-Backup können deshalb nicht resourceweise bewertet werden.

Terraform war außerdem nicht installiert. Selbst mit installiertem Werkzeug wäre ein erfolgreicher Aufruf in einem leeren Verzeichnis kein Erfüllungsnachweis.

## 9. Monitoring — PARTIAL; Grundanforderung erfüllt

Hier gibt es tatsächliche Implementierung und aktuelle Laufzeitnachweise:

- `kube-prometheus-stack` mit festgelegter Chart-Version.
- Prometheus und Alertmanager mit PVCs.
- kube-state-metrics, Node-Exporter und kubelet/cAdvisor-Metriken.
- Argo-ServiceMonitors und Traefik-PodMonitor.
- Vier Grafana-Dashboards.
- Acht getestete Alert-Regeln.
- Funktionierende Grafana-Anmeldung und gesperrter anonymer API-Zugriff.
- 16 aktive Scrape-Ziele, alle UP.

**Offene Punkte:**

- Keine FastAPI-Instrumentierung.
- Keine eigenen Anwendungs-/Business-Metriken.
- Kein PostgreSQL-Exporter.
- Kein Jenkins-Monitoring.
- App-Alerts berücksichtigen nur Dev und Stage.
- Alertmanager sendet an einen `null`-Receiver: [monitoring/values.yaml:92](/home/root-admin/fastapi-traefik-datascientest-project/monitoring/values.yaml:92).
- Standardregeln sind abgeschaltet; die acht eigenen Regeln ersetzen keine vollständige Plattformüberwachung.
- Grafana-Persistenz ist deaktiviert. Provisionierte Dashboards sind wiederherstellbar; sonstige UI-Änderungen und Zustand sind nicht dauerhaft.
- Monitoring-Dateien sind unversioniert.
- Die laufende Monitoring-Application nutzt Inline-Helm-Werte, noch nicht die vorgesehene Git-Multisource-Konfiguration.

**Bewertung:** Prometheus/Grafana sind erfüllt. Vollständiges Anwendungsmonitoring, Benachrichtigungen und reproduzierbarer Git-Betrieb sind teilweise erfüllt.

## 10. DevSecOps / Security — PARTIAL

**Die Mindestforderung von drei Sicherheitsmaßnahmen ist erfüllt.** Nachweisbar vorhanden sind beispielsweise:

1. Verschlüsselte SealedSecrets für Dev/Stage.
2. Namespacegebundene Secrets und getrennte Credentials.
3. Deaktiviertes ServiceAccount-Token-Mounting für App-Pods.
4. Eingeschränktes Argo AppProject.
5. Trennung von CI und trusted Publisher im ursprünglichen Design.
6. bcrypt-Passworthashing und JWT-Prüfung mit festgelegtem Algorithmus.
7. Verweigerter anonymer Grafana-Zugriff.

**Trotzdem bestehen relevante Sicherheitslücken:**

- Keine Trivy-/Snyk-Scans oder vergleichbare Image-/Dependency-Gates.
- **62 npm-Audit-Findings, davon drei critical.**
- Root-Laufzeit und fehlende Pod-Security-Konfiguration.
- Privilegiertes BuildKit ohne umgesetzte Isolationsgrenze.
- Keine App-NetworkPolicies.
- Dependabot zeigt für Python, npm und Docker auf `/`, obwohl die relevanten Dateien unter `backend/` und `frontend/` liegen.
- Compose veröffentlicht Datenbank, Adminer und weitere lokale Dienste standardmäßig auf allen Hostinterfaces.
- Der lokale Traefik-Override aktiviert eine ungeschützte Dashboard-API.
- Lokales Jenkins verwendet `loggedInUsersCanDoAnything`; für mehrere Benutzer ist das kein angemessenes Rollenmodell.
- Prod-TLS und GitHub-Schutzregeln sind nicht nachgewiesen.

**Aktueller npm-Befund:**

| Paket | Schwere | Einordnung |
|---|---|---|
| `form-data` | Critical | Direkte Dependency |
| `handlebars` | Critical | Transitive Buildtool-Dependency |
| `tar` | Critical | Transitive Buildtool-Dependency |
| `axios` | High | Direkte Dependency |

Fundstellen: [frontend/package.json:19](/home/root-admin/fastapi-traefik-datascientest-project/frontend/package.json:19) und das Lockfile. Die vollständige aktuelle Ausgabe liegt in [npm-audit.json](/tmp/frontend-audit-4ne54tvs/npm-audit.json).

Ein npm-Finding beweist nicht automatisch die Ausnutzbarkeit im ausgelieferten Browserbundle. Kritische Buildtool-Abhängigkeiten bleiben aber ein relevantes CI-Risiko.

**Secret-Prüfung:**

- Die getrackte Root-`.env` und Legacy-Secret-Manifeste enthalten Platzhalter, keine nachgewiesenen echten Zugangsdaten.
- Die vorhandenen SealedSecrets enthalten verschlüsselte Werte.
- Die Musterprüfung des Arbeitsbestands und der Git-Historie fand keine Treffer für die geprüften Private-Key-, AWS-Access-Key- und GitHub-Token-Formate.
- Historische sensible `.env`-Änderungen enthielten bei dieser Prüfung keine Nicht-Platzhalterwerte.

Diese Prüfung ersetzt keinen vollständigen Gitleaks-/TruffleHog-Lauf. Solche Scanner waren nicht verfügbar. Keine gefundenen Secret-Werte wurden ausgegeben.

## 11. Disaster Recovery — FAIL

| Ausfall / Recovery | Vorhanden | Bewertung |
|---|---|---|
| Container-Ausfall | Deployment, Restart-Verhalten, Liveness | Grundmechanismus erfüllt |
| Frontend-/Backend-Rollback | Git-Revert und alte Image-Digests | Dokumentiert und technisch vorbereitet |
| Node-Ausfall | Ein Node, lokaler Storage | Keine belastbare Wiederherstellung |
| PostgreSQL-Backup | Kein Job, Dump-Prozess oder Backupziel | Fehlt |
| Persistenter Storage | PVC, Schutz vor Argo-Pruning | Kein Backup |
| Terraform-Rebuild | Keine Terraform-Implementierung | Fehlt |
| Kubernetes-Rebuild | Lokaler kind-Bootstrap | Teilweise vorhanden, unversioniert |
| Secret-Recovery | Key-Backup und Recovery-Skripte | Teilweise vorhanden |
| Jenkins-Recovery | Neue Installation und Backup-Anleitung | Alte History/Credentials nicht wiederhergestellt |
| Daten-Restore-Test | Nicht vorhanden | Fehlt |

Besonders deutlich ist [MIGRATION_BACKUP_CHECKLIST.md:16](/home/root-admin/fastapi-traefik-datascientest-project/MIGRATION_BACKUP_CHECKLIST.md:16): Alte PostgreSQL-Daten gingen verloren; ein Dump war nicht vorhanden. Neue Datenbanken wurden initialisiert, die alten Zeilen nicht wiederhergestellt.

`Prune=false,Delete=false` am PVC schützt gegen bestimmte Argo-Löschvorgänge. Es schützt nicht gegen Hostverlust, Storage-Schäden oder Datenkorruption.

Es fehlen außerdem konkrete RPO-/RTO-Ziele, Backup-Aufbewahrung, Off-Host-Sicherung und regelmäßig getestete Restore-Schritte.

## 12. README und Dokumentation — PARTIAL

**Vorhanden:** Tech Stack, lokale Entwicklung, Docker, Backend/Frontend, Jenkins/GitOps, Umgebungsbeschreibung, Releases, Rollback und zusätzliche Monitoring-Runbooks.

**Fehlend oder inkonsistent:**

- README bleibt weitgehend die ursprüngliche FastAPI-Template-Beschreibung.
- Badges verweisen auf das Upstream-Projekt.
- `master`-Anleitungen widersprechen dem aktuellen `main`-Betrieb.
- README nennt Compose-Produktion, während `deployment.md` GitOps als Produktionsweg festlegt.
- Terraform-Anleitung fehlt.
- Konkrete Datenbank-Backup-/Restore-Anleitung fehlt.
- Aktueller Jenkins-Wiederherstellungsstatus ist nicht ausreichend mit dem ursprünglichen Betriebsführer verbunden.
- Credential-ID `gitops-write` widerspricht `gitops-app`.
- Release-Manager-Dokumentation widerspricht dem tatsächlichen `admin`-Gate.
- Aussagen über anfängliche Platzhalter treffen inzwischen nur noch auf Prod zu.
- Monitoring-Berichte beschreiben einen funktionierenden lokalen Bootstrap; sie beweisen keinen versionierten Git-Aufbau.
- `.env.example` fehlt. Die getrackte `.env` dient derzeit als Platzhaltervorlage.

## 13. Architecture Diagram — PARTIAL

Ein Mermaid-Diagramm existiert in [README-jenkins.md:8](/home/root-admin/fastapi-traefik-datascientest-project/README-jenkins.md:8).

Es zeigt Git, Jenkins, Publisher, GHCR, Promotion und Argo CD. Es ist ein brauchbares **Release-Prozessdiagramm**.

Für deine vollständige Architekturanforderung fehlen ausdrücklich:

- Terraform.
- Cloud-/Netzwerkinfrastruktur.
- Kubernetes-Cluster und Nodes.
- Ingress / Load Balancer.
- Services und Application Pods.
- ConfigMaps / Secrets.
- PostgreSQL und PVC.
- Prometheus / Grafana.
- Backupziel und Recovery-Datenfluss.

## 14. Abschlussübersicht

`PASS` bedeutet vollständig nachgewiesen, `PARTIAL` bedeutet vorhandene Umsetzung mit Lücken, `FAIL` bedeutet fehlende oder aktuell nicht ausreichende Umsetzung.

| Bereich | Status | Was vorhanden ist | Was fehlt | Priorität |
|---|---|---|---|---|
| Docker | PARTIAL | Erfolgreiche Builds, Lockfiles, Frontend-Multi-Stage, SHA-/Digest-Konzept | Non-Root, schlankes Backend, vollständig reproduzierbares Testimage | P1 |
| Dev/Prod | PARTIAL | Drei Overlays, getrennte Konfiguration und Namespaces | Betriebsfähiges Prod, automatische Dev-Promotion, Terraform-Isolation | P0 |
| Tests | PARTIAL | 55 Backend- und 12 CI-Tests erfolgreich; E2E vorhanden | Vollständiger E2E-Nachweis und verbindliches Pipeline-Gate; grüner Frontend-Lint | P1 |
| Kubernetes | PARTIAL | Deployments, Services, ConfigMaps, Secrets, Probes, Limits, PVC, Ingress | Pod-/Netzwerksicherheit, Prod-Bootstrap, dauerhafter Storage | P1 |
| CI/CD | PARTIAL | Gute Build-/Publisher-/Promotion-Implementierung | Aktive Jobs, Security Scan, automatische Dev-Bereitstellung | P0 |
| Terraform | FAIL | Keine Terraform-Implementierung | Gesamte Cloud-IaC, Backend, State-Isolation und CI-Prüfung | P0 |
| Monitoring | PARTIAL | Prometheus/Grafana live geprüft, Dashboards, Scraping, Regeln | App-Metriken, Benachrichtigungen, Git-Versionierung, Prod-Abdeckung | P1 |
| Security | PARTIAL | Mehr als drei konkrete Maßnahmen | Dependency-Fixes, Scangates, Container-/CI-Isolation | P0 |
| Disaster Recovery | FAIL | Git-Rollback, Secret-Recovery, lokaler Rebuild | Datenbank-/Storage-Backup und getesteter Restore | P0 |
| Documentation | PARTIAL | Umfangreiche Setup-/GitOps-/Monitoring-Dokumente | Konsistenz, Terraform, vollständige Recovery-Anleitung | P1 |
| Architecture Diagram | PARTIAL | GitOps-/Release-Diagramm | Vollständige Infrastruktur-, App-, Monitoring- und Backuparchitektur | P1 |

## CRITICAL

### C1 — Terraform vollständig fehlend

**Datei/Stelle:** Repositoryweit; keine `.tf`-/tfvars-Dateien.

**Problem:** Die explizite Terraform-Pflichtanforderung ist nicht erfüllt.

**Warum problematisch:** Cloud-Infrastruktur, State-Isolation und kontrollierter Infrastruktur-Rebuild sind nicht nachweisbar.

**Konkrete Lösung:** Terraform für die tatsächlich gewählte Zielplattform implementieren: Versionen, Provider, typisierte Variablen, Dev-/Prod-Konfiguration, Outputs und Remote Backend mit Verschlüsselung und Locking. CI um `fmt`, `init`, `validate` und `plan` ergänzen; Prod-Apply ausschließlich kontrolliert ausführen.

### C2 — Vollständiges CI/CD aktuell deaktiviert

**Datei/Stelle:** `infra/jenkins-host/jobs.groovy`, Zeilen 7–16; live bestätigt.

**Problem:** Buildjob deaktiviert, Publisher deaktivierter Platzhalter.

**Warum problematisch:** Vorhandener Pipeline-Code führt nicht automatisch zu getesteten, gepushten und deployten Versionen.

**Konkrete Lösung:** Isolierten trusted Publisher und passende Credentials konfigurieren; Buildjob nach Kapazitätsprüfung aktivieren; Trigger herstellen; einen vollständigen Commit→Tests→Build→Scan→Push→Deployment-Lauf nachweisen.

### C3 — Prod noch nicht betriebsfähig

**Datei/Stelle:** `deploy/overlays/prod/kustomization.yaml`, Zeilen 9 und 12; `argocd/applicationset.yaml`.

**Problem:** Platzhalter-Images, kein laufender Prod-Namespace, keine nachgewiesene Prod-Provisionierung.

**Warum problematisch:** Das Overlay rendert, würde mit diesen Images aber nicht erfolgreich starten.

**Konkrete Lösung:** Getestetes Artefaktpaar über den Release-Prozess einsetzen; Prod-Namespace, Secrets, Storage, DNS und TLS bereitstellen; erst danach die Prod-Application aktivieren. Einen genehmigten Release und Rollback demonstrieren.

### C4 — Automatisches Dev-Deployment fehlt

**Datei/Stelle:** `Jenkinsfile`, Zeilen 250–261; `Jenkinsfile.promote`, Zeilen 96–99; `ci/publish.sh`, letzte Verzweigung.

**Problem:** Automatisch wird Stage vorgesehen; Dev benötigt manuelle Auswahl und Freigabe.

**Warum problematisch:** Deine ausdrücklich geforderte automatische Dev-Bereitstellung ist damit nicht erfüllt.

**Konkrete Lösung:** Einen klar definierten Branch automatisch nach Dev promovieren. Prod weiterhin über Approval und Review absichern.

### C5 — Security Scan fehlt; kritische Dependencies vorhanden

**Datei/Stelle:** `frontend/package.json`, Zeilen 19–20 und 30; `frontend/package-lock.json`; beide Jenkinsfiles.

**Problem:** Drei kritische und 55 hohe npm-Findings; kein Security-Gate.

**Warum problematisch:** Unsichere Dependencies können gebaut und veröffentlicht werden, ohne die Pipeline zu stoppen.

**Konkrete Lösung:** Dependency-Baum gezielt aktualisieren, Lockfile erneuern und Regressionstests durchführen. Anschließend Dependency- und Image-Scans vor Publishing verbindlich einbauen. Kein blindes `npm audit fix --force`.

### C6 — Datenbank-Recovery fehlt

**Datei/Stelle:** `deploy/base/pvc-db.yaml`, `deploy/base/deployment-db.yaml`; `MIGRATION_BACKUP_CHECKLIST.md`, Zeile 16.

**Problem:** Keine regelmäßigen Backups, kein Off-Host-Ziel, kein Restore-Test.

**Warum problematisch:** Persistente Daten können bei Node-/Hostverlust endgültig verloren gehen.

**Konkrete Lösung:** Automatisiertes PostgreSQL-Backup, verschlüsseltes externes Backupziel, Aufbewahrung und Alarmierung einrichten. Restore in eine getrennte Datenbank testen und dokumentieren.

### C7 — Wesentliche Implementierung nicht versioniert

**Datei/Stelle:** `infra/`, `monitoring/`, neue Argo-Dateien und Bootstrap-Skripte; aktueller Git-Status.

**Problem:** Wichtige lokale Implementierungen fehlen in einem normalen Checkout.

**Warum problematisch:** Ein Prüfer kann den aktuellen Aufbau nicht aus dem abgegebenen Repository reproduzieren.

**Konkrete Lösung:** Nach Review die benötigten nicht geheimen Implementierungen versionieren. Private Schlüssel und lokale Credentials weiterhin ausschließen. Anschließend den Aufbau aus einem frischen Checkout überprüfen.

## SHOULD FIX

| ID | Datei / relevante Stelle | Problem und Auswirkung | Konkrete Lösung |
|---|---|---|---|
| S1 | `.github/workflows/test-backend.yml:6`, `lint-backend.yml:6`, `playwright.yml:6`, `test-docker-compose.yml:6` | Push-Tests hören auf `master`; `main` wird nicht abgedeckt | Trigger an die tatsächliche Branchstrategie anpassen |
| S2 | `README-jenkins.md:119`, `Jenkinsfile.promote:108` | Unterschiedliche Credential-IDs verhindern Setup nach Anleitung | Eine ID durchgängig verwenden |
| S3 | `.github/dependabot.yml:12`, `:19`, `:26` | Falsche Verzeichnisse für Python/npm/Docker | `backend/` und `frontend/` jeweils konfigurieren |
| S4 | `backend/Dockerfile:28`, `:36`; `frontend/Dockerfile:19`; aktive Deployments | Root und unnötige Runtime-Pakete erhöhen Angriffsfläche | Non-Root-Images und passende Security Contexts; Backend ohne Dev-Abhängigkeiten |
| S5 | `Jenkinsfile`, privilegierter BuildKit-Container; `ci/jenkins-controller-rbac.yaml`; `infra/jenkins-host/jenkins.yaml` | Dokumentierte CI-Isolation fehlt; breite lokale Benutzerrechte | CI isolieren, Admission-/Scheduling-Grenzen umsetzen und Rollenmodell verwenden |
| S6 | `infra/jenkins-host/run-tool.sh:18`, `:36` | 640-MiB-Container und 384-MiB-V8-Heap bergen Buildrisiko | Speicher unter Last messen und Limits anpassen; Audit-Build scheiterte mit 384-MiB-Heap und gelang mit größerem Heap |
| S7 | `frontend/tests/utils/privateApi.ts:3`; Jenkins-Teststages | E2E benötigt lokalen Client; kein verbindliches E2E-Gate | Generierung explizit in den Testablauf aufnehmen und Browsertests vor Promotion ausführen |
| S8 | `frontend/biome.json`; `frontend/package.json:9` | 22 Lintfehler; vorhandenes Lintskript verändert Dateien | Separates Checkskript ohne Auto-Fixes; generierten Code passend konfigurieren |
| S9 | `backend/app/api/routes/utils.py:34`; Backend-Readiness | Readiness erkennt DB-Ausfall nicht | Separate begrenzte Readiness-Prüfung; Liveness prozessbezogen lassen |
| S10 | `monitoring/values.yaml:92`; `backend/app/main.py` | Alerts werden nicht zugestellt; App-Metriken fehlen | Benachrichtigungskanal und FastAPI-Instrumentierung implementieren |
| S11 | `deploy/base/ingress-app.yaml:27`; Stage-Overlay | TLS nur referenziert; Stage-Dokumentation suggeriert teilweise verfügbare Docs-Route | Zertifikatsprozess fertigstellen; `/docs` bewusst routen oder Dokumentation korrigieren |
| S12 | `docker-compose.override.yml:11`, `:14`, `:36`, `:51` | Docker-Socket, insecure API und breit veröffentlichte lokale Ports | Lokale Ports an Loopback binden; Dashboard nur geschützt zugänglich machen |
| S13 | `.github/workflows/generate-client.yml:22`, `:39` | PR-Code wird im Kontext eines Schreibtokens ausgeführt | Generierung mit Leserechten prüfen; Schreibschritt getrennt und auf vertrauenswürdigem Code ausführen |
| S14 | `.github/workflows/test-docker-compose.yml:23` | `curl` ohne `--fail` kann HTTP-Fehler als Erfolg werten | `curl --fail --show-error` verwenden |
| S15 | `.gitignore` | Terraform-State-/Tooling-Regeln fehlen | Vor Einführung von Terraform `.terraform/`, State-, Plan- und sensible lokale Variablendateien ausschließen |
| S16 | `README.md`; `README-jenkins.md:8`; `deployment.md` | Zielbild, tatsächlicher Betrieb und Template-Inhalte widersprechen sich | README konsolidieren und vollständiges Architekturdiagramm ergänzen |

## NICE TO HAVE

- **Verfügbarkeit:** `deploy/overlays/prod/` um PodDisruptionBudgets, Topology-Spread und bei Bedarf Autoscaling ergänzen. StatefulSet allein ersetzt keine PostgreSQL-HA-Lösung.
- **Artefaktvertrauen:** Dockerfiles und GitHub Actions per Digest beziehungsweise Commit-SHA pinnen; SBOMs und Image-Signaturen erzeugen.
- **Anwendungssicherheit:** Login-/Recovery-Ratenbegrenzung ergänzen; Passwort-Recovery-Antworten in `backend/app/api/routes/login.py:54` gegen Account-Enumeration vereinheitlichen.
- **Betriebsqualität:** SLOs, HTTP-Fehlerraten, Latenzalarme und längere Restore-/Ausfallübungen ergänzen.
- **Frontend:** Vite-Bundle aufteilen; der geprüfte Hauptchunk liegt bei ungefähr 826 kB unkomprimiert.

## Priorisierte TODO-Liste

1. **Terraform-Zielplattform und vollständige IaC implementieren** — C1.
2. **Kritische Dependencies beheben und Security-Gates einbauen** — C5.
3. **Notwendige lokale Implementierung nach Review versionieren** — C7; Secret-Ausschlüsse vorher prüfen.
4. **Jenkins-Credentials, Isolation und Speicherbudget herstellen** — C2, S2, S5, S6.
5. **Build-/Publisherjobs aktivieren und vollständigen Pipeline-Lauf nachweisen** — C2.
6. **Automatisches Dev-Deployment umsetzen** — C4.
7. **GitHub-Trigger und Testgates korrigieren** — S1, S7, S8, S14.
8. **Datenbank-Backup und getesteten Restore einrichten** — C6.
9. **Prod mit echten Images, Secrets, Storage, DNS und TLS bereitstellen** — C3, S11.
10. **Prod-Approval, Branchschutz und Rollback tatsächlich demonstrieren** — C3.
11. **Container und Kubernetes härten** — S4, S5, S9, S12, S13.
12. **Dependabot reparieren und Monitoring-Benachrichtigungen ergänzen** — S3, S10.
13. **README, Recovery-Anleitung und Architekturdiagramm konsolidieren** — S16.

## Gesamtbewertung

**Project readiness: 53 / 100**

**Erfüllte Pflichtbestandteile:** funktionierende Dockerfiles, echte Unit-/API-/Integrationstests, Kubernetes-Grundressourcen, Dev-Konfiguration, tatsächlich laufendes Prometheus/Grafana und mindestens drei Sicherheitsmaßnahmen.

**Noch fehlende beziehungsweise unvollständige Pflichtbestandteile:** Terraform, aktive vollständige CI/CD-Kette, Security-Scan vor Publishing, automatisches Dev-Deployment, betriebsfähiges Prod, Datenbank-/Storage-Recovery und vollständige Architekturdokumentation.

**Vor der Abgabe unbedingt korrigieren:** Terraform, deaktivierte Pipeline, Prod-Platzhalter, kritische Dependencies und Backup/Restore. Den erfolgreichen lokalen Betrieb solltest du anschließend aus einem versionierten, frischen Checkout reproduzieren.

Ich nehme erst auf deine weitere Anweisung Änderungen vor.
