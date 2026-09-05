# shopping

買い物・決済と、承認の置き方。

## 購入は承認の後ろに置く

- 内容: 公式は送信、購入、金銭の移動、削除、公開、本番変更を承認の後ろに置くよう案内している。支払い確認はコンピュータのテイクオーバー（パスワードや 2FA と同じ扱い）。承認は提案中の操作を止めるだけで、すでに完了した作業は戻さない。
- 出典: [Approvals, security, and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)（2026-08-29 確認）
- 確認: 未

## Link で買い物する

- 内容: @link を接続し Bot に買い物を頼む。支出は毎回ユーザーが承認する。決済ごとにセキュアな使い捨てカードが発行される。現時点は US 向け。モバイル展開は近日。
- 出典: [x.com/bot/status/2093419921007108385](https://x.com/bot/status/2093419921007108385)（2026-08-28）、[x.com/bot/status/2093419922470961421](https://x.com/bot/status/2093419922470961421)
- 確認: 未

## 運用ルール（このリポジトリの採用ルール）

- 内容: 決済権限は本物のカードに直結させない。承認なしの自動購入は設定しない。
- 出典: 上項の公式境界を、この司令室の規約にしたもの。[Approvals, security, and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- 確認: 済（このリポジトリの規約）
