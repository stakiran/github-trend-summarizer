---
url: https://github.com/KeygraphHQ/shannon
keywords: AI pentesting, vulnerability assessment, Claude Agent SDK, Temporal workflow, security automation
oneliner: Claude Agent SDKを活用し、ソースコード解析から脆弱性の実証攻撃までを自律的に行うAIペネトレーションテストツール。
---

## Shannon — AI 自律型ペネトレーションテスター

### これは何？

Shannon は、Webアプリケーション／APIを対象とした**ホワイトボックス型の自律AIペンテストエージェント**。ソースコードと稼働中のアプリの両方にアクセスし、偵察→脆弱性分析→実証攻撃→レポート生成までの一連のセキュリティ監査を全自動で実行する。

内部構成は以下の通り：

| 層 | 技術 | 役割 |
|---|---|---|
| **オーケストレーション** | Temporal（耐障害ワークフロー） | 5フェーズのパイプライン制御・再開・リトライ |
| **AI エンジン** | Claude Agent SDK | 各フェーズのエージェントが自律的にコード分析・攻撃手法の立案・実行 |
| **セキュリティツール** | nmap, subfinder, WhatWeb, schemathesis | ポートスキャン、サブドメイン探索、技術スタック特定、APIファジング |
| **ブラウザ操作** | Playwright | ログインフロー、XSS実証、セッション操作 |
| **実行環境** | Docker（エフェメラルコンテナ） | スキャンごとに隔離された使い捨て環境 |

5つのフェーズ（**事前偵察 → 偵察 → 脆弱性分析×5並列 → 実証攻撃×5並列 → レポート**）が順次・並列に進行し、最終的にエグゼクティブ向けセキュリティレポートを出力する。

### 何が嬉しいのか？（既存手段との比較）

| 比較軸 | 従来のスキャナー（OWASP ZAP, Burp Suite等） | 手動ペンテスト | **Shannon** |
|---|---|---|---|
| ソースコード理解 | ✗ ブラックボックスのみ | △ 人が読む | **◎ AIがコード全体を解析** |
| 実証攻撃の自動化 | △ 定型パターンのみ | ◎ 人が創意工夫 | **○ AIが文脈を踏まえて攻撃を組み立て** |
| カバー範囲 | シグネチャベース・既知パターン | 広いが工数に依存 | **認可不備・ビジネスロジック等の論理的脆弱性にも対応** |
| コスト・時間 | 安い／速い | 高い／遅い（数日〜数週間） | **API利用料のみ／数十分〜数時間** |
| 再現性 | 高い | 低い（属人的） | **高い（同一設定で再実行可能）** |

要するに、「**ソースコードを読めるペンテスターが、ツールも駆使しながら自律的に検査してくれる**」という体験を、AIエージェントで実現している点が最大の差別化ポイント。

### 使うときの流れ

```
1. 準備
   ├─ Docker をインストール
   ├─ Anthropic API キーを取得
   └─ テスト対象のソースコードを用意

2. セットアップ（npx の場合）
   $ npx @keygraph/shannon setup     ← 対話式ウィザードで認証情報を設定
   （ローカルの場合は .env に ANTHROPIC_API_KEY を書くだけ）

3. スキャン実行
   $ npx @keygraph/shannon start -u https://target.example.com -r ./my-app
   　　オプション:
   　　  -c config.yaml   … 認証情報・スコープ制限等のYAML設定
   　　  -w my-audit      … 名前付きワークスペース（中断再開に対応）
   　　  --pipeline-testing … 軽量モードで素早く動作確認

4. モニタリング
   $ npx @keygraph/shannon logs my-audit   ← ログをリアルタイム確認
   　　Temporal Web UI (http://localhost:8233) でも進捗を可視化可能

5. 結果確認
   └─ 対象リポジトリの .shannon/deliverables/ にレポートが出力される
      └─ comprehensive_security_assessment_report.md（最終レポート）

6. 後片付け
   $ npx @keygraph/shannon stop [--clean]
```

認証付きアプリの場合は YAML 設定ファイルでログインフロー（フォーム認証・SSO・API・Basic認証）や TOTP シークレットを指定でき、エージェントが自動でログインしてからテストを行う。
