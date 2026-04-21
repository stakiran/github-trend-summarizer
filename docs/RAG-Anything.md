---
url: https://github.com/HKUDS/RAG-Anything
keywords: RAG, マルチモーダル, LightRAG, 知識グラフ, MinerU, VLM, 文書解析, Python
oneliner: PDF・画像・表・数式を含む文書を一気通貫で取り込めるマルチモーダル対応のオールインワン RAG フレームワーク。
---

# RAG-Anything まとめ

## 1. このリポジトリは何？

香港大学データインテリジェンス研究室（HKUDS）が開発する **マルチモーダル対応のオールインワン RAG フレームワーク** です。グラフ RAG の実装である **LightRAG を基盤** に拡張されており、テキストだけでなく **画像・表・数式・チャート** を含む複雑なドキュメントを単一のパイプラインで取り込んで検索・質問応答できます。

処理は次の 5 段階パイプラインで構成されます。

1. **Document Parsing**：MinerU / Docling / PaddleOCR などで PDF・Office・画像を解析。
2. **Multi-Modal Content Understanding**：コンテンツをモダリティ別に分類。
3. **Multimodal Analysis Engine**：VLM（GPT-4o など）で画像・表・数式を解釈。
4. **Multimodal Knowledge Graph Index**：LightRAG により知識グラフとベクトル索引を構築。
5. **Modality-Aware Retrieval**：テキスト／マルチモーダル両方のクエリに対応した検索。

対応形式は PDF、DOC/DOCX、PPT/PPTX、XLS/XLSX、TXT、MD、JPG/PNG/BMP/TIFF/GIF/WebP など広範です（Office 系は LibreOffice が必要）。主要モジュールは `raganything/` 配下の `raganything.py`（メインクラス）、`config.py`（設定）、`parser.py`、`modalprocessors.py`、`query.py`、`batch.py` など。Python 3.10+、現行バージョンは 1.2.10。

## 2. 何が嬉しいのか（既存手段との比較）

従来の RAG スタックは概ね以下の課題を抱えていました。

- **LangChain / LlamaIndex の標準 RAG**：テキスト中心で、画像や表は OCR 抽出したテキストに押し込むのが基本。図表の意味的理解が失われる。
- **LightRAG / GraphRAG**：グラフ構造化された検索に強いが、入口のマルチモーダルパースは別途自前で用意する必要がある。
- **MinerU / Docling 単体**：高精度な文書解析器だが、RAG のインデックス・検索・LLM 応答までは責務外。

RAG-Anything はこれらを **一つのフレームワークに統合** している点が差別化要素です。

- **マルチモーダル一貫処理**：`ImageModalProcessor` / `TableModalProcessor` / `EquationModalProcessor` / `GenericModalProcessor` が VLM を呼び、各モダリティを意味のあるエンティティとして知識グラフに格納。
- **パーサー差し替え可能**：`parser="mineru" | "docling" | "paddleocr"` を設定で切替。MinerU は GPU 加速・OCR・表抽出に対応。
- **既存解析結果の直接投入**：`insert_content_list()` で外部パイプラインの出力をそのまま取り込めるので、解析だけ他ツールを使う運用にも対応。
- **グラフ RAG を標準装備**：LightRAG の `hybrid` モード等を使ったモダリティ横断検索、`aquery_with_multimodal()` による画像・表を含むクエリが可能。
- **バッチ・並列処理**：`process_folder_complete()` と `BatchMixin`、`max_concurrent_files` によるフォルダ一括処理。

つまり「パーサー＋VLM＋グラフ RAG＋マルチモーダル検索」を自前で組み合わせる手間を省ける点が最大の価値です。

## 3. 使うときの流れ

**インストール**

```bash
pip install raganything            # 最小構成
pip install 'raganything[all]'     # 全機能（PaddleOCR・画像・テキスト拡張含む）
# 併せて LibreOffice を入れておくと Office 文書も処理可能
```

**典型的なコードフロー**（`examples/raganything_example.py` が参考）

```python
from raganything import RAGAnything, RAGAnythingConfig

config = RAGAnythingConfig(
    working_dir="./rag_storage",
    parser="mineru",              # or "docling" / "paddleocr"
    parse_method="auto",
    enable_image_processing=True,
    enable_table_processing=True,
    enable_equation_processing=True,
)

rag = RAGAnything(
    config=config,
    llm_model_func=llm_model_func,           # 例: GPT-4o-mini
    vision_model_func=vision_model_func,     # 例: GPT-4o（画像用 VLM）
    embedding_func=embedding_func,           # 例: text-embedding-3-large
)

# 1) 取り込み：ファイル/フォルダ単位のエンドツーエンド処理
await rag.process_document_complete("paper.pdf", output_dir="./output")
# または外部パース結果を直接投入
await rag.insert_content_list(content_list, file_path="paper.pdf")

# 2) クエリ：テキスト or マルチモーダル
answer = await rag.aquery("この論文の主結果は？", mode="hybrid")
answer = await rag.aquery_with_multimodal(
    "この図と本文はどう整合する？",
    multimodal_content=[{"type": "image", "img_path": "fig1.png"}],
    mode="hybrid",
)
```

**全体の流れ**：環境準備（LLM / VLM / Embedding 関数と API キーを用意）→ `RAGAnythingConfig` で挙動とパーサーを指定 → `RAGAnything` を初期化 → `process_document_complete` / `process_folder_complete` / `insert_content_list` で取り込み → `aquery` または `aquery_with_multimodal` で検索・回答。バッチ処理やモーダル単体の使い方は `examples/` 配下（`batch_processing_example.py`、`modalprocessors_example.py`、`insert_content_list_example.py` など）に揃っています。
