#!/usr/bin/env python3
from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Literal


def normalize_source_url(url: str) -> str:
    return url.strip().rstrip("/")


@dataclass(frozen=True)
class ApplyResult:
    kind: Literal["accepted", "skipped"]
    rows: list[dict]
    existing: dict | None


def apply_candidate(rows: list[dict], candidate: dict) -> ApplyResult:
    key = normalize_source_url(str(candidate.get("source_url") or ""))
    out = [copy(row) for row in rows]
    if not key:
        return ApplyResult(kind="skipped", rows=out, existing=None)
    for row in out:
        row_key = normalize_source_url(str(row.get("source_url") or ""))
        if row_key == key:
            return ApplyResult(kind="skipped", rows=out, existing=row)
    new_row = copy(candidate)
    return ApplyResult(kind="accepted", rows=out + [new_row], existing=new_row)
