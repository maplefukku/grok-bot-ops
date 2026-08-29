# 原則の名前で舵を切る

pstack は 21 の原則を個別スキルとして同梱します。`/poteto-mode` は複数ステップのタスクの冒頭でその索引を読み、タスクが引き金にするものを適用し、返事の中で適用した原則と、それが変えた判断を名指します。

原則は呼び出しません。名前で舵を切ります。各名前は、エージェントがすでに読んだ完全な規則を指すので、一文のほうが、段落の指示より正確に仕事を振り向けます。

## 実際の舵取り

エージェントが、既存のアダプタ 3 つに新しいアダプタを継ぎ足そうとしているとき:

```text
use subtract before you add. delete the obsolete adapters first, then design what's left.
```

ビルドが通ったから成功だと主張するとき:

```text
apply prove it works. run the real import flow and show me the written records.
```

並列の試みが同じブランチに書こうとしているとき:

```text
separate before serializing shared state. give each attempt its own worktree, no locks.
```

各句が効くのは、後ろの規則が具体だからです。エージェントは返事の中で、規則がどの判断を変えたかを言わねばなりません。判断の無い原則引用は、適用せずに名前を挙げただけの印です。

## 21 を短く

中核の原則は、どれだけ作るか、いつ設計を考え直すかを決めます:

- [Laziness Protocol](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md) は、削除と、問題を解く最小の変更を好む。
- [Foundational Thinking](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-foundational-thinking/SKILL.md) は、ロジックを書く前に中核のデータ構造を選ぶ。
- [Redesign from First Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-redesign-from-first-principles/SKILL.md) は、新しい要件を、最初からあったかのように統合する。
- [Subtract Before You Add](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-subtract-before-you-add/SKILL.md) は、上に積む前に不要な重荷を取り除く。
- [Minimize Reader Load](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-minimize-reader-load/SKILL.md) は、読者が頭に保持しなければならないレイヤと隠れ状態を畳む。
- [Outcome-Oriented Execution](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-outcome-oriented-execution/SKILL.md) は、捨てる互換状態を残さず、書き換えを目標設計へ収束させる。
- [Experience First](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-experience-first/SKILL.md) は、実装の都合よりユーザーの結果を選ぶ。
- [Exhaust the Design Space](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-exhaust-the-design-space/SKILL.md) は、先例が無いとき競合するプロトタイプを 2〜3 つ作る。
- [Build the Lever](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-build-the-lever/SKILL.md) は、仕事をする、または証明するスクリプトを作り、レビューアが再実行できるようにする。

アーキテクチャの原則は、状態、検証、互換性がどこに置かれるかを決めます:

- [Model the Domain](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md) は、繰り返す規則を散らばった条件分岐ではなく、ひとつの構造にエンコードする。
- [Boundary Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md) は境界で検証し、内部の型を信じる。
- [Type System Discipline](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md) は、違法な状態を表現不能にする。
- [Make Operations Idempotent](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md) は、リトライを同じ終端状態へ収束させる。
- [Migrate Callers Then Delete Legacy APIs](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) は、移行と削除を一波で行う。
- [Separate Before Serializing Shared State](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) は、協調を足す前に共有を取り除く。

検証の原則は、何が証明かを定義します:

- [Prove It Works](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md) はプロキシではなく本物の成果物を検証する。
- [Fix Root Causes](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md) はコードを変える前に再現し、原因まで辿る。
- [Sequence Work into Verifiable Units](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-sequence-verifiable-units/SKILL.md) は、小さい単位の終わりに確認を置き、それから次を始める。

委任の原則は、並列作業を正気に保ちます:

- [Guard the Context Window](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md) は大量の読み取りをサブエージェントに回し、発見はメインチャットに残す。
- [Never Block on the Human](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-never-block-on-the-human/SKILL.md) は可逆な仕事を進め、結果を提示する。

メタ原則がひとつ:

- [Encode Lessons in Structure](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) は、二度繰り返した助言を lint、確認、スクリプトにする。

リストを暗記しないでください。いま眺めて、ここにある名前を出せば防げたはずのことをエージェントがしていると気づいたら、戻ってきてください。語彙はそうやって残ります。

次: [自分のものにする](./09-make-it-yours.md)。
