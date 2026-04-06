---
url: https://github.com/ollama/ollama
keywords: LLM, ローカル推論, モデル管理, REST API, llama.cpp
oneliner: 大規模言語モデル（LLM）をローカル環境で手軽にダウンロード・実行・管理するためのオールインワンツール。
---

## Ollama — ローカル LLM 実行基盤

### これは何？

Ollama は、**大規模言語モデル（LLM）をローカルマシン上で簡単に動かすためのランタイム＋CLI＋APIサーバー**。内部的には llama.cpp をバックエンドに持ち、モデルのダウンロード・ロード・推論・管理をワンストップで提供する。Go で書かれており、macOS / Linux / Windows / Docker に対応。NVIDIA CUDA・AMD ROCm・Apple Metal による GPU アクセラレーションを自動検出する。

### 何が嬉しいのか？（既存手段との比較）

| 観点 | llama.cpp 直接利用 | vLLM / TGI 等 | **Ollama** |
|---|---|---|---|
| **セットアップ** | ビルド・モデル変換が必要 | Docker + GPU 設定が煩雑 | `ollama run llama3` の1コマンド |
| **モデル管理** | 手動でファイル配置 | 手動 or HuggingFace Hub | `pull/push/list/delete` で Docker 風に管理 |
| **GPU 割り当て** | 手動パラメータ指定 | 設定ファイルで指定 | 自動検出・自動割り当て |
| **API** | なし（CLI のみ） | OpenAI 互換 API | REST API（`localhost:11434`）＋ OpenAI 互換 ＋ Anthropic 互換 |
| **マルチモデル同時稼働** | 不可 | 可能だが設定が重い | スケジューラが自動でロード/アンロードを管理 |
| **対象ユーザー** | 開発者・研究者 | 本番サービス向け | **個人〜チームの日常利用に最適** |

要するに「**Docker が "コンテナを誰でも動かせる" にしたこと**」を、LLM に対してやっているのが Ollama。モデルの取得から実行まで、インフラ知識をほぼ要求しない。

### 使うときの流れ

```
1. インストール
   $ curl -fsSL https://ollama.com/install.sh | sh   # Linux
   # macOS: Homebrew or DMG / Windows: EXE インストーラ

2. モデルを取得して対話
   $ ollama run qwen3          # pull + 対話が一発で始まる
   >>> こんにちは！何でも聞いてください。

3. API サーバーとして使う（デフォルトで常時起動）
   $ curl http://localhost:11434/api/chat -d '{
       "model": "qwen3",
       "messages": [{"role":"user","content":"Goの並行処理を説明して"}]
     }'

4. モデル管理
   $ ollama list               # ローカルのモデル一覧
   $ ollama pull gemma3        # 新しいモデルを追加
   $ ollama rm mistral         # 不要なモデルを削除

5. カスタムモデル作成（Modelfile）
   FROM qwen3
   SYSTEM "あなたは日本語専門のアシスタントです"
   $ ollama create my-model -f Modelfile

6. 外部ツールとの連携
   - Claude Code / VS Code / Cline 等とワンコマンドで統合
   $ ollama launch claude
```

**ポイント**: サーバーはバックグラウンドで常駐し、モデルは使用後も一定時間メモリに保持される（keep_alive）。複数モデルの同時ロード・自動アンロードをスケジューラが管理するため、ユーザーはリソース管理を意識する必要がない。
