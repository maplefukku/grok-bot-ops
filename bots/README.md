# bots/

稼働中の Grok Bot の台帳です。coordinator（人間またはメインボット）は、ここを見て誰に何を渡すか決めます。コード工場ではありません。ボットの本体もスキルも、ここへコピーしません。

1 ボット 1 ファイル。[`_template.md`](./_template.md) から作ってください。

## 台帳が答えるべき質問

- そのボットの名前と id
- どのグループか
- 役割は何か（1行）
- 回すまで待つか
- このリポジトリに routine 原稿があるか。無ければ `無し`
- 各ボットファイルに `スキル` 行があるか（共有スキル。本体は置かない。無ければ `無し`）
- S1–S7 の対応は下の LOCK: S1–S7

毎日の collect / maintain はブランチ `ops/daily-YYYY-MM-DD` 1本と draft PR 1本に積む。ボットはマージしない。

## LOCK: PARALLEL FIRE（ふっくー / PdM）

独立ジョブは並列で火を付ける。直列待ちしない。Cursor Cloud Agent は枠内で並列無制限（compete / 3-shot pick-best / nest 可）。ChatGPT web は HARD TAB 直列（既存 chatgpt.com タブ1つだけ。新ウィンドウ/タブ禁止。rate-limit は共有バックオフ）。スキル参照: [parallel-fire-fleet](sand-workflow:parallel-fire-fleet) / [chatgpt-web-existing-tab](sand-workflow:chatgpt-web-existing-tab)。

## LOCK: DRAFT-STACK（#32 LOCK B）

live tip = 最新 daily bots PR。live daily draft は ≤2。吸収済み residue は superseded-close（新しい tip をコメントで指す）。ROLE-CHANGE/LOCK が SoT になったら PdM が undraft。台帳ボットは merge しない。endless rewrite を一つの lander に積まない。

## LOCK: S1–S7（#12 Q2）

共有 HOW-TO は各ボットファイルの `スキル` 1行。本体は置かない。このリポジトリの `skills/` に SKILL.md は無い。作成は スキル作成へ（eval 後、1 スキル 1 PR）。CreateAgent しない。Q5 の 46 体 slim は別パス。

| S | スキル | ボット |
|---|---|---|
| S1 | [author-shared-skill](sand-workflow:author-shared-skill) | [`スキル作成`](./スキル作成.md) |
| S2 | [fleet-composition-review](sand-workflow:fleet-composition-review) | [`編成評価`](./編成評価.md) |
| S3 | [fleet-stall-sweep](sand-workflow:fleet-stall-sweep) | [`監視`](./監視.md) |
| S4 | [completion-handoff](sand-workflow:completion-handoff) | [`台帳更新`](./台帳更新.md) |
| S5 | [job-brief](sand-workflow:job-brief) | [`PdM`](./PdM.md) / [`CMO`](./CMO.md) / [`SNSリーダー`](./SNSリーダー.md) / [`開発リーダー`](./開発リーダー.md) / [`GTM`](./GTM.md) |
| S6 | [account-design-pack](sand-workflow:account-design-pack) | [`アカウント設計`](./アカウント設計.md) |
| S7 | [ci-health-sweep](sand-workflow:ci-health-sweep) | [`CI運用`](./CI運用.md) |

JOB 順は S1 → S3 → S4 → S2 → S5 → S7 → S6。Q8 の Xネタ選別 / ネタ調査 は入れ替えない。

## LOCK: DOMAIN-UNIT（#16 PdM HARD CORRECT）

出荷単位と ADV、lane、cadence の正本は [`docs/process/`](../docs/process/README.md)。採択理由は [ADR 0003](../docs/decisions/0003-domain-unit-throughput.md)。この台帳へ規則を複製しない。席は増やさない。

## 司令室

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`CEO`](./CEO.md) | ceo。FLEET APEX。ONE JOBはふっくー HITL集約とorg優先。ROUTEのみ。tech→CTO、product→CPO、マーケ→CMO、eng CoS→PdM、bot-HR→CBO。独立ジョブは並列。ChatGPTはHARD TAB直列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`CTO`](./CTO.md) | cto。PdMの上（tech）。REPORT↑CEO。ONE JOBはtech-org戦略。実装もマージもしない。CreateAgentはCBO。独立ジョブは並列。ChatGPTはHARD TAB直列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`CPO`](./CPO.md) | cpo。プロダクト戦略。REPORT↑CEO。ONE JOBは何を作るか。実装もマージもしない。SNSはCMO。独立ジョブは並列。ChatGPTはHARD TAB直列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`監視`](./監視.md) | fleet.supervisor。ONE JOBはstall sweep→PdMへJOB。sweepは平日06-22を2時間おき JST（0 6,8,10,12,14,16,18,20,22 * * 1-5）。@every 2h ではない。回すまで待たない。FEATURE切り出しもmonkeyも自分ではしない。実装はしない。スキルは fleet-stall-sweep。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`PdM`](./PdM.md) | ONE JOBは優先順位・マージ判定・人待ちの整理。開発は開発リーダー、PRはPR確認。マージはCI緑かつCursor bot完了かつスレ0のときだけ。コードもcloneもCA launchもしない。入口は poteto-mode。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`CMO`](./CMO.md) | cmo。マーケ/SNSのCoS。開発はPdMのまま。入口はSNSリーダー。今はアカウント設計へ回す。ふっくーへは日本語。ボット間はプロトコル。コードもマージもIGログインもしない。独立した専門は並列で火を付ける。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`SNSリーダー`](./SNSリーダー.md) | sns.conductor。INはCMO。今は account.design → アカウント設計。後の動画・台本・世界観はボット未作成なので作らない。Cloud AgentはCMOのgrok-bot-ops docs JOB以外立てない。独立した専門は並列で火を付ける。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`CBO`](./CBO.md) | cbo。Chief Bot Officer。ONE JOBはCreateAgentと席設計。INはCEO、PdM、CMO、編成評価。自分以外はCreateAgentしない。独立ジョブは並列。ChatGPTはHARD TAB直列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`スキル作成`](./スキル作成.md) | skill.author。INはPdMまたはCMO。共有SKILL.mdを書く。ボットにもroutineにもしない。CreateAgentはCBO経由。CreateAgentしない。コーディング系スキルは /poteto-mode。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`GTM`](./GTM.md) | product.gtm。ONE JOBは平日 gtm-morning（0 6 * * 1-5）の壁打ち→PdMへdigest。listing/store copyは明示JOBのみ。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`開発リーダー`](./開発リーダー.md) | impl.conductor。ONE JOBはROUTE+FIRE。INはPdMまたは監視。ZuruNote/sauna-master/gakuse-ai/grok-bot-opsは各開発ボットへ回す。最大並列。残り仕事があるのにアイドルはFAIL。Cloud Agentは立てない。monkeyは品質Drive。実装と調査は毎回 /poteto-mode。リポごとに pstack 必須。landerはready-for-review。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Planner`](./Planner.md) | plan.only。grill-with-docs で to-spec にする。出典は mattpocock/skills。Cloud Agent は plan/spec のテキストだけ書き、GitHub issue は作らない。issue 起票は Planner が gh で行う。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。INは最先端手法とKnowhow収集の候補。OUTはPdMへのADOPTまたはREJECTのダイジェスト1通。FIREしない。実装しない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`OSS調査`](./OSS調査.md) | oss.survey。車輪の再発明をしない。GitHubはboxブラウザ。既存OSSのURL・ライセンス・最終push・できること・不足をPdMへ。cloneしない。PRもマージもしない。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`案件切り出し`](./案件切り出し.md) | issue.cut。INはPdMまたは監視。CI非依存のissueを最大3件、PdMとPlannerと監視へ渡す。新機能のdraft経路は可。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発ZuruNote`](./開発ZuruNote.md) | impl.via。ONE JOBはCAで実装+ADVクローズ。https://github.com/maplefukku/ZuruNote 。計画はPlanner。/poteto-modeとpstack必須。CA ENVは machine zurunote-ios-mini。MONKEYは品質Drive。landerはready。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発sauna-master`](./開発sauna-master.md) | impl.via。ONE JOBはCAで実装+ADVクローズ。https://github.com/maplefukku/sauna-master 。計画はPlanner。/poteto-modeとpstack必須。CA ENVは machine zurunote-ios-mini。MONKEYは品質Drive。landerはready。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発gakuse-ai`](./開発gakuse-ai.md) | impl.via。ONE JOBはCAで実装+ADVクローズ。https://github.com/maplefukku/gakuse-ai 。計画はPlanner。/poteto-modeとpstack必須。CA ENVは machine zurunote-ios-mini。MONKEYは品質Drive。Linux CIは lima gakuse-ci / gakuse-ci-2。landerはready。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発grok-bot-ops`](./開発grok-bot-ops.md) | impl.via。https://github.com/maplefukku/grok-bot-ops を Cloud Agent で実装する。INは開発リーダーかPdM。実装と調査は毎回 /poteto-mode。リポごとに pstack プラグイン必須。CA ENV default は Cursor cloud VM。新機能PRはdraft可。残件・ユーザー可視・CI landerはready-for-review。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`CI運用`](./CI運用.md) | ci.ops。対象は ZuruNote / sauna-master / gakuse-ai。担当は GitHub Actions と Ubicloud とセルフホスト runner の健全性。Swift の主は Xcode Cloud の Build-only（ZuruNote と sauna-master）。月次時間がほぼ0のときだけ Mac mini に切り替える。XC と Mac の Swift 二重実行はしない。ZuruNote の Linux は共有 Grok Bot Linux の zurunote-linux-1/2、溢れは Ubicloud。gakuse-ai の Linux は lima gakuse-ci / gakuse-ci-2（不要なら Stopped のまま、消さない）。bare の runs-on:self-hosted は使わない。同一 SHA の二重バックエンドはしない。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Apple運用`](./Apple運用.md) | apple.asc。Usage 時間を見る。残りがほぼ0なら PdM に知らせ、Mac mini が Swift を受ける。対象は ZuruNote と sauna-master。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Cursor運用`](./Cursor運用.md) | cursor.dashboard。Cloud Agent・Bugbot・Automations を見る。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Mini運用`](./Mini運用.md) | mini.ops.CLI。ONE JOBは登録マシン fukku-mac-mini の CLI だけ。ListMachinesして Shell/Read。Codex/ChatGPT.app/GUIは Mini Codex。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`品質Drive`](./品質Drive.md) | monkey.ops。ONE JOBは weekday MonkeyTest Drive/E2E（zurunote-ios-mini）。ZuruNote/sauna-master/gakuse-ai。証拠はGitHub issue。プロダクトコードは編集しない。開発ボットはmonkeyしない。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Mini Codex`](./Mini_Codex.md) | mini.codex-cua。ONE JOBは fukku-mac-mini で ChatGPT.app Codex・CU ON。GUIはCodexが動かす。CLIはMini運用。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`ChatGPT Pro`](./ChatGPT_Pro.md) | chatgpt.pro.advisor。行き詰まったときの相談。ChatGPT感性とも note執筆リーダーとも別。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`PR確認`](./PR確認.md) | pr.review-status。ONE JOBはmerge-ok factsだけ。緑かつCursor-bots完了かつLIVE thr=0。マージはしない。main向けはready。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |

## 外側ループ

正本は [`routines/collect-grokbot-knowhow.md`](../routines/collect-grokbot-knowhow.md) と [`routines/maintain-verification.md`](../routines/maintain-verification.md)。

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`Knowhow収集`](./Knowhow収集.md) | collect-grokbot-knowhow を回し、`docs/knowhow/` だけに出典付きで書く。毎日1本の `ops/daily-YYYY-MM-DD` draft PR に積む。候補を Planner に送る。ADOPT と REJECT は自分では書かない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`検証メンテ`](./検証メンテ.md) | maintain-verification を回し、verify スキルと `products/` 台帳だけを対象にする。台帳が空なら対象なし。毎日1本の `ops/daily-YYYY-MM-DD` draft PR に積む。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`台帳更新`](./台帳更新.md) | ledger.grok-bot-ops。bots/ と routines/ を更新する。毎日のCA書き込みは grok-bot-ops-ledger-write スキルに従う（本体はコピーしない）。CA env は cloud。CAは /poteto-mode 必須。pstack プラグインは grok-bot-ops に必須。毎日の台帳が完了したら（PR積んだか変更なし）PdMと編成評価へ同じ本文で EVAL-READY。フィールドは kind / date_jst / branch / pr / counts / hold。同一 date_jst は再送しない。構成の評価はしない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`編成評価`](./編成評価.md) | fleet.review。SPEC https://github.com/maplefukku/grok-bot-ops/issues/11 。INは台帳更新のEVAL-READYまたはPdM JOB。毎日フル評価（変更なしでも）。台帳は書かない。エージェントの作成削除はPdMへ提案。開発はPdM、マーケ分割はCMO。役割のwhy調査は /poteto-mode 必須。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`最先端手法`](./最先端手法.md) | discord.cutting-edge。手法を1つ gakuse.ai の Discord へ出す。候補を Planner に送る。ADOPT と WATCH と REJECT は PdM に送らない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`note執筆リーダー`](./note執筆リーダー.md) | note.writer。REPORT↑CMO。ONE JOBはnote.com下書き。chatgpt.com Pro HARD TAB。アイキャッチはnoteサムネ。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`noteサムネ`](./noteサムネ.md) | note.eyecatch。ONE JOBはnote.comアイキャッチ。REPORT↑note執筆リーダーとCMO。本文は書かない。ChatGPTはHARD TAB直列。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`UI調査`](./UI調査.md) | ui.research。近い事例の URL と、なぜ近いかを返す。CAは /poteto-mode 必須。対象リポに pstack プラグイン必須。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |

## キャラクター生産工場

チャンネル名はボットファイルにしない。下の4体がこのグループ。

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`工場長`](./工場長.md) | DESIGN.md のワークフロー（発散→収束→検証→拡張）を回し、3スパイスを確定して SPEC.yaml を組み立てる。独立した専門（キャラ考案 / デザイン考案 / ChatGPT画像）は並列で火を付ける。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`キャラ考案`](./キャラ考案.md) | DESIGN.md の軸のうち A存在 / F内面 / G言葉と名前 / H世界と関係性 / Kポジショニング だけを担う。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`デザイン考案`](./デザイン考案.md) | DESIGN.md の軸のうち B形 / C顔 / D線と質感 / E色 / I動き / Jかわいさ / Lメディア / M制作・運用 だけを担う。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`ChatGPT画像`](./ChatGPT画像.md) | chatgpt.com で SPEC どおりに画像を生成する。軸の値は選ばない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |

## X運用

@sora19ai。指揮者は X運用。指揮者本人は X 操作も本文も書かない。

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`X運用`](./X運用.md) | @sora19ai の X 運用の指揮者。独立した HANDS は並列で火を付ける。自分では X 操作も本文も書かない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`X TL ネタ調査`](./X_TL_ネタ調査.md) | X のネタ選定。おすすめ100×3と通知 ON、軸の公式1次（GitHub / 公式ブログ）だけを見る。2次とフォロー中は使わない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`バズ投稿ネタ深掘り調査`](./バズ投稿ネタ深掘り調査.md) | ネタを受け取ったら投稿前に1次情報（公式発表・リポジトリ・原文・日時・何が変わったか）まで調べる。ツイート本文は頼まれるまで書かない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`バズ投稿メディア`](./バズ投稿メディア.md) | ネタ調査のあとメディアを探す。動画優先。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`バズ投稿`](./バズ投稿.md) | 調査済みネタから X 投稿を書く。読者は AI で自動化したい人。changelog・スペック・出典は本文に入れない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`バズ投稿ツリー`](./バズ投稿ツリー.md) | バズ投稿の本文を受け取り、リプ欄を3〜5個の一本道で書く。枝分かれさせず、出典は一番下。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`48h引用誘導`](./48h引用誘導.md) | バズ投稿ツリーのあとに、直近48時間以内の自分の投稿を最大3本引用する。枝分かれさせない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`投稿したい`](./投稿したい.md) | ユーザーから「こういう投稿がしたい」を受け取る。言っていない事実は足さない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`1次引用投稿`](./1次引用投稿.md) | 1次の元投稿を引用して意見・驚きを書く。意見の前に ChatGPT感性へネタを渡す。長文（さらに表示）。2次は引用しない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`ChatGPT感性`](./ChatGPT感性.md) | chatgpt.com からユーザーの考え・感性を取る。取れたことだけ返し、無い感想は作らず、X 投稿はしない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`通知引用`](./通知引用.md) | 自分の投稿への引用通知を開き、いいねとリポストする。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`通知リプ`](./通知リプ.md) | X 通知の他人リプを開き、いいねする。開かずに返さない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`自己リポスト`](./自己リポスト.md) | 自分の投稿を1・3・6・12・24時間後にリポスト解除して再リポストする。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |

## 最後の一針

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`アカウント設計`](./アカウント設計.md) | account.design。新規ソーシャルアカウントならどれでも（まずIG）。ブランド専用ではない。INはCMOまたはSNSリーダー（PdMはconcept LOCKか回して）。docs/<slug>/ にパックを書く。laststitch は最初の案件であり役割そのものではない。IGログインも投稿もパスワードもマージもしない。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
