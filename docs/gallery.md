---
url: https://github.com/google-ai-edge/gallery
keywords: on-device-ai, android, llm-inference, mediapipe, gemma
oneliner: オープンソースLLMをスマートフォン上で完全オフライン実行できるデモ・実験用Androidアプリ
---

## Google AI Edge Gallery — 概要整理

### このリポジトリは何？

**スマートフォン上でLLM（大規模言語モデル）を完全にオンデバイスで動かすためのAndroid/iOSアプリ**のソースコード。Google が開発し、Play Store / App Store でも公開されている。

内部では **LiteRT（TensorFlow Lite 次世代）+ MediaPipe LLM API** を推論エンジンとして使い、Gemma 3n、Gemma 3 1B、Qwen 2.5 などのモデルを `.task` 形式でダウンロードしてローカル実行する。主な機能は以下の通り：

| 機能 | 内容 |
|---|---|
| **LLM Chat** | マルチターン会話（ストリーミング応答・思考過程表示対応） |
| **Prompt Lab** | temperature/top-k 等を細かく調整してシングルターン評価 |
| **Ask Image** | 画像を入力してマルチモーダル質問 |
| **Agent Skills** | JavaScript やネイティブ Intent で LLM の能力を拡張（地図表示、QRコード生成、メール送信など） |
| **Benchmark** | 推論速度・トークンスループットの計測 |

---

### 何が嬉しいの？（既存手段との比較）

| 観点 | Google AI Edge Gallery | クラウドAPI（Gemini API等） | 他のオンデバイス手段（llama.cpp, MLC-LLM等） |
|---|---|---|---|
| **プライバシー** | ◎ 全データ端末内完結 | △ サーバーに送信 | ◎ 同等 |
| **ネットワーク** | 不要（DL後） | 必須 | 不要（DL後） |
| **導入の手軽さ** | ◎ アプリをインストールするだけ | ◎ APIキー取得のみ | △ ビルド・変換作業が必要 |
| **拡張性** | ◎ Skill プラグインで JS/Intent 拡張可能 | ○ Function Calling | △ 自前実装 |
| **GPU最適化** | ◎ LiteRT が自動でGPU/CPUフォールバック | N/A | ○ バックエンド依存 |
| **対象ユーザー** | 開発者〜一般ユーザー | 開発者 | 上級開発者 |

**一言で言えば**：「オンデバイスLLMを**誰でもすぐ試せる**完成度の高いリファレンスアプリ」であることが最大の価値。llama.cpp 等はビルドやモデル変換の知識が必要だが、本アプリはモデル選択→ダウンロード→即会話、で完結する。さらに Skill システムにより function calling を活用した実用的なエージェント体験まで試せる。

---

### 使うときの流れ

```
1. インストール
   ├─ Play Store / App Store からインストール（一般ユーザー）
   └─ ソースからビルド（開発者：Android Studio で Android/src/ を開く）

2. モデルの取得
   ├─ アプリ内のモデル一覧から選択（Gemma 3n E2B 〜3.1GB 等）
   └─ Hugging Face 連携で自動ダウンロード → 端末ストレージに保存

3. タスクを選んで実行
   ├─ Chat：マルチターン会話を開始
   ├─ Prompt Lab：パラメータを調整しながら単発プロンプトを試す
   ├─ Ask Image：カメラや画像ファイルでマルチモーダル推論
   └─ Agent Skills：スキルをロードして拡張機能を使う
       ├─ 組み込みスキル（QR生成、Wikipedia検索、地図表示など）
       ├─ GitHub URL からスキルをインポート
       └─ 自作スキル（SKILL.md + JS で定義）

4.（開発者向け）カスタムタスクの追加
   └─ CustomTask インターフェースを実装 → Hilt で @IntoSet 登録
      → 独自の画面・推論ロジックをプラグイン的に追加可能
```

**開発者がフォークして使う場合**の要点：
- `model_allowlist.json` でサポートモデルを管理（バージョン別に `model_allowlists/` に履歴あり）
- 設定・ベンチマーク結果は **Protobuf + DataStore** で永続化
- UI は **Jetpack Compose + Material 3**、DI は **Hilt**、非同期は **Coroutines** という現代的な Android 構成
