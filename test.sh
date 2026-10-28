#!/bin/sh
# Runs every rule against its test file in a Semgrep container with no network.
set -eu
cd "$(dirname "$0")"
exec docker run --rm --network none -v "$PWD":/src:ro -w /src \
  "${SEMGREP_IMAGE:-semgrep/semgrep}" semgrep --test --metrics off --config rules tests
