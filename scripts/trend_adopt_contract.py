#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass

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
HTTP_RE = re.compile(r"https?://[^\s)>\]]+")


@dataclass(frozen=True)
class DecisionRow:
    date_jst: str
    source_bot: str
    title: str
    source_url: str
    decision: str
    理由: str
    route: str
    fired: str


def normalize_source_url(url: str) -> str:
    return url.strip().rstrip("/")


def _cell(cells: list[str], index: dict[str, int], name: str) -> str:
    pos = index.get(name)
    if pos is None or pos >= len(cells):
        return ""
    return cells[pos]


def _walk_decision_tables(
    text: str,
) -> tuple[bool, bool, list[tuple[str, DecisionRow]]]:
    found_section = False
    found_header = False
    in_section = False
    in_table = False
    index: dict[str, int] = {}
    rows: list[tuple[str, DecisionRow]] = []
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
            (
                line,
                DecisionRow(
                    date_jst=_cell(cells, index, "date_jst"),
                    source_bot=_cell(cells, index, "source_bot"),
                    title=_cell(cells, index, "title"),
                    source_url=_cell(cells, index, "source_url"),
                    decision=_cell(cells, index, "decision"),
                    理由=_cell(cells, index, "理由"),
                    route=_cell(cells, index, "route"),
                    fired=_cell(cells, index, "fired"),
                ),
            )
        )
    return found_section, found_header, rows


def iter_decision_rows(text: str) -> list[DecisionRow]:
    _, _, items = _walk_decision_tables(text)
    return [row for _, row in items]


def trend_log_errors(text: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    found_section, found_header, items = _walk_decision_tables(text)
    for line, row in items:
        if row.decision not in {"ADOPT", "REJECT"}:
            errors.append(f"decision must be ADOPT or REJECT: {line}")
        if not row.理由:
            errors.append(f"empty 理由: {line}")
        if not HTTP_RE.search(row.source_url):
            errors.append(f"source_url must match https?://: {line}")
        key = normalize_source_url(row.source_url)
        if key:
            if key in seen:
                errors.append(f"duplicate source_url: {line}")
            else:
                seen.add(key)
    if not found_section:
        errors.append("missing ## 判断記録")
    elif not found_header:
        errors.append("## 判断記録 has no decision table")
    return errors


def parser_self_check() -> list[str]:
    errors: list[str] = []
    header = (
        "## 判断記録\n"
        "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )
    valid = header + (
        "| 2026-09-05 | 最先端手法 | ok | https://example.com/ok | ADOPT | because | ops |  |\n"
    )
    if trend_log_errors(valid):
        errors.append("trend-log parser self-check: valid row produced errors")
    outside = (
        "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | 最先端手法 | x | https://example.com/out | WATCH |  | none |  |\n"
    )
    outside_err = "\n".join(trend_log_errors(outside))
    if "WATCH" in outside_err or "empty 理由" in outside_err:
        errors.append(
            "trend-log parser self-check: table outside 判断記録 was parsed"
        )
    if "判断記録" not in outside_err:
        errors.append(
            "trend-log parser self-check: missing ## 判断記録 was accepted"
        )
    empty_section = "## 判断記録\n\nno table\n"
    empty_err = "\n".join(trend_log_errors(empty_section))
    if "decision table" not in empty_err:
        errors.append(
            "trend-log parser self-check: empty 判断記録 was accepted"
        )
    cases = (
        (
            "missing 理由",
            header
            + "| 2026-09-05 | Knowhow収集 | t | https://example.com/a | REJECT |  | none |  |\n",
            "理由",
        ),
        (
            "illegal decision",
            header
            + "| 2026-09-05 | Knowhow収集 | t | https://example.com/b | WATCH | has reason | none |  |\n",
            "decision",
        ),
        (
            "non-http url",
            header
            + "| 2026-09-05 | Knowhow収集 | t | not-a-url | REJECT | has reason | none |  |\n",
            "http",
        ),
        (
            "duplicate source_url",
            header
            + "| 2026-09-05 | 最先端手法 | t1 | https://example.com/dup | ADOPT | one | ops |  |\n"
            + "| 2026-09-05 | Knowhow収集 | t2 | https://example.com/dup/ | REJECT | two | none |  |\n",
            "source_url",
        ),
    )
    for name, snippet, needle in cases:
        found = trend_log_errors(snippet)
        if not found:
            errors.append(f"trend-log parser self-check missed {name}")
            continue
        blob = "\n".join(found)
        if needle not in blob:
            errors.append(
                f"trend-log parser self-check: {name} errors omitted {needle}"
            )
    return errors
