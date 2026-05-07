以下、A4 一枚程度に整理した内容です。

---
url: https://github.com/PriorLabs/TabPFN
keywords: tabular, foundation-model, transformer, classification, regression, in-context-learning, scikit-learn, PyTorch
oneliner: 表形式データ向けの「学習済み基盤モデル」で、fit/predict をするだけで XGBoost 等を凌駕する精度を瞬時に出せる Transformer ベースのライブラリ。
---

# TabPFN (PriorLabs/TabPFN) 概要メモ

## 1. このリポジトリは何？

**TabPFN（Tabular Prior-data Fitted Network）** は、Prior Labs が公開している **表形式データ（tabular data）専用の基盤モデル（Foundation Model）** の公式実装。Nature 2025 掲載論文と TabPFN-2.5 テクニカルレポートに基づく。

- **正体**：合成データで事前学習済みの Transformer。`fit()` 時に学習データをそのまま「コンテキスト」として読み込み、`predict()` で推論する **in-context learning 型** の分類・回帰器。
- **API**：scikit-learn 互換の `TabPFNClassifier` / `TabPFNRegressor`。
- **モデル**：デフォルトは TabPFN-2.6（非商用ライセンス）、Apache 2.0 系の TabPFN-2 や TabPFN-2.5 も `ModelVersion` で切替可能。HuggingFace から自動ダウンロード。
- **対象規模**：〜50,000 行・〜2,000 特徴・〜10 クラスが推奨スイートスポット。GPU 推奨（CPU だと小規模のみ）。
- **付随リポ**：`tabpfn-client`（クラウド API）、`tabpfn-extensions`（HPO・SHAP・アンサンブル等）、`tabpfn-time-series`、ノーコード UI `TabPFN UX`。

主な構成: `src/tabpfn/`（`classifier.py`, `regressor.py`, `inference.py`, `finetuning/`, `preprocessing/`, `model/` 等）、`examples/`（分類・回帰・finetune・KV キャッシュ・SageMaker サンプル）、`tests/`。

## 2. 何が嬉しい？既存手段との比較

表形式タスクでは長年 **GBDT（XGBoost / LightGBM / CatBoost）** が王者で、ディープラーニング系（TabNet, FT-Transformer 等）はなかなか勝てなかった。TabPFN はそこを覆す。

| 観点 | GBDT (XGBoost等) | 従来の Tabular DL | **TabPFN** |
|---|---|---|---|
| 学習時間 | 数十秒〜分 | 分〜時間（要 HPO） | **ほぼゼロ秒**（重みは事前学習済み） |
| ハイパラ調整 | 必須 | 必須 | **基本不要**（デフォルトで強い） |
| 小〜中規模での精度 | 強い | 並 | **SOTA**（Nature 論文・TabPFN-2.5 で複数ベンチ更新） |
| 前処理 | 多くの場合スケーリング/エンコーディング要 | 同左 | **不要**（生データ投入推奨、欠損値もそのまま OK） |
| 大規模データ | 数百万行 OK | OK | △（〜10万行が限界、企業版で1000万行） |
| 解釈性・拡張 | 成熟 | 限定的 | extensions で SHAP・Feature Selection・PDP 等を提供 |

要するに **「小〜中規模の表データなら、調整なしで一発で最強クラスの精度が出る」** のが最大の売り。さらに、埋め込み抽出・データ生成・外れ値検知などの **教師なしユースケース** にも転用でき、「表データの GPT 的存在」と位置付けられる。

## 3. 使うときの流れ

### A. 標準ワークフロー（README の Mermaid フローチャートに対応）

1. **インストール**：`pip install tabpfn`（または `uv sync` でローカル開発）。
2. **インフラ判定**：GPU があればローカル TabPFN、無ければクラウド版 `tabpfn-client` を選ぶ。
3. **初回認証**：初回 `fit()` でブラウザが開き PriorLabs にログイン → ライセンス同意。CI 等では `TABPFN_TOKEN` 環境変数で代替。モデル重みも自動ダウンロード（`TABPFN_MODEL_CACHE_DIR` で配置場所変更可、`scripts/download_all_models.py` でオフライン用一括取得）。
4. **基本利用**（sklearn と全く同じ）：
   ```python
   from tabpfn import TabPFNClassifier
   clf = TabPFNClassifier()         # GPU 自動検出
   clf.fit(X_train, y_train)        # スケーリング・OHE は不要
   y_pred = clf.predict(X_test)     # X_test はまとめて投入（バッチ推奨）
   ```
5. **データ特性で分岐**：
   - テキスト列あり → クラウド API 推奨（ネイティブ対応）
   - 時系列 → `tabpfn-time-series`
   - 5万行超 → `ignore_pretraining_limits=True` または Large Datasets Guide
   - クラス数 >10 → `many_class` 拡張
6. **性能を伸ばしたい時**：
   - `examples/finetune_classifier.py` / `finetune_regressor.py` で fine-tuning
   - extensions の **HPO / Post-Hoc Ensemble / AutoTabPFN** を被せる
   - 推論を速くしたいなら `fit_mode='fit_with_cache'` で **KV キャッシュ**有効化
7. **解釈・運用**：extensions で **SHAP / SHAP-IQ / Partial Dependence / Feature Selection**。学習済み推論器は `save_fitted_tabpfn_model` / `load_fitted_tabpfn_model` で永続化。

### B. 注意ポイント（README の Tips）

- `predict` は **必ずまとめて呼ぶ**（毎回トレーニングセットを再計算するため、サンプルごとに呼ぶと約100倍遅い）。テストが大きければ 1000 件ずつチャンク。
- スケーリング・One-Hot などの **前処理はしない**（モデル内部で処理される）。
- 大規模本番運用や 10M 行超は **Enterprise Edition**（蒸留 MLP/Tree、Scaling Mode）が別途用意。
- 匿名テレメトリが既定 ON。`TABPFN_DISABLE_TELEMETRY=1` でオプトアウト可。
