---
url: https://github.com/davila7/claude-code-templates
keywords: Claude Code, コンポーネントライブラリ, CLI, エージェント, MCP
oneliner: Claude Code 向けのエージェント・コマンド・フック等のコンポーネントを npx 1コマンドでプロジェクトへインストールできるパッケージ管理CLI。
---

## このリポジトリは何？

**Claude Code** (Anthropic の AI コーディングツール) の設定ファイル群を「コンポーネント」として管理・配布する npm パッケージ (`claude-code-templates`) とその周辺インフラのモノレポ。

コンポーネントは以下の 6 種類：

| 種別 | 件数 | 概要 |
|---|---|---|
| **Agents** | 600+ | フロントエンド/DB/セキュリティ等の専門家ペルソナ |
| **Commands** | 200+ | `/create-pr` など Claude Code スラッシュコマンド |
| **MCPs** | 55+ | Stripe・Supabase・GitHub 等の外部サービス連携 |
| **Settings** | 60+ | Claude Code の動作設定ファイル |
| **Hooks** | 39+ | コミット前シークレットスキャン等の自動化トリガー |
| **Templates** | 14+ | プロジェクト丸ごとの設定セット |

---

## 何が嬉しいのか（既存手段との比較）

### 既存の手段
- **手書き**: `CLAUDE.md` や `.claude/agents/*.md` を自分で書く → 書式を覚える必要があり、書いたものは再利用されない
- **Cursor Rules / GitHub Copilot 指示ファイル**: ツール固有の設定が必要で相互流用不可
- **ChatGPT GPTs / Custom Instructions**: プロジェクト単位への適用が難しく、コード編集権限もない

### このリポジトリの優位点
| 観点 | 手書き | claude-code-templates |
|---|---|---|
| 初期コスト | 高（書式習得 + ゼロから作成） | 低（1 コマンドで完了） |
| 再利用性 | 個人ローカルのみ | OSS コミュニティと共有 |
| 品質担保 | なし | `component-reviewer` エージェントが自動検証 |
| カスタマイズ | 完全自由 | コンポーネント + 追記の組み合わせ |
| コンポーネント数 | 0 | 900+ |

npm における `create-react-app` に近い立ち位置——Claude Code 設定のパッケージマネージャー。

---

## 使うときの流れ

### 1. 探す
```
https://aitmpl.com  # ブラウザで検索・閲覧
```
または対話型 CLI で選ぶ：
```bash
npx claude-code-templates@latest
```

### 2. インストール（プロジェクトルートで実行）
```bash
# 単体インストール
npx claude-code-templates@latest --agent frontend-developer

# 複数一括
npx claude-code-templates@latest \
  --agent security-auditor \
  --command security-audit \
  --hook security/secret-scanner \
  --setting read-only-mode
```

→ `.claude/agents/frontend-developer.md` などが自動生成される。

### 3. Claude Code から呼び出す
```
# Claude Code のチャット内で
Use the frontend-developer agent to build a React dashboard.
```
または `/security-audit` などのスラッシュコマンドをそのまま実行。

### 4. （任意）自作コンポーネントを追加・公開
```
cli-tool/components/agents/{category}/{name}.md を作成
↓
component-reviewer エージェントでレビュー
↓
python scripts/generate_components_json.py でカタログ更新
↓
PR → マージでコミュニティに公開
```

---

**一言まとめ**: Claude Code の設定を「書く」から「インストールする」に変えるコンポーネントレジストリ。900+ の即戦力コンポーネントを 1 コマンドで取得でき、専門的なエージェントペルソナやセキュリティフックを手間なく導入できる。
