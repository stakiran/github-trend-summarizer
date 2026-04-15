---
url: https://github.com/google/magika
keywords: file-type-detection, deep-learning, content-type, onnx, security
oneliner: ディープラーニングでファイルの種類を高速・高精度に判定する Google 製ツール
---

## Magika — AI によるファイル種別検出

### これは何？

Google が開発・公開している**ファイルコンテンツタイプ検出ツール**。約 1 億ファイルで学習した小型の深層学習モデル（ONNX, 約 3 MB）を使い、**200 以上のファイル種別**（コード・文書・画像・音声・実行ファイル等）を識別する。Gmail・Google Drive・Safe Browsing・VirusTotal など Google 内部で実運用されており、週に数千億件のファイルを処理している実績がある。ICSE 2025 で論文発表済み。

### 何が嬉しいのか？ — 既存手法との比較

| 観点 | `file` / libmagic（従来） | **Magika** |
|---|---|---|
| 判定方式 | マジックナンバー＋ルールベースのヒューリスティクス | ディープラーニング（バイト列を直接トークン化） |
| 精度 | テキスト系（Markdown, SQL, YAML 等）で誤判定が多い | **平均精度 ~99%**。テキスト系でも高精度 |
| 速度 | ファイルサイズに依存 | **1 ファイルあたり ~2–5 ms**（CPU）。ファイルサイズにほぼ非依存（先頭・末尾各 1 KB のみ読む） |
| 対応種別 | 数百種（ルール追加が手作業） | 216 種。モデル再学習で拡張可能 |
| 信頼度制御 | なし | 種別ごとに閾値を設定。`HIGH` / `MEDIUM` / `BEST_GUESS` の 3 段階 |
| 依存 | C ライブラリ (libmagic) | ONNX Runtime のみ。ネットワーク不要で完全ローカル動作 |

**要するに**: ルールを手書きせずとも、特にテキスト系ファイルの判定精度が劇的に向上する。モデルが 3 MB と軽量なため、エッジ環境やブラウザ上でも動作可能。

### 使い方の流れ

#### 1. インストール（好みの方法を選択）

```bash
# Python（推奨）
pipx install magika

# macOS / Linux
brew install magika

# Rust
cargo install --locked magika-cli

# ワンライナー
curl -LsSf https://securityresearch.google/magika/install.sh | sh
```

#### 2-A. CLI で使う

```bash
# 単一ファイル
magika report.pdf
# → report.pdf: PDF document (document)

# ディレクトリを再帰的にスキャン
magika -r ./project/

# MIME タイプで出力
magika -i image.webp
# → image.webp: image/webp

# JSON 出力（スクリプト連携向け）
magika --json suspicious_file

# 標準入力から
cat unknown_blob | magika -
```

#### 2-B. Python API で使う

```python
from magika import Magika

m = Magika()

# パス指定
result = m.identify_path("./data.csv")
print(result.output.label)  # "csv"

# バイト列指定
result = m.identify_bytes(b'{"key": "value"}')
print(result.output.label)  # "json"

# バッチ処理（数千ファイルも高速）
results = m.identify_paths(list_of_paths)
```

#### 2-C. JavaScript（ブラウザ / Node.js）で使う

```javascript
import { Magika } from "magika";

const magika = await Magika.create();
const result = await magika.identifyBytes(fileBytes);
console.log(result.label);  // "javascript"
```

#### 3. 出力を活用する

返却される情報には **ラベル**（`python`）、**説明**（`Python source`）、**MIME タイプ**（`text/x-python`）、**グループ**（`code`）、**信頼スコア**（0.0–1.0）が含まれる。セキュリティスキャンのルーティング、アップロードファイルのバリデーション、大量ファイルの自動分類などに直接組み込める。

### 技術スタック概要

- **モデル**: ONNX 形式。ファイルの先頭 1024 バイト＋末尾 1024 バイトをバイト単位でトークン化し推論
- **実装**: CLI は Rust、ライブラリは Python / Rust / JS / Go（WIP）
- **ライセンス**: Apache 2.0
