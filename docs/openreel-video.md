---
url: https://github.com/Augani/openreel-video
keywords: video editor, browser-based, WebCodecs, WebGPU, CapCut alternative, React, TypeScript, client-side, open source, MIT
oneliner: ブラウザだけで完結する完全クライアントサイド動画エディタ（CapCut のオープンソース代替）
---

# OpenReel Video

## このリポジトリは何？

**OpenReel Video** は、ブラウザ上だけで動作するプロ仕様の動画編集エディタ。CapCut のオープンソース代替を標榜しており、MIT ライセンスで完全無料。**[openreel.video](https://openreel.video)** にアクセスすればすぐ使える。

- **構成**: pnpm モノレポ（TypeScript / React 18）
  - `apps/web` … 動画エディタの React フロントエンド（約 66k 行）
  - `apps/image` … 画像編集アプリ（派生）
  - `packages/core` … 動画/音声/グラフィクス/エクスポート/ストレージのコアエンジン（約 59k 行）
  - `packages/image-core`, `packages/ui` … 画像コアと共有 UI
- **主要技術**: WebCodecs（HW エンコード/デコード）、WebGPU（GPU 合成・描画）、Web Audio API、THREE.js、IndexedDB（自動保存）、Zustand（状態管理）、MediaBunny（メディア処理）、ffmpeg.wasm
- **機能**: マルチトラックタイムライン、フレーム精度カット/トリム/分割、トランジション、各種エフェクト、ブレンドモード、20+ テキストアニメーション、カラオケ字幕、シェイプ/SVG、キーフレーム、カラーグレーディング（カーブ・LUT）、オーディオエフェクト（EQ/コンプ/リバーブ等）、ビート検出、ノイズリダクション、画面録画、MP4/WebM/ProRes 4K 出力、AI アップスケーリング、無制限 Undo/Redo、自動保存
- **「AI 主導開発」**: Claude AI が Issue triage・実装・レビューを担当し、メンテナ Augustus 氏が最終承認するという運営モデルを公言している

## 既存の似た手段と比べた嬉しさ

| 観点 | OpenReel Video | CapCut / Premiere / DaVinci | Clipchamp / 各種 Web SaaS |
|---|---|---|---|
| インストール | **不要**（Chrome/Edge/Firefox/Safari で開くだけ） | 必要（数 GB） | 不要 |
| アップロード | **一切なし**（100% クライアントサイド） | ローカル | クラウドにアップ |
| プライバシー | 動画がデバイスから出ない | ローカル | サーバへ送信される懸念 |
| 価格 | **MIT で完全無料・透かしなし** | 有料 or サブスク・透かし付き | サブスク・機能制限 |
| 速度 | WebCodecs + WebGPU で HW アクセラレーション | ネイティブ最速 | サーバ依存・遅延あり |
| 改造 | **OSS なので自己ホスト・改造可** | 不可 | 不可 |
| 4K/ProRes | 対応 | 対応 | 制限あり |

要するに「**ローカルアプリ並みの機能をブラウザで、しかもクラウドに何も上げず、無料で、改造もできる**」という点が独自価値。CapCut のような透かしや課金、Clipchamp のようなクラウド送信を嫌うユーザーや、社内で動画を扱いたい組織にも刺さる。

## 使うときの流れ

### A. すぐ試す（推奨）
1. ブラウザで **https://openreel.video** を開く
2. 動画/画像/音声をドラッグ＆ドロップで読み込む（アップロードは発生しない）
3. タイムラインに配置 → カット/トリム/分割、テキスト・図形・字幕・エフェクト・キーフレームを追加
4. プレビューで確認しつつ、必要なら色調補正・音声ミックス・LUT 適用
5. **Export** から MP4/WebM/ProRes、解像度・ビットレート・FPS を指定して書き出し（端末内で完結、自動保存は IndexedDB）

### B. ローカルで動かす / 開発に参加
```bash
git clone https://github.com/Augani/openreel-video.git
cd openreel-video
pnpm install            # Node.js 18+, pnpm 8+
pnpm dev                # http://localhost:5173
# 本番ビルド
pnpm build && pnpm preview
```
コア WASM が必要な場合は `pnpm build:wasm`。コントリビュート時は `pnpm typecheck && pnpm test && pnpm lint` を回し、Conventional Commits（`feat: ...`）でブランチを作って PR を出すフロー。Issue は `needs-claude-review` ラベルで AI レビューが回り、24 時間以内に応答が返ってくる運用になっている。

### 推奨環境
Chrome/Edge 94+ または Firefox 130+ / Safari 16.4+、RAM 8GB 以上、4K 編集には専用 GPU 推奨。
