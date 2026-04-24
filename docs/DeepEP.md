---
url: https://github.com/deepseek-ai/DeepEP
keywords: MoE, expert-parallel, all-to-all, NVSHMEM, RDMA, NVLink, FP8, low-latency, CUDA, DeepSeek-V3
oneliner: Mixture-of-Experts（MoE）の dispatch / combine を高速化する、GPU 向け expert-parallel 通信ライブラリ。
---

# DeepEP 要約

## 1. このリポジトリは何？

**DeepEP** は、DeepSeek-AI が公開する **Mixture-of-Experts（MoE）／Expert Parallelism 専用の GPU 間通信ライブラリ**。中核は、MoE で必須となる **all-to-all（dispatch / combine）カーネル** を高スループット・低レイテンシで提供することにある。

- 実装は主に CUDA（`csrc/kernels/`）、上位に C++/PyTorch バインディング（`csrc/deep_ep.cpp`）と Python API（`deep_ep/buffer.py` の `Buffer`, `EventOverlap`）。
- 対応: Ampere(SM80)/Hopper(SM90) GPU、CUDA 11/12、PyTorch 2.1+、intranode は NVLink、internode は RDMA (InfiniBand / RoCE)。**NVSHMEM に依存**。
- 提供される2系統のカーネル:
  1. **Normal カーネル**: 学習・推論 prefill 向け。**NVLink ドメイン ⇄ RDMA ドメインの非対称帯域フォワーディング**に最適化（DeepSeek-V3 の group-limited gating と整合）。SM 使用数を制御可能、FP8 dispatch / BF16 combine に対応。
  2. **Low-latency カーネル**: 推論 decode 向けの **pure RDMA** 実装。**SM を消費しない hook ベースの通信-計算オーバーラップ**を提供（double-batch overlap に有効）。

## 2. 何が嬉しい？（既存手段との比較）

| 観点 | NCCL `all_to_all` / PyTorch 既定 | Megatron/FasterMoE などの MoE 実装 | **DeepEP** |
|---|---|---|---|
| MoE 特化 | 汎用集合通信 | MoE 特化だが通信層は NCCL/MPI 依存 | MoE の dispatch/combine に**特化したカーネル** |
| NVLink+RDMA の同時最適化 | 片方ずつ最適（非対称帯域は不得意） | NCCL 経由で非対称帯域を捌けない | **非対称帯域フォワーディングを明示設計**（NVLink 域 →→ RDMA 域を飽和：実測 RDMA ~50 GB/s, NVLink ~158 GB/s） |
| 低レイテンシ推論 | ~数百 μs〜ms オーダ | 同左 | **EP=8 で dispatch 77 μs / combine 114 μs**（H800+CX7 400Gb IB） |
| 通信-計算オーバーラップ | CUDA stream 任せ、SM を食う | kernel 側で SM を占有 | **受信 hook 方式で SM ゼロ占有**オーバーラップ可能 |
| 低精度 | 実装依存 | 多くは BF16/FP16 | **FP8 dispatch を一級対応** |
| SM 制御 | 不可 | 限定的 | `Buffer.set_num_sms` で静的に制御 |

つまり、「NCCL の上に載せた MoE」では取り切れない **非対称帯域・SM 占有・FP8・μs 級 decode** の4点を同時に解決する点が DeepEP の独自価値。論文 DeepSeek-V3 の production を支える実装でもある。

## 3. 使うときの流れ

1. **依存の準備**: CUDA / PyTorch / NVLink / RDMA(IB) を揃え、`third-party/README.md` に従って **NVSHMEM** をビルド。
2. **ビルド & インストール**:
   ```bash
   NVSHMEM_DIR=/path/to/nvshmem python setup.py install
   # 主な env var: DISABLE_SM90_FEATURES, TORCH_CUDA_ARCH_LIST, DISABLE_AGGRESSIVE_PTX_INSTRS
   ```
3. **クラスタ上で自動チューニング**: `tests/test_intranode.py` / `test_internode.py` / `test_low_latency.py` を走らせ、最適な config を取得（default は DeepSeek 社内クラスタ前提）。
4. **アプリに組み込む**（`import deep_ep`）:
   - `Buffer.set_num_sms(n)` で SM 予算を固定。
   - `get_dispatch_config(ep_size)` / `get_combine_config(ep_size)` から NVL/RDMA バッファサイズを算出し、プロセスグループごとに `Buffer` を1つ確保。
   - **学習 / prefill**:
     - forward: `get_dispatch_layout` → `buffer.dispatch(x, topk_idx, topk_weights, ...)` → MoE 計算 → `buffer.combine(y, handle)`
     - backward: dispatch の逆は combine、combine の逆は dispatch を呼ぶだけ（handle を再利用）。
     - `async_finish=True` + `previous_event` / `allocate_on_comm_stream` で計算とオーバーラップ。
   - **推論 decode（low-latency）**:
     - `Buffer(group, 0, rdma_bytes, low_latency_mode=True, num_qps_per_rank=local_experts)` で確保（QP 数 = ローカル expert 数が必須）。
     - `low_latency_dispatch(..., return_recv_hook=True)` が返す `hook()` を実計算の直前に呼ぶことで、**SM を使わない裏側 RDMA 受信**と計算を重ねる。`low_latency_combine` も同様。CUDA Graph 互換。
5. **運用上の注意**: IB の Virtual Lane (`NVSHMEM_IB_SL`) で normal / low-latency / その他のトラフィックを分離。高負荷時のみ adaptive routing を有効化推奨。congestion control は基本オフ。`.nc` PTX を使う積極最適化が効かない環境は `DISABLE_AGGRESSIVE_PTX_INSTRS=1` で回避。
