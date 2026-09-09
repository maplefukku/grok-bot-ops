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
SKILL_LINK_RE = re.compile(r"^\[((?:[^\]]|\\])*)\]\(sand-workflow:([^)\s]+)\)$")
S_ROW_RE = re.compile(r"^S\d+$")
WORKFLOW_ID_RE = re.compile(r"sand-workflow:([^)\s]+)")
README_BOT_LINK_RE = re.compile(r"\]\(\./([^)]+\.md)\)")
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
class SkillRef:
    name: str
    workflow: str  # sand-workflow id. "" for a bare name


@dataclass(frozen=True)
class LedgerSchema:
    keys: tuple[str, ...]
    groups: frozenset[str]
    hold_seats: frozenset[tuple[str, str]]
    skill_seats: frozenset[tuple[str, str]]


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


def required_skill_seats(readme_text: str) -> frozenset[tuple[str, str]]:
    seats: set[tuple[str, str]] = set()
    for line in readme_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or S_ROW_RE.match(cells[0]) is None:
            continue
        workflow_match = WORKFLOW_ID_RE.search(cells[1])
        files = README_BOT_LINK_RE.findall(cells[2])
        if workflow_match is None or not files:
            continue
        workflow = workflow_match.group(1)
        for name in files:
            seats.add((name, workflow))
    return frozenset(seats)


def ledger_schema(template_text: str, readme_text: str = "") -> LedgerSchema:
    return LedgerSchema(
        keys=FIELD_KEYS,
        groups=template_groups(template_text),
        hold_seats=HOLD_SEATS,
        skill_seats=required_skill_seats(readme_text),
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


def parse_skill_row(raw: str) -> tuple[tuple[SkillRef, ...], list[str]]:
    if raw == NONE:
        return ((), [])
    if not raw.strip():
        return ((), ["empty スキル"])
    refs: list[SkillRef] = []
    errors: list[str] = []
    for token in _tokens(raw):
        if token == NONE:
            errors.append("スキル mixes 無し")
            continue
        if token.startswith("["):
            match = SKILL_LINK_RE.match(token)
            if match is None:
                errors.append(f"skill link missing sand-workflow: {token}")
                continue
            name, workflow = match.group(1), match.group(2)
            if not name:
                errors.append(f"skill link has empty name: {token}")
                continue
            refs.append(SkillRef(name=name, workflow=workflow))
            continue
        if " " in token:
            errors.append(f"bare skill has whitespace: {token}")
            continue
        refs.append(SkillRef(name=token, workflow=""))
    return (tuple(refs), errors)


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
    refs, skill_errs = parse_skill_row(record.fields["スキル"])
    errors.extend(f"{rel}: {item}" for item in skill_errs)
    have = {ref.workflow for ref in refs if ref.workflow}
    for file, workflow in sorted(schema.skill_seats):
        if file == rel and workflow not in have:
            errors.append(
                f"{rel}: S table requires sand-workflow:{workflow} in スキル"
            )
    return errors


def tree_errors(bots_dir: Path, template_text: str) -> list[str]:
    readme_path = bots_dir / "README.md"
    has_readme = readme_path.is_file()
    readme_text = readme_path.read_text(encoding="utf-8") if has_readme else ""
    schema = ledger_schema(template_text, readme_text)
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
    if not has_readme:
        errors.append("README.md: missing")
        return errors
    linked = set(README_BOT_LINK_RE.findall(readme_text))
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

    def test_given_live_skill_shapes_when_parsed_then_refs_are_typed(self) -> None:
        self.assertEqual(
            parse_skill_row(
                "tool-path-prefer / [parallel-fire-fleet](sand-workflow:parallel-fire-fleet) / [Cloud開発](sand-workflow:cloud)"
            ),
            (
                (
                    SkillRef(name="tool-path-prefer", workflow=""),
                    SkillRef(
                        name="parallel-fire-fleet",
                        workflow="parallel-fire-fleet",
                    ),
                    SkillRef(name="Cloud開発", workflow="cloud"),
                ),
                [],
            ),
        )

    def test_given_none_when_parsed_then_empty_refs(self) -> None:
        self.assertEqual(parse_skill_row("無し"), ((), []))

    def test_given_empty_link_name_when_validated_then_skill_fails(self) -> None:
        broken = COMPLETE_LIVE.replace(
            "| スキル | 無し |",
            "| スキル | [](sand-workflow:x) |",
        )
        record = parse_bot_markdown(Path("Sample.md"), broken)
        found = record_errors(record, _schema())
        self.assertEqual(
            found,
            ["Sample.md: skill link has empty name: [](sand-workflow:x)"],
        )

    def test_given_readme_s_table_when_parsed_then_seats_are_file_id_pairs(self) -> None:
        readme = (
            "| S | スキル | ボット |\n"
            "|---|---|---|\n"
            "| S5 | [job-brief](sand-workflow:job-brief) | [`PdM`](./PdM.md) / [`CMO`](./CMO.md) |\n"
            "| S9 | [orphan](sand-workflow:orphan) | |\n"
        )
        self.assertEqual(
            required_skill_seats(readme),
            frozenset({("PdM.md", "job-brief"), ("CMO.md", "job-brief")}),
        )

    def test_given_seat_missing_required_skill_when_tree_walked_then_seat_fails(
        self,
    ) -> None:
        body = COMPLETE_LIVE.replace("# bot: Sample", "# bot: PdM").replace(
            "| 名前 | Sample |", "| 名前 | PdM |"
        )
        readme = (
            "| S5 | [job-brief](sand-workflow:job-brief) | [`PdM`](./PdM.md) |\n"
            "[`PdM`](./PdM.md)\n"
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(folder, {"PdM.md": body, "README.md": readme})
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(
            found,
            ["PdM.md: S table requires sand-workflow:job-brief in スキル"],
        )

    def test_given_seat_with_required_skill_when_tree_walked_then_no_seat_error(
        self,
    ) -> None:
        body = (
            COMPLETE_LIVE.replace("# bot: Sample", "# bot: PdM")
            .replace("| 名前 | Sample |", "| 名前 | PdM |")
            .replace(
                "| スキル | 無し |",
                "| スキル | [job-brief](sand-workflow:job-brief) |",
            )
        )
        readme = (
            "| S5 | [job-brief](sand-workflow:job-brief) | [`PdM`](./PdM.md) |\n"
            "[`PdM`](./PdM.md)\n"
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(folder, {"PdM.md": body, "README.md": readme})
            found = tree_errors(folder, TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(found, [])

    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])


if __name__ == "__main__":
    unittest.main()
