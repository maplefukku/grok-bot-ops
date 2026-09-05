# 0003. ドメイン単位で出荷量を管理する

- ステータス: Accepted
- 日付: 2026-09-05
- Issue: [#16](https://github.com/maplefukku/grok-bot-ops/issues/16)
- LOCK: [PdM HARD CORRECT](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543589865)

## 文脈

中央 CI は tiny PR の列を直列にする。leftover の山と ADV の ping-pong が詰まりである。[PdM HARD CORRECT](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543589865) は [LOCK-READY](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543582190) のサイズ規則を上書きする。境界と Done の品質は残す。契約 SoT は ARCH issue 3 本のままである。

[0002](./0002-trend-adopt-loop.md) は手順を ADR の外に置いた。この ADR も手順を外に置く。

## 決定

1. A から D の手順の正本は [`docs/process/README.md`](../process/README.md) である。C の席ゲートはこの ADR にある。書き込み箱は [`AGENTS.md`](../../AGENTS.md) である。
2. 出荷単位は機能 1 個、または domain 1 個であり、main への 1 merge である。tiny-slice packing は採らない。
3. 契約 SoT は gakuse-ai#2063、sauna-master#197、ZuruNote#242 の 3 つだけである。第 4 を作らない。パスは process pack の表である。
4. 席は提案のみである。提案は ADV closer と lane scheduler である。product CoS は既定 NO である。scheduler log が 2 週間で PdM をボトルネックと出したときだけ立てる。
5. CreateAgent は CBO である。この ADR の Accepted は CreateAgent 承認ではない。新しい bot ファイルは作らない。PdM はクローンしない。監視、開発リーダー、編成評価は維持する。issue の「dr eggbot」は CBO 経由であり、席を増やさない。
6. [`docs/knowhow/fleet.md`](../knowhow/fleet.md) は日付付きの観察である。食い違いは [`docs/process/README.md`](../process/README.md) が勝つ。
7. [`bots/README.md`](../../bots/README.md) は LOCK ポインタだけである。規則を複製しない。
8. glob-lock の live 表はこのリポジトリに置かない。

## 結果

- leftover と ADV ping-pong は unit の内側で切る。
- 中央 CI は unit 1 本につき 1 回払う。
- MUST は終端する。NIT は 1 回で終わる。
- 席は増えない。CreateAgent は動かない。
- 手順と観察が食い違うとき、読む先は process pack である。

## 却下した案

- tiny-slice の 1 PR = 1 細い slice。中央 CI が列を直列にする。
- ADR に A から D の手順を全文載せる。手順は pack に置く。理由はこの ADR である。
- `bots/README.md` に規則を全文載せる。台帳は誰の席かを持つ。
- `docs/process` を 4 ファイルに割る。呼び手は 1 ファイルで足りる。
- 第 4 の契約 SoT。ARCH issue 3 本で足りる。
- 新しい impl ボット、PdM のクローン、今すぐの CreateAgent。
- live な glob-locks.md。導出で足りる。
- `docs/knowhow/fleet.md` を正本にする。knowhow は日付付きの観察である。
