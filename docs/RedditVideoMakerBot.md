---
url: https://github.com/elebumm/RedditVideoMakerBot
keywords: Reddit, 動画自動生成, TTS, YouTube Shorts, TikTok
oneliner: Redditの投稿・コメントを自動で縦型ショート動画に変換するPython製ボット
---

## RedditVideoMakerBot とは

### 何をするリポジトリか

Redditの投稿やコメントを素材に、**TikTok／YouTube Shorts 風の縦型動画を全自動で生成する** Pythonツール。Reddit APIで取得したスレッドのスクリーンショットを、ゲームプレイ映像（Minecraft, GTA等）の上に重ね、テキスト読み上げ音声を付けた動画を一発で出力する。いわゆる「Redditリーディング動画」を量産するための専用パイプラインである。

### 何が嬉しいのか（既存手段との比較）

| 観点 | 手動編集（Premiere等） | 汎用自動化（n8n等） | **本リポジトリ** |
|---|---|---|---|
| 動画1本あたりの所要時間 | 30分〜数時間 | 要カスタム構築 | **数分（完全自動）** |
| 必要スキル | 動画編集スキル | プログラミング＋連携設計 | **設定ファイル記入のみ** |
| TTS選択肢 | 外部サービスを個別利用 | 個別連携が必要 | **7エンジン内蔵**（TikTok音声, ElevenLabs, AWS Polly, OpenAI TTS, gTTS 等） |
| バッチ処理 | 手作業の繰り返し | 可能だが構築コスト大 | **`times_to_run` 指定で連続生成** |
| 背景映像 | 自分で用意・合成 | 自分で用意 | **10種のゲーム映像＋BGMをYouTubeから自動DL** |

最大の利点は **「設定を書いてコマンド1つ叩くだけ」** で、Reddit→音声→スクリーンショット→動画合成→出力までの全工程が完結する点。手動編集のワークフローを完全に置き換えられる。

### 使い方の流れ

```
1. 環境準備
   ├─ Python 3.10+ / FFmpeg をインストール
   ├─ pip install -r requirements.txt
   └─ playwright install  (ブラウザ自動操作用)

2. 設定ファイル作成（config.toml）
   ├─ Reddit API クレデンシャル（client_id / secret / ユーザー名 / パスワード）
   ├─ 対象サブレディット名（例: AskReddit）
   ├─ TTS エンジン選択（tiktok / elevenlabs / gtts 等）
   ├─ 背景映像・BGM の選択（minecraft, lofi 等）
   └─ テーマ（dark/light）、解像度、コメント長フィルタ等を調整
       ※ Web GUI（python GUI.py → localhost:4000）からも設定可能

3. 動画生成
   $ python main.py
   ├─ Reddit API でスレッド取得＋コメント抽出
   ├─ Playwright で Reddit UI のスクリーンショット撮影
   ├─ 選択した TTS エンジンで読み上げ音声を生成
   ├─ YouTube から背景映像・BGMを自動ダウンロード
   └─ MoviePy + FFmpeg で最終動画を合成 → results/ に出力

4. 出力確認
   └─ results/ ディレクトリに MP4 動画が保存される
       （メタデータは videos.json に記録、GUI から一覧閲覧も可能）
```

### 補足：主な設定ポイント

- **ストーリーモード**（`storymode=true`）: コメントではなく投稿本文だけを読み上げる長文向けモード
- **AI類似度ソート**（`ai_similarity_enabled`）: キーワードに近い投稿を優先選択
- **多言語対応**: `post_lang` で100以上の言語に翻訳可能
- **NGワードフィルタ**: `blocked_words` で不適切な投稿を自動除外
