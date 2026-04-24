---
url: https://github.com/Anil-matcha/Open-Generative-AI
keywords: 生成AI, 画像生成, 動画生成, セルフホスト, Muapi, Electron, Next.js, リップシンク, オープンソース, 200モデル
oneliner: 200以上のAI画像・動画モデル（Flux/Sora/Veo/Kling等）をフィルタなし・自前環境で扱えるセルフホスト型の統合生成AIスタジオ。
---

# Open Generative AI 概要

## 1. このリポジトリは何？

**Higgsfield AI / Freepik AI / Krea AI / Openart AI などの商用クリエイティブ生成AIサービスの、オープンソース・無検閲な代替実装**。MIT ライセンスで公開されており、Web（Next.js）と Electron によるデスクトップアプリの両方で動作する統合スタジオアプリ。

アーキテクチャ:
- **Next.js 14 + React 18 + Tailwind** のモノレポ構成（`packages/studio` が共有コンポーネント・モデル定義を提供）
- バックエンドは自前を持たず、**[Muapi.ai](https://muapi.ai) の統合 API ゲートウェイ** 越しに 200 以上のモデル（Flux, Nano Banana 2, Seedream 5.0, Midjourney, Kling, Sora, Veo, Wan, Hailuo, Runway, Infinite Talk 等）を呼び出す BYOK 方式（APIキーは localStorage）
- デスクトップ版限定で **stable-diffusion.cpp** を組み込んだローカル推論エンジン（Z-Image, SD1.5系, SDXL, macOS Metal GPU 対応）も内蔵
- 5 つのスタジオ UI を提供: **Image / Video / Lip Sync / Cinema / Workflow**（最後はノードベースの多段パイプラインビルダー）

## 2. このリポジトリは何が嬉しいの？ — 既存サービスとの比較

README に明記された差別化ポイントを要約:

| 観点 | Higgsfield / Freepik / Krea / Openart 等 | Open Generative AI |
| --- | --- | --- |
| 料金 | サブスクリプション | 無料・OSS (MIT) |
| コンテンツフィルタ | 厳しいガードレール、プロンプト拒否あり | **一切なし（uncensored）** |
| モデル数 | 自社・提携プロプライエタリ中心 | **200+ のオープン/商用モデルを統一 UI で切替** |
| 複数画像参照 | 少数のみ | **最大 14 枚** を同時入力（Nano Banana 2 Edit 等） |
| リップシンク | 無し／限定的 | 画像駆動・動画駆動あわせて **9 モデル** 専用 Studio |
| セルフホスト | 不可 | 可（Web / macOS / Windows / Linux） |
| ローカル推論 | 基本不可 | デスクトップ版で API キー不要のオンデバイス生成 |
| ワークフロー | ブラックボックス | ノードベースのビジュアルビルダー＋コミュニティテンプレート |
| データ | クラウド保存 | ローカル (localStorage) に保持 |

要するに「**一つのモデル特化サービスを契約して機能/検閲に縛られる**」代わりに、「**Muapi 経由で最新 SOTA モデル群を一括で叩け、しかも UI・モデル定義を自分で拡張できる**」点が最大の利点。

## 3. 使うときの流れ

典型的な利用フローは 2 種類。

### A. ホスト版をブラウザで試す（最速）
1. `https://dev.muapi.ai/open-generative-ai` にアクセス
2. 無料アカウント登録 → そのまま Image/Video/Lip Sync/Cinema/Workflow を利用

### B. 自前で動かす（セルフホスト / 開発）
1. 前提: Node.js 18+ と Muapi.ai の API キーを用意
2. クローンと起動:
   ```bash
   git clone https://github.com/Anil-matcha/Open-Generative-AI.git
   cd Open-Generative-AI
   npm install        # packages/studio ワークスペースも同時導入
   npm run dev        # http://localhost:3000
   ```
3. 初回アクセス時にモーダルで Muapi API キーを入力（`localStorage` に保存、サーバには送られない）
4. 本番ビルド: `npm run build && npm run start`

### C. デスクトップアプリを使う
1. Releases から `.dmg` / `.exe` を入手（macOS は Gatekeeper 回避手順あり、`xattr -cr` 実行）
   - Linux は `npm run electron:build:linux` でローカルビルド（AppImage / .deb）
2. 初回起動でキーを入力
3. **ローカル推論**を使う場合: Settings → Local Models で sd.cpp エンジンを 1 クリック導入 → 使うモデル（Z-Image Turbo など）を DL → Image Studio の「⚡ Local」トグルで切替

### D. 各 Studio の基本的な操作パターン
- **Image / Video Studio**: 参照画像を上げずにプロンプト → T2I/T2V、参照画像をアップロード → 自動的に I2I/I2V 用モデルセットに切替。モデルごとに解像度・アスペクト比・品質・尺の UI が動的に変化
- **Lip Sync**: Portrait 画像 or 動画 ＋ 音声 → 発話動画
- **Cinema**: カメラ／レンズ／焦点距離／絞りを選ぶと内部でプロンプト修飾子に変換
- **Workflow**: テンプレ選択 or ノードエディタで I/V/A モデルを連結 → Playground でフォーム実行、Muapi API からも呼出可
- 生成結果・アップロード画像・履歴は localStorage に保存され、再読込してもジョブ継続。ワンクリックで DL 可能
