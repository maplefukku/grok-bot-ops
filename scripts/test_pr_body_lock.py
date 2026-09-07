#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "pr-body.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
SKILLS_README = ROOT / "skills" / "README.md"
BOTS_README = ROOT / "bots" / "README.md"
AGENTS = ROOT / "AGENTS.md"

BOX_SOT = "/workspace/fleet-scripts/pr-show-me-template.md"
QUIET_WRAP = "/workspace/fleet-scripts/quiet-test.sh --"
SHOW_ME_OSS = (
    "https://github.com/humanlayer/skills/blob/main/"
    "plugins/show-me/skills/show-me/SKILL.md"
)

HEADERS = (
    "## Readable change (show-me)",
    "## Pseudocode",
    "## Mermaid",
    "## TDD / BDD evidence",
)

NEEDLES = (
    BOX_SOT,
    *HEADERS,
    "Flag Y",
    SHOW_ME_OSS,
    "show-me-your-work",
    QUIET_WRAP,
    "Quiet is not skip",
    "job-brief",
    "sand-workflow:cloud",
    "sand-workflow:pr",
    "Beauty",
    "Coverage",
    "pending",
    "HARD LOCK",
)

PARSER_MUST_FAIL_WITHOUT = (
    BOX_SOT,
    HEADERS[0],
    "Flag Y",
    "Quiet is not skip",
)

POINTER_PATH = "docs/process/pr-body.md"
COMPLETE_FIXTURE = "\n".join(NEEDLES) + "\n"


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in NEEDLES if needle not in text]


class PrBodyLockTests(unittest.TestCase):
    def test_lock_page_exists(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")

    def test_lock_page_contains_required_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_lock_page_does_not_invent_coverage_percent(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")
        text = LOCK_PAGE.read_text(encoding="utf-8")
        self.assertNotRegex(text, r"Coverage[^.\n]{0,40}\d+\s*%")

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_process_readme_points_at_lock_page(self) -> None:
        text = PROCESS_README.read_text(encoding="utf-8")
        self.assertIn("pr-body.md", text)
        self.assertIn("Flag Y", text)

    def test_skills_readme_cites_same_sot_without_second_header_list(self) -> None:
        text = SKILLS_README.read_text(encoding="utf-8")
        self.assertIn(POINTER_PATH, text)
        self.assertIn(BOX_SOT, text)
        for header in HEADERS:
            self.assertNotIn(header, text, "skills/ must not copy the header list")

    def test_bots_readme_is_pointer_only(self) -> None:
        text = BOTS_README.read_text(encoding="utf-8")
        self.assertIn("LOCK: PR-BODY", text)
        self.assertIn("pr-body.md", text)
        for header in HEADERS:
            self.assertNotIn(header, text, "bots/ must not copy the header list")

    def test_agents_md_points_at_lock_page(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        self.assertIn("pr-body.md", text)


if __name__ == "__main__":
    unittest.main()
