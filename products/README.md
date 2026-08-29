# products/

工場が出荷するプロダクトの台帳です。coordinator（人間またはメインボット）は、ここを見てどのリポジトリに cloud agent を立てるか決めます。

1 プロダクト 1 ファイル。[`_template.md`](./_template.md) から作ってください。

## 台帳が答えるべき質問

- そのプロダクトのリポジトリはどこか
- 検証スキルは立っているか（`.cursor/skills/verify-<app>/`）。無ければ工場の信頼が無い
- feature map はどこか
- maintain-verification の routine は付いているか
- benny などの automation パックは入っているか
- 最後に検証スキルを確認した日と、その outcome（`clean` / `changed` / `blocked`）と PR リンク

## 台帳の書き戻し

[`routines/maintain-verification.md`](../routines/maintain-verification.md) が、各プロダクトの `/maintain-verification-skill` のあとでこのディレクトリだけを更新する。

| 欄 | 誰が書く | 値 |
|---|---|---|
| 最終確認日 | maintain の書き戻し | UTC の `YYYY-MM-DD`。未実施は `未` |
| 最終 outcome | 同上 | `clean` / `changed` / `blocked`。未実施は `未` |
| 最終 PR | 同上 | `changed` ならプロダクト側 PR の URL。それ以外は `無し` |

検証スキル本体はプロダクトリポジトリに置く。ここへコピーしない。

## 原則

- 検証スキル・feature map・automation パックの **本体はプロダクトリポジトリに置く**。ここに置くのはポインタと状態だけ。ここへ本体を集約すると、cloud agent のチェックアウトから見えなくなり、検証がインフラからドキュメントに退化する。
- 新しいプロダクトを登録したら、最初の仕事は検証スキルの bootstrap（[`automations/verification-bootstrap/`](../automations/verification-bootstrap/FOR_AGENTS.md)）。
