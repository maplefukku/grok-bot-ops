#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
BOTS = ROOT / "bots"
NON_SEATS = frozenset({"README.md", "_template.md"})
HITL_FILE = "アカウント設計.md"
HITL_ID = UUID("ddd63601-d4ba-4bc4-bec5-35bdf4415fc4")
HITL_GROUP = "| グループ | 最後の一針 |"

BotId = UUID

SEAT = """# bot: Sample

| 項目 | 値 |
|---|---|
| 名前 | Sample |
| id | {ident} |
| グループ | 司令室 |
| 役割 | one line |
| 回すまで動かない | いいえ |
| マージしない | はい |
| 参照 | 無し |
| スキル | 無し |
"""

TEMPLATE_PLACEHOLDER = """# bot: <名前>

| 項目 | 値 |
|---|---|
| 名前 | <日本語名> |
| id | <UUID> |
| グループ | 司令室 |
| 役割 | <1行> |
| 回すまで動かない | はい / いいえ |
| マージしない | はい |
| 参照 | 無し |
| スキル | 無し |
"""


def raw_id_cell(text: str) -> str | None:
    in_table = False
    for line in text.splitlines():
        if not in_table:
            if line.startswith("| 項目 |"):
                in_table = True
            continue
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= {"-"}:
            continue
        if cells[0] == "id":
            return cells[1]
    return None


def parse_bot_id(raw: str) -> BotId:
    return UUID(raw.strip())


def id_index(bots_dir: Path) -> tuple[dict[BotId, str], list[str]]:
    index: dict[BotId, str] = {}
    errors: list[str] = []
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in NON_SEATS:
            continue
        raw = raw_id_cell(path.read_text(encoding="utf-8"))
        if raw is None:
            errors.append(f"{path.name}: missing id")
            continue
        if not raw.strip():
            errors.append(f"{path.name}: empty id")
            continue
        try:
            bot_id = parse_bot_id(raw)
        except ValueError:
            errors.append(f"{path.name}: id is not a UUID: {raw}")
            continue
        if bot_id in index:
            errors.append(
                f"{path.name}: duplicate id {bot_id} ({index[bot_id]})"
            )
            continue
        index[bot_id] = path.name
    return index, errors


def id_uniqueness_errors(bots_dir: Path) -> list[str]:
    _index, errors = id_index(bots_dir)
    return errors


def wrap_errors() -> list[str]:
    return id_uniqueness_errors(BOTS)


def _write_tree(folder: Path, files: dict[str, str]) -> None:
    for name, body in files.items():
        (folder / name).write_text(body, encoding="utf-8")


def _seat(ident: str, name: str = "Sample") -> str:
    return SEAT.format(ident=ident).replace("Sample", name)


class BotsIdUniquenessTests(unittest.TestCase):
    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])

    def test_given_two_live_files_with_the_same_uuid_when_indexed_then_duplicate_id_fails(
        self,
    ) -> None:
        ident = "11111111-1111-1111-1111-111111111111"
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": _seat(ident),
                    "Other.md": _seat(ident, "Other"),
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(
            found,
            ["Sample.md: duplicate id 11111111-1111-1111-1111-111111111111 (Other.md)"],
        )

    def test_given_the_same_uuid_in_different_case_when_indexed_then_duplicate_id_fails(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Lower.md": _seat(
                        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "Lower"
                    ),
                    "Upper.md": _seat(
                        "{AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA}", "Upper"
                    ),
                    "Urn.md": _seat(
                        "urn:uuid:AaAaAaAa-AaAa-AaAa-AaAa-AaAaAaAaAaAa", "Urn"
                    ),
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(
            found,
            [
                "Upper.md: duplicate id aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa (Lower.md)",
                "Urn.md: duplicate id aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa (Lower.md)",
            ],
        )

    def test_given_template_placeholder_when_scanned_then_template_is_excluded(
        self,
    ) -> None:
        ident = "11111111-1111-1111-1111-111111111111"
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "_template.md": TEMPLATE_PLACEHOLDER,
                    "Sample.md": _seat(ident),
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(found, [])

    def test_given_readme_when_scanned_then_readme_is_excluded(self) -> None:
        ident = "11111111-1111-1111-1111-111111111111"
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "README.md": _seat(ident, "Ghost"),
                    "Sample.md": _seat(ident),
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(found, [])

    def test_given_a_missing_or_empty_id_when_parsed_then_id_fails(self) -> None:
        missing = _seat("11111111-1111-1111-1111-111111111111").replace(
            "| id | 11111111-1111-1111-1111-111111111111 |\n",
            "",
        )
        empty = _seat("11111111-1111-1111-1111-111111111111").replace(
            "| id | 11111111-1111-1111-1111-111111111111 |",
            "| id |  |",
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(folder, {"Missing.md": missing})
            missing_found = id_uniqueness_errors(folder)
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(folder, {"Empty.md": empty})
            empty_found = id_uniqueness_errors(folder)
        self.assertEqual(missing_found, ["Missing.md: missing id"])
        self.assertEqual(empty_found, ["Empty.md: empty id"])

    def test_given_a_non_uuid_id_when_parsed_then_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(folder, {"Sample.md": _seat("not-a-uuid")})
            found = id_uniqueness_errors(folder)
        self.assertEqual(found, ["Sample.md: id is not a UUID: not-a-uuid"])

    def test_given_a_hitl_live_seat_when_wrapped_then_it_is_counted_and_does_not_create_a_new_seat(
        self,
    ) -> None:
        hitl = BOTS / HITL_FILE
        body = hitl.read_text(encoding="utf-8")
        self.assertIn(HITL_GROUP, body)
        self.assertEqual(wrap_errors(), [])
        clone = body.replace("# bot: アカウント設計", "# bot: Clone").replace(
            "| 名前 | アカウント設計 |",
            "| 名前 | Clone |",
        )
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    HITL_FILE: body,
                    "Clone.md": clone,
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(
            found,
            [f"{HITL_FILE}: duplicate id {HITL_ID} (Clone.md)"],
        )
        self.assertFalse((BOTS / "Clone.md").exists())

    def test_given_two_different_uuids_when_indexed_then_no_uniqueness_errors(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "Sample.md": _seat(
                        "11111111-1111-1111-1111-111111111111"
                    ),
                    "Other.md": _seat(
                        "22222222-2222-2222-2222-222222222222", "Other"
                    ),
                },
            )
            found = id_uniqueness_errors(folder)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
