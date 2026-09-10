#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOTS_README = ROOT / "bots" / "README.md"
ISSUE_URL = "https://github.com/maplefukku/grok-bot-ops/issues/115"

README_NEEDLES: tuple[str, ...] = (
    "## LOCK: ROLE MAX-LENGTH（#115）",
    "504",
    "CI運用.md",
    "live census",
    "役割",
    "one line",
    "scripts/test_bots_description_max_length.py",
    "scripts/test_bots_description_max_length_lock.py",
    "quiet-test.sh --",
    "Quiet is not skip",
    "parallel-fire-fleet",
    "Cloud開発",
    "sand-workflow:cloud",
    "CreateAgent NONE",
    "harness",
    "Soft-HOLD",
    ISSUE_URL,
)

PARSER_MUST_FAIL_WITHOUT: tuple[str, ...] = (
    "## LOCK: ROLE MAX-LENGTH（#115）",
    "504",
    "CI運用.md",
    "scripts/test_bots_description_max_length.py",
    "quiet-test.sh --",
    "parallel-fire-fleet",
    ISSUE_URL,
)

COMPLETE_FIXTURE = "\n".join(README_NEEDLES) + "\n"


def lock_errors(text: str, needles: tuple[str, ...] = README_NEEDLES) -> list[str]:
    return [f"missing {needle}" for needle in needles if needle not in text]


class BotsDescriptionMaxLengthLockTests(unittest.TestCase):
    def test_given_bots_readme_lock_when_read_then_required_needles_are_present(
        self,
    ) -> None:
        self.assertTrue(BOTS_README.is_file(), "bots/README.md")
        self.assertEqual(lock_errors(BOTS_README.read_text(encoding="utf-8")), [])

    def test_given_complete_fixture_when_lock_errors_then_empty(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_given_fixture_missing_required_token_when_lock_errors_then_names_token(
        self,
    ) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(any(token in item for item in found), found)


if __name__ == "__main__":
    unittest.main()
