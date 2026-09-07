#!/usr/bin/env bash
# Repo WRAP of box SoT /workspace/fleet-scripts/merge-count-jst.sh
# (zn-merge-count-jst.sh is the ZuruNote sibling). gh pr list only.
# If the box script is executable, run it. Do not invent a second counter.
# Else run the embedded fleet body (same repos, same gh pr list, products.*.today).
# This file only reshapes to {day, by_repo, total} and applies the prior=0 need rule.
# Usage: scripts/merge-velocity-day.sh [YYYY-MM-DD] [prior-YYYY-MM-DD] [--hook]
set -euo pipefail
export MERGE_VELOCITY_SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
exec python3 - "$@" <<'PY'
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
REPOS = (
    "maplefukku/ZuruNote",
    "maplefukku/sauna-master",
    "maplefukku/gakuse-ai",
    "maplefukku/DevTogether",
    "maplefukku/grok-bot-ops",
)
BOX_DEFAULT = "/workspace/fleet-scripts/merge-count-jst.sh"


def short_name(full: str) -> str:
    return full.split("/", 1)[1]


def jst_day_of(iso: str) -> str:
    return (
        datetime.fromisoformat(iso.replace("Z", "+00:00"))
        .astimezone(JST)
        .date()
        .isoformat()
    )


def parse_argv(argv: list[str]) -> tuple[str | None, str | None, bool]:
    hook = False
    days: list[str] = []
    for arg in argv:
        if arg == "--hook":
            hook = True
        else:
            days.append(arg)
    return (days[0] if days else None, days[1] if len(days) > 1 else None, hook)


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


def embedded_fleet(day: str, prior_day: str) -> dict[str, object]:
    products: dict[str, dict[str, int]] = {}
    for full in REPOS:
        stamps = list_merged_at(full)
        products[short_name(full)] = {
            "today": count_on_day(stamps, day),
            "prior": count_on_day(stamps, prior_day),
        }
    return {"day": day, "prior_day": prior_day, "products": products}


def box_path() -> Path:
    return Path(os.environ.get("MERGE_COUNT_JST", BOX_DEFAULT))


def run_box(box: Path, argv: list[str]) -> dict[str, object]:
    proc = subprocess.run(
        [str(box), *argv],
        check=True,
        capture_output=True,
        text=True,
    )
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return json.loads(proc.stdout)


def fleet_payload(day: str, prior_day: str, fleet_argv: list[str]) -> dict[str, object]:
    box = box_path()
    self = Path(os.environ.get("MERGE_VELOCITY_SELF", ""))
    try:
        same = box.resolve() == self.resolve()
    except OSError:
        same = False
    if box.is_file() and os.access(box, os.X_OK) and not same:
        return run_box(box, fleet_argv)
    return embedded_fleet(day, prior_day)


def product_node(products: object, full: str) -> object:
    if not isinstance(products, dict):
        return {}
    node = products.get(full)
    if node is None:
        node = products.get(short_name(full))
    return {} if node is None else node


def node_int(node: object, key: str) -> int:
    if isinstance(node, int):
        return node if key == "today" else 0
    if isinstance(node, dict):
        raw = node.get(key, 0)
        return int(raw or 0)
    return 0


def reshape(raw: dict[str, object], day: str, prior_day: str) -> dict[str, object]:
    out_day = str(raw.get("day") or day)
    out_prior_day = str(raw.get("prior_day") or prior_day)
    by_repo: dict[str, int] = {}
    src_by = raw.get("by_repo")
    products = raw.get("products")
    if isinstance(src_by, dict) and src_by:
        for full in REPOS:
            by_repo[full] = int(src_by.get(full, 0) or 0)
    else:
        for full in REPOS:
            by_repo[full] = node_int(product_node(products, full), "today")
    total_raw = raw.get("total")
    if isinstance(total_raw, int):
        total = total_raw
    elif isinstance(total_raw, dict):
        total = int(total_raw.get("today") or 0)
    else:
        total = sum(by_repo.values())
    if isinstance(raw.get("prior"), int):
        prior = int(raw["prior"])
    elif isinstance(total_raw, dict):
        prior = int(total_raw.get("prior") or 0)
    else:
        prior = 0
        for full in REPOS:
            prior += node_int(product_node(products, full), "prior")
    need = 1 if prior == 0 else prior * 2
    return {
        "day": out_day,
        "prior_day": out_prior_day,
        "by_repo": by_repo,
        "total": total,
        "prior": prior,
        "need_2x": need,
        "pass": total >= need,
    }


def main(argv: list[str]) -> int:
    day_arg, prior_arg, hook = parse_argv(argv)
    day = day_arg or today_jst()
    prior_day = prior_arg or prior_of(day)
    fleet_argv = [a for a in argv if a != "--hook"]
    raw = fleet_payload(day, prior_day, fleet_argv)
    payload = reshape(raw, day, prior_day)
    print(json.dumps(payload, separators=(",", ":")))
    if hook and not payload["pass"]:
        print("ACCELERATE", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
PY
