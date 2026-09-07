#!/usr/bin/env bash
# Repo SoT for daily merge velocity (JST) across five products.
# Wraps box /workspace/fleet-scripts/merge-count-jst.sh and zn-merge-count-jst.sh
# (gh pr list only). After land, those box scripts may call this path or stay sibling WRAP.
# Usage: scripts/merge-velocity-day.sh [YYYY-MM-DD] [prior-YYYY-MM-DD] [--hook]
set -euo pipefail

REPOS=(
  maplefukku/ZuruNote
  maplefukku/sauna-master
  maplefukku/gakuse-ai
  maplefukku/DevTogether
  maplefukku/grok-bot-ops
)

hook=0
day=""
prior=""
for arg in "$@"; do
  case "$arg" in
    --hook) hook=1 ;;
    --*)
      echo "unknown flag: $arg" >&2
      exit 2
      ;;
    *)
      if [[ -z "$day" ]]; then
        day=$arg
      elif [[ -z "$prior" ]]; then
        prior=$arg
      else
        echo "usage: scripts/merge-velocity-day.sh [YYYY-MM-DD] [prior-YYYY-MM-DD] [--hook]" >&2
        exit 2
      fi
      ;;
  esac
done

read -r day prior search_start search_end < <(
  python3 - "$day" "$prior" <<'PY'
from datetime import date, datetime, timedelta, timezone
import sys

JST = timezone(timedelta(hours=9))
day_s, prior_s = sys.argv[1], sys.argv[2]


def parse_day(label: str, raw: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise SystemExit(f"{label} must be YYYY-MM-DD") from exc


today = datetime.now(JST).date()
day = parse_day("day", day_s) if day_s else today
prior = parse_day("prior", prior_s) if prior_s else day - timedelta(days=1)
start = prior - timedelta(days=1)
end = day + timedelta(days=1)
print(day.isoformat(), prior.isoformat(), start.isoformat(), end.isoformat())
PY
)

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

for repo in "${REPOS[@]}"; do
  safe=${repo//\//__}
  gh pr list \
    --repo "$repo" \
    --state merged \
    --limit 100 \
    --json mergedAt \
    --search "merged:${search_start}..${search_end}" \
    >"$workdir/${safe}.json"
done

python3 - "$day" "$prior" "$hook" "$workdir" "${REPOS[@]}" <<'PY'
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
day, prior, hook = sys.argv[1], sys.argv[2], sys.argv[3]
workdir = Path(sys.argv[4])
repos = sys.argv[5:]


def jst_day(raw: object) -> str | None:
    if not raw:
        return None
    text = str(raw).replace("Z", "+00:00")
    stamp = datetime.fromisoformat(text)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(JST).date().isoformat()


def count_for(day_key: str, rows: list[object]) -> int:
    n = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        if jst_day(row.get("mergedAt")) == day_key:
            n += 1
    return n


by_repo: dict[str, int] = {}
prior_total = 0
for repo in repos:
    rows = json.loads((workdir / f"{repo.replace('/', '__')}.json").read_text())
    if not isinstance(rows, list):
        rows = []
    by_repo[repo] = count_for(day, rows)
    prior_total += count_for(prior, rows)

total = sum(by_repo.values())
need_2x = 1 if prior_total == 0 else prior_total * 2
passed = total >= need_2x
print(
    json.dumps(
        {
            "day": day,
            "prior_day": prior,
            "by_repo": by_repo,
            "total": total,
            "prior": prior_total,
            "need_2x": need_2x,
            "pass": passed,
        },
        ensure_ascii=False,
    )
)
if hook == "1" and not passed:
    print(
        f"ACCELERATE day={day} total={total} need_2x={need_2x} prior={prior_total}",
        file=sys.stderr,
    )
PY
