---
url: https://github.com/vercel-labs/open-agents
keywords: AI-agent, cloud-sandbox, Vercel, autonomous-coding, open-source-template
oneliner: Vercel上でバックグラウンド動作するAIコーディングエージェントを構築するためのオープンソーステンプレート。
---

## Open Agents — 概要整理

### これは何？

**クラウド上で自律的に動く AI コーディングエージェント**を構築するためのフルスタック・テンプレートリポジトリ。Vercel Labs が公開している。  
ユーザーがチャットで指示を出すと、クラウド上のサンドボックス VM 内でコードの読み書き・ビルド・Git 操作などを AI が自律的に実行し、最終的にコミットや PR の作成まで行える。

アーキテクチャは 3 層構造：

| 層 | パッケージ | 役割 |
|---|---|---|
| **Web UI** | `apps/web` (Next.js) | チャット UI、認証、セッション管理、ワークフロー起動 |
| **Agent** | `packages/agent` | LLM 呼び出し＋ツールループによるオーケストレーション（Claude Opus 4.6 がデフォルト） |
| **Sandbox** | `packages/sandbox` | 隔離された VM（Vercel Sandbox）でのファイル操作・シェル実行 |

重要な設計判断として、**Agent は Sandbox の外で動く**。これにより VM のハイバネーション／再開と Agent の状態管理を分離し、耐久性のあるマルチステップ実行を実現している。

---

### 何が嬉しいの？（既存手段との比較）

| 比較軸 | Cursor / GitHub Copilot Workspace | Devin / OpenHands (OSS) | **Open Agents** |
|---|---|---|---|
| **実行環境** | ローカル or SaaS | クラウドVM (SaaS) | クラウドVM (セルフホスト可) |
| **ソースコード** | クローズド | 部分的にOSS | **完全OSS・テンプレート** |
| **カスタマイズ性** | プラグイン程度 | フォーク前提 | **ツール・スキル・サブエージェントを自由に追加** |
| **デプロイ先** | SaaSのみ | 自前構築 | **Vercelにワンクリック＋Neonで自動DB分離** |
| **耐久性** | セッション依存 | 独自実装 | **Vercel Workflow で永続化済み** |

つまり **「プロダクション品質の AI エージェントを自分のインフラで動かしたいが、ゼロから作りたくない」** というニーズに応える。  
ツール定義（`read`, `write`, `edit`, `grep`, `bash` 等）やスキルシステム（Markdown で定義）が最初から揃っており、サブエージェント（Explorer, Executor, Design）のパターンも実装済み。Vercel + Neon のプレビュー環境では DB ブランチが自動分離されるため、本番を壊さずに安全に試行錯誤できる。

---

### 使うときの流れ

```
1. セットアップ
   ├─ リポジトリをクローン
   ├─ 環境変数を設定（POSTGRES_URL, JWE_SECRET, Vercel OAuth, GitHub App 等）
   ├─ bun install → bun run web で起動
   └─ GitHub App を作成し、Webhook・OAuth を接続

2. セッション開始
   ├─ Web UI にログイン（Vercel OAuth）
   ├─ GitHub リポジトリを選択してセッションを作成
   └─ サンドボックス VM が自動でプロビジョニングされる

3. エージェントと対話
   ├─ チャットで自然言語の指示を送信
   ├─ Vercel Workflow が起動し、Agent がツールループを実行
   │   └─ read/write/edit/grep/bash 等のツールをサンドボックス内で駆使
   ├─ リアルタイムでストリーミング表示（差分ビュー・ファイルツリーも確認可能）
   └─ 必要に応じてサブエージェント（Explorer で調査、Executor で実装）に委譲

4. 成果物の反映
   ├─ auto-commit：ターン終了時に自動コミット
   ├─ auto-PR：変更をまとめて PR を自動作成
   └─ サンドボックスのプレビューポート（3000, 5173 等）で動作確認も可能

5. カスタマイズ（発展）
   ├─ packages/agent/tools/ に独自ツールを追加
   ├─ SKILL.md 形式で独自スキルを定義
   └─ subagents/ に専門エージェントを追加
```
