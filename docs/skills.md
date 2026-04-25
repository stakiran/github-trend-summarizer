---
url: https://github.com/mattpocock/skills
keywords: AI agent, skills management, CLI, Claude Code, package manager
oneliner: 45以上のAIコーディングエージェントに対応した「スキル」パッケージマネージャーCLIツール。
---

## このリポジトリは何？

`skills` は、AI コーディングエージェント（Claude Code・Cursor・Windsurf など 45 種超）向けの**スキルパッケージマネージャー CLI**。

「スキル」とは YAML frontmatter 付きの Markdown ファイル（`SKILL.md`）で、「どういう状況でエージェントが何をすべきか」を記述したものだ。GitHub リポジトリからスキルを取得し、各エージェントが読み込む所定のパス（`.claude/skills/`、`.cursor/skills/` など）にシンリンクまたはコピーで配置してくれる。

```bash
npx skills add vercel-labs/agent-skills   # GitHub shorthand で追加
npx skills find typescript                # インタラクティブ検索
npx skills list                           # インストール済み一覧
npx skills update                         # 一括更新
npx skills remove my-skill               # 削除
```

---

## 何が嬉しいのか？既存手段との比較

| 比較対象 | 課題 | skills の優位点 |
|---|---|---|
| **手動コピペ** | スキルが増えると管理が煩雑、更新が大変 | `npx skills update` 一発で全スキルを最新化 |
| **Git submodule** | エージェントごとにパスが違い、サブモジュールを複数管理する必要がある | エージェント種別を自動検出し正しいパスに配置 |
| **ただの dotfiles 共有** | 自分の設定しか共有できない、他人のスキルを取り込めない | GitHub 上のスキルリポジトリをエコシステムとして活用 |
| **エージェント固有の拡張機能** | 特定エージェント専用、他ツールに使い回しできない | `SKILL.md` 1 ファイルで 45 種エージェントをカバー |

シンリンクで配置するため、スキル本体は 1 か所にしか存在せず、`update` すれば全エージェントに即時反映される点が実務上の最大の旨味。

---

## 使うときの流れ

### 1. スキルを探してインストールする

```bash
# インタラクティブ検索（インストール数・スター数付きで候補一覧）
npx skills find react

# または直接追加（-g でグローバル、-y で確認スキップ）
npx skills add vercel-labs/agent-skills -g -y
```

特定エージェントや特定スキルに絞ることも可能：

```bash
npx skills add vercel-labs/agent-skills -a claude-code -s web-design-guidelines
```

### 2. スキルを自作して公開する

`npx skills init my-skill` でテンプレートを生成し、frontmatter と手順を記述：

```markdown
---
name: my-skill
description: XXX をするとき使う
---
## When to Use
〇〇な状況で使う

## Steps
1. まずこれをやる
2. 次にあれをやる
```

リポジトリを GitHub に push すれば、他の人が `npx skills add your-name/repo` で使えるようになる。

### 3. チーム・プロジェクトで共有する

プロジェクトルートで実行するとローカルの `.claude/skills/` 等に置かれ、`skills-lock.json` がコミットされる。CI や新メンバーは `npx skills experimental_install` で同一スキルセットを復元可能。

---

**一言でいうと**、npm / pip のように「スキルのエコシステム」を作り、AI エージェントの振る舞いをバージョン管理・共有できる基盤を提供するツール。
