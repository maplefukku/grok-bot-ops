#!/usr/bin/env bash
set -euo pipefail

REPOS=(
  maplefukku/ZuruNote
  maplefukku/sauna-master
  maplefukku/gakuse-ai
  maplefukku/DevTogether
  maplefukku/grok-bot-ops
)

DAY="${1:-}"
PRIOR_DAY="${2:-}"
if [[ -z "$DAY" ]]; then
  DAY="$(TZ=Asia/Tokyo date +%F)"
fi
if [[ -z "$PRIOR_DAY" ]]; then
  PRIOR_DAY="$(TZ=Asia/Tokyo date -d "${DAY} -1 day" +%F)"
fi

LIMIT=100
search_start="$(TZ=UTC date -d "${PRIOR_DAY}T00:00:00+09:00" +%F)"
search_end="$(TZ=UTC date -d "${DAY}T23:59:59+09:00" +%F)"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

index="$tmp/index.tsv"
: >"$index"
for repo in "${REPOS[@]}"; do
  out="$tmp/${repo//\//__}.json"
  gh pr list --repo "$repo" --state merged --limit "$LIMIT" \
    --search "merged:${search_start}..${search_end}" \
    --json number,mergedAt >"$out"
  printf '%s\t%s\n' "$repo" "$out" >>"$index"
done

DAY="$DAY" PRIOR_DAY="$PRIOR_DAY" INDEX="$index" LIMIT="$LIMIT" python3 - <<'PY'
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
REPOS = (
    "maplefukku/ZuruNote",
    "maplefukku/sauna-master",
    "maplefukku/gakuse-ai",
    "maplefukku/DevTogether",
    "maplefukku/grok-bot-ops",
)


def parse_day(raw: str) -> datetime:
    try:
        parsed = datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        raise SystemExit(f"day must be YYYY-MM-DD, got {raw!r}") from None
    return parsed.replace(tzinfo=JST)


def window(day: datetime) -> tuple[datetime, datetime]:
    start = day.astimezone(timezone.utc)
    end = (day + timedelta(days=1)).astimezone(timezone.utc)
    return start, end


def parse_merged_at(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw:
        return None
    text = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        ts = datetime.fromisoformat(text)
    except ValueError:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc)


def count_in_window(items: object, start: datetime, end: datetime) -> int:
    if not isinstance(items, list):
        raise SystemExit("gh pr list JSON must be an array")
    n = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        ts = parse_merged_at(item.get("mergedAt"))
        if ts is None:
            continue
        if start <= ts < end:
            n += 1
    return n


day = parse_day(os.environ["DAY"])
prior_day = parse_day(os.environ["PRIOR_DAY"])
today_start, today_end = window(day)
prior_start, prior_end = window(prior_day)

by_path: dict[str, Path] = {}
for line in Path(os.environ["INDEX"]).read_text(encoding="utf-8").splitlines():
    repo, path = line.split("\t", 1)
    by_path[repo] = Path(path)

limit = int(os.environ["LIMIT"])
by_repo: dict[str, int] = {}
prior_by_repo: dict[str, int] = {}
for repo in REPOS:
    path = by_path.get(repo)
    if path is None:
        raise SystemExit(f"missing gh dump for {repo}")
    items = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(items, list) and len(items) >= limit:
        raise SystemExit(
            f"{repo}: gh pr list hit --limit {limit}; merge window is incomplete"
        )
    by_repo[repo] = count_in_window(items, today_start, today_end)
    prior_by_repo[repo] = count_in_window(items, prior_start, prior_end)

total = sum(by_repo.values())
prior = sum(prior_by_repo.values())
need_2x = 1 if prior == 0 else prior * 2
report = {
    "day": day.date().isoformat(),
    "by_repo": by_repo,
    "total": total,
    "prior": prior,
    "need_2x": need_2x,
    "pass": total >= need_2x,
}
json.dump(report, sys.stdout, ensure_ascii=False)
sys.stdout.write("\n")
PY
