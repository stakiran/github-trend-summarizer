以下にまとめます。

---
url: https://github.com/zilliztech/claude-context
keywords: MCP, semantic code search, vector database, Milvus, embeddings, Claude Code, BM25, AST
oneliner: Claude Code などの AI コーディングエージェントに、コードベース全体をセマンティック検索して文脈として与える MCP プラグイン。
---

# zilliztech/claude-context 調査メモ

## このリポジトリは何？

**Claude Context** は、コードベース全体を「コーディングエージェントの context」として使えるようにする **MCP (Model Context Protocol) プラグイン**。Claude Code を中心に、Cursor / Gemini CLI / Codex CLI / Windsurf / Cline / Roo / VS Code など多数の MCP クライアントから利用できる。主要言語は TypeScript の pnpm モノレポで、以下の 4 パッケージで構成される。

- `@zilliz/claude-context-core` — インデクシングと検索のコアエンジン（embedding + ベクトル DB 統合）
- `@zilliz/claude-context-mcp` — MCP サーバ本体（`index_codebase`, `search_code`, `clear_index`, `get_indexing_status` の 4 ツールを提供）
- VSCode 拡張 "Semantic Code Search"
- Chrome 拡張

内部の実装の特徴：
- **ハイブリッド検索**：BM25（疎）＋ dense ベクトルの組み合わせ
- **AST ベースのコードチャンキング**（失敗時は文字数ベースにフォールバック）
- **Merkle tree による増分インデクシング**（変更ファイルだけ再埋め込み）
- **Embedding プロバイダ**：OpenAI / VoyageAI / Gemini / Ollama
- **ベクトル DB**：Milvus もしくは Zilliz Cloud（マネージド）
- 対応言語：TS/JS, Python, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, Markdown

## このリポジトリは何が嬉しい？（既存手段との比較）

**解決する痛み**：Claude Code などのエージェントは、既定ではファイル一覧やディレクトリを逐次読み込んで文脈を広げる多段ディスカバリを行うため、巨大リポジトリでは (1) トークン代が跳ね上がる、(2) 関連箇所を取り逃す、(3) ラウンドトリップで遅い。Claude Context は予めベクトル DB にコードをインデックスし、自然言語クエリで「関係あるチャンクだけ」を一発で投入する。公式の評価では同等の検索品質で **約 40% のトークン削減** と主張。

類似ツールとの差別化（README の FAQ より）：
- **Serena**：Language Server ベースの記号的理解に強い汎用コーディングエージェントツールキット。Claude Context はセマンティック検索に特化。
- **Context7**：最新ドキュメント/サンプルを注入して幻覚を防ぐのが主目的。社内コードは対象外。
- **DeepWiki**：GitHub リポジトリから対話的ドキュメントを「生成」する。検索インフラではない。
- **ripgrep/Grep 系**：キーワード一致のみで、`"ユーザー認証を扱う関数"` のような意味的問い合わせができない。

要するに「**自社/手元のコードベース全体を、意味レベルで検索できる恒常的インデックス**」を MCP 越しに任意のエージェントに与えられる、という層を埋めるプロダクト。

## 使うときの流れ

1. **前提を用意**
   - Node.js ≥ 20.0.0 かつ < 24.0.0
   - Zilliz Cloud の API キー（無料枠あり）または自前 Milvus
   - OpenAI（あるいは VoyageAI/Gemini/Ollama）の embedding API キー
2. **MCP サーバをクライアントに登録**。Claude Code の場合：
   ```bash
   claude mcp add claude-context \
     -e OPENAI_API_KEY=sk-... \
     -e MILVUS_TOKEN=... \
     -- npx @zilliz/claude-context-mcp@latest
   ```
   他クライアントは `mcpServers` 設定に同等の `npx` コマンドと env を書くだけ。
3. **対象プロジェクトを開いて会話で指示**
   - `Index this codebase` — AST で分割し埋め込み → Milvus/Zilliz に格納（初回のみ時間がかかる。以降は Merkle tree 差分で高速）
   - `Check the indexing status` — 進捗確認
   - `Find functions that handle user authentication` のような自然言語検索
4. **必要に応じてチューニング**：`.env` やクライアント設定で embedding モデル（例：`text-embedding-3-large`, `voyage-code-3`）、対象拡張子・除外パターンを調整。多人数開発では Zilliz Cloud を共有インデックスとして使える。
5. （MCP 以外の選択肢）直接アプリに組み込む場合は `@zilliz/claude-context-core` を import して `context.indexCodebase()` → `context.semanticSearch()`、IDE だけで使いたい場合は VS Code の "Semantic Code Search" 拡張。
