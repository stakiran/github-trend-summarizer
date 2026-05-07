---
url: https://github.com/decolua/9router
keywords: AI router, token saver, fallback, OAuth, OpenAI compatible
oneliner: 複数のAIコーディングCLI(Claude Code/Codex/Cursor等)を、無料・サブスク・格安の40+プロバイダにルーティングし、トークン節約と自動フォールバックで「コーディングを止めない」ローカルプロキシ。
---

# 9Router (decolua/9router) 整理メモ

## 1. このリポジトリは何？

**ローカルで動く「AIコーディング向けスマートルータ／プロキシ」**。Next.js 16 + React 19 製のダッシュボード付きで、`http://localhost:20128/v1` に **OpenAI互換のエンドポイント** を立てる。

- CLI 側（Claude Code, Codex, Cursor, Cline, Copilot, Antigravity, OpenClaw, Continue 等）の向き先を 9Router に変えるだけで、内部で **40+ プロバイダ・100+ モデル** を切り替えてくれる。
- 接続先タイプ:
  - **OAuth サブスク系**: Claude Code (Pro/Max), Codex, Copilot, Cursor, Antigravity
  - **無料系**: Kiro AI（Claude 4.5 / GLM-5 / MiniMax 無料無制限）, OpenCode Free（認証不要）, Vertex AI（$300クレジット）
  - **API キー系**: GLM, Kimi, MiniMax, OpenAI, Anthropic, Gemini, DeepSeek, Groq, xAI, Mistral, OpenRouter ほか多数
- 主要機能:
  - **RTK Token Saver**: `git diff` / `grep` / `ls` / `tree` 等の tool_result を圧縮し入力トークンを 20-40% カット（リクエスト単位、形式変換より前段で動作するので全フォーマット対応）。
  - **Caveman Mode**: 出力をぶっきらぼうにして出力トークンを最大65%削減。
  - **3層自動フォールバック**: サブスク → 格安 → 無料 を順番にロールオーバー。
  - **マルチアカウント / ラウンドロビン**, **OAuth 自動更新**, **クォータ可視化**, **OpenAI ↔ Claude ↔ Gemini ↔ Cursor ↔ Kiro ↔ Vertex の双方向フォーマット変換**, **Cloud Sync**, **使用量分析**。
- ストレージは LowDB（`~/.9router/db.json`, `usage.json`）。配信形態は `npm i -g 9router` / ソース起動 / Docker / Cloudflare Workers / VPS。

## 2. 何が嬉しい？既存手段との比較

| 比較対象 | 9Router の差分 |
|---|---|
| **単一プロバイダのCLIをそのまま使う**（例: Claude Code 単体） | クォータ枯渇＝即停止になりがち。9Router は無料/格安に**自動フォールバック**して止まらない。月額サブスクの未使用枠もフルに使い切れる。 |
| **OpenRouter / LiteLLM などの集約プロキシ** | OpenRouter は「課金API集約」が主、9Router は **無料 OAuth プロバイダ（Kiro, OpenCode Free, Vertex）を一級市民として扱える**点が独特。さらに RTK / Caveman による**トークン削減**が組み込み（OpenRouter にはない）。 |
| **自分でフォールバックを書く / aliases で切替** | ダッシュボード上で「コンボ」をGUIで作れて、クォータ・コスト・残時間が見える。CLI 側設定は1個（http://localhost:20128/v1）固定で済む。 |
| **CLI を毎回違うプロバイダに向け直す** | 1つの URL で済むため、Claude Code / Codex / Cursor / Cline / OpenClaw のどれからでも同じ設定。形式変換も内部で吸収。 |
| **クラウド SaaS 型ルータ** | ローカル動作なのでプロンプトが第三者を経由しない。OSS（MIT）でセルフホスト可。「9Router 自体は絶対課金しない」と明記。 |

要するに **「無料/サブスク/格安をまとめて1本のOpenAI互換エンドポイントに束ねる」+「リクエスト本体を圧縮して節約する」** が同居しているのが他に少ない強み。

## 3. 使うときの流れ

1. **インストール／起動**
   - 簡単: `npm install -g 9router && 9router` → ブラウザで `http://localhost:20128` のダッシュボードが開く。
   - ソース起動: `cp .env.example .env && npm install && PORT=20128 npm run dev`（本番は `npm run build && npm run start`）。Docker は `docker build -t 9router . && docker run -d -p 20128:20128 --env-file .env -v 9router-data:/app/data 9router`。
2. **プロバイダ接続**（Dashboard → Providers）
   - 無料で始めるなら **Kiro AI**（OAuth: AWS Builder ID / Google / GitHub）か **OpenCode Free**（認証不要）。
   - 有料サブスクを活用するなら Claude Code / Codex / Copilot / Cursor を OAuth 接続。トークンは自動リフレッシュ。
   - 格安バックアップとして GLM / MiniMax / Kimi の API キー追加。
3. **コンボ（フォールバック列）作成**（Dashboard → Combos）
   - 例: `cc/claude-opus-4-7` → `glm/glm-5.1` → `kr/claude-sonnet-4.5`。クォータ枯渇や失敗で順に降格。
4. **CLI ツール側を 9Router に向ける**
   - 共通: Base URL `http://localhost:20128/v1`、API Key はダッシュボードから発行されたものを貼る、Model はモデルID（例 `cc/claude-opus-4-7`）かコンボ名。
   - Claude Code は `~/.claude/config.json` の `anthropic_api_base` を差し替え。Codex は `OPENAI_BASE_URL` / `OPENAI_API_KEY` env。Cursor / Cline / Continue は OpenAI Compatible 設定。OpenClaw は `~/.openclaw/openclaw.json` で `9router` プロバイダ定義。
5. **運用**
   - RTK はデフォルトON（Endpoint 設定でトグル）。Usage Analytics でトークン・推定コスト・節約量を確認。
   - 公開デプロイ時は `JWT_SECRET` / `INITIAL_PASSWORD` / `API_KEY_SECRET` / `MACHINE_ID_SALT` を必ず変更し、`REQUIRE_API_KEY=true`、`AUTH_COOKIE_SECURE=true` を推奨。Cloud Sync を使う場合は `BASE_URL` / `CLOUD_URL` を指定。

> 端的に言うと、**「ローカルに 1 個のプロキシを立て、CLI を全部そこへ向け、コンボでフォールバックさせる」** のが基本ワークフロー。
