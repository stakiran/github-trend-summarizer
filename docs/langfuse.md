---
url: https://github.com/langfuse/langfuse
keywords: LLM Observability, Prompt Management, Evaluation, Tracing, Open Source, TypeScript, ClickHouse, Next.js
oneliner: LLM アプリケーションの開発・監視・評価・デバッグを一気通貫で行うオープンソースの LLM エンジニアリングプラットフォーム。
---

# langfuse/langfuse まとめ

## このリポジトリは何？

**Langfuse** は、LLM を組み込んだアプリケーションのライフサイクル全体（開発・監視・評価・デバッグ）を支援する **オープンソースの LLM エンジニアリングプラットフォーム**（YC W23、MIT ライセンス）。

主な構成要素は pnpm + Turborepo のモノレポで、以下のパッケージに分かれている。

- `web/` … Next.js 製の UI／tRPC／Public REST API
- `worker/` … キュー消費・バックグラウンド処理
- `packages/shared/` … ドメインモデル、Prisma(PostgreSQL) スキーマ、ClickHouse マイグレーション、キュー契約
- `ee/` … Enterprise 機能
- `fern/` … 公開 API 定義（OpenAPI ソース）

提供する主要機能は 6 つ。

1. **LLM Observability / Tracing** — LLM 呼び出しや RAG・エージェント挙動をトレース化し、セッション単位で可視化・デバッグ。
2. **Prompt Management** — プロンプトの中央管理・バージョニング・共同編集。強力なキャッシュで本番レイテンシに影響を与えない。
3. **Evaluations** — LLM-as-a-judge、ユーザーフィードバック、手動ラベリング、カスタム評価パイプラインを API/SDK でサポート。
4. **Datasets** — テストセット・ベンチマークを用いたリリース前・継続的評価。
5. **LLM Playground** — プロンプトとモデル設定の試行錯誤用 UI。トレースから直接ジャンプ可能。
6. **Public API / SDK** — Python・JS/TS の型付き SDK、OpenAPI 仕様、Postman コレクションで独自の LLMOps を組み立てられる。

## 何が嬉しいのか（既存手段との比較）

| 比較対象 | Langfuse の強み |
|---|---|
| LangSmith（クローズドな LangChain SaaS） | **MIT の OSS** でセルフホスト可（Docker Compose 5 分、Helm、Terraform テンプレも提供）。ベンダーロックインなし。 |
| Helicone・Arize Phoenix 等 OSS 観測ツール | Tracing だけでなく **プロンプト管理・評価・データセット・Playground を 1 つの UI に統合**。開発ループ全体をカバー。 |
| 自前で Postgres/ELK に log を貯める方式 | **ClickHouse + Redis キュー** を用いた大規模トレース用アーキテクチャが最初から組まれ、OpenTelemetry・LangChain・OpenAI SDK・LlamaIndex・LiteLLM・Vercel AI SDK・CrewAI など **20+ の統合**が即使える。 |
| SaaS 型評価ツール | 機密データを外に出さず自社 VPC で動かせる。EU/US の Cloud 版も選択可。 |

要は「観測・プロンプト・評価・データセットを **別々の SaaS で繋ぎ込む手間**」を、OSS 一つで、**SDK を数行入れるだけ**で成立させられる点が独自の価値。

## 使うときの流れ

1. **デプロイ環境を選ぶ**
   - Langfuse Cloud（無料枠あり）にサインアップ、もしくは `git clone && docker compose up` で自前環境にセルフホスト（VM / Kubernetes Helm / Terraform for AWS・Azure・GCP も可）。
2. **プロジェクトと API 鍵を作成**
   - UI でプロジェクトを作り、`LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` を発行。
3. **アプリに計装（instrumentation）を仕込む**
   - Python なら `pip install langfuse`、`@observe()` デコレータや `from langfuse.openai import openai` のようなドロップイン SDK を使う。
   - LangChain・LlamaIndex・Haystack・Vercel AI SDK・Mastra・LiteLLM などはコールバック／プロキシで自動計装。
4. **トレースを確認しながらデバッグ**
   - UI で LLM 呼び出し・RAG・ツール呼び出しをツリー表示でレビュー。気になる出力は **Playground** にそのまま飛ばしてプロンプト修正。
5. **プロンプトを Prompt Management に移管**
   - プロダクションコードからは Langfuse 経由でプロンプトを取得（キャッシュ済み）。バージョン管理・A/B を UI で回す。
6. **評価を回す**
   - 本番トレースに対して LLM-as-a-judge／ユーザーフィードバック／手動ラベルで継続評価。Datasets に代表トレースを積んでリグレッションテスト、CI からも API 経由で実行。
7. **API / Webhook で社内ワークフローに統合**
   - OpenAPI・型付き SDK で既存の LLMOps パイプラインや BI に連携し、運用に乗せる。
