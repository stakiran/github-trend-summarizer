I have enough to compose the summary. Let me write it.

---
url: https://github.com/PostHog/posthog
keywords: product-analytics, open-source, all-in-one, session-replay, feature-flags, experiments, self-hostable
oneliner: プロダクト分析・セッションリプレイ・フィーチャーフラグ・A/Bテスト・エラー追跡などを一つに束ねた、オープンソースの「オールインワン製品開発プラットフォーム」。
---

# PostHog/posthog ざっくり整理

## このリポジトリは何？

**PostHog** は、Web / モバイルアプリの「ユーザーがどう使っているか」を計測し、そのデータを基に機能をリリース・検証するまでの一連のワークフローをまとめて提供する、オープンソースの **オールインワン・プロダクト開発プラットフォーム** です。

- 言語構成: Python (Django) + TypeScript (React / kea) を中心に、ClickHouse・Kafka・Postgres をバックエンドに持つモノレポ。
- ライセンス: 本体は MIT。`ee/` 配下のみ独自ライセンス（完全 FOSS 版は `posthog-foss` リポジトリ）。
- 同梱される主な機能（`products/` 配下のサブパッケージとして実装）:
  - Product Analytics / Web Analytics（イベント計測、ファネル、リテンション、SQL クエリ "HogQL"）
  - Session Replay（実ユーザーの画面録画）
  - Feature Flags / Experiments（A/Bテスト、段階的リリース）
  - Error Tracking、Surveys（ノーコード NPS 等）
  - Data Warehouse / CDP（Stripe・HubSpot 等の外部データ同期、25+ 連携先へのエクスポート）
  - LLM Analytics（LLM アプリのトレース／コスト／レイテンシ計測）
  - MCP サーバ・Toolbar・Notebooks など開発者向けツール

## 既存の類似手段と比べて何が嬉しいか

同等のことをやろうとすると、典型的には **Google Analytics / Amplitude / Mixpanel（分析） + FullStory / Hotjar（リプレイ） + LaunchDarkly / Optimizely（フラグ／実験） + Sentry（エラー） + Segment（CDP） + SurveyMonkey（アンケート）** といった 5〜6 サービスを契約・配線する必要があり、次のような問題が出ます。

| 観点 | 既存の個別 SaaS 寄せ集め | PostHog |
|---|---|---|
| 費用・契約 | ベンダーごとに課金、利用量スケールで高額化 | 単一プラットフォーム、1M events/5k recordings/1M flag 等は無料枠。料金ページも公開 |
| データの一貫性 | プロダクトごとに別データベース。結合は Segment などで頑張る | 同じイベント・人物データがそのまま全機能（リプレイ、フラグ、実験、サーベイ）で共有される |
| 自前ホストの可否 | ほぼ全滅。あっても限定機能のみ | Docker 1行で Hobby デプロイ、Kubernetes 大規模運用もOK。データを自社内に留められる |
| ベンダーロックイン | JSON スキーマ非公開・SQLアクセス不可 なことが多い | HogQL で ClickHouse に直接 SQL、OpenAPI / MCP / SDK 多言語（JS, Next, React, iOS, Android, Python, Node, Go…）全部公開 |
| 「分析→検証」の距離 | 分析結果→別SaaSでフラグ→別SaaSで実験、と手作業 | 同じダッシュボード内で「ファネル脱落ユーザーにだけフラグON→実験」と地続きで運用可能 |

要するに **「Segment + Amplitude + Hotjar + LaunchDarkly + Sentry を一本化し、しかも自前ホストできる OSS」** が立ち位置です。

## 使うときの流れ

1. **インスタンスを用意する**
   - 推奨は [PostHog Cloud（US/EU）](https://us.posthog.com/signup) にサインアップ（無料枠あり）。
   - 自前で持ちたければ Linux + Docker で hobby デプロイ:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/posthog/posthog/HEAD/bin/deploy-hobby)"
     ```
     （〜100k events/月 までが目安。超えたら Cloud 推奨）
2. **SDK / スニペットを自プロダクトに仕込む**
   - Web なら JS スニペット 1 枚、または `posthog-js` / `posthog-js-lite`。
   - React Native / iOS / Android / Flutter、Python / Node / Go / Ruby / PHP / .NET なども公式 SDK あり。API 直叩きも可能。
3. **イベントを計測する（Autocapture or 明示的に `capture()`）**
   - クリック・PV・エラーなどは自動取得。ドメイン固有イベントだけ `posthog.capture('signup_completed', {...})` のように送る。
4. **分析・可視化**
   - ダッシュボードで Insights（ファネル、リテンション、パス、SQL）を組み、Session Replay で実際の操作を観察、Error Tracking で例外を追う。
5. **意思決定→機能提供に繋げる**
   - Feature Flag で段階リリース、Experiment で A/B 差分を統計的に評価、Survey で定性フィードバック、CDP / Batch Export で DWH や下流ツールへ連携。
6. **（開発者向け）拡張・カスタマイズ**
   - `products/<name>/` に backend (Django) + frontend (React/kea) を垂直スライスで追加する規約。
   - 新製品の雛形は `bin/hogli product:bootstrap <name>`。serializer を変えたら `hogli build:openapi` で型と MCP ツールを再生成、というのが開発サイクル。
