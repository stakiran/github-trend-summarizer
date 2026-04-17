---
url: https://github.com/BasedHardware/omi
keywords: AI wearable, 2nd brain, transcription, conversation capture, open source
oneliner: 画面と会話を24時間キャプチャしてリアルタイム文字起こし・要約・AIチャットを提供する、オープンソースの"第2の脳"プラットフォーム（ウェアラブル／スマホ／デスクトップ対応）。
---

# BasedHardware/omi

## このリポジトリは何？

**omi** は「自分の1st brainよりも信頼できる2nd brain」をうたう、オープンソースの常時キャプチャ型 AI アシスタント。主要言語は Dart（モバイルアプリ）で、以下のコンポーネントを単一リポジトリで束ねている。

| コンポーネント | ディレクトリ | 技術 |
|---|---|---|
| macOS デスクトップアプリ | `desktop/` | Swift + SwiftUI + Rust バックエンド |
| モバイルアプリ (iOS/Android) | `app/` | Flutter |
| バックエンド API | `backend/` | Python (FastAPI), Firebase, Firestore, Redis |
| ウェアラブル本体 ファーム | `omi/` | nRF + Zephyr (C) |
| スマートグラス ファーム | `omiGlass/` | ESP32-S3 (C) |
| SDK | `sdks/` | Python / Swift / React Native |
| MCP サーバ | `mcp/` | Model Context Protocol 連携 |
| プラグイン / ペルソナ | `plugins/`, `web/` | Next.js 他 |

バックエンドは Listen (REST)・Pusher (WebSocket)・VAD・Diarizer (GPU) のマイクロサービス構成で、STT に Deepgram、保存に Firestore、キャッシュに Redis、要約・チャットに LLM を使う。既に 30 万人以上が利用中、ライセンスは MIT。

## このリポジトリは何が嬉しいの？（類似手段との比較）

**コアバリュー**：画面 + 音声 + ウェアラブルの入力を一元化し、「見聞きしたすべてを覚えているチャット」と「要約・アクションアイテム自動生成」を提供する。

- **Rewind.ai / Limitless Pendant / Humane Pin と比較**：それらは基本的にクローズドな SaaS＋ハード。omi は **ハードウェアの回路図まで含めて全部 OSS（MIT）**。自前ビルド・自前ホスティング・プラグイン自作が可能で、ベンダーロックインが無い。
- **Otter.ai / Fireflies 等の議事録 SaaS と比較**：Otter 系は「会議の文字起こし」が中心。omi は**会議に限らず画面と生活全体を 24 時間キャプチャ**し、後からチャットで横断検索できる。さらに action items や memory として構造化され、REST API / SDK / MCP 経由で他ツール（Slack, GitHub, 独自 LLM）へ流せる。
- **ChatGPT / Claude Desktop と比較**：単なる対話 LLM ではなく、**自分の過去の発話・画面の文脈をすべて注入したうえで回答**してくれる。「あの会議で誰が何を約束したか」「先週見た記事の要点は」を即答できる。
- **自作スクリプト派と比較**：STT / 話者分離 / VAD / LLM 要約 / BLE プロトコル / Firestore 同期 / マルチプラットフォーム UI が**すでに統合済み**。Helm チャートと Modal ジョブで本番運用構成まで含まれている。

要するに「Rewind のフルスタック版を MIT でフォーク＆自作できる」のが最大の嬉しさ。

## 使うときの流れ

**(A) 利用者として試す（クラウドBE利用）**
1. macOS / iOS / Android 版をストア or `macos.omi.me` からインストール、もしくは `app.omi.me` をブラウザで開く。
2. ワンライナーで動作確認：`git clone … && cd omi/desktop && ./run.sh --yolo`（macOS 14+, Xcode, Node.js 必須）。
3. アプリが画面キャプチャ＋マイクを常時取り込み → クラウドでリアルタイム文字起こし → タイムライン・要約・アクションアイテム・AI チャットが UI に表示される。
4. 必要なら **Omi ウェアラブル**（BLE 接続）や **Omi Glass**（ESP32-S3、カメラ＋音声）を追加して 24 時間キャプチャに拡張。

**(B) 開発者としてフル自前構築**
1. 前提導入：`xcode-select --install`、Rust toolchain。
2. `desktop/Backend-Rust/.env.example` をコピーして認証情報を設定。`./run.sh` で起動。
3. モバイル開発は `cd app && bash setup.sh ios|android`、バックエンドは `backend/` の FastAPI をローカル起動（Firestore / Redis / Deepgram の接続先を設定）。
4. 機能追加は `plugins/` や SDK (`sdks/python`, `swift`, `react-native`) 経由でプラグイン化、または `mcp/` で Model Context Protocol サーバとして LLM クライアントに接続。
5. コミット前に pre-commit hook をリンク（`scripts/pre-commit`）。フォーマッタは Dart=120、Python=black 120、C/C++=clang-format。`backend/test.sh` / `app/test.sh` で検証してから PR（squash merge は禁止、regular merge のみ）。

**(C) ハードも自作したい場合**：`omi/`（ウェアラブル）・`omiGlass/`（グラス）にある回路図・BOM・Zephyr/ESP32 ファームを flash するだけで、市販 Omi を買わずに同等環境を再現できる。
