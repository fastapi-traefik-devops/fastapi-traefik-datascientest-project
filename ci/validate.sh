#!/bin/sh
set -eu
helpers=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p rendered /tmp/kubeconform-cache
for environment in dev stage prod; do
  kustomize build "kubernetes/apps/liora/overlays/$environment" > "rendered/$environment.yaml"
  python3 "$helpers/validate_gitops.py" "rendered/$environment.yaml" "$environment"
  # Built-in kinds use the default schemas; operator CRDs use the strict schemas generated
  # by crd_schema.py next to this script. A kind without any schema fails validation.
  kubeconform -cache /tmp/kubeconform-cache -strict -summary -kubernetes-version 1.35.0 \
    -schema-location default \
    -schema-location "$helpers/crd-{{.Group}}-{{.ResourceKind}}-{{.ResourceAPIVersion}}.json" \
    "rendered/$environment.yaml"
done
