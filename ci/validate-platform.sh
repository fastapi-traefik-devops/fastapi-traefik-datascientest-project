#!/bin/sh
# Validate the Argo CD objects and the monitoring resources Argo CD deploys.
# Custom resources (Application, AppProject, ServiceMonitor, PrometheusRule, ...) are
# checked against the community CRDs-catalog, pinned to a reviewed commit.
set -eu
catalog='https://raw.githubusercontent.com/datreeio/CRDs-catalog/d373c2da9702bc9509a004db83e57263fe3bdfc1/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json'
mkdir -p /tmp/kubeconform-cache
check() {
  kubeconform -cache /tmp/kubeconform-cache -strict -summary -kubernetes-version 1.35.0 \
    -schema-location default -schema-location "$catalog" "$@"
}
check argocd/*.yaml argocd/bootstrap/*.yaml infra/kind/app-stage-local.yaml infra/kind/project-fastapi.yaml
kustomize build monitoring | check -
