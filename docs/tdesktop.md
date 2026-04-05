---
url: https://github.com/telegramdesktop/tdesktop
keywords: telegram, desktop-messenger, cpp, qt, mtproto
oneliner: Telegram公式のデスクトップ向けメッセージングクライアントのオープンソース実装
---

# Telegram Desktop (`tdesktop`)

## これは何？

Telegram公式が開発・公開している**デスクトップ向けメッセージングアプリ**のソースコード。C++ / Qt で構築され、Windows 7+・macOS 10.13+・Linux をサポートする。GPLv3 ライセンスで公開されており、誰でもビルド・改変・再配布が可能。

アーキテクチャは大きく以下の層に分かれる。

| 層 | 役割 | 主要ディレクトリ |
|---|---|---|
| **Core / Launcher** | アプリ起動・設定・クラッシュレポート | `core/`, `main/` |
| **MTProto / API** | Telegram独自の暗号化通信プロトコル実装 | `mtproto/`, `api/` |
| **Data / Storage** | メッセージ・チャット・ユーザーのデータモデルとDB | `data/`, `storage/` |
| **UI / Window** | Qt ベースのウィジェット・スタイルシステム | `ui/`, `window/`, `dialogs/` |
| **機能モジュール** | 通話(WebRTC)・メディア再生・決済・パスポート等 | `calls/`, `media/`, `payment/` |

内部ライブラリ群（`lib_rpl`=リアクティブ、`lib_crl`=コルーチン、`lib_ui`=UI部品）を自前で持ち、外部には Qt6・OpenSSL・FFmpeg・WebRTC などに依存する。

---

## 何が嬉しいのか？（既存手段との比較）

| 観点 | tdesktop | Electron系クライアント (Signal Desktop等) | Web版 Telegram |
|---|---|---|---|
| **パフォーマンス** | C++/Qt ネイティブで軽量・高速 | Chromium同梱で重い (RAM 300MB~) | ブラウザ依存 |
| **機能の完全性** | モバイル版とほぼ同等（通話・E2E暗号化・ステッカー・決済） | アプリごとに差がある | 通話やファイル操作に制限あり |
| **カスタマイズ性** | ソースが公開されており自前ビルド可能。API ID を取得すれば独自クライアントも作れる | 多くは非公開または制限付き | 不可 |
| **プラットフォーム対応** | Win/macOS/Linux を1つのコードベースでカバー + Snap/Flatpak | 同様だが実行環境が重い | ブラウザがあればどこでも |
| **セキュリティ** | MTProto を C++ でネイティブ実装。E2E暗号化対応 | 同等 | TLS+サーバー依存 |

要するに「**公式品質のネイティブデスクトップクライアントを、オープンソースで自由に検証・改変できる**」点が最大の価値。サードパーティ開発者にとっては Telegram クライアント開発の実質的なリファレンス実装でもある。

---

## 使うときの流れ

### A. エンドユーザーとして使う場合

1. [公式サイト](https://desktop.telegram.org/) または各OS のパッケージマネージャ（Snap, Flatpak, Homebrew 等）からインストール
2. 電話番号で認証 → すぐに利用開始

### B. ソースからビルドする場合

```
1. 前提準備
   - Telegram API で api_id / api_hash を取得（https://my.telegram.org）
   - OS ごとの依存ツールを用意（CMake 3.25+, Python 3, コンパイラ）

2. ソース取得
   $ git clone --recursive https://github.com/telegramdesktop/tdesktop.git

3. ビルド（OS別）
   - Linux:  Docker ベースのビルドスクリプト（docs/building-linux.md）
   - macOS:  シェルスクリプト + Xcode（約55GB のディスク要）
   - Windows: configure.bat → MSVC でビルド

4. 実行
   ビルド成果物の Telegram バイナリを起動 → 電話番号認証
```

### C. 開発・改変する場合

1. 上記 B の手順でビルド環境を構築
2. `Telegram/SourceFiles/` 以下の該当モジュールを編集
3. スタイル変更は `.style` ファイル → ビルド時にC++コード生成
4. API層の変更は TL スキーマ（`td_scheme.cmake`）経由で型安全にコード生成
5. ビルド → 動作確認 → PR 提出
