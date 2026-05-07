---
url: https://github.com/z-lab/dflash
keywords: speculative-decoding, block-diffusion, LLM-inference, draft-model, vLLM, SGLang
oneliner: ブロック拡散モデルを用いて LLM の投機的デコーディング（Speculative Decoding）を高速化する軽量ドラフトモデル「DFlash」の公式実装。
---

# DFlash: Block Diffusion for Flash Speculative Decoding

## 1. このリポジトリは何？

**DFlash** は、大規模言語モデル（LLM）の推論を高速化するための **Speculative Decoding（投機的デコーディング）用の軽量「ドラフトモデル」** とその実装パッケージです。Z-Lab が公開する論文 *DFlash: Block Diffusion for Flash Speculative Decoding*（Chen, Liang, Liu, 2026, arXiv:2602.06036）の公式コードに該当します。

特徴は、ドラフトモデルとして従来一般的な「自己回帰型の小型モデル（EAGLE 系など）」ではなく、**Block Diffusion（ブロック拡散）モデル** を採用している点です。マスクトークンで埋めたブロックを並列に「拡散」的に生成（埋め直し）してドラフトトークン列を作り、それをターゲットモデルに検証させる構造になっています（`dflash/model.py` の `dflash_generate`、`build_target_layer_ids`、`extract_context_feature` 等）。

提供物は次の 3 点に整理できます。

- **ドラフトモデル本体**：Hugging Face 上に Qwen3 / Qwen3.5 / Qwen3-Coder / gpt-oss / Llama-3.1 / Kimi-K2.5 など多数のターゲット LLM 用の DFlash 重みを配布（README の対応表）。
- **推論バックエンド統合**：vLLM、SGLang、Hugging Face Transformers、MLX（Apple Silicon）の 4 系統で利用可能（`pyproject.toml` の optional-dependencies）。
- **ベンチマーク CLI**：`python -m dflash.benchmark` で gsm8k / math500 / humaneval / mbpp / mt-bench を共通条件で計測（`dflash/benchmark.py`）。

## 2. このリポジトリは何が嬉しいの？（既存手段との比較）

LLM 推論を速くする既存手段と並べると、ポジショニングが明確になります。

| 手段 | アプローチ | DFlash との関係 |
|---|---|---|
| 通常の自己回帰生成 | 1 トークンずつ逐次デコード | 比較対象（最も遅い） |
| 量子化 / KV キャッシュ最適化 | 1 トークンの計算コストを下げる | 直交。DFlash と併用可能 |
| Medusa / EAGLE / EAGLE-3 系ドラフト | 小型「自己回帰」ドラフトモデルで先読み | DFlash の主な競合 |
| **DFlash（本リポジトリ）** | **Block Diffusion による並列ドラフト生成** | 1 ステップで複数トークンを並列に下書き |

嬉しい点は次の通りです。

- **並列ドラフトでドラフト生成自体が速い**：自己回帰ドラフトはトークンを 1 つずつ書くため、ドラフト長を伸ばすほど線形に重くなる。DFlash はブロック単位で並列に書き直すため、1 回の forward で複数トークン分のドラフトを得られ、Speculative Decoding のボトルネックだった「ドラフト側のレイテンシ」が縮む。
- **対応モデルと対応バックエンドが広い**：vLLM・SGLang・Transformers・MLX を 1 リポジトリでカバーし、`vllm serve` の `--speculative-config '{"method": "dflash", ...}'` のような **既存サービング方式の差し替えだけで導入可能**。EAGLE 等と同列の選択肢として呼び出せる。
- **Apple Silicon もサポート**：`mlx` 経由で M5 Pro 等のローカル環境でも block_size 指定の `stream_generate` が使え、サーバ GPU 以外でも恩恵を受けられる。
- **再現性ある評価**：共通データセット・共通 CLI でドラフトの**受理率**やスループットを測れるため、EAGLE 等との横並び比較が現実的。

## 3. 使うときの流れ

典型的な利用ステップは 4 段階です。

1. **インストール**（バックエンドごとに別 venv 推奨）
   - Transformers: `uv pip install -e ".[transformers]"`
   - SGLang: `uv pip install -e ".[sglang]"`
   - vLLM: `uv pip install -e ".[vllm]"` の後に nightly vLLM を追加インストール
   - MLX: `pip install -e ".[mlx]"`

2. **ターゲット LLM と対応する DFlash ドラフトを選ぶ**
   README の対応表から、利用したい本体（例: `Qwen/Qwen3.5-27B`）に対応するドラフト（例: `z-lab/Qwen3.5-27B-DFlash`）を選択。

3. **サーバ起動 or 直接生成**
   - **vLLM**: `vllm serve <target> --speculative-config '{"method": "dflash", "model": "<draft>", "num_speculative_tokens": 15}' ...`
   - **SGLang**: `python -m sglang.launch_server --speculative-algorithm DFLASH --speculative-draft-model-path <draft> --speculative-num-draft-tokens 16 ...`
   - **Transformers**: `AutoModel.from_pretrained(<draft>, trust_remote_code=True)` の `draft.spec_generate(..., target=target)` を呼ぶ
   - **MLX**: `dflash.model_mlx.load` / `load_draft` を読み、`stream_generate(model, draft, tokenizer, prompt, block_size=16, ...)` でストリーム取得

4. **評価**
   `python -m dflash.benchmark --backend {vllm|sglang|transformers|mlx} --model <target> [--draft-model <draft>] --dataset gsm8k --num-prompts 128` で gsm8k / math500 / humaneval / mbpp / mt-bench を回し、スループットや受理率を比較。データセットは初回実行時に `cache/` 配下に JSONL でキャッシュされる。

要するに **「ターゲット LLM はそのまま、ドラフトを DFlash に差し替えるだけ」** で速度向上を狙える、Speculative Decoding のドラフト側コンポーネント、というのがこのリポジトリの位置づけです。
