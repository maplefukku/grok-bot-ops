#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ui_library.ingest import IngestInput, ingest_ref  # noqa: E402
from ui_library.registry_core import (  # noqa: E402
    RegistryCatalog,
    RegistryError,
    slug_from_url,
    validate_item_name,
    validate_registry_shape,
)


def _empty_registry(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "$schema": "https://ui.shadcn.com/schema/registry.json",
                "name": "@ui-refs",
                "items": [],
            }
        ),
        encoding="utf-8",
    )


class TestUiLibraryRegistry(unittest.TestCase):
    def test_default_registry_valid_shape(self):
        catalog = RegistryCatalog()
        data = catalog.load()
        errors = validate_registry_shape(data)
        self.assertEqual(errors, [], msg=errors)

    def test_search_finds_source_url_in_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "$schema": "https://ui.shadcn.com/schema/registry.json",
                        "name": "@ui-refs",
                        "items": [
                            {
                                "name": "ref-example-com-page",
                                "type": "registry:item",
                                "title": "Example page",
                                "description": "Nice spacing URL: https://example.com/page",
                                "categories": ["landing"],
                                "meta": {
                                    "fleet": {
                                        "sourceUrl": "https://example.com/page",
                                        "ingestedWhy": "Nice spacing",
                                        "useCases": ["landing"],
                                    }
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            catalog = RegistryCatalog(path)
            hits = catalog.search("example.com/page")
            self.assertEqual(len(hits), 1)

    def test_search_by_use_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "$schema": "https://ui.shadcn.com/schema/registry.json",
                        "name": "@ui-refs",
                        "items": [
                            {
                                "name": "a",
                                "type": "registry:item",
                                "title": "Landing A",
                                "description": "hero layout URL: https://example.com/a",
                                "categories": ["landing"],
                                "meta": {
                                    "fleet": {
                                        "useCases": ["landing"],
                                        "sourceUrl": "https://example.com/a",
                                        "ingestedWhy": "close hero",
                                    }
                                },
                            },
                            {
                                "name": "b",
                                "type": "registry:item",
                                "title": "Dashboard B",
                                "description": "tables URL: https://example.com/b",
                                "categories": ["dashboard"],
                                "meta": {
                                    "fleet": {
                                        "useCases": ["dashboard"],
                                        "sourceUrl": "https://example.com/b",
                                        "ingestedWhy": "tables",
                                    }
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            catalog = RegistryCatalog(path)
            hits = catalog.search("hero", use_case="landing")
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0].name, "a")

    def test_ingest_writes_disk_json_readable_by_fresh_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            _empty_registry(path)
            catalog = RegistryCatalog(path)
            name = ingest_ref(
                catalog,
                IngestInput(
                    url="https://example.com/inspiration",
                    why="Similar spacing to our checkout",
                    use_cases=("checkout",),
                ),
            )
            disk_path = path.parent / f"{name}.json"
            self.assertTrue(disk_path.is_file())
            fresh = RegistryCatalog(path)
            viewed = fresh.view(name)
            assert viewed is not None
            self.assertEqual(
                viewed["meta"]["fleet"]["sourceUrl"], "https://example.com/inspiration"
            )
            self.assertIn("mcpWirePath", viewed)

    def test_ingest_rejects_bad_url_and_empty_why(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            _empty_registry(path)
            catalog = RegistryCatalog(path)
            with self.assertRaises(RegistryError):
                ingest_ref(catalog, IngestInput(url="ftp://bad", why="x"))
            with self.assertRaises(RegistryError):
                ingest_ref(
                    catalog, IngestInput(url="https://example.com", why="   ")
                )

    def test_item_name_path_traversal_and_reserved(self):
        with self.assertRaises(RegistryError):
            validate_item_name("../evil")
        with self.assertRaises(RegistryError):
            validate_item_name("registry")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            _empty_registry(path)
            catalog = RegistryCatalog(path)
            with self.assertRaises(RegistryError):
                ingest_ref(
                    catalog,
                    IngestInput(url="https://example.com/x", why="why"),
                    name="../escaped",
                )

    def test_slug_includes_query_to_avoid_collision(self):
        a = slug_from_url("https://example.com/page?a=1")
        b = slug_from_url("https://example.com/page?b=2")
        self.assertNotEqual(a, b)

    def test_duplicate_names_fail_validation(self):
        data = {
            "$schema": "https://ui.shadcn.com/schema/registry.json",
            "name": "@ui-refs",
            "items": [
                {
                    "name": "dup",
                    "type": "registry:item",
                    "description": "one URL: https://a.example",
                    "meta": {
                        "fleet": {
                            "sourceUrl": "https://a.example",
                            "ingestedWhy": "a",
                        }
                    },
                },
                {
                    "name": "dup",
                    "type": "registry:item",
                    "description": "two URL: https://b.example",
                    "meta": {
                        "fleet": {
                            "sourceUrl": "https://b.example",
                            "ingestedWhy": "b",
                        }
                    },
                },
            ],
        }
        errors = validate_registry_shape(data)
        self.assertTrue(any("duplicate" in e for e in errors))

    def test_fixture_sample_search_and_get(self):
        catalog = RegistryCatalog()
        hits = catalog.search("ui.shadcn.com/blocks")
        names = [h.name for h in hits]
        self.assertIn("ref-fixture-x-ui-blocks-hero", names)

    def test_buddy_seed_search_view(self):
        catalog = RegistryCatalog()
        hits = catalog.search("ui.shadcn.com/docs/mcp", use_case="workflow")
        names = [h.name for h in hits]
        self.assertIn("ref-seed-buddy-taiyo-find-index-mcp", names)
        viewed = catalog.view("ref-seed-buddy-taiyo-find-index-mcp")
        assert viewed is not None
        self.assertIn("meta", viewed)
        self.assertEqual(
            viewed["meta"]["fleet"]["sourceUrl"], "https://ui.shadcn.com/docs/mcp"
        )

    def test_view_and_examples_mcp_wrap(self):
        catalog = RegistryCatalog()
        viewed = catalog.view("ref-fixture-x-ui-blocks-hero")
        assert viewed is not None
        self.assertEqual(viewed.get("registry"), "@ui-refs")
        examples = catalog.examples("FIXTURE", use_case="landing")
        names = [e.name for e in examples]
        self.assertIn("ref-fixture-x-ui-blocks-hero", names)

    def test_ingest_kebab_use_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            _empty_registry(path)
            catalog = RegistryCatalog(path)
            ingest_ref(
                catalog,
                IngestInput(
                    url="https://example.com/x",
                    why="Indexed description for search.",
                    use_cases=("Marketing Site",),
                ),
            )
            item = catalog.get(list(catalog.list_names())[0])
            assert item is not None
            self.assertEqual(item.use_cases, ("marketing-site",))


if __name__ == "__main__":
    unittest.main()
