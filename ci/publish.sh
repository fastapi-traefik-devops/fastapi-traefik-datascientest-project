#!/bin/sh
# Legacy entrypoint is intentionally closed: it used application-repository overlays.
set -eu
printf '%s\n' 'Use the reviewed trusted publisher; legacy publication is disabled.' >&2
exit 1
