# CI implementation

See [the operating guide](../infra/jenkins-host/README.md). Scripts in this directory are
executed by Jenkins; only the trusted promotion job receives write credentials.

## Existing K3s main pipeline

The normal `Jenkinsfile` runs the existing 13 functional gates on the resulting
application main commit and exports its tested runtime image archives. The
separate `trusted/publish` job publishes immutable images and updates only the
STAGE overlay in the infrastructure repository; Argo CD deploys that update.
The main job's approximately two-minute SCM poll is installed in job configuration
only after the first controlled cycle and manual STAGE verification succeed.
There is no nightly schedule or recurring multibranch indexing.

Application PRs run the same functional tests without exporting or publishing.
Manual DEV and the blocked PROD path are separate: PROD cannot be enabled until
the agreed automatic STAGE acceptance gate is implemented and verified. Images
must never be rebuilt for PROD. See [publication details](PUBLICATION.md) and the
[explicit archive contract](ARTIFACTS.md).

## Manual K3s migration checkpoint

`Jenkinsfile.migration` is an operator-installed, inline, manual-only Pipeline
for `host-ci`. Its `APP_COMMIT` must be an exact reviewed commit; `SOURCE_BUNDLE`
is a local Git bundle supplied on the CI work volume. This operator-held mode needs no
GitHub egress and binds no publishing credentials. Other jobs must remain held
while using this separate one-shot checkpoint; it is not the normal main poll. The infrastructure operator helper requests exactly one build
and restores the execution hold after it finishes or fails.

`python3 ci/phase1.py steps --profile migration` selects 13 existing functional
gates. Security scans, GitOps validation and release attestation are deferred.
Dependency installation uses `npm ci --no-audit`; explicit security steps remain
available in the unchanged full/release profiles. Tests create disposable Docker
PostgreSQL data and never connect to the application K3s databases.

JUnit/coverage reports and `migration-result.json` record actual outcomes and
deferred gates. By default this is not publication evidence: no `gates.json` or
image tarballs are produced. The explicit `EXPORT_IMAGES=true` option exports
tested archives and a functional candidate with deferred-scan evidence, but still
never publishes, promotes or deploys. The infrastructure helper binds this option
to a new `prepare --export-images` receipt; an existing build cannot be relabeled
as a candidate. A failure ends that one-shot request, with evidence retained.

The manual Pipeline generates its result through `python3 ci/phase1.py migration-report`.
This records incomplete functional steps separately from deferred checks; XML
collection, archiving and cleanup also run if result generation fails.
