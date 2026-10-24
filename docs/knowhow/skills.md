# skills

Grok Bot の skill（再利用できる手順の単位）の作り方と使い方。Teach a task の手順は [`routines.md`](./routines.md) にある。

## GitHub Security Lab の Fuzzing Taskflow

- 内容: C/C++ の GitHub repository を指すと、entrypoint の特定、build の解析、harness の作成、AFL++ の実行、coverage の読み取り、crash の triage、unique bug ごとの vulnerability report までを agent が進める、と GitHub Blog と @github。実行は [seclab-taskflows-fuzzing](https://github.com/GitHubSecurityLab/seclab-taskflows-fuzzing) の codespace で `./scripts/fuzzing/run_fuzzing.sh PROJECT`。引数は `owner/repo`。記事は、`afl-fuzz` と `clang` と、LLM が選んだ build コマンドを、container を挟まず host 上で実行するので、使い捨て環境（Codespace か捨てられる VM）で、昇格した権限なしに走らせる、と書く。既定モデルは Claude Sonnet 5。別モデルは `src/seclab_taskflows_fuzzing/configs/model_config.yaml`。
- 出典: [AI-powered fuzzing with the GitHub Security Lab Taskflow Agent](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/)（2026-09-24） · [repo](https://github.com/GitHubSecurityLab/seclab-taskflows-fuzzing) · [x.com/github/status/2109364666237350135](https://x.com/github/status/2109364666237350135)（2026-10-11）
- 確認: 未

## サポート Bot に billing などリスクの高い系統も繋ぐ

- 内容: 安全なツールだけではサポート自動化は足りない。請求やリスクの高い部分を繋いで、痛みのあるところを Bot が触れるようにする、という助言。
- 出典: [x.com/ChrisSimpson/status/2100002853565665639](https://x.com/ChrisSimpson/status/2100002853565665639)（2026-09-15）
- 確認: 未

## Agent の day-zero 期待（新入社員扱い）

- 内容: Agent は day zero ではあまり上手くない。新入社員と同様に期待値を置く、という product-team ライブストリーム上の助言。
- 出典: [x.com/ChrisSimpson/status/2099989191706780073](https://x.com/ChrisSimpson/status/2099989191706780073)（2026-09-15）
- 確認: 未

## skill は再利用できるワークフローの単位

- 内容: skill は「いつ使うか、手順、判断ルール、期待する出力、境界」を持つ再利用できるレシピ。自分で書く、直す、Teach a task で Bot のコンピュータ上の作業を録画してデモから下書きさせる、のいずれでも作れる。チャットの記憶は 1 会話に閉じるが、skill は自分の全 Bot で共有され、他の Bot が呼べ、routine が指せ、template に指示・skill・routine をまとめて同梱して配れる、という主張。
- 出典: [x.com/brianzhan1/status/2097455378179162132](https://x.com/brianzhan1/status/2097455378179162132)（2026-09-08）
- 確認: 未

## pstack `/create-formal-verification-skill`

- 内容: PR 709（merged 2026-10-18）が `/create-formal-verification-skill` を足す。PR 710 は version だけ `0.15.25` から `0.15.26`。skill は、書いた test が届かない race、retry、state machine、parser、unsafe code について、述べた範囲の全ケースで 1 つの property を見る。名前で呼び、area か bug を名指ししてもよい。強い対象を選び、tool を選んで理由を言う。当時の文は、concurrent / distributed では TLA+ をよくある出発点にし、全入力の性質には code 上の verifier、あらゆる大きさで成り立つ性質には proof、としていた。壊した変種で FAIL を見せてから pass を信じる。project-local skill を書き、次の agent が触れたかを判断し、1 コマンドで再実行し、本物の bug と modeling error を分ける。scratch の破壊で一度走らせてからその変更は捨てる。引き渡しは、何を確かめたか、tool と理由、bounds、結果、再実行、覆っていないもの。反例は code の言葉での短い手順。property を弱めて pass させず、頼まれない限り product code は変えない。`disable-model-invocation: true`。prompt と docs だけ。eval は未見の 6 repo（`timgit/pg-boss`、`vercel/swr`、`brettwooldridge/HikariCP`、`kubernetes/client-go`、`DaveGamble/cJSON`、`bluss/arrayvec`）。concurrency / distribution の 4 repo で skill の平均 29.0、先行 draft は 26.5。cJSON と arrayvec は 26.0 と 22.0。その 2 つでは checks の点が skill 3.75、draft 4.5。1 run は CBMC の loop bound が十分かを確認せず、別の 1 run は単一の実行コマンドが無かった。cJSON は CBMC、arrayvec は Kani を 4 run すべてで選んだ。n は repo と version あたり 1、skill の cJSON と arrayvec だけ 2。1 run の差は lead として扱う。event-order の tool 選択は、下の #721 が置き換えている。
- 出典: [PR 709](https://github.com/cursor/plugins/pull/709) · [PR 710](https://github.com/cursor/plugins/pull/710)（2026-10-18）
- 確認: 未

## `/setup-pstack` が formal verification を一度だけ提案する

- 内容: PR 715（merged 2026-10-18）は `/setup-pstack` の step 8 を足す。project に formal verification skill が無いとき、一度だけ `/create-formal-verification-skill` を提案し、yes ならそれを走らせる。step 7 の verification-skill 提案と同じ形。`poteto-help` と `docs/guide` は、その skill、この提案、`/ketchup`、`/sharpen`、`/in-your-own-words`、Claude Code の導入、Opening a PR の playbook、verification の Helpers、Babysit の Origin 経路（同梱 watcher は GitHub、Origin は Origin CLI）を書く。この PR は version を上げず、`maintain-formal-verification-skill` には触れていない。PR 712（merged 2026-10-18）は sharpen から「Don't hand back a rewritten prompt.」を外し、末尾を「without narrating the framing, then do the work.」にした。PR 713 はその変更だけの version bump で `0.15.26` から `0.15.27`。その末尾は 0.15.29 が置き換えている。
- 出典: [PR 715](https://github.com/cursor/plugins/pull/715) · [PR 712](https://github.com/cursor/plugins/pull/712) · [PR 713](https://github.com/cursor/plugins/pull/713)（2026-10-18）
- 確認: 未

## `/maintain-formal-verification-skill` と TLA+ の fallback

- 内容: PR 716（merged 2026-10-19）の `/maintain-formal-verification-skill` は、merge や refactor や、再チェックを飛ばした編集のあと、project-local の formal verify skill を code に合わせる。skill は名前ではなく中身で見つける。各 check は `in sync`、`updated`、`bug`、`blocked` のいずれかで終わる。product code は編集しない。pass させるために property を弱めない。blocked の check では sync commit を進めない。create skill は、覆う file と function と、最後に一致した sync commit を記録する。docs は README、poteto-help、guide の page 6 と 9。pstack の version は上げない。PR 721（merged 2026-10-19）は、event-order の問いでは言語を問わず TLA+ を既定にし、concurrent / distributed 向けだった前の文を外す。その言語で verifier が走らないときは、そう言い、関数の手書き model ではなく、生成した入力で出荷された code を試す。verifier の無い JavaScript library では、旧段落の 9 run のうち 6 が手書きの写しだけで主張を証明し、新段落の 9 run はすべて出荷された code を見た。eval は 2 つの変更を同時に、#716 の編集なしで試している。
- 出典: [PR 716](https://github.com/cursor/plugins/pull/716) · [PR 721](https://github.com/cursor/plugins/pull/721)（2026-10-19）
- 確認: 未

## pstack 0.15.29 の `/sharpen`

- 内容: PR 729（merged 2026-10-20）は `/sharpen` を元の 4 つの問いの番号リストに戻す。足すもの、一番生の材料、方法と tool、外からのチェック。加えて「Leave choices that are mine to make open instead of deciding them.」。書き直した prompt だけを返し、作業はしない。README、guide の `02-poteto-mode` と `10-recipes-and-pitfalls`、`/poteto-help` もそれに合わせた。`disable-model-invocation: true`。version は `0.15.28` から `0.15.29`。eval は事前登録の 2 round、held-out 6 場面、3 vendor の 3 model、他 vendor の盲検 judge、round あたり 36 packet。list の本文は全 gate を通り、choices を開いたままにする点は 0.50 から 1.00、judge が original より選んだ割合は 82%。使い方は `/sharpen` を走らせ、返った prompt を自分で貼るか、Bot にそれを実行するよう別に頼む。これは PR 712 の「then do the work」を置き換える。
- 出典: [PR 729](https://github.com/cursor/plugins/pull/729)（2026-10-20）
- 確認: 未
