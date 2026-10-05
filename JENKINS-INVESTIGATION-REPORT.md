> Historical investigation of the previous setup. Current namespaces, permissions
> and pipeline behavior are documented in [README-jenkins.md](README-jenkins.md).

# How I investigated the Jenkins failure

Date: 2026-10-01. Investigation performed with AI assistance using read-only checks and a server-side dry-run. No deployment, cleanup, restart, or pipeline modification was performed.

## Objective

Understand why Jenkins could not complete a build and investigate a reported error applying `jenkins-controller-dev-rbac.yaml`.

## Method and evidence

1. **Checked the cluster and controller.** The active context was `minikube`; namespaces `jenkins` and `dev` existed. The Jenkins StatefulSet was ready and its Pod was `2/2 Running`.
2. **Tested the RBAC hypothesis.** Server-side dry-run reported both RBAC resources unchanged. The controller used service account `jenkins` in namespace `jenkins`. Authorization checks permitted creating Pods, executing in Pods, and reading Pod logs in `dev`. Build #29 had successfully provisioned an agent. This did not reproduce the originally reported apply error.
3. **Correlated build and controller logs.** Build #29 reached frontend image-layer extraction. At approximately 10:39 UTC, controller logs reported `No space left on device`, failure to persist `program.dat`, and failure to save build metadata. Agent/pipeline execution errors followed.
4. **Inspected storage.** The VM had a 32 GiB disk and a 30 GiB root filesystem. During inspection, that filesystem was 88% used with 3.7 GiB available; inode use was 25%. Jenkins home used only 234 MiB. Its 8 GiB PVC used Minikube hostPath storage backed by the same filesystem. Host Docker reported approximately 2.377 GB of reclaimable build cache.
5. **Checked configuration consistency.** Build #29 loaded its Jenkinsfile from Git and used an agent definition different from the uncommitted local Jenkinsfile. A local edit alone therefore would not change the next SCM-based build.

## Conclusion

A confirmed failure was Jenkins being unable to persist pipeline state because storage writes returned ENOSPC. Shared host disk exhaustion during image building is strongly supported by the logs and storage layout. The exact peak usage was not captured; recovered free space afterward does not contradict the earlier failure.

The controller RBAC configuration passed validation in the inspected context. The user's original `kubectl apply` error remains unresolved without its exact output and execution context; it must not be automatically attributed to the disk incident.

## Proposed recovery and acceptance criteria

Review and reclaim disposable build cache, increase backing disk capacity if necessary, and publish the intended reviewed Jenkinsfile revision. Then run one build while monitoring disk space and controller logs. Recovery is verified only when the complete pipeline finishes, reports persist, and no new storage errors occur.

No recovery was executed or successful rerun claimed. The accompanying [cheat sheet](JENKINS-TROUBLESHOOTING.md) contains diagnostic commands and the recovery sequence.

## What I learned

I should distinguish kubectl permissions, controller health, agent provisioning, and build execution. A Running Pod is not proof of a healthy application, a PVC capacity field does not guarantee free space on hostPath storage, and the first concrete log error is more useful than later cascading symptoms.
