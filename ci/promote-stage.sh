#!/bin/sh
# Compatibility entrypoint uses the same trusted source/history and writer checks.
set -eu
export ACTION=stage
exec sh "$(dirname -- "$0")/publisher-action.sh"
