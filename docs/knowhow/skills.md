# skills

Grok Bot の skill（再利用できる手順の単位）の作り方と使い方。Teach a task の手順は [`routines.md`](./routines.md) にある。

## GitHub Security Lab の Fuzzing Taskflow

- 内容: C/C++ の GitHub repository を指すと、entrypoint の特定、build の解析、harness の作成、AFL++ の実行、coverage の読み取り、crash の triage、unique bug ごとの vulnerability report までを agent が進める、と GitHub Blog と @github。実行は [seclab-taskflows-fuzzing](https://github.com/GitHubSecurityLab/seclab-taskflows-fuzzing) の codespace で `./scripts/fuzzing/run_fuzzing.sh PROJECT`。引数は `owner/repo`。記事は、`afl-fuzz` と `clang` と、LLM が選んだ build コマンドを、container を挟まず host 上で実行するので、使い捨て環境（Codespace か捨てられる VM）で、昇格した権限なしに走らせる、と書く。既定モデルは Claude Sonnet 5。別モデルは `src/seclab_taskflows_fuzzing/configs/model_config.yaml`。
- 出典: [AI-powered fuzzing with the GitHub Security Lab Taskflow Agent](https://github.blog/security/application-security/ai-powered-fuzzing-with-the-github-security-lab-taskflow-agent/)（2026-09-24） · [repo](https://github.com/GitHubSecurityLab/seclab-taskflows-fuzzing) · [x.com/github/status/2109364666237350135](https://x.com/github/status/2109364666237350135)（2026-10-11）
- 確認: 未

## サポート Bot に billing などリスクの高い系統も繋ぐ

- 内容: 安全なツールだけではサポート自動化は足りない。請求やリスクの高い部分を繋いで、痛みのあるところを Bot が触れるようにする、という助言。
- 出典: [x.com/ChrisSimpson/status/2100002853565665639](https://x.com/ChrisSimpson/status/2100002853565665639)（2026-09-15）
- 確認: 未

## Agent の day-zero 期待（新入社員扱い）

- 内容: Agent は day zero ではあまり上手くない。新入社員と同様に期待値を置く、という product-team ライブストリーム上の助言。
- 出典: [x.com/ChrisSimpson/status/2099989191706780073](https://x.com/ChrisSimpson/status/2099989191706780073)（2026-09-15）
- 確認: 未

## skill は再利用できるワークフローの単位

- 内容: skill は「いつ使うか、手順、判断ルール、期待する出力、境界」を持つ再利用できるレシピ。自分で書く、直す、Teach a task で Bot のコンピュータ上の作業を録画してデモから下書きさせる、のいずれでも作れる。チャットの記憶は 1 会話に閉じるが、skill は自分の全 Bot で共有され、他の Bot が呼べ、routine が指せ、template に指示・skill・routine をまとめて同梱して配れる、という主張。
- 出典: [x.com/brianzhan1/status/2097455378179162132](https://x.com/brianzhan1/status/2097455378179162132)（2026-09-08）
- 確認: 未
