#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, NewType

ThreadRef = NewType("ThreadRef", str)
Commit = NewType("Commit", str)
Url = NewType("Url", str)

ADV_THRASH = "adv-thrash"


class ContractError(ValueError):
    pass


class Kind(Enum):
    FAILING_TEST = "failing test"
    CONTRACT_BREAK = "contract break"
    SECURITY = "security"
    STYLE = "style"
    EXTRA_DOCS = "extra docs"
    RENAME = "rename"


MUST_KINDS = frozenset({Kind.FAILING_TEST, Kind.CONTRACT_BREAK, Kind.SECURITY})
NIT_KINDS = frozenset({Kind.STYLE, Kind.EXTRA_DOCS, Kind.RENAME})


class Weight(Enum):
    MUST = "MUST"
    NIT = "NIT"


class History(Enum):
    FRESH = "fresh"
    ANSWERED = "answered"
    REOPENED = "reopened"


@dataclass(frozen=True)
class Theme:
    file: str
    lines: tuple[int, int] | None
    kind: Kind

    def __post_init__(self) -> None:
        if not self.file.strip():
            raise ContractError("theme file is empty")
        if self.lines is not None and self.lines[0] > self.lines[1]:
            raise ContractError("theme lines are inverted")


@dataclass(frozen=True)
class Prior:
    thread: ThreadRef
    theme: Theme


def _one_sentence(reason: str) -> str:
    text = reason.strip()
    if not text:
        raise ContractError("reason is empty")
    if "。" in text:
        raise ContractError("reason is not one sentence")
    return text


def _non_empty(value: str, name: str) -> str:
    text = value.strip()
    if not text:
        raise ContractError(f"{name} is empty")
    return text


@dataclass(frozen=True)
class Fix:
    commit: Commit
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "commit", Commit(_non_empty(str(self.commit), "commit")))
        object.__setattr__(self, "reason", _one_sentence(self.reason))


@dataclass(frozen=True)
class Skip:
    reason: str
    ref: Url

    def __post_init__(self) -> None:
        object.__setattr__(self, "reason", _one_sentence(self.reason))
        object.__setattr__(self, "ref", Url(_non_empty(str(self.ref), "ref")))


Verdict = Fix | Skip


@dataclass(frozen=True)
class Fact:
    thread: ThreadRef
    theme: Theme
    new_failing_check: bool
    history: History
    human_hold: bool
    prior: tuple[Prior, ...]
    verdict: Verdict | None = None

    def __post_init__(self) -> None:
        if not str(self.thread).strip():
            raise ContractError("thread is empty")
        if any(item.thread == self.thread for item in self.prior):
            raise ContractError("thread appears in prior")


@dataclass(frozen=True)
class Keep:
    pass


@dataclass(frozen=True)
class Owed:
    weight: Weight


@dataclass(frozen=True)
class Must:
    close: Verdict


@dataclass(frozen=True)
class Nit:
    reply: str


@dataclass(frozen=True)
class Thrash:
    prior: ThreadRef
    label: ClassVar[str] = ADV_THRASH


@dataclass(frozen=True)
class Dup:
    prior: ThreadRef


Decision = Keep | Owed | Must | Nit | Thrash | Dup


class State(Enum):
    RESOLVED = "resolved"
    OWED = "owed"
    HOLD = "hold"


@dataclass(frozen=True)
class ThreadState:
    thread: ThreadRef
    weight: Weight
    state: State
    replies: int
    label: str | None = None

    def __post_init__(self) -> None:
        if self.replies < 0:
            raise ContractError("replies is negative")
        if self.weight is Weight.NIT and self.replies > 1:
            raise ContractError("NIT replies exceed 1")
        if self.label is not None and self.label != ADV_THRASH:
            raise ContractError(f"unknown label: {self.label}")

    @property
    def terminal(self) -> bool:
        return self.state is State.RESOLVED


def weight_of(fact: Fact) -> Weight:
    if fact.new_failing_check or fact.theme.kind in MUST_KINDS:
        return Weight.MUST
    return Weight.NIT


_SETTLE = {
    Keep: (State.HOLD, 0, None),
    Owed: (State.OWED, 0, None),
    Must: (State.RESOLVED, 1, None),
    Nit: (State.RESOLVED, 1, None),
    Thrash: (State.RESOLVED, 0, Thrash.label),
    Dup: (State.RESOLVED, 0, None),
}


def settle(fact: Fact) -> ThreadState:
    before = 0 if fact.history is History.FRESH else 1
    state, delta, label = _SETTLE[type(decide(fact))]
    return ThreadState(
        thread=fact.thread,
        weight=weight_of(fact),
        state=state,
        replies=before + delta,
        label=label,
    )


MUST_ROW = "MUST threads"
NIT_ROW = "NIT threads"


@dataclass(frozen=True)
class Row:
    name: str
    blockers: tuple[ThreadRef, ...]

    @property
    def ok(self) -> bool:
        return not self.blockers


def closer_rows(states: Iterable[ThreadState]) -> tuple[Row, Row]:
    must: list[ThreadRef] = []
    nit: list[ThreadRef] = []
    for item in states:
        if item.terminal:
            continue
        if item.weight is Weight.MUST:
            must.append(item.thread)
        else:
            nit.append(item.thread)
    return (
        Row(name=MUST_ROW, blockers=tuple(must)),
        Row(name=NIT_ROW, blockers=tuple(nit)),
    )


def _must_path(fact: Fact) -> Decision:
    if fact.verdict is None:
        return Owed(weight=Weight.MUST)
    return Must(close=fact.verdict)


def _nit_line(verdict: Verdict) -> str:
    if isinstance(verdict, Fix):
        return f"NIT 直す。{verdict.reason}。{verdict.commit}。resolve。"
    return f"NIT 直さない。{verdict.reason}。{verdict.ref}。resolve。"


def _nit_path(fact: Fact) -> Decision:
    if fact.verdict is None:
        return Owed(weight=Weight.NIT)
    return Nit(reply=_nit_line(fact.verdict))


def _repeat_of(fact: Fact) -> ThreadRef | None:
    """Reopen guard: REOPENED without a new failing check repeats self -> Thrash."""
    for item in fact.prior:
        if item.theme == fact.theme:
            return item.thread
    if fact.history is History.REOPENED:
        return fact.thread
    return None


def decide(fact: Fact) -> Decision:
    if fact.human_hold:
        return Keep()
    if fact.history is History.ANSWERED:
        return Dup(prior=fact.thread)  # reopen guard: no ping-pong after Closer replied
    if fact.new_failing_check:
        return _must_path(fact)
    repeat = _repeat_of(fact)
    if repeat is not None:
        if fact.theme.kind in NIT_KINDS:
            return Thrash(prior=repeat)
        if fact.theme.kind in MUST_KINDS:
            return Dup(prior=repeat)
        raise ContractError(f"unknown kind: {fact.theme.kind}")
    if fact.theme.kind in MUST_KINDS:
        return _must_path(fact)
    if fact.theme.kind in NIT_KINDS:
        return _nit_path(fact)
    raise ContractError(f"unknown kind: {fact.theme.kind}")
