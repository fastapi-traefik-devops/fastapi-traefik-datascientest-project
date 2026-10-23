# Phase 9 initial cycle and retained target work

Local implementation only. Keep all Jenkins jobs, polling, schedules, publication
and deployment disabled until the operator explicitly approves a live checkpoint.
No security scans are added or run in this educational migration increment.

The regular Jenkinsfile runs all 13 existing functional gates on the resulting
checked-out main commit, exports those exact runtime images, and requests the
trusted publisher only for main. PR builds do not export/publish. The prepared
main job uses one SCM poll (`H/2 * * * *`), with no nightly cron, webhook
or recurring multibranch indexing. The operator installs it in the existing job
configuration only after the first controlled live cycle passes; the Jenkinsfile
does not enable it during that first run. `Jenkinsfile.migration` retains the inert
manual build by default;
`EXPORT_IMAGES=true` is an explicit archive-only checkpoint, with no publication.
Old build #2 cannot qualify: it has neither archives nor the candidate contract.

`candidate.json` records the exact SHA, allowlisted source job/build, successful
functional gates, archive/report SHA256 and all seven deferred steps, with
`security_scanned:false`. The trusted publisher independently requires a completed
SUCCESS source run, checks its actual revision, reports and archive integrity,
and uses explicit `--mode functional`. Default registry admission still requires
the original scan-backed release attestation; missing scans are never fabricated.
SHA tags are write-once and remote digests must match the exported bytes.

STAGE: successful current-main CI → immutable publication → direct infrastructure
main commit → Argo automatic deployment → automatic acceptance → acceptance
receipt in infrastructure main. No STAGE PR. The Jenkins lock spans publication,
the STAGE update, observation and the receipt. A failed observation is recorded
and fails the publisher build; it never rolls back. Until this wiring is installed
and live-verified, verify STAGE deployments manually. The writer rechecks exact
application main immediately before every infrastructure push and skips obsolete
builds (even if newer CI fails). Non-fast-forward infrastructure races retry from
the latest main, preserving unrelated changes. Two repositories cannot offer an
atomic transaction across the source-head check and infrastructure push.

Only STAGE kustomization.yaml, promotion.json and acceptance.json under
`kubernetes/apps/liora/overlays/stage/` may be changed directly. GitHub App
Contents write cannot itself restrict paths; the reviewed pinned writer does.
Verify branch rules and any necessary App exception before activation. Never run
code from the selected application/infrastructure checkout with writer credentials.
The old `ci/publish.sh` entrypoint fails closed.

## STAGE acceptance and remaining target work

`Jenkinsfile.promote` runs the observer for every promoted `stage` request
(restored from the prepared orchestration in commit `3b37b50`, still without
DEV/PROD actions). Activation needs the infrastructure `acceptance/` overlay with
one replica, its inbound node and connection Secret, and both helper bundles
rebuilt from the reviewed application commit. `ci/test_promote_pipeline.py`
pins the wiring: the observer runs inside the lock without credentials, and the
trusted helper records the receipt before the build verdict.

The `stage-observer` agent has read-only STAGE/Argo RBAC and no writer
credentials. It verifies Argo's source/path/main, Synced/Healthy, fully ready
Deployments/Pods, actual running manifest imageIDs and HTTPS root + health smoke.
A login interstitial cannot satisfy smoke. Evidence ties application SHA and both
digests to requested infrastructure commit, observed Argo revision, Pod UIDs and
UTC time. Failed observation records failure, blocks PROD and never rolls back.
The writer checks observed revision ancestry and current pair before recording
acceptance. New promotions invalidate current acceptance.

DEV remains manual through reviewed changes; an expanded Jenkins DEV workflow
is deferred. PROD is explicitly blocked in the CLI/writer and has no initial
publisher action. Fixture tests can exercise the preserved future promotion code,
but do not enable it. After automatic acceptance is implemented AND live-verified,
a reviewed change may enable manual PROD review branches; no automatic merge. DEV can use an approved feature-branch manual candidate.
The preserved future PROD path selects a
vX.Y.Z application tag and SHA, reuses SHA-image digests without rebuilding or
republishing, and requires matching successful STAGE acceptance in infrastructure
main history. A promotion record without acceptance is insufficient. Rollback is
manual. Credentials live only in private temporary authentication directories.

Initial live prerequisites, after explicit approval: publish reviewed source
commits, install the existing main CI/trusted publisher definitions and pinned
helpers, verify source SCM/credentials, controller token-mint egress and branch
access. Set the existing app-ci source to the application repository with only
`main` discovery; a one-time index may establish the main job, but recurring
folder indexing stays disabled. Enable only the main job's SCM polling and the
trusted publisher. Leave all imported PR/other jobs and the migration job held.
No observer, acceptance receipts or DEV/PROD expansion is required for this first
cycle. None of those operations
are performed by local tests. Existing admin login and K3s PostgreSQL data remain
unchanged.

Local checks (no network/registry/cluster writes):

```sh
python3 -B -m unittest discover -s ci -p 'test_*.py'
```

Infrastructure `scripts/ci/validate-gitops.sh` renders all environments, validates
canonical immutable images and rejects placeholders, with strict kubeconform when
available (required by the prepared PR workflow). The publisher uses its pinned
trusted validators against the infrastructure data checkout.
