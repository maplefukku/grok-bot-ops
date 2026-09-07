#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "pr-body.md"
PROCESS_INDEX = ROOT / "docs" / "process" / "README.md"
SKILLS_INDEX = ROOT / "skills" / "README.md"
BOTS_INDEX = ROOT / "bots" / "README.md"

BOX_TEMPLATE = "/workspace/fleet-scripts/pr-show-me-template.md"
HUMANLAYER_SHOW_ME = (
    "https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md"
)

MUST_H2 = (
    "## Readable change (show-me)",
    "## Pseudocode",
    "## Mermaid",
    "## TDD / BDD evidence",
)

NEEDLES = (
    BOX_TEMPLATE,
    HUMANLAYER_SHOW_ME,
    "show-me-your-work",
    "sand-workflow:job-brief",
    "sand-workflow:cloud",
    "sand-workflow:pr",
    "sand-workflow:pr-2",
    "quiet-test.sh --",
    *MUST_H2,
)

PARSER_MUST_FAIL_WITHOUT = (
    MUST_H2[0],
    MUST_H2[3],
    BOX_TEMPLATE,
    "show-me-your-work",
    "sand-workflow:job-brief",
    "sand-workflow:pr",
    "sand-workflow:pr-2",
)

COMPLETE_FIXTURE = "\n".join(NEEDLES) + "\n"

POINTER_FILES = (
    PROCESS_INDEX,
    SKILLS_INDEX,
    BOTS_INDEX,
)


def _token_char(ch: str) -> bool:
    return ch.isalnum() or ch in "-_"


def _has_needle(text: str, needle: str) -> bool:
    start = 0
    n = len(needle)
    while True:
        i = text.find(needle, start)
        if i < 0:
            return False
        left_ok = i == 0 or not _token_char(text[i - 1])
        end = i + n
        right_ok = end == len(text) or not _token_char(text[end])
        if left_ok and right_ok:
            return True
        start = i + 1


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in NEEDLES if not _has_needle(text, needle)]


def pointer_errors(text: str, rel: str) -> list[str]:
    errors: list[str] = []
    if "docs/process/pr-body.md" not in text and "./pr-body.md" not in text:
        errors.append(f"{rel}: missing SoT pointer docs/process/pr-body.md")
    return errors


class PrBodyLockTests(unittest.TestCase):
    def test_lock_page_exists(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")

    def test_lock_page_contains_required_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = "\n".join(n for n in NEEDLES if n != token) + "\n"
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_must_h2_lines_are_character_exact(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/pr-body.md")
        lines = set(LOCK_PAGE.read_text(encoding="utf-8").splitlines())
        missing = [header for header in MUST_H2 if header not in lines]
        self.assertEqual(missing, [], "MUST H2s must be exact standalone lines")

    def test_pointer_files_cite_sot_and_do_not_repeat_h2_headings(self) -> None:
        for path in POINTER_FILES:
            rel = str(path.relative_to(ROOT))
            with self.subTest(path=rel):
                self.assertTrue(path.is_file(), rel)
                text = path.read_text(encoding="utf-8")
                self.assertEqual(pointer_errors(text, rel), [])
                heading_hits = [
                    header
                    for header in MUST_H2
                    if f"\n{header}\n" in f"\n{text}\n"
                ]
                self.assertEqual(
                    heading_hits,
                    [],
                    f"{rel} must point, not copy the HARD LOCK H2s",
                )

    def test_skills_index_names_job_brief_cloud_and_pr(self) -> None:
        text = SKILLS_INDEX.read_text(encoding="utf-8")
        for skill in ("job-brief", "cloud", "pr", "pr-2"):
            self.assertTrue(
                _has_needle(text, skill),
                f"skills/README.md must name {skill}",
            )


if __name__ == "__main__":
    unittest.main()
