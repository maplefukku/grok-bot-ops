#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory import IngestOff, MemoryStore
from intent_memory.trend_log import (
    drafts_from_trend_log,
    iter_trend_log_rows,
    normalize_source_url,
    trend_log_errors,
)

ROOT = Path(__file__).resolve().parents[1]
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"
ADR_0002 = ROOT / "docs" / "decisions" / "0002-trend-adopt-loop.md"
ROUTINE = ROOT / "routines" / "decide-trend-adopt.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
PRECHECK_PAGE = ROOT / "docs" / "process" / "marketplace-precheck.md"
CBO = ROOT / "bots" / "CBO.md"
BOTS_README = ROOT / "bots" / "README.md"
MARKETPLACE_ADOPT_URL = "https://x.ai/news/grok-bot-procurement"

PRECHECK_PAGE_NEEDLES = (
    "https://x.ai/bot/marketplace",
    MARKETPLACE_ADOPT_URL,
    "export-bot-template",
    "CreateAgent NONE",
    "KEEP",
    "WRAP",
    "/poteto-mode",
    "sand-workflow:parallel-fire-fleet",
    "sand-workflow:cloud",
    "tool-path-prefer",
    "quiet-test.sh",
    "templates.md",
    "issues/92",
    "Haggle",
)
PRECHECK_POINTER_NEEDLES = ("marketplace-precheck.md",)
PARSER_MUST_FAIL_WITHOUT = (
    "https://x.ai/bot/marketplace",
    "export-bot-template",
    "CreateAgent NONE",
    "issues/92",
    "sand-workflow:cloud",
)
COMPLETE_PRECHECK_FIXTURE = "\n".join(PRECHECK_PAGE_NEEDLES) + "\n"


def precheck_page_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PRECHECK_PAGE_NEEDLES if needle not in text]


def precheck_pointer_errors(text: str) -> list[str]:
    return [
        f"missing {needle}" for needle in PRECHECK_POINTER_NEEDLES if needle not in text
    ]

HEADER = (
    "## 判断記録\n"
    "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
)


class TestTrendLogErrors(unittest.TestCase):
    def test_given_valid_adopt_row_when_errors_then_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | 最先端手法 | ok | https://example.com/ok | ADOPT | because | ops |  |\n"
        )
        self.assertEqual(trend_log_errors(text), [])

    def test_given_watch_decision_when_errors_then_decision(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | https://example.com/b | WATCH | has reason | none |  |\n"
        )
        self.assertIn("decision", "\n".join(trend_log_errors(text)))

    def test_given_empty_reason_when_errors_then_reason(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | https://example.com/a | REJECT |  | none |  |\n"
        )
        self.assertIn("理由", "\n".join(trend_log_errors(text)))

    def test_given_non_http_url_when_errors_then_http(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | not-a-url | REJECT | has reason | none |  |\n"
        )
        self.assertIn("http", "\n".join(trend_log_errors(text)))

    def test_given_trailing_slash_dup_when_errors_then_source_url(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | 最先端手法 | t1 | https://example.com/dup | ADOPT | one | ops |  |\n"
            "| 2026-09-05 | Knowhow収集 | t2 | https://example.com/dup/ | REJECT | two | none |  |\n"
        )
        self.assertIn("source_url", "\n".join(trend_log_errors(text)))

    def test_given_table_outside_section_when_errors_then_missing_section_only(
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

    def test_given_section_without_table_when_errors_then_decision_table(
        self,
    ) -> None:
        self.assertIn(
            "decision table",
            "\n".join(trend_log_errors("## 判断記録\n\nno table\n")),
        )

    def test_given_live_trend_log_when_errors_then_empty(self) -> None:
        self.assertEqual(trend_log_errors(TREND_LOG.read_text(encoding="utf-8")), [])

    def test_given_spaced_trailing_slash_when_normalize_then_stripped(self) -> None:
        self.assertEqual(
            normalize_source_url(" https://example.com/x/ "),
            "https://example.com/x",
        )


class TestTrendLogDryRun(unittest.TestCase):
    def test_given_live_rows_when_append_then_ingest_off(self) -> None:
        drafts = drafts_from_trend_log(TREND_LOG.read_text(encoding="utf-8"))
        self.assertTrue(drafts)
        store = MemoryStore()
        for draft in drafts:
            self.assertEqual(draft.actor, "bot:Planner")
            with self.assertRaises(IngestOff):
                store.append(draft)


class TestTrendLogHitlKeep(unittest.TestCase):
    def test_given_manuscripts_then_soft_hold_needles_present(self) -> None:
        adr = ADR_0002.read_text(encoding="utf-8")
        routine = ROUTINE.read_text(encoding="utf-8")
        log = TREND_LOG.read_text(encoding="utf-8")
        self.assertIn("ボットは行をマージしない", adr)
        self.assertIn("WATCH 列は置かない", adr)
        self.assertIn("CreateAgent は使わない", adr)
        self.assertIn("Never FIRE. Never implement. No Discord writeback.", routine)
        self.assertIn("保留は WATCH にしない", log)


class TestMarketplacePrecheckWrap(unittest.TestCase):
    def test_given_live_page_when_needles_then_empty(self) -> None:
        self.assertTrue(PRECHECK_PAGE.is_file(), "docs/process/marketplace-precheck.md")
        self.assertEqual(
            precheck_page_errors(PRECHECK_PAGE.read_text(encoding="utf-8")),
            [],
        )

    def test_given_process_readme_when_linked_then_precheck_path_present(self) -> None:
        self.assertEqual(
            precheck_pointer_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_cbo_when_read_then_precheck_path_present(self) -> None:
        self.assertEqual(
            precheck_pointer_errors(CBO.read_text(encoding="utf-8")),
            [],
        )

    def test_given_bots_readme_when_read_then_precheck_path_present(self) -> None:
        self.assertEqual(
            precheck_pointer_errors(BOTS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(precheck_page_errors(COMPLETE_PRECHECK_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_PRECHECK_FIXTURE.replace(token, "")
                found = precheck_page_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
