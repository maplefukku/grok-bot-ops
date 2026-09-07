#!/usr/bin/env bash
# Thin WRAP of GitHub Rulesets REST API.
# Gold shape: maplefukku/ZuruNote ruleset 18800881 (main-pr-only).
# Docs: https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset
# Usage: scripts/apply-main-pr-only-ruleset.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BODY="${ROOT}/scripts/main-pr-only-ruleset.json"
REPO="${GITHUB_REPOSITORY:-maplefukku/grok-bot-ops}"
NAME="main-pr-only"

if [[ ! -f "$BODY" ]]; then
  printf '%s\n' "missing ${BODY}" >&2
  exit 2
fi

existing="$(gh api "repos/${REPO}/rulesets" --jq ".[] | select(.name==\"${NAME}\") | .id")"
if [[ -n "$existing" ]]; then
  gh api --method PUT "repos/${REPO}/rulesets/${existing}" --input "$BODY"
else
  gh api --method POST "repos/${REPO}/rulesets" --input "$BODY"
fi

gh api --method PATCH "repos/${REPO}" --input - <<'JSON'
{
  "allow_auto_merge": true,
  "delete_branch_on_merge": true
}
JSON
