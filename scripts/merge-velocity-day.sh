#!/usr/bin/env bash
# This path is the repo SoT for units merged / JST day.
# WRAP of box /workspace/fleet-scripts/merge-count-jst.sh + zn-merge-count-jst.sh (gh pr list only).
# Box may wrap/call this after land, or stay sibling WRAP.
set -euo pipefail
exec python3 - "$@" <<'PY'
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
REPOS = (
    "maplefukku/ZuruNote",
    "maplefukku/sauna-master",
    "maplefukku/gakuse-ai",
    "maplefukku/DevTogether",
    "maplefukku/grok-bot-ops",
)


def jst_day_of(iso: str) -> str:
    # UTC calendar date of mergedAt leaks neighbor days; 15:00Z is JST midnight.
    return (
        datetime.fromisoformat(iso.replace("Z", "+00:00"))
        .astimezone(JST)
        .date()
        .isoformat()
    )


def need_2x(prior: int) -> int:
    return 1 if prior == 0 else prior * 2


def parse_argv(argv: list[str]) -> tuple[str | None, str | None, bool]:
    hook = False
    days: list[str] = []
    for arg in argv:
        if arg == "--hook":
            hook = True
        else:
            days.append(arg)
    day = days[0] if days else None
    prior_day = days[1] if len(days) > 1 else None
    return day, prior_day, hook


def today_jst() -> str:
    return datetime.now(JST).date().isoformat()


def prior_of(day: str) -> str:
    return (datetime.fromisoformat(day).date() - timedelta(days=1)).isoformat()


def list_merged_at(repo: str) -> list[str]:
    proc = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "merged",
            "--json",
            "mergedAt",
            "--limit",
            "1000",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = json.loads(proc.stdout)
    return [row["mergedAt"] for row in rows if row.get("mergedAt")]


def count_on_day(merged_ats: list[str], day: str) -> int:
    return sum(1 for iso in merged_ats if jst_day_of(iso) == day)


def main(argv: list[str]) -> int:
    day_arg, prior_arg, hook = parse_argv(argv)
    day = day_arg or today_jst()
    prior_day = prior_arg or prior_of(day)
    by_repo: dict[str, int] = {}
    prior = 0
    for repo in REPOS:
        stamps = list_merged_at(repo)
        by_repo[repo] = count_on_day(stamps, day)
        prior += count_on_day(stamps, prior_day)
    total = sum(by_repo.values())
    need = need_2x(prior)
    payload = {
        "day": day,
        "prior_day": prior_day,
        "by_repo": by_repo,
        "total": total,
        "prior": prior,
        "need_2x": need,
        "pass": total >= need,
    }
    print(json.dumps(payload, separators=(",", ":")))
    if hook and not payload["pass"]:
        print("ACCELERATE", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
PY
