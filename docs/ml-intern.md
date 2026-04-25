---
url: https://github.com/huggingface/ml-intern
keywords: 自律型MLエージェント, Hugging Face, 論文調査, モデル学習, コード生成
oneliner: Claude AIを使って論文調査・モデル訓練・Hubへのデプロイまでをエンドツーエンドで自律実行するMLエンジニアリングアシスタント。
---

# huggingface/ml-intern

## このリポジトリは何？

**ML Intern** は、Claude（LLM）をバックエンドとして動く **自律型MLエンジニアリングエージェント**。ユーザーが「このデータセットでLlamaをfine-tuneして」と一言指示するだけで、論文調査・コード生成・GPU ジョブ投入・HF Hub へのアップロードまでを自律的に実行する。

Hugging Face のエコシステム（Hub・Spaces・Datasets・MCP サーバー・GitHub）への深いアクセス権を持ち、`hf_jobs` ツールで T4〜A100 の GPU を選択してトレーニングジョブを直接サブミットできる点が他のエージェントと一線を画す。

---

## 何が嬉しいの？既存手段との比較

| 観点 | ml-intern | 汎用コーディングエージェント（Copilot等） | MLflow / Kubeflow 等のMLOps基盤 |
|------|-----------|------------------------------------------|--------------------------------|
| 論文調査 | `hf_papers` ツールで自律実行 | なし | なし |
| HF Hub 操作 | 組み込みツールで直接実行 | プロンプト補完のみ | なし |
| GPU ジョブ投入 | `hf_jobs` で T4/A10G/A100 を選択可 | なし | 要インフラ設定 |
| コンテキスト管理 | 170k tokens で自動圧縮・セッション永続化 | 都度リセット | 無関係 |
| 操作単位 | 自然言語1文 | ファイル単位の補完 | YAML定義のワークフロー |

**一番の強み：** 「HFエコシステムに特化した道具立て（16ツール）」と「反復エージェントループ（最大300ステップ）」を組み合わせ、人間が介入せずにML作業を完結できること。`yolo_mode` を有効にすれば承認ダイアログも省略可。

---

## 使うときの流れ

### 1. セットアップ
```bash
git clone git@github.com:huggingface/ml-intern.git
cd ml-intern
uv sync
uv tool install -e .
```

`.env` に3つのトークンを設定する：
```
ANTHROPIC_API_KEY=...   # Claude API
HF_TOKEN=...            # Hugging Face
GITHUB_TOKEN=...        # GitHub
```

### 2. 起動モード

| モード | コマンド | 用途 |
|--------|----------|------|
| 対話型 | `ml-intern` | 会話を続けながら作業 |
| ヘッドレス | `ml-intern "fine-tune llama on my dataset"` | CI/スクリプトから呼び出し |
| モデル指定 | `ml-intern --model anthropic/claude-opus-4-6 "..."` | モデル切替 |

### 3. 内部の実行フロー

```
ユーザー入力
  └→ submission_queue（非同期キュー）
       └→ AgentLoop（Session + ContextManager）
            └→ LLM呼び出し（LiteLLM経由 / AWS Bedrock対応）
                 └→ ツール呼び出しをパース
                      └→ 要確認操作は承認プロンプト表示
                           └→ ToolRouter → 各ツール実行（MCP含む）
                                └→ 結果をコンテキストに追加 → ループ継続
```

### 4. 代表的な自律タスク例
- `"Write a training script for image classification and run it on T4"` → スクリプト生成＋GPU ジョブ投入
- `"Find recent LoRA papers and summarize key ideas"` → `hf_papers` で論文取得・要約
- `"Upload my model to Hub as a private repo"` → `hf_repo_files` + `hf_repo_git` で自動プッシュ

### 5. 設定チューニング
`configs/main_agent_config.json` で挙動を制御：
- `yolo_mode: true` → 全操作を自動承認（CI向け）
- `confirm_cpu_jobs: false` → CPUジョブの承認スキップ
- `save_sessions: true` → HF Hub にセッションを永続化
- `reasoning_effort: "max"` → Claude の思考量を最大化
