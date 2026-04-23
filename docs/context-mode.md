---
url: https://github.com/mksglu/context-mode
keywords: MCP, context window, sandbox, AI coding agent, session continuity
oneliner: AIコーディングエージェントのコンテキストウィンドウをサンドボックスとFTS5で守るMCPサーバー。
---

# context-mode リポジトリ整理

## このリポジトリは何？

**context-mode** は、AIコーディングエージェント（Claude Code / Gemini CLI / Cursor / VS Code Copilot 等、計12プラットフォーム対応）の **コンテキストウィンドウ問題を解決するMCPサーバー** です。主言語は TypeScript、ライセンスは Elastic License 2.0。

エージェントが `Playwright スナップショット`, `GitHub issues`, `アクセスログ` 等をツール経由で取得すると、**生データがそのまま会話コンテキストを浪費**します（例：56 KB / 59 KB / 45 KB）。30分で40%が消費され、compact が走ると編集中ファイル・タスク・ユーザの要望まで忘れる。これが解決対象の「コンテキスト問題」です。

核となる3つの機能：

1. **Context Saving**：`ctx_execute` / `ctx_batch_execute` / `ctx_fetch_and_index` 等6つのサンドボックスツールで、生データは分離サブプロセス内で処理し、`stdout` と要約だけを返す（315 KB → 5.4 KB、98%削減）。
2. **Session Continuity**：ファイル編集・git操作・タスク・エラー・ユーザ判断を SQLite に記録。compact 発生時は全部を戻すのではなく、**FTS5 + BM25 + Porter stem + trigram + RRF + Levenshtein** で検索可能化し、`<session_knowledge>` として最小限だけ注入。
3. **Think in Code**：「LLMはデータ処理器ではなく、コード生成器として使う」という方針を12プラットフォームで強制。50ファイルを読み込むのではなく、LLMが書いたスクリプトが集計し `console.log` で答えだけ返す。

## 既存手段と比べた嬉しさ

| 比較対象 | 違い |
|---|---|
| **CLI出力フィルタ（例：`head`, `grep` でエージェントが節約）** | context-mode はMCPプロトコル層でサンドボックス化。**生データがそもそもコンテキストに入らない**ため、うっかり全量が流入する事故が起きない。 |
| **RAG系クラウド（Context7など）** | 完全ローカル。`~/.context-mode/content/` の SQLite のみ。テレメトリ/アカウント/クラウド同期なし。プライバシー重視。 |
| **モデル側のcompact機能** | compactは重要情報（編集中ファイル、ユーザ指示）を失う。context-mode は Priority-tier snapshot（≤2 KB）+ FTS5 indexで**最後のプロンプトとタスク状態を必ず復元**。 |
| **単純なMCPツール追加** | フックで `Bash` / `Read` / `WebFetch` を**プログラム的に横取り・禁止・リダイレクト**（対応プラットフォームで~98%削減、非対応で~60%）。セキュリティポリシー（`Bash(sudo *)` deny等）もサンドボックス内まで一貫適用。 |
| **URL再取得** | 24h TTLキャッシュ + 14日クリーンアップ。`--continue` でindex済みdocsが持続、再フェッチ不要。 |

ベンチ例：Playwright 56 KB→299 B、Git log 153 commits 11.6 KB→107 B、リポ調査 986 KB→62 KB。セッション時間が ~30分 → ~3時間に延びる。

## 使うときの流れ

1. **インストール**：プラットフォームに応じて
   - Claude Code：`/plugin marketplace add mksglu/context-mode` → `/plugin install context-mode@context-mode`（フル自動）
   - その他：`npm install -g context-mode` → 各CLIの設定ファイル（`settings.json` / `mcp.json` / `opencode.json` 等）に MCPサーバとフックを追記
   - フック非対応（Zed / Antigravity）：`AGENTS.md` / `GEMINI.md` を手動コピー
2. **検証**：`/context-mode:ctx-doctor` または `ctx doctor` を実行。ランタイム/フック/FTS5を診断。
3. **通常のプロンプトを書くだけ**：フックが `Bash` / `Read` / `WebFetch` を横取りし、サンドボックスツール（`ctx_batch_execute` 等）に誘導。LLMは「コードを書いて実行→結果だけ取得」を自動で行う。
4. **複数情報源を調べる時**：`ctx_batch_execute` で複数コマンド＋複数クエリを1コールで発行。
5. **ドキュメント参照**：`ctx_fetch_and_index(url)` → `ctx_search(queries)`。WebFetch で生HTMLを流し込まない。
6. **compact／`--continue`**：自動。`PreCompact` がsnapshotを作り、`SessionStart` が Session Guide（Last Request / Tasks / Decisions / Files / Errors / Git 等14項目）を注入。ユーザは再説明不要。
7. **可観測性**：`ctx stats`（削減量）、`ctx insight`（15+メトリクスのローカルWebダッシュボード）、`ctx purge`（全index削除）。

要するに「**インストール→普通に使う→勝手に98%節約＆セッションが生き延びる**」というツールです。
