---
url: https://github.com/goharbor/harbor
keywords: container-registry, cloud-native, vulnerability-scanning, CNCF, OCI
oneliner: コンテナイメージの保存・署名・脆弱性スキャン・レプリケーションを統合的に提供するCNCF公式のクラウドネイティブレジストリ
---

## Harbor — クラウドネイティブ・コンテナレジストリ

### これは何？

Harbor は **CNCF（Cloud Native Computing Foundation）Graduated プロジェクト**のオープンソース・コンテナレジストリ。Docker Distribution（OCI 準拠レジストリ）をベースに、**セキュリティ・アクセス制御・イメージ管理**の機能群を上乗せした「エンタープライズ対応のプライベートレジストリ」。

内部は Go + Angular 製のマイクロサービス構成で、Core API / Job Service / Registry Controller / Web Portal / PostgreSQL / Redis の 7 サービスが Docker Compose または Helm Chart でデプロイされる。現行バージョンは **v2.16.0**。

---

### 何が嬉しいのか？（既存手段との比較）

| 観点 | Docker Hub / GitHub Packages | 素の Docker Registry | **Harbor** |
|---|---|---|---|
| **脆弱性スキャン** | 有料 or 制限付き | なし | **Trivy 統合で全イメージ自動スキャン** |
| **RBAC / マルチテナント** | 組織単位のみ | なし | **プロジェクト単位のロール制御・クォータ管理** |
| **イメージ署名** | 限定的 | なし | **Cosign / Notation 署名をネイティブサポート** |
| **レプリケーション** | なし | なし | **複数レジストリ間で Push/Pull 双方向同期** |
| **保持ポリシー** | 手動削除 | 手動 | **タグ・日時ベースの自動 Retention + GC** |
| **認証統合** | 独自アカウント | Basic認証のみ | **LDAP / OIDC / AD / ロボットアカウント** |
| **監査ログ** | なし | なし | **全操作の Audit Log + Webhook 通知** |
| **運用場所** | SaaS（外部） | オンプレ可 | **オンプレ・クラウド問わず自前運用可能** |

**一言で言えば：** 「素の Docker Registry では足りないガバナンス・セキュリティ機能を全部入りにした、自前運用できるレジストリ」。Docker Hub に機密イメージを置けない企業や、マルチクラウド環境でイメージを同期したいチームに最適。

---

### 使うときの流れ

```
1. デプロイ
   ├─ シングルノード → オフラインインストーラ or Docker Compose
   └─ Kubernetes     → Helm Chart（harbor-helm）or Harbor Operator

2. 初期設定（Web UI: https://<harbor-host>）
   ├─ 管理者ログイン（デフォルト: admin / Harbor12345）
   ├─ 認証バックエンド設定（LDAP / OIDC など）
   └─ プロジェクト作成 + メンバー招待 + ロール付与

3. イメージの Push / Pull（通常の docker コマンド）
   $ docker login <harbor-host>
   $ docker tag myapp:v1 <harbor-host>/myproject/myapp:v1
   $ docker push <harbor-host>/myproject/myapp:v1

4. セキュリティ運用
   ├─ 脆弱性スキャン：Push 時自動 or 手動 or 定期スケジュール
   ├─ イメージ署名 ：Cosign で署名 → Harbor が署名を検証・表示
   └─ CVE 許可リスト：許容する CVE をプロジェクト単位で管理

5. ライフサイクル管理
   ├─ Retention ポリシー：「直近 N 個だけ保持」等のルールで自動削除
   ├─ Immutable タグ  ：本番タグの上書きを禁止
   └─ GC（ガベージコレクション）：未参照 Blob の定期クリーンアップ

6. マルチサイト運用（必要に応じて）
   └─ レプリケーションポリシーで他 Harbor / Docker Hub / ECR / ACR 等と同期
```

---

### アーキテクチャ概観

```
[ユーザー / CI/CD] ──HTTPS──▶ [Nginx Proxy]
                                  ├──▶ Portal (Angular UI)
                                  ├──▶ Core API (Go / Beego)
                                  │      ├── RBAC・認証・ポリシー管理
                                  │      └── PostgreSQL / Redis
                                  ├──▶ Registry (OCI Distribution)
                                  │      └── Registryctl
                                  └──▶ Job Service (非同期タスク)
                                         ├── スキャン / レプリケーション
                                         └── GC / Retention / Webhook
```
