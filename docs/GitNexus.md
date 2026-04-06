---
url: https://github.com/abhigyanpatwari/GitNexus
keywords: knowledge-graph, code-intelligence, graph-rag, mcp, static-analysis
oneliner: ソースコードをナレッジグラフ化し、AIエージェントや対話的UIから依存関係・影響範囲・実行フローを即座に問い合わせられるコードインテリジェンスエンジン。
---

## GitNexus — ゼロサーバー・コードインテリジェンスエンジン

### これは何？

GitNexus は、任意のコードベースを **ナレッジグラフ** に変換するツール。Tree-sitter で 14 言語の AST を解析し、関数呼び出し・インポート・継承などの関係を抽出したうえで、Leiden アルゴリズムによる機能クラスタリングや BFS による実行フロー検出まで自動で行う。構築されたグラフは以下の 2 つの経路で利用できる。

| 経路 | 対象ユーザー | 仕組み |
|------|-------------|--------|
| **CLI + MCP サーバー** | 日常開発者（Cursor / Claude Code / Codex 等） | `gitnexus analyze` でインデックス → エディタが MCP 経由で 16 種のツールを呼び出す |
| **Web UI** | コード探索したい人 | ブラウザに ZIP やフォルダを投げ込む → WASM 上でグラフ構築 → Sigma.js で可視化 + LLM チャット |

コア技術スタック: Node.js / Tree-sitter / LadybugDB（グラフDB）/ Graphology / BM25+ベクトル検索の RRF ハイブリッド。Web 版は全て WASM でブラウザ完結（コードが外に出ない）。

---

### 何が嬉しいのか？（既存手段との比較）

| 観点 | GitNexus | DeepWiki 等のドキュメント生成系 | 一般的な Graph RAG |
|------|----------|-------------------------------|-------------------|
| **目的** | 構造的な分析・影響範囲把握 | コードの理解・説明 | 知識ベースからの検索回答 |
| **事前計算** | クラスタリング・実行フロー・信頼度スコアまで構築済み | ドキュメントを生成するだけ | 生のエッジのみ、LLM が逐次探索 |
| **1 回の問い合わせ精度** | `impact` 1 回で blast radius（影響範囲）+ リスクレベルが返る | — | 10 回以上のクエリチェーンが必要 |
| **小型 LLM との相性** | ツール側が重い処理を済ませるため小型モデルでも機能 | 大コンテキストが前提 | 大コンテキストが前提 |
| **プライバシー** | 完全ローカル（CLI も Web も） | サーバー送信あり | 構成次第 |

要するに「**AIエージェントがコードを変更する前に "何が壊れるか" を 1 コマンドで把握できる**」のが最大の価値。従来の grep / LSP では得られない、クラスタ横断の影響伝播とリスク判定が自動で付く。

---

### 使うときの流れ

#### A. CLI + MCP（開発者向け・推奨）

```
1. セットアップ（初回のみ）
   $ npx gitnexus setup
   → Cursor / Claude Code 等を自動検出し MCP 設定を書き込む

2. リポジトリをインデックス
   $ cd /path/to/repo
   $ npx gitnexus analyze
   → .gitnexus/ にグラフDB生成、~/.gitnexus/registry.json に登録
   → AGENTS.md, CLAUDE.md を自動生成

3. エディタで使う
   ・MCP 経由で AI エージェントがツールを呼び出す
   ・主要ツール:
     - query("認証バリデーション")  → 関連する実行フローを検索
     - context("validateUser")      → 呼び出し元/先・所属プロセス一覧
     - impact("UserService.validate", "upstream") → 影響範囲 + リスクレベル
     - detect_changes()             → コミット前に変更の波及範囲を確認
     - rename("oldName", "newName", dry_run=true) → グラフ対応の安全リネーム

4. コミット前チェック
   $ gitnexus detect_changes  → 変更が意図した範囲に収まっているか確認
```

#### B. Web UI（ブラウザ完結・お試し向け）

```
1. https://gitnexus.vercel.app を開く
2. ZIP またはローカルフォルダをドラッグ＆ドロップ
3. ブラウザ内で WASM がグラフを構築（数秒〜数十秒）
4. グラフを視覚的に探索 / 実行フローを追跡 / Nexus AI に質問
   → LLM は OpenAI / Gemini / Anthropic / Ollama から選択可能
```
