---
url: https://github.com/tobi/qmd
keywords: local-search, rag, sqlite, vector-search, mcp
oneliner: ローカル環境で完結するドキュメント検索エンジンCLIで、BM25・ベクトル検索・LLMリランキングを組み合わせたハイブリッド検索を提供する。
---

## QMD — Query Markup Documents

### これは何？

ローカルで動作する **ドキュメント専用のハイブリッド検索エンジン**。議事録・ナレッジベース・個人メモなど、手元のテキストファイル群を「コレクション」として登録し、CLI から高精度に全文検索できる。内部は SQLite 上に構築されており、以下の 3 つの検索方式を組み合わせる：

| 検索方式 | 技術 | 特徴 |
|---|---|---|
| **キーワード検索** | SQLite FTS5 (BM25) | 高速・完全一致に強い |
| **ベクトル検索** | sqlite-vec + embeddinggemma | 意味的に近い文書を発見 |
| **LLM リランキング** | qwen3-reranker (ローカル推論) | 検索結果の精度を最終調整 |

`qmd query` コマンドではこの 3 つを **Reciprocal Rank Fusion (RRF)** で統合し、さらに LLM によるクエリ拡張（類義語・言い換え生成）も自動で行う。すべてローカル完結で、外部 API 不要。

### 何が嬉しいのか？（既存手段との比較）

| 比較対象 | QMD の優位点 |
|---|---|
| **grep / ripgrep** | キーワード完全一致しかできない。QMD はベクトル検索で「意味が近い」文書も拾える |
| **Obsidian / Notion 検索** | 特定アプリに閉じた検索。QMD は任意のテキストファイルを横断でき、CLI/SDK/MCP 経由でどこからでも使える |
| **Elasticsearch 等** | サーバー構築が必要。QMD は SQLite 1 ファイルで完結し、`npm install -g` だけで使える |
| **OpenAI Embeddings 等** | クラウド API 依存。QMD はモデルを自動ダウンロードしローカルで推論するため、データが外部に出ない |

**QMD ならではの特徴的な機能：**

- **コンテキストシステム** — コレクションやパスごとに説明文を付与でき、検索結果と一緒に返る。AI エージェントが結果を解釈する際の精度が上がる
- **AST 対応チャンキング** — tree-sitter で関数・クラス単位にコードを分割。トークン境界でぶった切らない
- **MCP サーバー内蔵** — Claude Desktop などの AI アシスタントから直接検索できる（HTTP モードならモデルを常駐させ高速応答）

### 使うときの流れ

```
① インストール
   npm install -g @tobilu/qmd

② コレクション登録（ドキュメントフォルダを指定）
   qmd collection add ~/Documents/notes --name mynotes --mask '**/*.md'

③ コンテキスト付与（任意だが推奨）
   qmd context add qmd://mynotes/ "個人の技術メモ。主にGoとTypeScript"

④ インデックス構築
   qmd update          # 全文検索インデックスを作成
   qmd embed           # ベクトル埋め込みを生成（初回はモデル自動DL）

⑤ 検索
   qmd query "認証フローの実装方法"   # ← ハイブリッド検索（推奨）
   qmd search "OAuth"                # ← キーワードのみ（高速）
   qmd vsearch "ログイン処理"         # ← ベクトルのみ

⑥ ドキュメント取得
   qmd get "#abc123"                 # 検索結果の docid で本文を取得
   qmd multi-get "docs/**/*.md"      # glob で一括取得
```

**日常的な運用は ④→⑤ の繰り返し**。ドキュメントが更新されたら `qmd update` → `qmd embed` で再インデックスする。AI エージェント連携したい場合は `qmd mcp --http --daemon` でバックグラウンドサーバーを立てておけばよい。
