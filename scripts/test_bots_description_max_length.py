#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOTS = ROOT / "bots"
NON_SEATS = frozenset({"README.md", "_template.md"})
# Live census 2026-09-10. Longest 役割: CI運用.md (504 chars).
ROLE_MAX_LEN = 504
LONGEST_SEAT = "CI運用.md"

SEAT = """# bot: Sample

| 項目 | 値 |
|---|---|
| 名前 | Sample |
| id | 11111111-1111-1111-1111-111111111111 |
| グループ | 司令室 |
| 役割 | {role} |
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


@dataclass(frozen=True)
class RoleShape:
    length: int
    has_newline: bool


def raw_role_cell(text: str) -> str | None:
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
        if cells[0] == "役割":
            return cells[1]
    return None


def parse_role_shape(role: str) -> RoleShape:
    return RoleShape(
        length=len(role),
        has_newline="\n" in role or "\r" in role,
    )


def role_length_errors(
    name: str,
    role: str | None,
    *,
    max_len: int = ROLE_MAX_LEN,
) -> list[str]:
    if role is None:
        return [f"{name}: missing 役割"]
    shape = parse_role_shape(role)
    errors: list[str] = []
    if shape.has_newline:
        errors.append(f"{name}: 役割 must be one line")
    if shape.length > max_len:
        errors.append(
            f"{name}: 役割 length {shape.length} > {max_len} (max {max_len})"
        )
    return errors


def tree_errors(bots_dir: Path, *, max_len: int = ROLE_MAX_LEN) -> list[str]:
    errors: list[str] = []
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in NON_SEATS:
            continue
        role = raw_role_cell(path.read_text(encoding="utf-8"))
        errors.extend(role_length_errors(path.name, role, max_len=max_len))
    return errors


def live_census(bots_dir: Path) -> tuple[int, str]:
    longest = 0
    seat = ""
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in NON_SEATS:
            continue
        role = raw_role_cell(path.read_text(encoding="utf-8"))
        if role is None:
            continue
        length = len(role)
        if length > longest:
            longest = length
            seat = path.name
    return longest, seat


def wrap_errors() -> list[str]:
    return tree_errors(BOTS)


def _write_tree(folder: Path, files: dict[str, str]) -> None:
    for name, body in files.items():
        (folder / name).write_text(body, encoding="utf-8")


def _seat(role: str, name: str = "Sample") -> str:
    return SEAT.format(role=role).replace("Sample", name)


def _ok_role(length: int) -> str:
    body = "x" * max(0, length - len("独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"))
    return f"{body}独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"


class BotsDescriptionMaxLengthTests(unittest.TestCase):
    def test_given_live_census_when_measured_then_longest_is_ci_ops_at_pinned_max(
        self,
    ) -> None:
        longest, seat = live_census(BOTS)
        self.assertEqual(seat, LONGEST_SEAT)
        self.assertEqual(longest, ROLE_MAX_LEN)

    def test_given_role_at_pinned_max_when_validated_then_no_errors(self) -> None:
        role = _ok_role(ROLE_MAX_LEN)
        self.assertEqual(len(role), ROLE_MAX_LEN)
        found = role_length_errors("Sample.md", role)
        self.assertEqual(found, [])

    def test_given_role_one_char_over_max_when_validated_then_length_fails(
        self,
    ) -> None:
        role = _ok_role(ROLE_MAX_LEN + 1)
        found = role_length_errors("Sample.md", role)
        self.assertEqual(
            found,
            [
                f"Sample.md: 役割 length {ROLE_MAX_LEN + 1} > {ROLE_MAX_LEN} "
                f"(max {ROLE_MAX_LEN})"
            ],
        )

    def test_given_role_with_embedded_newline_when_validated_then_one_line_fails(
        self,
    ) -> None:
        role = "ONE JOB。\n独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"
        found = role_length_errors("Sample.md", role)
        self.assertEqual(found, ["Sample.md: 役割 must be one line"])

    def test_given_template_placeholder_when_scanned_then_template_is_excluded(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "_template.md": TEMPLATE_PLACEHOLDER,
                    "Sample.md": _seat(_ok_role(80)),
                },
            )
            found = tree_errors(folder)
        self.assertEqual(found, [])

    def test_given_readme_when_scanned_then_readme_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "README.md": _seat("x" * 600, "Ghost"),
                    "Sample.md": _seat(_ok_role(80)),
                },
            )
            found = tree_errors(folder)
        self.assertEqual(found, [])

    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])

    def test_given_markdown_without_a_table_when_parsed_then_role_is_none(self) -> None:
        self.assertIsNone(raw_role_cell("# bot: Sample\n\nno table\n"))

    def test_given_a_missing_role_cell_when_validated_then_role_fails(self) -> None:
        found = role_length_errors("Ghost.md", None)
        self.assertEqual(found, ["Ghost.md: missing 役割"])


if __name__ == "__main__":
    unittest.main()
