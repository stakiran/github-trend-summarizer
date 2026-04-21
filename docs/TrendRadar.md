---
url: https://github.com/sansan0/TrendRadar
keywords: trend-monitor, news-aggregation, keyword-filter, ai-analysis, multi-channel-push, rss, mcp, github-actions, docker, python
oneliner: 中国主要メディア11媒体＋RSSの話題をキーワード／AIで絞り込み、複数チャネルに自動通知する軽量な世論・トレンド監視ツール。
---

# TrendRadar リポジトリ調査メモ

## このリポジトリは何？

- **一言で**：多数の中国系ニュースプラットフォーム（知乎・微博・抖音・B站・百度・头条・澎湃・凤凰・贴吧・華爾街見聞・財聯社の計 11 媒体）＋ RSS フィードをクロールし、キーワード／AI でフィルタして、自分の使う通知チャネルに自動配信する「個人用世論・トレンド監視ダッシュボード」。
- **実装言語／構成**：Python 製（`trendradar/` 配下に `crawler` `ai` `notification` `report` `storage` `core` `utils` などのパッケージ）。設定は `config/config.yaml` と `timeline.yaml`、フィルタは `frequency_words.txt`（キーワード）または `ai_interests.txt`（AI 用自然文）で行う。ブラウザ上でこれら YAML を編集する GUI（`docs/index.html` → GitHub Pages）も同梱。
- **デプロイ形態**：(A) GitHub Actions（デフォルト／S3 互換のリモートストレージに状態を保存、7 日ごとのチェックインで再延長）、(B) Docker/compose、(C) ローカル Python 実行、の 3 通り。データは HTML レポート（`index.html`）としても出力され、GitHub Pages/Cloudflare Pages にもそのまま公開できる。
- **通知先**：企業WeChat・個人WeChat・飛書・DingTalk・Telegram・Email・ntfy・Bark・Slack・汎用 Webhook（Discord/IFTTT 等）。
- **AI 連携**：LiteLLM 経由で DeepSeek/OpenAI/Gemini/Anthropic/Ollama など 100+ プロバイダに対応し、**AI 要約レポート／多言語翻訳／AI によるニュース仕分け（v6.5.0）** に利用。さらに `mcp_server/` として MCP（Model Context Protocol）サーバを同梱し、Claude Desktop や Cherry Studio から「自分が集めたニュース DB」を自然言語で分析できる。

## 既存の似た手段と比べて何が嬉しい？

| 比較対象 | TrendRadar の差別点 |
|---|---|
| 各アプリの公式ホット一覧（微博/知乎/頭条など） | **11 媒体を横断集約**し、プラットフォームのアルゴリズム推薦ではなく **自分のキーワード／興味文** で並び替え。アプリ依存から脱却できる |
| IFTTT / Zapier + 個別 RSS | 中国系主要プラットフォームの非公式 API（newsnow 経由）をそのまま扱えるので、RSS が無い/弱い媒体もカバー。通知チャネルも 10 種以上を同梱済みでコーディング不要 |
| 単純な RSS リーダー（Inoreader 等） | **ランキング推移と「新着 🆕」検出**、同一話題のクロスプラットフォーム比較、3 種の push モード（daily/current/incremental）で「二重通知ゼロ」を実現 |
| 自前スクリプト＋cron | GitHub Actions テンプレートまで込み、Secrets に Webhook を入れるだけで 30 秒デプロイ可。曜日/時間帯ごとに「朝はキーワード、夜は AI」のように **タイムライン別戦略切替** が可能 |
| LLM でニュース要約する自作エージェント | LiteLLM による抽象化でモデル差し替え自由、翻訳／分析／AI フィルタが設定 1 行で有効化。MCP サーバ同梱で「溜めたデータを自分の Claude と会話できる」のはかなりユニーク |

要するに **「多ソース集約 × 自分ルールのフィルタ × AI 補強 × 10+ 通知先 × GH Actions/Docker ワンクリック」** をまとめて提供し、かつデータは完全自前（ローカル SQLite or 自前 S3）で持てる、というのが最大の価値。

## 使うときの流れ

1. **デプロイ方式を選ぶ**
   - 個人サーバ/NAS がある → Docker（`docker/docker-compose.yml` を起動）
   - サーバなし → GitHub の「Use this template」で fork → GitHub Actions で定時実行（Cloudflare R2 などのクラウドストレージを準備）
2. **通知先の Webhook を取得** し、リポジトリの `Settings → Secrets` に `WEWORK_WEBHOOK_URL` / `FEISHU_WEBHOOK_URL` / `TELEGRAM_BOT_TOKEN` 等、決まった名前で登録（複数同時 OK）。
3. **監視設定を書く**（Web エディタ <https://sansan0.github.io/TrendRadar/> で GUI 編集可）
   - `config/config.yaml`：対象プラットフォーム、RSS フィード、push モード（daily/current/incremental）、表示順、AI・翻訳の有効化
   - `config/timeline.yaml`：`morning_evening` などのプリセット、または曜日×時間帯で push/AI 戦略を切替
   - `config/frequency_words.txt`：「AI」「BYD」「教育政策」のようなキーワード（空なら全件通知）／または `ai_interests.txt` に自然文で興味を記述し `filter.method: ai` に
4. **（任意）AI 機能を有効化**：`ai.api_key` を Secret に入れ、`ai_translation.enabled: true` や `ai_filter.min_score: 6` を指定。プロンプトは `ai_analysis_prompt.txt` / `ai_translation_prompt.txt` で好みにカスタム。
5. **実行**：Actions が定期実行（または Docker コンテナが cron 動作）→ クロール → フィルタ → AI 整形 → 各通知先へ push。同時にリポジトリ直下の `index.html` に HTML レポートが出力され、GitHub Pages で閲覧可（ダークモード・検索・タブ切替・`/`・`W`・`D` などのショートカット付き）。
6. **（発展）深掘り分析**：`mcp_server/` を立てて Claude Desktop / Cherry Studio に接続し、`search_news` → `read_article` などの MCP ツールで、蓄積データを自然言語で傾向分析・感情分析させる。
7. **運用**：GH Actions を使う場合は **7 日おきに Actions 画面から Check In ワークフローを手動実行** して有効期限を延長する、というのが唯一の定期メンテナンス。
