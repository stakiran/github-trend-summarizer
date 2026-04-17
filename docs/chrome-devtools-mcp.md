以上から十分情報が揃ったのでまとめる。

---
url: https://github.com/ChromeDevTools/chrome-devtools-mcp
keywords: MCP, Chrome DevTools, coding agent, Puppeteer, performance trace
oneliner: Chrome DevTools の機能をコーディングエージェントに橋渡しする MCP サーバ。Chrome を起動・操作・計測させ、デバッグや性能分析を任せられるようにする。
---

# ChromeDevTools/chrome-devtools-mcp

## このリポジトリは何？

`chrome-devtools-mcp` は、**Gemini / Claude / Cursor / Copilot などのコーディングエージェントから「本物の Chrome ブラウザ」を操作・検査できるようにする MCP（Model Context Protocol）サーバ**（TypeScript/Node.js 実装、npm パッケージ公開）。Google Chrome DevTools チームが公式にメンテしている。

- 内部では **Puppeteer** で Chrome を自動操作し、**Chrome DevTools Protocol (CDP)** 経由で DevTools の計測機能（パフォーマンストレース、Lighthouse、ネットワーク、コンソール、ヒープスナップショットなど）を呼び出す
- ツールは以下カテゴリで計 **29 ツール**を提供
  - Input 自動化（click / fill / type_text / drag / upload_file …）
  - ナビゲーション（navigate_page / new_page / wait_for …）
  - エミュレーション（emulate / resize_page）
  - パフォーマンス（performance_start_trace / performance_analyze_insight / take_memory_snapshot）
  - ネットワーク（list_network_requests / get_network_request）
  - デバッグ（evaluate_script / list_console_messages / lighthouse_audit / take_screenshot / take_snapshot）
- 基本機能だけ使う `--slim` モード（3 ツール）、MCP を介さず使える CLI、Claude Code 向けプラグイン（MCP + Skills 同梱）も用意

設計原則（`docs/design-principles.md`）として「Agent-Agnostic」「トークン節約のため生データではなく意味的サマリを返す」「重い成果物はファイルパス/URI で返す」「自己修復できるエラーメッセージ」など、エージェント向けに最適化された API を志向している点が特徴。

## このリポジトリは何が嬉しいの？

**「LLM エージェントがフロントエンドを“実際に動かして”検証・デバッグ・性能評価できる」** こと。既存手段との違いは次の通り。

| 比較対象 | 位置付け・違い |
|---|---|
| Puppeteer / Playwright をエージェントから直接叩く | 生 API は粒度が細かすぎ、返すデータも大きく LLM 向けでない。本ツールは**意味のある粒度のツール**と**要約済みレスポンス**を提供 |
| Playwright MCP など汎用ブラウザ自動化 MCP | 操作中心で、**パフォーマンストレース・Lighthouse 監査・CrUX フィールドデータ・ヒープスナップショット・ソースマップ付きスタックトレース**など DevTools 固有の**計測/解析能力**が強い |
| ヘッドレス実行スクリプトや CI 計測 | 人手で書く必要があり対話的ではない。本ツールは**エージェントが自律的に「このページの LCP を測って原因分析して」と依頼できる** |
| Chrome DevTools の手動操作 | 人間が画面で行うため繰り返しにくい。エージェントに**再現可能・連続的に**回させられる |

結果として、エージェントに「実装 → ブラウザで開く → コンソールエラー拾う → 性能トレース取る → 修正」のループを任せられるのが最大の嬉しさ。

## 使うときはどういう流れに沿う？

1. **前提準備**：Node.js v20.19+ / Chrome stable 以降 / npm を用意
2. **MCP クライアントに登録**：`~/.claude.json` や Cursor / VS Code / Codex / Windsurf 等の MCP 設定に、次を追加（`npx` で毎回最新を取得）
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest"]
       }
     }
   }
   ```
   Claude Code なら `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`、あるいは `/plugin install chrome-devtools-mcp`（Skills も同梱）。
3. **オプションで用途に合わせて設定**：`--headless` / `--isolated`（使い捨てプロファイル）/ `--channel=canary` / `--viewport=1280x720` / `--slim` / `--browser-url=http://127.0.0.1:9222`（既存 Chrome に接続）/ `--no-usage-statistics` など
4. **エージェントに自然言語で指示**：例）`Check the performance of https://developers.chrome.com`
   - 最初のツール呼び出し時に Chrome が自動起動（接続モードを除く）
   - エージェントが `new_page` → `navigate_page` → `performance_start_trace` → `performance_stop_trace` → `performance_analyze_insight` などを連鎖呼び出し
5. **結果の受け取り**：大きな成果物（スクリーンショット、トレース）はファイル/リソース URI として、分析結果は要約テキストとしてエージェントに返り、エージェントが人間に説明・次のアクションへ反映する
6. **応用**：E2E 風のフォーム操作確認、コンソールエラー/ネットワーク失敗の切り分け、Lighthouse 監査、レスポンシブ/デバイスエミュレーション、ヒープリークの調査など、日常的なフロント開発ループに組み込む
