#!/bin/sh
set -eu
mkdir -p rendered /tmp/kubeconform-cache
for environment in dev stage prod; do
  kustomize build "deploy/overlays/$environment" > "rendered/$environment.yaml"
  kubeconform -cache /tmp/kubeconform-cache -strict -summary -kubernetes-version 1.31.0 "rendered/$environment.yaml"
done
