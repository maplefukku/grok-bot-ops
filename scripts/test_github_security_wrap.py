#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WRAP_FILES: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    (
        ".github/dependabot.yml",
        (
            "version: 2",
            'package-ecosystem: "github-actions"',
            'interval: "weekly"',
            "groups:",
            "patterns:",
        ),
        (
            'package-ecosystem: "pip"',
            "renovate",
        ),
    ),
    (
        ".github/CODEOWNERS",
        (
            "* @maplefukku",
            "/.github/ @maplefukku",
        ),
        (),
    ),
    (
        ".github/workflows/codeql.yml",
        (
            "github/codeql-action/init",
            "language: python",
            "language: actions",
        ),
        (
            "merge_group",
            "- language: javascript-typescript",
        ),
    ),
    (
        ".github/workflows/scorecard.yml",
        (
            "ossf/scorecard-action",
            "publish_results: false",
        ),
        (),
    ),
    (
        ".github/workflows/ci.yml",
        (),
        ("merge_group",),
    ),
    (
        ".github/workflows/dependabot-auto-merge.yml",
        (
            "dependabot/fetch-metadata",
            "gh pr merge --auto",
        ),
        ("merge_group",),
    ),
    (
        "scripts/apply-main-pr-only-ruleset.sh",
        (
            "18800881",
            "repos/${REPO}/rulesets",
            "allow_auto_merge",
            "delete_branch_on_merge",
        ),
        ("merge_queue",),
    ),
    (
        "scripts/main-pr-only-ruleset.json",
        (
            '"name": "main-pr-only"',
            '"type": "deletion"',
            '"required_review_thread_resolution": true',
            '"context": "check"',
            "Cursor Approval Agent: Pull Request Router and Approver",
        ),
        (
            "merge_queue",
            "TypeScript",
            "Drizzle",
        ),
    ),
    (
        "docs/process/README.md",
        (
            "Dependabot",
            "18800881",
            "main-pr-only",
            "Org+GHAS",
        ),
        (
            "enable-secret-scanning",
            "enable-push-protection",
            "secret_scanning.yml",
        ),
    ),
)

ABSENT_PATHS = (".github/secret_scanning.yml",)


class GithubSecurityWrapTests(unittest.TestCase):
    def test_given_required_wrap_files_when_read_then_needles_match(self) -> None:
        for rel, must, must_not in WRAP_FILES:
            path = ROOT / rel
            with self.subTest(path=rel):
                self.assertTrue(path.is_file(), rel)
                text = path.read_text(encoding="utf-8")
                for needle in must:
                    self.assertIn(needle, text)
                for needle in must_not:
                    self.assertNotIn(needle, text)

    def test_given_secret_scanning_when_looked_up_then_fully_dropped(self) -> None:
        for rel in ABSENT_PATHS:
            with self.subTest(path=rel):
                self.assertFalse((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
