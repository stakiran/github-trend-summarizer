---
url: https://github.com/HKUDS/DeepTutor
keywords: AI tutoring, multi-agent, RAG, personalized learning, LLM
oneliner: マルチエージェント協調とRAGを活用した、パーソナライズ型AI学習アシスタントプラットフォーム
---

## DeepTutor とは

香港大学 (HKUDS) が開発した**エージェントネイティブなAI個別指導プラットフォーム**。単なるLLMチャットラッパーではなく、複数のAIエージェントが協調して「計画→推論→回答生成」のパイプラインを実行する本格的なマルチエージェントシステム。Python + FastAPI（バックエンド）、Next.js（フロントエンド）で構成され、Web UI / CLI / Docker いずれからも利用できる。

### 5つのコアモード

| モード | 内容 |
|---|---|
| **Chat** | ツール拡張付き対話（RAG・Web検索・コード実行を自律選択） |
| **Deep Solve** | Planner → Solver（ReActループ） → Writer の3エージェント協調で問題を段階的に解く |
| **Quiz Generation** | ナレッジベースに基づいた評価問題を自動生成 |
| **Deep Research** | トピックをサブ課題に分解し、並列リサーチエージェントを投入してレポート化 |
| **Math Animator** | 数学概念を Manim アニメーションに自動変換して視覚化 |

---

## 何が嬉しいのか ― 既存ツールとの比較

| 観点 | 従来のAIチャット（ChatGPT等） | 従来のRAGアプリ（Dify等） | **DeepTutor** |
|---|---|---|---|
| **問題解決の深さ** | 単一LLM応答 | 検索+生成の1段 | Plan→ReAct→Write の**マルチエージェントパイプライン** |
| **学習者への適応** | 会話履歴のみ | なし | **永続的学習者プロファイル**（要約＋学習スタイル）が全機能で共有される |
| **ナレッジベース** | ファイル添付のみ | 静的RAG | LlamaIndex基盤の**増分更新可能なRAG**。複数KBを切り替え可能 |
| **自律エージェント** | なし | ワークフロー定義が必要 | **TutorBot**：独自メモリ・スキル・定期タスク・マルチチャネル（Telegram/Discord/Slack等）を持つ自律エージェント |
| **モード統合** | 単一チャット | 機能ごとにアプリが分離 | 1つのセッション内で5モードをシームレスに切り替え、**コンテキストを共有** |
| **エージェント連携** | ― | ― | CLI がJSON構造化出力に対応し、外部AIエージェントからの**プログラマティック制御**が可能 |

要するに、「教材PDFをアップロードし、自分だけの個別指導AIを立ち上げ、学習が進むにつれてAI側も自分の理解度を学習していく」という体験を、オープンソースかつセルフホストで実現できる点が最大の価値。

---

## 使い方の流れ

### 1. セットアップ（3通り）

```bash
# A) ガイド付きセットアップ（推奨）
git clone https://github.com/HKUDS/DeepTutor.git && cd DeepTutor
conda create -n deeptutor python=3.11 && conda activate deeptutor
python scripts/start_tour.py   # 対話形式でLLM/埋め込み/検索プロバイダを設定

# B) Docker（最速）
cp .env.example .env           # LLM_API_KEY 等を記入
docker compose -f docker-compose.ghcr.yml up -d
# → http://localhost:3782 でアクセス

# C) CLI のみ
pip install -e ".[cli]"
```

### 2. 知識の投入

- **Web UI**：Knowledge Hub から PDF / Markdown をアップロード → 自動でベクトルインデックス化
- **CLI**：`deeptutor kb create physics --doc ch1.pdf --doc ch2.pdf`

### 3. 学習開始

```bash
# Web UI: ブラウザで http://localhost:3782 を開き、チャット開始
# CLI 例:
deeptutor chat                                          # 対話REPL
deeptutor run deep_solve "x^2 - 5x + 6 = 0 を解け" --kb math  # 一発実行
deeptutor run deep_question "量子力学" --config num_questions=5  # クイズ生成
```

### 4. パーソナライズの深化

- 対話を重ねるたびに **Memory Service** が学習者プロファイル（得意分野・学習スタイル・目標）を自動更新
- **TutorBot** を作成すれば、Telegram や Discord 上で常駐し、復習リマインドや定期テストも自律的に実行

### 5. アーキテクチャの要点（開発者向け）

```
ユーザー入力
  ↓
ChatOrchestrator（ルーティング）
  ├─ Level 1: Tools（RAG / Web検索 / コード実行 / 論文検索 等）
  └─ Level 2: Capabilities（Chat / DeepSolve / Quiz / Research / MathAnimator）
        ↓
    StreamBus（非同期イベント配信）→ WebSocket / CLI
```

ツールもCapabilityもプラグイン形式で、`BaseTool` / `BaseCapability` を継承すれば独自拡張が可能。LLMプロバイダは **litellm** 経由で OpenAI / Anthropic / Azure / ローカルモデルを切り替えられる。
