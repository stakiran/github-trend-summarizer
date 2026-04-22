---
url: https://github.com/open-metadata/OpenMetadata
keywords: metadata, data-catalog, data-discovery, data-lineage, data-governance
oneliner: データ発見・観測・ガバナンスを一元化する、コネクタ豊富なオープンソース統合メタデータプラットフォーム
---

# OpenMetadata リポジトリ整理

## このリポジトリは何？

**OpenMetadata** は、データ発見（Discovery）／データ観測（Observability）／データガバナンス（Governance）を一つのプラットフォームで扱う、**統合メタデータ管理基盤**のOSS。中央メタデータリポジトリ、列レベルのリネージ、チームコラボレーション機能を備える。

構成は4層：

- **Metadata Schemas**（`openmetadata-spec/`）: JSON Schema による正準データモデル定義。コード生成の起点。
- **Metadata Store**（`openmetadata-service/`）: Java 21 + Dropwizard ベースの REST API と MySQL/PostgreSQL + Elasticsearch/OpenSearch をバックエンドにしたメタデータの中央リポジトリ。
- **Metadata APIs**: 上記 Schema を基にした UI・外部ツール連携用 API。
- **Ingestion Framework**（`ingestion/`）: Python 3.10–3.11 + Pydantic 2 によるプラガブルな取り込み基盤。BigQuery・Snowflake・Redshift・Databricks・Airflow・dbt・Tableau 等 **75〜84 種のコネクタ**を同梱。

加えて React/TypeScript フロントエンド（`openmetadata-ui/`、Tailwind v4 の `tw:` プレフィックスを採用した独自コンポーネントライブラリ）、Airflow ベースのワークフロー、K8s オペレータ、MCP サーバ、SDK（Java/Python）、Docker 一式が同梱された **モノレポ**。

## 何が嬉しいか（既存手段との比較）

| 従来手段 | 課題 | OpenMetadata の解 |
|---|---|---|
| Excel / Confluence での手作り台帳 | 常に陳腐化、リネージ不可 | コネクタ経由で自動取り込み・同期 |
| DataHub（LinkedIn 発） | Kafka 依存のイベント駆動でスタックが重い | MySQL/PostgreSQL + ES/OS のみで軽量起動、Docker 1 コマンド |
| Amundsen（Lyft 発） | 発見特化でガバナンス・観測が弱い | Discovery + Lineage + Quality + Governance + Observability を一本化 |
| Alation / Collibra 等 商用 | 高価でベンダーロックイン | Apache 2.0 完全 OSS、セルフホスト可能 |
| 個別ツール併用（Great Expectations + Marquez + Atlas…） | 連携コストが高い | 単一プラットフォームで完結、Slack/Teams/Webhook 連携も標準 |

特色は **Schema-First アーキテクチャ**（`make generate` で Java/Python/TS のモデルを一括生成）、**列レベルリネージ**、ノーコード Data Quality、KPI ダッシュボード、ロール/ポリシーベースの細粒度アクセス制御、そして「メタデータを書くプロデューサー」と「検索・ガバナンス UI」を共通 API で結ぶ一貫設計。

## 使うときの流れ

### 1. 触ってみる（評価フェーズ）
- [sandbox.open-metadata.org](http://sandbox.open-metadata.org) で UI を体験。
- ローカル実行は Docker 一発：
  ```bash
  ./docker/run_local_docker.sh -m ui -d mysql
  ```
  → `localhost:8585` で UI、MySQL + ES + Airflow が起動。

### 2. コネクタ設定（メタデータ取り込み）
1. UI の **Settings → Services** から対象（例: Snowflake、BigQuery、Airflow、dbt…）を選択。
2. 接続情報を入力（内部的には `openmetadata-spec/` の Connection JSON Schema から動的生成されるフォーム）。
3. Ingestion Pipeline を作成 → Airflow で定期実行。テーブル・列・オーナー・クエリ・リネージが自動登録される。

### 3. 活用
- **Discovery**: キーワード/タグ/ドメイン検索で資産を横断発見。
- **Governance**: ドメイン・データプロダクト定義、タグ/Glossary 用語での分類、ポリシーと Role 付与。
- **Quality**: テーブルにテスト（Null率、ユニーク性、カスタム SQL 等）をノーコード付与し Test Suite 化。
- **Collaboration**: コメント、タスク、アナウンス、Slack/Teams/Webhook へイベント通知。
- **Lineage**: 列レベルで上流下流を可視化、手動編集も可能。

### 4. 拡張・開発（コントリビュータ向け）
- スキーマ変更 → `mvn clean install`（spec）→ `make generate`（全言語モデル再生成）。
- バックエンド: `mvn clean package`、`mvn spotless:apply`。
- フロント: `yarn start` / `yarn test` / `yarn playwright:run`。
- 独自コネクタ: `ingestion/src/metadata/ingestion/source/` 配下にプラグインとして追加。

**要するに**、OSS で自前運用可能な「データカタログ + データ品質 + リネージ + ガバナンス + 観測」の全部乗せ基盤であり、スキーマ駆動の拡張性と豊富なコネクタで、DataHub/Amundsen/商用カタログの代替として位置付けられる。
