---
url: https://github.com/Alishahryar1/free-claude-code
keywords: Claude Code, プロキシ, NVIDIA NIM, OpenRouter, LM Studio, Discord Bot, Anthropic API互換
oneliner: Claude Code の Anthropic API 呼び出しを NVIDIA NIM / OpenRouter / DeepSeek / LM Studio / llama.cpp に透過的にルーティングして、無料または自前ホストで Claude Code を動かすためのプロキシサーバ。
---

# free-claude-code 調査まとめ

## 1. このリポジトリは何？

**Claude Code（公式 CLI / VSCode 拡張 / IntelliJ 拡張）の Anthropic API リクエストを、別の LLM プロバイダに横流しするローカルプロキシサーバ** です。Python 3.14 + FastAPI + uv で実装されており、`uvicorn server:app --port 8082` で起動して、Claude Code 側には `ANTHROPIC_BASE_URL=http://localhost:8082` を指定するだけで接続先がすり替わります。Claude Code 自体には一切手を加えません。

### 主要構成
- `server.py` … FastAPI エントリポイント（`/v1/messages`, `/v1/messages/count_tokens`, `/v1/models` などを Anthropic 互換で公開）
- `api/` … ルート、リクエスト種別判定、トリビアル要求のローカル応答
- `providers/` … `BaseProvider` と `OpenAICompatibleProvider` を基底に、NVIDIA NIM / OpenRouter / DeepSeek / LM Studio / llama.cpp の各プロバイダ実装。`providers/common/` に SSE ビルダ、メッセージ変換、エラーマッピング等を共通化
- `messaging/` … Discord / Telegram ボット（`MessagingPlatform` ABC）で Claude Code を遠隔操作、セッション永続化、ツリー型スレッド
- `cli/` … Claude CLI セッション／プロセス管理
- `config/`, `tests/` … 設定と pytest スイート

### 対応プロバイダ
| Provider | プレフィックス | コスト |
|---|---|---|
| NVIDIA NIM | `nvidia_nim/...` | 無料（40 req/min） |
| OpenRouter | `open_router/...` | 無料モデル多数 / 課金 |
| DeepSeek   | `deepseek/...`   | 従量 |
| LM Studio  | `lmstudio/...`   | ローカル無料 |
| llama.cpp  | `llamacpp/...`   | ローカル無料 |

`MODEL_OPUS` / `MODEL_SONNET` / `MODEL_HAIKU` / `MODEL`（フォールバック）で Opus/Sonnet/Haiku をモデル単位で別プロバイダに振り分け可能。

## 2. 何が嬉しいのか（類似手段との比較）

- **Anthropic 公式課金が不要**：Claude Code は本来 Anthropic API キー＋従量課金が必要だが、NIM の 40 req/min 無料枠や OpenRouter の `:free` モデル、あるいは完全ローカル（LM Studio / llama.cpp）で動かせる。
- **Claude Code 側に改造が不要**：`ANTHROPIC_BASE_URL` と `ANTHROPIC_AUTH_TOKEN` の 2 つの環境変数を差し替えるだけ。CLI・VSCode 拡張・IntelliJ ACP・Cursor 等もそのまま使える。
- **類似案と比較しての独自性**：
  - *Aider / Continue / Cline* など別クライアントを入れる流派と違い、**Claude Code そのものの UX** を保てる。
  - *litellm* のような汎用プロキシと比べ、**Claude Code 固有の挙動に特化**：
    - トリビアル要求（quota probe / タイトル生成 / prefix 検出 / サジェスト / filepath 抽出）の 5 カテゴリをローカルで即応答し、プロバイダのクォータを節約
    - `<think>` タグや `reasoning_content` を Claude の native thinking ブロックに変換
    - ツール呼び出しをテキストで返すモデル向けのヒューリスティック tool-use パーサ
    - Task ツール傍受による subagent の `run_in_background=False` 強制
    - 予防的 rolling-window スロットル＋429 指数バックオフ＋同時実行上限
- **Discord / Telegram ボット同梱**：Claude Code を遠隔で自律コーディング実行。音声メモは Whisper（ローカル or NIM gRPC）で文字起こし。ツリー型会話で分岐、`/stop` `/clear` `/stats` 等のコマンドあり。既存の OSS では珍しい組み合わせ。
- **`claude-pick`（fzf 連携）** でモデルを起動時に対話選択。

## 3. 使うときの流れ

### A. ローカルで Claude Code を無料化するだけの最小ルート
1. `uv` をインストール（`pip install uv`）。Claude Code 本体もインストール。
2. `git clone` → `cd free-claude-code` → `cp .env.example .env`。  
   または `uv tool install git+.../free-claude-code.git` → `fcc-init` で `~/.config/free-claude-code/.env` を生成。
3. `.env` にプロバイダの API キー（例：`NVIDIA_NIM_API_KEY=...`）と `MODEL_OPUS` / `MODEL_SONNET` / `MODEL_HAIKU` / `MODEL`（`provider_prefix/model/name` 形式）、必要なら `ENABLE_THINKING` と `ANTHROPIC_AUTH_TOKEN` を設定。
4. プロキシ起動：  
   `uv run uvicorn server:app --host 0.0.0.0 --port 8082`  
   （パッケージ版なら `free-claude-code`）
5. 別ターミナルで Claude Code を起動：  
   `ANTHROPIC_AUTH_TOKEN=freecc ANTHROPIC_BASE_URL=http://localhost:8082 claude`  
   VSCode 拡張は `claudeCode.environmentVariables` に同じ 2 つを JSON で書き込み、IntelliJ は `installed.json` の `acp.registry.claude-acp.env` を編集。
6. （任意）`alias claude-pick=/path/to/claude-pick` を `~/.zshrc` に仕込んで fzf でモデル切り替え。

### B. Discord/Telegram から遠隔で Claude Code を回すルート
1. 上記 A を実施。
2. Discord Developer Portal で Bot を作成、Message Content Intent を有効化。
3. `.env` に `MESSAGING_PLATFORM=discord`、`DISCORD_BOT_TOKEN`、`ALLOWED_DISCORD_CHANNELS`、さらに `CLAUDE_WORKSPACE` と `ALLOWED_DIR`（作業可能ディレクトリ）を設定。Telegram なら `MESSAGING_PLATFORM=telegram` と `TELEGRAM_BOT_TOKEN` / `ALLOWED_TELEGRAM_USER_ID`。
4. 音声メモを使うなら `uv sync --extra voice_local`（ローカル Whisper）か `--extra voice`（NIM）。`WHISPER_DEVICE` と `WHISPER_MODEL` を設定。
5. プロキシサーバ起動 → OAuth2 でチャンネルに Bot 招待 → チャンネルで発話するとタスクが実行され、思考トークン・ツール呼び出し・結果がライブストリームで返る。返信でスレッド分岐、`/stop` `/clear` `/stats` で制御。

### C. 開発者として拡張する場合
1. `uv run ruff format` → `uv run ruff check` → `uv run ty check` → `uv run pytest` の 4 点セットを通す（CI 必須）。`# type: ignore` 追加は禁止。
2. 新規プロバイダ追加は `OpenAICompatibleProvider` を継承して `__init__` で `provider_name` / `base_url` / `api_key` を渡すのが最短。完全カスタムなら `BaseProvider.stream_response()` を実装。
3. メッセージングプラットフォーム追加は `MessagingPlatform` ABC（`start / stop / send_message / edit_message / on_message`）を実装。
