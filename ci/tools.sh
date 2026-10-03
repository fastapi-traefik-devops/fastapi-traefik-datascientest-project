#!/bin/sh
# Used only on disposable amd64 Linux agents. Versions are deliberately explicit.
set -eu
mkdir -p /tmp/ci-bin
fetch() {
  url=$1; file=$2
  curl --fail --silent --show-error --location --retry 3 "$url" -o "$file"
}
fetch https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v5.6.0/kustomize_v5.6.0_linux_amd64.tar.gz /tmp/kustomize.tar.gz
echo "54e4031ddc4e7fc59e408da29e7c646e8e57b8088c51b84b3df0864f47b5148f  /tmp/kustomize.tar.gz" | sha256sum -c -
tar xzf /tmp/kustomize.tar.gz -C /tmp/ci-bin kustomize
fetch https://github.com/yannh/kubeconform/releases/download/v0.6.7/kubeconform-linux-amd64.tar.gz /tmp/kubeconform.tar.gz
echo "95f14e87aa28c09d5941f11bd024c1d02fdc0303ccaa23f61cef67bc92619d73  /tmp/kubeconform.tar.gz" | sha256sum -c -
tar xzf /tmp/kubeconform.tar.gz -C /tmp/ci-bin kubeconform
fetch https://github.com/google/go-containerregistry/releases/download/v0.20.3/go-containerregistry_Linux_x86_64.tar.gz /tmp/crane.tar.gz
echo "36c67a932f489b3f2724b64af90b599a8ef2aa7b004872597373c0ad694dc059  /tmp/crane.tar.gz" | sha256sum -c -
tar xzf /tmp/crane.tar.gz -C /tmp/ci-bin crane
