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
    validate_registry_shape,
)


class TestUiLibraryRegistry(unittest.TestCase):
    def test_default_registry_valid_shape(self):
        catalog = RegistryCatalog()
        data = catalog.load()
        errors = validate_registry_shape(data)
        self.assertEqual(errors, [], msg=errors)

    def test_search_by_use_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "$schema": "https://ui.shadcn.com/schema/registry.json",
                        "name": "@fleet-ui",
                        "items": [
                            {
                                "name": "a",
                                "type": "registry:item",
                                "title": "Landing A",
                                "description": "hero layout",
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
                                "description": "tables",
                                "categories": ["dashboard"],
                                "meta": {"fleet": {"useCases": ["dashboard"]}},
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
            self.assertEqual(hits[0].source_url, "https://example.com/a")

    def test_ingest_url_why_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "$schema": "https://ui.shadcn.com/schema/registry.json",
                        "name": "@fleet-ui",
                        "items": [],
                    }
                ),
                encoding="utf-8",
            )
            catalog = RegistryCatalog(path)
            name = ingest_ref(
                catalog,
                IngestInput(
                    url="https://example.com/inspiration",
                    why="Similar spacing to our checkout",
                    use_cases=("checkout",),
                    title="Checkout inspo",
                ),
            )
            self.assertTrue(name.startswith("ref-"))
            item = catalog.get(name)
            assert item is not None
            self.assertEqual(item.why, "Similar spacing to our checkout")
            self.assertIn("checkout", item.use_cases)


if __name__ == "__main__":
    unittest.main()
