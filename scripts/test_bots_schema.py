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
LINK_RE = re.compile(r"^\[(?:[^\]]|\\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)$")
SKILL_LINK_RE = re.compile(r"^\[(?:[^\]]|\\])*\]\(sand-workflow:[^)\s]+\)$")
TOKEN_SPLIT = re.compile(r"\s+/\s+")
# Pin the one live HITL row. A fifth group for every file would invent seats.
HOLD_SEATS = frozenset({("アカウント設計.md", "最後の一針")})


@dataclass(frozen=True)
class BotRecord:
    path: Path
    heading_name: str
    fields: dict[str, str]

    @property
    def is_template(self) -> bool:
        return self.path.name == TEMPLATE_NAME


@dataclass(frozen=True)
class LedgerSchema:
    keys: tuple[str, ...]
    groups: frozenset[str]
    hold_seats: frozenset[tuple[str, str]]


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


def ledger_schema(template_text: str) -> LedgerSchema:
    return LedgerSchema(
        keys=FIELD_KEYS,
        groups=template_groups(template_text),
        hold_seats=HOLD_SEATS,
    )


def group_allowed(record: BotRecord, schema: LedgerSchema) -> bool:
    group = record.fields["グループ"]
    if group in schema.groups:
        return True
    return (record.path.name, group) in schema.hold_seats


def _is_uuid(value: str) -> bool:
    try:
        UUID(value)
    except ValueError:
        return False
    return True


def _tokens(value: str) -> list[str]:
    return [part.strip() for part in TOKEN_SPLIT.split(value) if part.strip()]


def _ref_errors(rel: str, ref: str) -> list[str]:
    if ref == NONE:
        return []
    if not ref.strip():
        return [f"{rel}: empty 参照"]
    errors: list[str] = []
    for token in _tokens(ref):
        match = LINK_RE.match(token)
        if match is None:
            errors.append(f"{rel}: 参照 must be 無し or a markdown link")
            continue
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "sand-workflow:")):
            errors.append(f"{rel}: 参照 must be in-repo: {token}")
    return errors


def _skill_errors(rel: str, skill: str) -> list[str]:
    if skill == NONE:
        return []
    if not skill.strip():
        return [f"{rel}: empty スキル"]
    errors: list[str] = []
    for token in _tokens(skill):
        if token == NONE:
            errors.append(f"{rel}: スキル mixes 無し")
        elif token.startswith("["):
            if SKILL_LINK_RE.match(token) is None:
                errors.append(f"{rel}: skill link missing sand-workflow: {token}")
        elif " " in token:
            errors.append(f"{rel}: bare skill has whitespace: {token}")
    return errors


def record_errors(record: BotRecord, schema: LedgerSchema) -> list[str]:
    errors: list[str] = []
    rel = record.path.name
    keys = tuple(record.fields)
    if keys != schema.keys:
        errors.append(f"{rel}: keys {keys} != {schema.keys}")
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
    if not group_allowed(record, schema):
        errors.append(f"{rel}: unknown グループ {record.fields['グループ']}")
    if not record.fields["役割"].strip():
        errors.append(f"{rel}: empty 役割")
    wait = record.fields["回すまで動かない"]
    if wait not in YES_NO:
        errors.append(f"{rel}: 回すまで動かない must be はい or いいえ")
    merge = record.fields["マージしない"]
    if merge != MERGE_LOCK:
        errors.append(f"{rel}: マージしない must be はい")
    errors.extend(_ref_errors(rel, record.fields["参照"]))
    errors.extend(_skill_errors(rel, record.fields["スキル"]))
    return errors


def tree_errors(bots_dir: Path, template_text: str) -> list[str]:
    schema = ledger_schema(template_text)
    errors: list[str] = []
    ids: dict[str, str] = {}
    names: dict[str, str] = {}
    live: list[str] = []
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        record = parse_bot_markdown(path, path.read_text(encoding="utf-8"))
        errors.extend(record_errors(record, schema))
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

COMPLETE_HOLD = """# bot: アカウント設計

| 項目 | 値 |
|---|---|
| 名前 | アカウント設計 |
| id | 22222222-2222-2222-2222-222222222222 |
| グループ | 最後の一針 |
| 役割 | existing HITL seat |
| 回すまで動かない | はい |
| マージしない | はい |
| 参照 | [routines/x.md](../routines/x.md) |
| スキル | tool-path-prefer / [job-brief](sand-workflow:job-brief) |
"""


def _schema() -> LedgerSchema:
    return ledger_schema(TEMPLATE.read_text(encoding="utf-8"))


def _write_tree(folder: Path, files: dict[str, str]) -> None:
    for name, body in files.items():
        (folder / name).write_text(body, encoding="utf-8")


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
        self.assertEqual(record_errors(record, _schema()), [])

    def test_given_pinned_hold_seat_when_validated_then_no_errors(self) -> None:
        record = parse_bot_markdown(Path("アカウント設計.md"), COMPLETE_HOLD)
        self.assertEqual(record_errors(record, _schema()), [])

    def test_given_new_file_on_hold_group_when_validated_then_group_fails(self) -> None:
        body = (
            COMPLETE_HOLD.replace("# bot: アカウント設計", "# bot: 新HITL席")
            .replace("| 名前 | アカウント設計 |", "| 名前 | 新HITL席 |")
            .replace(
                "22222222-2222-2222-2222-222222222222",
                "33333333-3333-3333-3333-333333333333",
            )
        )
        record = parse_bot_markdown(Path("新HITL席.md"), body)
        found = record_errors(record, _schema())
        self.assertTrue(any("グループ" in item for item in found), found)

    def test_given_missing_skill_row_when_validated_then_keys_fail(self) -> None:
        broken = COMPLETE_LIVE.replace("| スキル | 無し |\n", "")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("keys" in item for item in found), found)

    def test_given_bad_uuid_when_validated_then_id_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "11111111-1111-1111-1111-111111111111", "not-a-uuid"
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("UUID" in item for item in found), found)

    def test_given_merge_no_when_validated_then_merge_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| マージしない | はい |", "| マージしない | いいえ |"
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("マージしない" in item for item in found), found)

    def test_given_invented_group_when_validated_then_group_fails(self) -> None:
        broken = COMPLETE_LIVE.replace("司令室", "新席")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("グループ" in item for item in found), found)

    def test_given_heading_mismatch_when_validated_then_heading_fails(self) -> None:
        broken = COMPLETE_LIVE.replace("# bot: Sample", "# bot: Other")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("heading" in item for item in found), found)

    def test_given_empty_role_when_validated_then_role_fails(self) -> None:
        broken = COMPLETE_LIVE.replace("| 役割 | one line |", "| 役割 |  |")
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("役割" in item for item in found), found)

    def test_given_bad_wait_flag_when_validated_then_wait_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| 回すまで動かない | いいえ |", "| 回すまで動かない | たぶん |"
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("回すまで動かない" in item for item in found), found)

    def test_given_external_ref_when_validated_then_ref_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| 参照 | 無し |",
            "| 参照 | [x](https://example.com/x.md) |",
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("in-repo" in item for item in found), found)

    def test_given_junk_beside_ref_link_when_validated_then_ref_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| 参照 | 無し |",
            "| 参照 | junk / [routines/x.md](../routines/x.md) |",
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("参照" in item for item in found), found)

    def test_given_garbage_after_skill_link_when_validated_then_skill_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| スキル | 無し |",
            "| スキル | [x](sand-workflow:x) garbage here |",
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertTrue(any("sand-workflow" in item for item in found), found)

    def test_given_duplicate_id_when_tree_walked_then_duplicate_fails(self) -> None:
        other = COMPLETE_LIVE.replace("# bot: Sample", "# bot: Other").replace(
            "| 名前 | Sample |", "| 名前 | Other |"
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": COMPLETE_LIVE,
                    "Other.md": other,
                    "README.md": "[`Sample`](./Sample.md) [`Other`](./Other.md)\n",
                },
            )
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("duplicate id" in item for item in found), found)

    def test_given_duplicate_name_when_tree_walked_then_duplicate_fails(self) -> None:
        other = COMPLETE_LIVE.replace(
            "11111111-1111-1111-1111-111111111111",
            "44444444-4444-4444-4444-444444444444",
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": COMPLETE_LIVE,
                    "Copy.md": other,
                    "README.md": "[`Sample`](./Sample.md) [`Copy`](./Copy.md)\n",
                },
            )
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("duplicate 名前" in item for item in found), found)

    def test_given_readme_without_live_file_when_tree_walked_then_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": COMPLETE_LIVE,
                    "README.md": "[`Sample`](./Sample.md) [`Ghost`](./Ghost.md)\n",
                },
            )
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("links to missing Ghost.md" in item for item in found), found)

    def test_given_live_file_absent_from_readme_when_tree_walked_then_link_fails(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": COMPLETE_LIVE,
                    "README.md": "no bot links\n",
                },
            )
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("missing link to Sample.md" in item for item in found), found)

    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])


if __name__ == "__main__":
    unittest.main()
