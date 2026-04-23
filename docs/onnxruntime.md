---
url: https://github.com/microsoft/onnxruntime
keywords: ONNX, 推論エンジン, 機械学習, クロスプラットフォーム, Execution Provider, ハードウェアアクセラレーション, モデル最適化, C++, Python, エッジ推論
oneliner: ONNX形式のMLモデルを多様なハードウェア上で高速に推論・学習させるためのクロスプラットフォーム・マルチ言語対応のランタイム。
---

# microsoft/onnxruntime 調査メモ

## このリポジトリは何？

Microsoftが中心となって開発している **ONNX Runtime (ORT)**、すなわち「ONNX 形式で表現された機械学習モデルを本番環境で動かすための、クロスプラットフォーム・高性能な推論／学習エンジン」である。

- 主要言語は C++（`onnxruntime/core` 配下にグラフ最適化、カーネル実装、セッション管理などのコア実装）。
- 以下の **多数の言語バインディング** を同梱：`include/` (C/C++)、`python/`、`csharp/`、`java/`、`js/`（Node.js & Web/WASM）、`objectivec/`、`rust/`、`winml/`。
- 各種ハードウェア向けの **Execution Provider (EP)** を `onnxruntime/core/providers/` に多数持つ：`cpu`, `cuda`, `dml`(DirectML), `coreml`, `tensorrt`, `nv_tensorrt_rtx`, `openvino`, `qnn`(Qualcomm), `nnapi`(Android), `webgpu`, `webnn`, `xnnpack`, `dnnl`, `migraphx`, `cann`(Huawei), `acl`(Arm), `vitisai`(AMD/Xilinx), `snpe`, `azure` など。
- 学習向けコード `orttraining/` も存在し、PyTorch 既存スクリプトへ1行追加で多ノードGPU学習を加速するモジュールが提供される。
- 独自の行列演算ライブラリ `mlas`、量子化ツール `quantization`、ビルド系 `cmake/`, `tools/`, `build.{sh,bat}` などが揃う本格プロダクト。

## 何が嬉しいの？（既存手段との比較）

ML推論を「学習した時のフレームワーク」でそのまま行うと、① フレームワーク依存が残る、② エッジ/モバイル/ブラウザ等に展開しづらい、③ ハード固有の加速を個別実装する必要がある、という課題がある。ONNX Runtime はこれらを一気に解決する。

| 観点 | PyTorch/TF をそのまま使う | TensorRT / CoreML / OpenVINO 単体 | ONNX Runtime |
|---|---|---|---|
| 対応モデル | 各FW固有 | ベンダ固有形式に変換が必要 | **ONNX 共通形式**（PyTorch/TF/Keras/sklearn/LightGBM/XGBoost 等から変換可） |
| 対応HW | GPU中心、最適化は自前 | 特定ベンダのみ | CPU / NVIDIA / AMD / Intel / Apple / Qualcomm / ARM / Web / Android / iOS を **同一API** で切替 |
| 配布サイズ・依存 | 重い（数百MB〜） | 各ベンダSDKが必要 | 軽量ビルド・WASM/モバイル向けスリム構成あり |
| API | Python 中心 | C++ 中心 | **C/C++/C#/Java/Python/JS/ObjC/Rust** を公式提供 |
| 最適化 | 手動 | ベンダ依存 | グラフ最適化＋量子化＋EP選択を自動化 |
| 学習 | フル機能 | 基本不可 | ORTModule で PyTorch 学習を加速 |

要するに「**書いたモデルをどこにでも速く運べる共通レイヤ**」であり、学習FWとデプロイ先HWを疎結合にできる点が既存手段より優れる。ブラウザ(WebGPU/WebAssembly)まで同じAPIで届く点は他にほぼない強み。

## 使うときの流れ

1. **モデルをONNXに変換**
   - PyTorch: `torch.onnx.export(...)`、TF/Keras: `tf2onnx`、sklearn: `skl2onnx` などで `.onnx` を生成。
2. **（任意）最適化・量子化**
   - `onnxruntime/python/tools/` や `onnxruntime.quantization` で graph optimization / INT8量子化 / ORTフォーマット化を実施（モバイル向けには `.ort`）。
3. **ターゲットに合わせたONNX Runtimeを入手**
   - `pip install onnxruntime`（CPU）/ `onnxruntime-gpu` / `onnxruntime-directml` / `onnxruntime-node`・`onnxruntime-web`（JS）/ NuGet・Maven・CocoaPods・crates.io からも取得可能。自前ビルドは `build.sh` / `build.bat` で EP を `--use_cuda` 等で指定。
4. **セッションを作って推論**
   - 典型コード（Python）:
     ```python
     import onnxruntime as ort
     sess = ort.InferenceSession("model.onnx",
         providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
     outputs = sess.run(None, {"input": x})
     ```
   - C++ / C# / Java / JS も `InferenceSession` → `Run` のほぼ同じ流れ。`providers` の並び順がフォールバック順。
5. **（学習の場合）** `from onnxruntime.training import ORTModule; model = ORTModule(model)` で既存 PyTorch 学習ループをそのまま加速。
6. **デプロイ**
   - サーバ: Python/C# サービス、ブラウザ: onnxruntime-web（WASM/WebGPU）、モバイル: onnxruntime-mobile（Android/iOS）、Windows組込: WinML/DirectML、Edge: QNN/NNAPI/CoreML EP など、同じ`.onnx`を使い回して展開する。

補助資料は `docs/`（`OperatorKernels.md`, `C_API_Guidelines.md`, `Memory_Optimizer.md` 等）と `samples/`（`cxx/`, `nodejs/`）、および公式サンプルリポジトリ `onnxruntime-inference-examples` を参照するのが早い。
