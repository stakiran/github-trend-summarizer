---
url: https://github.com/opendataloader-project/opendataloader-pdf
keywords: PDF parser, AI-ready data, RAG, reading order, table extraction, accessibility, hybrid mode, LangChain, MCP
oneliner: AI/RAG パイプライン向けに構造化データを高精度・高速に抽出するオープンソース PDF パーサー
---

## OpenDataLoader PDF — 概要整理

### これは何？

**PDF を AI が扱いやすい構造化データに変換する**オープンソース（Apache-2.0）のパーサー。Java コアエンジンに Python / Node.js のラッパー SDK を備えたモノレポ構成で、CLI・SDK・MCP（Claude Desktop 等）・LangChain 統合など多彩なインターフェースを提供する。Hancom Inc. がスポンサー。

出力形式は **JSON（バウンディングボックス付き）・Markdown・HTML・テキスト・注釈付き PDF・Tagged PDF** の 6 種。見出し・段落・表・リスト・画像・数式・キャプションを意味的に分類し、全要素に座標情報を付与する。

---

### 何が嬉しいのか？（既存ツールとの比較）

| 観点 | OpenDataLoader PDF | docling | marker | pymupdf4llm |
|---|---|---|---|---|
| **総合精度** | **0.907** | 0.882 | 0.861 | 0.732 |
| **表抽出 (TEDS)** | **0.928** | 0.887 | 0.808 | 0.401 |
| **読み順 (NID)** | **0.934** | 0.898 | 0.826 | 0.731 |
| **ローカル速度** | **0.015 秒/頁** | 0.762 | 53.9 | 0.091 |
| **バウンディングボックス** | ✅ 全要素 | ✗ | ✗ | ✗ |
| **AI 安全（隠しテキスト検出）** | ✅ 組込み | ✗ | ✗ | ✗ |
| **GPU 不要のローカルモード** | ✅ | △ | ✗ | ✅ |
| **ライセンス** | Apache-2.0 | Apache-2.0 | **AGPL** | Apache-2.0 |

**3 つの差別化ポイント：**

1. **速度と精度の両立** — ローカルモード（Java のみ）は GPU 不要で 60 頁/秒超。複雑な表・スキャン PDF は Hybrid モード（Docling 等のバックエンド）に自動ルーティングし精度を最大化する「スマートトリアージ」設計。
2. **AI パイプライン前提の設計** — 全要素にバウンディングボックスを付与、出力が決定的（同一入力→同一出力）。プロンプトインジェクション対策（隠しテキスト・極小文字・不可視レイヤー除去）や個人情報サニタイズ機能を内蔵。
3. **PDF アクセシビリティ自動化** — Tagged PDF への自動タグ付け（Q2 2026 予定）を Apache-2.0 で提供する初の OSS。PDF Association・veraPDF と連携し PDF/UA 準拠を目指す。

---

### 使うときの流れ

```
① インストール
    Python:  pip install opendataloader-pdf
    Node.js: npm install @opendataloader/pdf
    Java:    Maven dependency を追加

② 基本変換（ローカルモード — GPU 不要）
    CLI:     opendataloader-pdf input.pdf --format json,markdown
    Python:  opendataloader_pdf.convert(input_path=["input.pdf"], format="markdown")
    Node.js: await convert(["input.pdf"], { format: "markdown" })

③ 高精度変換（Hybrid モード — 複雑な表・スキャン PDF 向け）
    pip install "opendataloader-pdf[hybrid]"
    # ターミナル 1: バックエンドサーバー起動
    opendataloader-pdf-hybrid --port 5002
    # ターミナル 2: Hybrid 指定で変換
    opendataloader-pdf --hybrid docling-fast input.pdf

④ RAG / LLM パイプラインへの組込み
    - LangChain:  OpenDataLoaderPDFLoader → split → vector store → retriever
    - MCP:        Claude Desktop / Cursor 等に MCP サーバーとして登録
    - バッチ処理:  ディレクトリごと渡せば単一 JVM で一括処理（起動コスト最小化）

⑤ 出力を活用
    - JSON: バウンディングボックス・メタデータ付き構造化データ → 精密な後処理に
    - Markdown: そのまま LLM のコンテキストに投入
    - Tagged PDF: アクセシビリティ準拠ドキュメントとして配布
```

> **開発者向け注意:** Java 側の CLI オプションを変更したら必ず `npm run sync` を実行すること。Python / Node.js バインディングの自動生成が走り、忘れるとラッパーが壊れる。
