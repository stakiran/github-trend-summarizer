---
url: https://github.com/thedotmack/claude-mem
keywords: claude-code, persistent-memory, plugin, context-injection, session-management
oneliner: Claude Code のセッション間でコンテキストを自動保存・圧縮・再注入し、AIの"記憶喪失"を解消するプラグイン。
---

## claude-mem とは何か

Claude Code 向けの**永続メモリプラグイン**。セッション中に Claude が行ったツール操作（ファイル読み書き、コマンド実行、検索など）を自動キャプチャし、Claude Agent SDK で意味的に圧縮したうえで SQLite + ChromaDB（ベクトル検索）に蓄積する。次回セッション開始時に、関連する過去コンテキストを自動で注入する。

**アーキテクチャの要点：**

| レイヤー | 役割 |
|---|---|
| **6つのライフサイクルフック** | SessionStart / UserPromptSubmit / PostToolUse / Summary / SessionEnd 等でイベントを捕捉 |
| **Worker サービス** (port 37777) | Bun 上の Express API。AI 圧縮・埋め込み生成を非同期処理 |
| **SQLite + ChromaDB** | 観測データの永続化とハイブリッド検索（キーワード FTS5 + ベクトル） |
| **MCP サーバー** | `search` / `timeline` / `get_observations` ツールを Claude Code に提供 |
| **Viewer UI** | React 製 Web UI (localhost:37777) でメモリストリームを閲覧 |

---

## 何が嬉しいのか — 既存手段との比較

**解決する課題：** AI コーディングアシスタントはセッションが切れると過去の判断・修正履歴・プロジェクト知識をすべて失う。

| 手段 | 限界 | claude-mem の優位性 |
|---|---|---|
| **手動メモ / CLAUDE.md** | 書き忘れ・更新コスト大 | 完全自動。ユーザー負担ゼロ |
| **プロンプトに過去ログ貼付** | トークン爆発・選別が手動 | 3層プログレッシブ検索で **トークン消費を～1/10** に削減 |
| **汎用 RAG** | 外部 ML 基盤が必要、セットアップ重い | `npx claude-mem install` 一発。SQLite + ローカル Chroma で軽量 |
| **Claude Code 素の状態** | セッション跨ぎの記憶なし | 過去セッションの要約・観測を自動注入 |

**その他の差別化ポイント：**
- `<private>` タグによるプライバシー制御（タグ内はストレージに保存されない）
- Claude Code 以外にも Gemini CLI / Cursor / OpenCode 等に対応
- CLAIM-CONFIRM キューとサーキットブレーカーによる堅牢な非同期処理

---

## 使うときの流れ

### 1. インストール（1コマンド）

```bash
npx claude-mem install
```

Bun・uv（Python）が未導入なら自動インストールされる。DB・Worker・フックが一括セットアップされる。

### 2. 通常の作業（完全自動）

```
セッション開始
  └─ Worker 起動 → 過去の関連コンテキストを自動注入
      ↓
作業中（ファイル編集・コマンド実行など）
  └─ PostToolUse フックが各操作を非同期キャプチャ
     → Worker が AI 圧縮 → SQLite/Chroma に保存
      ↓
セッション終了
  └─ セッション要約を自動生成・保存
```

ユーザーは何も意識しなくてよい。次のセッションで自動的に過去文脈が利用可能になる。

### 3. 能動的に過去を検索したいとき

```
/mem-search 認証の実装
```

内部では 3 段階で効率的に絞り込む：

1. **search** — インデックスから候補取得（～50トークン/件）
2. **timeline** — 前後の時系列コンテキストを確認
3. **get_observations** — 必要な ID のみ全文取得

### 4. Web UI で閲覧

`http://localhost:37777` にアクセスすると、日付別のメモリストリーム・セッション一覧・検索が利用できる。
