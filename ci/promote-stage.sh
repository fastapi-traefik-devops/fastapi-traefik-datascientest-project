#!/bin/sh
# Trusted publisher only: after the SHA images are published, record them for stage on main.
# promote.py verifies the digests in GHCR, rewrites deploy/overlays/stage, validates the
# overlays and pushes one GitOps commit; Argo CD deploys it. Credentials live only in a
# temporary directory and are never printed.
set -eu
set +x
: "${EXPECTED_SOURCE_SHA:?verified source SHA required}" "${GHCR_USER:?}" "${GHCR_TOKEN:?}" "${GIT_TOKEN:?}"
promote=${PROMOTE_PY:-$(dirname -- "$0")/promote.py}
credentials=$(mktemp -d)
trap 'rm -rf "$credentials"' EXIT HUP INT TERM
# GHCR packages are private: promote.py reads the image digests with crane.
export DOCKER_CONFIG="$credentials/docker"
mkdir -p "$DOCKER_CONFIG"
printf '%s' "$GHCR_TOKEN" | crane auth login ghcr.io -u "$GHCR_USER" --password-stdin >/dev/null
# GitHub App installation tokens authenticate Git over HTTPS as user x-access-token.
cat > "$credentials/askpass" <<'ASKPASS'
#!/bin/sh
case "$1" in
  *Username*) printf '%s\n' x-access-token ;;
  *) printf '%s\n' "$GIT_TOKEN" ;;
esac
ASKPASS
chmod 700 "$credentials/askpass"
export GIT_ASKPASS="$credentials/askpass" GIT_TERMINAL_PROMPT=0
python3 "$promote" stage "$EXPECTED_SOURCE_SHA"
