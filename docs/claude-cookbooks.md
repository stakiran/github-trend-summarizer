---
url: https://github.com/anthropics/claude-cookbooks
keywords: Claude API, Jupyter Notebook, レシピ集, エージェント, RAG, ツール連携
oneliner: Anthropic公式が提供する、Claude APIの実践的な使い方を70以上のノートブックで学べるレシピ集。
---

## このリポジトリは何？

Anthropic公式の **Claude API クックブック**。Claude APIを使って何かを作りたい開発者向けに、**70以上のJupyter Notebook** を「レシピ」として提供するリポジトリ。各ノートブックは**一つのテーマを上から下まで実行可能な形で完結**させており、コード・解説・実行結果がすべてセットで含まれている。

カバー範囲は広く、以下のカテゴリに分かれる：

| ディレクトリ | 内容 |
|---|---|
| `capabilities/` | RAG、分類、要約、テキスト→SQL、知識グラフなど基本能力 |
| `tool_use/` | ツール呼び出し、構造化JSON抽出、メモリ管理、コンテキスト圧縮 |
| `multimodal/` | 画像認識、チャート読み取り、文書OCR |
| `patterns/agents/` | エージェントワークフロー（オーケストレータ、評価・最適化ループ） |
| `claude_agent_sdk/` | Agent SDKによるリサーチエージェント、SREエージェント等 |
| `managed_agents/` | Managed Agents APIでコードベース探索、テスト修正、Slack Bot等 |
| `misc/` | バッチ処理、プロンプトキャッシュ、評価構築、モデレーション |
| `third_party/` | Pinecone, LlamaIndex, MongoDB, Deepgram等の外部連携 |
| `extended_thinking/` | 拡張思考（長い推論チェーン）の活用パターン |

## 何が嬉しいの？（既存手段との比較）

| 比較対象 | claude-cookbooks の優位性 |
|---|---|
| **公式APIドキュメント** | ドキュメントは「機能の説明」、クックブックは「実際に動くアプリの作り方」。ドキュメントで概念を理解した後、クックブックでそのまま動かせるコードを手に入れられる。 |
| **OpenAI Cookbook等の他社レシピ** | Claude特有の機能（拡張思考、ツール連携のClaude流作法、Managed Agents、Agent SDK）に最適化されている。Claude APIの癖やベストプラクティスが反映済み。 |
| **個人ブログ・Qiita記事** | Anthropic公式メンテナンスで**モデルID・APIバージョンが常に最新**に保たれる（dated IDを使わないルール等）。断片的な記事と違い、品質チェック（CI/pre-commit/レビュー）が効いている。 |
| **ゼロから自分で試行錯誤** | RAGの再ランキング戦略、プロンプトキャッシュの投機的適用、コンテキスト圧縮など、**試行錯誤の結果得られるノウハウがすでに詰まっている**。車輪の再発明を避けられる。 |

要するに、「Claude APIで○○を作りたい」と思ったときに、**動くコードとセットで最短距離の出発点**を提供してくれるのが最大の価値。

## 使うときの流れ

```
1. やりたいことに近いノートブックを探す
   └─ registry.yaml にタイトル・説明・カテゴリ付きで全ノートブックが一覧化されている

2. 環境をセットアップする
   $ git clone https://github.com/anthropics/claude-cookbooks.git
   $ cd claude-cookbooks
   $ uv sync --all-extras          # 依存パッケージを一括インストール
   $ cp .env.example .env          # .env に ANTHROPIC_API_KEY を記入

3. ノートブックを開いて上から実行する
   $ jupyter notebook capabilities/summarization/summarization.ipynb
   - 各ノートブックは「1テーマ完結・上から下まで実行可能」が原則
   - 出力セルも残されているので、実行前に結果のイメージを把握できる

4. 自分のプロジェクトに転用する
   - コードをコピーして自分のアプリに組み込む
   - モデルIDやプロンプトを自分の用途に合わせて変更する
```

ライセンスはMITなので、商用利用を含めコードの転用は自由。
