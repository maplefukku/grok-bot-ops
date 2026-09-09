# Shared one computer（owner 席 WRAP）

## Purpose

[issue 91](https://github.com/maplefukku/grok-bot-ops/issues/91) の WRAP である。ADOPT 行は [`trend-log.md`](../decisions/trend-log.md) の 2026-09-07 Shared one computer である。一次は [`docs/knowhow/computer.md`](../knowhow/computer.md) の「Bot を増やせとは公式は書いていない」と [x.com/madogiwacowork/status/2096721289599922688](https://x.com/madogiwacowork/status/2096721289599922688)、[Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps) である。引用は [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[Cloud開発](sand-workflow:cloud)、tool-path-prefer、schedules-force-agency、[`quiet-test.sh`](../../scripts/quiet-test.sh)、poteto-mode である。

このページは WRAP だけである。新しい席は invent しない。新しいテスト本体は invent しない。並列マシンは invent しない。CreateAgent NONE である。

## 対象

CBO（CreateAgent と席設計）、schedules-force-agency を持つ席、編成評価、PdM である。

## 範囲

### 対象にする

CreateAgent の前チェックと、schedules-force-agency の前チェックである。共有 1 マシン上の owner 席と、詰まったときだけの specialist と、成果物の handoff である。

### 対象にしない

CreateAgent NEW seats は対象外である。wipe の発明は対象外である。プロダクトコードは対象外である。監視の cron 時計は変えない。品質Drive の HOLD は再開しない。

## SoT

席の台帳は [`bots/README.md`](../../bots/README.md) である。席ゲートは [ADR 0003](../decisions/0003-domain-unit-throughput.md) の決定 4 と 5 である。CreateAgent は [`bots/CBO.md`](../../bots/CBO.md) である。knowhow は [`docs/knowhow/computer.md`](../knowhow/computer.md) である。knowhow は日付付きの観察であり、正本ではない。

## bake

| 事実 | 値 |
|---|---|
| owner 席 | 1 JOB につき成果物の持ち主は既存の 1 席 |
| specialist | 詰まったときだけ。既存席から出す。例は ChatGPT Astra Pro、OSS調査、Mini Codex。CreateAgent しない |
| handoff | 共有 1 マシンでは成果物（PR URL、issue、ファイル）で受け渡す。並列マシンは発明しない |
| 人が触る | 戻せないことだけ（spend、sign、send、ログイン）。[ADR 0004](../decisions/0004-chat-secrets-webhook-astra-thrift.md) と同型 |
| リポ作業 | Cloud Agent。[Cloud開発](sand-workflow:cloud)、tool-path-prefer。並列は CA 側で取る（[parallel-fire-fleet](sand-workflow:parallel-fire-fleet)）。共有マシン上の席を増やして並列にしない |
| 席 | 足す前に減らす |

## チェックリスト

### CreateAgent チェック（CBO）

どれかが新規席に落ちるなら REJECT である。

1. Marketplace の KEEP または WRAP を先に見たか。
2. owner 席は既にあるか。
3. 詰まりは既存 specialist で足りるか。
4. 成果物 handoff で足りるか。
5. 空殻席にならないか。
6. 減らす席はどれか。

### schedules-force-agency チェック

1. schedule は owner 席に 1 本である。
2. 同じ JOB の第二 cron を置かない。型は [`監視`](../../bots/監視.md) である。
3. 共有マシンでの schedule は handoff で受け渡す。並列マシンを立てない。
4. 詰まりで specialist を schedule に足さない。都度の JOB である。
