#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory.contract import AtomDraft, Kind, Source

JST = ZoneInfo("Asia/Tokyo")
TREND_HEADERS = (
    "date_jst",
    "source_bot",
    "title",
    "source_url",
    "decision",
    "理由",
    "route",
    "fired",
)


def iter_trend_log_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_section = False
    in_table = False
    index: dict[str, int] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip() == "判断記録"
            in_table = False
            index = {}
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and all(c and set(c) <= {"-", ":"} for c in cells):
            continue
        labels = set(cells)
        if set(TREND_HEADERS) <= labels:
            index = {name: cells.index(name) for name in TREND_HEADERS}
            in_table = True
            continue
        if not in_table:
            continue
        row = {}
        for name in TREND_HEADERS:
            pos = index[name]
            row[name] = cells[pos] if pos < len(cells) else ""
        rows.append(row)
    return rows


def draft_from_trend_row(row: dict[str, str]) -> AtomDraft:
    decision = row["decision"]
    route = row["route"] or "none"
    source_bot = row["source_bot"]
    source_url = row["source_url"].strip()
    fired = row["fired"].strip()
    created = datetime.strptime(row["date_jst"], "%Y-%m-%d").replace(tzinfo=JST)
    body = "\n".join(
        (
            row["理由"],
            f"source_url: {source_url}",
            f"fired: {fired}",
        )
    )
    return AtomDraft(
        kind=Kind.DECISION,
        source=Source.BOT,
        actor="bot:Planner",
        tags=(
            "trend-adopt",
            f"decision:{decision}",
            f"route:{route}",
            f"source_bot:{source_bot}",
        ),
        body=body,
        source_url=source_url,
        created_at=created,
        expires_at=None,
    )


def drafts_from_trend_log(text: str) -> list[AtomDraft]:
    return [draft_from_trend_row(row) for row in iter_trend_log_rows(text)]


def _draft_dict(draft: AtomDraft) -> dict:
    return {
        "kind": draft.kind.value,
        "source": draft.source.value,
        "tags": list(draft.tags),
        "body": draft.body,
        "actor": draft.actor,
        "related_ids": list(draft.related_ids),
        "source_url": draft.source_url,
        "github_url": draft.github_url,
        "gb_url": draft.gb_url,
        "created_at": draft.created_at.isoformat() if draft.created_at else None,
        "expires_at": draft.expires_at.isoformat() if draft.expires_at else None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run map trend-log rows to intent_atom drafts"
    )
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("docs/decisions/trend-log.md"),
    )
    args = parser.parse_args(argv)
    drafts = drafts_from_trend_log(args.path.read_text(encoding="utf-8"))
    json.dump(
        [_draft_dict(draft) for draft in drafts],
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
