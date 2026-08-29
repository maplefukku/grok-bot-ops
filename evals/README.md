# evals/

スキルとプロンプト変更の盲検評価の記録です。

ルールはひとつ。**評価を通っていないスキル変更は `skills/` に入れない。** スキル編集は将来の全セッションに効くので、実験として扱います。

## やり方

[Eval プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) を使います:

```text
/poteto-mode run the eval playbook on this skill change. same task for both variants, candidates stay blind.
```

観察者効果への対策がプレイブックに組んであります。候補エージェントは「eval」も「candidate」も互いの存在も知らされず、サニタイズしたディレクトリで自然に見える仕事を受けます。ジャッジは中立ラベルで採点します。

## 記録の形式

1 評価 1 ファイル: `evals/<YYYY-MM-DD>-<slug>.md`

- 何を変えたか（変更前後のスキルへのリンク）
- 課題と変種
- ジャッジの評決と、自分で全出力を読んだ結果
- 採用 / 不採用と理由

評決に反対なら、自分の判断より先にルーブリックを疑うこと。
