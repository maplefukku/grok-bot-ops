# bots/

稼働中の Grok Bot の台帳です。coordinator（人間またはメインボット）は、ここを見て誰に何を渡すか決めます。コード工場ではありません。ボットの本体もスキルも、ここへコピーしません。

1 ボット 1 ファイル。[`_template.md`](./_template.md) から作ってください。

## 台帳が答えるべき質問

- そのボットの名前と id
- どのグループか
- 役割は何か（1行）
- 回すまで待つか
- このリポジトリに routine 原稿があるか。無ければ `無し`

毎日の collect / maintain はブランチ `ops/daily-YYYY-MM-DD` 1本と draft PR 1本に積む。ボットはマージしない。

## 司令室

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`PdM`](./PdM.md) | チーフ・オブ・スタッフ。優先順位を決め、開発は 開発リーダー、PR は PR確認。ボットへの依頼は独立なら並列で渡してよい。マージはCIグリーンだけではしない。Cursor bot終了かつコメント全部resolvedまで待つ。ユーザーへは日本語。ボット間はプロトコル。コードは書かない。入口は poteto-mode。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`GTM`](./GTM.md) | product.gtm。公式 https://x.ai/bot/guides/grok-bot-for-gtm 。CoSはPdM。ZuruNote / sauna-master / gakuse-ai のローンチ資料。公開はPdMかユーザーのyes。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発リーダー`](./開発リーダー.md) | impl.conductor。開発リーダー。ZuruNoteは開発ZuruNote、sauna-masterは開発sauna-master、gakuse-aiは開発gakuse-ai、grok-bot-opsは開発grok-bot-opsへ回す。独立したプロダクト仕事は並列。Cloud Agentは立てない。プロダクト実装の CA ENV default は machine zurunote-ios-mini。grok-bot-ops は Cursor cloud VM。Planner は Cursor VM。main向けPRはready。draftは捨て検証だけ。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Planner`](./Planner.md) | plan.only。grill-with-docs で to-spec にする。出典は mattpocock/skills。Cloud Agent は plan/spec のテキストだけ書き、GitHub issue は作らない。issue 起票は Planner が gh で行う。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`OSS調査`](./OSS調査.md) | oss.survey。車輪の再発明をしない。GitHubはboxブラウザ。既存OSSのURL・ライセンス・最終push・できること・不足をPdMへ。cloneしない。PRもマージもしない。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`案件切り出し`](./案件切り出し.md) | issue.cut。CI 非依存の issue を1件、PdM と Planner の両方へ渡す。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発ZuruNote`](./開発ZuruNote.md) | impl.via。https://github.com/maplefukku/ZuruNote を Cloud Agent で実装する。計画 issue は Planner から受ける。CA ENV default は machine zurunote-ios-mini。main 向け PR は ready-for-review。draft は捨て検証だけ。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発sauna-master`](./開発sauna-master.md) | impl.via。https://github.com/maplefukku/sauna-master を Cloud Agent で実装する。計画 issue は Planner から受ける。CA ENV default は machine zurunote-ios-mini。main 向け PR は ready-for-review。draft は捨て検証だけ。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発gakuse-ai`](./開発gakuse-ai.md) | impl.via。https://github.com/maplefukku/gakuse-ai を Cloud Agent で実装する。計画issueはPlannerから。INは開発リーダーかPdM。CA ENV default は machine zurunote-ios-mini。main向けPRはready。draftは捨て検証だけ。Linux CIは lima gakuse-ci / gakuse-ci-2。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`開発grok-bot-ops`](./開発grok-bot-ops.md) | impl.via。https://github.com/maplefukku/grok-bot-ops を Cloud Agent で実装する。INは開発リーダーかPdM。CA ENV default は Cursor cloud VM。main向けPRはready。draftは捨て検証だけ。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`CI運用`](./CI運用.md) | ci.ops。ZuruNote と sauna-master。Linux の主は Mac mini Lima の gakuse-ci / gakuse-ci-2。zurunote-linux-1/2 は使わない。Swift の主は Xcode Cloud。残時間がほぼ0のときだけ Mac mini に切り替える。XC と Mac の Swift 二重実行はしない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Apple運用`](./Apple運用.md) | apple.asc。Usage 時間を見る。残りがほぼ0なら PdM に知らせ、Mac mini が Swift を受ける。対象は ZuruNote と sauna-master。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Cursor運用`](./Cursor運用.md) | cursor.dashboard。Cloud Agent・Bugbot・Automations を見る。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`Mini運用`](./Mini運用.md) | mini.ops。登録マシン fukku-mac-mini で Shell と Codex CUA。ssh-GUI禁止、余分な XC / Archive 開始禁止、15件PRキュー禁止。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`ChatGPT Pro`](./ChatGPT_Pro.md) | chatgpt.pro.advisor。行き詰まったときの相談。ChatGPT感性とも note執筆とも別。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`PR確認`](./PR確認.md) | 全プロダクト PR の目的・ユーザー変化・CI・コンフリクト・残課題と isDraft を見る。main 向けは ready。draft は捨て検証だけ。マージ可はグリーンかつ Cursor-bots 完了かつスレッド resolved のときだけ。自動で見続けない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |

## 外側ループ

正本は [`routines/collect-grokbot-knowhow.md`](../routines/collect-grokbot-knowhow.md) と [`routines/maintain-verification.md`](../routines/maintain-verification.md)。

| 名前 | 役割 | 回すまで動かない |
|---|---|---|
| [`Knowhow収集`](./Knowhow収集.md) | collect-grokbot-knowhow を回し、`docs/knowhow/` だけに出典付きで書く。毎日1本の `ops/daily-YYYY-MM-DD` draft PR に積む。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`検証メンテ`](./検証メンテ.md) | maintain-verification を回し、verify スキルと `products/` 台帳だけを対象にする。台帳が空なら対象なし。毎日1本の `ops/daily-YYYY-MM-DD` draft PR に積む。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`台帳更新`](./台帳更新.md) | ledger.grok-bot-ops。bots/ と routines/ を更新する。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`最先端手法`](./最先端手法.md) | discord.cutting-edge。手法を1つ gakuse.ai の Discord へ出す。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | いいえ |
| [`note執筆`](./note執筆.md) | note.writer。1次調査のあと chatgpt.com Pro で書く。「出して」まで投稿しない。ChatGPT Pro（相談）とも ChatGPT感性とも別。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |
| [`UI調査`](./UI調査.md) | ui.research。近い事例の URL と、なぜ近いかを返す。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） | はい |

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
