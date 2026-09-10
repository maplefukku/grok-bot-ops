#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory.trend_log import (
    DecisionRow,
    iter_trend_log_rows,
    normalize_source_url,
    trend_log_errors,
)

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "trend-adopt-reject.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
PLANNER = ROOT / "bots" / "Planner.md"
BOTS_README = ROOT / "bots" / "README.md"
ADR_0002 = ROOT / "docs" / "decisions" / "0002-trend-adopt-loop.md"
ROUTINE = ROOT / "routines" / "decide-trend-adopt.md"
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"

ISSUE_URL = "https://github.com/maplefukku/grok-bot-ops/issues/117"
ISSUE_19_URL = "https://github.com/maplefukku/grok-bot-ops/issues/19"
LOCK_COMMENT = "issues/19#issuecomment-5543826572"
SCAFFOLD_REJECT_URL = ISSUE_19_URL

PAGE_NEEDLES: tuple[str, ...] = (
    "REJECT",
    "ADOPT",
    "WATCH",
    "証拠不足",
    "再浮上",
    "source_url",
    "dedup",
    "先勝ち",
    "ボットは行をマージしない",
    "Never FIRE",
    "CreateAgent NONE",
    "decide-trend-adopt.md",
    "0002-trend-adopt-loop.md",
    "trend_log.py",
    "trend_adopt_idempotency.py",
    "sand-workflow:parallel-fire-fleet",
    "sand-workflow:cloud",
    "tool-path-prefer",
    "poteto-mode",
    "quiet-test.sh",
    "Quiet is not skip",
    "test_trend_adopt_reject_lock.py",
    ISSUE_URL,
    LOCK_COMMENT,
)
PROCESS_README_NEEDLES: tuple[str, ...] = (
    "trend-adopt-reject.md",
    "issue 117",
    "REJECT",
)
PLANNER_NEEDLES: tuple[str, ...] = ("trend-adopt-reject.md",)
BOTS_README_NEEDLES: tuple[str, ...] = (
    "LOCK: TREND-ADOPT REJECT",
    "docs/process/trend-adopt-reject.md",
    "CreateAgent NONE",
)
FIRED_NEEDLES: tuple[str, ...] = (
    "trend-adopt-reject.md",
    "issues/117",
    "CreateAgent NONE",
)
PARSER_MUST_FAIL_WITHOUT: tuple[str, ...] = (
    "証拠不足",
    "WATCH",
    "CreateAgent NONE",
    "trend_adopt_idempotency.py",
    ISSUE_URL,
    "sand-workflow:cloud",
)

HEADER = (
    "## 判断記録\n"
    "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
)


def lock_errors(text: str, needles: tuple[str, ...] = PAGE_NEEDLES) -> list[str]:
    return [f"missing {needle}" for needle in needles if needle not in text]


def process_readme_errors(text: str) -> list[str]:
    return [
        f"missing {needle}"
        for needle in PROCESS_README_NEEDLES
        if needle not in text
    ]


def planner_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PLANNER_NEEDLES if needle not in text]


def bots_readme_errors(text: str) -> list[str]:
    return [
        f"missing {needle}" for needle in BOTS_README_NEEDLES if needle not in text
    ]


def _scaffold_reject_row(text: str) -> DecisionRow | None:
    for row in iter_trend_log_rows(text):
        if normalize_source_url(row.source_url) == normalize_source_url(SCAFFOLD_REJECT_URL):
            if row.decision == "REJECT":
                return row
    return None


def fired_errors(text: str) -> list[str]:
    errors: list[str] = []
    row = _scaffold_reject_row(text)
    if row is None:
        return ["missing scaffold REJECT row for issue 19"]
    fired = row.fired.strip()
    if not fired:
        errors.append("scaffold REJECT fired is empty")
        return errors
    for needle in FIRED_NEEDLES:
        if needle not in fired:
            errors.append(f"fired missing {needle}")
    return errors


class TrendAdoptRejectLockTests(unittest.TestCase):
    def test_given_live_page_when_lock_errors_then_empty(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/trend-adopt-reject.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_given_live_process_readme_when_errors_then_empty(self) -> None:
        self.assertEqual(
            process_readme_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_live_planner_when_errors_then_empty(self) -> None:
        self.assertEqual(planner_errors(PLANNER.read_text(encoding="utf-8")), [])

    def test_given_live_bots_readme_when_errors_then_empty(self) -> None:
        self.assertEqual(
            bots_readme_errors(BOTS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_live_trend_log_scaffold_reject_when_fired_errors_then_empty(
        self,
    ) -> None:
        self.assertEqual(fired_errors(TREND_LOG.read_text(encoding="utf-8")), [])

    def test_given_adr_and_routine_when_hitl_needles_then_present(self) -> None:
        adr = ADR_0002.read_text(encoding="utf-8")
        routine = ROUTINE.read_text(encoding="utf-8")
        self.assertIn("WATCH 列は置かない", adr)
        self.assertIn("CreateAgent は使わない", adr)
        self.assertIn("Never FIRE. Never implement.", routine)

    def test_given_watch_decision_when_trend_log_errors_then_decision(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | t | https://example.com/w | WATCH | "
            "hold | none |  |\n"
        )
        self.assertIn("decision", "\n".join(trend_log_errors(text)))

    def test_given_reject_without_evidence_gap_when_page_then_still_valid_row(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | 最先端手法 | t | https://example.com/r | REJECT | "
            "seat already exists | none |  |\n"
        )
        self.assertEqual(trend_log_errors(text), [])

    def test_given_complete_page_fixture_when_lock_errors_then_empty(self) -> None:
        self.assertEqual(lock_errors("\n".join(PAGE_NEEDLES) + "\n"), [])

    def test_given_page_fixture_missing_token_when_lock_errors_then_names_token(
        self,
    ) -> None:
        fixture = "\n".join(PAGE_NEEDLES) + "\n"
        for token in PAGE_NEEDLES:
            with self.subTest(missing=token):
                stripped = fixture.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_given_parser_must_fail_tokens_when_stripped_then_rejected(self) -> None:
        fixture = "\n".join(PAGE_NEEDLES) + "\n"
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = fixture.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_given_scaffold_reject_with_fired_when_errors_then_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | 第4ボット | "
            f"{SCAFFOLD_REJECT_URL} | REJECT | because | none | "
            "trend-adopt-reject.md WRAP LIVE; issues/117; CreateAgent NONE |\n"
        )
        self.assertEqual(fired_errors(text), [])

    def test_given_scaffold_empty_fired_when_errors_then_fired_is_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | 第4ボット | "
            f"{SCAFFOLD_REJECT_URL} | REJECT | because | none |  |\n"
        )
        self.assertIn("scaffold REJECT fired is empty", "\n".join(fired_errors(text)))

    def test_given_scaffold_adopt_when_errors_then_missing_reject_row(self) -> None:
        text = HEADER + (
            "| 2026-09-05 | Knowhow収集 | 第4ボット | "
            f"{SCAFFOLD_REJECT_URL} | ADOPT | because | none |  |\n"
        )
        self.assertIn(
            "missing scaffold REJECT row for issue 19",
            "\n".join(fired_errors(text)),
        )


if __name__ == "__main__":
    unittest.main()
