---
url: https://github.com/ggml-org/llama.cpp
keywords: LLM, inference, C++, quantization, edge-deployment
oneliner: C/C++で実装された軽量・高速なLLM推論エンジンで、量子化によりコンシューマ向けハードウェアでも大規模言語モデルを動かせる。
---

## llama.cpp 概要

### このリポジトリは何？

C/C++ で書かれた **LLM（大規模言語モデル）の推論エンジン**。LLaMA, Mistral, Qwen, Phi, Gemma など **70以上のモデルアーキテクチャ**に対応し、CPU・GPU を問わず幅広いハードウェア上で LLM を実行できる。独自フォーマット **GGUF** でモデルを管理し、1.5〜8bit の多段階量子化に対応している。OpenAI互換の REST API サーバーも同梱されており、ローカル環境で ChatGPT ライクなサービスを構築できる。

---

### 何が嬉しいのか？（既存手段との比較）

| 観点 | llama.cpp | PyTorch / HuggingFace Transformers | vLLM / TGI (サーバー型) |
|---|---|---|---|
| **依存関係** | ほぼゼロ（C/C++のみ） | Python + CUDA + 大量ライブラリ | Python + CUDA 必須 |
| **最小動作環境** | CPU のみの PC やスマホでも可 | GPU (VRAM 大) がほぼ必須 | サーバーグレード GPU 前提 |
| **量子化** | 1.5〜8bit を標準搭載、CLI 一発 | 外部ツール (GPTQ 等) が必要 | 限定的 |
| **セットアップ** | cmake → build → 実行 (3ステップ) | 仮想環境構築 + pip 大量インストール | Docker + GPU ドライバ設定 |
| **対応プラットフォーム** | Windows/macOS/Linux/Android/iOS/WASM | 主に Linux + CUDA | Linux + CUDA |
| **GPU加速** | CUDA, Metal, Vulkan, HIP 等を選択可 | CUDA 中心 | CUDA 中心 |

**一言で言えば**：Python 環境や高価な GPU がなくても、手元の PC・スマホで LLM を動かせる唯一の現実的な選択肢。7B パラメータモデルを 4bit 量子化すれば、**RAM 4〜6GB 程度**で推論できる。

---

### 使うときの流れ

```
① モデル入手 ─→ ② (必要なら)変換 ─→ ③ ビルド ─→ ④ 実行
```

**① モデルを入手する**
- Hugging Face 等から GGUF 形式のモデルをダウンロード（TheBloke 氏の量子化済みモデルが定番）
- 既に HF 形式 (safetensors) を持っている場合は次のステップへ

**② GGUF 形式に変換・量子化する**（GGUF 形式なら不要）
```bash
python convert_hf_to_gguf.py ./my-model/          # HF → GGUF 変換
./build/bin/llama-quantize model.gguf model-Q4_K_M.gguf Q4_K_M  # 量子化
```

**③ ビルドする**
```bash
cmake -B build          # 構成（GPU使用時は -DGGML_CUDA=ON 等を追加）
cmake --build build --config Release
```

**④ 推論を実行する**（用途に合わせて選択）

| 用途 | コマンド例 |
|---|---|
| **対話チャット** | `./build/bin/llama-cli -m model-Q4_K_M.gguf` |
| **API サーバー** | `./build/bin/llama-server -m model-Q4_K_M.gguf --port 8080` |
| **プログラム組込** | `libllama` の C API (`llama.h`) をリンクして自作アプリに統合 |

API サーバーは OpenAI 互換のため、既存の ChatGPT 向けクライアントやライブラリをそのまま `localhost:8080` に向けるだけで利用できる。Python, Go, Rust, Node.js など **20以上の言語バインディング**も公開されている。
