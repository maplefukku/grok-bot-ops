#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory import (  # noqa: E402
    FEELING_TTL_DAYS,
    AtomDraft,
    ContractError,
    IngestOff,
    Kind,
    MemoryStore,
    Source,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "docs" / "intent-memory" / "schema.sql"
FAR_FUTURE = datetime(2100, 1, 1, tzinfo=timezone.utc)
PAST = datetime(2020, 1, 1, tzinfo=timezone.utc)
NOW = datetime(2026, 9, 4, tzinfo=timezone.utc)


def _draft(**kwargs) -> AtomDraft:
    values = dict(
        kind=Kind.INTENT,
        tags=("fleet",),
        body="body",
        actor="pdm",
        embedding=(1.0, 0.0, 0.0, 0.0),
        source=Source.HUMAN,
    )
    values.update(kwargs)
    return AtomDraft(**values)


class TestIsolation(unittest.TestCase):
    def test_by_tags_human_never_returns_bot_row_even_when_tags_match(self):
        store = MemoryStore()
        store.append(
            _draft(tags=("fleet", "lock"), body="human lock", embedding=(1.0, 0.0))
        )
        store.seed_fixture(
            _draft(
                kind=Kind.CRITIQUE_BOT,
                source=Source.BOT,
                tags=("fleet", "lock"),
                body="bot lock",
                actor="bot",
                embedding=(0.0, 1.0),
            )
        )
        rows = store.by_tags(("fleet", "lock"), source=Source.HUMAN)
        self.assertTrue(rows)
        self.assertTrue(all(atom.source is Source.HUMAN for atom in rows))
        self.assertTrue(all(atom.kind is not Kind.CRITIQUE_BOT for atom in rows))
        self.assertTrue(all(atom.body != "bot lock" for atom in rows))

    def test_similar_human_never_returns_bot_row_even_when_bot_vector_is_closer(self):
        store = MemoryStore()
        query = (1.0, 0.0, 0.0)
        human = store.append(
            _draft(tags=("fleet",), body="far human", embedding=(0.0, 1.0, 0.0))
        )
        store.seed_fixture(
            _draft(
                kind=Kind.CRITIQUE_BOT,
                source=Source.BOT,
                tags=("fleet",),
                body="near bot",
                actor="bot",
                embedding=(1.0, 0.0, 0.0),
            )
        )
        rows = store.similar(query, source=Source.HUMAN, limit=5)
        self.assertEqual([atom.id for atom in rows], [human.id])
        self.assertTrue(all(atom.source is Source.HUMAN for atom in rows))
        self.assertTrue(all(atom.body != "near bot" for atom in rows))


class TestIngest(unittest.TestCase):
    def test_append_rejects_critique_bot(self):
        store = MemoryStore()
        with self.assertRaises(IngestOff):
            store.append(
                _draft(
                    kind=Kind.CRITIQUE_BOT,
                    source=Source.BOT,
                    body="bot critique",
                    actor="bot",
                )
            )

    def test_append_rejects_source_bot(self):
        store = MemoryStore()
        with self.assertRaises(IngestOff):
            store.append(_draft(source=Source.BOT, actor="bot"))

    def test_seed_fixture_inserts_bot_critique_for_isolation_tests(self):
        store = MemoryStore()
        atom = store.seed_fixture(
            _draft(
                kind=Kind.CRITIQUE_BOT,
                source=Source.BOT,
                tags=("fleet",),
                body="seeded bot",
                actor="bot",
                embedding=(0.0, 1.0, 0.0, 0.0),
            )
        )
        self.assertIs(atom.kind, Kind.CRITIQUE_BOT)
        self.assertIs(atom.source, Source.BOT)
        human_rows = store.by_tags(("fleet",), source=Source.HUMAN)
        bot_rows = store.by_tags(("fleet",), source=Source.BOT)
        self.assertEqual(human_rows, [])
        self.assertEqual([row.id for row in bot_rows], [atom.id])


class TestTtl(unittest.TestCase):
    def test_expired_feeling_omitted_from_reads(self):
        store = MemoryStore()
        store.append(
            _draft(
                kind=Kind.FEELING,
                tags=("mood",),
                body="stale feeling",
                embedding=(1.0, 0.0),
                expires_at=PAST,
            )
        )
        live = store.append(
            _draft(
                kind=Kind.FEELING,
                tags=("mood",),
                body="live feeling",
                embedding=(0.0, 1.0),
                expires_at=NOW + timedelta(days=1),
            )
        )
        tagged = store.by_tags(("mood",), source=Source.HUMAN, now=NOW)
        near = store.similar((0.0, 1.0), source=Source.HUMAN, limit=5, now=NOW)
        self.assertEqual([atom.body for atom in tagged], ["live feeling"])
        self.assertEqual([atom.id for atom in near], [live.id])

    def test_critique_human_visible_when_now_is_far_future(self):
        store = MemoryStore()
        atom = store.append(
            _draft(
                kind=Kind.CRITIQUE_HUMAN,
                tags=("fail",),
                body="human critique stays",
                embedding=(1.0, 0.0),
            )
        )
        self.assertIsNone(atom.expires_at)
        tagged = store.by_tags(("fail",), source=Source.HUMAN, now=FAR_FUTURE)
        near = store.similar((1.0, 0.0), source=Source.HUMAN, limit=5, now=FAR_FUTURE)
        self.assertEqual([row.id for row in tagged], [atom.id])
        self.assertEqual([row.id for row in near], [atom.id])

    def test_feeling_default_ttl_is_90_days(self):
        store = MemoryStore()
        created = datetime(2026, 1, 1, tzinfo=timezone.utc)
        atom = store.append(
            _draft(
                kind=Kind.FEELING,
                tags=("mood",),
                body="default ttl",
                embedding=(1.0, 0.0),
                created_at=created,
            )
        )
        self.assertEqual(FEELING_TTL_DAYS, 90)
        self.assertEqual(atom.expires_at, created + timedelta(days=90))


class TestTagsAndPairing(unittest.TestCase):
    def test_tag_filter_is_exact_names_and(self):
        store = MemoryStore()
        both = store.append(
            _draft(tags=("fleet", "lock"), body="both", embedding=(1.0, 0.0, 0.0))
        )
        store.append(
            _draft(tags=("fleet",), body="fleet-only", embedding=(0.0, 1.0, 0.0))
        )
        store.append(
            _draft(tags=("lock",), body="lock-only", embedding=(0.0, 0.0, 1.0))
        )
        store.append(
            _draft(
                tags=("fleet-ops", "lock"),
                body="near name",
                embedding=(1.0, 1.0, 0.0),
            )
        )
        rows = store.by_tags(("fleet", "lock"), source=Source.HUMAN)
        self.assertEqual([atom.id for atom in rows], [both.id])
        fleet = store.by_tags(("fleet",), source=Source.HUMAN)
        self.assertEqual({atom.body for atom in fleet}, {"both", "fleet-only"})
        with self.assertRaises(ContractError):
            store.by_tags((), source=Source.HUMAN)

    def test_pairing_critique_bot_iff_source_bot(self):
        store = MemoryStore()
        with self.assertRaises(ContractError):
            store.seed_fixture(
                _draft(
                    kind=Kind.CRITIQUE_BOT,
                    source=Source.HUMAN,
                    body="mismatched critique_bot",
                )
            )
        ok = store.seed_fixture(
            _draft(
                kind=Kind.CRITIQUE_BOT,
                source=Source.BOT,
                body="paired bot",
                actor="bot",
            )
        )
        self.assertIs(ok.source, Source.BOT)

    def test_pairing_other_kinds_iff_source_human(self):
        others = (
            Kind.INTENT,
            Kind.DECISION,
            Kind.BELIEF,
            Kind.FEELING,
            Kind.CRITIQUE_HUMAN,
        )
        for kind in others:
            with self.subTest(kind=kind):
                store = MemoryStore()
                extra = {}
                if kind is Kind.FEELING:
                    extra["expires_at"] = NOW + timedelta(days=90)
                with self.assertRaises(ContractError):
                    store.seed_fixture(
                        _draft(
                            kind=kind,
                            source=Source.BOT,
                            body="mismatched human-kind",
                            actor="bot",
                            **extra,
                        )
                    )


class TestNoNetwork(unittest.TestCase):
    def test_fixture_vectors_no_openai_client_or_api_key(self):
        os.environ.pop("OPENAI_API_KEY", None)
        for name in ("openai", "httpx", "requests"):
            self.assertNotIn(name, sys.modules)
        store = MemoryStore()
        store.append(_draft(embedding=(1.0, 0.0)))
        rows = store.similar((1.0, 0.0), source=Source.HUMAN, limit=1)
        self.assertEqual(len(rows), 1)
        for name in ("openai", "httpx", "requests"):
            self.assertNotIn(name, sys.modules)
        contract_path = Path(__file__).with_name("contract.py")
        source = contract_path.read_text(encoding="utf-8")
        self.assertNotIn("openai", source.lower())
        self.assertNotIn("OpenAI", source)


class TestSchemaSql(unittest.TestCase):
    def test_schema_sql_encodes_extension_table_source_and_checks(self):
        text = SCHEMA.read_text(encoding="utf-8")
        self.assertIn("CREATE EXTENSION", text)
        self.assertIn("vector", text)
        self.assertIn("intent_atom", text)
        self.assertRegex(text, r"\bsource\b")
        lower = text.lower()
        pairing_ok = (
            "intent_atom_pairing" in lower
            or ("critique_bot" in lower and "source" in lower)
        )
        feeling_ok = "intent_atom_feeling" in lower or (
            "feeling" in lower and "expires_at" in lower
        )
        critique_ok = (
            "intent_atom_critique_human" in lower or "critique_human" in lower
        )
        self.assertTrue(pairing_ok, "schema must encode pairing")
        self.assertTrue(feeling_ok, "schema must encode feeling expiry")
        self.assertTrue(critique_ok, "schema must encode critique_human")
        self.assertIn("cardinality(requested) >= 1", text)


class TestReadApiShape(unittest.TestCase):
    def test_by_tags_and_similar_require_source(self):
        store = MemoryStore()
        with self.assertRaises(TypeError):
            store.by_tags(("fleet",))
        with self.assertRaises(TypeError):
            store.similar((1.0, 0.0), limit=1)


class TestCli(unittest.TestCase):
    def test_cli_similar_human_default_omits_closer_bot_row(self):
        import json
        import subprocess

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "intent_memory" / "read.py"),
                "--vector",
                "1",
                "0",
                "0",
                "0",
                "--n",
                "5",
                "--fixture",
                str(ROOT / "scripts" / "intent_memory" / "fixtures.json"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        rows = json.loads(proc.stdout)
        self.assertTrue(rows)
        self.assertTrue(all(row["source"] == "human" for row in rows))
        self.assertTrue(all(row["kind"] != "critique_bot" for row in rows))
        self.assertTrue(
            all(row["body"] != "Bot row must not leak into human reads." for row in rows)
        )


if __name__ == "__main__":
    unittest.main()
