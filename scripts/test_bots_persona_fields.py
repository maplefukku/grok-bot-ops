#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOTS = ROOT / "bots"
NON_SEATS = frozenset({"README.md", "_template.md"})
PARALLEL_CLAUSE = "独立ジョブは並列"
VIRTUES_CLAUSE = "3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"

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

PARALLEL_VARIANTS = (
    "独立ジョブは並列。",
    "独立ジョブは並列（直列待ちしない）。",
    "独立ジョブは並列で火を付ける。",
)


@dataclass(frozen=True)
class Persona:
    parallel_at: int | None
    virtues_at: int | None
    role_len: int

    def virtues_terminal(self) -> bool:
        if self.virtues_at is None:
            return False
        return self.virtues_at + len(VIRTUES_CLAUSE) == self.role_len


def _index(text: str, needle: str) -> int | None:
    found = text.find(needle)
    if found < 0:
        return None
    return found


def parse_persona(role: str) -> Persona:
    return Persona(
        parallel_at=_index(role, PARALLEL_CLAUSE),
        virtues_at=_index(role, VIRTUES_CLAUSE),
        role_len=len(role),
    )


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


def persona_errors(name: str, role: str | None) -> list[str]:
    if role is None:
        return [f"{name}: missing 役割"]
    persona = parse_persona(role)
    errors: list[str] = []
    if persona.parallel_at is None:
        errors.append(f"{name}: 役割 missing {PARALLEL_CLAUSE}")
    if not persona.virtues_terminal():
        errors.append(f"{name}: 役割 must end with {VIRTUES_CLAUSE}")
    if (
        persona.parallel_at is not None
        and persona.virtues_at is not None
        and persona.parallel_at > persona.virtues_at
    ):
        errors.append(f"{name}: {PARALLEL_CLAUSE} must precede 3美徳")
    return errors


def tree_errors(bots_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(bots_dir.glob("*.md")):
        if path.name in NON_SEATS:
            continue
        role = raw_role_cell(path.read_text(encoding="utf-8"))
        errors.extend(persona_errors(path.name, role))
    return errors


def wrap_errors() -> list[str]:
    return tree_errors(BOTS)


def _write_tree(folder: Path, files: dict[str, str]) -> None:
    for name, body in files.items():
        (folder / name).write_text(body, encoding="utf-8")


def _seat(role: str, name: str = "Sample") -> str:
    return SEAT.format(role=role).replace("Sample", name)


def _ok_role(parallel: str) -> str:
    return f"ONE JOB。{parallel}{VIRTUES_CLAUSE}"


class BotsPersonaFieldsTests(unittest.TestCase):
    def test_given_complete_seat_when_validated_then_no_errors(self) -> None:
        found = persona_errors("Sample.md", _ok_role("独立ジョブは並列。"))
        self.assertEqual(found, [])

    def test_given_the_three_observed_parallel_variants_when_validated_then_no_errors(
        self,
    ) -> None:
        for parallel in PARALLEL_VARIANTS:
            found = persona_errors("Sample.md", _ok_role(parallel))
            self.assertEqual(found, [], parallel)

    def test_given_missing_parallel_clause_when_validated_then_parallel_fails(
        self,
    ) -> None:
        role = f"ONE JOB。{VIRTUES_CLAUSE}"
        found = persona_errors("Sample.md", role)
        self.assertEqual(found, ["Sample.md: 役割 missing 独立ジョブは並列"])

    def test_given_missing_virtues_clause_when_validated_then_virtues_fails(
        self,
    ) -> None:
        found = persona_errors("Sample.md", "ONE JOB。独立ジョブは並列。")
        self.assertEqual(
            found,
            [
                "Sample.md: 役割 must end with "
                "3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"
            ],
        )

    def test_given_trailing_text_after_virtues_when_validated_then_virtues_fails(
        self,
    ) -> None:
        role = f"{_ok_role('独立ジョブは並列。')} extra"
        found = persona_errors("Sample.md", role)
        self.assertEqual(
            found,
            [
                "Sample.md: 役割 must end with "
                "3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）"
            ],
        )

    def test_given_reversed_clause_order_when_validated_then_order_fails(self) -> None:
        role = f"{VIRTUES_CLAUSE}。独立ジョブは並列。"
        found = persona_errors("Sample.md", role)
        self.assertEqual(
            found,
            [
                "Sample.md: 役割 must end with "
                "3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー）",
                "Sample.md: 独立ジョブは並列 must precede 3美徳",
            ],
        )

    def test_given_template_placeholder_when_scanned_then_template_is_excluded(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            _write_tree(
                folder,
                {
                    "_template.md": TEMPLATE_PLACEHOLDER,
                    "Sample.md": _seat(_ok_role("独立ジョブは並列。")),
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
                    "README.md": _seat("no persona clauses", "Ghost"),
                    "Sample.md": _seat(_ok_role("独立ジョブは並列。")),
                },
            )
            found = tree_errors(folder)
        self.assertEqual(found, [])

    def test_given_live_ledger_when_wrapped_then_no_errors(self) -> None:
        self.assertEqual(wrap_errors(), [])

    def test_given_markdown_without_a_table_when_parsed_then_role_is_none(self) -> None:
        self.assertIsNone(raw_role_cell("# bot: Sample\n\nno table\n"))

    def test_given_a_missing_role_cell_when_validated_then_role_fails(self) -> None:
        found = persona_errors("Ghost.md", None)
        self.assertEqual(found, ["Ghost.md: missing 役割"])


if __name__ == "__main__":
    unittest.main()
