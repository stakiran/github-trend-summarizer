---
url: https://github.com/kepano/obsidian-skills
keywords: obsidian, agent-skills, markdown, claude-code, pkm
oneliner: AIエージェント（Claude Code等）にObsidianのMarkdown・Bases・Canvas・CLIの扱い方を教えるスキル集。
---

## obsidian-skills とは

### 何をするリポジトリか

Obsidian の独自フォーマット（Markdown拡張、`.base`、`.canvas`）を **AIエージェントが正しく読み書きできるようにするための"スキル定義集"**。[Agent Skills 仕様](https://agentskills.io/specification) に準拠しており、Claude Code・Codex CLI・OpenCode などのエージェントにプラグインとして組み込める。

同梱スキルは **5 つ**：

| スキル | 対象ファイル | できること |
|---|---|---|
| **obsidian-markdown** | `.md` | Wikilink・Callout・埋め込み・YAML frontmatter など Obsidian 固有記法の正確な生成 |
| **obsidian-bases** | `.base` | ノートをDB的に集約するビュー（テーブル/カード/リスト/マップ）の定義・フィルタ・関数 |
| **json-canvas** | `.canvas` | ノード＋エッジで構成されるビジュアルキャンバス（マインドマップ・フロー図等）の生成 |
| **obsidian-cli** | — | 起動中の Obsidian を CLI 経由で操作（ノート読み書き・検索・プラグイン開発支援） |
| **defuddle** | — | Web ページから広告等を除去しクリーンな Markdown を抽出（トークン節約） |

---

### 何が嬉しいのか ─ 既存手段との比較

| 比較軸 | 従来のやり方 | obsidian-skills を使う場合 |
|---|---|---|
| **AIにObsidianノートを書かせる** | 汎用Markdownで出力→Wikilink・Callout等が不正確／欠落 | スキルがObsidian固有構文のルールを教えるため、**最初から正しい形式で出力**される |
| **`.base` / `.canvas` の生成** | スキーマを毎回プロンプトで説明するか、手動で書く | エージェントがスキーマ・関数一覧・バリデーションルールを把握済みで、**自然言語の指示だけで正確に生成**できる |
| **Obsidian CLI 操作** | ドキュメントを自分で読みコマンドを組み立てる | エージェントがコマンド体系を理解しており、「日報に追記して」等の**口語的な指示で操作可能** |
| **Webページの取り込み** | WebFetchで全HTML取得→トークン大量消費 | defuddle で本文だけ抽出し**トークンを大幅節約** |

要するに、**"Obsidianの方言"をエージェントに一括で教え込む辞書**のような役割を果たす。プロンプトに毎回仕様を貼る手間がなくなり、出力精度も上がる。

---

### 使い方の流れ

#### 1. インストール（いずれか一つ）

```bash
# Claude Code Marketplace 経由（推奨）
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills

# npx skills 経由
npx skills add git@github.com:kepano/obsidian-skills.git

# 手動: Obsidian Vault のルートに .claude/ フォルダとしてコピー
```

#### 2. エージェントに指示を出す

インストール後は特別な操作は不要。エージェントが `.md` / `.base` / `.canvas` に関する作業を検知すると、対応するスキルが**自動的にアクティブ化**される。

```
例: 「読書メモのテンプレートをObsidian Markdownで作って」
  → obsidian-markdown スキルが発動し、frontmatter・Callout・Wikilink 付きで生成

例: 「#project タグが付いたノートを期限順に並べる Base を作って」
  → obsidian-bases スキルが発動し、フィルタ・ソート付き .base ファイルを生成

例: 「このURLの内容をノートに取り込んで」
  → defuddle でクリーン抽出 → obsidian-markdown で整形して保存
```

#### 3. 結果を Obsidian で確認

生成されたファイルは Vault 内に直接書き出されるため、Obsidian を開けばそのまま閲覧・編集できる。CLI スキルを使えば、エージェントから Obsidian アプリへリアルタイムに反映させることも可能。
