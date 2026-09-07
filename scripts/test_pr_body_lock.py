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

SKILL_ENTRYPOINTS = (
    "sand-workflow:job-brief",
    "sand-workflow:cloud",
    "sand-workflow:pr-2",
    "sand-workflow:pr",
)

HARNESS_NAMES = (
    "pr-show-me-template.md",
    "pr-body.sh",
    "show-me.sh",
    "run-pr-body.sh",
)

NEEDLES = HEADERS + (
    BOX_TEMPLATE,
    SHOW_ME,
    "OSS調査",
    "MIT",
    "2026-08-13",
    "show-me-your-work",
    "job-brief",
    "sand-workflow:cloud",
    "sand-workflow:pr-2",
    "sand-workflow:pr",
    "CreateAgent",
    "quiet-test.sh",
    "WRAP",
    "harness",
    "FAIL",
)

POINTER_PATHS = (PROCESS_INDEX, BOTS_INDEX, SKILLS_INDEX, AGENTS)

PARSER_MUST_FAIL_WITHOUT = HEADERS + (BOX_TEMPLATE, SHOW_ME, "OSS調査")

COMPLETE_FIXTURE = "\n".join(NEEDLES) + "\n"

_TOKEN_FOLLOW = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")


def token_in(text: str, needle: str) -> bool:
    start = 0
    while True:
        found = text.find(needle, start)
        if found < 0:
            return False
        end = found + len(needle)
        nxt = text[end] if end < len(text) else ""
        if nxt == "" or nxt not in _TOKEN_FOLLOW:
            return True
        start = found + 1


def lock_errors(text: str) -> list[str]:
    return [f"missing {needle}" for needle in NEEDLES if not token_in(text, needle)]


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

    def test_oss_survey_comes_before_headers(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)
        text = LOCK_PAGE.read_text(encoding="utf-8")
        oss = text.find("## OSS調査")
        first = text.find(HEADERS[0])
        self.assertGreaterEqual(oss, 0, "OSS調査")
        self.assertGreaterEqual(first, 0, HEADERS[0])
        self.assertLess(oss, first)

    def test_headers_are_exact_and_in_order(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)
        lines = LOCK_PAGE.read_text(encoding="utf-8").splitlines()
        positions = []
        for header in HEADERS:
            self.assertIn(header, lines, header)
            positions.append(lines.index(header))
        self.assertEqual(positions, sorted(positions))

    def test_no_invented_ca_brief_template(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), SOT_REL)
        text = LOCK_PAGE.read_text(encoding="utf-8")
        self.assertNotIn("## CA brief", text)
        fences = text.split("```")
        for chunk in fences[1::2]:
            copied = [header for header in HEADERS if header in chunk]
            self.assertEqual(copied, [], "fenced second header list")

    def test_no_invented_harness_file(self) -> None:
        hits: list[Path] = []
        for name in HARNESS_NAMES:
            hits.extend(
                path
                for path in ROOT.rglob(name)
                if ".git" not in path.parts
            )
        self.assertEqual(hits, [])

    def test_bots_lock_names_skill_entrypoints(self) -> None:
        text = BOTS_INDEX.read_text(encoding="utf-8")
        start = text.find("LOCK: PR-BODY")
        self.assertGreaterEqual(start, 0, "LOCK: PR-BODY")
        section = text[start:]
        nxt = section.find("\n## ", 2)
        if nxt != -1:
            section = section[:nxt]
        for uri in SKILL_ENTRYPOINTS:
            with self.subTest(uri=uri):
                self.assertTrue(token_in(section, uri), uri)

    def test_skills_dir_has_no_skill_md(self) -> None:
        hits = list((ROOT / "skills").rglob("SKILL.md"))
        self.assertEqual(hits, [])

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
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                copied = [header for header in HEADERS if header in text]
                self.assertEqual(copied, [], f"{path.name} copied headers")

    def test_parser_does_not_treat_pr2_as_pr(self) -> None:
        only_pr2 = COMPLETE_FIXTURE.replace("sand-workflow:pr\n", "")
        self.assertIn("sand-workflow:pr-2", only_pr2)
        self.assertFalse(token_in(only_pr2, "sand-workflow:pr"))
        found = lock_errors(only_pr2)
        self.assertTrue(found)
        self.assertIn("sand-workflow:pr", "\n".join(found))

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
