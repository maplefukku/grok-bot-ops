#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from intent_memory import Atom, AtomDraft, Kind, MemoryStore, Source


def _parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def _load_fixture(path: Path, store: MemoryStore) -> None:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit(f"{path}: fixture root must be a list")
    for row in rows:
        embedding = row.get("embedding")
        store.seed_fixture(
            AtomDraft(
                kind=Kind(row["kind"]),
                tags=tuple(row["tags"]),
                body=row["body"],
                actor=row["actor"],
                embedding=tuple(embedding) if embedding is not None else None,
                source=Source(row.get("source", "human")),
                related_ids=tuple(row.get("related_ids") or ()),
                created_at=_parse_time(row.get("created_at")),
                expires_at=_parse_time(row.get("expires_at")),
            )
        )


def _atom_dict(atom: Atom) -> dict:
    return {
        "id": atom.id,
        "kind": atom.kind.value,
        "source": atom.source.value,
        "tags": list(atom.tags),
        "body": atom.body,
        "related_ids": list(atom.related_ids),
        "embedding": list(atom.embedding) if atom.embedding is not None else None,
        "actor": atom.actor,
        "created_at": atom.created_at.isoformat(),
        "expires_at": atom.expires_at.isoformat() if atom.expires_at else None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read intent_atom rows from a fixture")
    parser.add_argument("--tags", nargs="+", default=None)
    parser.add_argument("--vector", nargs="+", type=float, default=None)
    parser.add_argument("-n", "--n", type=int, default=5)
    parser.add_argument("--source", default="human", choices=("human", "bot"))
    parser.add_argument("--fixture", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.vector is None and not args.tags:
        parser.error("provide --tags, --vector, or both")
    store = MemoryStore()
    _load_fixture(args.fixture, store)
    source = Source(args.source)
    if args.vector is not None:
        atoms = store.similar(args.vector, source=source, limit=args.n)
        if args.tags:
            wanted = tuple(args.tags)
            atoms = [
                atom
                for atom in atoms
                if all(tag in atom.tags for tag in wanted)
            ]
    else:
        atoms = store.by_tags(args.tags, source=source)[: args.n]
    json.dump(
        [_atom_dict(atom) for atom in atoms],
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
