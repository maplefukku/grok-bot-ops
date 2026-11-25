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

## pstack 0.15.34 の `/statechart`

- 内容: PR 977、PR 982、PR 983（merged 2026-10-27 13:08–13:33 JST）。`statechart SPEC.tla` は 1 コマンドで、TLC で TLA+ model を調べ、Mermaid の statechart を描き、壊れた各 rule への最短 path を報告する。TypeScript は build なしで、Node 22.18 以降、Bun 1.1.5 以降、または Deno 2.0 以降で走る。signal で殺された check は exit 2。出力を書くのは exit 0 と 1 だけ。`/statechart` skill は、chart から TLA+ への skeleton、spec に対する code audit、fixed marks を外した。PR 982 は、property trace が qualified action name を保つ。
- 出典: [PR 977](https://github.com/cursor/plugins/pull/977) · [PR 982](https://github.com/cursor/plugins/pull/982) · [PR 983](https://github.com/cursor/plugins/pull/983)（2026-10-27）
- 確認: 未

## pstack Orchestrate は agentic

- 内容: PR 1043（merged 2026-10-28 08:12 JST）。coordinator は Task で worker を起こし、program の状態を Project tracker（notes.md）に置き、PR と CI の event subscription で PR を見る。code は書かない。orch script は呼ばない。polling loop は走らせない。topology は、PR あたり owner 1 人、独立した task ごとに新しい worker、sub-coordinator は深くて 3 段、PR ごとに別の model family の verifier、広げる前に pilot を 1 単位。supervision は、各 kickoff が完了を示す evidence を名指しし、coordinator は報告の前に diff と、生きている `gh pr view` と `gh pr checks` の出力を読む。
- 出典: [PR 1043](https://github.com/cursor/plugins/pull/1043)（2026-10-28）
- 確認: 未

## 少数の Bot と、自分で skill を書く

- 内容: lauren @poteto（2026-11-01 02:01 JST）。良い Bot は少なく。Bot は教えられると自分の skill を書く（任意で private の GitHub repo）。connector、Vault、自分の email を渡す。copy-paste や手作業は Bot に引き継がせる。intern のように onboard する。voice で考えを出し、「自分の言葉で言い直して」と頼む。
- 出典: [x.com/poteto/status/2116576229319233596](https://x.com/poteto/status/2116576229319233596)（2026-11-01）
- 確認: 未

## Grok Bot と Cursor で作った game の検証

- 内容: lauren @poteto（2026-11-02 08:57 JST）。Grok Bot と Cursor で game を作った。約 1,150 PR を 4 日、初回 download の予算で build を落とす約 124 KB gz は、side project の自己申告で、benchmark ではない。60 fps で敵 500 は目標で、測定値ではない。見つけた bug class ごとに lint rule。主要な system ごとに TLA+ の formal verification skill を 1 つ（state machine ごとではない）。`.hot.ts` の path context と、allocation を禁じる lint。deterministic な sim。headless の Bot が難度を調整する。comment は lint で禁じる。
- 出典: [x.com/poteto/status/2117043478140276847](https://x.com/poteto/status/2117043478140276847) · [launch](https://x.com/poteto/status/2117004709198475365)（2026-11-02）
- 確認: 未

## adversarial review より実測と形式手法

- 内容: poteto（pstack の作者）。adversarial な agent の code review は、nitpick と YAGNI に迷うので token の無駄がほとんど。その token は、動かして測る実測と、formal verification に使う。pstack は interrogate skill をあまり使わなくなり、外すかもしれない。
- 出典: [x.com/poteto/status/2117437607940681849](https://x.com/poteto/status/2117437607940681849)
- 確認: 未

## 形式手法の層と /statechart

- 内容: poteto。形式手法は agent の作業では限界がある。仮定のもとで spec との一致を示す。層は (1) constraint、type、lint (2) 実測の test と eval (3) 熱い経路の形式手法（TLA+ / TLC、Lean / Dafny、CBMC / Kani）。意図の review には /statechart（pstack の statechart skill）を使う。形式手法は bug の無い code を保証しない。spec は人から来て、数学からではない。model と code はずれ得る。
- 出典: [x.com/poteto/status/2118416074601545968](https://x.com/poteto/status/2118416074601545968) · [statechart skill](https://github.com/cursor/plugins/tree/main/pstack/skills/statechart) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568042366718447687)
- 確認: 未

## token は検証が先

- 内容: Cindy Sridharan（@copyconstruct）の自己申告。検証の手順を足したあと、以前の agent PR の痛みは消えた。1 日の token の約 70% は patch の検証、作るのは約 20–30%。merge の前は full CI build ではなく、狙いを絞った micro-test を使い、空いた compute を agent の深い分析に回す。
- 出典: [2118529738532925725](https://x.com/copyconstruct/status/2118529738532925725) · [2118544247129276756](https://x.com/copyconstruct/status/2118544247129276756) · [2118539184654938154](https://x.com/copyconstruct/status/2118539184654938154) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568104033246253196)
- 確認: 未

## 変更を検証可能にする prompt

- 内容: Matt Pocock の常設 prompt「How do we make this change fully verifiable?」は、agent に、緑だと言うだけでなく、本物の service への sign-up と frontend の click-through で変更を示すよう押す。使い方は、agent の patch のあとの既定の検証の問い。検証は script か e2e として commit し、次の agent が証明を再利用する。個人の prompt の助言。品質が上がったという自己申告。測った数字は無い。関連として挙げるだけで、追加の主張はしない。CloudflareDev の security-audit skill と、alibi hook。
- 出典: [x.com/mattpocockuk/status/2118313863917564136](https://x.com/mattpocockuk/status/2118313863917564136) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568165436367831061) · [CloudflareDev](https://x.com/CloudflareDev/status/2118013149538390253) · [alibi](https://x.com/neil_xbt/status/2118542135108800612) · [repo](https://github.com/codegobrrrr9/alibi)
- 確認: 未

## skill と自己改善のループ

- 内容: Ben Holmes（Warp、AI Engineer の talk。2026-11-08 05:54 JST）。team の agent trace（transcript、tool call、出力）を集める。採点する agent が、LLM-as-judge の rubric（talk の例は efficiency、verbosity、redundant tests）で会話を採点する。自己改善の pass（talk は cron。例は直近の失敗を毎日）が skill か config の変更を提案する。点数を時間で残し、merge した skill を、主張ではなく折れ目と照合する。ここでの使い方は、session のあと既存の reflect skill で、小さい rubric に照らして trace を見、繰り返す失敗から skill か config を更新する。新しい agent は立てない。任意の一回は、local の setup に Skill Doctor。自己申告の talk と Warp の demo。独立した研究は無い。出典は改善率を書いていない。Skill Doctor と Warp Factories は、この型の Warp の実装。訂正: 提案は人が見るまで採用しない。Warp の公式 blog は、本当の A/B test ではないと書く。BHolmes は Warp の DevEx engineering を率いる。改善率の数字は無い。Skill Doctor の URL は https://www.warp.dev/skill-doctor （古い /skilldoctor は 404）。
- 出典: [x.com/BHolmesDev/status/2119171765343854726](https://x.com/BHolmesDev/status/2119171765343854726) · [talk](https://www.youtube.com/watch?v=pz74r-4dGfQ) · [Skill Doctor](https://www.warp.dev/skill-doctor) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568889369274617926)（2026-11-08）
- 確認: 未

## coding agent をチームのように扱う

- 内容: Addy Osmani の X Article（2026-11-08 16:32 JST、Your coding agents made you a manager）。coding agent をチームを扱うように動かす。pass/fail の検査（test、build、lint、diff script、screenshot）を渡し、結果を証明として求める。検証の command は CLAUDE.md に書く。brief は repo が見せられないものだけ（なぜ、制約、範囲外、検査）。2 回直したことは CLAUDE.md か共有 skill に入れる。prompt、CLAUDE.md、skill は依頼。hook、deny rule、managed setting は常に強制される。doc の行が無視されるなら hook にする。hook が好みだけなら外す（Over-process is the new micromanagement）。先に計画し、別の session がその計画を見る。重ならない task に分ける。2 回直して失敗したら、session を消して prompt を書き直す。人は product、security、出荷の判断を残す。緑の 600 行 diff を承認するのは code ratification で、review ではない（The unit of review is the unit of comprehension.）。無人の実行の前に 5 つ答える。完了の姿、自分での検証、境界、guardrail（turn か spend の上限）、出力の行き先と誰が承認するか。3 file で試し、試用期間を置く。注意ではなく検証を拡げる（orchestration tax）。測るのは cycle time、revert、手戻りで、AI が書いた code の割合ではない。WIP を限る。review と検証が足りない資源だから。ここでの使い方は、検査と証明に create-verification-skill と prove-it-works、2 回直したら AGENTS.md か skill に reflect、AGENTS.md から ADR の folder、硬い規則だけ tollgate 風の hook、計画の review に architect skill と Elephant-Goldfish。新しい agent は立てない。訂正: 記事は AGENTS.md を書いていない（CLAUDE.md だけ。上の AGENTS.md への対応はこちらの翻案）。manager になるというキャリアの助言ではない。ほかの仕事を可能にして良い結果を出す、という意味。実践のエッセイで、測った結果は無い。例の brief の p95 の数字は just for example。tool の例（/goal、/batch、/rewind、/code-review、Stop hook）は Claude Code 固有で、やり方は持ち越せる。著者は Anthropic で Claude Code に関わる（X bio は Claude Code @anthropicai）。すでに出ている proof-of-work（thdxr）、fully-verifiable（mattpocockuk）、ADR（kentcdodds）と一部重なる。新しいのは、manager の playbook の枠、依頼と強制の区別、2 回失敗したら reset、無人の 5 問、orchestration tax。
- 出典: [x.com/addyosmani/status/2119332146485891501](https://x.com/addyosmani/status/2119332146485891501) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568949296693383168)（2026-11-08）
- 確認: 未

## guard は本物の経路で試す

- 内容: hook か deny rule が試されたと言えるのは、その guard だけが拒める段で、agent が自分の tool call で禁じられた動作をしようとするのを見たあと。hook script に sample JSON を pipe すると matcher を飛ばす。agent が guard を足したと言うことは、disk にある証明ではない。事例は、Claude Code の PreToolUse の delete hook が手で pipe した JSON では通り、matcher「Write|Edit|MultiEdit|NotebookEdit」が Bash を外したので、11 時間 39 分、shell command を 0 件しか見ていなかった。drill は呼び出しを分ける。`rm -rf records/events`（hook）、python の shutil.rmtree（sandbox）、未 commit の行がある file への `git checkout -- file`（hook だけが捕まる）。settings を変えたらやり直す。自己申告。Claude Code 2.1.302、macOS、bypassPermissions。like は 1。subprocess の git checkout の穴は開いたまま。訂正: Towow.ai を著者の会社と呼ばない。表示名が repo Towow-ai/harness-patterns に関わるだけで、所有は未確認。試験は本番ではなく、偽の file の捨てる repo。公式の hooks docs では、matcher を省くとすべての tool が対象。
- 出典: [x.com/NatureBlueee/status/2119558107726540949](https://x.com/NatureBlueee/status/2119558107726540949) · [reply](https://x.com/NatureBlueee/status/2119558108821291394) · [drill](https://github.com/Towow-ai/harness-patterns/blob/main/03-guarded-delete/README.md) · [hooks](https://code.claude.com/docs/en/hooks#matcher-patterns)（2026-11-09）
- 確認: 未

## review は人のコメントで採点する

- 内容: Michael Elabd（Trajectory Labs の共同創業者、元 DeepMind。2026-11-09 07:47 JST）。code review の agent は本物の bug を見つけるが、slop に埋もれる。チームのエンジニアが手で書いた review comment の dataset を作り、Trajectory Labs の platform で Greptile の review agent を 3 つの目的で post-train した。(1) 短さ（word count）(2) 人の言葉への近さ（LLM-as-a-judge）(3) Greptile が見つける bug との一致。thread は frontier model より揃い、安いと書く（chart だけで、vendor の自己申告）。訂正: Elabd は 3 つの目的で Greptile の review agent を Trajectory Labs の platform 上で post-train した（採点だけではない）。訓練の方法の詳細は無い。Greptile 自体は変えていない。こちらの使い方は採点だけ（既存の reflect か pr-2 の rubric）。fine-tuning はしない。数字は彼の chart だけ（held-out 333 で 0.645 から 0.843、1.64 ドル。GPT-6 Astra は 0.815、33 ドル）。第三者の eval は無い。
- 出典: [x.com/MichaelElabd/status/2119562604024909847](https://x.com/MichaelElabd/status/2119562604024909847)（2026-11-09）
- 確認: 未
