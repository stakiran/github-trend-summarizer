---
url: https://github.com/TelegramMessenger/Telegram-iOS
keywords: Telegram, iOS, Swift, メッセンジャー, オープンソース
oneliner: Telegram公式のiOSクライアントアプリの完全なソースコード
---

## Telegram-iOS — リポジトリ概要

### これは何？

**Telegram公式が公開している、iOS版Telegramアプリの完全なソースコード**である。Swift/Objective-Cで書かれており、Bazelビルドシステムで構築される。350以上のサブモジュールに分割された大規模なモジュラーアーキテクチャを持ち、メッセージング・通話（WebRTC）・メディア処理・暗号化・ウィジェット・Apple Watch対応など、アプリの全機能が含まれている。

主要な構成は以下の通り：

| ディレクトリ | 役割 |
|---|---|
| `Telegram/` | メインアプリ本体と各種Extension（通知・共有・Siri・Widget等） |
| `submodules/` | 350超のモジュール群（UI・ネットワーク・暗号化・メディア等） |
| `third-party/` | 外部依存ライブラリ（WebRTC, libvpx, dav1d等） |
| `build-system/` | Bazelベースのビルド構成・スクリプト群 |

### 何が嬉しいのか？（既存手段との比較）

| 観点 | Telegram-iOS | 一般的なOSSメッセンジャー (Signal等) |
|---|---|---|
| **公式クライアント** | Telegram公式がメンテナンスする本番コード | Signalも公式だが、機能の幅はTelegramが圧倒的 |
| **カスタムビルド** | 自前のAPI IDを取得し、独自ビルド版を作成・配布可能 | 多くのOSSアプリでも可能だが、Telegramほど手順が整備されていない |
| **学習教材としての価値** | 数百万ユーザーが使う商用品質のiOSアプリ設計を学べる。モジュール分割・非同期処理・UIアーキテクチャの実例として極めて貴重 | 同規模のOSS iOSアプリは非常に少ない |
| **透明性・検証** | 暗号化やプロトコル（MTProto）の実装を第三者が監査可能 | Signalも同様だが、Telegramはサーバー非公開のため、クライアント検証の重要度が高い |
| **拡張・改変** | フォークして独自機能を追加したカスタムクライアントを開発可能（Nicegram等が実例） | Signal系は改変版の配布に制限がある場合も |

### 使うときの流れ

**前提:** macOS環境、Xcode 26.2、Bazel 8.4.2 が必要。

```
1. リポジトリをクローン
   $ git clone --recursive -j8 https://github.com/TelegramMessenger/Telegram-iOS.git

2. Telegram APIの認証情報を取得
   → https://my.telegram.org からアプリを登録し、api_id / api_hash を取得

3. 開発用設定ファイルを作成
   → build-system/template_minimal_development_configuration.json を編集
   → Team ID（Apple Developer）やAPI情報を記入

4. Xcodeプロジェクトを生成
   $ python3 build-system/Make/Make.py \
       --cacheDir="$HOME/telegram-bazel-cache" \
       generateProject \
       --configurationPath=<設定ファイルパス> \
       --xcodeManagedCodesigning

5. Xcodeで開いてビルド・実行
   → シミュレータのみなら --disableProvisioningProfiles を追加
   → IPA生成は generateProject の代わりに build コマンドを使用
```

> **注意:** Telegramのブランド名・ロゴを使った非公式アプリの配布にはライセンス上の制約がある。カスタムビルドを公開する場合は、名称やアイコンの変更が必要。
