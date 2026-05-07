---
url: https://github.com/LearningCircuit/local-deep-research
keywords: Deep Research, Local LLM, Ollama, RAG, SearXNG
oneliner: ローカル LLM と多数の検索エンジンを組み合わせ、引用付きの「深い調査レポート」を自分のマシン上で生成できるプライバシー重視の AI リサーチアシスタント。
---

# Local Deep Research (LDR) ざっくり整理

## 1. このリポジトリは何？

**「OpenAI Deep Research のオープンソース版」を、完全ローカル運用できる形で実装した AI リサーチアシスタント**。

- 複雑な質問を投げると、LLM がエージェント的にループで検索→要約→再検索を繰り返し、**出典付きのレポート**を自動生成する。
- LLM は **Ollama / LM Studio / llama.cpp**（ローカル）と **OpenAI / Anthropic / Google / OpenRouter**（クラウド）を切替可能。
- 検索ソースは 10 系統以上：**arXiv / PubMed / Semantic Scholar / Wikipedia / SearXNG / GitHub / Tavily / Brave / Google(SerpAPI) / Wayback Machine / The Guardian / ローカル文書 / 任意の LangChain Retriever**。
- フロントは Flask ベースの Web UI（`http://localhost:5000`）+ REST API + **MCP サーバ（Claude Desktop / Claude Code 連携用 `ldr-mcp`）** + Python API（`from local_deep_research.api import ...`）。
- データは **SQLCipher (AES-256) でユーザーごとに暗号化**された DB に保存。テレメトリ・解析・トラッキングなし。
- ベンチマークでは **SimpleQA で約 95%（GPT-4.1-mini + SearXNG + focused-iteration 構成）** を主張。
- 配布形態：PyPI (`pip install local-deep-research`)、Docker / Docker Compose、Unraid テンプレート。MIT ライセンス。

## 2. このリポジトリは何が嬉しいの？（既存比較）

| 比較対象 | LDR の差別化ポイント |
|---|---|
| **OpenAI / Gemini / Perplexity の Deep Research** | クローズドかつクラウド限定。LDR は **完全ローカル実行可（Ollama+SearXNG だけで外部 API ゼロ）** で、機密案件・ジャーナリスト・社内文書調査に使える。API コストもゼロ化できる。 |
| **GPT Researcher 等の OSS Deep Research 系** | LDR は **検索エンジンの種類が圧倒的に多い**（arXiv/PubMed/Semantic Scholar/NASA ADS/Zenodo/PubChem 等の学術系まで網羅）。さらに **20+ のリサーチ戦略**（Quick Summary / Detailed / Report / 新しい LangGraph Agent 等）から選べる。 |
| **素の LangChain RAG / 自前スクリプト** | Web UI、認証、研究履歴、PDF/Markdown 出力、レート制御、コスト/性能を可視化する **Analytics Dashboard**、定期購読（News Subscription）、**ジャーナル品質スコアリング（212K+ ソース、predatory ジャーナル検知）** などが最初から揃っている。 |
| **生のローカル LLM チャット** | 「検索→ダウンロード→ライブラリにインデックス→次回はローカル文書も合わせて検索」という **知識ベースが時間とともに積み上がる** ループが組み込まれている。 |
| **セキュリティ面** | **SQLCipher による per-user 暗号化 DB**、ゼロ知識（パスワード復旧なし）、Cosign 署名済み Docker イメージ + SLSA provenance + SBOM。CodeQL/Semgrep/Bearer 等を CI で常時回している。 |

要するに、**「Deep Research 的体験 × ローカル/プライバシー × 学術検索の網羅性 × 蓄積型の個人ナレッジベース」** を一つにまとめたのが他にない強み。

## 3. 使うときの流れ

最も標準的なのは **Docker Compose ルート**。

1. **環境を立てる**
   - 推奨：Ollama コンテナ（LLM 提供） + SearXNG コンテナ（メタ検索） + LDR コンテナをまとめて起動。
     ```bash
     # 1) LLM
     docker run -d -p 11434:11434 --name ollama ollama/ollama
     docker exec ollama ollama pull gpt-oss:20b
     # 2) 検索
     docker run -d -p 8080:8080 --name searxng searxng/searxng
     # 3) LDR 本体
     docker run -d -p 5000:5000 --network host \
       --name local-deep-research -v deep-research:/data \
       -e LDR_DATA_DIR=/data localdeepresearch/local-deep-research
     ```
   - 軽くやるなら `pip install local-deep-research` でも可。

2. **ブラウザで `http://localhost:5000` にアクセス**してアカウント作成（暗号化 DB がここで初期化される）。Settings → LLM でモデル（例：`gpt-oss:20b` / `qwen3:27b`）と検索エンジンを選択。

3. **リサーチモードを選んで質問を投げる**
   - Quick Summary（30 秒〜3 分） / Detailed Research / Report Generation / Document Analysis。
   - 戦略は `focused-iteration`（高精度実績）や、新しい `langgraph-agent`（LLM 自身が検索エンジンを動的選択するエージェント）。

4. **結果を確認・活用**
   - WebSocket で進捗がリアルタイム表示 → 完了後、引用付きレポートを **PDF / Markdown でエクスポート**。
   - 気に入ったソースをそのまま **Library にダウンロード → 自動でテキスト抽出＆インデックス化**。次回以降は自分の蓄積文書と Web を横断検索できる。

5. **応用パス**
   - **Python から自動化**：`quick_query(user, pass, "...")` や `LDRClient` で REST 経由実行。
   - **Claude Desktop / Claude Code から呼ぶ**：`pip install "local-deep-research[mcp]"` して `ldr-mcp` を MCP サーバ登録 → `quick_research` / `detailed_research` / `generate_report` などを Claude のツールとして使える。
   - **社内ナレッジ統合**：FAISS/Chroma/Pinecone/Weaviate などの LangChain Retriever を `retrievers={...}` で渡せば社内文書も検索対象に。
   - **定期リサーチ購読**：トピックを subscribe して daily/weekly のダイジェストを自動生成。
   - **ベンチマーク**：`python -m local_deep_research.benchmarks --dataset simpleqa --examples 50` で自分の構成を計測し、Hugging Face のコミュニティリーダーボードに投稿可能。
