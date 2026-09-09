#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory.contract import AtomDraft, Kind, Source
from trend_adopt_contract import TREND_HEADERS, DecisionRow, iter_decision_rows

JST = ZoneInfo("Asia/Tokyo")


def iter_trend_log_rows(text: str) -> list[dict[str, str]]:
    return [asdict(row) for row in iter_decision_rows(text)]


def draft_from_trend_row(row: dict[str, str] | DecisionRow) -> AtomDraft:
    data = asdict(row) if isinstance(row, DecisionRow) else row
    decision = data["decision"]
    route = data["route"] or "none"
    source_bot = data["source_bot"]
    source_url = data["source_url"].strip()
    fired = data["fired"].strip()
    created = datetime.strptime(data["date_jst"], "%Y-%m-%d").replace(tzinfo=JST)
    body = "\n".join(
        (
            data["理由"],
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
    return [draft_from_trend_row(row) for row in iter_decision_rows(text)]


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
