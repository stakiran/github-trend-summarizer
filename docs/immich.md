---
url: https://github.com/immich-app/immich
keywords: self-hosted, photo-management, google-photos-alternative
oneliner: Google Photos のようなリッチな写真・動画管理をセルフホスト環境で実現するオープンソースソリューション
---

## Immich — セルフホスト型 写真・動画管理プラットフォーム

### このリポジトリは何？

Immich は、**Google Photos や iCloud の代替**を目指すセルフホスト型の写真・動画管理ソリューション。モノレポ構成で以下の主要コンポーネントから成る。

| コンポーネント | 技術スタック | 役割 |
|---|---|---|
| **server/** | NestJS (TypeScript) | REST API・ジョブ管理・認証 |
| **web/** | SvelteKit + Tailwind CSS | Web フロントエンド |
| **mobile/** | Flutter (iOS/Android) | モバイルアプリ（自動バックアップ） |
| **machine-learning/** | Python + ONNX Runtime | 顔認識・CLIP 検索・OCR |

デプロイは **Docker Compose 一発**で完結し、PostgreSQL (pgvector)・Redis がバックエンドを支える。

### 既存手段と比べて何が嬉しいのか？

| 観点 | Google Photos / iCloud | Immich |
|---|---|---|
| **データ主権** | クラウドベンダーに依存 | 自分のサーバーに全データを保持。プライバシー完全管理 |
| **コスト** | 容量課金（月額制） | 自前ストレージのみ。容量上限なし |
| **AI 検索** | ベンダーのクラウド AI | **CLIP による意味検索**・**顔認識クラスタリング**をローカル実行。データが外部に出ない |
| **マルチユーザー** | 家族プラン等の制約あり | ユーザー数無制限。パートナー共有・公開リンク・読み取り専用ギャラリー等を柔軟に設定 |
| **HW アクセラレーション** | — | GPU トランスコード (NVENC/QSV/VAAPI) と ML 推論 (CUDA/ROCm/OpenVINO) に対応 |
| **拡張性** | クローズド | OpenAPI SDK・プラグイン機構・OSS (AGPL-v3) |

一言で言えば、**「クラウドに写真を預けたくないが、Google Photos 級の体験は欲しい」** という需要にピンポイントで応える。

### 使うときの流れ

```
1. 環境準備
   └─ Docker & Docker Compose をインストール

2. デプロイ（数分）
   └─ .env に DB パスワード・メディア保存先を設定
   └─ docker compose up -d で 4 コンテナ (server / ML / Redis / PostgreSQL) が起動
   └─ http://<host>:2283 で Web UI にアクセス

3. 初期セットアップ
   └─ 管理者アカウントを作成
   └─ ストレージ・ユーザー・外部ライブラリ等を設定

4. 写真・動画の取り込み
   ├─ モバイルアプリ (iOS/Android) をインストール → 自動バックアップ ON
   ├─ Web UI からドラッグ＆ドロップでアップロード
   └─ CLI ツール (immich-cli) で既存ライブラリを一括インポート

5. 日常利用
   ├─ タイムライン閲覧・アルバム整理・お気に入り・アーカイブ
   ├─ 顔認識で人物ごとに自動分類 → 名前を付けて管理
   ├─ 自然言語やオブジェクトで横断検索（CLIP）
   ├─ 地図ビューで撮影地を俯瞰
   └─ 「◯年前の今日」メモリーズ通知

6. 共有・コラボレーション
   └─ 他ユーザー招待 / パートナー共有 / パスワード付き公開リンク
```

> **まとめ:** Docker を動かせるサーバー（NAS・VPS・自宅 PC）があれば、Google Photos と遜色ない写真管理体験を **完全に自分の手元** で運用できる。ML 機能もローカル完結のため、プライバシーとコストの両面で優位性がある。
