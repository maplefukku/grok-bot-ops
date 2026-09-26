#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory import AtomDraft, IngestOff, Kind, MemoryStore, Source  # noqa: E402
from intent_memory.disposition import DISPOSITIONS, canonical_thread  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LOCK_PAGE = ROOT / "docs" / "process" / "adv-disposition.md"
PROCESS_README = ROOT / "docs" / "process" / "README.md"
PR_BODY = ROOT / "docs" / "process" / "pr-body.md"
TREND_LOG = ROOT / "docs" / "decisions" / "trend-log.md"
FIXTURE = ROOT / "scripts" / "intent_memory" / "fixtures.json"

ISSUE_URL = "https://github.com/maplefukku/grok-bot-ops/issues/140"
PR_297 = "https://github.com/maplefukku/sauna-master/pull/297"
WONTFIX_THREAD = f"{PR_297}#discussion_r3952453491"
HARVEST_THREADS = (
    WONTFIX_THREAD,
    f"{PR_297}#discussion_r3952411869",
    f"{PR_297}#discussion_r4028777512",
    f"{PR_297}#discussion_r4029228334",
)
ADV_SUCCESS_ROW = (
    "| ADV SUCCESS | ADV が SUCCESS。skip / dismiss は SUCCESS ではない |"
)

PAGE_NEEDLES: tuple[str, ...] = (
    ISSUE_URL,
    "adv-disposition",
    "issue 118",
    "第二の Closer ではない",
    "t13247u",
    "auto-intake ではない",
    "OOS",
    "WONTFIX",
    "NOT warranted",
    "boundary issue",
    "`adv-followup`",
    "first-wins",
    "theme 行",
    "prev-fps",
    "ADV は disposition を書かない",
    "`pdm`",
    "`user`",
    "IngestOff",
    "bot:Closer",
    "disposition.py",
    "adv_closer.py",
    "trend_log.py",
    "disposition:reject|oos|invalid",
    "product:<repo>",
    "upstream",
    "downstream",
    "Dup / Thrash",
    "新しい failing check は無条件に MUST",
    "disposition ≠ ADV SUCCESS",
    "trend-log.md",
    "0001-intent-memory-postgres-pgvector.md",
    "0002-trend-adopt-loop.md",
    "sand-workflow:pr-2",
    "sand-workflow:cloud",
    "sand-workflow:finding-to-spec",
    "ADOPT B",
    "ADOPT D",
    "r3952453491",
    "#297 は reopen しない",
    "#287",
    "OOS registry",
    "CreateAgent NONE",
    "HOLD merge=PM",
    "quiet-test.sh",
    "Quiet is not skip",
    "test_adv_disposition_lock.py",
    "adv-disposition-lock",
)
PROCESS_README_NEEDLES: tuple[str, ...] = (
    "adv-disposition.md",
    "issue 140",
    "`adv-followup`",
    "upstream",
    "disposition を保存しても ADV SUCCESS ではない",
    "adv-disposition-lock",
)
PARSER_MUST_FAIL_WITHOUT: tuple[str, ...] = (
    ISSUE_URL,
    "IngestOff",
    "disposition ≠ ADV SUCCESS",
    "新しい failing check は無条件に MUST",
    "CreateAgent NONE",
    "sand-workflow:cloud",
)


def needle_errors(text: str, needles: tuple[str, ...]) -> list[str]:
    return [f"missing {needle}" for needle in needles if needle not in text]


def invariance_errors(pr_body: str, trend_log: str) -> list[str]:
    errors: list[str] = []
    if ADV_SUCCESS_ROW not in pr_body:
        errors.append("pr-body.md ADV SUCCESS row changed")
    if "disposition" in pr_body:
        errors.append("pr-body.md mentions disposition")
    for needle in ("disposition:", "sauna-master/pull/297"):
        if needle in trend_log:
            errors.append(f"trend-log.md contains {needle}")
    return errors


def _harvest_rows() -> list[dict]:
    rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return [row for row in rows if "adv" in row["tags"]]


def _draft(row: dict) -> AtomDraft:
    return AtomDraft(
        kind=Kind(row["kind"]),
        tags=tuple(row["tags"]),
        body=row["body"],
        actor=row["actor"],
        source=Source(row.get("source", "human")),
        source_url=row.get("source_url"),
        github_url=row.get("github_url"),
    )


class AdvDispositionLockTests(unittest.TestCase):
    def test_given_live_page_when_needles_then_empty(self) -> None:
        self.assertTrue(LOCK_PAGE.is_file(), "docs/process/adv-disposition.md")
        self.assertEqual(
            needle_errors(LOCK_PAGE.read_text(encoding="utf-8"), PAGE_NEEDLES), []
        )

    def test_given_live_process_readme_when_needles_then_empty(self) -> None:
        self.assertEqual(
            needle_errors(
                PROCESS_README.read_text(encoding="utf-8"), PROCESS_README_NEEDLES
            ),
            [],
        )

    def test_given_live_pr_body_and_trend_log_when_invariance_then_empty(self) -> None:
        self.assertEqual(
            invariance_errors(
                PR_BODY.read_text(encoding="utf-8"),
                TREND_LOG.read_text(encoding="utf-8"),
            ),
            [],
        )

    def test_given_disposition_in_pr_body_when_invariance_then_flagged(self) -> None:
        found = invariance_errors(ADV_SUCCESS_ROW + "\ndisposition persist\n", "")
        self.assertIn("pr-body.md mentions disposition", found)
        found = invariance_errors("", "| x | disposition:oos |")
        self.assertIn("pr-body.md ADV SUCCESS row changed", found)
        self.assertIn("trend-log.md contains disposition:", found)

    def test_given_complete_page_fixture_when_needles_then_empty(self) -> None:
        self.assertEqual(needle_errors("\n".join(PAGE_NEEDLES) + "\n", PAGE_NEEDLES), [])

    def test_given_page_fixture_missing_token_when_needles_then_names_token(
        self,
    ) -> None:
        fixture = "\n".join(PAGE_NEEDLES) + "\n"
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                found = needle_errors(fixture.replace(token, ""), PAGE_NEEDLES)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))

    def test_given_fixture_harvest_when_read_by_cli_then_four_threads_and_mill_lesson(
        self,
    ) -> None:
        store = MemoryStore()
        for row in _harvest_rows():
            store.seed_fixture(_draft(row))
        atoms = store.by_tags(
            ("adv", "product:sauna-master"), source=Source.HUMAN, reader="cli"
        )
        decisions = [atom for atom in atoms if atom.kind is Kind.DECISION]
        critiques = [atom for atom in atoms if atom.kind is Kind.CRITIQUE_HUMAN]
        self.assertEqual(
            tuple(atom.source_url for atom in decisions), HARVEST_THREADS
        )
        self.assertEqual(len(critiques), 1)
        self.assertEqual(critiques[0].source_url, PR_297)
        wontfix = [atom for atom in decisions if atom.source_url == WONTFIX_THREAD]
        self.assertEqual(len(wontfix), 1)
        self.assertIn("disposition:reject", wontfix[0].tags)

    def test_given_fixture_harvest_when_checked_then_tags_and_actors_hold_the_lock(
        self,
    ) -> None:
        allowed = {"adv", "product:sauna-master"} | {
            f"disposition:{item}" for item in DISPOSITIONS
        }
        for row in _harvest_rows():
            with self.subTest(source_url=row.get("source_url")):
                self.assertEqual(row.get("source", "human"), "human")
                self.assertIn(row["actor"], {"pdm", "user"})
                self.assertLessEqual(set(row["tags"]), allowed)
                if row["kind"] == "decision":
                    self.assertEqual(
                        canonical_thread(row["source_url"]), row["source_url"]
                    )
                    self.assertEqual(
                        sum(tag.startswith("disposition:") for tag in row["tags"]), 1
                    )

    def test_given_harvest_rows_as_source_bot_when_append_then_ingest_off(
        self,
    ) -> None:
        store = MemoryStore()
        for row in _harvest_rows():
            draft = _draft(row)
            for actor in (row["actor"], "bot:Closer"):
                with self.subTest(source_url=row.get("source_url"), actor=actor):
                    with self.assertRaises(IngestOff):
                        store.append(replace(draft, source=Source.BOT, actor=actor))
        self.assertEqual(store.by_tags(("adv",), source=Source.BOT, reader="pdm"), [])


if __name__ == "__main__":
    unittest.main()
