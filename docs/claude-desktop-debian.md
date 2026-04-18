---
url: https://github.com/aaddrick/claude-desktop-debian
keywords: Claude Desktop, Linux, Electron, Debian, AppImage, RPM, Nix, AUR, MCP, パッケージング
oneliner: Windows 版 Claude Desktop を Linux ネイティブで動作するように再パッケージングするビルドスクリプト集。
---

# aaddrick/claude-desktop-debian 整理メモ

## このリポジトリは何？

Anthropic 社の AI デスクトップアプリ **Claude Desktop**（公式には Windows / macOS のみ提供）を、**Linux でネイティブに動かすための非公式ビルドスクリプト集**。

- 公式の Windows インストーラ（`.exe`）を取得 → `7z` で展開 → 内部の `app.asar`（Electron アプリ本体）を抽出 → Linux 向けに `sed`/正規表現でパッチ（BrowserWindow の `frame`、ネイティブトレイ、テーマ周りなど）を当て直し、各種 Linux パッケージ形式に再構成する。
- 出力形式は多彩：
  - `.deb`（Debian / Ubuntu / Mint）
  - `.rpm`（Fedora / RHEL / CentOS）
  - `.AppImage`（ディストロ非依存）
  - **AUR** パッケージ `claude-desktop-appimage`（Arch）
  - **Nix flake**（NixOS、`claude-desktop` と FHS 版 `claude-desktop-fhs`）
- さらに GitHub Pages 上で **APT / DNF リポジトリ**を公開しており、`apt upgrade` / `dnf upgrade` で自動更新可能。
- 主要スクリプトは `build.sh`（bash、STYLEGUIDE 準拠・shellcheck/actionlint 対応）、参照用のビーティファイ済みソースを `build-reference/` に置き、ミニファイ変数名の変化に耐える正規表現戦略を採る。
- **MCP (Model Context Protocol)** をサポート（設定は `~/.config/Claude/claude_desktop_config.json`）、グローバルホットキー（Ctrl+Alt+Space、X11 / Wayland）、システムトレイ連携、`--doctor` 診断コマンドを内蔵。実験機能として Cowork モード（bubblewrap サンドボックス or ホスト直実行）も既定で有効。

## 何が嬉しいのか（既存手段との比較）

| 手段 | 代償 | 本リポジトリとの差 |
|------|------|--------------------|
| Wine / Bottles で Windows 版を動かす | 起動遅い・IME 崩壊・トレイ/ホットキー/MCP 不安定 | 本物の Linux ネイティブ Electron として動くため IME・Wayland・トレイが素直に通る |
| ブラウザ版 claude.ai を PWA | デスクトップ機能（MCP、グローバルホットキー、トレイ常駐）が使えない | MCP とホットキー、トレイ常駐までそのまま使える |
| 先行の k3d3 製 `claude-desktop-linux-flake` | NixOS 専用、メンテ停止気味 | **deb/rpm/AppImage/AUR/Nix を一括カバー**。APT/DNF リポジトリまで提供し、自動更新まで面倒を見る |
| 自前で `.exe` を展開してパッチ | ミニファイ変数が毎リリース変わり壊れる | `build.sh` が正規表現＋動的変数抽出で追従、CI が**上流バージョンの自動検知と URL 更新**（`check-claude-version` workflow）まで実施 |
| Electron アプリ一般を AppImage 化するだけ | Linux 固有のトレイアイコン / 枠なしウィンドウ / ネイティブテーマ問題が残る | `frame-fix-wrapper.js` によるラッパー注入、トレイアイコン差し替え、Wayland/XWayland 対応など **Linux 固有バグのパッチが蓄積**（`docs/learnings/` に知見も集約） |

要するに「Claude Desktop を Linux で**ちゃんと普通に使う**」ための、**ディストロ網羅・自動更新・MCP 対応**をワンストップで整えた実装。個別に Wine 起動やブラウザ PWA で済ませるよりも、ネイティブ機能（MCP、ホットキー、トレイ）が揃い、メンテナンス負荷も肩代わりされる。

## 使うときの流れ

### A. エンドユーザとして入れる（推奨）
1. 自分のディストロに応じて選ぶ：
   - **Debian/Ubuntu**: GPG 鍵を `/usr/share/keyrings/` に置き、`deb https://aaddrick.github.io/claude-desktop-debian stable main` を登録 → `sudo apt install claude-desktop`。
   - **Fedora/RHEL**: `claude-desktop.repo` を `/etc/yum.repos.d/` に置いて `sudo dnf install claude-desktop`。
   - **Arch**: `yay -S claude-desktop-appimage`（または `paru`）。
   - **NixOS**: `nix profile install github:aaddrick/claude-desktop-debian`（MCP 付きなら `#claude-desktop-fhs`）。
   - それ以外 / お試し: [Releases](https://github.com/aaddrick/claude-desktop-debian/releases) から `.deb` / `.rpm` / `.AppImage` を直接ダウンロード。
2. 初回起動後、必要に応じて `~/.config/Claude/claude_desktop_config.json` に MCP サーバ設定を追加。
3. 不調なら `claude-desktop --doctor` を実行し、表示サーバ・サンドボックス・MCP 設定・トレイ backend の健全性を確認。

### B. 自分でビルドする / 開発する
1. `git clone` 後、`./build.sh` を実行（ディストロを自動判定してフォーマット選択）。
2. 明示指定する場合: `./build.sh --build {deb|rpm|appimage|nix}`、デバッグ時は `--clean no`、上流配布が古い時は `--exe /path/to/Claude-Setup.exe` でローカルのインストーラを流用。
3. 内部的には「`.exe` 展開 → `app.asar` → `asar extract` → `sed -E` で正規表現パッチ → ラッパー JS (`frame-fix-entry.js` / `frame-fix-wrapper.js`) 注入 → 再梱包 → パッケージング」の順。
4. ソース調査は `build-reference/app-extracted/.vite/build/*.js`（prettier 整形済み）を読み、本物の minified コードとは空白揺れが違う点に注意しながら正規表現を書く。
5. コミット前に `/lint`（shellcheck + actionlint）で静的解析。CI は GitHub Actions で走り、タグ `v{REPO_VERSION}+claude{CLAUDE_DESKTOP_VERSION}` を push するとリリース build がトリガされ、deb/rpm/AppImage 成果物と APT/DNF リポジトリ更新が同時に回る。
6. 上流 Claude Desktop の新版が出ると `check-claude-version` workflow が `CLAUDE_DESKTOP_VERSION` 変数と `build.sh` の URL を自動更新 → 新タグ作成まで無人で進む。
