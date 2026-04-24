---
url: https://github.com/dani-garcia/vaultwarden
keywords: Bitwarden, Rust, password-manager, self-hosted, Docker, Rocket, Diesel, SQLite, MySQL, PostgreSQL
oneliner: 公式 Bitwarden クライアント互換の軽量なパスワードマネージャサーバを Rust で再実装した、セルフホスト向けの非公式実装。
---

# vaultwarden (dani-garcia/vaultwarden)

## このリポジトリは何？
- **公式 Bitwarden サーバの非公式な互換実装**。Rust 製で、Bitwarden Client API とほぼフル互換。旧名は `bitwarden_rs`。
- 公式 Bitwarden クライアント（ブラウザ拡張・モバイル・デスクトップ・CLI）からそのまま接続できるよう、同じ REST API を実装している。
- 主要構成（`src/` 配下）:
  - `main.rs` / `config.rs` / `auth.rs` — 起動・設定・認証基盤
  - `api/` — `core`（Vault/Organization/Send 等の本体 API）, `identity.rs`（ログイン/JWT）, `admin.rs`（管理画面）, `icons.rs`（Webサイトアイコン）, `notifications.rs`（WebSocket通知）, `push.rs`（モバイルPush）, `web.rs`（Web Vault 配信）
  - `db/` — Diesel ORM による SQLite / MySQL / PostgreSQL 対応
  - `mail.rs`, `sso.rs`, `crypto.rs`, `ratelimit.rs` 等
- Web フレームワークは **Rocket**、ORM は **Diesel**。Web Vault（ブラウザから使う UI）は姉妹プロジェクト `bw_web_builds` で改変したものを同梱。
- 実装機能は個人Vault / 添付 / Organization（Collection, Group, Policy, Event Log, Directory Connector, Admin Reset）/ 2FA（TOTP, Email, WebAuthn, YubiKey, Duo）/ Emergency Access / Send / 管理画面など、ほぼフルセット。
- ライセンスは **AGPL-3.0-only**。

## このリポジトリは何が嬉しいの？（既存との比較）
- **公式 Bitwarden Self-hosted との比較**
  - 公式は .NET ベースで複数のサービス（Identity, API, Admin, SQL Server, nginx 等）を Docker Compose で束ねる構成。**メモリ数百 MB ～ 1GB 以上** を要求し、Raspberry Pi や小型 VPS では厳しい。
  - Vaultwarden は **単一バイナリ**。SQLite を選べば **常駐 10–30MB 程度**、ARM でも快適に動く。小規模個人・家庭・小組織のセルフホストに最適。
- **有償機能が無料で使える**
  - 公式は Organization の高度機能（Groups, Policies, Emergency Access, Directory Sync 等）が有償（Premium/Enterprise）。Vaultwarden はこれらを API 互換で提供（免責：互換実装であり公式サポート外）。
- **他の OSS パスワード管理ツール（KeePass/Bitwarden 公式以外）との比較**
  - KeePass 系は DB ファイルを自分で同期（Dropbox等）する必要があり、モバイルやチーム共有の体験は劣る。Vaultwarden は公式 Bitwarden クライアントをそのまま使える＝同期・共有・2FA・UX が洗練されている。
- **セルフホスト前提の細部配慮**：Admin バックエンド、SQLite/MySQL/PostgreSQL 選択可、S3 互換ストレージへの添付ファイル保存、SSO (OIDC)、YubiKey/WebAuthn 等、運用で必要なピースが揃う。

## 使うときの流れ
1. **デプロイ**: 公式推奨は Docker/Podman コンテナ（`ghcr.io` / `docker.io` / `quay.io`）。
   ```shell
   docker run -d --name vaultwarden \
     -e DOMAIN="https://vw.domain.tld" \
     -v /vw-data/:/data/ \
     -p 127.0.0.1:8000:80 \
     vaultwarden/server:latest
   ```
   またはソースから `cargo build --features sqlite` でバイナリ生成も可能。
2. **HTTPS 化**: Web Crypto API の要件から `localhost` 以外は HTTPS 必須。Nginx/Caddy/Traefik 等の **リバースプロキシ経由** で TLS 終端するのが推奨（Rocket の TLS も可）。
3. **初期設定**: 環境変数（`DOMAIN`, `SIGNUPS_ALLOWED`, `SMTP_*`, `ADMIN_TOKEN` など）または管理画面（`/admin`）から設定。`ADMIN_TOKEN` を設定すると管理 UI からユーザ管理・SMTP 等を GUI 設定できる。
4. **クライアント接続**: 公式 Bitwarden のブラウザ拡張・モバイル・デスクトップアプリの「サーバ URL」を自前ドメインに切り替え → アカウント作成 → 既存 Bitwarden からエクスポートしたデータをインポート。
5. **組織・共有**: Organization を作成し、Collection / Group / Policy を設定してチーム共有。必要に応じて 2FA、Emergency Access、Send、SSO (OIDC) を有効化。
6. **運用**: `/vw-data/`（SQLite 本体、添付、アイコンキャッシュ、RSA キー）の **定期バックアップ** が最重要。問題報告は公式 Bitwarden ではなく本プロジェクトの Matrix / GitHub Discussions / Discourse へ。
