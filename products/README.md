# products/

工場が出荷するプロダクトの台帳です。coordinator（人間またはメインボット）は、ここを見てどのリポジトリに cloud agent を立てるか決めます。

1 プロダクト 1 ファイル。[`_template.md`](./_template.md) から作ってください。

## 台帳が答えるべき質問

- そのプロダクトのリポジトリはどこか
- 検証スキルは立っているか（`.cursor/skills/verify-<app>/`）。無ければ工場の信頼が無い
- feature map はどこか
- maintain-verification の routine は付いているか
- benny などの automation パックは入っているか

## 原則

- 検証スキル・feature map・automation パックの **本体はプロダクトリポジトリに置く**。ここに置くのはポインタと状態だけ。ここへ本体を集約すると、cloud agent のチェックアウトから見えなくなり、検証がインフラからドキュメントに退化する。
- 新しいプロダクトを登録したら、最初の仕事は検証スキルの bootstrap（[`automations/verification-bootstrap/`](../automations/verification-bootstrap/FOR_AGENTS.md)）。
