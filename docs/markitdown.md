---
url: https://github.com/microsoft/markitdown
keywords: markdown, converter, LLM, document, file-conversion
oneliner: あらゆるファイル形式（PDF・Office・画像・音声など）をMarkdownに変換するPythonツール
---

## MarkItDown — ファイル→Markdown 変換ツール

### これは何？

Microsoft が公開している **Python ライブラリ兼 CLI ツール**。PDF・Word・Excel・PowerPoint・HTML・画像・音声など **20 種以上のファイル形式を Markdown テキストに変換**する。見出し・表・リスト・リンクといった文書構造をできる限り保持したまま Markdown に落とし込む点が特徴。

```bash
# CLI
pip install 'markitdown[all]'
markitdown report.pdf -o report.md

# Python API
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("report.pdf")
print(result.markdown)
```

### 何が嬉しいのか？ — 既存ツールとの比較

| 観点 | MarkItDown | textract / Apache Tika など |
|---|---|---|
| **出力形式** | **Markdown**（見出し・表・リストを構造化） | プレーンテキスト（構造が失われがち） |
| **LLM 親和性** | Markdown は LLM が最も扱いやすい形式。RAG パイプラインにそのまま投入可能 | トークン効率やコンテキスト理解で不利 |
| **対応形式の幅** | PDF, DOCX, PPTX, XLSX, HTML, 画像(EXIF), 音声, YouTube, Wikipedia, RSS, ZIP 等 | 同等〜やや広いが、Web 系ソースは非対応が多い |
| **拡張性** | Python entry-point ベースの**プラグイン機構**。優先度付きで既存コンバータの差し替えも可能 | 拡張には本体改修が必要なことが多い |
| **LLM 連携** | OpenAI 互換クライアントを渡すと画像キャプション生成・音声文字起こしを自動実行 | LLM 連携は自前で組む必要あり |
| **MCP サーバー** | Claude Desktop 等から直接呼べる MCP パッケージを同梱 | なし |

> **一言で言えば**: 「あらゆるファイルを、LLM が読みやすい Markdown に統一変換するハブ」。RAG・要約・分析といった LLM ワークフローの**前処理を一行で済ませる**のが最大の価値。

### 使い方の流れ

```
1. インストール
   ┌─────────────────────────────────────────────┐
   │ pip install 'markitdown[pdf,docx,pptx]'     │  ← 必要な形式だけ選べる
   │ pip install markitdown-ocr                   │  ← OCR が要れば追加
   └─────────────────────────────────────────────┘

2. 変換（3 つの入力経路）
   ┌──────────────────┐
   │ ローカルファイル  │  md.convert("file.pdf")
   │ URL              │  md.convert("https://example.com/page.html")
   │ バイナリストリーム│  md.convert_stream(io_obj, extension=".pdf")
   └──────────────────┘
         │
         ▼
   ┌─────────────────────────────────────────────┐
   │  MarkItDown 内部パイプライン                 │
   │  1. magika でファイル種別を自動判定          │
   │  2. 優先度順にコンバータを試行               │
   │  3. Markdown を正規化して返却                │
   └─────────────────────────────────────────────┘
         │
         ▼
3. 結果を取得
   result.markdown   → 変換された Markdown 文字列
   result.title      → 文書タイトル（取得できた場合）

4. 活用例
   - LLM に渡して要約・QA・翻訳
   - RAG のチャンクソースとして Embedding
   - ナレッジベース構築の前処理
```

### アーキテクチャの要点

- **コンバータは独立モジュール**（`converters/` に 22 個）。`accepts()` → `convert()` の 2 メソッドで構成され、追加・差し替えが容易。
- **プラグイン機構**: `pyproject.toml` の entry-point に登録するだけで、`--use-plugins` や `enable_plugins=True` で有効化。
- **オプショナル依存**: `[pdf]`, `[docx]` 等のエクストラで必要なものだけインストールでき、最小構成では軽量に使える。
