---
url: https://github.com/microsoft/agent-framework
keywords: AI Agent, Multi-Agent Workflow, Microsoft, LLM Orchestration, Python, .NET
oneliner: AIエージェントとマルチエージェントワークフローの構築・オーケストレーション・デプロイを Python/.NET で行うための Microsoft 製フレームワーク。
---

## これは何？

Microsoft が開発した、**LLM ベースの AI エージェントを構築・連携・運用するためのフレームワーク**。Python と .NET の両方で同等の API を提供する。単一エージェントの構築から、複数エージェントをグラフ構造で連携させるワークフロー、本番デプロイまでを一貫してカバーする。

コア構造はシンプルで、`Agent`（LLM と対話する主体）、`Tool`（エージェントが呼び出す関数）、`Workflow`（複数エージェントの実行グラフ）の 3 層で成り立つ。

## 何が嬉しいのか？（既存手段との比較）

| 観点 | Agent Framework | LangChain / LangGraph | AutoGen | CrewAI |
|---|---|---|---|---|
| **設計思想** | Protocol ベース（duck typing） | 継承ベース | クラス継承 | ロール定義 |
| **言語** | **Python + .NET 両対応** | ほぼ Python | Python | Python |
| **ワークフロー** | Pregel モデル（同期的スーパーステップ） | DAG ベース | 会話ベース | チーム構造 |
| **ミドルウェア** | 3 層（Agent / Chat / Function） | Runnable chain | なし | なし |
| **コンテキスト管理** | 5 種のメッセージ圧縮戦略 | 手動 | なし | なし |
| **評価** | ローカル＋クラウド＋ベンチマーク内蔵 | 外部連携 | 一部 | 限定的 |
| **本番運用** | Azure Functions / Durable Task / A2A 対応 | 限定的 | 限定的 | 限定的 |

**主な差別化ポイント：**

1. **Protocol ベース設計** — フレームワークのクラスを継承しなくても、`run()` メソッドさえ持てばエージェントとして扱える。既存コードへの組み込みが容易。
2. **エンタープライズ向け機能が組み込み** — ツール実行前の承認フロー、チェックポイント／再開、OpenTelemetry による可観測性が最初から用意されている。
3. **.NET との対称性** — C# チームと Python チームが同じ概念モデルで開発できる。
4. **宣言的エージェント定義** — YAML/JSON でエージェントを定義し、コード変更なしに構成を変更可能。

## 使うときの流れ

### Step 1：インストール

```bash
pip install agent-framework[openai]   # OpenAI の場合
pip install agent-framework[foundry]  # Azure AI Foundry の場合
```

### Step 2：チャットクライアント作成（LLM プロバイダーの選択）

```python
from agent_framework.openai import OpenAIChatClient
client = OpenAIChatClient(model="gpt-4o", api_key="...")
```

OpenAI / Azure OpenAI / Anthropic / Bedrock / Ollama など多数対応。

### Step 3：エージェント定義（ツール付き）

```python
from agent_framework import Agent, tool

@tool
def get_weather(location: str) -> str:
    return f"{location}は晴れです"

agent = Agent(
    client=client,
    name="WeatherBot",
    instructions="天気について答えるアシスタントです。",
    tools=[get_weather],
)
```

### Step 4：実行

```python
result = await agent.run("東京の天気は？")
print(result.text)  # → "東京は晴れです"
```

ストリーミングも `stream=True` で対応。

### Step 5：複数エージェントの連携（必要に応じて）

```python
from agent_framework import WorkflowBuilder

workflow = (
    WorkflowBuilder(start_executor=research_agent)
    .add_edge(research_agent, editor_agent)
    .build()
)
result = await workflow.run("AIの最新動向をまとめて")
```

エージェント同士を**グラフのエッジ**でつなぎ、条件分岐・ファンアウト・ヒューマンインザループも可能。

### Step 6：本番デプロイ（必要に応じて）

Azure Functions、Durable Task Framework、A2A（Agent-to-Agent）プロトコルなどでホスティング。評価フレームワークで品質を担保しつつ運用に乗せる。

---

**まとめ：** 「LLM エージェントを PoC で終わらせず本番に持っていく」ことを強く意識した設計。LangChain が"何でもできる汎用ツールキット"なのに対し、本フレームワークは**プロトコル準拠・ミドルウェア・可観測性・承認フロー**といったエンタープライズ要件を構造的に組み込んでいる点が最大の特徴。
