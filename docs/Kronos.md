---
url: https://github.com/shiyu-coder/Kronos
keywords: financial-time-series, foundation-model, candlestick-forecasting
oneliner: 世界45以上の取引所データで事前学習された、金融K線（ローソク足）時系列予測のための基盤モデル
---

## Kronos — 金融市場の"言語"のための基盤モデル

### これは何？

Kronos は **金融市場のK線（ローソク足＝OHLCV）データに特化した時系列予測の基盤モデル**（AAAI 2026 採択）。世界45以上の取引所から収集したデータで事前学習されており、株式・暗号通貨・先物など多様なアセットに適用できる。

アーキテクチャは **2段階構成**：

| ステージ | 役割 | 手法 |
|---|---|---|
| **Tokenizer** | 連続的なOHLCVデータを離散トークンに変換 | Encoder-Decoder Transformer + Binary Spherical Quantization (BSQ) |
| **Predictor** | トークン列から未来のトークンを自己回帰的に生成 | Decoder-only Transformer（RoPE・時間埋め込み付き） |

トークンは **階層構造**（s1: 粗い粒度 → s2: 細かい粒度）で表現され、Predictor は s1 を先に予測してから s2 を条件付きで生成する「粗→精」戦略を取る。モデルサイズは mini (4.1M) ～ large (499.2M) の4種が Hugging Face (`NeoQuasar/`) で公開されている。

---

### 何が嬉しいの？ ― 既存手法との比較

| 観点 | 汎用時系列基盤モデル (TimesFM, Chronos 等) | Kronos |
|---|---|---|
| **対象ドメイン** | 天気・需要予測など汎用 | **金融K線に特化**（ノイズが多く非定常な金融データ向けに設計） |
| **入力形式** | 単変量 or 多変量の数値系列 | **OHLCV＋出来高の構造化されたK線**をネイティブに扱う |
| **トークン化** | パッチ分割やスカラー量子化 | **階層的 BSQ** により粗→精の2段階で情報を圧縮・復元 |
| **時間情報** | 位置埋め込みのみが多い | **分・時・曜日・日・月の明示的な時間埋め込み**で季節性・市場カレンダーを反映 |
| **学習データ** | 公開ベンチマーク中心 | **45以上の取引所**の実市場データで事前学習済み |
| **確率的予測** | モデルによる | Temperature / Top-p サンプリングで**複数の予測パスを生成**し、不確実性を表現 |

要するに、「汎用TSFMを金融に転用する」のではなく、**金融K線のドメイン知識をアーキテクチャ・学習データの両面に組み込んだ初の基盤モデル**という点が最大の差別化ポイント。

---

### 使うときの流れ

#### 1. インストール

```bash
pip install torch>=2.0.0 einops huggingface_hub safetensors pandas numpy matplotlib tqdm
```

#### 2. 推論（予測）— 最短3ステップ

```python
from model import KronosTokenizer, Kronos, KronosPredictor
import pandas as pd

# ① モデルをHugging Faceからロード
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
predictor = KronosPredictor(model, tokenizer, max_context=512)

# ② CSVデータを準備（列: open, high, low, close, volume, amount）
df = pd.read_csv("data/XSHG_5min_600977.csv")
df['timestamps'] = pd.to_datetime(df['timestamps'])
x_df = df.iloc[:400][['open','high','low','close','volume','amount']]

# ③ 予測実行
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=df['timestamps'][:400],
    y_timestamp=df['timestamps'][400:520],
    pred_len=120,
    T=1.0, top_p=0.9, sample_count=1
)
```

`examples/` 配下にバッチ予測・出来高なし予測のサンプルもある。

#### 3. ファインチューン（自前データへの適応）

2つのルートが用意されている：

| 方式 | 対象 | コマンド |
|---|---|---|
| **CSV ベース** (`finetune_csv/`) | 任意のCSVデータ | `python train_sequential.py --config config.yaml` |
| **Qlib ベース** (`finetune/`) | A株市場データ (Qlib経由) | `torchrun ... train_tokenizer.py` → `train_predictor.py` |

いずれも **Tokenizer → Predictor の順に段階的に学習**する。マルチGPU (DDP) 対応。

#### 4. Web UI で可視化

```bash
cd webui && python run.py  # → http://localhost:7070
```

K線チャート上で予測結果と実績を重ねて確認でき、パラメータ（Temperature, Top-p, サンプル数）をインタラクティブに調整可能。
