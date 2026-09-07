#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "quiet-test.md"
BOX_SOT = "/workspace/fleet-scripts/quiet-test.sh"

NEEDLES = (
    BOX_SOT,
    "fail-cap B",
    "QUIET_FAIL_LINES",
    "500",
    "--log",
    "QUIET_KEEP_FAIL_LOG",
    "Quiet is not skip",
    "xcbeautify",
    "quiet-test.sh --",
    "run-quiet.sh",
)

PARSER_MUST_FAIL_WITHOUT = (
    "500",
    "--log",
    "Quiet is not skip",
    BOX_SOT,
)

COMPLETE_FIXTURE = "\n".join(NEEDLES) + "\n"


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in NEEDLES if needle not in text]


class QuietTestLockTests(unittest.TestCase):
    def test_lock_page_exists(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")

    def test_lock_page_contains_required_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
