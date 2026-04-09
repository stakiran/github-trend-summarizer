---
url: https://github.com/coleam00/Archon
keywords: AI coding workflow, Claude Code SDK, DAG executor, worktree isolation, deterministic development
oneliner: AI コーディングエージェントの実行フローを YAML ワークフローとして定義・再現可能にするオープンソースのハーネスビルダー
---

## Archon とは何か

AI コーディングエージェント（Claude Code, Codex）に対する**ワークフローエンジン**。「Issue を直して」と頼むたびに結果がバラつく問題を、**開発プロセスそのものを YAML の DAG（有向非巡回グラフ）として定義**することで解決する。

各ノードは 4 種類ある:

| ノード種別 | 役割 |
|---|---|
| `prompt` | AI にインラインで指示を出す |
| `command` | 再利用可能な Markdown プロンプトを呼ぶ |
| `bash` | シェルスクリプトを実行（テスト・lint 等） |
| `loop` | 条件を満たすまで AI を反復実行 |

ノード間は `depends_on` で依存関係を宣言し、独立ノードは**自動的に並列実行**される。例えば「5 つのコードレビュー観点を同時に走らせ、結果を統合して自動修正する」といった並列マルチエージェントパイプラインが YAML 数十行で書ける。

実行基盤は Bun + TypeScript。Web UI（React）、CLI、Slack / Telegram / Discord / GitHub のどこからでも同じワークフローを起動でき、結果は SSE でリアルタイムにストリーミングされる。

## 既存手段と比べて何が嬉しいのか

| 比較対象 | Archon の優位点 |
|---|---|
| **素の Claude Code / Codex を直接使う** | 毎回プロンプトを手打ちする必要がなく、計画→実装→テスト→PR→レビュー→自動修正の一連を**ワンコマンドで再現可能**に実行できる。結果のブレが小さい |
| **GitHub Actions / CI** | CI は「コードが push された後」に動くが、Archon は**コードを書く工程そのもの**を自動化する。AI ノードと bash ノードを混在させ、計画・実装・検証のループを回せる |
| **Aider / Continue 等の AI コーディングツール** | 単発の対話ではなく、**複数ステップを宣言的に連鎖**できる。ノードごとに `fresh` コンテキストを切ることでコンテキスト肥大も防止。さらに git worktree による**自動隔離**で、複数タスクを安全に並行実行できる |
| **n8n / Dify 等の汎用ワークフロー** | ソフトウェア開発に特化。git worktree 隔離、`$BASE_BRANCH` / `$ARTIFACTS_DIR` 等の開発向け変数、PR 作成・レビュー統合がネイティブに組み込まれている |

要約すると、**「AI に何をどの順で考えさせ・実行させるか」をコードとしてバージョン管理し、チームで共有・再現できる**点が最大の価値。

## 使うときの流れ

```
1. セットアップ
   $ git clone → bun install → .env に ANTHROPIC_API_KEY を設定
   $ bun run dev          # Web UI (5173) + API サーバ (3090) が起動

2. プロジェクト登録
   Web UI の Projects 画面、または CLI で対象リポジトリを登録
   （ローカルパス指定 or git clone）

3. ワークフロー確認・カスタマイズ
   $ bun run cli workflow list   # 17 個のデフォルトが表示される
   必要なら .archon/workflows/ にコピーして YAML を編集

4. 実行（CLI の場合）
   $ bun run cli workflow run archon-fix-github-issue "Fix issue #42"
   → 自動で worktree が作られ、分類→調査→実装→テスト→PR→レビュー→修正が一気に走る

   実行（Web UI の場合）
   チャット欄に「Fix issue #42」と入力 → ルーターが適切なワークフローへ振り分け
   → 進捗がリアルタイムでストリーミング表示される

5. 結果確認
   完了すると PR が自動作成され、レビューコメント付きで GitHub に上がる
   Web UI の Dashboard でステータス一覧・履歴も確認可能
```

**ポイント**: ワークフローは `.archon/workflows/` に YAML でコミットしておけば、チームの誰が・どのプラットフォームから実行しても同じプロセスが再現される。「AI コーディングの属人化」を防ぐインフラとして機能する。
