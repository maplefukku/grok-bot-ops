#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ci import trend_log_errors  # noqa: E402
from intent_memory.trend_log import DecisionRow, iter_trend_log_rows  # noqa: E402
from trend_adopt_idempotency import (  # noqa: E402
    apply_candidate,
    normalize_source_url,
)

TREND_LOG = _ROOT / "docs" / "decisions" / "trend-log.md"


def _snapshot(rows: list[dict]) -> list[dict]:
    return [dict(row) for row in rows]


def _ledger_row(row: DecisionRow) -> dict[str, str]:
    return {
        "date_jst": row.date_jst,
        "source_bot": row.source_bot,
        "title": row.title,
        "source_url": row.source_url,
        "decision": row.decision,
        "理由": row.reason,
        "route": row.route,
        "fired": row.fired,
    }


class TrendAdoptIdempotencyTests(unittest.TestCase):
    def _assert_pure(self, rows: list[dict], result) -> None:
        before_id = id(rows)
        before = _snapshot(rows)
        self.assertIsNot(result.rows, rows)
        self.assertEqual(id(rows), before_id)
        self.assertEqual(_snapshot(rows), before)
        if rows and result.rows:
            self.assertIsNot(result.rows[0], rows[0])

    def test_given_empty_ledger_when_apply_first_candidate_then_accepted_one_row(self) -> None:
        rows: list[dict] = []
        candidate = {"source_url": "https://example.com/first"}
        before = _snapshot(rows)
        result = apply_candidate(rows, candidate)
        self._assert_pure(rows, result)
        self.assertEqual(_snapshot(rows), before)
        self.assertEqual(result.kind, "accepted")
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(result.rows[0]["source_url"], "https://example.com/first")
        self.assertIs(result.existing, result.rows[0])
        self.assertNotIn("fired", result.existing)

    def test_given_existing_row_when_apply_same_url_opposite_decision_then_skipped_no_merge(
        self,
    ) -> None:
        rows = [
            {
                "source_url": "https://example.com/keep",
                "decision": "ADOPT",
                "理由": "keep this reason",
            }
        ]
        candidate = {
            "source_url": "https://example.com/keep",
            "decision": "REJECT",
            "理由": "overwrite me",
            "title": "other title",
        }
        before = _snapshot(rows)
        result = apply_candidate(rows, candidate)
        self._assert_pure(rows, result)
        self.assertEqual(result.kind, "skipped")
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(result.existing["decision"], "ADOPT")
        self.assertEqual(result.existing["理由"], "keep this reason")
        self.assertEqual(result.rows[0]["decision"], "ADOPT")
        self.assertEqual(result.rows[0]["理由"], "keep this reason")
        self.assertEqual(_snapshot(rows), before)
        self.assertNotEqual(result.existing.get("理由"), candidate["理由"])

    def test_given_existing_dup_when_apply_trailing_slash_or_padded_url_then_skipped(
        self,
    ) -> None:
        rows = [{"source_url": "https://example.com/dup"}]
        slash = apply_candidate(rows, {"source_url": "https://example.com/dup/"})
        padded = apply_candidate(
            rows, {"source_url": "  https://example.com/dup/  "}
        )
        self._assert_pure(rows, slash)
        self.assertEqual(slash.kind, "skipped")
        self.assertEqual(padded.kind, "skipped")
        self.assertEqual(len(slash.rows), 1)
        self.assertEqual(len(padded.rows), 1)
        self.assertEqual(
            normalize_source_url("https://example.com/dup/"),
            "https://example.com/dup",
        )
        self.assertEqual(
            normalize_source_url("  https://example.com/dup/  "),
            "https://example.com/dup",
        )

    def test_given_same_new_candidate_applied_twice_then_one_row_second_skipped(
        self,
    ) -> None:
        candidate = {"source_url": "https://example.com/once"}
        first = apply_candidate([], candidate)
        second = apply_candidate(first.rows, candidate)
        self.assertEqual(first.kind, "accepted")
        self.assertEqual(second.kind, "skipped")
        self.assertEqual(len(first.rows), 1)
        self.assertEqual(len(second.rows), 1)
        self.assertEqual(
            [row["source_url"] for row in second.rows],
            ["https://example.com/once"],
        )
        self.assertEqual(_snapshot(first.rows), _snapshot(second.rows))

    def test_given_ledger_already_has_row_when_retry_apply_then_skipped_not_added(
        self,
    ) -> None:
        rows = [{"source_url": "https://example.com/crash-after-write", "decision": "REJECT"}]
        result = apply_candidate(
            rows,
            {
                "source_url": "https://example.com/crash-after-write",
                "decision": "ADOPT",
            },
        )
        self._assert_pure(rows, result)
        self.assertEqual(result.kind, "skipped")
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(result.existing["decision"], "REJECT")

    def test_given_two_different_urls_when_each_applied_then_two_rows_both_accepted(
        self,
    ) -> None:
        empty: list[dict] = []
        first = apply_candidate(empty, {"source_url": "https://example.com/a"})
        second = apply_candidate(first.rows, {"source_url": "https://example.com/b"})
        self.assertEqual(first.kind, "accepted")
        self.assertEqual(second.kind, "accepted")
        self.assertEqual(len(second.rows), 2)
        self.assertEqual(
            [row["source_url"] for row in second.rows],
            ["https://example.com/a", "https://example.com/b"],
        )

    def test_given_existing_empty_fired_when_candidate_has_job_url_then_fired_stays_empty(
        self,
    ) -> None:
        rows = [
            {
                "source_url": "https://example.com/hold",
                "decision": "ADOPT",
                "理由": "park",
                "fired": "",
            }
        ]
        candidate = {
            "source_url": "https://example.com/hold",
            "decision": "ADOPT",
            "理由": "park",
            "fired": "https://cursor.com/agents/JOB123",
        }
        result = apply_candidate(rows, candidate)
        self._assert_pure(rows, result)
        self.assertEqual(result.kind, "skipped")
        self.assertEqual(result.existing["fired"], "")
        self.assertEqual(result.rows[0]["fired"], "")
        self.assertEqual(rows[0]["fired"], "")

    def test_given_live_trend_log_when_each_row_applied_again_then_skipped_fixed_point(
        self,
    ) -> None:
        text = TREND_LOG.read_text(encoding="utf-8")
        live = iter_trend_log_rows(text)
        ledger = [_ledger_row(row) for row in live]
        count = len(ledger)
        self.assertGreater(count, 0)
        keys_before = [normalize_source_url(row["source_url"]) for row in ledger]
        current = ledger
        for row in live:
            result = apply_candidate(current, _ledger_row(row))
            self.assertEqual(result.kind, "skipped")
            self.assertEqual(len(result.rows), count)
            current = result.rows
        keys_after = [normalize_source_url(row["source_url"]) for row in current]
        self.assertEqual(keys_after, keys_before)
        self.assertEqual(len(current), count)

    def test_given_trailing_slash_pair_when_trend_log_errors_then_duplicate_source_url(
        self,
    ) -> None:
        snippet = (
            "## 判断記録\n"
            "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| 2026-09-05 | 最先端手法 | t1 | https://example.com/dup | ADOPT | one | ops |  |\n"
            "| 2026-09-05 | Knowhow収集 | t2 | https://example.com/dup/ | REJECT | two | none |  |\n"
        )
        found = trend_log_errors(snippet)
        blob = "\n".join(found)
        self.assertTrue(any("duplicate source_url" in item for item in found), blob)

    def test_given_empty_source_url_when_apply_then_skipped_ledger_unchanged(self) -> None:
        rows = [{"source_url": "https://example.com/kept"}]
        before = _snapshot(rows)
        result = apply_candidate(rows, {"source_url": ""})
        self._assert_pure(rows, result)
        self.assertEqual(result.kind, "skipped")
        self.assertIsNone(result.existing)
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(_snapshot(result.rows), before)
        self.assertEqual(_snapshot(rows), before)


if __name__ == "__main__":
    unittest.main()
