---
url: https://github.com/NousResearch/hermes-agent
keywords: AI-agent, self-improving, multi-platform, tool-calling, NousResearch
oneliner: Nous Research が開発する、スキル自己学習機能付きのマルチプラットフォーム AI エージェントフレームワーク。
---

## Hermes Agent — 概要整理

### 1. これは何？

Nous Research が開発する**自己改善型の AI エージェントフレームワーク**。LLM にツール呼び出しループ（エージェントループ）を組み合わせ、ターミナル操作・ファイル編集・Web 検索・ブラウザ操作・コード実行など **40 種以上のツール**を自律的に使い分けて複雑なタスクを遂行する。最大の特徴は「**使うほど賢くなる学習ループ**」を内蔵している点で、タスク実行中に得たノウハウを "スキル" として保存・再利用・改善し続ける。

対応 LLM は OpenRouter 経由の 200+ モデルのほか、Anthropic / OpenAI / Gemini / ローカル（Ollama, vLLM 等）を切り替え可能。

---

### 2. 何が嬉しいのか？（既存ツールとの比較）

| 観点 | Hermes Agent | Claude Code / Cursor 等 | AutoGPT / CrewAI 等 |
|---|---|---|---|
| **自己学習** | ✅ スキルを自動生成・蓄積し次回以降に再利用 | ❌ セッション単位で忘れる | △ メモリはあるが体系的な学習ループなし |
| **マルチプラットフォーム** | ✅ CLI＋Telegram / Discord / Slack / WhatsApp / Signal 等 **18 種のメッセージング基盤** に単一インスタンスで接続 | ❌ エディタ/CLI のみ | △ API サーバは立てられるが統合 Gateway なし |
| **LLM 非依存** | ✅ 任意のプロバイダ・モデルをホットスワップ | ❌ 特定ベンダにロック | △ 対応範囲は限定的 |
| **実行環境の柔軟性** | ✅ ローカル / Docker / SSH / Modal（サーバレス）/ Daytona をバックエンドに選択可能 | ❌ ローカルのみ | △ Docker 対応程度 |
| **MCP 連携** | ✅ MCP サーバを任意追加 | ✅ | △ |
| **RL / 研究用途** | ✅ 軌跡保存・バッチ生成・Atropos 連携で強化学習に直結 | ❌ | ❌ |
| **スケジューラ** | ✅ cron 内蔵で無人定期実行 | ❌ | △ |

**一言で言うと：** 「コーディング支援」に閉じず、**メッセージングボット・定期ジョブ・研究用データ収集**まで一貫して扱え、さらにスキル学習で使い込むほど効率が上がる点が差別化ポイント。

---

### 3. 使うときの流れ

```
① セットアップ
   $ pip install hermes-agent   # または git clone → pip install -e .
   $ hermes setup               # 対話ウィザードで API キー・モデル・ターミナル設定

② 対話的に使う（CLI）
   $ hermes                     # TUI 起動 → 自然言語で指示
   $ hermes -q "○○を調べて"      # ワンショット実行

③ メッセージング Gateway として使う
   $ hermes gateway             # Telegram / Discord 等にボットとして常駐

④ スキルの活用・拡張
   /skills                      # スキルハブを閲覧・インストール
   （複雑タスクを実行すると自動的にスキル化される）

⑤ 定期実行
   $ hermes cron                # cron ジョブを登録し無人運用

⑥ プログラムから呼ぶ
   from run_agent import AIAgent
   agent = AIAgent(model="...", enabled_toolsets=["web","code"])
   result = agent.run_conversation("タスク内容")
```

**設定ファイルは `~/.hermes/` 以下**に集約される（`config.yaml` で設定、`.env` で API キー管理、`state.db` でセッション永続化）。プロファイル機能でマルチテナント運用も可能。
