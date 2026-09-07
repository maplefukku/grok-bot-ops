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
            "javascript-typescript",
        ),
        ("merge_group",),
    ),
    (
        ".github/workflows/scorecard.yml",
        (
            "ossf/scorecard-action",
            "publish_results: true",
        ),
        (),
    ),
    (
        ".github/workflows/ci.yml",
        (),
        ("merge_group",),
    ),
    (
        "docs/process/README.md",
        (
            "Dependabot",
            "enable-secret-scanning",
        ),
        (),
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

    def test_given_secret_scanning_yml_when_looked_up_then_file_is_absent(self) -> None:
        for rel in ABSENT_PATHS:
            with self.subTest(path=rel):
                self.assertFalse((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
