---
url: https://github.com/badlogic/pi-mono
keywords: AI agent, coding agent, unified LLM API, TypeScript, CLI
oneliner: 20以上のLLMプロバイダを統一APIで扱えるコーディングエージェントCLI・TUI/Web UIライブラリ・Slackボットを含むAIエージェントツールキット
---

## pi-mono とは何か

TypeScript 製の **AI エージェント・モノレポ**。以下の 7 パッケージで構成される。

| パッケージ | 役割 |
|---|---|
| **pi-ai** | 20+ プロバイダ（Anthropic / OpenAI / Gemini / Bedrock / Mistral 等）を**統一 API** で扱う LLM ライブラリ |
| **pi-agent-core** | ステートフルなエージェントランタイム（ツール実行・イベント駆動・コンテキスト管理） |
| **pi-coding-agent** | ターミナルで動く**対話型コーディングエージェント CLI**（`pi` コマンド） |
| **pi-tui** | 差分レンダリング方式の軽量ターミナル UI フレームワーク |
| **pi-web-ui** | ブラウザ向けチャット UI の Web Components（mini-lit + Tailwind） |
| **pi-mom** | LLM 搭載の **Slack ボット**（Docker サンドボックス付き） |
| **pi-pods** | vLLM を GPU ポッド（DataCrunch / RunPod / Vast.ai 等）にデプロイする CLI |

---

## 何が嬉しいのか — 既存ツールとの比較

| 比較軸 | Claude Code / Cursor / Aider 等 | pi-mono |
|---|---|---|
| **LLM ロックイン** | 特定プロバイダに依存しがち | 20+ プロバイダを同一 API で切替可能。会話途中でのプロバイダ乗り換え（Cross-Provider Handoff）もサポート |
| **拡張性** | プラグインや MCP 等の独自プロトコル | **TypeScript 拡張 + Skills（CLIツール）+ プロンプトテンプレート + テーマ**を npm/git で配布可能。ツール追加・コマンド追加・UI 差し替えまで可能 |
| **統合モード** | 主に対話 UI のみ | 対話 TUI / ワンショット出力（`-p`） / JSON イベントストリーム / RPC / SDK の **5 モード**。CI やパイプラインにそのまま組み込める |
| **自前デプロイ** | クラウド API 前提 | `pi-pods` で vLLM を GPU ポッドに自動セットアップ。OSS モデルを自前運用できる |
| **Slack 連携** | 別途構築が必要 | `pi-mom` で Slack ボットが即座に立ち上がり、bash 実行・ファイル操作・スケジュール実行まで可能 |
| **Web UI** | 提供なし or 独自 | `pi-web-ui` でブラウザ向けチャット UI をコンポーネントとして埋め込める |
| **設計思想** | 機能を組込みで増やす | **コアを最小に保ち、拡張で増やす**。MCP 不採用（代わりに Skills）、サブエージェント不採用（代わりに拡張）など、シンプルさ重視 |

**一言で言えば**：プロバイダ非依存・高拡張性・マルチ配信形態（CLI/Web/Slack）を 1 つのモノレポで実現している点が差別化ポイント。

---

## 使うときの流れ

### 1. コーディングエージェント CLI として使う（最も基本的なユースケース）

```bash
# インストール
npm install -g @mariozechner/pi-coding-agent

# プロバイダの認証（OAuth or 環境変数）
pi /login            # ブラウザで OAuth ログイン
# または
export ANTHROPIC_API_KEY=sk-ant-...

# 対話モードで起動
pi

# ワンショットで質問
pi -p "このコードのバグを見つけて"

# モデル・思考レベルを指定
pi --provider anthropic --model claude-sonnet-4 --thinking high "設計を考えて"

# セッション復帰
pi -c                # 直前のセッション継続
pi -r                # セッション一覧から選択
```

### 2. プロジェクトにカスタマイズを入れる

```
my-project/
├── .pi/
│   ├── settings.json        # プロジェクト固有設定
│   ├── extensions/          # カスタムツール（TypeScript）
│   ├── skills/              # CLI ツール（SKILL.md 付き）
│   └── prompts/             # 再利用プロンプトテンプレート
├── AGENTS.md                # プロジェクト指示書（自動読み込み）
└── ...
```

### 3. ライブラリとして組み込む

```typescript
// pi-ai: 統一 LLM API を自分のアプリで使う
import { getModel, streamSimple } from "@mariozechner/pi-ai";

const model = getModel("anthropic", "claude-sonnet-4-20250514");
const stream = streamSimple(model, messages, { reasoning: "medium" });
for await (const event of stream) { /* text / tool_call / thinking */ }

// pi-agent-core: エージェントランタイムを組み込む
import { Agent } from "@mariozechner/pi-agent-core";
```

### 4. Slack ボット / GPU ポッド運用（応用）

```bash
# Slack ボット起動
mom --sandbox=docker:mom-sandbox ./data

# GPU ポッドに vLLM デプロイ
pi pods setup dc1 "ssh root@..." --models-path /models
pi start Qwen/Qwen2.5-Coder-32B-Instruct --name qwen
pi agent qwen -i   # デプロイしたモデルで対話
```
