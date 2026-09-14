#!/usr/bin/env python3
"""Fleet WRAP for shadcn MCP: search / view / examples (seat = npx shadcn@latest mcp)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ui_library.registry_core import RegistryCatalog  # noqa: E402

MCP_WRAP = {
    "search": "search_items_in_registries",
    "view": "view_items_in_registries",
    "examples": "get_item_examples_from_registries",
    "list": "list_items_in_registries",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fleet @ui-refs query WRAP (shadcn MCP tools)")
    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Path to registry.json (default: scripts/ui_library/data/registry.json)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_p = sub.add_parser("list", help=f"MCP WRAP: {MCP_WRAP['list']}")
    list_p.add_argument("--limit", type=int, default=50)
    list_p.add_argument("--offset", type=int, default=0)

    search_p = sub.add_parser("search", help=f"MCP WRAP: {MCP_WRAP['search']}")
    search_p.add_argument("query", nargs="?", default="")
    search_p.add_argument("--use-case", dest="use_case", default=None)
    search_p.add_argument("--limit", type=int, default=20)
    search_p.add_argument("--offset", type=int, default=0)

    view_p = sub.add_parser("view", help=f"MCP WRAP: {MCP_WRAP['view']}")
    view_p.add_argument("name")

    ex_p = sub.add_parser("examples", help=f"MCP WRAP: {MCP_WRAP['examples']}")
    ex_p.add_argument("query")
    ex_p.add_argument("--use-case", dest="use_case", default=None)
    ex_p.add_argument("--limit", type=int, default=10)

    get_p = sub.add_parser("get", help="Alias of view (public summary fields)")
    get_p.add_argument("name")

    args = parser.parse_args(argv)
    catalog = RegistryCatalog(args.registry)

    if args.cmd == "list":
        names = catalog.list_names()[args.offset : args.offset + args.limit]
        print(json.dumps({"mcpTool": MCP_WRAP["list"], "items": names}, ensure_ascii=False, indent=2))
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
                {
                    "mcpTool": MCP_WRAP["search"],
                    "query": args.query,
                    "useCase": args.use_case,
                    "items": [h.as_public() for h in hits],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.cmd == "view":
        payload = catalog.view(args.name)
        if payload is None:
            print(json.dumps({"error": "not_found", "name": args.name}), file=sys.stderr)
            return 1
        print(json.dumps({"mcpTool": MCP_WRAP["view"], "item": payload}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "examples":
        hits = catalog.examples(args.query, use_case=args.use_case, limit=args.limit)
        print(
            json.dumps(
                {
                    "mcpTool": MCP_WRAP["examples"],
                    "query": args.query,
                    "useCase": args.use_case,
                    "items": [h.as_public() for h in hits],
                },
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
