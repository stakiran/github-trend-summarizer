---
url: https://github.com/deepseek-ai/DeepGEMM
keywords: FP8, GEMM, CUDA, MoE, JIT, Tensor Core, Hopper, Blackwell
oneliner: 低精度（FP8/FP4/BF16）GEMM と MoE 関連カーネルを JIT で提供する、簡潔かつ高性能な NVIDIA GPU 向けテンソルコアカーネル集
---

# DeepGEMM 概要まとめ

## このリポジトリは何？

DeepSeek 社が公開する、**NVIDIA SM90 (Hopper) / SM100 (Blackwell) 向け統一テンソルコアカーネルライブラリ**。大規模言語モデル（LLM）の中核演算である

- FP8 / FP4 / BF16 の **GEMM**（`D = C + A @ B`、NT/TN/NN/TT レイアウト）
- **Grouped GEMM**（contiguous / masked、MoE 向けに M 軸や K 軸でグループ化）
- **Mega MoE**：EP dispatch → Linear1(FP8×FP4) → SwiGLU → Linear2 → EP combine を 1 つの巨大カーネルに融合し、NVLink 通信とテンソルコア計算を重ねる
- **MQA Logits**（DeepSeek V3.2 の lightning indexer 用、prefill/decoding 両対応）
- **HyperConnection**、MoE 逆伝播向けの Weight-Gradient カーネル 等

を **1 つの CUDA コードベース**にまとめ、インストール時の CUDA コンパイルを排し、実行時に軽量な C++ JIT モジュール（NVCC / NVRTC）でコンパイルする。CUTLASS / CuTe の概念を参考にしつつも、テンプレート地獄に依存せず、コア関数数を意図的に絞った「読めるカーネル集」に仕立てている点が特徴。

主な構成：`deep_gemm/`（Python API・テスト・MoE ユーティリティ）、`csrc/`（C++/CUDA 実装、JIT、API glue）、`tests/`（BF16・FP8×FP4・attention・Mega MoE・layout 等のテスト）、`third-party/`（CUTLASS, {fmt} サブモジュール）。

## 何が嬉しい？既存の似た手段との比較

| 比較対象 | DeepGEMM の優位点 |
|---|---|
| **CUTLASS / CuTe** | テンプレートや algebra に深入りせず、カーネル本体がシンプルで学習・改造が容易。にもかかわらず H800 で最大 **~1550 TFLOPS** を達成し、専門家チューニング実装に匹敵または上回る。 |
| **cuBLAS / cuBLASLt** | FP8 の **fine-grained scaling**（SM90 は FP32 SF、SM100 は UE8M0 パック SF）を第一級機能として持ち、LLM 特有のブロック量子化にフィット。 |
| **PyTorch 既製 MoE** | MoE 専用の **contiguous / masked grouped GEMM** と、通信計算を融合する **Mega MoE** 一体型カーネルを提供（DeepEP と組み合わせ可）。CUDA Graph / 可変トークン数に対応。 |
| **事前ビルド型カーネル** | 全カーネルを **JIT コンパイル**するため、形状・SM 数・TC 利用率などを実行時に最適化できる。ディスクキャッシュ（`$HOME/.deep_gemm`）、NVRTC 化で最大 10 倍ビルド高速化。 |

また `set_num_sms` / `set_tc_util` / `set_pdl`（Programmatic Dependent Launch）等で細粒度のリソース制御ができ、実用レベルの LLM 推論／学習スタックに組み込みやすい。MIT ライセンス。

## 使うときの流れ

1. **環境準備**：SM90 or SM100 GPU、Python 3.8+、C++20 コンパイラ、CUDA 12.3+（SM90）/ 12.9+（SM100、推奨）、PyTorch 2.1+。
2. **取得**：`git clone --recursive` で CUTLASS・{fmt} のサブモジュールも取る。
3. **インストール**：`./install.sh`（開発時は `./develop.sh` で JIT モジュールをビルド）。
4. **入力準備**：A/B テンソルを指示レイアウト（例：NT なら row-major / col-major）で用意し、**LHS スケールファクタを TMA-aligned かつ転置済み**にしておく（SM100 は UE8M0 パック）。入力転置や FP8 キャストはユーザ側／前段カーネルで実施。必要なら `get_mn_major_tma_aligned_packed_ue8m0_tensor` などのヘルパで整形。
5. **カーネル呼び出し**：用途に応じて Python API を選ぶ。
   - 通常 GEMM：`deep_gemm.fp8_gemm_{nt,nn,tn,tt}` / `bf16_gemm_*`
   - MoE 前向き（prefill/training）：`m_grouped_fp8_gemm_{nt,nn}_contiguous`（各 expert 区間は M ブロック境界にアラインメント）
   - MoE 逆伝播：`k_grouped_fp8_gemm_tn_contiguous`
   - MoE 推論デコード（CUDA Graph）：`m_grouped_fp8_gemm_nt_masked`（マスクで有効部分のみ計算）
   - DeepSeek V3.2 indexer：`fp8_mqa_logits` / `fp8_paged_mqa_logits`
   - Mega MoE：`get_symm_buffer_for_mega_moe` で symmetric memory を確保 → `transform_weights_for_mega_moe` で重み変換 → バッファに入力コピー → `fp8_fp4_mega_moe` を呼ぶ（multi-process 起動・PyTorch 2.9+ 必須）。
6. **チューニング／デバッグ**：`DG_PRINT_CONFIGS` で選択された config 確認、`DG_JIT_USE_NVRTC=1` で高速ビルド、`DG_JIT_DUMP_SASS/PTX` で生成コード確認、`DG_JIT_PTXAS_CHECK` で local memory 使用を assert、`set_tc_util` や `set_num_sms` で占有調整。具体例は `tests/test_core.py` / `test_mega_moe.py` / `test_attention.py` を参照。
