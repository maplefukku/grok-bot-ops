# Grok Bot の Skill ノウハウ v2（Grok Bot だけ）

調査日: 2026-10-29 0時台（JST）。v1（`grok-bot-skills.md`）はそのまま残しています。
この v2 では、Cursor IDE や Cursor エージェントの skill の仕組み、つまり cursor/plugins の README、PR #702 と #300、pstack の authoring playbook、`globs` などの Cursor の決まりごとは、出典として使っていません。v1 でそれらだけを根拠にしていた主張も、すべて外しました。

ラベル:
- **[1° official]**: x.ai/changelog/bot、docs.x.ai/grok-bot、@bot の投稿
- **[Grok Bot built-in]**: Grok Bot に入っている Cursor 管理の skill。Skill tool で読み込んだもの
- **[box verified]**: この Bot のコンピューターで読み取り専用で確かめたもの
- **[community]**: Grok Bot の skill について書いた X のコミュニティ投稿
- **[未確認]**: 一次情報で裏が取れなかったもの

---

## 1. Grok Bot の skill とは

**定義**
- skill は、作業のやり方をまとめた、何度でも使える指示です。手順、判断ルール、出力の形、安全の境界をまとめておきます。[1° official] https://docs.x.ai/grok-bot/skills-routines-and-automations
- **自分の private skill は、自分のすべての Bot で共有される1つのライブラリです。** ある Bot が見つけられないときは、Connect apps を開き、接続数を押して、Private skills からその Bot で有効にします。[1° official] 同上
- 使うにはアプリやログインが必要な skill もあります。[1° official] 同上

### 種類ごとの、読み込み・編集・削除

**① Cursor 管理（組み込み）の skill**
- 例: `skill-authoring`、`routines`、`learn-from-demonstration`、`site-playbooks-*`。
- **読み込み:** Skill tool で読みます。[box verified] このセッション
- **編集・削除:** UpdateSkill の対象は「user-created skills」だけです [Grok Bot built-in] `skill-authoring`。なので組み込み skill は、Bot からは編集も削除もできません [Grok Bot built-in]。
- **ファイルの場所:** 指示には「ファイルとしては box にない」とありましたが、実際はキャッシュのコピーが box にあります。`/home/box/agent-data/managed-skills/skills/<id>/SKILL.md`（56件）と `managed-skills/cache.json`（`{id,name,description,body}`、取得は 10/28 12:13 JST）です。[box verified]
- 2026-09-25 に、人気の旅行・食事・買い物・配送サイト向けの組み込みガイドが追加されました（box では `site-playbooks-*` がこれに当たります）。[1° official] https://x.ai/changelog/bot

**② plugin の skill**
- **入れ方・外し方:** Connect apps で plugin を入れたり外したりして管理します。**読み取り専用**で、ファイルは編集しません。[Grok Bot built-in] `skill-authoring`（box のコピーに「their file paths appear in the agent_skills catalog… treat them as READ-ONLY」とあります）
- **使えるようになるタイミング:** 情報が2つあります。
  - 作業中に plugin を入れたら、その skill はすぐ使えます。[1° official] changelog v0.75.8（2026-10-24）
  - 新しく入れた tool と skill は、次のメッセージから使えます。[Grok Bot built-in] `add-connector`
  - 新しい changelog を優先すると、v0.75.8 からは「すぐ」になっています。
- **上限:** 1つの Bot が使える plugin の skill は 24 から 200 に増えました。[1° official] changelog v0.71.2（2026-10-14）
- **box 上の場所:** `/home/box/agent-data/plugin-skills/cache.json` に 58件あります（キーは `id, pluginId, pluginName, name, description, filePath, skillRelativePath …`）。[box verified]

**③ ユーザーが作った skill**
- **場所:** `/home/box/agent-data/workflows/<slug>/SKILL.md` で、65件あります。[box verified]
- **作成・書き換え:** `UpdateSkill` の action `"write"` で作ります。既存の id を渡すと書き換えになります。[Grok Bot built-in] `skill-authoring`
- **削除:** action `"delete"` で消します。**削除はすべての assistant に効く**ので、先にユーザーに確認します。[Grok Bot built-in] 同上
- **チャットから:** 「Save the process we just used as a skill called …」と頼んでも作れます。[1° official] docs
- **デモから:** Teach a task でデモを録画すると、`learn-from-demonstration` が UpdateSkill で下書きの skill を作ります。[1° official] docs / [Grok Bot built-in] `learn-from-demonstration`

**④ チームの skill と template の skill**
- **チームへの公開:** Connect apps を開き、接続数を押して skill を選び、**Publish** します。description がないと公開できません。公開後は **Sync** で編集を反映し、**Unpublish** で取り下げます。アプリ付属の skill や template 由来の skill は公開できません。[1° official] docs「Share a skill with your team」
- **template から入った skill:** Private skills に「From template」と表示されます。[1° official] changelog v0.77.0（2026-10-26）
- **template の書き出し:** `CreateBotShareJson` に、残す skill（個人の情報は抜く）と getting-started skill を入れます。[Grok Bot built-in] `export-bot-template`
- **公開リンクで見えるもの:** template の公開リンクからは skill と routine の中身が見えます。API キーや社内 URL は入れません。[1° official] https://docs.x.ai/grok-bot/bots
- **Team Bot の skill:** owner と Manager が編集します。[1° official] changelog 2026-09-26 / 09-30
- **共有している Bot の skill:** owner が入れた skill は、メンバー全員のチャットで動きます。[1° official] https://docs.x.ai/grok-bot/approvals-security-and-privacy

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 2. Bot が skill を使うと決めるまで

- **カタログ:** Bot に見えるのは id（フォルダ名）と、いつ使うかを書いた説明です。長い説明は短く切られ、「…[truncated]」となるものや省略されるものもあります。このセッションのカタログには「Some descriptions above are shortened or left out」と出ています。[box verified]
- **description:** skill を使うか決めるときに読まれるのは description だけです。なので「いつ使うか」を書きます。[Grok Bot built-in] `skill-authoring`
- **読み込み:** Skill tool で名前を指定すると、SKILL.md の本文、フォルダの場所、helper file の名前が返ります。相対パスはそのフォルダを起点に解決されます。[Grok Bot built-in] Skill tool の説明
- **ユーザーからの呼び出し:**
  - docs と chat の説明では「**名前で頼む**」で、`@` は Bot、グループ、routine、アプリ用です。[1° official] https://docs.x.ai/grok-bot/chat-and-collaboration
  - changelog 2026-10-07 には「Typing / … no longer opens a menu of skills」とあります。[1° official]
  - `skill-authoring` の「/ or @ で呼べる」は古い書き方です。新しい情報を優先して、今は**名前で頼む**のが確実です。[Grok Bot built-in]
- **routine の中の @メンション:** 「Run @Daily standup, then …」のように書くと、実行のときに読まれる参照になります。コピーにはなりません。[Grok Bot built-in] `skill-authoring`
- **会話の要約のあと:** カタログは更新される。[Grok Bot built-in]
- **入れたばかりでカタログにまだ無い skill:** 次のターンから、Skill tool で名前を指定すれば読める。[Grok Bot built-in]
- **速さ:** memory や skill が多い Bot でも、返事が数秒止まることはなくなりました。[1° official] changelog 2026-09-25

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 3. routine・memory・Vault・Bot の profile との関係

| 役割 | 置く場所 | 根拠 |
|---|---|---|
| **どうやるか** | skill | [1° official] docs / FAQ https://docs.x.ai/grok-bot/faq |
| **いつ、どの Bot が** | routine。`agents/<id>/automations/<slug>/automation.json` と `runs.json` | [1° official] docs / [box verified] |
| 好み、守るルール、自分についての事実、作業の日誌 | memory。Bot ごとに `agents/<id>/memory/profile.md` と `memory/log/`（日誌） | [1° official] docs「What a Bot remembers」/ [box verified] |
| 全 Bot で共有する、自分についての事実 | 共有の memory。名前とタイムゾーンなど。box では `user-memory/by-agent/<id>/profile.md` と `log/` | [1° official] docs / [box verified] |
| ログイン情報、カード、連絡先 | **Vault**（skill にも memory にも書かない） | [1° official] https://docs.x.ai/grok-bot/vault 、docs の memory 節 |
| Bot の名前、説明、ラベル | Bot の profile。`agents/<id>/profile.json`（キーは `name, description, title, …`） | [box verified] / [1° official] docs（About） |
| 安全の境界 | 承認と Auto-review のルール（memory だけに頼らない） | [1° official] docs |

- **個別の情報は routine に書く:** どのチャンネル、どの repo、誰のカレンダーかは、skill ではなく、その skill を動かす routine に書きます。skill 本体には汎用的な手順だけを書きます。[Grok Bot built-in] `skill-authoring`
- **template の説明は短く:** 数文までにして、詳しい内容は skill や memory に入れます。[Grok Bot built-in] `export-bot-template`
- **skill は Bot ごとではない:** skill は Bot ごとのフォルダ（`agents/<id>/`）には入っておらず、`workflows/` に1つだけあります。全 Bot 共通のライブラリという点と合っています。[box verified]
- **Bot を Duplicate したとき:** 有効にした skill はコピーされますが、memory はコピーされません。[1° official] docs（Organize your roster、iPhone）

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 4. いつ skill にするか、どう書くか

**いつ作るか**
- まず1回、手作業で確実にこなしてから skill にし、そのあとで routine にします。[1° official] docs「Start with a one-time task…」
- 繰り返し使えて、何をするかがはっきりした複数ステップの作業なら、**自分の判断で保存して、あとから伝えます**。保存する価値があるか迷うときだけ先に聞きます。[Grok Bot built-in] `skill-authoring`

**書く内容**
- 書く項目は6つ: ①いつ使うか ②必要な入力とアクセス ③手順 ④結果の確かめ方 ⑤何を返すか ⑥何に承認が要るか。[1° official] docs「Save a skill」
- 形式は YAML の frontmatter（`name`、`description` は必須）と markdown の本文です。[Grok Bot built-in] `skill-authoring`
- 本文は**汎用的な手順**にします。入力は `{item}` のように差し替えられる形にし、URL やラベルのような変わりにくい目印を使い、送信・支払い・注文の前には確認を入れます。パスワードなどの秘密は書きません。[Grok Bot built-in] `learn-from-demonstration` §5
- name は短い命令形にし、description は「いつ使うか」を1行で書きます。[Grok Bot built-in] 同上
- デモから作った skill は下書きです。判断ルール、失敗したときの扱い、承認の境界を書き足して、安全な入力で試してから routine にします。[1° official] docs

**pill（チャットに出るリンク）**
- 返信の中で `[name](sand-workflow:<id>)` と書くと（id はフォルダ名）、押すと Settings でその skill が開く pill として表示されます。[Grok Bot built-in] `skill-authoring`
- box の skill 同士も、この形で互いにリンクしています（切れているリンクは0件）。[box verified]

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 5. たくさんの Bot で使うときの設計と、この box の skill ライブラリ

**box の全体像** [box verified]
- user skill は 65件。frontmatter のキーはすべて `name` と `description` だけで、helper file はありません。
- 組み込みは 56件、plugin は 58件です。

**流れ用の skill ＋ ステップ用の skill という形**（実例）[box verified]
- `x-2`（X 運用のまとめ役）が、`workflow-1786732503642`、`…2846561`、`…3281380`、`…3964155`、`1`、`tip-memory-bake` などを `sand-workflow:` で呼んでいます。
- ただし、`workflow-1786732503642` が逆に `x-2` と `x` を参照していて、**参照がぐるっと一周しています**。

**良い例** [box verified]
- 説明が「Use when …」で始まり、いつ使うかが最初に書いてある: `completion-handoff`, `onion-check`, `test-audit`
- 短くて1つの仕事だけをする: `tip-memory-bake`（26行）, `grok-bot-ops-ledger-write`（20行）, `48h`（31行）
- 古い id を残すときに、本文を移さず、転送用の短い skill にしている: `sim-teardown` は description に「Pointer to mini-sim-teardown」とあり、19行だけ
- よく参照されていて、手順を書き写さずに参照で済ませている: `cloud`（29回参照）, `tool-path-prefer`（28回）

**避けたい例** [box verified]
- **id から中身がわからない:** `1`, `x-2`, `pr-2`, `workflow-<数字>`（8件）, `skill-1787982731378`。いずれも name は日本語の表示名です（name と id が一致するのは 39/65 件）。
- **説明が長すぎる:** `cloud` が 1,311文字、`tool-path-prefer` が 1,140、`workflow-1786732503642` が 728、`conductor-keep-moving` が 626。カタログでは途中で切られます。
- **社内の略語が多い:** 24件の説明に `HARD` や `SoftACC` などが入っています。
- **特定の人や Bot に依存している:** 11件の本文にユーザー名、4件に agent の UUID が入っていて、`skill-authoring` の「汎用的に書く」に反します。
- **重なっていそうなもの:** `pr`/`pr-2`、`x`/`x-2`/`workflow-*`、`chatgpt`/`chatgpt-web-existing-tab`、`ui`/`ui-library-invoke`、`seat-memory-watch`/`shared-memory-watch`/`tip-memory-bake`、user の `author-shared-skill` と組み込みの `skill-authoring`。
- **skill 以外のデータが `workflows/` にある:** `workflows/character-design/` には SKILL.md がなく、`skill-1787982731378` がそこのファイルを参照しています。
- **書きかけのファイルが残っている:** `workflows/cloud/` と `workflows/tool-path-prefer/` に `SKILL.md.7.*.tmp` があります。

**コミュニティの実例** [community]
- 自作の skill を取り込んでも、リモートのリポジトリの更新には自動で追いつきませんでした。routine で Bot 自身に skill を取ってこさせ、ユーザーの skill として設定するのが確実だったそうです: https://x.com/_inady_/status/2109152901474254898
- 持ち主の違う Bot 同士が、同じ skill（SKILL.md）と webhook でやり取りできたという例: https://x.com/notf/status/2109226839684378810
- アプリ、スキル、テンプレートの違いを整理した投稿: https://x.com/yamamoto_wb/status/2114177271443669105
- @bot の返信では、X の投稿を「再利用できる skill にして」と頼むと、自分の Bot に渡されます [1° official]: https://x.com/bot/status/2114593254742122785 。skill を一時的に無効にしてほしいという依頼もあります: https://x.com/bot/status/2115085068444053799

**設計の提案** [未確認: 公式に書かれた決まりではなく、上の事実から考えた提案です]
1. 流れ用の skill を1つにして、ステップ用の skill はその下に置きます。ステップ用の skill から流れ用の skill へは参照を戻さず（一周させない）、routine は流れ用の skill だけを @メンションします。
2. id は英小文字のハイフンつなぎで、何をするかがわかる名前にします。日本語の name だと `workflow-<数字>` のような id になるように見えますが、これは [未確認] です。
3. description は最初の1文に「いつ使うか」を書き、およそ200文字までにします（カタログで切られる位置は [未確認]）。略語は使いません。
4. 重なっている skill は1つにまとめ、古い id は転送用の短い skill（`sim-teardown` のような形）として残します。
5. 個別の情報（Bot の ID、人の名前、チャンネル）は routine か memory に移し、skill は汎用的なままにします。

---

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 未確認の一覧
- 日本語の name から `workflow-<数字>` の id ができる仕組み
- カタログで説明が切られる文字数
- `.tmp` ファイルが動作に影響するか
- 5章の「設計の提案」1〜5（公式の決まりではありません）
- 補足: box 上の `skill-authoring` のコピーは、Skill tool で読み込んだ本文より1文多くなっています（plugin の skill は実ファイルで、カタログにパスが出るという文）。どちらが最新かは [未確認] です。

- 出典: [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [changelog](https://x.ai/changelog/bot)
- 確認: 未
## 出典
- https://x.ai/changelog/bot （v0.77.0 2026-10-26 / v0.75.8 2026-10-24 / v0.71.2 2026-10-14 / 2026-10-07 / 2026-09-30 / 2026-09-26 / 2026-09-25）
- https://docs.x.ai/grok-bot/skills-routines-and-automations
- https://docs.x.ai/grok-bot/bots
- https://docs.x.ai/grok-bot/faq
- https://docs.x.ai/grok-bot/chat-and-collaboration
- https://docs.x.ai/grok-bot/settings-and-notifications
- https://docs.x.ai/grok-bot/approvals-security-and-privacy
- https://docs.x.ai/grok-bot/vault
- @bot: https://x.com/bot/status/2114593254742122785 , https://x.com/bot/status/2115085068444053799
- [community]: https://x.com/_inady_/status/2109152901474254898 , https://x.com/notf/status/2109226839684378810 , https://x.com/yamamoto_wb/status/2114177271443669105
- [Grok Bot built-in]: `skill-authoring`, `learn-from-demonstration`, `export-bot-template`, `add-connector`（Skill tool と `/home/box/agent-data/managed-skills/skills/`）、Skill tool の説明
- [box verified]: `/home/box/agent-data/workflows/`, `managed-skills/`, `plugin-skills/cache.json`, `agents/<id>/{memory,automations,profile.json}`, `user-memory/by-agent/`

- 確認: 未
