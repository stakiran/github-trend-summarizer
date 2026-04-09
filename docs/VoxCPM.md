---
url: https://github.com/OpenBMB/VoxCPM
keywords: text-to-speech, tokenizer-free, voice-cloning, multilingual, diffusion-autoregressive
oneliner: トークナイザを使わない直接拡散自己回帰アーキテクチャにより、多言語音声合成・声質デザイン・高忠実度ボイスクローニングを実現する大規模TTSモデル。
---

## VoxCPM2 — Tokenizer-Free 大規模音声合成モデル

### これは何？

OpenBMB が開発した **2B パラメータの Text-to-Speech (TTS) モデル**。最大の特徴は「**Tokenizer-Free**」アーキテクチャで、従来の TTS が音声をいったん離散トークンに変換してから生成するのに対し、VoxCPM2 は **拡散オートレグレッシブ (Direct Diffusion Autoregressive)** 方式で音声波形を直接生成する。200 万時間超の多言語音声データで学習されており、**30 言語 + 中国語 9 方言**に対応する。Apache 2.0 ライセンスで完全オープンソース。

内部構成は 4 モジュールに分かれる：

| モジュール | 役割 |
|---|---|
| **Base LM** (MiniCPM4) | テキスト→意味表現のエンコード |
| **Residual LM** | 音響残差の軽量モデリング |
| **Local Encoder** | 参照音声パッチの特徴量抽出 |
| **Local DiT** | Conditional Flow Matching (CFM) による波形デコード |

出力は **48 kHz スタジオ品質**。リアルタイムストリーミングにも対応し、RTX 4090 で RTF ≈ 0.3 を達成する。

---

### 何が嬉しいのか？（既存手法との比較）

| 観点 | 従来の TTS（VALL-E, XTTS 等） | VoxCPM2 |
|---|---|---|
| **音声トークナイザ** | 必須（離散コード化で情報損失） | **不要** — 拡散で直接生成し量子化劣化を回避 |
| **音質** | 16〜24 kHz が主流 | **48 kHz** 超解像デコーダで高音質 |
| **多言語対応** | 数言語〜十数言語 | **30 言語 + 方言 9 種** を単一モデルでカバー |
| **声の制御方法** | 参照音声のみ | 3 モード（テキスト記述だけで声をデザイン／参照音声でクローン／完全再現） |
| **ファインチューニング** | フル学習が多い | **LoRA 対応**で少量データ・低 VRAM でも追加学習可能 |
| **ライセンス** | 商用不可が多い | **Apache 2.0** で商用利用可 |

特に「**Voice Design**」モード — 参照音声なしで「落ち着いた低音の男性声」のような自然言語指示だけから声を生成できる点は、従来のクローニング中心の TTS にはない独自の強みである。

---

### 使うときの流れ

#### 1. インストール

```bash
pip install voxcpm          # PyPI からインストール
# 依存: torch>=2.5, torchaudio, gradio, funasr 等
```

#### 2. 推論（3 つのモード）

**CLI で使う場合：**

```python
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained("openbmb/VoxCPM2-2B")  # HuggingFace から自動DL

# (A) Voice Design — テキスト指示で声を作る
audio = model.synthesize(text="こんにちは", voice_desc="穏やかな女性の声")

# (B) Controllable Cloning — 参照音声＋スタイル指示でクローン
audio = model.synthesize(text="...", ref_audio="ref.wav", control="明るく速めに")

# (C) Ultimate Cloning — 参照音声＋書き起こしで忠実再現
audio = model.synthesize(text="...", ref_audio="ref.wav", ref_text="書き起こし")
```

**Web UI で使う場合：**

```bash
python app.py   # Gradio UI が起動（3 モードをタブで切替）
```

#### 3. ファインチューニング（自分の声・ドメインに特化）

```bash
# データ準備: JSONL形式 {"audio": "path.wav", "text": "書き起こし", "duration": 3.5}
# LoRA FT（VRAM節約）
python scripts/train_voxcpm_finetune.py --args.load conf/voxcpm_v2/voxcpm_finetune_lora.yaml

# Web UIで学習+推論を一括管理
python lora_ft_webui.py
```

設定は YAML で管理され、LoRA rank・学習率・バッチサイズ等を柔軟に変更できる。学習後のモデルは同じ推論パイプラインにそのまま読み込める。
