#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
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
_HEADER_NEEDLES = frozenset({"decision", "source_url", "理由"})
_HTTP_RE = re.compile(r"https?://[^\s)>\]]+")


@dataclass(frozen=True)
class DecisionRow:
    date_jst: str
    source_bot: str
    title: str
    source_url: str
    decision: str
    reason: str
    route: str
    fired: str
    line: str


def normalize_source_url(url: str) -> str:
    return url.strip().rstrip("/")


def _cell(cells: list[str], index: dict[str, int], name: str) -> str:
    pos = index.get(name)
    if pos is None or pos >= len(cells):
        return ""
    return cells[pos]


def _walk_decision_tables(
    text: str,
) -> tuple[bool, bool, list[DecisionRow]]:
    found_section = False
    found_header = False
    in_section = False
    in_table = False
    index: dict[str, int] = {}
    rows: list[DecisionRow] = []
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip() == "判断記録"
            in_table = False
            index = {}
            if in_section:
                found_section = True
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and all(c and set(c) <= {"-", ":"} for c in cells):
            continue
        labels = set(cells)
        if _HEADER_NEEDLES <= labels:
            index = {name: cells.index(name) for name in TREND_HEADERS if name in cells}
            in_table = True
            found_header = True
            continue
        if not in_table:
            continue
        rows.append(
            DecisionRow(
                date_jst=_cell(cells, index, "date_jst"),
                source_bot=_cell(cells, index, "source_bot"),
                title=_cell(cells, index, "title"),
                source_url=_cell(cells, index, "source_url"),
                decision=_cell(cells, index, "decision"),
                reason=_cell(cells, index, "理由"),
                route=_cell(cells, index, "route"),
                fired=_cell(cells, index, "fired"),
                line=line,
            )
        )
    return found_section, found_header, rows


def iter_trend_log_rows(text: str) -> list[DecisionRow]:
    _, _, rows = _walk_decision_tables(text)
    return rows


def trend_log_errors(text: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    found_section, found_header, rows = _walk_decision_tables(text)
    for row in rows:
        if row.decision not in {"ADOPT", "REJECT"}:
            errors.append(f"decision must be ADOPT or REJECT: {row.line}")
        if not row.reason:
            errors.append(f"empty 理由: {row.line}")
        if not _HTTP_RE.search(row.source_url):
            errors.append(f"source_url must match https?://: {row.line}")
        key = normalize_source_url(row.source_url)
        if key:
            if key in seen:
                errors.append(f"duplicate source_url: {row.line}")
            else:
                seen.add(key)
    if not found_section:
        errors.append("missing ## 判断記録")
    elif not found_header:
        errors.append("## 判断記録 has no decision table")
    return errors


def draft_from_trend_row(row: DecisionRow) -> AtomDraft:
    route = row.route or "none"
    source_url = row.source_url.strip()
    fired = row.fired.strip()
    created = datetime.strptime(row.date_jst, "%Y-%m-%d").replace(tzinfo=JST)
    body = "\n".join(
        (
            row.reason,
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
            f"decision:{row.decision}",
            f"route:{route}",
            f"source_bot:{row.source_bot}",
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
