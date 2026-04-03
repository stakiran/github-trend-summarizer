---
url: https://github.com/dmtrKovalenko/fff.nvim
keywords: fuzzy-file-finder, frecency, mcp-server, neovim-plugin, simd-search
oneliner: 頻度・鮮度（Frecency）とクエリ学習で検索精度を高める、AI エージェント／Neovim 向け高速ファイル検索ツールキット
---

## fff.nvim とは

**FFF (Fast File Finder)** は、Rust で書かれた高速ファイル検索エンジンを核に、**Neovim プラグイン**・**AI エージェント用 MCP サーバー**・**Node.js / C ライブラリ**として利用できる統合ファイル検索ツールキットである。

ワークスペースは 6 つの Rust クレートで構成される：

| クレート | 役割 |
|---|---|
| `fff-core` | 検索エンジン本体（ファジー検索・grep・スコアリング・Frecency） |
| `fff-nvim` | Neovim 向け LuaJIT FFI バインディング |
| `fff-mcp` | Claude Code 等の AI エージェント向け MCP サーバー |
| `fff-grep` | スタンドアロン grep 実装 |
| `fff-query-parser` | クエリ言語パーサ（制約・ファジー・glob） |
| `fff-c` | C FFI エクスポート |

---

## 何が嬉しいのか ― 既存ツールとの比較

### 1. Frecency（頻度×鮮度）による学習型ランキング

fzf や Telescope はファジー一致スコアのみでランキングする。FFF は **LMDB に永続化された Frecency データベース**を持ち、「よく開くファイル」「最近変更されたファイル」を自動的に上位に押し上げる。さらに **Query Tracker** が「このクエリで過去に何を選んだか」を記憶し、3 回以上同じ選択をすると指数的にスコアを増幅する（Combo Boost）。

### 2. SIMD 最適化と Bigram プレフィルタ

- **AVX2 対応の case-insensitive memmem** でバイト列検索を高速化
- **Bigram 逆引きインデックス**（2 文字組み合わせの bitmap）で、ファジーマッチ前に候補を大幅に絞り込む
- 結果として ripgrep 比で **コンテンツ検索 10〜50 倍高速**、fzf 比で **ファイル名検索 10 倍高速**（README 記載値）

### 3. AI エージェントへのネイティブ対応

Claude Code 標準の Glob/Grep ツールの代替として MCP サーバーを提供。AI 用には Frecency の減衰曲線（半減期 3 日 / 履歴 7 日）を人間用（10 日 / 30 日）と分離し、セッション単位で変わる AI のコンテキストに最適化している。

### 4. 統一された制約構文

拡張子（`*.rs`）、パス（`src/`）、git ステータス（`git:modified`）、除外（`!test/`）を単一クエリで混在指定でき、grep でもファイル検索でも同じ構文が使える。

| 観点 | fzf | ripgrep | Telescope | **FFF** |
|---|---|---|---|---|
| ランキング | ファジースコア | 関連度 | ファジースコア | **Frecency + Combo + Git** |
| 記憶の永続化 | なし | なし | セッション内 | **LMDB 永続化** |
| AI エージェント統合 | なし | なし | なし | **MCP サーバー内蔵** |
| grep モード | — | 正規表現のみ | — | **Plain / Regex / Fuzzy** |

---

## 使い方の流れ

### Neovim ユーザーの場合

```lua
-- 1. lazy.nvim 等でインストール（プリビルドバイナリを自動DL）
{ "dmtrKovalenko/fff.nvim", build = ":FFFDownload" }

-- 2. セットアップ（Frecency・履歴・git 連携を有効化）
require("fff").setup({
  frecency = { enabled = true },
  history  = { enabled = true },
})

-- 3. 日常操作
require("fff").find_files()   -- ファイルピッカーを開く
require("fff").live_grep()    -- ライブ grep を開く
-- → 使うほど Frecency DB が育ち、検索精度が向上する

-- 4. 診断・メンテナンス
-- :FFFHealth / :FFFClearCache / :FFFDebug
```

### AI エージェント（Claude Code 等）の場合

```bash
# 1. MCP サーバーをインストール
curl -L https://dmtrkovalenko.dev/install-fff-mcp.sh | bash

# 2. Claude Code の MCP 設定に追加
# ~/.claude/settings.json → mcpServers.fff を登録

# 3. CLAUDE.md に指示を追記（推奨）
#    "ファイル検索には fff ツールを使うこと"

# 4. 利用可能なツール:
#    - find_files: ファイル名でファジー検索
#    - grep:       ファイル内容を検索
#    - multi_grep: 複数パターンの OR 検索
```

### Node.js / C ライブラリとして

Bun/Node.js バインディング（`packages/fff-bun`, `packages/fff-node`）や C FFI（`crates/fff-c`）経由で、任意のアプリケーションに検索エンジンを組み込める。

---

**要約**: FFF は「使えば使うほど賢くなるファイル検索」を、Neovim と AI エージェントの両方に SIMD レベルの速度で提供するツールキットである。
