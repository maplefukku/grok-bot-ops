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
    EDGE_URL_KEYS,
    FEELING_TTL_DAYS,
    HUMAN_KINDS,
    AtomDraft,
    ContractError,
    IngestOff,
    Kind,
    MemoryStore,
    Source,
    WriteAclHold,
)
from intent_memory.trend_log import drafts_from_trend_log  # noqa: E402

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
        self.assertIn("related_ids uuid[]", text)
        self.assertNotRegex(text, r"\bsource_url\s+text\b")
        self.assertNotRegex(text, r"\bgithub_url\s+text\b")
        self.assertNotRegex(text, r"\bgb_url\s+text\b")


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


class TestHumanIngest(unittest.TestCase):
    def test_append_accepts_each_human_kind(self):
        for kind in HUMAN_KINDS:
            with self.subTest(kind=kind):
                store = MemoryStore()
                extra = {}
                if kind is Kind.FEELING:
                    extra["expires_at"] = NOW + timedelta(days=90)
                atom = store.append(_draft(kind=kind, body=kind.value, **extra))
                self.assertIs(atom.source, Source.HUMAN)
                self.assertIs(atom.kind, kind)
                rows = store.by_tags(("fleet",), source=Source.HUMAN)
                self.assertEqual([row.id for row in rows], [atom.id])

    def test_human_kinds_exclude_critique_bot(self):
        self.assertNotIn(Kind.CRITIQUE_BOT, HUMAN_KINDS)


class TestEdges(unittest.TestCase):
    def test_related_ids_and_body_url_fields_round_trip(self):
        store = MemoryStore()
        related = "11111111-1111-1111-1111-111111111111"
        atom = store.append(
            _draft(
                body="edge body",
                related_ids=(related,),
                source_url="https://example.com/primary",
                github_url="https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543719022",
                gb_url="https://github.com/maplefukku/grok-bot-ops/issues/18",
            )
        )
        self.assertEqual(atom.related_ids, (related,))
        self.assertEqual(atom.source_url, "https://example.com/primary")
        self.assertEqual(
            atom.github_url,
            "https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543719022",
        )
        self.assertEqual(
            atom.gb_url, "https://github.com/maplefukku/grok-bot-ops/issues/18"
        )
        for key in EDGE_URL_KEYS:
            self.assertIn(f"{key}:", atom.body)
        tagged = store.by_tags(("fleet",), source=Source.HUMAN)
        self.assertEqual(tagged[0].source_url, atom.source_url)

    def test_fixture_human_filter_keeps_url_edges(self):
        import json
        import subprocess

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "intent_memory" / "read.py"),
                "--tags",
                "fleet",
                "lock",
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
        self.assertTrue(any(row.get("source_url") for row in rows))
        self.assertTrue(any(row.get("related_ids") for row in rows))


class TestTrendLogDryRun(unittest.TestCase):
    def test_trend_log_maps_to_bot_decision_and_append_rejects(self):
        text = (ROOT / "docs" / "decisions" / "trend-log.md").read_text(
            encoding="utf-8"
        )
        drafts = drafts_from_trend_log(text)
        self.assertTrue(drafts)
        store = MemoryStore()
        for draft in drafts:
            self.assertIs(draft.kind, Kind.DECISION)
            self.assertIs(draft.source, Source.BOT)
            self.assertEqual(draft.actor, "bot:Planner")
            self.assertIn("trend-adopt", draft.tags)
            self.assertIn("source_url:", draft.body)
            self.assertIsNone(draft.expires_at)
            with self.assertRaises(IngestOff):
                store.append(draft)
        self.assertEqual(store.by_tags(("trend-adopt",), source=Source.HUMAN), [])

    def test_trend_log_cli_dry_run_prints_bot_drafts_only(self):
        import json
        import subprocess

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "intent_memory" / "trend_log.py"),
                "--dry-run",
                "--path",
                str(ROOT / "docs" / "decisions" / "trend-log.md"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        rows = json.loads(proc.stdout)
        self.assertTrue(rows)
        self.assertTrue(all(row["source"] == "bot" for row in rows))
        self.assertTrue(all(row["kind"] == "decision" for row in rows))


class TestPostgresWrap(unittest.TestCase):
    def test_runbook_and_compose_wrap_official_pgvector(self):
        runbook = ROOT / "docs" / "intent-memory" / "postgres.md"
        compose = ROOT / "docs" / "intent-memory" / "docker-compose.yml"
        recipe = ROOT / "docs" / "intent-memory" / "read-recipe.md"
        text = runbook.read_text(encoding="utf-8")
        yml = compose.read_text(encoding="utf-8")
        recipe_text = recipe.read_text(encoding="utf-8")
        self.assertIn("CREATE EXTENSION", text)
        self.assertIn("pgvector/pgvector", text)
        self.assertIn("https://github.com/pgvector/pgvector", text)
        self.assertIn("pgvector/pgvector:pg18-trixie", yml)
        self.assertIn("./schema.sql", yml)
        self.assertNotIn("neo4j", text.lower())
        self.assertNotIn("mem0", text.lower())
        self.assertIn("by_tags", recipe_text)
        self.assertIn("similar", recipe_text)
        self.assertIn("Planner dry-run", recipe_text)
        self.assertIn("RecallMemory", recipe_text)


class TestWriteAcl(unittest.TestCase):
    def test_given_pdm_human_intent_when_append_then_row_is_stored(self):
        store = MemoryStore()
        atom = store.append(
            _draft(
                kind=Kind.INTENT,
                source=Source.HUMAN,
                actor="pdm",
                body="pdm intent",
            )
        )
        self.assertEqual(atom.actor, "pdm")
        self.assertIs(atom.kind, Kind.INTENT)
        self.assertIs(atom.source, Source.HUMAN)
        self.assertEqual(atom.body, "pdm intent")
        rows = store.by_tags(("fleet",), source=Source.HUMAN)
        self.assertEqual([row.id for row in rows], [atom.id])

    def test_given_user_human_decision_when_append_then_row_is_stored(self):
        store = MemoryStore()
        atom = store.append(
            _draft(
                kind=Kind.DECISION,
                source=Source.HUMAN,
                actor="user",
                body="user decision",
            )
        )
        self.assertEqual(atom.actor, "user")
        self.assertIs(atom.kind, Kind.DECISION)
        self.assertIs(atom.source, Source.HUMAN)
        self.assertEqual(atom.body, "user decision")
        rows = store.by_tags(("fleet",), source=Source.HUMAN)
        self.assertEqual([row.id for row in rows], [atom.id])

    def test_given_planner_human_intent_when_append_then_write_acl_hold_and_store_empty(
        self,
    ):
        store = MemoryStore()
        with self.assertRaises(WriteAclHold) as ctx:
            store.append(
                _draft(
                    kind=Kind.INTENT,
                    source=Source.HUMAN,
                    actor="planner",
                    body="planner intent",
                )
            )
        self.assertIn("HITL PARK", str(ctx.exception))
        self.assertEqual(store.by_tags(("fleet",), source=Source.HUMAN), [])

    def test_given_human_source_bot_actor_when_append_then_write_acl_hold_and_store_empty(
        self,
    ):
        store = MemoryStore()
        with self.assertRaises(WriteAclHold) as ctx:
            store.append(
                _draft(
                    kind=Kind.INTENT,
                    source=Source.HUMAN,
                    actor="bot",
                    body="spoofed bot actor",
                )
            )
        self.assertIn("HITL PARK", str(ctx.exception))
        self.assertEqual(store.by_tags(("fleet",), source=Source.HUMAN), [])

    def test_given_empty_actor_when_append_then_write_acl_hold_and_store_empty(self):
        store = MemoryStore()
        with self.assertRaises(WriteAclHold) as ctx:
            store.append(
                _draft(
                    kind=Kind.INTENT,
                    source=Source.HUMAN,
                    actor="",
                    body="empty actor",
                )
            )
        self.assertIn("HITL PARK", str(ctx.exception))
        self.assertEqual(store.by_tags(("fleet",), source=Source.HUMAN), [])

    def test_given_trend_log_shaped_draft_when_append_then_ingest_off_not_write_acl_hold(
        self,
    ):
        store = MemoryStore()
        with self.assertRaises(IngestOff) as ctx:
            store.append(
                _draft(
                    kind=Kind.DECISION,
                    source=Source.BOT,
                    actor="bot:Planner",
                    body="trend-log shaped",
                )
            )
        self.assertNotIsInstance(ctx.exception, WriteAclHold)
        self.assertEqual(str(ctx.exception), "bot ingest is off")
        self.assertEqual(store.by_tags(("fleet",), source=Source.HUMAN), [])
        self.assertEqual(store.by_tags(("fleet",), source=Source.BOT), [])

    def test_given_critique_bot_draft_when_seed_fixture_then_bot_row_is_stored(self):
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
        self.assertEqual(atom.actor, "bot")
        self.assertEqual(atom.body, "seeded bot")
        self.assertEqual(store.by_tags(("fleet",), source=Source.HUMAN), [])
        bot_rows = store.by_tags(("fleet",), source=Source.BOT)
        self.assertEqual([row.id for row in bot_rows], [atom.id])

    def test_given_each_human_kind_when_append_with_actor_pdm_then_row_is_stored(self):
        for kind in HUMAN_KINDS:
            with self.subTest(kind=kind):
                store = MemoryStore()
                extra = {}
                if kind is Kind.FEELING:
                    extra["expires_at"] = NOW + timedelta(days=90)
                atom = store.append(
                    _draft(kind=kind, actor="pdm", body=kind.value, **extra)
                )
                self.assertEqual(atom.actor, "pdm")
                self.assertIs(atom.source, Source.HUMAN)
                self.assertIs(atom.kind, kind)
                self.assertEqual(atom.body, kind.value)
                rows = store.by_tags(("fleet",), source=Source.HUMAN)
                self.assertEqual([row.id for row in rows], [atom.id])

    def test_given_read_recipe_when_opened_then_names_q2_allowlist_and_write_acl_hold(
        self,
    ):
        recipe_text = (
            ROOT / "docs" / "intent-memory" / "read-recipe.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Q2", recipe_text)
        self.assertIn("`pdm`", recipe_text)
        self.assertIn("`user`", recipe_text)
        self.assertIn("WriteAclHold", recipe_text)
        self.assertIn("HITL PARK", recipe_text)
        self.assertIn("seed_fixture", recipe_text)

    def test_given_schema_sql_when_read_then_bot_actor_rows_remain_representable(self):
        text = SCHEMA.read_text(encoding="utf-8")
        self.assertNotIn("actor IN ('pdm','user')", text)
        self.assertNotRegex(text, r"CHECK\s*\(\s*actor\s+IN")
        self.assertIn("actor text NOT NULL", text)


if __name__ == "__main__":
    unittest.main()

