#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from completion_handoff import (  # noqa: E402
    Branch,
    ContractError,
    Counts,
    Delivered,
    Handoff,
    HoldRef,
    Label,
    NoChange,
    Stacked,
    Suppressed,
    fan_out,
    lock_errors,
    parse,
    render,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER_BOT = ROOT / "bots" / "台帳更新.md"
BOTS_README = ROOT / "bots" / "README.md"
REVIEW_BOT = ROOT / "bots" / "編成評価.md"

LEDGER_NEEDLES: tuple[str, ...] = (
    "EVAL-READY",
    "kind / date_jst / branch / pr / counts / hold",
    "同一 date_jst は再送しない",
    "PMと編成評価へ同じ本文",
    "sand-workflow:completion-handoff",
    "構成の評価はしない",
)
README_NEEDLES: tuple[str, ...] = (
    "| S4 | [completion-handoff](sand-workflow:completion-handoff) | [`台帳更新`](./台帳更新.md) |",
    "ops/daily-YYYY-MM-DD",
)
REVIEW_NEEDLES: tuple[str, ...] = ("INは台帳更新のEVAL-READY",)

STACKED_BODY = (
    "kind: EVAL-READY\n"
    "date_jst: 2026-09-09\n"
    "branch: ops/daily-2026-09-09\n"
    "pr: https://github.com/maplefukku/grok-bot-ops/pull/88\n"
    "counts: ADD 5, ROLE-CHANGE 1\n"
    "hold: #5 #7 #10"
)
NO_CHANGE_BODY = (
    "kind: EVAL-READY\n"
    "date_jst: 2026-09-09\n"
    "branch: ops/daily-2026-09-09\n"
    "pr: 変更なし\n"
    "counts: 無し\n"
    "hold: 無し"
)


def _stacked() -> Handoff:
    return Handoff(
        date_jst=date(2026, 9, 9),
        outcome=Stacked(88),
        counts=Counts(
            items=((Label("ADD"), 5), (Label("ROLE-CHANGE"), 1)),
        ),
        hold=(HoldRef("#5"), HoldRef("#7"), HoldRef("#10")),
    )


def _no_change() -> Handoff:
    return Handoff(
        date_jst=date(2026, 9, 9),
        outcome=NoChange(),
        counts=Counts(items=()),
        hold=(),
    )


class RenderTests(unittest.TestCase):
    def test_given_a_stacked_handoff_when_rendered_then_body_equals_six_line_literal(
        self,
    ) -> None:
        self.assertEqual(render(_stacked()), STACKED_BODY)

    def test_given_a_no_change_handoff_when_rendered_then_body_equals_none_marks(
        self,
    ) -> None:
        self.assertEqual(render(_no_change()), NO_CHANGE_BODY)


class RoundTripTests(unittest.TestCase):
    def test_given_render_of_both_fixtures_when_parsed_then_equals_handoff(self) -> None:
        stacked = _stacked()
        no_change = _no_change()
        self.assertEqual(parse(render(stacked)), stacked)
        self.assertEqual(parse(render(no_change)), no_change)


class ContractTests(unittest.TestCase):
    def test_given_branch_for_other_day_when_constructed_then_contract_error(
        self,
    ) -> None:
        with self.assertRaises(ContractError) as ctx:
            Handoff(
                date_jst=date(2026, 9, 9),
                outcome=NoChange(),
                counts=Counts(items=()),
                hold=(),
                branch=Branch("ops/daily-2026-09-08"),
            )
        self.assertEqual(
            str(ctx.exception),
            "branch does not match date_jst: ops/daily-2026-09-08",
        )

    def test_given_no_change_with_add_1_when_constructed_then_contract_error(
        self,
    ) -> None:
        with self.assertRaises(ContractError) as ctx:
            Handoff(
                date_jst=date(2026, 9, 9),
                outcome=NoChange(),
                counts=Counts(items=((Label("ADD"), 1),)),
                hold=(),
            )
        self.assertEqual(str(ctx.exception), "変更なし with non-zero counts")

    def test_given_pr_0_when_stacked_then_contract_error(self) -> None:
        with self.assertRaises(ContractError) as ctx:
            Stacked(0)
        self.assertEqual(str(ctx.exception), "pr is not positive")

    def test_given_duplicate_hold_refs_when_constructed_then_contract_error(self) -> None:
        with self.assertRaises(ContractError) as ctx:
            Handoff(
                date_jst=date(2026, 9, 9),
                outcome=NoChange(),
                counts=Counts(items=()),
                hold=(HoldRef("#5"), HoldRef("#5")),
            )
        self.assertEqual(str(ctx.exception), "duplicate hold ref: #5")

    def test_given_duplicate_count_label_when_constructed_then_contract_error(
        self,
    ) -> None:
        with self.assertRaises(ContractError) as ctx:
            Counts(items=((Label("ADD"), 1), (Label("ADD"), 2)))
        self.assertEqual(str(ctx.exception), "duplicate count label: ADD")


class ParseTests(unittest.TestCase):
    def test_given_parse_text_missing_hold_line_when_parsed_then_missing_field_hold(
        self,
    ) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: https://github.com/maplefukku/grok-bot-ops/pull/88\n"
            "counts: ADD 5, ROLE-CHANGE 1"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "missing field: hold")

    def test_given_branch_line_missing_and_rest_in_order_when_parsed_then_missing_field_branch(
        self,
    ) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "pr: https://github.com/maplefukku/grok-bot-ops/pull/88\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "missing field: branch")

    def test_given_pr_line_twice_when_parsed_then_duplicate_field_pr(self) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: 88\n"
            "pr: 89\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "duplicate field: pr")

    def test_given_compact_separator_and_blank_lines_when_parsed_then_equals_handoff(
        self,
    ) -> None:
        text = (
            "\n"
            "kind:EVAL-READY\n"
            "  date_jst:  2026-09-09\n"
            "branch:ops/daily-2026-09-09\n"
            "pr:https://github.com/maplefukku/grok-bot-ops/pull/88\n"
            "counts:ADD 5, ROLE-CHANGE 1\n"
            "hold:#5 #7 #10\n"
            "\n"
        )
        self.assertEqual(parse(text), _stacked())

    def test_given_extra_note_line_when_parsed_then_unknown_field_note(self) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: https://github.com/maplefukku/grok-bot-ops/pull/88\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10\n"
            "note: x"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "unknown field: note")

    def test_given_pr_and_branch_lines_swapped_when_parsed_then_field_out_of_order_pr(
        self,
    ) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "pr: https://github.com/maplefukku/grok-bot-ops/pull/88\n"
            "branch: ops/daily-2026-09-09\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "field out of order: pr")

    def test_given_kind_done_when_parsed_then_kind_is_not_eval_ready(self) -> None:
        text = (
            "kind: DONE\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: 変更なし\n"
            "counts: 無し\n"
            "hold: 無し"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(str(ctx.exception), "kind is not EVAL-READY: DONE")

    def test_given_other_repo_pr_url_when_parsed_then_not_a_ledger_pr(self) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: https://github.com/other/repo/pull/1\n"
            "counts: 無し\n"
            "hold: 無し"
        )
        with self.assertRaises(ContractError) as ctx:
            parse(text)
        self.assertEqual(
            str(ctx.exception),
            "pr is not a ledger PR: https://github.com/other/repo/pull/1",
        )

    def test_given_hash_pr_when_parsed_then_stacked(self) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: #88\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10"
        )
        self.assertEqual(parse(text).outcome, Stacked(pr=88))

    def test_given_bare_integer_pr_when_parsed_then_stacked(self) -> None:
        text = (
            "kind: EVAL-READY\n"
            "date_jst: 2026-09-09\n"
            "branch: ops/daily-2026-09-09\n"
            "pr: 88\n"
            "counts: ADD 5, ROLE-CHANGE 1\n"
            "hold: #5 #7 #10"
        )
        self.assertEqual(parse(text).outcome, Stacked(pr=88))


class FanOutTests(unittest.TestCase):
    def test_given_empty_sent_when_fan_out_then_delivered_identical_body(self) -> None:
        self.assertEqual(
            fan_out(_stacked(), frozenset()),
            Delivered(to=("PM", "編成評価"), body=STACKED_BODY),
        )

    def test_given_sent_containing_the_date_when_fan_out_then_suppressed(self) -> None:
        self.assertEqual(
            fan_out(_stacked(), frozenset({date(2026, 9, 9)})),
            Suppressed(date(2026, 9, 9)),
        )

    def test_given_fan_out_twice_with_first_date_added_to_sent_then_second_is_suppressed(
        self,
    ) -> None:
        handoff = _stacked()
        first = fan_out(handoff, frozenset())
        self.assertEqual(
            first,
            Delivered(to=("PM", "編成評価"), body=STACKED_BODY),
        )
        second = fan_out(handoff, frozenset({date(2026, 9, 9)}))
        self.assertEqual(second, Suppressed(date(2026, 9, 9)))


class LockWrapTests(unittest.TestCase):
    def test_given_ledger_bot_file_when_locked_then_no_errors(self) -> None:
        self.assertEqual(
            lock_errors(LEDGER_BOT.read_text(encoding="utf-8"), LEDGER_NEEDLES),
            [],
        )

    def test_given_bots_readme_when_locked_then_no_errors(self) -> None:
        self.assertEqual(
            lock_errors(BOTS_README.read_text(encoding="utf-8"), README_NEEDLES),
            [],
        )

    def test_given_review_bot_file_when_locked_then_no_errors(self) -> None:
        self.assertEqual(
            lock_errors(REVIEW_BOT.read_text(encoding="utf-8"), REVIEW_NEEDLES),
            [],
        )

    def test_given_skills_dir_when_checked_then_completion_handoff_box_does_not_exist(
        self,
    ) -> None:
        self.assertFalse((ROOT / "skills" / "completion-handoff").exists())

    def test_given_fixture_missing_one_needle_when_lock_errors_then_missing_that_needle(
        self,
    ) -> None:
        fixture = (
            "kind / date_jst / branch / pr / counts / hold\n"
            "同一 date_jst は再送しない\n"
            "PMと編成評価へ同じ本文\n"
            "sand-workflow:completion-handoff\n"
            "構成の評価はしない"
        )
        self.assertEqual(
            lock_errors(fixture, LEDGER_NEEDLES),
            ["missing EVAL-READY"],
        )


if __name__ == "__main__":
    unittest.main()
