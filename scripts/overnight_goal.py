#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Files:
    count: int


@dataclass(frozen=True)
class Lines:
    count: int


@dataclass(frozen=True)
class DomainUnit:
    pass


DiffCap = Files | Lines | DomainUnit

_REGISTRY: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("goal", ("goal", "ゴール")),
    (
        "done-when",
        ("done-when", "done when", "done-criteria", "done criteria", "完了条件"),
    ),
    ("touch scope", ("touch scope", "touch-scope", "scope")),
    ("diff cap", ("diff cap", "diff-cap")),
    ("mid-run verify", ("mid-run verify", "mid run verify", "verify")),
    ("verifier", ("verifier", "independent verifier")),
)
_CANONICALS: tuple[str, ...] = tuple(name for name, _ in _REGISTRY)
_UNBOUNDED = set("*/.")
_DURATION_EN = re.compile(
    r"\b\d+\s*(h|hr|hrs|hour|hours|min|mins|minute|minutes)\b",
    re.IGNORECASE,
)
_DURATION_JA = re.compile(r"\d+\s*(時間|分)")
_DIFF_CAP_RE = re.compile(r"(\d+)\s*(files?|lines?|ファイル|行)", re.IGNORECASE)
_VERIFIER_EN = re.compile(r"\b(self|author|same ca|me)\b", re.IGNORECASE)
_VERIFIER_JA = ("自分", "作者", "同じ CA", "同じCA")
_LIST_PREFIXES = ("- ", "* ", "1. ")


def _norm(heading: str) -> str:
    return " ".join(heading.split()).casefold()


_SPELLING_TO_CANONICAL: dict[str, str] = {
    _norm(spelling): canonical
    for canonical, spellings in _REGISTRY
    for spelling in spellings
}


@dataclass(frozen=True)
class GoalBrief:
    goal: str
    done_when: tuple[str, ...]
    touch_scope: tuple[str, ...]
    diff_cap: DiffCap
    mid_run_verify: str
    verifier: str


class BriefError(ValueError):
    def __init__(self, errors: list[str]) -> None:
        super().__init__(errors)
        self.errors = errors


def _strip_item(line: str) -> str:
    for prefix in _LIST_PREFIXES:
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return line


def _touch_tokens(lines: tuple[str, ...]) -> tuple[str, ...]:
    tokens: list[str] = []
    for line in lines:
        for part in re.split(r"[,\s]+", _strip_item(line)):
            token = part.replace("`", "").strip()
            if token:
                tokens.append(token)
    return tuple(tokens)


def _parse_diff_cap(body: str) -> DiffCap | str:
    match = _DIFF_CAP_RE.search(body)
    if match is not None:
        count = int(match.group(1))
        unit = match.group(2).casefold()
        if unit in {"file", "files", "ファイル"}:
            return Files(count)
        return Lines(count)
    lowered = body.casefold()
    if any(needle in lowered for needle in ("domain-unit", "domain unit", "1 pr", "one pr")):
        return DomainUnit()
    return f"diff cap is neither N files/lines nor domain-unit: {body}"


def _dependent_verifier(body: str) -> bool:
    if _VERIFIER_EN.search(body):
        return True
    return any(needle in body for needle in _VERIFIER_JA)


def _section_lines(text: str) -> dict[str, tuple[str, ...]]:
    found: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and stripped.startswith("## "):
            current = _SPELLING_TO_CANONICAL.get(_norm(stripped[3:]))
            if current is not None:
                found[current] = []
            continue
        if current is not None and stripped:
            found[current].append(stripped)
    return {name: tuple(lines) for name, lines in found.items()}


def _collect(text: str) -> tuple[list[str], GoalBrief | None]:
    sections = _section_lines(text)
    errors: list[str] = []
    goal = ""
    done_when: tuple[str, ...] = ()
    touch_scope: tuple[str, ...] = ()
    diff_cap: DiffCap | None = None
    mid_run_verify = ""
    verifier = ""
    for canonical in _CANONICALS:
        lines = sections.get(canonical)
        if lines is None:
            errors.append(f"missing ## {canonical}")
            continue
        if not lines:
            errors.append(f"empty ## {canonical}")
            continue
        body = " ".join(lines)
        if canonical == "goal":
            goal = body
        elif canonical == "done-when":
            done_when = tuple(_strip_item(line) for line in lines)
            for entry in done_when:
                if _DURATION_EN.search(entry) or _DURATION_JA.search(entry):
                    errors.append(f"done-when is a duration, not a predicate: {entry}")
        elif canonical == "touch scope":
            touch_scope = _touch_tokens(lines)
            for token in touch_scope:
                if set(token) <= _UNBOUNDED:
                    errors.append(f"touch scope is unbounded: {token}")
        elif canonical == "diff cap":
            parsed = _parse_diff_cap(body)
            if isinstance(parsed, str):
                errors.append(parsed)
            else:
                diff_cap = parsed
        elif canonical == "mid-run verify":
            mid_run_verify = body
            if "quiet-test.sh --" not in body:
                errors.append(
                    f"mid-run verify must run through quiet-test.sh -- <cmd>: {body}"
                )
        else:
            verifier = body
            if _dependent_verifier(body):
                errors.append(f"verifier is not independent: {body}")
    if errors:
        return errors, None
    assert diff_cap is not None
    return [], GoalBrief(
        goal=goal,
        done_when=done_when,
        touch_scope=touch_scope,
        diff_cap=diff_cap,
        mid_run_verify=mid_run_verify,
        verifier=verifier,
    )


def parse_brief(text: str) -> GoalBrief:
    errors, brief = _collect(text)
    if errors or brief is None:
        raise BriefError(errors)
    return brief


def brief_errors(text: str) -> list[str]:
    errors, _brief = _collect(text)
    return errors


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: overnight_goal.py <path> [<path> ...]", file=sys.stderr)
        return 2
    failed = False
    for raw in args:
        text = sys.stdin.read() if raw == "-" else Path(raw).read_text(encoding="utf-8")
        errors = brief_errors(text)
        if errors:
            failed = True
            print(f"FAIL {raw}")
            for item in errors:
                print(f"  {item}")
        else:
            print(f"ok   {raw}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
