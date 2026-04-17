```markdown
---
url: https://github.com/lukilabs/craft-agents-oss
keywords: AI Agent, Claude Agent SDK, Electron, MCP, Desktop App
oneliner: Claude Agent SDK と Pi SDK を基盤に「ドキュメント中心」で複数エージェントと協働する、オープンソースのエージェントネイティブ・デスクトップアプリ（craft.do 製）。
---

# Craft Agents（lukilabs/craft-agents-oss）まとめ

## 1. このリポジトリは何？

craft.do が開発した **Agent Native なデスクトップ/サーバー型エージェント基盤**。Apache 2.0 OSS。

- **中核**: `@anthropic-ai/claude-agent-sdk`（Claude 系）と **Pi SDK**（Google/OpenAI/Copilot 系）を並列で使える「マルチバックエンド・エージェントランナー」。
- **構成**: Bun + TypeScript のモノレポ。
  - `apps/electron`（React + shadcn/ui の GUI、メイン UX）
  - `apps/cli`（WebSocket で接続する CLI クライアント）
  - `packages/server`（ヘッドレスな RPC/WS サーバー）
  - `packages/shared`（agent, auth, credentials[AES-256-GCM], sessions, sources, statuses）
  - `packages/core`（型定義）
- **主要機能**:
  - マルチセッション Inbox、ステータスワークフロー（Todo→In Progress→Needs Review→Done）、フラグ、ラベル。
  - **Sources**: MCP サーバー（stdio ローカル含む）／REST API（Google・Slack・Microsoft）／ローカル FS・Obsidian・Git を「Source」として workspace に接続。
  - **Skills**（workspace 単位の指示セット、Claude Code からの移行可）、**Automations**（cron／ラベル付与／ツール実行などイベント駆動）、`@mention` で即時参照。
  - **Permission Modes**（Explore / Ask to Edit / Auto、SHIFT+TAB で切替）。
  - Multi-File Diff ビュー、テーマ（App＋Workspace のカスケード）、添付（画像・PDF・Office 自動変換）、ディープリンク（`craftagents://…`）。
  - **Remote Server モード**: Electron をシンクライアントとして `ws/wss` で遠隔サーバーに接続、Docker 対応。

## 2. 何が嬉しい？（既存手段との比較）

| 比較対象 | Craft Agents の差分 |
|---|---|
| **Claude Code / Codex CLI（CLI エージェント）** | CLI でなく「受信箱型 GUI」。複数セッションを並行監視でき、ステータス・フラグ・ラベルで業務管理。Claude Code の skills / MCP を "import" できる移行パスあり。 |
| **Claude Desktop** | MCP だけでなく **REST API や OpenAPI 仕様、Postgres 直結などを Source として扱える**。Anthropic 以外に Google AI Studio・ChatGPT Plus(OAuth)・GitHub Copilot・OpenRouter・Ollama なども同居。 |
| **Cursor / Windsurf などコードエディタ系** | コードより **ドキュメント中心**の UI。craft.do の 32+ ドキュメントツールと統合。「コーディングで拡張」ではなく「プロンプトで拡張」が前提。 |
| **LangGraph / AutoGen など OSS フレームワーク** | フレームワークではなく完成品のアプリ。自分で UI を書く必要なし。Apache 2.0 なので改変可、かつ **Craft Agents 自身で Craft Agents を開発**しているため「プロンプト主導のカスタマイズ」で実用レベル。 |
| **ChatGPT / Claude Web UI** | 権限モード、長時間バックグラウンドタスク、ヘッドレスサーバー、CI から叩ける CLI、TLS 付き WS、自動化、暗号化クレデンシャルなど**運用機能**が揃う。 |

要は「**Claude Code 相当のパワー × デスクトップ GUI × 任意の API/MCP を即接続 × OSS**」というポジション。

## 3. 利用の流れ

1. **インストール**: ワンライナー (`install-app.sh` / `.ps1`) またはソースから `bun install && bun run electron:start`。
2. **API 接続を選択**: Anthropic（APIキー or Claude Max）／Google AI Studio／ChatGPT Plus OAuth／GitHub Copilot OAuth／OpenRouter 等のカスタムエンドポイント。
3. **Workspace 作成**: セッション・Source・Skill・Status・Theme の単位。`~/.craft-agent/workspaces/{id}/` に保存。
4. **Sources を接続**（任意）: 「Linear を source に追加して」と頼めば API/MCP を自動調査・設定。OpenAPI や MCP JSON を貼り付けても可。Google 系だけは自前 OAuth クライアント ID/Secret が必要（README に手順）。
5. **Skills を用意**（任意）: Claude Code から import、または「こういう Skill を作って」と依頼。
6. **セッションを開始**: `Cmd+N`。`@source` `@skill` で Source/Skill を引き込み、SHIFT+TAB で権限モードを切替。必要ならバックグラウンド実行に回して Inbox で管理。
7. **自動化**（任意）: "Every weekday 9am …" と自然言語で伝えるか `automations.json` に `SchedulerTick` / `LabelAdd` 等のトリガを書く。
8. **リモート/ヘッドレス運用**（任意）: VPS で `CRAFT_SERVER_TOKEN=… bun run packages/server/src/index.ts` を起動 → デスクトップを `CRAFT_SERVER_URL=wss://…` で thin client 接続。CI では `craft-cli run "…"` が自己完結でサーバーを起動・実行・終了。
```
