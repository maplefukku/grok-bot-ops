#!/usr/bin/env python3
"""Local and CI checks for this Markdown + plugin.json ops repo.

Checks:
  1. Relative Markdown / image links resolve on disk
  2. docs/knowhow forbids 「リンク要補完」 and requires an http(s) source
  3. .cursor-plugin/plugin.json is valid JSON
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".github"}
FENCE_RE = re.compile(r"^```")
# [text](url) or ![alt](url), optional title after the URL
LINK_RE = re.compile(r"!?\[(?:[^\]]|\\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTTP_RE = re.compile(r"https?://[^\s)>\]]+")
PLACEHOLDER = "リンク要補完"
SKIP_KNOWHOW = {"readme.md", "_template.md"}


def iter_markdown() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def strip_fences(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def check_relative_links() -> list[str]:
    errors: list[str] = []
    for path in iter_markdown():
        text = strip_fences(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith(
                ("http://", "https://", "mailto:", "grokbot://", "#")
            ):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: escapes repo: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {raw}")
    return errors


def knowhow_entry_files() -> list[Path]:
    directory = ROOT / "docs" / "knowhow"
    files: list[Path] = []
    for path in sorted(directory.glob("*.md")):
        if path.name.lower() in SKIP_KNOWHOW:
            continue
        files.append(path)
    return files


def check_updates(path: Path) -> list[str]:
    errors: list[str] = []
    rows: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0] in {"時期", "---"} or set(cells[0]) <= {"-"}:
            continue
        rows.append(line)
        if not HTTP_RE.search(cells[2]):
            errors.append(f"{path.relative_to(ROOT)}: no http(s) source: {line}")
    if not rows:
        body = path.read_text(encoding="utf-8")
        if "まだ公式出典付きの項目が無い" not in body:
            errors.append(
                f"{path.relative_to(ROOT)}: empty log needs "
                "「まだ公式出典付きの項目が無い」"
            )
    return errors


def check_topic(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    for part in parts[1:]:
        heading = part.splitlines()[0].strip() if part.strip() else "(empty)"
        if "出典" not in part or not HTTP_RE.search(part):
            errors.append(
                f"{path.relative_to(ROOT)}: 「{heading}」 has no http(s) 出典"
            )
    return errors


def check_knowhow() -> list[str]:
    errors: list[str] = []
    directory = ROOT / "docs" / "knowhow"
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if path.name.lower() in SKIP_KNOWHOW:
            continue
        if PLACEHOLDER in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"{path.relative_to(ROOT)}: contains {PLACEHOLDER}")
    for path in knowhow_entry_files():
        if path.name == "updates.md":
            errors.extend(check_updates(path))
        else:
            errors.extend(check_topic(path))
    return errors


def check_plugin_json() -> list[str]:
    path = ROOT / ".cursor-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"{path.relative_to(ROOT)}: missing"]
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(ROOT)}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"{path.relative_to(ROOT)}: root must be an object"]
    return []


def main() -> int:
    errors: list[str] = []
    for label, fn in (
        ("relative-md-links", check_relative_links),
        ("knowhow-sources", check_knowhow),
        ("plugin-json", check_plugin_json),
    ):
        found = fn()
        if found:
            print(f"FAIL {label}")
            for item in found:
                print(f"  {item}")
            errors.extend(found)
        else:
            print(f"ok   {label}")
    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
