#! /usr/bin/env bash

# Generates SealedSecret manifests for one overlay (dev or prod) from
# real secret values, so no plaintext credential ever needs to be committed.
#
# Requires: kubeseal (https://github.com/bitnami-labs/sealed-secrets), and
# either a running sealed-secrets controller (to fetch its cert live) or a
# saved public cert passed via SEALED_SECRETS_CERT.
#
# Usage:
#   SECRET_KEY=... \
#   FIRST_SUPERUSER_PASSWORD=... \
#   SMTP_PASSWORD=... \
#   POSTGRES_PASSWORD=... \
#   ./scripts/seal-secrets.sh dev
#
# Optional env vars:
#   SEALED_SECRETS_CERT           Path to a saved controller public cert.
#                                  If unset, kubeseal fetches it live from
#                                  the cluster in your current kubeconfig
#                                  context.
#   SEALED_SECRETS_CONTROLLER_NAME       Default: sealed-secrets-controller
#   SEALED_SECRETS_CONTROLLER_NAMESPACE  Default: kube-system

set -e

OVERLAY="${1?Usage: $0 <dev|prod>}"
OVERLAY_DIR="k8s/overlays/${OVERLAY}"

if [ ! -d "${OVERLAY_DIR}" ]; then
  echo "No such overlay: ${OVERLAY_DIR}" >&2
  exit 1
fi

NAMESPACE="${OVERLAY}"

KUBESEAL_ARGS=(--namespace "${NAMESPACE}" --format yaml)
if [ -n "${SEALED_SECRETS_CERT:-}" ]; then
  KUBESEAL_ARGS+=(--cert "${SEALED_SECRETS_CERT}")
else
  KUBESEAL_ARGS+=(
    --controller-name "${SEALED_SECRETS_CONTROLLER_NAME:-sealed-secrets-controller}"
    --controller-namespace "${SEALED_SECRETS_CONTROLLER_NAMESPACE:-kube-system}"
  )
fi

seal() {
  local secret_name="$1"
  local out_file="${OVERLAY_DIR}/sealed-secret-${secret_name%-secrets}.yaml"
  shift
  kubectl create secret generic "${secret_name}" \
    --namespace "${NAMESPACE}" \
    --dry-run=client -o yaml \
    "$@" \
  | kubeseal "${KUBESEAL_ARGS[@]}" \
  > "${out_file}"
  echo "Wrote ${out_file}"
}

seal backend-secrets \
  --from-literal=SECRET_KEY="${SECRET_KEY?Variable not set}" \
  --from-literal=FIRST_SUPERUSER_PASSWORD="${FIRST_SUPERUSER_PASSWORD?Variable not set}" \
  --from-literal=SMTP_PASSWORD="${SMTP_PASSWORD:-}" \
  --from-literal=POSTGRES_PASSWORD="${POSTGRES_PASSWORD?Variable not set}"

seal db-secrets \
  --from-literal=POSTGRES_PASSWORD="${POSTGRES_PASSWORD?Variable not set}"

######seal frontend-secrets

echo "Done. Review the generated files, then commit them:"
echo "  git add ${OVERLAY_DIR}/sealed-secret-*.yaml"
