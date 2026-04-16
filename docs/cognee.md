---
url: https://github.com/topoteretes/cognee
keywords: knowledge-graph, AI-memory, RAG, ECL-pipeline, vector-search, LLM, agent-memory, ontology
oneliner: あらゆる形式のデータを知識グラフ＋ベクタ検索の「AI メモリ」に変換し、エージェントに永続的な文脈を与える OSS ナレッジエンジン。
---

# topoteretes/cognee

## このリポジトリは何？

**Cognee** は、AI エージェントのための「記憶（メモリ）」基盤を構築する OSS のナレッジエンジン。テキスト・PDF・DOCX・CSV・画像・音声・コード・URL など任意形式のデータを取り込み、LLM を用いてエンティティとリレーションを抽出、**知識グラフ＋ベクタ検索＋リレーショナル DB のハイブリッド**として永続化する。従来の RAG に代わる **ECL (Extract → Cognify → Load)** パイプラインが中核。

- 言語: Python 3.9–3.13 / FastAPI / CLI / Web UI
- 主要 API: `cognee.remember()`, `cognee.recall()`, `cognee.forget()`, `cognee.improve()`（低レベルには `add / cognify / search / memify`）
- グラフ DB: Kuzu（既定）, Neo4j, Neptune, Postgres
- ベクタ DB: LanceDB（既定）, ChromaDB, PGVector, Qdrant, Weaviate, Milvus
- LLM: OpenAI, Anthropic, Gemini, Azure, Bedrock, Ollama, LM Studio, vLLM など litellm 経由で広く対応
- Claude Code / Hermes Agent 向けプラグイン、マルチテナント権限制御、OWL オントロジー連携、Modal 分散実行など周辺機能が厚い

## このリポジトリは何が嬉しいの？（既存手段との比較）

| 観点 | 単純な RAG / LangChain + ベクタ DB | Neo4j + 手書き Cypher | **Cognee** |
|---|---|---|---|
| セットアップ | 自前で埋め込み・チャンク化・検索ロジックを構築 | スキーマ設計と抽出処理を全て自作 | `pip install` + API キーで数行から開始 |
| データ構造 | ベクタのみ（意味的類似だけ） | グラフのみ（意味類似は弱い） | **グラフ＋ベクタ＋リレーショナルを統合** |
| 抽出 | チャンク単位でそのまま保存 | ルール/NER 実装が必要 | LLM + Instructor/BAML でエンティティ・関係を構造化抽出 |
| 検索戦略 | 類似度 Top-K の 1 種類 | Cypher 手書き | GRAPH_COMPLETION / TRIPLET / RAG / TEMPORAL / CYPHER / NL など **15 種類の検索タイプ**を切替・自動ルーティング |
| 進化するメモリ | 追記のみ | 再設計が面倒 | `memify` でルール/要約を付加、フィードバックで自己改善 |
| マルチテナント | 自前実装 | 自前実装 | ユーザ×データセット単位で DB を分離する ACL を標準装備 |
| 運用 | ツールを自分で束ねる | 運用基盤もろもろ自作 | CLI / UI / Cognee Cloud / Modal・Railway・Fly.io への 1-click デプロイ |

要するに「**ベクタ検索だけでは拾えない関係性**」と「**グラフだけでは扱えない意味類似**」の両方を、自前実装なしに得られる。さらにオントロジーによる語彙統制、時系列対応（TEMPORAL 検索）、Claude Code の会話を自動で永続メモリ化するプラグインなど、エージェントの長期記憶として即使える装備が揃っている点が差別化ポイント。

## 使うときの流れ

1. **インストール & 設定**
   ```bash
   uv pip install cognee
   export LLM_API_KEY="sk-..."    # 既定は OpenAI。他プロバイダは .env で切替
   ```
2. **remember（取り込み＝ add + cognify + improve）** ： 任意形式のデータを投入すると、分類 → チャンク化 → LLM でエンティティ/関係抽出 → 要約 → グラフ DB とベクタ DB に格納される。
   ```python
   await cognee.remember("Cognee turns documents into AI memory.")
   await cognee.remember(open("spec.pdf","rb"), dataset_name="my_project")
   ```
3. **recall（検索）** ： 自動ルーティングで最適な検索戦略を選択。用途別に `query_type=` を明示することも可能（GRAPH_COMPLETION / TRIPLET / RAG / TEMPORAL 等）。
   ```python
   results = await cognee.recall("What does the user prefer?", session_id="chat_1")
   ```
4. **improve / memify（育てる）** ： フィードバックやルール抽出で知識グラフを強化し、次回以降の回答精度を継続的に向上。
5. **forget（削除）** ： データセット単位で忘却。
6. **運用オプション**
   - `cognee-cli -ui` でローカル UI、`cognee.serve(url=...)` で Cognee Cloud に切替
   - Claude Code / Hermes Agent にプラグイン接続すれば、セッションを跨いだ永続メモリに
   - 大規模・本番では Postgres + PGVector + Neo4j に差し替え、Modal/Fly.io/Railway へデプロイ

典型パターンは **「remember でデータを育て続け → recall で文脈注入 → improve で品質向上」** という 3 ステップループで、これをエージェント側から呼ぶだけで長期記憶を持つ AI を構築できる。
