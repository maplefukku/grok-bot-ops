from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Mapping, Sequence

FEELING_TTL_DAYS = 90


class Kind(Enum):
    INTENT = "intent"
    DECISION = "decision"
    BELIEF = "belief"
    FEELING = "feeling"
    CRITIQUE_HUMAN = "critique_human"
    CRITIQUE_BOT = "critique_bot"


class Source(Enum):
    HUMAN = "human"
    BOT = "bot"


class ContractError(ValueError):
    pass


class IngestOff(Exception):
    pass


class WriteAclHold(Exception):
    pass


class ReadAclHold(Exception):
    pass


class DeleteAclHold(Exception):
    pass


HUMAN_WRITE_ACTORS = frozenset({"pdm", "user"})
HUMAN_DELETE_ACTORS = HUMAN_WRITE_ACTORS

READ_ACL: Mapping[str, frozenset[Source]] = {
    "pdm": frozenset({Source.HUMAN, Source.BOT}),
    "user": frozenset({Source.HUMAN, Source.BOT}),
    "planner": frozenset({Source.HUMAN}),
    "kanshi": frozenset({Source.HUMAN}),
    "cli": frozenset({Source.HUMAN}),
}


def _check_read(reader: str, source: Source) -> None:
    if source not in READ_ACL.get(reader, frozenset()):
        raise ReadAclHold(
            f"HITL HOLD: reader {reader!r} may not read source={source.value}"
        )


def _check_delete(actor: str) -> None:
    if actor not in HUMAN_DELETE_ACTORS:
        raise DeleteAclHold("HITL PARK: actor is not an allowlisted human deleter")


EDGE_URL_KEYS = ("source_url", "github_url", "gb_url")
HUMAN_KINDS = (
    Kind.INTENT,
    Kind.DECISION,
    Kind.BELIEF,
    Kind.FEELING,
    Kind.CRITIQUE_HUMAN,
)


@dataclass(frozen=True)
class AtomDraft:
    kind: Kind
    tags: tuple[str, ...]
    body: str
    actor: str
    embedding: tuple[float, ...] | None = None
    source: Source = Source.HUMAN
    related_ids: tuple[str, ...] = ()
    created_at: datetime | None = None
    expires_at: datetime | None = None
    source_url: str | None = None
    github_url: str | None = None
    gb_url: str | None = None


@dataclass(frozen=True)
class Atom:
    id: str
    kind: Kind
    source: Source
    tags: tuple[str, ...]
    body: str
    related_ids: tuple[str, ...]
    embedding: tuple[float, ...] | None
    actor: str
    created_at: datetime
    expires_at: datetime | None
    source_url: str | None = None
    github_url: str | None = None
    gb_url: str | None = None


def _cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    dot = 0.0
    n_left = 0.0
    n_right = 0.0
    for a, b in zip(left, right, strict=True):
        dot += a * b
        n_left += a * a
        n_right += b * b
    if n_left == 0.0 or n_right == 0.0:
        return 0.0
    return dot / math.sqrt(n_left * n_right)


def _as_embedding(value: Sequence[float] | None) -> tuple[float, ...] | None:
    if value is None:
        return None
    return tuple(float(x) for x in value)


def _pairing_ok(kind: Kind, source: Source) -> bool:
    return (kind is Kind.CRITIQUE_BOT) is (source is Source.BOT)


def _clean_url(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _parse_edge_urls(body: str) -> dict[str, str | None]:
    found = {key: None for key in EDGE_URL_KEYS}
    for line in body.splitlines():
        for key in EDGE_URL_KEYS:
            prefix = f"{key}:"
            if line.startswith(prefix):
                found[key] = _clean_url(line[len(prefix) :])
    return found


def _merge_edge_urls(
    body: str,
    source_url: str | None,
    github_url: str | None,
    gb_url: str | None,
) -> str:
    incoming = {
        "source_url": _clean_url(source_url),
        "github_url": _clean_url(github_url),
        "gb_url": _clean_url(gb_url),
    }
    kept: list[str] = []
    for line in body.splitlines():
        matched = next(
            (key for key in EDGE_URL_KEYS if line.startswith(f"{key}:")),
            None,
        )
        if matched is not None and incoming.get(matched):
            continue
        kept.append(line)
    for key in EDGE_URL_KEYS:
        value = incoming[key]
        if value:
            kept.append(f"{key}: {value}")
    return "\n".join(kept)


class MemoryStore:
    def __init__(self) -> None:
        self._atoms: list[Atom] = []
        self._embedding_dim: int | None = None

    def append(self, draft: AtomDraft) -> Atom:
        if draft.kind is Kind.CRITIQUE_BOT or draft.source is Source.BOT:
            raise IngestOff("bot ingest is off")
        if draft.actor not in HUMAN_WRITE_ACTORS:
            raise WriteAclHold("HITL PARK: actor is not an allowlisted human writer")
        return self._insert(draft)

    def seed_fixture(self, draft: AtomDraft) -> Atom:
        return self._insert(draft)

    def delete(self, atom_id: str, *, actor: str) -> Atom:
        _check_delete(actor)
        atom = next((item for item in self._atoms if item.id == atom_id), None)
        if atom is None:
            raise ContractError("delete requires an existing atom")
        if atom.source is Source.BOT:
            raise DeleteAclHold("HITL HOLD: bot rows may not be deleted")
        if atom.kind is Kind.CRITIQUE_HUMAN:
            raise ContractError("critique_human must not be deleted")
        self._atoms.remove(atom)
        return atom

    def by_tags(
        self,
        tags: Sequence[str],
        *,
        source: Source,
        reader: str,
        now: datetime | None = None,
    ) -> list[Atom]:
        _check_read(reader, source)
        as_of = now if now is not None else datetime.now(timezone.utc)
        wanted = tuple(tags)
        if not wanted:
            raise ContractError("by_tags requires at least one tag")
        return [
            atom
            for atom in self._atoms
            if atom.source is source
            and not _expired(atom, as_of)
            and all(tag in atom.tags for tag in wanted)
        ]

    def similar(
        self,
        vector: Sequence[float],
        *,
        source: Source,
        reader: str,
        limit: int,
        now: datetime | None = None,
    ) -> list[Atom]:
        _check_read(reader, source)
        as_of = now if now is not None else datetime.now(timezone.utc)
        query = tuple(float(x) for x in vector)
        scored: list[tuple[float, Atom]] = []
        for atom in self._atoms:
            if atom.source is not source or _expired(atom, as_of):
                continue
            if atom.embedding is None or len(atom.embedding) != len(query):
                continue
            scored.append((_cosine_similarity(query, atom.embedding), atom))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [atom for _, atom in scored[:limit]]

    def _insert(self, draft: AtomDraft) -> Atom:
        if not _pairing_ok(draft.kind, draft.source):
            raise ContractError("kind/source pairing violated")
        created_at = draft.created_at or datetime.now(timezone.utc)
        expires_at = _resolve_expiry(draft.kind, created_at, draft.expires_at)
        embedding = _as_embedding(draft.embedding)
        if embedding is not None:
            if self._embedding_dim is None:
                self._embedding_dim = len(embedding)
            elif len(embedding) != self._embedding_dim:
                raise ContractError("embedding dimension mismatch")
        body = _merge_edge_urls(
            draft.body,
            draft.source_url,
            draft.github_url,
            draft.gb_url,
        )
        edges = _parse_edge_urls(body)
        atom = Atom(
            id=str(uuid.uuid4()),
            kind=draft.kind,
            source=draft.source,
            tags=tuple(draft.tags),
            body=body,
            related_ids=tuple(draft.related_ids),
            embedding=embedding,
            actor=draft.actor,
            created_at=created_at,
            expires_at=expires_at,
            source_url=edges["source_url"],
            github_url=edges["github_url"],
            gb_url=edges["gb_url"],
        )
        self._atoms.append(atom)
        return atom


def _expired(atom: Atom, now: datetime) -> bool:
    return atom.expires_at is not None and atom.expires_at <= now


def _resolve_expiry(
    kind: Kind,
    created_at: datetime,
    expires_at: datetime | None,
) -> datetime | None:
    if kind is Kind.FEELING:
        if expires_at is None:
            return created_at + timedelta(days=FEELING_TTL_DAYS)
        return expires_at
    if kind is Kind.CRITIQUE_HUMAN and expires_at is not None:
        raise ContractError("critique_human must not expire")
    return expires_at
