---
url: https://github.com/openai/openai-agents-python
keywords: OpenAI, Agents SDK, multi-agent, Python, LLM, tools, handoffs, guardrails, tracing, sandbox
oneliner: OpenAI 公式の軽量マルチエージェントフレームワーク。Agent／Tool／Handoff／Guardrail といった最小限の抽象で複雑なエージェントワークフローを Python で構築できる。
---

# openai/openai-agents-python 概要

## このリポジトリは何？

**OpenAI Agents SDK（Python 版）** の公式実装。LLM にツール・指示・ガードレール・他エージェントへの引き継ぎ（Handoff）を与え、「マルチエージェントワークフロー」を組むための軽量フレームワーク。

- **言語／配布**: Python 3.10+、PyPI で `openai-agents` として公開。
- **プロバイダ非依存**: OpenAI Responses API・Chat Completions API に加え、LiteLLM 等を介した 100+ LLM に対応。
- **中核の抽象（`src/agents/` 配下）**:
  - `Agent` … instructions / tools / handoffs / guardrails を持つ LLM 定義
  - `Runner` … エージェント実行ループ（同期・非同期・ストリーミング）
  - `tool` / `function_tool` … Python 関数・MCP・ホスト済みツールを統一 I/F でツール化
  - `handoffs` … 別エージェントへの委譲
  - `guardrail` … 入出力の検証・遮断
  - `memory` / `sessions` … 会話履歴の自動管理（Redis・SQLAlchemy オプション）
  - `tracing` … 実行トレースの可視化（OpenAI Traces UI 連携）
  - `sandbox` … v0.14 で追加された「Sandbox Agent」（ファイル操作やコマンド実行を安全な環境で行う長時間タスク向け）
  - `realtime` / `voice` … `gpt-realtime` による音声エージェント
- 豊富な `examples/`（basic, agent_patterns, handoffs, mcp, research_bot, customer_service, realtime, voice, sandbox…）と MkDocs による公式ドキュメント、`tests/` 完備。

## このリポジトリは何が嬉しいの？（類似手段との比較）

| 比較対象 | Agents SDK の優位点 |
|---|---|
| **OpenAI API を直接叩く**（Responses / Chat Completions） | tool calling ループ・JSON スキーマ生成・履歴管理・リトライ・ストリーミングの「定型コード」を肩代わり。Python 関数に `@function_tool` を付けるだけで型・description・引数スキーマを自動生成。 |
| **LangChain / LangGraph** | 抽象が最小（Agent・Tool・Handoff・Guardrail の 4 概念中心）で学習コストが低い。グラフ DSL を強制せず、素の Python + async で書ける。OpenAI Responses API とネイティブ連携し、Tracing UI と直結。 |
| **AutoGen / CrewAI 等のマルチエージェント FW** | 「Agents as tools」「Handoffs」という2方式でマルチエージェントを素直に表現。Guardrail、Human-in-the-loop、Session 永続化、Sandbox 実行が**公式サポート**でバージョン整合が取れる。 |
| **自作の ReAct ループ** | トレーシング／ガードレール／セッション中断・再開（`RunState` スキーマ管理）／MCP／リアルタイム音声まで揃っているため、PoC から本番まで同じ抽象で延ばせる。 |

要するに **「OpenAI 公式が面倒を見る、最小抽象でベンダーロックインの薄いマルチエージェント実装」** が価値。

## 使うときの流れ

1. **インストール**
   ```bash
   pip install openai-agents   # or: uv add openai-agents
   export OPENAI_API_KEY=...
   ```
   音声なら `[voice]`、Redis セッションなら `[redis]` extras。

2. **ツールを定義**（任意）
   ```python
   @function_tool
   def get_weather(city: str) -> Weather: ...
   ```
   Pydantic 型から入出力スキーマが自動生成される。MCP サーバや hosted tool も同じ `tools=[...]` に混ぜられる。

3. **Agent を組み立てる**
   ```python
   agent = Agent(
       name="Assistant",
       instructions="You are a helpful agent.",
       tools=[get_weather],
       handoffs=[other_agent],       # 必要なら他エージェントへ委譲
       input_guardrails=[...],       # 必要なら入力検証
   )
   ```

4. **Runner で実行**
   ```python
   result = await Runner.run(agent, "What's the weather in Tokyo?")
   print(result.final_output)
   ```
   `Runner.run_sync` / `Runner.run_streamed` も選択可能。内部で tool 呼び出し・handoff・ガードレールのループを自動実行。

5. **発展**
   - 複数エージェントを「agents-as-tools」または「handoffs」で連携（`examples/agent_patterns/` に routing / parallelization / llm-as-judge / deterministic 等のレシピあり）。
   - `Session` で履歴永続化、`RunState` 保存で中断・再開、Human-in-the-loop で承認フローを実装。
   - **Sandbox Agent** でリポジトリ操作・ファイル編集など長尺タスクを実行。
   - Tracing UI で会話・ツール呼び出しを可視化し、デバッグ／評価。

6. **開発者として貢献する場合**
   - `make sync` → 実装 → `make format` / `make lint` / `make typecheck` / `make tests`（`CLAUDE.md` の `$code-change-verification` を遵守）→ PR テンプレートで提出。
