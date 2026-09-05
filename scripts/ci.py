#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import re
import sys
import unittest
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


def trend_log_errors(text: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    in_section = False
    in_decisions = False
    found_section = False
    found_header = False
    idx_decision = idx_url = idx_reason = -1
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip() == "判断記録"
            in_decisions = False
            if in_section:
                found_section = True
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and all(c and set(c) <= {"-", ":"} for c in cells):
            continue
        labels = set(cells)
        if {"decision", "source_url", "理由"} <= labels:
            idx_decision = cells.index("decision")
            idx_url = cells.index("source_url")
            idx_reason = cells.index("理由")
            in_decisions = True
            found_header = True
            continue
        if not in_decisions:
            continue
        decision = cells[idx_decision] if idx_decision < len(cells) else ""
        url = cells[idx_url] if idx_url < len(cells) else ""
        reason = cells[idx_reason] if idx_reason < len(cells) else ""
        if decision not in {"ADOPT", "REJECT"}:
            errors.append(f"decision must be ADOPT or REJECT: {line}")
        if not reason:
            errors.append(f"empty 理由: {line}")
        if not HTTP_RE.search(url):
            errors.append(f"source_url must match https?://: {line}")
        key = url.strip().rstrip("/")
        if key:
            if key in seen:
                errors.append(f"duplicate source_url: {line}")
            else:
                seen.add(key)
    if not found_section:
        errors.append("missing ## 判断記録")
    elif not found_header:
        errors.append("## 判断記録 has no decision table")
    return errors


def _trend_log_parser_self_check() -> list[str]:
    errors: list[str] = []
    header = (
        "## 判断記録\n"
        "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )
    valid = header + (
        "| 2026-09-05 | 最先端手法 | ok | https://example.com/ok | ADOPT | because | ops |  |\n"
    )
    if trend_log_errors(valid):
        errors.append("trend-log parser self-check: valid row produced errors")
    outside = (
        "| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        "| 2026-09-05 | 最先端手法 | x | https://example.com/out | WATCH |  | none |  |\n"
    )
    outside_err = "\n".join(trend_log_errors(outside))
    if "WATCH" in outside_err or "empty 理由" in outside_err:
        errors.append(
            "trend-log parser self-check: table outside 判断記録 was parsed"
        )
    if "判断記録" not in outside_err:
        errors.append(
            "trend-log parser self-check: missing ## 判断記録 was accepted"
        )
    empty_section = "## 判断記録\n\nno table\n"
    empty_err = "\n".join(trend_log_errors(empty_section))
    if "decision table" not in empty_err:
        errors.append(
            "trend-log parser self-check: empty 判断記録 was accepted"
        )
    cases = (
        (
            "missing 理由",
            header
            + "| 2026-09-05 | Knowhow収集 | t | https://example.com/a | REJECT |  | none |  |\n",
            "理由",
        ),
        (
            "illegal decision",
            header
            + "| 2026-09-05 | Knowhow収集 | t | https://example.com/b | WATCH | has reason | none |  |\n",
            "decision",
        ),
        (
            "non-http url",
            header
            + "| 2026-09-05 | Knowhow収集 | t | not-a-url | REJECT | has reason | none |  |\n",
            "http",
        ),
        (
            "duplicate source_url",
            header
            + "| 2026-09-05 | 最先端手法 | t1 | https://example.com/dup | ADOPT | one | ops |  |\n"
            + "| 2026-09-05 | Knowhow収集 | t2 | https://example.com/dup/ | REJECT | two | none |  |\n",
            "source_url",
        ),
    )
    for name, snippet, needle in cases:
        found = trend_log_errors(snippet)
        if not found:
            errors.append(f"trend-log parser self-check missed {name}")
            continue
        blob = "\n".join(found)
        if needle not in blob:
            errors.append(
                f"trend-log parser self-check: {name} errors omitted {needle}"
            )
    return errors


def check_trend_log() -> list[str]:
    errors: list[str] = []
    errors.extend(_trend_log_parser_self_check())
    path = ROOT / "docs" / "decisions" / "trend-log.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append("docs/decisions/trend-log.md: missing")
        return errors
    prefix = str(path.relative_to(ROOT))
    for item in trend_log_errors(text):
        errors.append(f"{prefix}: {item}")
    return errors


def _run_unittest_module(module: str, label: str) -> list[str]:
    scripts = str(ROOT / "scripts")
    inserted = scripts not in sys.path
    if inserted:
        sys.path.insert(0, scripts)
    buf = io.StringIO()
    try:
        suite = unittest.defaultTestLoader.loadTestsFromName(module)
        result = unittest.TextTestRunner(stream=buf, verbosity=1).run(suite)
    except Exception as exc:
        return [f"{label} tests could not run: {exc}"]
    finally:
        if inserted and sys.path and sys.path[0] == scripts:
            sys.path.pop(0)
    if result.testsRun < 1:
        return [f"{label} tests ran 0 tests"]
    if result.wasSuccessful():
        return []
    return [f"{label} tests failed\n{buf.getvalue().rstrip()}"]


def check_intent_memory_contract() -> list[str]:
    return _run_unittest_module("intent_memory.test_contract", "intent-memory")


def check_local_worktree_prune() -> list[str]:
    return _run_unittest_module("test_local_worktree_prune", "local-worktree-prune")


def main() -> int:
    errors: list[str] = []
    for label, fn in (
        ("relative-md-links", check_relative_links),
        ("knowhow-sources", check_knowhow),
        ("plugin-json", check_plugin_json),
        ("intent-memory-contract", check_intent_memory_contract),
        ("local-worktree-prune", check_local_worktree_prune),
        ("trend-log-decisions", check_trend_log),
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
