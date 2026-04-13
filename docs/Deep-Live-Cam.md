---
url: https://github.com/hacksider/Deep-Live-Cam
keywords: deepfake, face-swap, real-time, insightface, onnx
oneliner: 1枚の顔画像だけでリアルタイム顔入れ替え・動画ディープフェイクを実現するデスクトップツール
---

## Deep-Live-Cam — 概要整理

### これは何？

**たった1枚の顔写真**を入力するだけで、Webカメラ映像や動画中の顔をリアルタイムに差し替えるデスクトップアプリケーション。内部的には以下のモデルパイプラインで動作する。

| ステージ | 使用モデル/ライブラリ | 役割 |
|---|---|---|
| 顔検出・解析 | InsightFace (Buffalo-L) | 顔の位置・ランドマーク・特徴量の抽出 |
| 顔入れ替え | InSwapper 128 (ONNX) | ソース顔→ターゲット顔のスワップ |
| 顔高画質化 | GFPGAN / GPEN (ONNX) | スワップ後の顔を自然に復元・高解像度化 |
| 後処理 | OpenCV + NumPy | 口マスク保持、色補正、ポアソンブレンド、透過度調整 |

GUI は CustomTkinter 製で、映像処理は FFmpeg パイプによるインメモリ処理。GPU は NVIDIA CUDA / Apple CoreML / DirectML / OpenVINO に対応し、CPU フォールバックもある。

---

### 何が嬉しいのか？（既存手段との比較）

| 観点 | Deep-Live-Cam | 従来ツール (DeepFaceLab, Roop 等) |
|---|---|---|
| **必要な学習データ** | 顔写真 **1枚** で即実行 | 数百〜数千枚の学習画像 + 数時間のモデル学習が必要 |
| **リアルタイム性** | Webカメラ映像を **ライブで** 顔入れ替え可能 | 基本はオフラインのバッチ処理。ライブ対応なし |
| **セットアップの手軽さ** | `pip install` → モデル2つDL → `python run.py` で GUI 起動 | 環境構築が複雑、GPU 前提、学習パイプラインの理解が必要 |
| **複数人対応** | Face Mapping 機能で「誰の顔を誰に」を GUI 上で指定可能 | スクリプト改修や個別モデル学習が必要なことが多い |
| **品質補正** | GFPGAN/GPEN による顔復元、口マスク保持で自然な表情維持 | 別途ポスト処理ツールが必要な場合が多い |

要するに、**「学習不要・1枚で即座にリアルタイム顔スワップ」** という手軽さが最大の差別化ポイント。Roop の後継的な立ち位置で、ライブカメラ対応と UI の洗練が加わっている。

---

### 使い方の流れ

```
1. 環境準備
   ├─ Python 3.11 + FFmpeg をインストール
   ├─ git clone → python -m venv venv → pip install -r requirements.txt
   └─ models/ に inswapper_128_fp16.onnx, GFPGANv1.4.onnx を配置
       (HuggingFace からダウンロード)

2. 起動
   $ python run.py                          # GUI モード
   $ python run.py -s face.jpg -t video.mp4 -o out.mp4  # CLI モード

3-A. 動画モード（バッチ処理）
   ├─ GUI で「ソース顔画像」と「ターゲット動画」を選択
   ├─ オプション調整（顔エンハンサー、口マスク、透過度 等）
   └─ [Start] → 処理完了後に出力ファイル生成

3-B. ライブモード（リアルタイム）
   ├─ GUI で「ソース顔画像」を選択
   ├─ カメラをドロップダウンから選択
   ├─ [Live] → 10〜30秒のモデルロード後、リアルタイム顔スワップ開始
   └─ OBS 等でキャプチャして録画・配信
```

**主要 CLI オプション（抜粋）:**
- `--execution-provider cuda|coreml|directml` — GPU 指定
- `--frame-processor face_swapper face_enhancer` — 処理パイプライン選択
- `--many-faces` — 画面内の全顔を一括スワップ
- `--mouth-mask` — 口元を元映像のまま保持（自然な会話表現用）
- `--nsfw-filter` — 不適切コンテンツのフィルタリング
