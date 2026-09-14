#!/usr/bin/env python3
"""CLI query/get for fleet ui-library index (MCP seat is shadcn CLI — see docs/process/ui-library-mcp.md)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ui_library.registry_core import RegistryCatalog  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fleet UI library registry query/get")
    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Path to registry.json (default: scripts/ui_library/data/registry.json)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_p = sub.add_parser("list", help="List item names")
    list_p.add_argument("--limit", type=int, default=50)
    list_p.add_argument("--offset", type=int, default=0)

    search_p = sub.add_parser("search", help="Search by text and optional use-case")
    search_p.add_argument("query", nargs="?", default="")
    search_p.add_argument("--use-case", dest="use_case", default=None)
    search_p.add_argument("--limit", type=int, default=20)
    search_p.add_argument("--offset", type=int, default=0)

    get_p = sub.add_parser("get", help="Get one item by registry name")
    get_p.add_argument("name")

    args = parser.parse_args(argv)
    catalog = RegistryCatalog(args.registry)

    if args.cmd == "list":
        names = catalog.list_names()[args.offset : args.offset + args.limit]
        print(json.dumps({"items": names}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "search":
        hits = catalog.search(
            args.query,
            use_case=args.use_case,
            limit=args.limit,
            offset=args.offset,
        )
        print(
            json.dumps(
                {"query": args.query, "useCase": args.use_case, "items": [h.as_public() for h in hits]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.cmd == "get":
        item = catalog.get(args.name)
        if item is None:
            print(json.dumps({"error": "not_found", "name": args.name}), file=sys.stderr)
            return 1
        print(json.dumps(item.as_public(), ensure_ascii=False, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
