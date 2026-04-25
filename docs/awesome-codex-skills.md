---
url: https://github.com/ComposioHQ/awesome-codex-skills
keywords: Codex CLI, スキル, ワークフロー自動化, Composio, MCP
oneliner: Codex CLI／API 向けのモジュール型「スキル」を厳選したキュレーションリポジトリで、SKILL.md 一ファイルを配置するだけで Codex のふるまいを拡張できる。
---

# ComposioHQ/awesome-codex-skills

## このリポジトリは何？

**OpenAI Codex CLI／API に "スキル" を追加するためのキュレーション集。**

スキルとは `SKILL.md`（YAML frontmatter ＋ Markdown 手順書）を核とする **モジュール型の命令バンドル**。`~/.codex/skills/<スキル名>/` に置くだけで Codex がそのスキルを自動認識し、「議事録をアクション一覧に変換」「GitHub Actions の失敗を自動修正」「Notion にナレッジを記録」といった決まりきった作業を Codex に肩代わりさせられる。

現在のラインナップは **メインスキル約 48 個＋Composio 統合スキル 100 個以上**。Python スクリプトやリファレンスドキュメントを同梱した高機能なものから、`SKILL.md` 一枚だけのシンプルなものまで、粒度が揃っている。

---

## 既存の似た手段と比べて何が嬉しいの？

| 比較軸 | システムプロンプト直書き | MCP サーバー自作 | **awesome-codex-skills** |
|--------|----------------------|----------------|--------------------------|
| 再利用性 | × コピペ管理 | △ サーバー単位 | **◎ スキル単位でポータブル** |
| コンテキスト効率 | × 常に全文注入 | ○ | **◎ 必要なスキルだけロード** |
| 導入コスト | ◎ | × サーバー起動必要 | **◎ フォルダを置くだけ** |
| 外部 API 連携 | △ 手書き | ○ | **◎ Composio 経由で 1000+ アプリ対応** |
| コミュニティ共有 | × | △ | **◎ GitHub でスキルをインストール／公開** |

**最大の差分は「Context 効率＋ポータビリティ」**。システムプロンプトに何でも書くと毎回トークンを消費するが、スキルは Codex が必要なときだけロードする仕組み（Progressive Disclosure）。かつ `SKILL.md` 形式で標準化されているため、チーム間・プロジェクト間での共有が容易。MCP サーバーより導入が軽く、Composio 統合で外部 API 連携も手厚い。

---

## 使うときの流れ

### 1. スキルをインストール
```bash
# skill-installer を使って GitHub から直接取得
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path gh-fix-ci
# → ~/.codex/skills/gh-fix-ci/ に配置される
```

### 2. Codex を起動してスキルを呼び出す
```bash
codex
# Codex が skills/ ディレクトリを自動スキャンし認識
# プロンプト例: "PR の CI 失敗を調べて直して"
```
Codex は `SKILL.md` の `description` フィールドを見てトリガー条件を判断し、関連スキルを自動適用する。

### 3. 外部連携が必要な場合（Composio）
```bash
# connect スキルで認証
composio login
composio add github   # 使いたいアプリを追加
# 以降は composio-skills/ 配下のスキルが利用可能に
```

### 4. 自作スキルを作る
```
~/.codex/skills/my-skill/
└── SKILL.md   ← frontmatter(name, description) + Markdown 手順書だけで最小動作
```
`skill-creator` スキルを使えば対話形式でテンプレートを生成でき、`scripts/`（決定論的な操作を外部化）や `reference/`（詳細ドキュメント）を後から追加して育てられる。

---

**一言まとめ：** "Codex 版の dotfiles 管理" のようなもの。`~/.codex/skills/` に置くだけで Codex の能力を宣言的に拡張でき、チームやコミュニティでスキルを共有・再利用できる軽量エコシステム。
