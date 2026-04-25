---
url: https://github.com/Universal-Commerce-Protocol/ucp
keywords: オープンスタンダード, AIエージェント, 商取引プロトコル, JSON Schema, 決済相互運用性
oneliner: AIエージェントと複数プラットフォーム間でEC取引を安全に自動化するためのオープン商取引仕様。
---

## このリポジトリは何？

**Universal Commerce Protocol (UCP)** は、AIエージェント・EC プラットフォーム・決済サービスプロバイダー（PSP）・ブランド間の商取引を統一するオープン標準仕様。Google・Shopify・Walmart・Target・Etsy が共同設計し、Stripe・PayPal・Visa・Adyen など 30 社以上が採用推奨している。

実体は「コードライブラリ」ではなく「仕様書 ＋ JSON Schema ＋ OpenAPI/JSON-RPC 定義のセット」。Python は MkDocs によるドキュメント自動生成のためだけに使われる。

**カバーする機能:**

| Capability | 内容 |
|---|---|
| Checkout | セッション管理・カート・税計算・配送 |
| Identity Linking | OAuth 2.0 による安全なアカウント連携 |
| Order | Webhook ベースの注文ライフサイクル管理 |
| Catalog | 商品検索・商品詳細ルックアップ |
| Payment Token Exchange | PSP ↔ 認証情報プロバイダー間トークン交換 |

---

## 何が嬉しいの？既存の似た手段との比較

### 課題：既存手段の断片化

| 既存手段 | 限界 |
|---|---|
| 各 EC の独自 API（Shopify API 等） | プラットフォーム固有。乗り換え・連携コスト大 |
| Stripe / PayPal 等の決済 SDK | 決済に特化。カート・注文・配送は別途自前実装 |
| OpenAPI 仕様書（個社作成） | 命名・フロー・セキュリティモデルが標準化されていない |
| Model Context Protocol (MCP) 単体 | AI ↔ ツール呼び出しのトランスポート層のみ。商取引セマンティクスなし |

### UCP の優位点

1. **転送プロトコル非依存** — 同一スキーマを REST・MCP（AI エージェント向け）・A2A（Agent-to-Agent）で使い回せる
2. **AIエージェント対応を正面から設計** — LLM がユーザー代理で購入・支払いを行うユースケースを想定済み
3. **セキュリティが組み込み** — AP2 支払い委任・メッセージ署名（Content-Digest / Signature ヘッダー）・OAuth 2.0 が仕様に含まれる
4. **拡張性** — Capabilities（コア機能）＋ Extensions（割引・AP2 Mandate 等）の分離設計。逆ドメイン名前空間で独自拡張も衝突しない
5. **業界横断の支持** — 主要プラットフォーム・PSP が仕様策定に参加しているため、実装後の相互接続ハードルが低い

---

## 使うときはどういう流れに沿う？

### 登場ロール

```
Platform（EC プラットフォーム）
Business（ブランド・ストア）
CP（Credential Provider：Google Pay 等）
PSP（Payment Service Provider：Stripe 等）
```

### 典型フロー：AIエージェントによる購買

```
① Discover          ユーザーの AI エージェントが UCP 対応ストアのエンドポイントを検出
② Checkout Session  POST /checkout-sessions でセッション開始
                    → status: incomplete
③ Cart 構築         カートにアイテム・配送先・支払い方法を PATCH で積み上げ
④ Identity Link     OAuth 2.0 でユーザーアカウントとエージェントを安全に紐づけ
⑤ Payment Token     CP（例：Google Pay）と PSP（例：Stripe）間でトークン交換
⑥ Complete         status が ready_for_complete になったら決済確定
⑦ Order Webhook    ストアから注文ステータス更新を Webhook で受信
```

### 実装者別の入口

| 立場 | やること |
|---|---|
| **Platform/Business** | `source/services/shopping/rest.openapi.json` を実装。JSON Schema の checkout/cart/order に準拠したレスポンスを返す |
| **AI エージェント開発者** | `source/services/shopping/mcp.openrpc.json` を使い MCP ツールとして Checkout Session を呼ぶ |
| **PSP/CP** | `docs/specification/payment-handler-guide.md` に従い Payment Token Exchange・署名検証を実装 |
| **仕様確認** | `https://ucp.dev`（MkDocs でビルドされたサイト）または `docs/specification/` を参照 |
| **適合性テスト** | 別リポジトリ `Universal-Commerce-Protocol/conformance` で Conformance Test を実行 |

---

一言で言えば「**EC 版の OpenID Connect**」。異なるプラットフォーム間を跨いで AI が安全に買い物できるように、認証・カート・決済・注文の全ステップを標準化した仕様です。
