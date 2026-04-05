---
url: https://github.com/Blaizzy/mlx-vlm
keywords: MLX, Vision-Language-Model, Apple-Silicon, VLM推論, ファインチューニング
oneliner: Apple Silicon上でVision Language Model（VLM）の推論・微調整をローカル実行するためのPythonパッケージ。
---

## MLX-VLM — Apple Silicon 向け VLM 推論・微調整フレームワーク

### これは何？

Apple の機械学習フレームワーク **MLX** をバックエンドに、**Vision Language Model（VLM）** をMac上でローカル実行するためのPythonパッケージ。画像・動画・音声を理解し、テキストで応答するマルチモーダルモデルを、CLI／Python API／Web UI／OpenAI互換サーバーなど多彩なインターフェースで利用できる。

対応モデルは **57アーキテクチャ** に及び、Qwen2/2.5/3-VL、LLaVA系、Gemma3/4、DeepSeek-VL、Phi-4、Pixtral、InternVL など主要なVLMをほぼ網羅する。推論だけでなく **LoRA/QLoRA によるファインチューニング** にも対応している。

---

### 既存手段と比べて何が嬉しいのか？

| 観点 | MLX-VLM | 既存手段（llama.cpp / vLLM / HF Transformers 等） |
|---|---|---|
| **Apple Silicon 最適化** | MLX のユニファイドメモリを活用し、GPU⇔CPUのコピー不要。M1〜M4 で最高効率 | llama.cpp は Metal 対応だがVLMサポートは限定的。vLLM は NVIDIA GPU 前提 |
| **VLM 特化** | 画像・動画・音声入力をネイティブサポート。57モデル対応 | HF Transformers は汎用だが Mac での量子化推論は手間がかかる |
| **軽量な導入** | `pip install mlx-vlm` 一発。CUDA不要、Docker不要 | vLLM/TGI は Linux + NVIDIA GPU 環境が実質必須 |
| **マルチターン高速化** | Vision Feature Cache（LRUキャッシュ）で2回目以降の画像エンコードをスキップし **11倍以上高速化** | 同等機能を持つ軽量ツールは少ない |
| **KVキャッシュ量子化** | TurboQuant により KVメモリを **76%削減**（128kコンテキスト時） | llama.cpp にも KV量子化はあるがVLMでの統合は限定的 |
| **ファインチューニング** | LoRA/QLoRA による SFT を Mac 上で完結可能 | 通常は Linux + NVIDIA GPU 環境が必要 |

一言でまとめると、**「Mac だけで VLM を本格的に動かせる唯一の実用的選択肢」** というポジション。

---

### 使うときの流れ

#### 1. インストール

```bash
pip install mlx-vlm
```

#### 2-A. CLI でサクッと推論

```bash
# 単発の画像質問
python -m mlx_vlm.generate --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit \
  --prompt "この画像を説明して" --image path/to/image.jpg

# 対話的チャット
python -m mlx_vlm.chat --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit
```

#### 2-B. Python API で組み込み

```python
from mlx_vlm import load, generate

model, processor = load("mlx-community/Qwen2.5-VL-3B-Instruct-4bit")
output = generate(model, processor, "この画像は何？", image="photo.jpg")
```

ストリーミング (`stream_generate`) やバッチ推論 (`batch_generate`) も同じ API 体系で利用可能。

#### 2-C. OpenAI 互換サーバーとして起動

```bash
python -m mlx_vlm.server --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit
```

`/chat/completions` エンドポイントが立ち上がり、既存の OpenAI クライアントからそのまま呼べる。

#### 3. （任意）ファインチューニング

HuggingFace Datasets 形式のデータセットを用意し、LoRA アダプタを学習させる。学習後のアダプタは推論時に `--adapter-path` で指定するだけで適用される。

#### 4. （任意）モデル変換

HuggingFace 上の PyTorch モデルを MLX 形式に変換して利用することも可能。

```bash
python -m mlx_vlm.convert --hf-path <HFモデルパス> -q
```
