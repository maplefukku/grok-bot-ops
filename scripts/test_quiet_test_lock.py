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

SUCCESS_PAGE_NEEDLES = (
    BOX_SOT,
    "issue 74",
    "SUCCESS line-budget",
    "QUIET_OK_LINES",
    "10",
    "Soft-HOLD",
    "HITL",
    "PARK",
    "tool-path-prefer",
)

SUCCESS_FLEET_NEEDLES = (
    "QUIET_OK_LINES",
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

SUCCESS_PARSER_MUST_FAIL_WITHOUT = (
    "issue 74",
    "SUCCESS line-budget",
    "QUIET_OK_LINES",
    "PARK",
    "tool-path-prefer",
)

COMPLETE_FIXTURE = "\n".join(PAGE_NEEDLES) + "\n"
COMPLETE_FLEET_FIXTURE = (
    "QUIET_FAIL_LINES=500\n"
    "QUIET_OK_LINES=10\n"
    "--log\n"
    "QUIET_KEEP_FAIL_LOG\n"
)
COMPLETE_SUCCESS_FIXTURE = "\n".join(SUCCESS_PAGE_NEEDLES) + "\n"
COMPLETE_SUCCESS_FLEET_FIXTURE = "\n".join(SUCCESS_FLEET_NEEDLES) + "\n"

EXIT_PAGE_NEEDLES = (
    BOX_SOT,
    "issue 96",
    "exit-code contract",
    "SUCCESS",
    "FAIL",
    "exit 2",
    "fleet missing",
    "Quiet is not skip",
    "exec",
    "parallel-fire-fleet",
    "tool-path-prefer",
    "Soft-HOLD",
    "HITL",
    "CreateAgent",
)

EXIT_PARSER_MUST_FAIL_WITHOUT = (
    "issue 96",
    "exit-code contract",
    "exit 2",
    "fleet missing",
    "Quiet is not skip",
    "parallel-fire-fleet",
)

COMPLETE_EXIT_FIXTURE = "\n".join(EXIT_PAGE_NEEDLES) + "\n"

FAIL_TAIL_PAGE_NEEDLES = (
    BOX_SOT,
    "issue 93",
    "FAIL verbose-tail",
    "QUIET_FAIL_LINES",
    "`QUIET_FAIL_LINES` は 500",
    "tail",
    "full-log path",
    "--log",
    "QUIET_KEEP_FAIL_LOG",
    "REJECT A",
    "drip",
    "exit code",
    "Quiet is not skip",
    "parallel-fire-fleet",
    "tool-path-prefer",
    "Soft-HOLD",
    "HITL",
    "PARK",
    "CreateAgent",
)

FAIL_TAIL_FLEET_NEEDLES = (
    "tail",
    "QUIET_FAIL_LINES",
)

FAIL_TAIL_PARSER_MUST_FAIL_WITHOUT = (
    "issue 93",
    "FAIL verbose-tail",
    "`QUIET_FAIL_LINES` は 500",
    "full-log path",
    "REJECT A",
    "drip",
    "parallel-fire-fleet",
)

COMPLETE_FAIL_TAIL_FIXTURE = "\n".join(FAIL_TAIL_PAGE_NEEDLES) + "\n"
COMPLETE_FAIL_TAIL_FLEET_FIXTURE = "\n".join(FAIL_TAIL_FLEET_NEEDLES) + "\n"

FAIL_EXIT_PAGE_NEEDLES = (
    BOX_SOT,
    "issue 114",
    "FAIL exit contract",
    "AI-readable",
    "nonzero",
    "unchanged",
    "QUIET_FAIL_LINES",
    "tail",
    "full-log path",
    "QUIET_OK_LINES",
    "SUCCESS",
    "minimal",
    "REJECT A",
    "drip",
    "Quiet is not skip",
    "parallel-fire-fleet",
    "tool-path-prefer",
    "Soft-HOLD",
    "HITL",
    "PARK",
    "CreateAgent",
)

FAIL_EXIT_PARSER_MUST_FAIL_WITHOUT = (
    "issue 114",
    "FAIL exit contract",
    "AI-readable",
    "parallel-fire-fleet",
    "Quiet is not skip",
)

COMPLETE_FAIL_EXIT_FIXTURE = "\n".join(FAIL_EXIT_PAGE_NEEDLES) + "\n"


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


def success_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in SUCCESS_PAGE_NEEDLES if needle not in text]


def success_fleet_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in SUCCESS_FLEET_NEEDLES if needle not in text]


def exit_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in EXIT_PAGE_NEEDLES if needle not in text]


def fail_tail_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in FAIL_TAIL_PAGE_NEEDLES if needle not in text]


def fail_tail_fleet_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in FAIL_TAIL_FLEET_NEEDLES if needle not in text]


def fail_exit_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in FAIL_EXIT_PAGE_NEEDLES if needle not in text]


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

    def test_lock_page_contains_success_line_budget_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(success_lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_process_readme_points_at_success_line_budget(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("quiet-test.md", text)
        self.assertIn("issue 74", text)
        self.assertIn("QUIET_OK_LINES", text)
        self.assertIn("SUCCESS line-budget", text)

    def test_fleet_sot_matches_success_line_budget_when_present(self) -> None:
        path = fleet_sot_path()
        if not (path.is_file() and os.access(path, os.X_OK)):
            self.skipTest(f"box absent at {path}")
        self.assertEqual(success_fleet_lock_errors(path.read_text(encoding="utf-8")), [])

    def test_success_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(success_lock_errors(COMPLETE_SUCCESS_FIXTURE), [])

    def test_success_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in SUCCESS_PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_SUCCESS_FIXTURE.replace(token, "")
                found = success_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_success_fleet_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(success_fleet_lock_errors(COMPLETE_SUCCESS_FLEET_FIXTURE), [])

    def test_success_fleet_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in SUCCESS_FLEET_NEEDLES:
            with self.subTest(missing=token):
                stripped = COMPLETE_SUCCESS_FLEET_FIXTURE.replace(token, "")
                found = success_fleet_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_lock_page_contains_exit_code_contract_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(exit_lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_process_readme_points_at_exit_code_contract(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("quiet-test.md", text)
        self.assertIn("issue 96", text)
        self.assertIn("exit-code contract", text)

    def test_exit_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(exit_lock_errors(COMPLETE_EXIT_FIXTURE), [])

    def test_exit_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in EXIT_PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_EXIT_FIXTURE.replace(token, "")
                found = exit_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_lock_page_contains_fail_verbose_tail_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(fail_tail_lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_process_readme_points_at_fail_verbose_tail(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("quiet-test.md", text)
        self.assertIn("issue 93", text)
        self.assertIn("FAIL verbose-tail", text)
        self.assertIn("full-log path", text)

    def test_fleet_sot_matches_fail_verbose_tail_when_present(self) -> None:
        path = fleet_sot_path()
        if not (path.is_file() and os.access(path, os.X_OK)):
            self.skipTest(f"box absent at {path}")
        self.assertEqual(fail_tail_fleet_lock_errors(path.read_text(encoding="utf-8")), [])

    def test_fail_tail_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(fail_tail_lock_errors(COMPLETE_FAIL_TAIL_FIXTURE), [])

    def test_fail_tail_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in FAIL_TAIL_PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FAIL_TAIL_FIXTURE.replace(token, "")
                found = fail_tail_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_fail_tail_fleet_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(fail_tail_fleet_lock_errors(COMPLETE_FAIL_TAIL_FLEET_FIXTURE), [])

    def test_fail_tail_fleet_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in FAIL_TAIL_FLEET_NEEDLES:
            with self.subTest(missing=token):
                stripped = COMPLETE_FAIL_TAIL_FLEET_FIXTURE.replace(token, "")
                found = fail_tail_fleet_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_lock_page_contains_fail_exit_contract_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/quiet-test.md")
        self.assertEqual(fail_exit_lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_process_readme_points_at_fail_exit_contract(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("quiet-test.md", text)
        self.assertIn("issue 114", text)
        self.assertIn("FAIL exit contract", text)
        self.assertIn("AI-readable", text)

    def test_fail_exit_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(fail_exit_lock_errors(COMPLETE_FAIL_EXIT_FIXTURE), [])

    def test_fail_exit_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in FAIL_EXIT_PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FAIL_EXIT_FIXTURE.replace(token, "")
                found = fail_exit_lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
