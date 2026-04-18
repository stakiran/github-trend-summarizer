---
url: https://github.com/thunderbird/thunderbolt
keywords: AI client, self-hosted, cross-platform, Tauri, BYOM, E2E encryption, on-prem, offline-first, MPL-2.0
oneliner: モデル・データを自分で所有できる、セルフホスト可能なクロスプラットフォーム AI クライアント（MZLA / Mozilla 関連）
---

# thunderbird/thunderbolt まとめ

## このリポジトリは何？

**Thunderbolt** は、Mozilla の助成を受けた MZLA Technologies（Thunderbird と同じ運営元）が開発する、**オープンソース（MPL-2.0）のクロスプラットフォーム AI クライアント**です。「AI You Control: Choose your models. Own your data. Eliminate vendor lock-in.」をスローガンに掲げ、ChatGPT/Claude/Gemini のような AI チャット UI を、**利用するモデル・データ保管場所・認証基盤をユーザー側で選べる形**で提供します。

主な構成：
- **フロントエンド**：React 19 + Vite + Radix UI + Zustand + TanStack Query、AI 層は Vercel AI SDK + MCP クライアント
- **シェル**：Tauri により **Web / macOS / Linux / Windows / iOS / Android** の単一コードベースを実現
- **ローカル永続化**：SQLite + Drizzle（オフラインファースト設計、現在は一部機能が認証依存）
- **バックエンド（セルフホスト可）**：Bun + Elysia、認証は Better Auth（OTP/OIDC、Keycloak 対応）、同期は PowerSync + PostgreSQL、LLM は推論プロキシ経由で Anthropic / OpenAI / Mistral / OpenRouter / Ollama / llama.cpp などへルーティング
- **E2E 暗号化（Preview）**：有効時は端末側で暗号化してからサーバに送信、サーバは暗号文のみ保持
- **デプロイ**：Docker Compose、Kubernetes マニフェスト、Pulumi (AWS Fargate / EKS) を同梱

現在のステータスは「エンタープライズ向け on-prem を当面のターゲットとした早期開発中／セキュリティ監査中」。チャット・検索・MCP・OIDC・カスタムプロバイダ登録などは利用可能、エージェントメモリやフルオフラインは Planned。

## 何が嬉しい？既存手段との比較

| 比較対象 | Thunderbolt の差別化ポイント |
|---|---|
| **ChatGPT / Claude.ai など SaaS 製品** | 会話履歴や添付がベンダーサーバに残らず、**自前インフラで完結**。モデルも自由に差し替えでき、ベンダーロックインが無い。 |
| **Ollama / LM Studio / Jan など純ローカル UI** | 単なるローカル推論 UI に留まらず、**マルチデバイス同期（PowerSync）・OIDC/SSO・E2E 暗号化・MCP・OAuth 連携（Google/Microsoft）** までエンタープライズ要件を束ねている。 |
| **LibreChat / OpenWebUI など OSS Web UI** | **Tauri による真のクロスプラットフォーム（モバイル含む）** と、SQLite をソース・オブ・トゥルースとするオフラインファースト設計。さらに Mozilla 系という組織的な信頼性。 |
| **自作 LangChain アプリ** | 認証・同期・暗号化・UI・配布までパッケージ済みで、**「OSS を `docker compose up` で立てれば社内 AI クライアントが手に入る」** という具体的なゴールに最短距離。 |

要するに「**BYOM（持ち込みモデル）× BYO インフラ × 全 OS 対応 × エンタープライズ認証**」を一つの OSS で揃えた点が特徴。

## 使うときの流れ

1. **自前サーバを建てる**（管理者）
   - `git clone` → `cd deploy` → `cp .env.example .env` → `docker compose up --build`
   - これで Frontend (`:3000`)、Backend、PostgreSQL、Keycloak (`:8180`、admin/admin)、PowerSync、MongoDB が立ち上がる。realm は `config/keycloak-realm.json` から自動インポート。
   - 本番用途では `deploy/k8s/` の Kubernetes マニフェスト、あるいは `deploy/pulumi/`（AWS Fargate / EKS）を利用。

2. **認証 & モデルプロバイダ設定**
   - Keycloak（または OIDC IdP）でユーザを作成し、アプリからサインイン。
   - アプリの設定画面で **OpenAI 互換 API キー**（Anthropic / OpenAI / Mistral / OpenRouter）や **Ollama / llama.cpp のローカルエンドポイント**を登録。公式推論エンドポイントは未提供のため BYOK 必須。

3. **日常利用（エンドユーザ）**
   - 各 OS 向けクライアント（Web / Mac / Linux / Windows / iOS / Android）からログイン。
   - **Chat Mode / Search Mode / Research Mode (Preview) / Chat Widgets** を使い分けて対話。MCP サーバ接続、Google / Microsoft 連携、Tasks (Preview) も利用可能。
   - データは端末の SQLite に保存され、オプションで E2E 暗号化したまま PowerSync 経由でデバイス間同期。

4. **開発・貢献したい場合**
   - 前提：Bun / Rust / Docker。`make setup` → `cp .env.example .env`（ルート・`backend/` 両方）→ `make docker-up` → `cd backend && bun dev` → `bun dev`（Web）または `bun tauri:dev:desktop|ios|android`。
   - テストは `bun run test`（フロント）／`bun run test:backend`。詳細は `docs/development.md`・`docs/architecture.md`・`docs/e2e-encryption.md` を参照。
