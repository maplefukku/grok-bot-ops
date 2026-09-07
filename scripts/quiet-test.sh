#!/usr/bin/env bash
# Repo WRAP of box SoT /workspace/fleet-scripts/quiet-test.sh
# Do not invent a second quiet body.
# Usage: scripts/quiet-test.sh -- <cmd>
set -euo pipefail
FLEET="${QUIET_TEST:-/workspace/fleet-scripts/quiet-test.sh}"
if [[ -f "$FLEET" && -x "$FLEET" ]]; then
  exec "$FLEET" "$@"
fi
if [[ "${1:-}" == "--" ]]; then
  shift
fi
if [[ "$#" -eq 0 ]]; then
  printf '%s\n' "scripts/quiet-test.sh: fleet missing at ${FLEET}; pass -- <cmd>" >&2
  exit 2
fi
exec "$@"
