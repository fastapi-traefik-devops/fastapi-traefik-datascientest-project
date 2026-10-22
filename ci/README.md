# CI implementation

See [the operating guide](../infra/jenkins-host/README.md). Scripts in this directory are
executed by Jenkins; only the trusted promotion job receives write credentials.

## Manual K3s migration checkpoint

`Jenkinsfile.migration` is an operator-installed, inline, manual-only Pipeline
for `host-ci`. Its `APP_COMMIT` must be an exact reviewed commit; `SOURCE_BUNDLE`
is a local Git bundle supplied on the CI work volume. The controller needs no
GitHub egress and the build binds no publishing credentials. All imported jobs
remain disabled. The infrastructure operator helper requests exactly one build
and restores the execution hold after it finishes or fails.

`python3 ci/phase1.py steps --profile migration` selects 13 existing functional
gates. Security scans, GitOps validation and release attestation are deferred.
Dependency installation uses `npm ci --no-audit`; explicit security steps remain
available in the unchanged full/release profiles. Tests create disposable Docker
PostgreSQL data and never connect to the application K3s databases.

JUnit/coverage reports and `migration-result.json` record actual outcomes and
deferred gates. This is not release evidence: no `gates.json`, image tarballs,
publication, promotion or deployment is produced. A failure ends this checkpoint;
retry and later automation require a separate operator decision.

The manual Pipeline generates its result through `python3 ci/phase1.py migration-report`.
This records incomplete functional steps separately from deferred checks; XML
collection, archiving and cleanup also run if result generation fails.
