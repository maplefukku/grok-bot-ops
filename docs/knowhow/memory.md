# Grok Bot のメモリの仕組み（ノウハウ）

調査: 2026-10-28 23:50–24:10 JST / Cursor＆Grok Bot特化リサーチ seat / invent=N
ラベル: **[1° official]** = 公式 URL あり、**[box verified]** = この seat の box で読み取り専用で確認（コマンドかパスを付記）。推測した内容は §9 にだけ書いた。
本文に secret・token・ユーザーの私的な内容は載せていない（フィールド名と構造だけ）。

---

## 1. 結論（5行）

1. Bot ごとに自分のメモリ（profile と journal）を持ち、名前やタイムゾーンなどユーザーに関する少数の事実だけは全 Bot で共有される（shared_profile と shared_journal）。[1° official] bots#what-a-bot-remembers
2. 保存するかどうかは Bot が自分で決め、ユーザーに確認しない。確実に残したいときは「覚えて」と頼む。確認・訂正・削除も chat で頼む（personal Bot にはメモリ画面がない）。[1° official]
3. 0.75.2 から、1つの chat で保存した内容がその Bot との全 chat で使われるようになった。0.77.0 で Settings → General → Import に Import Memory が加わった。[1° official] changelog
4. 現在のメモリの実体は box の外にある。box にある `memory/*.md` は 2026-10-04 までの古いスナップショットで、RecallMemory が返す 10/10 以降の事実は box のどのファイルにも入っていない。[box verified]
5. メモリは情報源の代わりにならない。変わる事実は元のシステムを確認し、安全のための境界は Auto-review ルールで守る。ログイン・カード・連絡先は Vault に入れる。[1° official]

---

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 2. メモリの種類と書き手

| 種類（RecallMemory の表示） | 中身 | 書き手 | 根拠 |
|---|---|---|---|
| `profile` | その Bot の役割・ルール・好みなど長く続く事実 | その Bot 本人 | [box verified] RecallMemory `within:"profile"` の出力に `[profile]` と表示 |
| `journal` | 日付つきの作業ログ | その Bot 本人 | [box verified] RecallMemory 出力の `[journal]` |
| `shared_profile` | 全 Bot に共通のユーザーの事実（名前・TZ・好み） | 各 Bot が書き、`via <Bot名>` が付く | [box verified] 出力 `[shared_profile via Buddy]` / [1° official]「a few facts about you … are shared by all your Bots」 |
| `shared_journal` | 全 Bot に共通の日付つきの出来事 | 各 Bot が書き、`via <Bot名>` が付く | [box verified] 出力 `[shared_journal via 最先端開発手法]` |

- 公式が挙げる保存対象は次の4つ。[1° official] bots#what-a-bot-remembers
  - 仕事の進め方と好み
  - 守るよう頼まれたルール
  - 名前やタイムゾーンなどユーザーに関する事実
  - 一緒にやった作業の日付つきログ
- Bot は確認なしで自分の判断で保存する。保存しても返信で触れないことがある。「Remember that …」と頼めば確実に残る。[1° official]
- 書き込み API: box にある古い prompt スナップショット（後述）には次の記述がある。
  - `update_state target "memory"` で書き込む。
  - action は `write`（tier は profile / log / note）と `forget`（記録された事実の本文をそのまま指定）。
  - scope は agent / user / project。
  - [box verified] `agents/<id>/store.db` の kv `memoryPromptSnapshot.render`（sqlite を `mode=ro` で開いた）。
  - UpdateMemory の説明は、種類を profile、journal、shared_profile、shared_journal の4つと書く。write は重複を除く。forget は、記録された事実の本文そのもので落とす。shared の事実には `[via <assistant>]` が付く。[box verified]
  - UpdateMemory が旧 `update_state target "memory"` の後継かは、まだ推測（§9）。
- `[via <assistant>]` タグ:
  - スナップショットの記述は「Shared facts are tagged [via <assistant>] so you can tell which assistant learned each one」。[box verified]
  - 旧 shard の .md にも `[via 最先端手法]` `[via ルーチン作成]` などが残っている。[box verified] `rg -o "\[via [^\]]*\]" user-memory`
- shared Bot（Teams）: チーム全体向けに保存するときはそう伝える。個人についての事実はチーム向けには保存しない。[1° official] shared-bots

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 3. 毎ターン見えるものと Recall でしか届かないもの

- 毎ターン見えるもの: prompt のメモリ欄に載る「最近の一部」だけ。古い snapshot の構成は次のとおり。[box verified] `memoryPromptSnapshot` の、事実行以外の行
  - `About the user (shared)` と `Recently (shared)`
  - 自分の `About the user` と `Recently`
  - 枠に入りきらない分は「(40 more shared profile facts on disk — call RecallMemory …)」のように件数だけ表示される。
- Recall でしか届かないもの: その枠から外れた古い journal と shared の事実。
  - RecallMemory の説明: 「Search your durable memory for facts that are not in the memory section of your prompt: older journal entries, notes that have aged out of the recent slice, and shared user facts recorded by any of this user's assistants」。[box verified] GetDynamicTools の RecallMemory schema
  - 読み取り専用。結果には日付・種類・（shared なら）書いた Bot が付く。`within` で種類を絞れる。
  - 実測: 全体検索は 1926 facts、`within:"profile"` は 20 facts が対象だった。[box verified]
- 公式の説明: 「retains stable preferences, important facts, and summaries … without replaying every prior message」。[1° official]

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 4. 優先順位・衝突・訂正

- 自分のメモリと shared が食い違ったら、自分のメモリを優先する。
  - snapshot の記述: 「when a shared user fact conflicts with your OWN memory, prefer your own — it is curated for your role」。[box verified]
- shared の事実どうしは新しい方が勝つ。
  - snapshot の記述: 「write the corrected fact into YOUR shard … the newest wins on conflict」「Never edit another assistant's shard」。[box verified]
- 旧 snapshot には project memory もあり、順位は OWN → project → user だった（「the most specific wins」）。現在もあるかは未確認（§9）。[box verified]
- 公式の訂正方法: [1° official] bots#see-correct-or-remove-a-memory
  - 確認は「What do you remember about me?」、訂正は「That's out of date. I moved to Denver.」、削除は「Forget that …」。
  - shared の事実が間違っていれば、どの Bot に正しい内容を伝えてもよい。
  - 完全に消すには、それを保存した Bot に頼む。
- Bot を削除すると、その Bot が他の Bot 向けに保存した shared の事実も一緒に消える。[1° official] bots#delete-a-bot

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 5. メモリとほかの仕組みの違い

| 仕組み | 何を入れるか | メモリとの違い | 根拠 |
|---|---|---|---|
| Skills | 手順・判断ルール・出力形式 | Private skills は全 Bot 共通のライブラリ。アプリや template に付いてきた skill は publish できない | [1° official] skills-routines-and-automations |
| （box 上の skill） | `workflows/<name>/SKILL.md`（frontmatter は name と description） | 66 フォルダ。Cursor 管理の skill は `managed-skills/skills/<name>/SKILL.md` と `cache.json` `{fetchedAt, skills[{id,name,description,body}]}`（56件）。plugin の skill は `plugin-skills/cache.json` `{authBlocked,currentUserId,fetchedAt,installFolders,skills[{id,name,description,filePath,installPath,pluginId,pluginName,pluginVersion,…}]}` | [box verified] `ls`/`jq keys` |
| Routines | いつ何を実行するか | `agents/<id>/automations/<slug>/automation.json` `{createdAt,enabled,lastRunAt,name,prompt,provenance,schedule,triggerPresentation}` と `runs.json` `[{id,requestId,startedAt,finishedAt,status,trigger}]` | [box verified] |
| Vault | ログイン・カード・連絡先（住所・電話・メール） | 「belong in Vault, not in memory」。Bot はパスワードやカード番号を見ない。chat で渡した連絡先は Vault の Contact info に保存され、保存したことが伝えられる | [1° official] bots / vault |
| Agent stores | Bot 間で共有するファイル | `/cursor/stores` は FUSE（`fuse.agent-store`）。この Bot の store `store-b02ea6c2-…` は空のディレクトリだった | [box verified] `mount`、`ls -la` |
| Bot の profile と description | 名前・アバター・説明 | `agents/<id>/profile.json` のキーは `name, description, title, avatarShape, avatarColor, namedBy, serverId, harness`。公式によると personal Bot には description も Bot settings ページもなく、変更は chat で伝える（shared Bot は About で編集） | [box verified] / [1° official] bots#edit-a-bot |
| 共有コンピュータ | ファイル・ブラウザのログイン | 全 Bot で共有。Bot を削除しても残るので、別に片付ける | [1° official] docs.x.ai/grok-bot |

- `/home/box/reference/app-ui.md` には「per-agent Settings subpage (avatar, name, title, description…)」とある。公式 docs の「Personal Bots no longer have a description」と食い違うので、新しい公式 docs を優先する。[box verified] と [1° official]

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 6. Import Memory

- 0.77.0（2026-10-26）: 「Import Memory to Grok Bot, in Settings, brings your preferences and context from another AI assistant into your primary Bot.」 Grok Bot 0.75.2 以上が必要。[1° official] changelog
- 手順: [1° official] settings-and-notifications#import と bots#import-memory-from-another-assistant
  1. Settings → General → Import で **Start Import** を押す。
  2. 表示されたプロンプトを、ほかのアシスタントとの chat に貼る。
  3. その答えを2つ目の欄に貼って **Add to Memory** を押す。
  4. Grok Bot が内容を primary Bot に送り、その chat を開く。
- 取り込み先は primary Bot だけ。shared Bot は primary Bot になれない。[1° official] bots

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 7. メモリ関連の changelog（日付は changelog の表記）

| 日付 / 版 | 内容 |
|---|---|
| 2026-09-25 | 保存したメモリや skill が多い Bot でも数秒待たずに返信し、メモリの save と forget が確実に動くようになった |
| 2026-09-26（Teams） | Publish to Team で「chat and memories」ごとチーム用にコピーするか、Start fresh を選べる。Team Bot は人ごとに private notes を持ち、アプリ・Slack・routine をまたいで使う |
| v0.75.2（2026-10-22） | personal Bot が1つの chat で保存した内容はその Bot との全 chat で使われ、変更できるのは本人だけ。Voice call が過去の通話と最近の chat を参照できる。Bot の削除で会話・メモリ・routine・添付が完全に消える |
| v0.77.0（2026-10-26） | Import Memory を追加。Team Bot につながったチームメイトは自分の connector とメモリを使う（Teams）。チームメイトの 1:1 では、別の chat で保存された本人のメモが引き継がれる（Teams）。Vault に Hints 欄が付いた（メモリではなく Vault で使い分けを指示する） |

出典はすべて https://x.ai/changelog/bot [1° official]。@bot には memory の機能告知（reply 以外の投稿）が見つからなかった（`from:bot (memory OR remember) -is:reply` で0件）。reply ではメモリより先に情報源を確認するよう繰り返し案内している（例: https://x.com/bot/status/2113466424828047471）。

- 確認: 未
## 8. box 上の構造（読み取り専用の調査）

```
/home/box/agent-data -> /home/box/sand-data   (symlink, 2026-10-18 07:56)
├─ agents/<agentId>/
│   ├─ profile.json        {name,description,title,avatarShape,avatarColor,namedBy,serverId,harness}  (harness は全 23 Bot が "temporal")
│   ├─ settings.json       {notifyOnAgentUpdates}
│   ├─ memory/profile.md   "# About the user" + "- (YYYY-MM-DD) <fact>"   ← 古いスナップショット
│   ├─ memory/log/YYYY-MM.md  "# Memory log" + 日付つきの事実
│   ├─ automations/<slug>/{automation.json,runs.json}
│   ├─ store.db (sqlite)   tables: kv, blobs, transcript_entries{seq,id,entry}, automation_completion_inbox{seq,id,text,attribution,acknowledged}
│   │    kv keys: metadata, origin, agentProfilePromptSnapshot{version,profileSection,systemIdentity{name,description},announcedIdentity,compactionEpoch},
│   │             memoryPromptSnapshot{render,compactionEpoch}, promptSectionSnapshots{memory,automations,agent_directory,mcp_instructions},
│   │             episodePending[{ts,user,agent}], lastTurnSettlement, requestIds, unreadState, …
│   ├─ conversation-blobs.db (blobs{id,data}), audit.jsonl {agentId,command,eventId,shellKind,target,ts,turnId,type}
│   └─ attachments/, assets/
├─ user-memory/            shared の旧 shard: by-agent/<agentId>/{profile.md, log/YYYY-MM.md}（43 フォルダ）, log.md, fleet-hard.md
├─ workflows/<skill>/SKILL.md   private skills（66）
├─ managed-skills/{cache.json, skills/<name>/SKILL.md}   Cursor 管理（56）
├─ plugin-skills/cache.json
├─ search-index.db         messages{id,agent_id,entry_id,role,timestamp_ms,body,seq,in_main_chat}, media, server_cursors（随時更新、chat の検索用）
├─ settings.json           app 全体の設定（keys: userTimeZone, autoReviewInstructions, mcpBoxServers, pinnedAgentIds, notifications, …）
└─ （*-secrets.json・cookie・gateway などの資格情報系ファイルは開いていない）
/cursor/stores/<storeId>   FUSE "fuse.agent-store"（初めてアクセスしたときに mount）
```

**メモリのファイルは box にあるか → 現在の実体は box の外にある。** [box verified]
- `agents/*/memory` と `user-memory` のファイル（.md と .txt）の mtime は 2026-10-18 07:57〜08:09 に集中している。例外は、自分で shell から書いた .txt が 10-20 と 10-27 に更新されているだけ。（`find … -printf '%T…'`）
- .md の事実行で最も新しい日付は `2026-10-04`。（`rg -o '^- \((20…)\)'`）
- RecallMemory は 10-10 の `[profile]`、10-19 の `[journal]`、10-21 の `[shared_journal]` を返したが、同じ文字列は box のどこにもない。（`rg -l "PR #720" …` は0件）
- `store.db` の transcript で最も新しいエントリは 2026-09-17。prompt スナップショットのパスも旧名の `/home/box/sand-data/...`。
- `search-index.db` だけは今日も更新されている（23:37）。中身はメッセージの検索 index で、メモリではない。

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 9. [推測]（原典で読んでいないもの）

- 推測1: box の `memory/*.md` は 2026-10-18 の box 再作成（`/home` の mtime は 10-18 00:06）で復元された旧データで、今のメモリはサーバー側に保存され、prompt に挿入され、RecallMemory で検索されている。根拠は §8 の mtime と内容の差だけ。
- 推測2: UpdateMemory が旧 `update_state target "memory"` の後継かどうかは、まだ推測である。
- 推測3: project memory（OWN → project → user）は旧 snapshot にあるだけで、現行も使えるかは不明（`agent-data/projects` は存在しない）。
- 推測4: `managed-skills` は box 上では `-rw-r--r-- box` で書ける。それでも「Cursor 管理の skill は読み取り専用」とされるのは、server の cache（`fetchedAt`）から上書きで同期されるためと思われる。ファイルの権限で守られているわけではない。
- 推測5: `agent-data/memory/` と `memory-log/` にある *.txt は、Bot が shell で書いたメモでメモリ本体ではない（仕組みの文書は見つからなかった）。

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## 10. 実用 Tips（根拠があるものだけ）

1. 長く守らせたいルールは「From now on, …」と伝えて、覚えるよう頼む。一回限りの作業指示は普通に書く。[1° official] bots#edit-a-bot
2. 確実に残したい事実は「Remember that …」とはっきり頼む（自動保存は返信に出ないことがある）。[1° official]
3. shared の事実が古くなっていたら、どの Bot に正しい内容を伝えてもよい。完全に消したいときは、保存した Bot に Forget を頼む。[1° official]
4. Bot を消すとその Bot が書いた shared の事実も消える。役目を終えた Bot は Delete より Hide from sidebar にする。[1° official]
5. Duplicate（iPhone）では learned memory はコピーされない。新しい Bot には役割を伝え直す。[1° official] bots#organize-your-roster
6. 住所・電話・カード・ログインは Vault に入れ、使い分けは Vault の Hints に書く。メモリには入れない。[1° official] vault / v0.77.0
7. 大事な判断の前は、メモリではなく今の情報源を開き直させる。安全のための境界は Auto-review の Ask first ルールで守る。[1° official] bots#memory-is-not-a-source-of-truth、faq
8. Bot は古い事実を `RecallMemory`（`within` で種類を絞れる）で探す。box の `memory/*.md` を grep しても古いスナップショットしか見えない。[box verified]

---

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未
## Sources

- https://x.ai/changelog/bot （v0.77.0 2026-10-26、v0.75.2 2026-10-22、2026-09-26、2026-09-25）
- https://docs.x.ai/grok-bot
- https://docs.x.ai/grok-bot/bots （#what-a-bot-remembers、#edit-a-bot、#delete-a-bot、#organize-your-roster）
- https://docs.x.ai/grok-bot/settings-and-notifications （#import）
- https://docs.x.ai/grok-bot/vault
- https://docs.x.ai/grok-bot/skills-routines-and-automations
- https://docs.x.ai/grok-bot/shared-bots
- https://docs.x.ai/grok-bot/faq
- https://x.com/bot/status/2113466424828047471 （@bot の reply。情報源を先に確認する例）
- box verified: RecallMemory の schema と出力、`/home/box/agent-data/**`（ls/stat/jq keys、sqlite は `mode=ro` で schema と key だけ）、`mount`、`/home/box/reference/app-ui.md`

- 出典: [changelog](https://x.ai/changelog/bot) · [bots](https://docs.x.ai/grok-bot/bots)
- 確認: 未

## 同時の memory 保存（v0.78.1）

- 内容: 2つの memory 保存が同時でも、互いを上書きしない。
- 出典: [changelog v0.78.1](https://x.ai/changelog/bot)（2026-10-27）
- 確認: 未

## changelog v1.2.3 の memory の分け方

- 内容: memory は、people/orgs、profile、standing instructions、projects で別々に保たれる。
- 出典: [changelog v1.2.3](https://x.ai/changelog/bot)（2026-11-18）
- 確認: 未

## Agent memory の dreaming

- 内容: 暇な時間に session transcript を見直して、永続する agent memory を組み直す。transcript と照らして古い note を直し、つながった表現を作り、小さい最上位の層をあとの session へ上げる。ここでの使い方は、session のあと既存の reflect skill で note を transcript と照合し、古いものを直す。常時読む最上位の層は小さく保つ。数字は Anthropic の内部 eval だけ。Dreams API は research preview。GA も価格も、独立した検証も無い。
- 出典: [x.com/AnthropicAI/status/2118814753154064501](https://x.com/AnthropicAI/status/2118814753154064501) · [components of agent memory](https://www.anthropic.com/research/components-of-agent-memory) · [Discord](https://discord.com/channels/1372518933713911858/1374242195778834505/1568828295644979200)（2026-11-07）
- 確認: 未
