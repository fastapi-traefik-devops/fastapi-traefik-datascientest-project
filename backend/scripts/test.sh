#!/usr/bin/env bash

set -e
set -x

coverage run --source=app -m pytest "$@"
coverage report --show-missing
coverage xml
coverage html --title "Backend coverage"
