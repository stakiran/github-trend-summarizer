---
url: https://github.com/Hmbown/DeepSeek-TUI
keywords: DeepSeek, TUI, coding agent, Rust, ratatui, terminal, MCP, LSP, auto-mode, sub-agents
oneliner: DeepSeek V4 をバックエンドに、ターミナル上で動作する Rust 製のキーボード駆動コーディングエージェント TUI。
---

# DeepSeek-TUI 整理メモ

## 1. このリポジトリは何？

- **正体**: ターミナル（TUI）で動く、DeepSeek V4 専用のコーディングエージェント。Rust 製で、`deepseek`（ディスパッチャ CLI）と `deepseek-tui`（ratatui 製の本体ランタイム）の 2 バイナリ構成。
- **対象モデル**: `deepseek-v4-pro` / `deepseek-v4-flash`（1M トークンコンテキスト、思考ブロックのストリーミング、prefix-cache 込みのコスト計上に対応）。
- **できること**: ファイルの read/edit、シェル実行、git 操作、Web 検索/閲覧、apply-patch、サブエージェント協調、MCP サーバ接続、LSP（rust-analyzer / pyright / tsserver / gopls / clangd）による編集後インライン診断など。
- **配布形態**: npm（`deepseek-tui`、ビルド済みバイナリの取得ラッパ）、Cargo（`deepseek-tui-cli` / `deepseek-tui`）、Homebrew tap、GitHub Releases の事前ビルド（Linux x64/ARM64、macOS x64/ARM64、Windows x64）。
- **API バックエンド**: DeepSeek 公式に加え NVIDIA NIM、Fireworks、OpenRouter、Novita、SGLang/vLLM/Ollama 等の OpenAI 互換エンドポイントに切替可能。
- **付帯機能**: HTTP/SSE 用の `deepseek serve --http`、Zed 連携用の ACP アダプタ、セッション保存/再開/フォーク、ワークスペースのスナップショットによる `/restore`、永続タスクキュー、Skills（GitHub から導入できる指示パック）、ユーザメモリ、4 言語ローカライズ（en/ja/zh-Hans/pt-BR）。

## 2. 何が嬉しいの？（既存の似た手段との比較）

| 観点 | DeepSeek-TUI | Claude Code / Codex CLI 等の他 TUI エージェント | 単独の DeepSeek Web チャット |
|---|---|---|---|
| バックエンド | DeepSeek V4 専用最適化（思考ブロック、cache hit/miss を可視化したコスト推定） | 各 LLM ベンダ固有 | DeepSeek 公式 UI |
| **Auto モード** | 1 ターンごとに `flash` の小さなルーティング呼び出しでモデルと thinking レベルを自動選択。コストと品質を自動最適化 | 多くは手動でモデル指定 | 手動切替 |
| 操作モード | Plan（読み取り専用）/ Agent（承認ゲート）/ YOLO（全自動）の 3 段 | ツールにより差。Plan の sandbox を read-only に強制する設計 | なし |
| 安全性 | サイド `.git` でターン前後スナップショット → `/restore` でロールバック、本物の `.git` を汚さない | 同様の機能を持つものもあるがリポを直接触る場合あり | なし |
| 拡張性 | MCP サーバ接続、Skills（GitHub から `install`、バックエンドサービス不要）、サブエージェント、RLM (`rlm_query`) で flash 子エージェントへ並列分析 | ツールにより MCP は対応、Skill 仕様は独自 | なし |
| 開発体験 | LSP 診断を編集ごとに自動収集してモデルに次ターンのコンテキストとして注入 | 一部対応 | なし |
| 透明性 | 1M トークン文脈の使用量、prefix キャッシュのヒット率、ターン/セッション単位コストを TUI に常時表示 | 限定的 | なし |
| ヘッドレス利用 | `serve --http` で HTTP/SSE API、`serve --acp` で Zed の ACP エージェント化 | ベンダ依存 | 不可 |

要するに「**DeepSeek を最も安く・賢く・安全に回すための専用ハーネス**」で、Rust バイナリ単体で動き、Plan/Agent/YOLO の段階的承認、サイド git でのロールバック、Auto モードによる per-turn のモデル/思考レベル自動選択といった現代的な agent UX をフルセットで備えている点が、汎用エージェント CLI よりも DeepSeek 用途で際立つ。

## 3. 使うときの流れ

1. **インストール**（いずれか 1 つ）
   - `npm install -g deepseek-tui`（推奨・最速）
   - `cargo install deepseek-tui-cli --locked && cargo install deepseek-tui --locked`
   - `brew tap Hmbown/deepseek-tui && brew install deepseek-tui`
   - GitHub Releases からバイナリ直接 DL
2. **API キー設定**（初回起動時にプロンプトされ `~/.deepseek/config.toml` に保存）
   - もしくは `deepseek auth set --provider deepseek` / `export DEEPSEEK_API_KEY=...`
   - `deepseek doctor` で疎通・キーソースを確認、`deepseek auth status` で現在のクレデンシャル元を表示。
3. **起動**
   - `deepseek` で対話 TUI、`deepseek "explain this function"` で one-shot、`deepseek --model auto "fix this bug"` でモデル自動選択、`deepseek --yolo` で全ツール自動承認。
4. **モード切替**: `Tab` で Plan → Agent → YOLO を循環。`Shift+Tab` で reasoning effort（off → high → max）。`F1` ヘルプ、`Ctrl+K` コマンドパレット、`@path` でファイル/ディレクトリ添付。
5. **編集サイクル**
   - Plan モードで読み取りのみ調査 → `update_plan` / `checklist_write` で計画提示。
   - Agent モードで承認ゲート付きにファイル編集・シェル・git・Web を実行。編集後は LSP 診断が自動でモデルに戻る。
   - 失敗したら `/restore` または `revert_turn` でサイド git のスナップショットからロールバック。
6. **セッション運用**: `Ctrl+R` または `deepseek resume --last` で再開、`deepseek fork <ID>` で任意ターンから分岐、`Ctrl+S` でドラフトを stash。
7. **拡張**: `/skills` でスキル一覧、`/skill install github:<owner>/<repo>` で導入、MCP サーバを `~/.deepseek/config.toml` に追加して外部ツールを連携、`deepseek serve --http` でヘッドレス運用、`deepseek serve --acp` で Zed の ACP エージェントとして組み込み。
8. **コスト管理**: TUI 下部にターン/セッションのトークン・コスト・キャッシュ命中率がリアルタイム表示されるので、`auto` モードや `flash` 固定とのトレードオフを見ながら進める。
