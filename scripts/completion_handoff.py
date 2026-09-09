#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import ClassVar, NewType

KIND = "EVAL-READY"
FIELDS = ("kind", "date_jst", "branch", "pr", "counts", "hold")
DESTINATIONS = ("PdM", "編成評価")
LEDGER_REPO = "maplefukku/grok-bot-ops"
NONE_MARK = "無し"
NO_CHANGE_MARK = "変更なし"

Branch = NewType("Branch", str)
Label = NewType("Label", str)
HoldRef = NewType("HoldRef", str)

_PR_URL_PREFIX = f"https://github.com/{LEDGER_REPO}/pull/"


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Stacked:
    pr: int

    def __post_init__(self) -> None:
        if self.pr < 1:
            raise ContractError("pr is not positive")


@dataclass(frozen=True)
class NoChange:
    pass


Outcome = Stacked | NoChange


def daily_branch(date_jst: date) -> Branch:
    return Branch(f"ops/daily-{date_jst.isoformat()}")


def pr_url(pr: int) -> str:
    return f"https://github.com/{LEDGER_REPO}/pull/{pr}"


@dataclass(frozen=True)
class Counts:
    items: tuple[tuple[Label, int], ...]

    def __post_init__(self) -> None:
        seen: set[str] = set()
        normalized: list[tuple[Label, int]] = []
        for label, n in self.items:
            text = str(label).strip()
            if not text:
                raise ContractError("count label is empty")
            if text in seen:
                raise ContractError(f"duplicate count label: {text}")
            if n < 0:
                raise ContractError(f"count {text} is negative")
            seen.add(text)
            normalized.append((Label(text), n))
        object.__setattr__(self, "items", tuple(normalized))

    def total(self) -> int:
        return sum(n for _, n in self.items)


@dataclass(frozen=True)
class Handoff:
    date_jst: date
    outcome: Outcome
    counts: Counts
    hold: tuple[HoldRef, ...]
    branch: Branch | None = field(default=None)
    kind: ClassVar[str] = KIND

    def __post_init__(self) -> None:
        expected = daily_branch(self.date_jst)
        if self.branch is None:
            object.__setattr__(self, "branch", expected)
        elif self.branch != expected:
            raise ContractError(f"branch does not match date_jst: {self.branch}")
        seen: set[str] = set()
        hold: list[HoldRef] = []
        for ref in self.hold:
            text = str(ref).strip()
            if not text:
                raise ContractError("hold ref is empty")
            if text in seen:
                raise ContractError(f"duplicate hold ref: {text}")
            seen.add(text)
            hold.append(HoldRef(text))
        object.__setattr__(self, "hold", tuple(hold))
        if isinstance(self.outcome, NoChange) and self.counts.total() != 0:
            raise ContractError("変更なし with non-zero counts")


def _render_pr(outcome: Outcome) -> str:
    if isinstance(outcome, Stacked):
        return pr_url(outcome.pr)
    return NO_CHANGE_MARK


def _render_counts(counts: Counts) -> str:
    if not counts.items:
        return NONE_MARK
    return ", ".join(f"{label} {n}" for label, n in counts.items)


def _render_hold(hold: tuple[HoldRef, ...]) -> str:
    if not hold:
        return NONE_MARK
    return " ".join(str(ref) for ref in hold)


def render(handoff: Handoff) -> str:
    values = {
        "kind": KIND,
        "date_jst": handoff.date_jst.isoformat(),
        "branch": str(handoff.branch),
        "pr": _render_pr(handoff.outcome),
        "counts": _render_counts(handoff.counts),
        "hold": _render_hold(handoff.hold),
    }
    return "\n".join(f"{name}: {values[name]}" for name in FIELDS)


def _parse_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ContractError(f"date_jst is not YYYY-MM-DD: {value}") from None
    if parsed.isoformat() != value:
        raise ContractError(f"date_jst is not YYYY-MM-DD: {value}")
    return parsed


def _parse_pr(value: str) -> Outcome:
    if value == NO_CHANGE_MARK:
        return NoChange()
    number: int | None = None
    if value.startswith("#") and value[1:].isdigit():
        number = int(value[1:])
    elif value.startswith(_PR_URL_PREFIX):
        rest = value[len(_PR_URL_PREFIX) :]
        if rest.isdigit() and value == pr_url(int(rest)):
            number = int(rest)
    elif value.isdigit():
        number = int(value)
    if number is not None and number >= 1:
        return Stacked(number)
    raise ContractError(f"pr is not a ledger PR: {value}")


def _parse_counts(value: str) -> Counts:
    if value == NONE_MARK:
        return Counts(items=())
    items: list[tuple[Label, int]] = []
    for chunk in value.split(","):
        piece = chunk.strip()
        label_s, sep, n_s = piece.rpartition(" ")
        label_s = label_s.strip()
        n_s = n_s.strip()
        if not sep or not label_s or not n_s:
            raise ContractError(f"counts is malformed: {value}")
        try:
            n = int(n_s)
        except ValueError:
            raise ContractError(f"counts is malformed: {value}") from None
        items.append((Label(label_s), n))
    if not items:
        raise ContractError(f"counts is malformed: {value}")
    return Counts(items=tuple(items))


def _parse_hold(value: str) -> tuple[HoldRef, ...]:
    if value == NONE_MARK:
        return ()
    return tuple(HoldRef(part) for part in value.split())


def _entries(text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        name, sep, raw = line.partition(":")
        name = name.strip()
        if not sep or name not in FIELDS:
            raise ContractError(f"unknown field: {name or line.strip()}")
        entries.append((name, raw.strip()))
    return entries


def parse(text: str) -> Handoff:
    entries = _entries(text)
    names = [name for name, _ in entries]
    for name in FIELDS:
        if name not in names:
            raise ContractError(f"missing field: {name}")
    for name in names:
        if names.count(name) > 1:
            raise ContractError(f"duplicate field: {name}")
    for name, expected in zip(names, FIELDS):
        if name != expected:
            raise ContractError(f"field out of order: {name}")
    values = dict(entries)
    kind = values["kind"]
    if kind != KIND:
        raise ContractError(f"kind is not EVAL-READY: {kind}")
    date_jst = _parse_date(values["date_jst"])
    return Handoff(
        date_jst=date_jst,
        outcome=_parse_pr(values["pr"]),
        counts=_parse_counts(values["counts"]),
        hold=_parse_hold(values["hold"]),
        branch=Branch(values["branch"]),
    )


@dataclass(frozen=True)
class Delivered:
    to: tuple[str, ...]
    body: str


@dataclass(frozen=True)
class Suppressed:
    date_jst: date


FanOut = Delivered | Suppressed


def fan_out(handoff: Handoff, sent: frozenset[date]) -> FanOut:
    if handoff.date_jst in sent:
        return Suppressed(handoff.date_jst)
    return Delivered(to=DESTINATIONS, body=render(handoff))


def lock_errors(text: str, needles: tuple[str, ...]) -> list[str]:
    return [f"missing {n}" for n in needles if n not in text]
