#!/usr/bin/env python3
from __future__ import annotations

import re
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
BOTS = ROOT / "bots"
TEMPLATE = BOTS / "_template.md"
SKIP_FILES = frozenset({"README.md"})
TEMPLATE_NAME = "_template.md"
FIELD_KEYS = (
    "名前",
    "id",
    "グループ",
    "役割",
    "回すまで動かない",
    "マージしない",
    "参照",
    "スキル",
)
YES_NO = frozenset({"はい", "いいえ"})
MERGE_LOCK = "はい"
NONE = "無し"
HEADING_RE = re.compile(r"^# bot: (.+)$")
LINK_RE = re.compile(r"\[(?:[^\]]|\\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TOKEN_SPLIT = re.compile(r"\s+/\s+")
# アカウント設計 already uses this group on main. Issue #8 stays OOS.
HOLD_GROUPS = frozenset({"最後の一針"})


@dataclass(frozen=True)
class BotRecord:
    path: Path
    heading_name: str
    fields: dict[str, str]

    @property
    def is_template(self) -> bool:
        return self.path.name == TEMPLATE_NAME


def parse_bot_markdown(path: Path, text: str) -> BotRecord:
    heading_name = ""
    fields: dict[str, str] = {}
    in_table = False
    for line in text.splitlines():
        if not heading_name:
            match = HEADING_RE.match(line.strip())
            if match:
                heading_name = match.group(1).strip()
        if line.startswith("| 項目 |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= {"-"}:
            continue
        fields[cells[0]] = cells[1]
    return BotRecord(path=path, heading_name=heading_name, fields=fields)


def template_keys(text: str) -> tuple[str, ...]:
    return tuple(parse_bot_markdown(TEMPLATE, text).fields)


def template_groups(text: str) -> frozenset[str]:
    raw = parse_bot_markdown(TEMPLATE, text).fields.get("グループ", "")
    return frozenset(
        part.strip() for part in raw.split("/") if part.strip() and "<" not in part
    )


def allowed_groups(template_text: str) -> frozenset[str]:
    return template_groups(template_text) | HOLD_GROUPS


def _is_uuid(value: str) -> bool:
    try:
        UUID(value)
    except ValueError:
        return False
    return True


def _tokens(value: str) -> list[str]:
    return [part.strip() for part in TOKEN_SPLIT.split(value) if part.strip()]


def record_errors(record: BotRecord, groups: frozenset[str]) -> list[str]:
    errors: list[str] = []
    rel = record.path.name
    keys = tuple(record.fields)
    if keys != FIELD_KEYS:
        errors.append(f"{rel}: keys {keys} != {FIELD_KEYS}")
        return errors
    if not record.heading_name:
        errors.append(f"{rel}: missing # bot: heading")
    if record.is_template:
        return errors
    name = record.fields["名前"]
    if not name or "<" in name:
        errors.append(f"{rel}: empty 名前")
    if record.heading_name != name:
        errors.append(f"{rel}: heading {record.heading_name!r} != 名前 {name!r}")
    ident = record.fields["id"]
    if not _is_uuid(ident):
        errors.append(f"{rel}: id is not a UUID: {ident}")
    group = record.fields["グループ"]
    if group not in groups:
        errors.append(f"{rel}: unknown グループ {group}")
    if not record.fields["役割"].strip():
        errors.append(f"{rel}: empty 役割")
    wait = record.fields["回すまで動かない"]
    if wait not in YES_NO:
        errors.append(f"{rel}: 回すまで動かない must be はい or いいえ")
    merge = record.fields["マージしない"]
    if merge != MERGE_LOCK:
        errors.append(f"{rel}: マージしない must be はい")
    ref = record.fields["参照"]
    if ref != NONE:
        if not ref.strip():
            errors.append(f"{rel}: empty 参照")
        elif not LINK_RE.search(ref):
            errors.append(f"{rel}: 参照 must be 無し or a markdown link")
    skill = record.fields["スキル"]
    if skill != NONE:
        if not skill.strip():
            errors.append(f"{rel}: empty スキル")
        for token in _tokens(skill):
            if token == NONE:
                errors.append(f"{rel}: スキル mixes 無し")
            elif token.startswith("[") and "sand-workflow:" not in token:
                errors.append(f"{rel}: skill link missing sand-workflow: {token}")
            elif not token.startswith("[") and " " in token:
                errors.append(f"{rel}: bare skill has whitespace: {token}")
    return errors


def tree_errors(bots_dir: Path, template_text: str) -> list[str]:
    groups = allowed_groups(template_text)
    errors: list[str] = []
    ids: dict[str, str] = {}
    names: dict[str, str] = {}
    live: list[str] = []
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        record = parse_bot_markdown(path, path.read_text(encoding="utf-8"))
        errors.extend(record_errors(record, groups))
        if record.is_template:
            continue
        live.append(path.name)
        ident = record.fields.get("id", "")
        name = record.fields.get("名前", "")
        if ident and ident in ids:
            errors.append(f"{path.name}: duplicate id {ident} ({ids[ident]})")
        elif ident:
            ids[ident] = path.name
        if name and name in names:
            errors.append(f"{path.name}: duplicate 名前 {name} ({names[name]})")
        elif name:
            names[name] = path.name
    readme_path = bots_dir / "README.md"
    if not readme_path.is_file():
        errors.append("README.md: missing")
        return errors
    linked = set(re.findall(r"\]\(\./([^)]+\.md)\)", readme_path.read_text(encoding="utf-8")))
    linked.discard(TEMPLATE_NAME)
    live_set = set(live)
    for name in sorted(live_set - linked):
        errors.append(f"README.md: missing link to {name}")
    for name in sorted(linked - live_set):
        errors.append(f"README.md: links to missing {name}")
    return errors


def wrap_errors() -> list[str]:
    if not TEMPLATE.is_file():
        return ["bots/_template.md: missing"]
    text = TEMPLATE.read_text(encoding="utf-8")
    errors: list[str] = []
    keys = template_keys(text)
    if keys != FIELD_KEYS:
        errors.append(f"bots/_template.md: keys {keys} != {FIELD_KEYS}")
    errors.extend(tree_errors(BOTS, text))
    return errors


COMPLETE_LIVE = """# bot: Sample

| 項目 | 値 |
|---|---|
| 名前 | Sample |
| id | 11111111-1111-1111-1111-111111111111 |
| グループ | 司令室 |
| 役割 | one line |
| 回すまで動かない | いいえ |
| マージしない | はい |
| 参照 | 無し |
| スキル | 無し |
"""

COMPLETE_HOLD = """# bot: HoldSeat

| 項目 | 値 |
|---|---|
| 名前 | HoldSeat |
| id | 22222222-2222-2222-2222-222222222222 |
| グループ | 最後の一針 |
| 役割 | existing HITL seat |
| 回すまで動かない | はい |
| マージしない | はい |
| 参照 | [routines/x.md](../routines/x.md) |
| スキル | tool-path-prefer / [job-brief](sand-workflow:job-brief) |
"""


def _groups() -> frozenset[str]:
    return allowed_groups(TEMPLATE.read_text(encoding="utf-8"))


class BotsSchemaTests(unittest.TestCase):
    def test_given_template_when_parsed_then_keys_are_the_eight_ledger_fields(self) -> None:
        keys = template_keys(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(
            keys,
            (
                "名前",
                "id",
                "グループ",
                "役割",
                "回すまで動かない",
                "マージしない",
                "参照",
                "スキル",
            ),
        )

    def test_given_complete_row_when_validated_then_no_errors(self) -> None:
        record = parse_bot_markdown(Path("Sample.md"), COMPLETE_LIVE)
        self.assertEqual(record_errors(record, _groups()), [])

    def test_given_hold_group_when_validated_then_no_errors(self) -> None:
        record = parse_bot_markdown(Path("HoldSeat.md"), COMPLETE_HOLD)
        self.assertEqual(record_errors(record, _groups()), [])

    def test_given_missing_skill_row_when_validated_then_keys_fail(self) -> None:
        broken = COMPLETE_LIVE.replace("| スキル | 無し |\n", "")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, frozenset({"司令室"}))
        self.assertTrue(any("keys" in item for item in found), found)

    def test_given_bad_uuid_when_validated_then_id_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "11111111-1111-1111-1111-111111111111", "not-a-uuid"
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, frozenset({"司令室"}))
        self.assertTrue(any("UUID" in item for item in found), found)

    def test_given_merge_no_when_validated_then_merge_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| マージしない | はい |", "| マージしない | いいえ |"
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, frozenset({"司令室"}))
        self.assertTrue(any("マージしない" in item for item in found), found)

    def test_given_invented_group_when_validated_then_group_fails(self) -> None:
        broken = COMPLETE_LIVE.replace("司令室", "新席")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _groups())
        self.assertTrue(any("グループ" in item for item in found), found)

    def test_given_heading_mismatch_when_validated_then_heading_fails(self) -> None:
        broken = COMPLETE_LIVE.replace("# bot: Sample", "# bot: Other")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, frozenset({"司令室"}))
        self.assertTrue(any("heading" in item for item in found), found)

    def test_given_duplicate_id_when_tree_walked_then_duplicate_fails(self) -> None:
        other = COMPLETE_LIVE.replace("Sample", "Other").replace(
            "11111111-1111-1111-1111-111111111111",
            "11111111-1111-1111-1111-111111111111",
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            (folder / "Sample.md").write_text(COMPLETE_LIVE, encoding="utf-8")
            (folder / "Other.md").write_text(other, encoding="utf-8")
            (folder / "README.md").write_text(
                "[`Sample`](./Sample.md) [`Other`](./Other.md)\n",
                encoding="utf-8",
            )
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("duplicate id" in item for item in found), found)

    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])


if __name__ == "__main__":
    unittest.main()
