---
url: https://github.com/shanraisshan/claude-code-best-practice
keywords: Claude Code, ベストプラクティス, エージェント設計, スキル, サブエージェント
oneliner: Claude Code の拡張機能（サブエージェント・スキル・コマンド・フック）の設計パターンを網羅的にまとめたリファレンス実装リポジトリ
---

## このリポジトリは何？

Claude Code（Anthropic の AI 開発 CLI）を**本格的に使いこなすための設計パターン集・リファレンス実装**。アプリケーションのコードベースではなく、「Claude Code の `.claude/` ディレクトリをどう構成すべきか」を実例付きで示すドキュメント＋設定ファイル群である。

キャッチコピーは *"from vibe coding to agentic engineering — practice makes claude perfect"*。気軽な AI コーディングから、**再現性のあるマルチエージェント開発**へ移行するためのガイドという位置づけ。

### 主な構成要素

| ディレクトリ | 内容 |
|---|---|
| `.claude/agents/` | サブエージェント定義（weather-agent, presentation-curator 等） |
| `.claude/commands/` | スラッシュコマンド定義（`/weather-orchestrator` 等） |
| `.claude/skills/` | スキル定義（weather-fetcher, weather-svg-creator 等） |
| `.claude/hooks/` | フックスクリプト（音声通知、Git コミット時処理など24種のイベント対応） |
| `best-practice/` | 8 本のベストプラクティス文書（コマンド68個、設定60項目超を網羅） |
| `reports/` | メモリスコープ、ツール活用、レート制限などの分析レポート |
| `tips/` | Claude Code 開発者 Boris Cherny 氏の助言を収録 |
| `orchestration-workflow/` | **Command → Agent → Skill** パターンの動作デモ（天気カード生成） |

---

## 何が嬉しいの？ ─ 既存手段との比較

| 比較軸 | 公式ドキュメント / Changelog | 個人のCLAUDE.md | **本リポジトリ** |
|---|---|---|---|
| **網羅性** | 機能単位で分散、全体像が掴みにくい | 自分のプロジェクトに特化 | 9 概念（サブエージェント・スキル・コマンド・フック・MCP・設定・メモリ・ワークフロー・先進機能）を**横断的に整理** |
| **実例** | コードスニペット程度 | 自己流の断片 | `.claude/` 配下に**コピー可能な完全なリファレンス実装**がある |
| **設計指針** | 「何ができるか」止まり | 暗黙知 | **「何をどう組み合わせるべきか」**まで踏み込む（例：コマンドでワークフロー起動→エージェントに委譲→スキルで知識注入、という3層設計） |
| **鮮度** | リリース時に更新 | 自分で追従が必要 | Changelog 差分を追跡する仕組み（`workflow-*-agent`）を内蔵し、**ドリフト検知で自己更新**する |
| **チーム共有** | 各自が読む | 共有しにくい | `settings.json`（チーム共有）と `settings.local.json`（個人上書き）の**5 層設定階層**をそのまま使える |

一言でまとめると、**「Claude Code の `.claude/` ディレクトリの"お手本"をまるごと提供してくれる」** のが最大の価値。ゼロから設計する試行錯誤を省き、実証済みのパターンを自分のプロジェクトに移植できる。

---

## 使うときの流れ

```
1. 理解する ─ 概念を把握
   └─ README.md の CONCEPTS テーブルで 9 概念の全体像を掴む
   └─ best-practice/ 配下の文書で各機能の詳細・frontmatter 仕様を確認

2. 真似る ─ 設定とパターンをコピー
   └─ .claude/ ディレクトリ構造（agents/, commands/, skills/, hooks/）を
      自分のプロジェクトにコピーし、不要な部分を削る
   └─ settings.json のパーミッション設定・フック設定を参考に自プロジェクト版を作成
   └─ CLAUDE.md を 200 行以内で書き、溢れたら .claude/rules/ に分割

3. 組み立てる ─ ワークフローを設計
   └─ orchestration-workflow/ の天気デモを参考に
      「Command → Agent → Skill」の 3 層パターンで自分のワークフローを構築
   └─ サブエージェントは Agent ツールで呼び出し、bash 経由では呼ばない
   └─ 汎用エージェントではなく、機能特化エージェント＋スキル（段階的開示）で設計

4. 運用する ─ コンテキスト管理とメンテナンス
   └─ コンテキスト 50% で手動 /compact を実行
   └─ 複雑なタスクは Plan モードから開始し、サブタスクは 50% 以内で完了する粒度に分割
   └─ Git コミットはファイル単位で分離（レビュー・revert しやすくする）
```

**最小限の始め方**: `best-practice/claude-memory.md` を読んで CLAUDE.md を書く → `best-practice/claude-commands.md` を読んでコマンドを 1 つ作る → 動いたらエージェント・スキルに拡張、という段階的アプローチが推奨される。
