---
url: https://github.com/cline/cline
keywords: VS Code拡張, AIコーディングエージェント, MCP, ターミナル操作, ブラウザ操作
oneliner: ファイル編集・コマンド実行・ブラウザ操作までこなす、IDE内で動く人間承認付きの自律型AIコーディングエージェント。
---

# cline/cline まとめ

## このリポジトリは何？
**Cline** は VS Code（と CLI / JetBrains 系）用の **自律型 AI コーディングエージェント** を提供する OSS プロジェクト。ユーザーがタスクを自然言語で投げると、Claude Sonnet などの LLM が以下のツールを駆使して段階的に実行する：

- **ファイルの作成・編集**（差分ビュー付き、Linter/コンパイラのエラーも監視して自己修正）
- **ターミナルコマンド実行**（VS Code v1.93 の shell integration API を活用、dev サーバのログも追尾）
- **ヘッドレスブラウザ操作**（クリック／タイプ／スクショ＋コンソールログ取得）
- **MCP (Model Context Protocol) 連携**：独自ツールを生やし、Jira / AWS / PagerDuty などへ拡張可能
- **チェックポイント機能**：作業の各ステップでワークスペースのスナップショットを取り、Compare / Restore 可能

中身は TypeScript 主体で、`src/`（拡張本体）、`webview-ui/`（React の UI）、`cli/`（Ink ベースの TUI）、`proto/`（gRPC 風の内部通信スキーマ）、`standalone/` などから構成される大規模モノレポ。バージョン 3.80.0、Apache-2.0。

## このリポジトリは何が嬉しいの？（既存手段との比較）
| 比較対象 | Cline の立ち位置 |
| --- | --- |
| **GitHub Copilot / Cursor の補完** | 補完や単発チャットでなく、「調査→編集→実行→修正」までをループで回す**エージェント型**。タスクを投げっぱなしできる。 |
| **Devin / Auto-GPT 系の全自律エージェント** | サンドボックス丸投げではなく、**各ファイル変更・各コマンド実行にユーザ承認を挟む human-in-the-loop**。安全かつ途中介入しやすい。 |
| **ChatGPT の Code Interpreter** | ローカルの自分のリポジトリ／ターミナル／ブラウザに直接作用できる。AST 探索・regex 検索・Linter 監視で**大規模既存プロジェクトにも強い**。 |
| **特定 LLM ベンダ依存のツール** | OpenRouter / Anthropic / OpenAI / Gemini / Bedrock / Vertex / Cerebras / Groq / Ollama / LM Studio など**モデル自由**。企業向けに SSO・VPC・セルフホストも提供。 |
| **一般的な MCP クライアント** | 「こういうツールを追加して」と頼むと、**MCP サーバ自体を生成・インストール**してくれる。 |

さらに、**トークン数と API コストを都度表示**、`@url` `@file` `@folder` `@problems` などのコンテキスト挿入ショートカット、Timeline と連動した変更履歴 UI など、実務向けの細部が作り込まれているのも特徴。

## 使うときの流れ
1. **インストール**：VS Code Marketplace から "Cline" を入れる（社内 CLI 派は `cli/` の TUI を利用）。
2. **モデル／API キー設定**：使いたいプロバイダ（Anthropic / OpenRouter / Bedrock / ローカル Ollama 等）を選びキーを登録。必要ならプロキシは `@/shared/net` 経由で自動対応。
3. **タスクを投入**：チャット欄に自然言語で指示（画像貼り付けでモックアップ→実装も可）。必要に応じ `@file` `@folder` `@problems` `@url` で文脈を渡す。
4. **Cline が調査**：ファイル構造と AST を読み、関連ファイルを検索・参照して計画を立てる。
5. **ステップ実行＋都度承認**：
   - ファイル編集は**差分ビュー**で確認 → Approve／編集／Reject
   - コマンド実行は**ターミナルに提示** → 承認すると実行、長時間プロセスは "Proceed While Running" でバックグラウンド化
   - 必要ならブラウザを起動して E2E 的に動作確認
6. **エラーがあれば自己修正ループ**：Linter／コンパイル／実行ログを Cline 自身が読み取り、自動で直しに行く。
7. **チェックポイントで安全網**：気に入らない結果はワークスペース単位／タスク単位で Restore。気に入れば続行。
8. **完了**：最終コマンド（例：`open index.html`）がワンクリックで叩ける状態で提示され、タスク終了。必要なら "add a tool that…" と頼んで MCP ツールを増やし、次のタスクに備える。
