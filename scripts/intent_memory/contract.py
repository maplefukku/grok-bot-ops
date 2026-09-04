from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Sequence

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


class MemoryStore:
    def __init__(self) -> None:
        self._atoms: list[Atom] = []
        self._embedding_dim: int | None = None

    def append(self, draft: AtomDraft) -> Atom:
        if draft.kind is Kind.CRITIQUE_BOT or draft.source is Source.BOT:
            raise IngestOff("bot ingest is off")
        return self._insert(draft)

    def seed_fixture(self, draft: AtomDraft) -> Atom:
        return self._insert(draft)

    def by_tags(
        self,
        tags: Sequence[str],
        *,
        source: Source,
        now: datetime | None = None,
    ) -> list[Atom]:
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
        limit: int,
        now: datetime | None = None,
    ) -> list[Atom]:
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
        atom = Atom(
            id=str(uuid.uuid4()),
            kind=draft.kind,
            source=draft.source,
            tags=tuple(draft.tags),
            body=draft.body,
            related_ids=tuple(draft.related_ids),
            embedding=embedding,
            actor=draft.actor,
            created_at=created_at,
            expires_at=expires_at,
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
