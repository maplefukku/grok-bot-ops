#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "quiet-test.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
BOX_SOT = "/workspace/fleet-scripts/quiet-test.sh"

PAGE_NEEDLES = (
    BOX_SOT,
    "fail-cap B",
    "QUIET_FAIL_LINES",
    "`QUIET_FAIL_LINES` は 500",
    "QUIET_OK_LINES",
    "`QUIET_OK_LINES` は 10",
    "--log",
    "QUIET_KEEP_FAIL_LOG",
    "Quiet is not skip",
    "xcbeautify",
    "quiet-test.sh --",
    "run-quiet.sh",
    "issue 69",
    "issue 45",
    "CI-independent",
    "HITL",
    "Soft-HOLD",
)

README_NEEDLES = (
    BOX_SOT,
    "500",
    "quiet-test.md",
    "issue 45",
    "issue 69",
    "fail-cap B",
)

FLEET_NEEDLES = (
    "QUIET_FAIL_LINES",
    "QUIET_OK_LINES",
    "--log",
    "QUIET_KEEP_FAIL_LOG",
)

FAIL_DEFAULT_RE = re.compile(r"QUIET_FAIL_LINES[^\n]*\b500\b")
OK_DEFAULT_RE = re.compile(r"QUIET_OK_LINES[^\n]*\b10\b")

PARSER_MUST_FAIL_WITHOUT = (
    "`QUIET_FAIL_LINES` は 500",
    "--log",
    "Quiet is not skip",
    BOX_SOT,
    "CI-independent",
    "HITL",
    "issue 69",
)

COMPLETE_FIXTURE = "\n".join(PAGE_NEEDLES) + "\n"
COMPLETE_FLEET_FIXTURE = (
    "QUIET_FAIL_LINES=500\n"
    "QUIET_OK_LINES=10\n"
    "--log\n"
    "QUIET_KEEP_FAIL_LOG\n"
)


def fleet_sot_path() -> Path:
    return Path(os.environ.get("QUIET_TEST", BOX_SOT))


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PAGE_NEEDLES if needle not in text]


def readme_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in README_NEEDLES if needle not in text]


def fleet_default_errors(text: str) -> list[str]:
    errors: list[str] = []
    if not FAIL_DEFAULT_RE.search(text):
        errors.append("missing QUIET_FAIL_LINES default 500")
    if not OK_DEFAULT_RE.search(text):
        errors.append("missing QUIET_OK_LINES default 10")
    return errors


def fleet_lock_errors(text: str) -> list[str]:
    missing = [f"missing {needle}" for needle in FLEET_NEEDLES if needle not in text]
    missing.extend(fleet_default_errors(text))
    return missing


class QuietTestLockTests(unittest.TestCase):
    def test_lock_page_exists(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")

    def test_lock_page_contains_required_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_process_readme_points_at_lock_page(self) -> None:
        self.assertEqual(
            readme_lock_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_fleet_sot_matches_fail_cap_b_when_present(self) -> None:
        path = fleet_sot_path()
        if not (path.is_file() and os.access(path, os.X_OK)):
            self.skipTest(f"box absent at {path}")
        self.assertEqual(fleet_lock_errors(path.read_text(encoding="utf-8")), [])

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_fleet_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(fleet_lock_errors(COMPLETE_FLEET_FIXTURE), [])

    def test_fleet_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in FLEET_NEEDLES:
            with self.subTest(missing=token):
                stripped = COMPLETE_FLEET_FIXTURE.replace(token, "")
                found = fleet_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
