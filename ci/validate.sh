#!/bin/sh
set -eu
helpers=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p rendered /tmp/kubeconform-cache
for environment in dev stage prod; do
  kustomize build "kubernetes/apps/liora/overlays/$environment" > "rendered/$environment.yaml"
  python3 "$helpers/validate_gitops.py" "rendered/$environment.yaml" "$environment"
  # CloudNativePG kinds have no bundled schema; skip only those, keep strict elsewhere.
  kubeconform -cache /tmp/kubeconform-cache -strict -summary -kubernetes-version 1.35.0 \
    -skip Cluster,ObjectStore "rendered/$environment.yaml"
done
