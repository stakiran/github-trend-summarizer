---
url: https://github.com/ahujasid/blender-mcp
keywords: Blender, MCP, Claude, 3D modeling, AI-assisted
oneliner: Model Context Protocol (MCP) を介して Claude AI から Blender を直接操作し、自然言語で 3D シーンを構築できるブリッジツール。
---

## Blender MCP — Claude AI × Blender 連携ブリッジ

### これは何？

**Blender MCP** は、3DCG ソフト **Blender** と **Claude AI** を **Model Context Protocol (MCP)** で双方向接続するツール。2 つのコンポーネントで構成される。

| コンポーネント | 役割 |
|---|---|
| **Blender アドオン** (`addon.py`) | Blender 内で TCP ソケットサーバー（デフォルト `localhost:9876`）を起動し、JSON コマンドを受けて `bpy` API を実行する |
| **MCP サーバー** (`server.py`) | Claude Desktop / Cursor 等の MCP クライアントと Blender アドオンを中継。Claude に対して「シーン取得」「コード実行」「アセット検索・ダウンロード」「AI 3D 生成」などのツールを公開する |

Claude はこれらのツールを組み合わせ、**自然言語の指示だけで** Blender 上に 3D シーンを構築・編集できる。ビューポートのスクリーンショット取得もできるため、Claude が結果を "見て" 修正を繰り返す対話的ワークフローが可能。

---

### 何が嬉しいの？ ― 既存手段との比較

| 観点 | 従来の方法 | Blender MCP |
|---|---|---|
| **AI で Blender を操作** | Claude に Python スクリプトを書かせ → 手動でコピペ実行 | Claude が直接 Blender にコマンドを送信。コピペ不要 |
| **双方向フィードバック** | AI は実行結果を知らない（一方通行） | シーン情報取得・スクリーンショット返却で **Claude が結果を確認しながら反復改善** |
| **アセット調達** | Poly Haven / Sketchfab を手動ブラウズ → DL → インポート | Claude が **検索・DL・インポートまで一気通貫**で実行（Poly Haven / Sketchfab / Hyper3D Rodin / Hunyuan3D に対応） |
| **テキストから 3D 生成** | 外部サービスで生成 → 手動インポート → 位置調整 | Claude が **テキストや画像から 3D モデルを生成し、そのまま Blender に配置** |
| **拡張性** | アドオンごとに独自 API | MCP 標準プロトコルなので、対応クライアントなら何でも接続可能 |

要するに「**AI と Blender の間の手作業をすべて自動化**」し、自然言語だけでシーン制作を完結させる点が最大の価値。

---

### 使うときの流れ

```
┌──────────────────────────────────────────────────┐
│  1. セットアップ（初回のみ）                       │
│     ① addon.py を Blender にインストール・有効化    │
│     ② Claude Desktop 等の MCP 設定に blender-mcp  │
│        を追加（uvx blender-mcp で起動）            │
│     ③ 必要に応じて API キーを設定                  │
│        (Sketchfab / Hyper3D / Hunyuan3D)          │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  2. 接続                                          │
│     Blender サイドバー > BlenderMCP タブ            │
│     → 使いたいアセットライブラリにチェック           │
│     → 「Connect to Claude」をクリック               │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  3. 自然言語で指示（対話ループ）                    │
│     例:「中世の城のシーンを作って」                  │
│                                                    │
│     Claude が内部で行うこと:                        │
│       get_scene_info()    → 現状把握               │
│       search/download     → アセット調達            │
│       execute_blender_code → 配置・マテリアル設定   │
│       get_viewport_screenshot → 結果確認            │
│       → 不満なら修正を繰り返す                      │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  4. 完成したシーンを Blender 上で確認・保存         │
└──────────────────────────────────────────────────┘
```

**ポイント**: ユーザーは基本的に **Claude に日本語（自然言語）で話すだけ**。Blender の操作知識や Python スクリプティングは不要。Claude がツールを自律的に選択・実行し、結果を見ながらシーンを仕上げてくれる。
