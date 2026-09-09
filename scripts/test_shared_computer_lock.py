#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory.trend_log import iter_trend_log_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "shared-computer.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
BOTS_README = ROOT / "bots" / "README.md"
CBO = ROOT / "bots" / "CBO.md"
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"

ISSUE_URL = "https://github.com/maplefukku/grok-bot-ops/issues/91"
SOURCE_URL = "https://x.com/madogiwacowork/status/2096721289599922688"

PAGE_NEEDLES: tuple[str, ...] = (
    "owner 席",
    "specialist",
    "handoff",
    "CreateAgent",
    "CreateAgent NONE",
    "schedules-force-agency",
    "並列マシン",
    "減らす",
    "Marketplace",
    "parallel-fire-fleet",
    "tool-path-prefer",
    "Cloud開発",
    "sand-workflow:cloud",
    ISSUE_URL,
    SOURCE_URL,
    "第二 cron",
    "戻せない",
    "poteto-mode",
    "quiet-test.sh",
)

PARSER_MUST_FAIL_WITHOUT: tuple[str, ...] = (
    "owner 席",
    "CreateAgent NONE",
    "schedules-force-agency",
    "並列マシン",
    "Marketplace",
    ISSUE_URL,
    SOURCE_URL,
    "第二 cron",
    "戻せない",
)

COMPLETE_FIXTURE = "\n".join(PAGE_NEEDLES) + "\n"


def lock_errors(text: str, needles: tuple[str, ...] = PAGE_NEEDLES) -> list[str]:
    return [f"missing {needle}" for needle in needles if needle not in text]


def cbo_role(text: str) -> str:
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == "役割":
            return cells[1]
    return ""


class SharedComputerLockTests(unittest.TestCase):
    def test_given_lock_page_when_read_then_required_needles_are_present(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/shared-computer.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_given_lock_page_when_read_then_rejects_createagent_new_seats(self) -> None:
        text = LOCK_PAGE.read_text(encoding="utf-8")
        self.assertIn("CreateAgent NONE", text)

    def test_given_process_readme_when_read_then_points_at_shared_computer(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("shared-computer.md", text)

    def test_given_bots_readme_lock_when_read_then_points_at_shared_computer(self) -> None:
        text = BOTS_README.read_text(encoding="utf-8")
        self.assertIn("## LOCK: SHARED ONE COMPUTER（#91）", text)
        self.assertIn("docs/process/shared-computer.md", text)

    def test_given_cbo_role_when_read_then_has_owner_seat_specialist_and_handoff(self) -> None:
        role = cbo_role(CBO.read_text(encoding="utf-8"))
        self.assertIn("owner 席", role)
        self.assertIn("specialist", role)
        self.assertIn("handoff", role)

    def test_given_trend_log_shared_computer_row_when_parsed_then_fired_cites_issue_91(
        self,
    ) -> None:
        rows = [
            row
            for row in iter_trend_log_rows(TREND_LOG.read_text(encoding="utf-8"))
            if row.source_url == SOURCE_URL
        ]
        self.assertEqual(len(rows), 1, SOURCE_URL)
        fired = rows[0].fired.strip()
        self.assertTrue(fired, "fired cell empty")
        self.assertIn(ISSUE_URL, fired)

    def test_given_complete_fixture_when_lock_errors_then_empty(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_given_fixture_missing_required_token_when_lock_errors_then_names_token(
        self,
    ) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
