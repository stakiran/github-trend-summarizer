---
url: https://github.com/VectifyAI/PageIndex
keywords: RAG, Vectorless, LLM, Tree Index, Reasoning, PDF, Document Retrieval
oneliner: 長文ドキュメントを「目次ツリー」として索引化し、LLMの推論でツリー探索することでベクトルDBを使わずに高精度な検索を行う"Vectorless RAG"フレームワーク。
---

# PageIndex 概要

## このリポジトリは何？

**PageIndex** は、長文PDF/Markdown向けの **Vectorless（ベクトルレス）かつ Reasoning-based（推論ベース）な RAG** を実現する Python フレームワーク（VectifyAI 製、MITライセンス）。中核アイデアは以下の2ステップ：

1. **Tree Index 生成**：PDFの目次（ToC）を解析し、章・節を `node_id` / `start_index` / `end_index` / `summary` を持つ階層的なJSONツリーへ変換（`run_pageindex.py`）。
2. **Tree Search による検索**：LLMがそのツリーを「人間が目次をめくるように」たどり、関連ノードを推論で選択。ベクトル類似度ではなく **関連性そのもの** で取得する。

主な構成：
- `pageindex/page_index.py` …PDF→ツリー化のメインロジック
- `pageindex/page_index_md.py` …Markdown向け（`#` の階層を利用）
- `pageindex/retrieve.py` …`get_document` / `get_document_structure` / `get_page_content` の3ツール
- `pageindex/client.py` …`PageIndexClient`（ローカルワークスペース管理）
- `examples/agentic_vectorless_rag_demo.py` …OpenAI Agents SDK と組み合わせたエージェント例
- LLM呼び出しは LiteLLM 経由でマルチプロバイダ対応（OpenAI / Anthropic 等）

## 何が嬉しいの？（既存手段との比較）

従来の **vector RAG（チャンク分割＋埋め込み＋ベクトルDB）** との違い：

| 観点 | 一般的な Vector RAG | PageIndex |
|---|---|---|
| 索引 | 固定長チャンク + 埋め込みベクトル | ドキュメント本来の章節構造ツリー |
| 検索原理 | 類似度（similarity） | LLMによる関連性推論（relevance） |
| インフラ | ベクトルDB（Pinecone/Faiss等）必須 | **不要**。JSONツリー＋LLMだけ |
| チャンク分割 | 必要（境界で文脈断絶しがち） | **不要**。自然なセクション単位 |
| 説明性 | 不透明な“vibe retrieval” | ページ番号・節IDで根拠が追跡可能 |
| 文脈考慮 | クエリ単発の埋め込みが中心 | 会話履歴やドメイン知識を都度反映可 |
| ベンチ | — | FinanceBench で **98.7%** の SOTA を主張 |

要するに「**ベクトルDBの運用コストとチャンク境界問題から解放され、専門ドキュメントで必要な多段推論や根拠提示に強い**」のが嬉しい点。財務報告・規制文書・法務/技術マニュアル・教科書など、長く構造化された文書での効果が大きい。

## 使うときの流れ

### A. ツリー索引の生成（最小利用）
1. `pip install --upgrade -r requirements.txt`
2. `.env` に `OPENAI_API_KEY=...`（LiteLLM 経由で他プロバイダも可）を設定
3. PDFなら `python3 run_pageindex.py --pdf_path /path/to/doc.pdf`
   Markdownなら `--md_path /path/to/doc.md`
4. `./results/<docname>_structure.json` にツリー（title / node_id / start_index / end_index / summary）が出力される

主なオプション：`--model`、`--toc-check-pages`、`--max-pages-per-node`、`--max-tokens-per-node`、`--if-add-node-summary` など（`config.yaml` の値を上書き）。

### B. Agentic Vectorless RAG として使う
1. `pip install openai-agents` を追加
2. `PageIndexClient(workspace=...)` でクライアントを生成し、`client.index(pdf_path)` でドキュメントIDを得る
3. エージェントに3ツール（`get_document` / `get_document_structure` / `get_page_content`）を渡す
4. ユーザの質問に対し、LLMが自律的に「メタ情報を見る → ツリーから該当節を選ぶ → 該当ページのみ取得して回答」という人間の調査フローを再現
5. サンプル実行：`python3 examples/agentic_vectorless_rag_demo.py`

### C. さらに高品質が必要な場合
本リポジトリは標準PDFパース前提。複雑なPDFや大規模コーパスでは公式の **Cloud Service（OCR強化＋API/MCP）** や **Chat Platform**（chat.pageindex.ai）への移行が想定されている。`cookbook/` には Vision RAG（OCR不要、ページ画像直読み）や agentic retrieval などの Notebook も同梱。
