---
url: https://github.com/onyx-dot-app/onyx
keywords: RAG, LLM, enterprise-search, self-hosted, AI-chat
oneliner: 社内ドキュメントやSaaSを横断検索し、LLMで対話的に回答を得られるオープンソースAIプラットフォーム
---

## Onyx — オープンソース AI プラットフォーム

### これは何？

Onyx は、組織内に散在するドキュメント・SaaS・ナレッジを **50 種以上のコネクタ**（Slack, Confluence, Google Drive, Notion, GitHub, SharePoint など）で一元的にインデックス化し、LLM を介した **チャット形式の検索・回答** を提供するセルフホスト型プラットフォームである。ハイブリッド検索（ベクトル＋キーワード）と RAG（Retrieval-Augmented Generation）を組み合わせ、社内情報に基づく正確な回答を生成する。

バックエンドは Python/FastAPI + Celery、フロントエンドは Next.js/React で構成され、PostgreSQL・Vespa（ベクトルDB）・Redis を基盤とする。MIT ライセンスの Community Edition と、SSO/RBAC/監査ログ等を備えた Enterprise Edition の二層構造。

---

### 既存ツールと比べて何が嬉しいのか？

| 比較軸 | ChatGPT / Copilot 等 SaaS | 社内 RAG 自作 | **Onyx** |
|---|---|---|---|
| **データの所在** | 外部クラウド送信 | 自社管理 | **自社管理（セルフホスト）** |
| **コネクタ数** | 限定的 | 自前実装が必要 | **50+ を標準搭載** |
| **LLM 選択** | ベンダー固定 | 自由だが構築コスト大 | **任意 LLM（OpenAI, Anthropic, Ollama 等）を設定のみで切替** |
| **導入コスト** | 低いが制約あり | 高い（数週〜数ヶ月） | **`curl` 1行 or Docker Compose で即起動** |
| **エンタープライズ機能** | ベンダー依存 | すべて自作 | **SSO/RBAC/SCIM/監査を標準提供** |

要するに、「**社内データを外に出さず、好きな LLM で、コネクタ設定だけで使い始められる**」点が最大の差別化ポイントである。Deep Research（多段リサーチ）、コード実行サンドボックス、音声モード、MCP 連携といった先進機能もオープンソースで利用できる。

---

### 使うときの流れ

```
1. デプロイ
   └─ Docker Compose で起動（Lite版: <1GB / 標準版: フル機能）
      $ curl -fsSL https://onyx.app/install_onyx.sh | bash

2. 初期設定（管理画面 /admin）
   ├─ LLM プロバイダを登録（APIキー設定）
   └─ データソースのコネクタを追加（Slack, Google Drive 等を認証・接続）

3. インデックス構築（自動）
   └─ Celery ワーカーがバックグラウンドで
      文書取得 → チャンク化 → 埋め込み → Vespa 登録 を実行

4. 利用開始（チャット画面 /app）
   ├─ 自然言語で質問 → 社内ドキュメントを根拠に回答生成
   ├─ カスタムエージェント作成（特定知識・ツール付き）
   └─ Web 検索・コード実行・画像生成なども統合利用可能

5. 運用
   ├─ コネクタは定期同期（自動）
   ├─ RBAC でユーザー/グループ単位のアクセス制御
   └─ 監査ログ・利用分析で運用状況を可視化
```
