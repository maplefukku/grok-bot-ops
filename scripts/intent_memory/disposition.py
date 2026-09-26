#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from adv_closer import ContractError, Skip, Theme, ThreadRef, Url
from adv_closer import Kind as ThemeKind
from intent_memory.contract import AtomDraft, Kind, Source

DISPOSITIONS = ("reject", "oos", "invalid")
CLOSER_ACTOR = "bot:Closer"
_THREAD_RE = re.compile(
    r"^https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)/pull/(?P<pr>\d+)"
    r"(?:/files(?:/[0-9a-f]+)?)?#(?:discussion_)?r(?P<id>\d+)$"
)
_ISSUE_RE = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+/issues/\d+$")
_HTTP_RE = re.compile(r"^https?://\S+$")


@dataclass(frozen=True)
class Disposition:
    thread: ThreadRef
    theme: Theme
    claim: str
    disposition: str
    verdict: Skip

    def __post_init__(self) -> None:
        object.__setattr__(self, "thread", canonical_thread(str(self.thread)))
        claim = self.claim.strip()
        if not claim or "\n" in claim:
            raise ContractError("claim must be one line")
        object.__setattr__(self, "claim", claim)
        if self.disposition not in DISPOSITIONS:
            raise ContractError(f"unknown disposition: {self.disposition}")
        if not _HTTP_RE.match(str(self.verdict.ref)):
            raise ContractError("ref must be an http(s) URL")
        if self.disposition == "oos" and not _ISSUE_RE.match(str(self.verdict.ref)):
            raise ContractError("oos ref must be the boundary issue URL")

    @property
    def product(self) -> str:
        match = _THREAD_RE.match(str(self.thread))
        assert match is not None
        return match.group("repo")


def canonical_thread(url: str) -> ThreadRef:
    match = _THREAD_RE.match(url.strip())
    if match is None:
        raise ContractError(f"not a PR review thread URL: {url!r}")
    owner, repo, pr, thread_id = match.group("owner", "repo", "pr", "id")
    return ThreadRef(
        f"https://github.com/{owner.lower()}/{repo.lower()}/pull/{pr}"
        f"#discussion_r{thread_id}"
    )


def theme_line(item: Disposition) -> str:
    return f"theme: {item.theme.file} × {item.theme.kind.value} × {item.claim}"


def draft_from_disposition(item: Disposition) -> AtomDraft:
    body = "\n".join((item.verdict.reason, theme_line(item)))
    return AtomDraft(
        kind=Kind.DECISION,
        source=Source.BOT,
        actor=CLOSER_ACTOR,
        tags=("adv", f"disposition:{item.disposition}", f"product:{item.product}"),
        body=body,
        source_url=str(item.thread),
        github_url=str(item.verdict.ref),
        expires_at=None,
    )


def drafts_from_dispositions(items: list[Disposition]) -> list[AtomDraft]:
    seen: set[str] = set()
    drafts: list[AtomDraft] = []
    for item in items:
        if item.thread in seen:
            continue
        seen.add(item.thread)
        drafts.append(draft_from_disposition(item))
    return drafts


def disposition_from_record(record: dict) -> Disposition:
    return Disposition(
        thread=ThreadRef(record["thread"]),
        theme=Theme(file=record["glob"], lines=None, kind=ThemeKind(record["kind"])),
        claim=record["claim"],
        disposition=record["disposition"],
        verdict=Skip(reason=record["reason"], ref=Url(record["ref"])),
    )


def _draft_dict(draft: AtomDraft) -> dict:
    return {
        "kind": draft.kind.value,
        "source": draft.source.value,
        "tags": list(draft.tags),
        "body": draft.body,
        "actor": draft.actor,
        "source_url": draft.source_url,
        "github_url": draft.github_url,
        "expires_at": None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run map Closer disposition records to intent_atom drafts"
    )
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--path", type=Path, required=True)
    args = parser.parse_args(argv)
    records = json.loads(args.path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit(f"{args.path}: root must be a list")
    drafts = drafts_from_dispositions([disposition_from_record(r) for r in records])
    json.dump(
        [_draft_dict(draft) for draft in drafts],
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
