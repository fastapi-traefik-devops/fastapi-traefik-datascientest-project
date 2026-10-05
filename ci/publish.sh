#!/bin/sh
# Executes only in the trusted publisher, never in an application build Pod.
set -eu
set +x
credential_dir=$(mktemp -d)
trap 'rm -rf "$credential_dir"' EXIT HUP INT TERM
export DOCKER_CONFIG="$credential_dir/docker"
mkdir -p "$DOCKER_CONFIG"
printf '%s' "$GHCR_TOKEN" | crane auth login ghcr.io -u "$GHCR_USER" --password-stdin
cat > "$credential_dir/askpass" <<'ASKPASS'
#!/bin/sh
case "$1" in
  *Username*) printf '%s\n' "$GIT_USER" ;;
  *Password*) printf '%s\n' "$GIT_TOKEN" ;;
esac
ASKPASS
chmod 700 "$credential_dir/askpass"
export GIT_ASKPASS="$credential_dir/askpass" GIT_TERMINAL_PROMPT=0
repo=https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git
if [ "$PROMOTION_MODE" = release ]; then
  # Resolve annotated/lightweight tag in a separate data-only clone.
  git clone --quiet --no-checkout "$repo" "$credential_dir/source"
  IMAGE_SHA=$(git -C "$credential_dir/source" rev-parse "refs/tags/$RELEASE_TAG^{commit}")
  git -C "$credential_dir/source" merge-base --is-ancestor "$IMAGE_SHA" origin/main
  export IMAGE_SHA
  # promote.py fails closed for missing images, checks stage evidence, never builds.
  python3 ci/promote.py prod "$IMAGE_SHA" --release "$RELEASE_TAG"
  exit
fi
# Existing SHA tags are NEVER overwritten. Partial publication is retryable.
# Re-running CI may produce different bytes; retain the original successful image.
for component in backend frontend; do
  image="$REGISTRY_NAMESPACE/fastapi-$component:sha-$IMAGE_SHA"
  if crane digest "$image" > "$credential_dir/digest" 2> "$credential_dir/error"; then
    echo "Retaining existing immutable $component image for $IMAGE_SHA"
  elif grep -Eq 'MANIFEST_UNKNOWN|NAME_UNKNOWN' "$credential_dir/error"; then
    crane push "artifacts/$component-ci.tar" "$image"
  else
    echo 'Registry lookup failed; refusing to treat it as a missing image' >&2
    exit 1
  fi
done
if [ "$PROMOTION_MODE" = dev ]; then
  python3 ci/promote.py dev "$IMAGE_SHA"
elif [ "$SOURCE_JOB" = app-ci/main ]; then
  python3 ci/promote.py stage "$IMAGE_SHA"
fi
