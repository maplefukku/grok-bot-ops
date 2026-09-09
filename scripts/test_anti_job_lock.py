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
)

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "anti-job.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
BOTS_README = ROOT / "bots" / "README.md"
SHOPPING = ROOT / "docs" / "knowhow" / "shopping.md"
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"
HAGGLE_URL = "https://x.ai/bot/marketplace/bots/haggle-bot"

PAGE_NEEDLES = (
    "spend / sign / send",
    "explicit go",
    "purchases",
    "send-on-behalf",
    "Auto-review",
    HAGGLE_URL,
    "https://x.ai/news/grok-bot-procurement",
    "https://docs.x.ai/grok-bot/approvals-security-and-privacy",
    "grok-bot-ops/issues/90",
    "CreateAgent しない",
    "standing approval",
    "request_box_help",
    "SKILL.md は置かない",
    "shopping.md",
    "trend-log.md",
    "0004",
    "tool-path-prefer",
    "sand-workflow:parallel-fire-fleet",
    "sand-workflow:cloud",
    "Quiet is not skip",
    "test_anti_job_lock.py",
)
PROCESS_README_NEEDLES = (
    "anti-job.md",
    "issue 90",
    "spend / sign / send",
    "explicit go",
)
BOTS_README_NEEDLES = (
    "LOCK: ANTI-JOB",
    "docs/process/anti-job.md",
    "explicit go",
    "CreateAgent",
)
SHOPPING_NEEDLES = ("anti-job.md",)
FIRED_NEEDLES = ("anti-job.md", "CreateAgent NONE")

HEADER = (
    "## 判断記録\n"
    "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
)


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PAGE_NEEDLES if needle not in text]


def process_readme_errors(text: str) -> list[str]:
    return [
        f"missing {needle}"
        for needle in PROCESS_README_NEEDLES
        if needle not in text
    ]


def bots_readme_errors(text: str) -> list[str]:
    return [
        f"missing {needle}" for needle in BOTS_README_NEEDLES if needle not in text
    ]


def shopping_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in SHOPPING_NEEDLES if needle not in text]


def _haggle_row(text: str) -> DecisionRow | None:
    for row in iter_trend_log_rows(text):
        if normalize_source_url(row.source_url) == HAGGLE_URL:
            return row
    return None


def fired_errors(text: str) -> list[str]:
    errors: list[str] = []
    row = _haggle_row(text)
    if row is None:
        return ["missing haggle row"]
    if row.decision != "ADOPT":
        errors.append("haggle decision is not ADOPT")
    fired = row.fired.strip()
    if not fired:
        errors.append("haggle fired is empty")
        return errors
    for needle in FIRED_NEEDLES:
        if needle not in fired:
            errors.append(f"fired missing {needle}")
    return errors


FILE_LOCKS = (
    ("process_readme", PROCESS_README_NEEDLES, process_readme_errors),
    ("bots_readme", BOTS_README_NEEDLES, bots_readme_errors),
    ("shopping", SHOPPING_NEEDLES, shopping_errors),
)


class AntiJobLockTests(unittest.TestCase):
    def test_given_live_page_when_lock_errors_then_empty(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/anti-job.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_given_live_process_readme_when_errors_then_empty(self) -> None:
        self.assertEqual(
            process_readme_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_live_bots_readme_when_errors_then_empty(self) -> None:
        self.assertEqual(
            bots_readme_errors(BOTS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_live_shopping_when_errors_then_empty(self) -> None:
        self.assertEqual(shopping_errors(SHOPPING.read_text(encoding="utf-8")), [])

    def test_given_live_trend_log_when_fired_errors_then_empty(self) -> None:
        self.assertEqual(fired_errors(TREND_LOG.read_text(encoding="utf-8")), [])

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

    def test_given_complete_file_fixture_when_errors_then_empty(self) -> None:
        for name, needles, fn in FILE_LOCKS:
            with self.subTest(name=name):
                self.assertEqual(fn("\n".join(needles) + "\n"), [])

    def test_given_file_fixture_missing_token_when_errors_then_names_token(
        self,
    ) -> None:
        for name, needles, fn in FILE_LOCKS:
            fixture = "\n".join(needles) + "\n"
            for token in needles:
                with self.subTest(name=name, missing=token):
                    stripped = fixture.replace(token, "")
                    found = fn(stripped)
                    self.assertTrue(found, f"{name} missing {token} was accepted")
                    self.assertIn(token, "\n".join(found))

    def test_given_haggle_adopt_with_fired_when_errors_then_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-09 | Haggle | t | "
            "https://x.ai/bot/marketplace/bots/haggle-bot | ADOPT | because | "
            "ops | anti-job.md LIVE; CreateAgent NONE |\n"
        )
        self.assertEqual(fired_errors(text), [])

    def test_given_haggle_empty_fired_when_errors_then_fired_is_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-09 | Haggle | t | "
            "https://x.ai/bot/marketplace/bots/haggle-bot | ADOPT | because | "
            "ops |  |\n"
        )
        self.assertIn("haggle fired is empty", "\n".join(fired_errors(text)))

    def test_given_haggle_fired_lacking_createagent_none_when_errors_then_names_token(
        self,
    ) -> None:
        text = HEADER + (
            "| 2026-09-09 | Haggle | t | "
            "https://x.ai/bot/marketplace/bots/haggle-bot | ADOPT | because | "
            "ops | anti-job.md LIVE |\n"
        )
        self.assertIn("CreateAgent NONE", "\n".join(fired_errors(text)))

    def test_given_haggle_url_trailing_slash_when_errors_then_empty(self) -> None:
        text = HEADER + (
            "| 2026-09-09 | Haggle | t | "
            "https://x.ai/bot/marketplace/bots/haggle-bot/ | ADOPT | because | "
            "ops | anti-job.md LIVE; CreateAgent NONE |\n"
        )
        self.assertEqual(fired_errors(text), [])

    def test_given_no_haggle_row_when_errors_then_missing_haggle_row(self) -> None:
        text = HEADER + (
            "| 2026-09-09 | other | t | https://example.com/x | ADOPT | "
            "because | ops |  |\n"
        )
        self.assertIn("missing haggle row", "\n".join(fired_errors(text)))

    def test_given_haggle_reject_when_errors_then_not_adopt(self) -> None:
        text = HEADER + (
            "| 2026-09-09 | Haggle | t | "
            "https://x.ai/bot/marketplace/bots/haggle-bot | REJECT | because | "
            "ops | anti-job.md LIVE; CreateAgent NONE |\n"
        )
        self.assertIn("not ADOPT", "\n".join(fired_errors(text)))


if __name__ == "__main__":
    unittest.main()
