---
url: https://github.com/docusealco/docuseal
keywords: e-signature, PDF, document-signing, DocuSign-alternative, Ruby on Rails
oneliner: PDF にフォーム項目を配置し、Web 上で記入・電子署名を完結させられる、オープンソースの DocuSign 代替プラットフォーム。
---

# docusealco/docuseal 調査メモ

## このリポジトリは何？

**DocuSeal** は、PDF を使った電子文書の「作成 → 記入 → 署名 → 配布」を Web 上で完結できる、**オープンソースの電子署名プラットフォーム**（DocuSign / Adobe Sign の代替）。

- 言語/構成: **Ruby on Rails**（コントローラ 90 本超、`app/models` に `Template` / `Submission` / `Submitter` / `WebhookUrl` 等）+ JavaScript フロント + Tailwind CSS。
- ライセンス: **AGPLv3 + 追加条項**（OSS だが SaaS 再販に制限あり）。商用 Pro 版（白ラベル、SSO/SAML、SMS 認証、条件付きフィールド、CSV 一括送信など）が同コードベース内に実装されている。
- デプロイ手段: **Docker 1 コマンド**（`docker run -p 3000:3000 -v.:/data docuseal/docuseal`）、`docker-compose.yml`（PostgreSQL + Caddy で HTTPS 自動化）、Heroku / Railway / DigitalOcean / Render 用ボタンも用意。
- 機能: PDF フォームビルダー（WYSIWYG）、12 種のフィールド（署名・日付・チェックボックス・ファイル等）、複数署名者、SMTP メール、AWS S3 / GCS / Azure 保存、PDF 署名検証、API + Webhook、PWA、MCP 対応（`mcp_controller.rb` あり）、UI 7 言語 / 署名 14 言語。
- 統合: **React / Vue / Angular / 素の JS** 用の埋め込み SDK（`docs/embedding/`）、**8 言語の API クライアント例**（`docs/api/` に Ruby/Python/Node/Go/Java/PHP/C#/TS/Shell）、`openapi.json` 完備。

## 何が嬉しい？既存手段との比較

| 観点 | DocuSign / Adobe Sign | 自作（PDF 編集ライブラリ等） | **DocuSeal** |
|---|---|---|---|
| コスト | 月額課金、ユーザー/送信数で増加 | 開発工数が膨大 | **OSS で無料**、Pro 機能のみ有償 |
| データ管理 | ベンダーのクラウドに保存 | 自前 | **自社サーバー / S3 等にセルフホスト可**（KYC・医療・金融など機密文書向き） |
| カスタマイズ | API 経由のみ、UI は不可 | 何でもできるが大変 | **コードを直接拡張可、白ラベル・埋め込み可** |
| 立ち上げ速度 | 即日（SaaS） | 数週間〜 | **Docker で数分** |
| 法令対応 | 国別に違いあり | 自力 | PDF 署名の暗号検証、タイムスタンプサーバー対応あり |

要するに「**DocuSign の機能を、自社インフラ・自社ドメインで、低コストかつ自由に組み込みたい**」というニーズに刺さる。特に SaaS 製品に「文書署名フロー」を埋め込みたい開発者が、React/Vue 用 SDK + API + Webhook をそのまま利用できる点が強い。

## 使うときの流れ

1. **デプロイ**: `docker run docuseal/docuseal` または `docker-compose up`（Caddy が自動で Let's Encrypt 証明書を発行）。SQLite で動くが、本番は PostgreSQL/MySQL を `DATABASE_URL` で指定。
2. **初期セットアップ**: `/setup` で管理者アカウント作成 → SMTP・ストレージ（S3/GCS/Azure）・SSO・Webhook URL などを設定画面から登録。
3. **テンプレート作成（Templates）**: PDF または DOCX をアップロード → WYSIWYG ビルダーでフィールド（署名・日付・テキスト・チェック等）をドラッグ配置 → 署名者ロールを定義。HTML / PDF テキストタグからの自動生成 API も可能。
4. **送信（Submissions）**: テンプレートから「Submission」を生成し、署名者（Submitter）にメール/SMS で招待 URL を送信。一括送信は CSV/XLSX インポート（Pro）。
5. **署名フロー**: 受信者はリンクからモバイル対応ページで記入・描画署名 → 完了すると PDF に電子署名が埋め込まれ、関係者全員にメール配布。
6. **連携**: REST API（`/api/...` 配下、`openapi.json` 準拠）と Webhook（form / submission / template イベント）で外部システム（CRM・基幹）と接続、もしくは React/Vue/Angular の `<DocusealForm>` コンポーネントで自社アプリに UI を直接埋め込み。
7. **検証・監査**: 完成 PDF は `verify_pdf_signature_controller` 等で署名検証可能、`SubmissionEvent` に閲覧/署名/拒否などの監査ログが残る。
