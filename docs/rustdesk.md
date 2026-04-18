---
url: https://github.com/rustdesk/rustdesk
keywords: Rust, リモートデスクトップ, セルフホスト, TeamViewer代替, P2P, Flutter, TCPホールパンチング, リレーサーバー
oneliner: Rust製のオープンソースなリモートデスクトップソフトで、TeamViewer/AnyDeskの代替として設定不要で動作し、サーバーを自分で建てれば完全にデータを自己管理できる。
---

# RustDesk リポジトリ概要

## このリポジトリは何？

**RustDesk** は、Rust で書かれたオープンソースのリモートデスクトップアプリケーションのソースコードリポジトリです。TeamViewer / AnyDesk のような「離れた場所の PC を遠隔操作する」ソフトウェアを、**自己ホスト（セルフホスト）可能な形**で提供することを目的としています。

主な構成要素：

- **`src/`**：Rust 製のコア。`src/client.rs`（ピア接続）、`src/server/`（音声・クリップボード・入力・映像サービスと通信）、`src/rendezvous_mediator.rs`（rustdesk-server との通信、TCP ホールパンチや中継接続の待ち受け）、`src/platform/`（OS 依存コード）。
- **`libs/`**：再利用ライブラリ。`hbb_common`（ビデオコーデック・設定・TCP/UDP ラッパ・protobuf・ファイル転送用 FS 関数）、`scrap`（画面キャプチャ）、`enigo`（キーボード/マウス制御）、`clipboard`（ファイルのコピー&ペースト）。
- **`flutter/`**：デスクトップ/モバイル向け新 UI（旧 Sciter UI は deprecated）。Web クライアント用 JS も含む。
- **ビルド関連**：`Cargo.toml`, `build.py`, `Dockerfile`, `vcpkg.json`, `flatpak/`, `appimage/`, `fastlane/` などで Windows / Linux / macOS / iOS / Android / Web まで幅広くカバー。

ライセンスは AGPL-3.0（`LICENCE`）。クライアント本体のみがこのリポジトリで、サーバー（rustdesk-server）は別リポジトリです。

## 既存手段と比べて何が嬉しい？

| 観点 | TeamViewer / AnyDesk | VNC / RDP | **RustDesk** |
|---|---|---|---|
| ライセンス | 商用・商用利用は有料 | 大抵 OSS | **OSS（AGPL）・無料** |
| セルフホスト | 原則不可 | 可だが NAT越えが面倒 | **公式リレー/ランデブーサーバを自前で建てられる** |
| NAT 越え | 対応 | 基本対応せず | **TCP ホールパンチング＋リレーで自動対応** |
| セットアップ | アカウント必要 | 転送設定が必要 | **ダウンロードして即起動、設定不要** |
| データ管理 | ベンダー依存 | 自社内 | **自前サーバーならデータが外に出ない** |
| 性能 | ○ | 画質・速度で見劣り | **Rust＋VP9/AV1/Opus でネイティブ性能** |

要するに「**TeamViewer の使い勝手の良さ**」と「**VNC 級の自己完結性**」を両立させ、さらに Rust ならではの速度・安全性とマルチプラットフォーム対応（Win/macOS/Linux/iOS/Android/Web）を備えたのが強みです。商用ライセンス料や突然のアカウント BAN、帯域制限に悩まされずに済みます。

## 使うときの流れ

### A. エンドユーザーとしての利用

1. [Releases](https://github.com/rustdesk/rustdesk/releases) からインストーラを入手（F-Droid / Flathub も可）。
2. 操作される側・する側の両 PC で起動すると、各端末に 9 桁の ID とパスワードが自動表示される。
3. 操作する側で相手の ID を入力し、パスワードを入れれば即リモート接続。公式ランデブー/リレーサーバが自動で仲介。
4. 必要に応じて **画面共有・ファイル転送・TCP トンネリング** などのモードを切り替える。

### B. 自前サーバー運用（プライバシー重視の典型パターン）

1. [rustdesk-server](https://github.com/rustdesk/rustdesk-server) を VPS などに立てる。
2. クライアント側の設定で自分のランデブー/リレーサーバーのアドレスと鍵を登録。
3. 以降すべての接続は自分のサーバーを経由 → データが第三者クラウドを経由しない。

### C. 開発者としてソースからビルド

1. Rust ツールチェインと C++ ビルド環境を用意。
2. `vcpkg` をインストールし、`libvpx / libyuv / opus / aom` を入れて `VCPKG_ROOT` を設定。
3. Sciter の動的ライブラリを `target/debug` に配置（Sciter 版の場合）。
4. `git clone --recurse-submodules https://github.com/rustdesk/rustdesk` → `cargo run` で起動。
5. 面倒なら **Docker ビルド**：`docker build -t rustdesk-builder .` してコンテナ内でビルドすると依存解決を丸投げできる。Flutter 版は GitHub Actions の CI ワークフロー（`.github/workflows/flutter-build.yml`）が参考実装。
