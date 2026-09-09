#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory.trend_log import iter_trend_log_rows, normalize_source_url  # noqa: E402
from overnight_goal import (  # noqa: E402
    DomainUnit,
    Files,
    GoalBrief,
    Lines,
    brief_errors,
    main,
    parse_brief,
)

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "process" / "overnight-goal.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"
HERMES_URL = "https://x.com/Teknium/status/2095412050751332838"

PAGE_NEEDLES = (
    "sand-workflow:overnight-goal-cleanup",
    "sand-workflow:cloud",
    "sand-workflow:parallel-fire-fleet",
    "tool-path-prefer",
    "issue 89",
    "trend-log.md",
    "07-overnight.md",
    "## done-when",
    "## touch scope",
    "## diff cap",
    "## mid-run verify",
    "## verifier",
    "時間の長さは完了条件ではない",
    "quiet-test.sh --",
    "Quiet is not skip",
    "domain-unit",
    "micro",
    "Soft-HOLD",
    "CreateAgent",
    "harness",
    "scripts/overnight_goal.py",
)
README_NEEDLES = ("overnight-goal.md", "issue 89", "overnight /goal")
PARSER_MUST_FAIL_WITHOUT = (
    "Soft-HOLD",
    "## verifier",
    "quiet-test.sh --",
    "scripts/overnight_goal.py",
)

COMPLETE_BRIEF = """## Goal
WRAP Hermes /goal overnight cleanup into docs/process.

## done-when
- docs/process/overnight-goal.md exists and scripts/quiet-test.sh -- python3 scripts/ci.py exits 0
- trend-log fired cell for the Hermes row names the page

## touch scope
docs/process/overnight-goal.md docs/process/README.md scripts/overnight_goal.py scripts/test_overnight_goal.py

## diff cap
domain-unit fat lander, 1 PR

## mid-run verify
scripts/quiet-test.sh -- python3 scripts/ci.py

## verifier
PR確認 merge-ok + PdM Flag Y. Independent of the impl CA.

## no-new-box
WRAP existing skills only.
"""

ISSUE_89_BRIEF = """## Goal
Soft Domain WRAP Hermes /goal overnight cleanup pattern into grok-bot-ops (ADOPT trend-log). Cite existing overnight-goal-cleanup skill — do not invent a new harness.

## done-when
ONE fat domain lander PR: docs/process or routines pointer + CI/quiet-test evidence that overnight /goal shape (done-criteria, touch scope, diff cap, mid-run verify, independent verifier Soft-HOLD) is encoded; PR body exact4.

## touch scope
docs/process, docs/decisions (trend-log fired cell), routines/ if needed, tests that lock the docs/contract

## diff cap
domain-unit fat lander — no drip micro PRs

## no-new-box
WRAP existing overnight-goal-cleanup + cloud skill only. REJECT invent Amp/Orbs/new overnight runner.

## OOS
CreateAgent; product app code; on-demand; Soft Flag filler

Cite parallel-fire-fleet + cloud + quiet-test.sh + poteto-mode. CreateAgent NONE.
"""

COMPLETE_GOAL = GoalBrief(
    goal="WRAP Hermes /goal overnight cleanup into docs/process.",
    done_when=(
        "docs/process/overnight-goal.md exists and scripts/quiet-test.sh -- python3 scripts/ci.py exits 0",
        "trend-log fired cell for the Hermes row names the page",
    ),
    touch_scope=(
        "docs/process/overnight-goal.md",
        "docs/process/README.md",
        "scripts/overnight_goal.py",
        "scripts/test_overnight_goal.py",
    ),
    diff_cap=DomainUnit(),
    mid_run_verify="scripts/quiet-test.sh -- python3 scripts/ci.py",
    verifier="PR確認 merge-ok + PdM Flag Y. Independent of the impl CA.",
)


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PAGE_NEEDLES if needle not in text]


def readme_lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in README_NEEDLES if needle not in text]


def _with_section(brief: str, heading: str, body: str) -> str:
    lines = brief.splitlines()
    out: list[str] = []
    i = 0
    target = heading.casefold()
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("## ") and stripped[3:].strip().casefold() == target:
            out.append(lines[i])
            if body:
                out.append(body)
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("## "):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + "\n"


def _without_section(brief: str, heading: str) -> str:
    lines = brief.splitlines()
    out: list[str] = []
    i = 0
    target = heading.casefold()
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("## ") and stripped[3:].strip().casefold() == target:
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("## "):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + "\n"


class CompleteBriefTests(unittest.TestCase):
    def test_given_complete_brief_then_no_errors_and_typed_goal_brief(self) -> None:
        self.assertEqual(brief_errors(COMPLETE_BRIEF), [])
        self.assertEqual(parse_brief(COMPLETE_BRIEF), COMPLETE_GOAL)


class Issue89Tests(unittest.TestCase):
    def test_given_issue_89_body_then_missing_mid_run_verify_and_verifier(self) -> None:
        self.assertEqual(
            brief_errors(ISSUE_89_BRIEF),
            ["missing ## mid-run verify", "missing ## verifier"],
        )


class DoneWhenTests(unittest.TestCase):
    def test_given_english_duration_entry_then_duration_error(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "done-when", "- work on this for 4 hours")
        self.assertEqual(
            brief_errors(text),
            ["done-when is a duration, not a predicate: work on this for 4 hours"],
        )

    def test_given_japanese_duration_entry_then_duration_error(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "done-when", "- 8時間で終わる")
        self.assertEqual(
            brief_errors(text),
            ["done-when is a duration, not a predicate: 8時間で終わる"],
        )


class TouchScopeTests(unittest.TestCase):
    def test_given_glob_star_token_then_unbounded_error(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "touch scope", "**")
        self.assertEqual(brief_errors(text), ["touch scope is unbounded: **"])


class DiffCapTests(unittest.TestCase):
    def test_given_unparsed_diff_cap_then_neither_error(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "diff cap", "small")
        self.assertEqual(
            brief_errors(text),
            ["diff cap is neither N files/lines nor domain-unit: small"],
        )

    def test_given_twenty_files_then_files_cap(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "diff cap", "20 files")
        self.assertEqual(brief_errors(text), [])
        self.assertEqual(parse_brief(text).diff_cap, Files(20))

    def test_given_three_hundred_lines_then_lines_cap(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "diff cap", "300 lines")
        self.assertEqual(brief_errors(text), [])
        self.assertEqual(parse_brief(text).diff_cap, Lines(300))


class MidRunVerifyTests(unittest.TestCase):
    def test_given_npm_test_then_quiet_test_error(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "mid-run verify", "npm test")
        self.assertEqual(
            brief_errors(text),
            ["mid-run verify must run through quiet-test.sh -- <cmd>: npm test"],
        )


class VerifierTests(unittest.TestCase):
    def test_given_self_then_not_independent(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "verifier", "self")
        self.assertEqual(brief_errors(text), ["verifier is not independent: self"])

    def test_given_sakusha_ca_then_not_independent(self) -> None:
        text = _with_section(COMPLETE_BRIEF, "verifier", "作者 CA")
        self.assertEqual(brief_errors(text), ["verifier is not independent: 作者 CA"])


class EmptySectionTests(unittest.TestCase):
    def test_given_verifier_heading_then_immediate_next_section_then_empty_error(
        self,
    ) -> None:
        text = _with_section(COMPLETE_BRIEF, "verifier", "")
        self.assertEqual(brief_errors(text), ["empty ## verifier"])


class AliasTests(unittest.TestCase):
    def test_given_kanryo_joken_heading_then_accepted_as_done_when(self) -> None:
        text = COMPLETE_BRIEF.replace("## done-when", "## 完了条件")
        self.assertEqual(brief_errors(text), [])
        self.assertEqual(parse_brief(text), COMPLETE_GOAL)


class MultipleErrorTests(unittest.TestCase):
    def test_given_unbounded_scope_and_missing_verifier_then_registry_order(self) -> None:
        text = _without_section(
            _with_section(COMPLETE_BRIEF, "touch scope", "**"),
            "verifier",
        )
        self.assertEqual(
            brief_errors(text),
            ["touch scope is unbounded: **", "missing ## verifier"],
        )


class CliTests(unittest.TestCase):
    def test_given_ok_and_bad_paths_when_main_then_exit_1_and_literal_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ok_path = root / "ok.md"
            bad_path = root / "bad.md"
            ok_path.write_text(COMPLETE_BRIEF, encoding="utf-8")
            bad_path.write_text(ISSUE_89_BRIEF, encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main([str(ok_path), str(bad_path)])
            self.assertEqual(code, 1)
            self.assertEqual(
                buf.getvalue(),
                (
                    f"ok   {ok_path}\n"
                    f"FAIL {bad_path}\n"
                    "  missing ## mid-run verify\n"
                    "  missing ## verifier\n"
                ),
            )

    def test_given_no_args_when_main_then_exit_2(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(main([]), 2)


class LockWrapTests(unittest.TestCase):
    def test_given_overnight_goal_page_then_exists_and_lock_errors_empty(self) -> None:
        self.assertTrue(PAGE.is_file(), "docs/process/overnight-goal.md")
        self.assertEqual(lock_errors(PAGE.read_text(encoding="utf-8")), [])

    def test_given_process_readme_then_lock_errors_empty(self) -> None:
        self.assertEqual(
            readme_lock_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_complete_needles_fixture_then_lock_errors_empty(self) -> None:
        self.assertEqual(lock_errors("\n".join(PAGE_NEEDLES)), [])

    def test_given_fixture_missing_required_token_then_lock_error_names_token(self) -> None:
        fixture = "\n".join(PAGE_NEEDLES)
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = fixture.replace(token, "")
                found = lock_errors(stripped)
                self.assertEqual(found, [f"missing {token}"])


class TrendLogLockTests(unittest.TestCase):
    def test_given_hermes_row_then_fired_contains_overnight_goal_and_issue_89(self) -> None:
        rows = [
            row
            for row in iter_trend_log_rows(TREND_LOG.read_text(encoding="utf-8"))
            if normalize_source_url(row.source_url)
            == normalize_source_url(HERMES_URL)
        ]
        self.assertEqual(len(rows), 1)
        fired = rows[0].fired
        self.assertIn("overnight-goal.md", fired)
        self.assertIn("issues/89", fired)


if __name__ == "__main__":
    unittest.main()
