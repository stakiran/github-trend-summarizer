---
url: https://github.com/addyosmani/agent-skills
keywords: AI coding agents, skills, slash commands, software lifecycle, prompt engineering, code quality
oneliner: AIコーディングエージェントに「シニアエンジニア相当の開発プロセス」を踏ませるためのスキル/スラッシュコマンド集。
---

# addyosmani/agent-skills 整理メモ

## 1. このリポジトリは何？

**「AIコーディングエージェント向けの本番品質エンジニアリング・スキル集」** です。Claude Code / Cursor / Gemini CLI / Windsurf / OpenCode / GitHub Copilot / Kiro IDE など、Markdownの指示を受け付けるエージェントなら何にでも適用できる、プロンプト/ルールファイル形式の「ワークフロー資産」です。

中身は大きく4種類のアセット：

- **20の Skill（`skills/*/SKILL.md`）**：要件定義から運用まで、ソフトウェア開発ライフサイクル全段階の手順書。例：`spec-driven-development`, `test-driven-development`, `incremental-implementation`, `code-review-and-quality`, `security-and-hardening`, `performance-optimization`, `git-workflow-and-versioning`, `shipping-and-launch` など。
- **7つのスラッシュコマンド**（Claude Code / Gemini CLI 用）：`/spec`, `/plan`, `/build`, `/test`, `/review`, `/code-simplify`, `/ship`。各コマンドが対応する Skill を自動的に呼び出すエントリポイント。
- **3つの Agent ペルソナ**（`agents/`）：`code-reviewer`（シニア・スタッフエンジニア視点）/ `test-engineer`（QA視点）/ `security-auditor`（脅威モデリング・OWASP視点）。
- **4つの Reference チェックリスト**（`references/`）：testing / security / performance / accessibility の詳細項目を、必要時のみロードするための補助資料。

各 Skill は **「Overview / When to Use / Process / Common Rationalizations（言い訳と反論）/ Red Flags / Verification（証跡）」** という固定アナトミーで書かれており、エージェントが手順をスキップしないよう"反・合理化テーブル"と"検証ゲート"が組み込まれている点が特徴。Google の *Software Engineering at Google* と *engineering practices guide* の概念（Hyrum's Law、Beyonce Rule、テストピラミッド、Chesterton's Fence、Trunk-Based Development、Shift Left など）が手順に直接埋め込まれています。

## 2. 何が嬉しいの？（既存手段との比較）

AIエージェントは放っておくと「最短ルート」を走り、仕様書・テスト・セキュリティレビューなどを省きがち。これに対し本リポジトリは：

| 観点 | 一般的な `CLAUDE.md` / `.cursorrules` の自前ルール | Awesome系プロンプト集 | **agent-skills** |
|---|---|---|---|
| 粒度 | 散文的・属人的 | 単発プロンプト中心 | **手順 + 検証 + 出口条件**まで揃った"プロセス" |
| ライフサイクル網羅 | 部分的 | バラバラ | Define→Plan→Build→Verify→Review→Ship を**一貫設計** |
| サボり防止 | なし | なし | **Anti-rationalization 表**（"後でテスト書く"等への反論を内蔵）|
| 検証 | 任意 | 任意 | **証跡必須**（テストパス・ビルド出力・実測値）|
| ツール非依存 | エージェント依存 | 形式バラバラ | プレーンMarkdownなので**主要ツール全部に流用可** |
| コンテキスト効率 | 全部突っ込みがち | - | **Progressive disclosure**（必要時のみ参照） |

要するに、「シニアエンジニアが当たり前にやる規律」をテンプレ化してエージェントに強制させ、**プロトタイプ品質→本番品質**へ底上げするための"装備一式"。自分でプロンプトを書き溜めるより、検証ゲート・反論テーブル付きで完成度が高い。

## 3. 使うときの流れ

### インストール（Claude Code 例）
```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```
※ 他ツールは `docs/<tool>-setup.md` 参照。プレーンMarkdownなのでコピペでも動く。

### 推奨ロード（最小構成）
まずは3つだけ読み込む：`spec-driven-development` / `test-driven-development` / `code-review-and-quality`。

### 開発ライフサイクルでの典型フロー
```
   /spec        /plan         /build         /test        /review        /ship
 ┌──────┐    ┌──────┐     ┌──────┐      ┌──────┐    ┌──────┐      ┌──────┐
 │ Idea │ →  │ Spec │ →   │ Code │  →   │ Test │ →  │  QA  │  →   │  Go  │
 │Refine│    │ PRD  │     │ Impl │      │Debug │    │ Gate │      │ Live │
 └──────┘    └──────┘     └──────┘      └──────┘    └──────┘      └──────┘
```

1. **`/spec`** … 何を作るか PRD を書く（`SPEC.md` 生成）。  
2. **`/plan`** … 仕様を小さな実装可能タスクに分解（`tasks/plan.md`, `tasks/todo.md` 生成）。  
3. **`/build`** … 薄い垂直スライス単位で実装→テスト→検証→コミット。フィーチャーフラグ・安全なデフォルト・ロールバック容易性を確保。UI なら `frontend-ui-engineering` が、API なら `api-and-interface-design` が自動的に発火。  
4. **`/test`** … Red-Green-Refactor、80/15/5 ピラミッド、DAMP > DRY、Beyonceルール等。失敗テストの triage は `debugging-and-error-recovery`。  
5. **`/review`** … ~100行単位の五軸レビュー、Severityラベル、`code-reviewer` ペルソナ起動。必要なら `security-auditor` / `test-engineer` も呼ぶ。`/code-simplify` で Chesterton's Fence と Rule of 500 を適用。  
6. **`/ship`** … pre-launch チェックリスト、段階的ロールアウト、フラグライフサイクル、ロールバック手順、モニタリング。

### 補助
- 詳細パターンが必要なら `references/*.md`（testing/security/performance/a11y）を都度ロード。  
- `SPEC.md` や `tasks/*` は **作業中のリビングドキュメント**。マージ前に消すか、`.gitignore` に入れるかは任意。  
- 全 Skill を一度にロードしないこと（コンテキスト浪費）。タスクに応じて選択ロード。

> **設計哲学**：「Process, not prose」「Verification is non-negotiable」「Anti-rationalization built-in」「Progressive disclosure」。"なんとなく合ってそう"を許さず、テスト・実測・出力で証拠を出させるのが核。
