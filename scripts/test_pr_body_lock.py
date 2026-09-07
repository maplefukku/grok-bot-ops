#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "pr-body.md"
PROCESS_INDEX = ROOT / "docs" / "process" / "README.md"
BOTS_INDEX = ROOT / "bots" / "README.md"
SKILLS_INDEX = ROOT / "skills" / "README.md"
AGENTS = ROOT / "AGENTS.md"
BOX_TEMPLATE = "/workspace/fleet-scripts/pr-show-me-template.md"
SHOW_ME = (
    "https://github.com/humanlayer/skills/blob/main/"
    "plugins/show-me/skills/show-me/SKILL.md"
)
SOT_REL = "docs/process/pr-body.md"

HEADERS = (
    "## Readable change (show-me)",
    "## Pseudocode",
    "## Mermaid",
    "## TDD / BDD evidence",
)

NEEDLES = HEADERS + (
    BOX_TEMPLATE,
    SHOW_ME,
    "show-me-your-work",
    "job-brief",
    "sand-workflow:cloud",
    "sand-workflow:pr",
    "CA brief",
    "CreateAgent",
    "quiet-test.sh",
)

POINTER_PATHS = (PROCESS_INDEX, BOTS_INDEX, SKILLS_INDEX, AGENTS)

PARSER_MUST_FAIL_WITHOUT = HEADERS + (BOX_TEMPLATE, SHOW_ME, "show-me-your-work")

COMPLETE_FIXTURE = "\n".join(NEEDLES) + "\n"


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in NEEDLES if needle not in text]


def pointer_errors(text: str, rel: str) -> list[str]:
    errors: list[str] = []
    if SOT_REL not in text and "pr-body.md" not in text:
        errors.append(f"{rel}: missing pointer to {SOT_REL}")
    return errors


class PrBodyLockTests(unittest.TestCase):
    def test_lock_page_exists(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)

    def test_lock_page_contains_required_needles(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)
        self.assertEqual(lock_errors(LOCK_PAGE.read_text(encoding="utf-8")), [])

    def test_headers_are_exact_and_in_order(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)
        text = LOCK_PAGE.read_text(encoding="utf-8")
        positions = [text.find(header) for header in HEADERS]
        self.assertTrue(all(pos >= 0 for pos in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_pointers_cite_same_sot(self) -> None:
        for path in POINTER_PATHS:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file(), str(path))
                found = pointer_errors(
                    path.read_text(encoding="utf-8"),
                    str(path.relative_to(ROOT)),
                )
                self.assertEqual(found, [])

    def test_pointers_do_not_invent_second_header_list(self) -> None:
        for path in POINTER_PATHS:
            if path == LOCK_PAGE:
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                copied = [header for header in HEADERS if header in text]
                self.assertEqual(copied, [], f"{path.name} copied headers")

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
