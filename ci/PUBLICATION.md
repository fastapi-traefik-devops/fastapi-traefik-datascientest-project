# Prepared Phase 9 publication

Local implementation only. Keep all Jenkins jobs, polling, schedules, publication
and deployment disabled until the operator explicitly approves a live checkpoint.
No security scans are added or run in this educational migration increment.

The regular Jenkinsfile runs all 13 existing functional gates on the resulting
checked-out main commit, exports those exact runtime images, and requests the
trusted publisher only for main. PR builds do not export/publish. No cron is
installed. `Jenkinsfile.migration` retains the inert manual build by default;
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
main commit → Argo automatic deployment → automatic acceptance. No STAGE PR.
The Jenkins lock spans publication/promotion/acceptance. The writer rechecks exact
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

A separate `stage-observer` agent has read-only STAGE/Argo RBAC and no writer
credentials. It verifies Argo's source/path/main, Synced/Healthy, fully ready
Deployments/Pods, actual running manifest imageIDs and HTTPS root + health smoke.
A login interstitial cannot satisfy smoke. Evidence ties application SHA and both
digests to requested infrastructure commit, observed Argo revision, Pod UIDs and
UTC time. Failed observation records failure, blocks PROD and never rolls back.
The writer checks observed revision ancestry and current pair before recording
acceptance. New promotions invalidate current acceptance.

DEV and PROD remain manual, producing review branches/compare links; no automatic
merge. DEV can use an approved feature-branch manual candidate. PROD selects a
vX.Y.Z application tag and SHA, reuses SHA-image digests without rebuilding or
republishing, and requires matching successful STAGE acceptance in infrastructure
main history. A promotion record without acceptance is insufficient. Rollback is
manual. Credentials live only in private temporary authentication directories.

Before live approval: publish reviewed source commits separately, install reviewed
Jenkins definitions and immutable helper pins, prepare observer node/Secrets/RBAC,
verify controller token-mint egress and branch access. None of those operations
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
