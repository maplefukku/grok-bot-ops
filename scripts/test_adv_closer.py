#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from adv_closer import (  # noqa: E402
    ADV_THRASH,
    MUST_KINDS,
    MUST_ROW,
    NIT_KINDS,
    NIT_ROW,
    Commit,
    ContractError,
    Dup,
    Fact,
    Fix,
    History,
    Keep,
    Kind,
    Must,
    Nit,
    Owed,
    Prior,
    Row,
    Skip,
    State,
    Theme,
    ThreadRef,
    ThreadState,
    Thrash,
    Url,
    Weight,
    closer_rows,
    decide,
    settle,
    weight_of,
)

ROOT = Path(__file__).resolve().parents[1]
PROCESS_README = ROOT / "docs" / "process" / "README.md"
ADR_0003 = ROOT / "docs" / "decisions" / "0003-domain-unit-throughput.md"

NIT_LINE_LOCK = "NIT <直す|直さない>。<理由 1 文>。<commit または参照 URL>。resolve。"

README_NEEDLES: tuple[str, ...] = (
    "## A. スレッドの分類",
    "MUST",
    "NIT",
    "DUP",
    *(kind.value for kind in Kind),
    "WONTFIX",
    "どちらも resolve する",
    "返信は最大 1 回",
    "各スレッド返信 ≤ 1",
    "新しい failing check",
    "同テーマ",
    "bot が違っても同テーマ",
    "先行スレッド",
    ADV_THRASH,
    NIT_LINE_LOCK,
    "Closer は Resolve を所有する",
    "HOLD",
    "Closer の終端は resolve である",
    "Owed と HOLD は終端ではない",
    MUST_ROW,
    NIT_ROW,
    "Closer は Flag しない",
)
ADR_NEEDLES: tuple[str, ...] = (
    "ADV closer",
    "CreateAgent",
    "MUST は終端する。NIT は 1 回で終わる",
    "席は増えない。CreateAgent は動かない",
    "新しい bot ファイルは作らない",
)
PARSER_MUST_FAIL_WITHOUT: tuple[str, ...] = (
    ADV_THRASH,
    "WONTFIX",
    "HOLD",
    NIT_LINE_LOCK,
    "Closer は Flag しない",
)
COMPLETE_README_FIXTURE = "\n".join(README_NEEDLES) + "\n"

PRIOR_REF = ThreadRef("PRRT_old")
SELF_REF = ThreadRef("PRRT_self")
STYLE_THEME = Theme(file="api/handlers.py", lines=(40, 52), kind=Kind.STYLE)
RENAME_THEME = Theme(file="Sources/App/Foo.swift", lines=(10, 20), kind=Kind.RENAME)
SECURITY_THEME = Theme(file="apps/api/auth.py", lines=(88, 91), kind=Kind.SECURITY)


def lock_errors(text: str, needles: tuple[str, ...] = README_NEEDLES) -> list[str]:
    return [f"missing {needle}" for needle in needles if needle not in text]


def _fact(
    *,
    thread: ThreadRef = SELF_REF,
    theme: Theme = RENAME_THEME,
    new_failing_check: bool = False,
    history: History = History.FRESH,
    human_hold: bool = False,
    prior: tuple[Prior, ...] = (),
    verdict: Fix | Skip | None = None,
) -> Fact:
    return Fact(
        thread=thread,
        theme=theme,
        new_failing_check=new_failing_check,
        history=history,
        human_hold=human_hold,
        prior=prior,
        verdict=verdict,
    )


class NitFirstReplyTests(unittest.TestCase):
    def test_given_fresh_rename_and_no_verdict_when_decide_then_owed_nit(self) -> None:
        self.assertEqual(decide(_fact()), Owed(weight=Weight.NIT))

    def test_given_fresh_rename_and_skip_when_decide_then_nit_reply_is_lock_line(self) -> None:
        fact = _fact(
            verdict=Skip(
                reason="名前はモジュールの慣例に従っている",
                ref=Url("https://github.com/maplefukku/ZuruNote/blob/main/STYLE.md"),
            )
        )
        self.assertEqual(
            decide(fact),
            Nit(
                reply=(
                    "NIT 直さない。名前はモジュールの慣例に従っている。"
                    "https://github.com/maplefukku/ZuruNote/blob/main/STYLE.md。resolve。"
                )
            ),
        )

    def test_given_fresh_style_and_fix_when_decide_then_nit_reply_says_naosu_with_commit(self) -> None:
        fact = _fact(
            theme=STYLE_THEME,
            verdict=Fix(commit=Commit("a1b2c3d"), reason="呼び手と同じ語に揃えた"),
        )
        self.assertEqual(
            decide(fact),
            Nit(reply="NIT 直す。呼び手と同じ語に揃えた。a1b2c3d。resolve。"),
        )


class ThrashTests(unittest.TestCase):
    def test_given_same_theme_prior_from_other_bot_when_no_new_check_then_thrash_points_at_prior(
        self,
    ) -> None:
        fact = _fact(
            thread=ThreadRef("PRRT_new"),
            theme=STYLE_THEME,
            prior=(Prior(thread=PRIOR_REF, theme=STYLE_THEME),),
        )
        action = decide(fact)
        self.assertEqual(action, Thrash(prior=PRIOR_REF))
        self.assertEqual(action.label, "adv-thrash")

    def test_given_reopened_nit_when_no_new_check_then_thrash_points_at_self(self) -> None:
        fact = _fact(theme=STYLE_THEME, history=History.REOPENED)
        self.assertEqual(decide(fact), Thrash(prior=SELF_REF))

    def test_given_closer_already_replied_when_no_new_check_then_never_nit_for_any_kind(
        self,
    ) -> None:
        for kind in Kind:
            for history in (History.ANSWERED, History.REOPENED):
                with self.subTest(kind=kind, history=history):
                    fact = _fact(
                        theme=Theme(file="x.py", lines=(1, 2), kind=kind),
                        history=history,
                    )
                    action = decide(fact)
                    self.assertNotIsInstance(action, Nit)


class MustTests(unittest.TestCase):
    def test_given_nit_kind_with_new_failing_check_when_no_verdict_then_owed_must(self) -> None:
        self.assertEqual(
            decide(_fact(new_failing_check=True)),
            Owed(weight=Weight.MUST),
        )

    def test_given_same_theme_prior_with_new_failing_check_when_decide_then_must_not_dup(
        self,
    ) -> None:
        fact = _fact(
            new_failing_check=True,
            prior=(Prior(thread=PRIOR_REF, theme=RENAME_THEME),),
        )
        self.assertEqual(decide(fact), Owed(weight=Weight.MUST))

    def test_given_security_and_skip_with_evidence_when_decide_then_must_closes_with_skip(
        self,
    ) -> None:
        close = Skip(
            reason="flag OFF の経路で到達不能で test_auth_flag_off が証拠",
            ref=Url("https://github.com/maplefukku/gakuse-ai/actions/runs/1234/job/5678"),
        )
        fact = _fact(theme=SECURITY_THEME, verdict=close)
        self.assertEqual(decide(fact), Must(close=close))

    def test_given_failing_test_and_fix_when_decide_then_must_closes_with_fix(self) -> None:
        close = Fix(commit=Commit("a1b2c3d"), reason="回帰テストを足した")
        fact = _fact(
            theme=Theme(file="t.py", lines=(1, 1), kind=Kind.FAILING_TEST),
            verdict=close,
        )
        self.assertEqual(decide(fact), Must(close=close))


class DupTests(unittest.TestCase):
    def test_given_security_repeat_of_prior_when_no_new_check_then_dup_points_at_prior(
        self,
    ) -> None:
        fact = _fact(
            theme=SECURITY_THEME,
            prior=(Prior(thread=PRIOR_REF, theme=SECURITY_THEME),),
        )
        action = decide(fact)
        self.assertEqual(action, Dup(prior=PRIOR_REF))
        self.assertFalse(hasattr(action, "label"))

    def test_given_answered_thread_not_reopened_when_decide_then_dup_of_self(self) -> None:
        self.assertEqual(
            decide(_fact(history=History.ANSWERED)),
            Dup(prior=SELF_REF),
        )

    def test_given_answered_thread_with_new_failing_check_when_decide_then_dup_of_self_for_any_kind(
        self,
    ) -> None:
        for kind in Kind:
            with self.subTest(kind=kind):
                fact = _fact(
                    theme=Theme(file="x.py", lines=(1, 2), kind=kind),
                    history=History.ANSWERED,
                    new_failing_check=True,
                )
                self.assertEqual(decide(fact), Dup(prior=SELF_REF))


class HoldTests(unittest.TestCase):
    def test_given_human_hold_when_any_kind_any_check_any_history_then_keep(self) -> None:
        for kind in Kind:
            for failing in (False, True):
                for history in History:
                    with self.subTest(kind=kind, failing=failing, history=history):
                        fact = _fact(
                            theme=Theme(file="x.py", lines=None, kind=kind),
                            new_failing_check=failing,
                            history=history,
                            human_hold=True,
                        )
                        self.assertEqual(decide(fact), Keep())


class IdempotentTests(unittest.TestCase):
    def test_given_same_fact_when_decide_twice_then_actions_are_equal(self) -> None:
        fact = _fact(
            verdict=Skip(
                reason="rename は別 unit",
                ref=Url("https://example.com/r"),
            )
        )
        self.assertEqual(decide(fact), decide(fact))


class BoundaryTests(unittest.TestCase):
    def test_given_two_sentence_reason_when_building_skip_then_contract_error(self) -> None:
        with self.assertRaises(ContractError):
            Skip(reason="一つ。二つ", ref=Url("https://example.com/r"))

    def test_given_empty_commit_when_building_fix_then_contract_error(self) -> None:
        with self.assertRaises(ContractError):
            Fix(commit=Commit("  "), reason="揃えた")

    def test_kinds_partition_must_and_nit(self) -> None:
        self.assertEqual(frozenset(Kind), MUST_KINDS | NIT_KINDS)
        self.assertEqual(MUST_KINDS & NIT_KINDS, frozenset())


class NoChromeTests(unittest.TestCase):
    def test_module_source_has_no_github_client_no_createagent_and_imports_no_network(
        self,
    ) -> None:
        source = (_SCRIPTS / "adv_closer.py").read_text(encoding="utf-8")
        lower = source.lower()
        for token in ("github", "httpx", "requests", "urllib", "subprocess", "createagent", "flag"):
            self.assertNotIn(token, lower)
        for name in ("github", "httpx", "requests"):
            self.assertNotIn(name, sys.modules)


class LockWrapTests(unittest.TestCase):
    def test_process_readme_section_a_contains_lock_words(self) -> None:
        self.assertEqual(lock_errors(PROCESS_README.read_text(encoding="utf-8")), [])

    def test_adr_0003_contains_lock_words(self) -> None:
        self.assertEqual(
            lock_errors(ADR_0003.read_text(encoding="utf-8"), ADR_NEEDLES),
            [],
        )

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(lock_errors(COMPLETE_README_FIXTURE), [])

    def test_parser_rejects_fixture_missing_required_token(self) -> None:
        for token in PARSER_MUST_FAIL_WITHOUT:
            with self.subTest(missing=token):
                stripped = COMPLETE_README_FIXTURE.replace(token, "")
                found = lock_errors(stripped)
                self.assertTrue(found, f"missing {token} was accepted")
                self.assertIn(token, "\n".join(found))


class SettleTests(unittest.TestCase):
    def test_given_fresh_rename_with_skip_when_settle_then_resolved_nit_and_terminal(
        self,
    ) -> None:
        fact = _fact(
            verdict=Skip(
                reason="名前はモジュールの慣例に従っている",
                ref=Url("https://github.com/maplefukku/ZuruNote/blob/main/STYLE.md"),
            )
        )
        state = settle(fact)
        self.assertEqual(
            state,
            ThreadState(
                thread=SELF_REF,
                weight=Weight.NIT,
                state=State.RESOLVED,
                replies=1,
                label=None,
            ),
        )
        self.assertTrue(state.terminal)

    def test_given_fresh_rename_no_verdict_when_settle_then_owed_nit_and_not_terminal(
        self,
    ) -> None:
        state = settle(_fact())
        self.assertEqual(
            state,
            ThreadState(SELF_REF, Weight.NIT, State.OWED, replies=0),
        )
        self.assertFalse(state.terminal)

    def test_given_human_hold_on_security_answered_when_settle_then_must_hold_not_terminal(
        self,
    ) -> None:
        state = settle(
            _fact(theme=SECURITY_THEME, history=History.ANSWERED, human_hold=True)
        )
        self.assertEqual(
            state,
            ThreadState(SELF_REF, Weight.MUST, State.HOLD, replies=1),
        )
        self.assertFalse(state.terminal)

    def test_given_same_theme_prior_style_when_settle_then_resolved_thrash_no_reply(
        self,
    ) -> None:
        fact = _fact(
            thread=ThreadRef("PRRT_new"),
            theme=STYLE_THEME,
            prior=(Prior(thread=PRIOR_REF, theme=STYLE_THEME),),
        )
        self.assertEqual(
            settle(fact),
            ThreadState(
                ThreadRef("PRRT_new"),
                Weight.NIT,
                State.RESOLVED,
                replies=0,
                label="adv-thrash",
            ),
        )

    def test_given_reopened_style_with_no_new_check_when_settle_then_thrash_one_reply(
        self,
    ) -> None:
        self.assertEqual(
            settle(_fact(theme=STYLE_THEME, history=History.REOPENED)),
            ThreadState(
                SELF_REF,
                Weight.NIT,
                State.RESOLVED,
                replies=1,
                label="adv-thrash",
            ),
        )

    def test_given_answered_thread_when_settle_then_dup_resolved_one_reply(self) -> None:
        self.assertEqual(
            settle(_fact(history=History.ANSWERED)),
            ThreadState(SELF_REF, Weight.NIT, State.RESOLVED, replies=1),
        )

    def test_given_rename_new_failing_check_and_fix_when_settle_then_must_resolved(
        self,
    ) -> None:
        fact = _fact(
            new_failing_check=True,
            verdict=Fix(commit=Commit("a1b2c3d"), reason="回帰テストを足した"),
        )
        self.assertEqual(
            settle(fact),
            ThreadState(SELF_REF, Weight.MUST, State.RESOLVED, replies=1),
        )

    def test_given_security_repeat_of_prior_when_settle_then_must_dup_no_reply(
        self,
    ) -> None:
        fact = _fact(
            theme=SECURITY_THEME,
            prior=(Prior(thread=PRIOR_REF, theme=SECURITY_THEME),),
        )
        self.assertEqual(
            settle(fact),
            ThreadState(SELF_REF, Weight.MUST, State.RESOLVED, replies=0),
        )


class ConvergenceTests(unittest.TestCase):
    def test_given_fresh_nit_skip_when_answered_then_reopened_then_each_settle_is_literal(
        self,
    ) -> None:
        skip = Skip(
            reason="名前はモジュールの慣例に従っている",
            ref=Url("https://github.com/maplefukku/ZuruNote/blob/main/STYLE.md"),
        )
        self.assertEqual(
            settle(_fact(verdict=skip)),
            ThreadState(SELF_REF, Weight.NIT, State.RESOLVED, replies=1),
        )
        self.assertEqual(
            settle(_fact(history=History.ANSWERED)),
            ThreadState(SELF_REF, Weight.NIT, State.RESOLVED, replies=1),
        )
        self.assertEqual(
            settle(_fact(history=History.REOPENED)),
            ThreadState(
                SELF_REF,
                Weight.NIT,
                State.RESOLVED,
                replies=1,
                label="adv-thrash",
            ),
        )

    def test_given_every_kind_failing_history_hold_prior_verdict_when_settle_then_contracts_hold(
        self,
    ) -> None:
        skip = Skip(reason="rename は別 unit", ref=Url("https://example.com/r"))
        for kind in Kind:
            for failing in (False, True):
                for history in History:
                    for hold in (False, True):
                        theme = Theme("x.py", (1, 2), kind)
                        for prior in ((), (Prior(PRIOR_REF, theme),)):
                            for verdict in (None, skip):
                                fact = _fact(
                                    thread=SELF_REF,
                                    theme=theme,
                                    new_failing_check=failing,
                                    history=history,
                                    human_hold=hold,
                                    prior=prior,
                                    verdict=verdict,
                                )
                                with self.subTest(
                                    kind=kind,
                                    failing=failing,
                                    history=history,
                                    hold=hold,
                                    prior=prior,
                                    verdict=verdict,
                                ):
                                    state = settle(fact)
                                    self.assertEqual(state.weight, weight_of(fact))
                                    if state.weight is Weight.NIT:
                                        self.assertLessEqual(state.replies, 1)
                                    action = decide(fact)
                                    self.assertEqual(
                                        state.terminal,
                                        isinstance(
                                            action, (Must, Nit, Thrash, Dup)
                                        ),
                                    )
                                    if isinstance(action, Owed):
                                        self.assertEqual(action.weight, state.weight)


class RowTests(unittest.TestCase):
    def test_given_no_threads_when_closer_rows_then_both_ok(self) -> None:
        rows = closer_rows(())
        self.assertEqual(rows, (Row(MUST_ROW, ()), Row(NIT_ROW, ())))
        self.assertTrue(rows[0].ok)
        self.assertTrue(rows[1].ok)

    def test_given_must_owed_nit_resolved_must_hold_when_closer_rows_then_must_blockers_keep_order(
        self,
    ) -> None:
        t1 = ThreadRef("T1")
        t2 = ThreadRef("T2")
        t3 = ThreadRef("T3")
        rows = closer_rows(
            (
                ThreadState(t1, Weight.MUST, State.OWED, replies=0),
                ThreadState(t2, Weight.NIT, State.RESOLVED, replies=1),
                ThreadState(t3, Weight.MUST, State.HOLD, replies=1),
            )
        )
        self.assertEqual(
            rows,
            (Row("MUST threads", (t1, t3)), Row("NIT threads", ())),
        )

    def test_given_nit_owed_and_must_resolved_when_closer_rows_then_nit_blocks(
        self,
    ) -> None:
        nit_thread = ThreadRef("NIT_owed")
        must_thread = ThreadRef("MUST_resolved")
        rows = closer_rows(
            (
                ThreadState(nit_thread, Weight.NIT, State.OWED, replies=0),
                ThreadState(must_thread, Weight.MUST, State.RESOLVED, replies=1),
            )
        )
        self.assertEqual(
            rows,
            (Row("MUST threads", ()), Row("NIT threads", (nit_thread,))),
        )
        self.assertTrue(rows[0].ok)
        self.assertFalse(rows[1].ok)

    def test_given_closer_rows_result_when_read_then_two_named_rows(self) -> None:
        rows = closer_rows(())
        self.assertEqual(len(rows), 2)
        self.assertEqual([row.name for row in rows], ["MUST threads", "NIT threads"])


class ThreadStateBoundaryTests(unittest.TestCase):
    def test_given_nit_replies_two_when_building_then_contract_error(self) -> None:
        with self.assertRaises(ContractError):
            ThreadState(SELF_REF, Weight.NIT, State.RESOLVED, replies=2)

    def test_given_negative_replies_when_building_then_contract_error(self) -> None:
        with self.assertRaises(ContractError):
            ThreadState(SELF_REF, Weight.MUST, State.RESOLVED, replies=-1)

    def test_given_unknown_label_when_building_then_contract_error(self) -> None:
        with self.assertRaises(ContractError):
            ThreadState(
                SELF_REF, Weight.MUST, State.RESOLVED, replies=0, label="other"
            )

    def test_given_reopened_security_with_new_check_and_fix_when_settle_then_must_two_replies(
        self,
    ) -> None:
        fact = _fact(
            theme=SECURITY_THEME,
            history=History.REOPENED,
            new_failing_check=True,
            verdict=Fix(commit=Commit("a1b2c3d"), reason="回帰テストを足した"),
        )
        self.assertEqual(
            settle(fact),
            ThreadState(SELF_REF, Weight.MUST, State.RESOLVED, replies=2),
        )


if __name__ == "__main__":
    unittest.main()
