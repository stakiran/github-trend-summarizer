---
url: https://github.com/AIDC-AI/Pixelle-Video
keywords: AI動画生成, ショート動画, ComfyUI, TTS, 自動編集
oneliner: トピックを一言入力するだけで台本作成〜画像/動画生成〜ナレーション合成〜BGM付き動画完成まで全自動で行う、ComfyUIベースのAIショート動画エンジン。
---

# Pixelle-Video まとめ

## このリポジトリは何？

**AIDC-AI（Alibaba International Digital Commerce）が公開する、AIフルオート・ショート動画生成エンジン。** トピックを1つ入力するだけで、次のパイプラインを自動実行し、最終的に完成動画（output/）を書き出す Python + Streamlit 製アプリ。

- **処理フロー**（`resources/flow_en.png`、`pixelle_video/pipelines/` 参照）:
  台本生成 → 画像プランニング → フレーム毎処理（画像/動画/音声合成） → 動画合成
- **主要コンポーネント**:
  - `web/app.py`（Streamlit UI）と `api/`（FastAPI サーバ、ルータ・タスクキュー付き）
  - `pixelle_video/pipelines/`: `standard` / `linear` / `asset_based` / `custom` の複数パイプライン（デジタルヒューマン、画像→動画、モーショントランスファー等にも対応）
  - `pixelle_video/services/`: LLM・TTS・画像解析・動画解析・HTMLフレーム生成・永続化・履歴管理
  - `workflows/selfhost` と `workflows/runninghub`: ComfyUI ワークフロー JSON（Flux, Qwen-Image, Nano Banana, WAN 2.1/2.2, LTX2, Edge-TTS, Index-TTS, Spark-TTS など多数）
  - `templates/`（1080x1080 / 1080x1920 / 1920x1080 縦横比別 HTML テンプレート）、`bgm/`（BGM 素材）
- **対応 LLM**: GPT / Qwen / DeepSeek / Ollama など。**ライセンス**: Apache-2.0。Windows オールインワン zip、Docker、ソース（uv）の 3 配布形態。

## 既存の似た手段と比較して何が嬉しい？

類似プロジェクト（MoneyPrinterTurbo、NarratoAI、MoneyPrinterPlus 等、READMEで参照されている）と比べたときの差別化ポイント：

1. **ComfyUI ワークフローを「原子的な能力」として差し替え可能**  
   画像生成を FLUX → Qwen-Image → Nano Banana、TTS を Edge-TTS → Index-TTS → ChatTTS、動画を WAN 2.1 → WAN 2.2 → LTX2 など、JSON を差し替えるだけで入れ替え可能。似た動画自動化ツールは「モデル固定」「クラウド API 依存」が多いが、Pixelle-Video は自作ワークフローをそのまま流し込める拡張性がウリ。
2. **完全無料運用が現実的**  
   LLM=Ollama (ローカル) + ComfyUI=ローカル GPU の構成で 0 円運用が可能、という方針を公式に提示。Qwen 併用の「極低コスト構成」、RunningHub 併用の「クラウド構成」の 3 段階を選べる。
3. **UI + API の両面提供**  
   Streamlit のノーコード GUI と FastAPI ベースの REST API（`api/routers`, `api/tasks`）を同梱しており、個人利用から自動化パイプラインへの組込みまで守備範囲が広い。
4. **拡張機能の幅**  
   デジタルヒューマン、画像→動画、**モーショントランスファー**（参照動画 + 画像で動きを転写）など、単なる「スライド + ナレーション」系の自動化ツールを超えた pipeline を標準搭載。縦/横/正方形テンプレート・カスタム HTML テンプレート・ボイスクローン（Index-TTS）対応。
5. **導入の容易さ**  
   Windows ユーザー向けに依存一式同梱の zip、macOS/Linux 向けに `uv run streamlit run web/app.py` の一発起動、Docker Compose も同梱。

## 使うときの流れ

1. **インストール**  
   - Windows: リリースからオールインワン zip をダウンロード → `start.bat` 起動。  
   - macOS/Linux: `uv` と `ffmpeg` をインストール → `git clone` → `uv run streamlit run web/app.py`。  
   - もしくは `docker-compose up` / `./docker-start.sh`。
2. **初回設定**（ブラウザで `http://localhost:8501` を開き「⚙️ System Configuration」を展開）  
   - **LLM**: Qwen / GPT-4o / DeepSeek / Ollama などから選び API Key 入力。  
   - **画像生成**: ローカル ComfyUI URL（既定 `http://127.0.0.1:8188`）または RunningHub API Key を設定。
3. **入力（左カラム）**: トピック文（AI に台本生成させる）または確定済みスクリプトを入力。BGM を「なし / 内蔵 / `bgm/` 自作」から選択。
4. **音声設定（中央カラム）**: TTS ワークフロー（Edge-TTS / Index-TTS 等）を選択。必要ならボイスクローン用リファレンス音声をアップロード、プレビュー。
5. **ビジュアル設定（中央カラム）**: 画像生成ワークフロー（`workflows/` 配下の JSON）、画像サイズ、プロンプト接頭辞、動画テンプレート（`static_*` / `image_*` / `video_*` の HTML）を選択。
6. **生成（右カラム）**: 「🎬 Generate Video」を押すと、台本 → 画像 → 音声 → 合成と段階進捗が表示され、完了後に動画プレビュー。ファイルは `output/` に保存。
7. **カスタマイズ（任意）**: ComfyUI を触れるユーザは `workflows/selfhost` に独自 JSON を追加して能力を差し替え、HTML を書けるユーザは `templates/` に独自テンプレートを追加可能。API 経由でのバッチ呼び出しは `api/` のエンドポイント利用。
