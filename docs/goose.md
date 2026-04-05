---
url: https://github.com/block/goose
keywords: AI-agent, MCP, LLM-agnostic, autonomous-coding, Rust
oneliner: 任意のLLMで動作し、MCPベースの拡張機構を持つオープンソースの自律型AIコーディングエージェント
---

## Goose — オープンソース自律型AIエージェント

### これは何？

Block社が開発する **ローカル実行型のAIコーディングエージェント**。コード提案にとどまらず、プロジェクトの雛形生成・コード編集・コマンド実行・テスト・外部API連携までを自律的にこなす。Rust製のバックエンド (`goosed`) に対し、**CLI (`goose`)** と **Electron デスクトップアプリ** の2つのフロントエンドを持つ。Apache 2.0 ライセンス。

コアとなる設計思想は2つ:

1. **LLM非依存** — Claude, GPT-4, Gemini, Ollama等ローカルモデルまで **40以上のプロバイダ** に対応。プロバイダロックインがない。
2. **MCP (Model Context Protocol) ベースの拡張** — Anthropic策定のオープン標準プロトコルでツールを統合。独自プラグイン仕様ではなく、既存のMCPサーバがそのまま使える。

### 既存ツールと比べて何が嬉しい？

| 観点 | GitHub Copilot / Cursor | Claude Code | **Goose** |
|---|---|---|---|
| LLM選択 | 固定〜数種 | Claude固定 | **40+プロバイダ自由選択** |
| 拡張性 | エディタプラグイン依存 | MCP対応 | **MCP標準 + 100超の既存サーバ即利用** |
| 実行モデル | 提案中心 | 自律実行 | **自律実行（auto/approve/smart_approve切替）** |
| コスト最適化 | なし | なし | **要約用に安価モデルを併用、コンテキスト自動圧縮** |
| ローカル実行 | ✕ | ✕ | **◎（Ollama/LM Studioでオフライン可）** |
| OSS | ✕ | ✕ | **◎（Apache 2.0、カスタムディストロも可能）** |
| エディタ統合 | ◎ | CLI中心 | **ACP対応でJetBrains/Zedに接続可** |

要するに「**どのLLMでも、どの環境でも、標準プロトコルで拡張できる自律エージェント**」という立ち位置。OSSゆえに社内ポリシーに合わせたカスタマイズも容易。

### 使うときの流れ

```
1. インストール
   ├─ macOS: brew install goose  /  Desktop版DMG
   ├─ Linux: install.sh スクリプト
   └─ Windows: Desktop版インストーラ

2. 初期設定  (goose configure)
   ├─ LLMプロバイダ選択（Anthropic, OpenAI, Azure, Ollama …）
   ├─ APIキー入力（またはOAuth認証）
   └─ 権限モード選択（auto / approve / smart_approve）

3. 拡張(Extension)の追加（任意）
   ├─ 組み込み: developer(デフォルト有効), memory, computer-controller 等
   └─ 外部MCP: npx @modelcontextprotocol/server-github 等を config.yaml に追記

4. セッション開始
   $ goose                     # 対話セッション
   $ goose run "タスク内容"    # ワンショット実行
   - .goosehints ファイルでプロジェクト固有の指示を与えられる
   - レシピ/プランで複雑なワークフローを定義可能

5. エージェントが自律動作
   - ファイル作成・編集（find-and-replace方式でトークン節約）
   - シェルコマンド実行、テスト、デバッグ
   - 外部API呼び出し（GitHub, DB, Slack等はMCP経由）
   - コンテキストが肥大化すると自動要約で圧縮

6. セッション管理
   - 会話履歴は永続化され、再開可能
   - Chat Recallで過去セッション横断検索
```

### リポジトリ構成（主要部分）

| ディレクトリ | 内容 |
|---|---|
| `crates/goose` | コアロジック（プロバイダ統合・ツール実行・コンテキスト管理） |
| `crates/goose-cli` | CLI フロントエンド |
| `crates/goose-server` | Axum ベースの HTTP/WebSocket バックエンド |
| `crates/goose-mcp` | 組み込みMCP拡張群（developer, memory等） |
| `crates/goose-acp` | Agent Client Protocol 対応（エディタ連携） |
| `ui/desktop` | Electron デスクトップアプリ（React/TypeScript） |
| `documentation/` | Docusaurus ドキュメントサイト |
