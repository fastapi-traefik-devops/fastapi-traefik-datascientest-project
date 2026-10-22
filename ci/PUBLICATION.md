# Phase 9 initial cycle and retained target work

Local implementation only. Keep all Jenkins jobs, polling, schedules, publication
and deployment disabled until the operator explicitly approves a live checkpoint.
No security scans are added or run in this educational migration increment.

The regular Jenkinsfile runs all 13 existing functional gates on the resulting
checked-out main commit, exports those exact runtime images, and requests the
trusted publisher only for main. PR builds do not export/publish. The prepared
main Jenkinsfile uses one SCM poll (`H/2 * * * *`), with no nightly cron, webhook
or recurring multibranch indexing. This trigger is NOT installed live. `Jenkinsfile.migration` retains the inert
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
main commit → Argo automatic deployment. No STAGE PR. Automatic acceptance
is the later target increment.
For the initial cycle the Jenkins lock spans publication and the STAGE update.
Automatic acceptance is deferred; verify the first STAGE deployment manually.
The writer rechecks exact
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

## Deferred target implementation

The observer and acceptance code below is preserved and fixture-tested; it is
NOT called by the initial publisher and no observer agent is needed for that
cycle. Full prepared orchestration is retained in Git commit `3b37b50`; extend
the same publisher later rather than adding a duplicate pipeline.

A separate planned `stage-observer` agent has read-only STAGE/Argo RBAC and no writer
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
