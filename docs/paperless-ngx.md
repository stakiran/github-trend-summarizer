情報が十分集まったので、まとめを出力します。

---
url: https://github.com/paperless-ngx/paperless-ngx
keywords: ドキュメント管理, OCR, Django, セルフホスト, 全文検索
oneliner: 紙書類をスキャンしてOCR・自動タグ付け・全文検索できるセルフホスト型ドキュメント管理システム。
---

# paperless-ngx 概要

## このリポジトリは何？

**Paperless-ngx** は、紙の書類をスキャンしてデジタルアーカイブ化し、検索可能な形で一元管理するための OSS ドキュメント管理システム (DMS) です。元プロジェクト `the-paperless-project/paperless` と `paperless-ng` の公式後継として、コミュニティ主導で継続開発されています。自分のサーバ（または NAS、Raspberry Pi など）に Docker で立て、ブラウザ UI から文書を閲覧・管理します。ライブデモは `demo.paperless-ngx.com`（`demo`/`demo`）。

- **バックエンド**: Django 5.x + Python 3.10–3.12、Celery + Redis でジョブキュー、DB は PostgreSQL / MariaDB / SQLite
- **OCR**: `ocrmypdf` + Tesseract（100+ 言語対応）、Office 文書は Apache Tika 経由
- **フロントエンド**: Angular (TypeScript)（`src-ui/`）
- **主要ディレクトリ**: `src/`（Django アプリ）、`src-ui/`（SPA）、`docker/compose/`（デプロイ用テンプレート）、`docs/`、`install-paperless-ngx.sh`

## このリポジトリは何が嬉しいの？

**「紙を捨てたいが、Evernote や Dropbox に丸投げするのは不安」という層にピッタリ**のツールです。既存手段との比較：

| 比較対象 | paperless-ngx の優位点 |
|---|---|
| 手動のフォルダ管理 | OCR により画像/PDF が全文検索対象に。ファイル名・階層に頼らず、タグ・通信元 (Correspondent)・文書タイプで多軸分類できる |
| Evernote / Dropbox / Google Drive | **完全セルフホスト**でデータがローカルに留まる。サブスク不要、ベンダーロックインなし。PDF/A 形式で長期保存 |
| 元祖 paperless / paperless-ng | 活発なメンテ、多言語 UI、カスタムフィールド、ワークフロー、共有リンク、マルチユーザー権限など機能が大幅拡張 |
| DEVONthink 等の商用 DMS | 無料・オープンソース、API 経由で拡張可能、モバイルスキャナアプリ連携エコシステムあり |

差別化の核は、**機械学習ベースの自動分類**（過去のタグ付け履歴から新しい文書のタグ・発信元を推定）と、**メール取り込み**（IMAP で添付を自動投入）、**ワークフロー**（取り込み時のイベントトリガで処理を自動化）です。

## 使うときの流れ

1. **デプロイ**: `docker/compose/` 内の `docker-compose.*.yml` を選ぶか、`install-paperless-ngx.sh` で対話的にセットアップ。webserver / DB / broker / gotenberg / tika のコンテナ群が起動
2. **設定**: `paperless.conf.example` を参考に環境変数（言語、OCR 設定、USER、タイムゾーン等）を決める
3. **取り込み (Consume)**: スキャナや複合機から consume フォルダへ PDF/画像を放り込む → Celery ワーカーが OCR → テキスト抽出 → PDF/A に再保存
4. **分類**: タグ / 通信元 / 文書タイプ / カスタムフィールドを付与。ML による自動推定や、正規表現・ワークフローでの自動タグ付けも可
5. **活用**: Angular UI から全文検索（サジェスト・関連度ソート）、保存済みビュー、共有リンク、REST API や公式モバイルアプリ経由の参照。メール取り込み・定期バックアップで運用を回す

**向いているユーザー**: プライバシー重視で自分のサーバを持てる個人、請求書や契約書を大量に抱える SOHO / 小規模組織、ペーパーレス化と長期検索性を同時に満たしたい人。
