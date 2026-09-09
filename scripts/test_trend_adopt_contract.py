#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from trend_adopt_contract import (
    normalize_source_url,
    parser_self_check,
    trend_log_errors,
)

ROOT = Path(__file__).resolve().parents[1]
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"
ADR_0002 = ROOT / "docs" / "decisions" / "0002-trend-adopt-loop.md"
ROUTINE = ROOT / "routines" / "decide-trend-adopt.md"

HEADER = (
    "## 判断記録\n"
    "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
)


class TestTrendAdoptContract(unittest.TestCase):
    def test_given_valid_adopt_row_under_judgement_when_trend_log_errors_then_empty(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-05 | 最先端手法 | ok | https://example.com/ok | ADOPT | because | ops |  |\n"
        )
        self.assertEqual(trend_log_errors(text), [])

    def test_given_decision_watch_when_trend_log_errors_then_contains_decision(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | https://example.com/b | WATCH | has reason | none |  |\n"
        )
        blob = "\n".join(trend_log_errors(text))
        self.assertIn("decision", blob)

    def test_given_empty_reason_when_trend_log_errors_then_contains_reason(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | https://example.com/a | REJECT |  | none |  |\n"
        )
        blob = "\n".join(trend_log_errors(text))
        self.assertIn("理由", blob)

    def test_given_source_url_not_a_url_when_trend_log_errors_then_contains_http(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | not-a-url | REJECT | has reason | none |  |\n"
        )
        blob = "\n".join(trend_log_errors(text))
        self.assertIn("http", blob)

    def test_given_urls_differing_by_trailing_slash_when_trend_log_errors_then_source_url(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-05 | 最先端手法 | t1 | https://example.com/dup | ADOPT | one | ops |  |\n"
            "| 2026-09-05 | Knowhow収集 | t2 | https://example.com/dup/ | REJECT | two | none |  |\n"
        )
        blob = "\n".join(trend_log_errors(text))
        self.assertIn("source_url", blob)

    def test_given_watch_table_outside_judgement_and_no_section_when_trend_log_errors_then_section_only(
        self,
    ) -> None:
        text = (
            "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| 2026-09-05 | 最先端手法 | x | https://example.com/out | WATCH |  | none |  |\n"
        )
        blob = "\n".join(trend_log_errors(text))
        self.assertNotIn("WATCH", blob)
        self.assertNotIn("empty 理由", blob)
        self.assertIn("判断記録", blob)

    def test_given_judgement_section_with_no_table_when_trend_log_errors_then_decision_table(
        self,
    ) -> None:
        blob = "\n".join(trend_log_errors("## 判断記録\n\nno table\n"))
        self.assertIn("decision table", blob)

    def test_given_live_trend_log_when_trend_log_errors_then_empty(self) -> None:
        text = TREND_LOG.read_text(encoding="utf-8")
        self.assertEqual(trend_log_errors(text), [])

    def test_given_parser_self_check_then_empty(self) -> None:
        self.assertEqual(parser_self_check(), [])

    def test_given_url_with_spaces_and_slash_when_normalize_then_stripped(
        self,
    ) -> None:
        self.assertEqual(
            normalize_source_url(" https://example.com/x/ "),
            "https://example.com/x",
        )

    def test_given_hitl_keep_manuscripts_then_needles_present(self) -> None:
        adr = ADR_0002.read_text(encoding="utf-8")
        routine = ROUTINE.read_text(encoding="utf-8")
        self.assertIn("マージしない", adr)
        self.assertIn("FIRE しない", adr)
        self.assertIn("WATCH", adr)
        self.assertIn("Do not merge", routine)
        self.assertIn("Never FIRE", routine)
        self.assertIn("No Discord writeback", routine)


if __name__ == "__main__":
    unittest.main()
