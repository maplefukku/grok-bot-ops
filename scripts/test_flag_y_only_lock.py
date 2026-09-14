#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

ROOT = Path(__file__).resolve().parents[1]
PR_BODY = ROOT / "docs" / "process" / "pr-body.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"

ISSUE_127 = "grok-bot-ops/issues/127"

PR_BODY_NEEDLES: tuple[str, ...] = (
    "### PdM merge sweep（Flag Y ONLY）",
    "behind0",
    "thr0",
    "FULL CLEAN",
    "APPROVED",
    "ADV SUCCESS",
    "Flag≠Bugbot",
    "HOLD merge=PM",
    ISSUE_127,
    "merge-ok 4 行",
    "author.__typename",
    "`User`",
    "`Bot`",
    "reviewDecision",
    "PullRequestReview",
    "test_flag_y_only_lock.py",
    "Quiet is not skip",
)

PROCESS_README_NEEDLES: tuple[str, ...] = (
    ISSUE_127,
    "test_flag_y_only_lock.py",
    "Flag≠Bugbot",
    "HOLD merge=PM",
    "merge-ok 4 行",
    "flag-y-only-lock",
)


def pr_body_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in PR_BODY_NEEDLES if needle not in text]


def process_readme_errors(text: str) -> list[str]:
    return [
        f"missing {needle}"
        for needle in PROCESS_README_NEEDLES
        if needle not in text
    ]


class FlagYOnlyLockTests(unittest.TestCase):
    def test_given_live_pr_body_when_errors_then_empty(self) -> None:
        self.assertTrue(PR_BODY.is_file(), "docs/process/pr-body.md")
        self.assertEqual(pr_body_errors(PR_BODY.read_text(encoding="utf-8")), [])

    def test_given_live_process_readme_when_errors_then_empty(self) -> None:
        self.assertEqual(
            process_readme_errors(PROCESS_README.read_text(encoding="utf-8")),
            [],
        )

    def test_given_complete_pr_body_fixture_when_errors_then_empty(self) -> None:
        self.assertEqual(pr_body_errors("\n".join(PR_BODY_NEEDLES) + "\n"), [])

    def test_given_pr_body_fixture_missing_token_when_errors_then_names_token(
        self,
    ) -> None:
        fixture = "\n".join(PR_BODY_NEEDLES) + "\n"
        for token in PR_BODY_NEEDLES:
            with self.subTest(missing=token):
                stripped = fixture.replace(token, "")
                found = pr_body_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


if __name__ == "__main__":
    unittest.main()
