---
url: https://github.com/sherlock-project/sherlock
keywords: OSINT, username-search, social-media, reconnaissance, Python
oneliner: ユーザー名を入力するだけで381以上のSNS・Webサービスからアカウントの存在を一括検索するOSINTツール。
---

## Sherlock — ユーザー名によるソーシャルアカウント横断検索ツール

### これは何？

Sherlock は、指定したユーザー名が **381 以上の SNS・Web サービス** に存在するかを一括で並列検索する Python 製の CLI ツール。GitHub、Twitter/X、Instagram、Reddit、Qiita など多種多様なサイトに対応し、各サイトへの HTTP リクエスト結果（ステータスコード・レスポンス本文・リダイレクト先）を解析して「アカウントが存在するか否か」を判定する。

検出方式はサイトごとに 3 種類使い分けている:

| 方式 | 判定ロジック |
|---|---|
| `status_code` | 404 等の特定ステータスコードで「不在」と判定 |
| `message` | レスポンス本文中のエラーメッセージの有無で判定 |
| `response_url` | リダイレクト先 URL で判定 |

### 何が嬉しいのか？（既存手段との比較）

| 観点 | 手動検索 / Google検索 | 類似ツール (Namechk等 Web版) | **Sherlock** |
|---|---|---|---|
| **対応サイト数** | 1つずつ手動 | 数十〜百程度 | **381+（随時更新）** |
| **速度** | 非常に遅い | 中程度 | **20並列リクエストで高速** |
| **プライバシー** | — | 第三者サービスに依存 | **ローカル実行、ログなし** |
| **カスタマイズ性** | なし | なし | プロキシ/Tor対応、サイト絞り込み、NSFW除外、独自サイト追加可 |
| **出力形式** | — | Web画面のみ | **コンソール / TXT / CSV / XLSX** |
| **自動化** | 困難 | API次第 | CLI でパイプライン連携容易 |

特に **OSINT（公開情報調査）** の文脈で、セキュリティ調査・ペネトレーションテスト・自分のデジタルフットプリント確認に重宝される。Kali Linux や BlackArch にも公式パッケージとして収録されている点が信頼性を裏付ける。

### 使い方の流れ

```
1. インストール
   $ pipx install sherlock-project   # または docker / brew / apt

2. 基本検索（ユーザー名を指定するだけ）
   $ sherlock john_doe
   → 381サイトに並列リクエスト → 見つかったプロフィールURLをリアルタイム表示

3. よく使うオプション
   $ sherlock john_doe jane_doe      # 複数ユーザー名を同時検索
   $ sherlock --site GitHub --site Twitter john_doe  # 特定サイトに絞る
   $ sherlock --csv --xlsx john_doe  # CSV/Excelで結果を保存
   $ sherlock --tor john_doe         # Tor経由で匿名検索
   $ sherlock --nsfw john_doe        # NSFWサイトも含める
   $ sherlock "john{?}doe"           # john_doe, john-doe, john.doe を一括生成

4. 結果の確認
   - コンソール: 色付きでリアルタイム表示（緑=発見、黄=不明、赤=未発見）
   - ファイル: john_doe.txt に発見URLが一覧保存される
   - --browse オプションで見つかったURLをブラウザで一括オープン
```

**アーキテクチャ要点**: サイト定義は `resources/data.json` に集約されており、デフォルトでは起動時に GitHub 上の最新版を取得する。これにより、ツール本体を更新しなくてもサイト対応状況が常に最新に保たれる設計になっている。
