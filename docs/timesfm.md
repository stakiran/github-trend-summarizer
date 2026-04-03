---
url: https://github.com/google-research/timesfm
keywords: time-series, forecasting, foundation-model, zero-shot, google-research
oneliner: Google Research が開発した、学習不要（ゼロショット）で任意の時系列を予測できる基盤モデル。
---

## TimesFM（Time Series Foundation Model）概要

### これは何？

Google Research が開発・公開した **時系列予測のための事前学習済み基盤モデル**。大量の多様な時系列データで事前学習されたデコーダ型 Transformer（200M パラメータ）であり、**追加の学習なし（ゼロショット）** で、売上・需要・センサー・気温・エネルギーなど任意の単変量時系列を確率的に予測できる。2024 年 ICML 採択。

---

### 何が嬉しいのか？ ― 既存手法との比較

| 観点 | 従来手法（ARIMA / Prophet / LightGBM 等） | TimesFM |
|---|---|---|
| **準備コスト** | 系列ごとにモデル選定・学習・チューニングが必要 | **ゼロショット**。学習不要で即予測 |
| **汎化性** | ドメインごとに再学習。新系列にはコールドスタート問題 | 多領域で事前学習済み。未知の系列にもそのまま適用可能 |
| **確率的予測** | 手法によっては点予測のみ | 9 分位点（10%〜90%）の予測区間を標準出力 |
| **コンテキスト長** | 限定的（Prophet は長期可だがモデル構造固定） | 最大 **16,384 ステップ** の長大な過去情報を活用 |
| **バッチ処理** | 系列単位の逐次処理が一般的 | 数千系列を一括推論でき、スループットが高い |
| **外部変数** | Prophet・LightGBM 等は対応 | `forecast_with_covariates()` で動的・静的共変量に対応（XReg） |
| **欠損値処理** | 前処理が必要 | 先頭 NaN の除去・中間 NaN の線形補間を自動実行 |

> **一言で言えば**：「どんな時系列でも、学習なしで投げるだけでそこそこ以上の予測が返ってくる」のが最大の利点。PoC や多系列を一括処理する場面で特に威力を発揮する。

---

### 使うときの流れ

```
① インストール → ② モデル読み込み → ③ 設定（compile） → ④ 予測（forecast）
```

#### ① インストール

```bash
pip install timesfm[torch]   # PyTorch バックエンド（推奨）
```

#### ② モデルの読み込み（HuggingFace Hub から自動ダウンロード）

```python
import timesfm

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)
```

#### ③ 推論設定の確定（`compile`）

```python
model.compile(timesfm.ForecastConfig(
    max_context=1024,                    # 使う過去の長さ（最大 16,384）
    max_horizon=256,                     # 予測ステップ数（最大 1,024）
    normalize_inputs=True,               # 入力の正規化（推奨 True）
    use_continuous_quantile_head=True,    # 連続分位点ヘッド
    infer_is_positive=True,              # 入力が正値なら出力も正にクランプ
))
```

#### ④ 予測の実行

```python
import numpy as np

# 複数系列をまとめて渡せる（リストで）
inputs = [np.array([120, 135, 148, 160, ...], dtype=np.float32)]

point, quantiles = model.forecast(horizon=12, inputs=inputs)
# point.shape    → (系列数, 12)        … 中央値予測
# quantiles.shape → (系列数, 12, 10)   … mean + 9分位点
```

#### ⑤ （応用）外部変数を使った予測

```python
point, quantiles = model.forecast_with_covariates(
    inputs=sales_list,
    dynamic_numerical_covariates={"price": price_list},
    dynamic_categorical_covariates={"holiday": holiday_list},
    xreg_mode="xreg + timesfm",
)
```

---

### まとめ

- **最小 3 メソッド**（`from_pretrained` → `compile` → `forecast`）で完結するシンプルな API
- ゼロショットで使えるため、**PoC の立ち上げや大量系列の一括予測**に最適
- 精度を追い込みたい場合は共変量（XReg）やコンフィグ調整で拡張可能
- PyTorch / JAX 両対応、CPU でも動作（GPU 推奨）
