---
url: https://github.com/RooCodeInc/Roo-Code
keywords: VSCode拡張, AIコーディングエージェント, マルチLLM対応, 自律エージェント, カスタムモード
oneliner: VSCode上で動作するオープンソースのAI自律コーディングエージェントで、40以上のLLMプロバイダーに対応しファイル操作・コマンド実行・コードレビューを自動化する。
---

# Roo Code — リポジトリ解説

## このリポジトリは何？

**Roo Code** は VS Code 拡張として動作する **AI 自律コーディングエージェント**。  
「_Your AI-Powered Dev Team, Right in Your Editor_」をコンセプトに、LLM がファイルの読み書き・ターミナルコマンド実行・コードベース検索などをエージェントループで自動的に行う。

### 構成（Turbo + pnpm モノレポ）

| パッケージ | 役割 |
|---|---|
| `src/` | VS Code 拡張本体 |
| `apps/cli` | `roo` CLI ツール |
| `packages/core` | プラットフォーム非依存のエージェントコア |
| `packages/types` | 共有 TypeScript 型定義 |
| `apps/web-roo-code` | Web ダッシュボード（Next.js） |

---

## 何が嬉しいの？

### 既存ツールとの比較

| 機能 | **Roo Code** | GitHub Copilot | Cursor | Cline |
|---|---|---|---|---|
| エージェントループ | ✅ 完全自律 | ❌ 補完のみ | △ 部分的 | ✅ |
| LLM プロバイダー | ✅ **40+ 対応** | ❌ 独自 | ❌ 独自 | △ 数種 |
| カスタムモード | ✅ 18+ 内蔵＋自作可 | ❌ | ❌ | ❌ |
| ターミナル実行 | ✅ | ❌ | ❌ | ✅ |
| チェックポイント | ✅ 状態保存・復元 | ❌ | ❌ | ❌ |
| CLI ツール | ✅ | ❌ | ❌ | ❌ |
| セルフホスト LLM | ✅ Ollama / LM Studio | ❌ | ❌ | △ |
| OSS | ✅ Apache 2.0 | ❌ | ❌ | ✅ |

### 主な差別化ポイント

1. **40+ LLM プロバイダー対応** — Anthropic, OpenAI, Gemini, Deepseek, AWS Bedrock, Ollama など何でも使える
2. **アダプティブモード** — `Code` / `Architect` / `Debug` / `Ask` などを切り替え可能。`.roomodes` ファイルでプロジェクト固有のカスタムモードも定義できる
3. **26+ エージェントツール** — ファイル操作・差分適用・コードベース検索・MCP 連携など揃っており、LLM が自律的に組み合わせて使う
4. **チェックポイント機能** — タスクの状態を保存し、途中から再開・巻き戻しが可能
5. **安全設計** — デフォルトは diff / コマンドを表示して都度承認。自動承認モードも選択可能

---

## 使うときの流れ

### 1. インストール

```bash
# VS Code マーケットプレイスから
ext install RooVeterinaryInc.roo-cline

# または CLI
npm install -g @roo-code/cli
```

### 2. プロバイダー設定

VS Code 設定（または `.env`）で使いたい LLM とキーを指定。

### 3. タスクを投げる

**サイドバー（GUI）**

- サイドバーのチャット欄に指示を入力 → エージェントが計画・提案・実行
- 差分やコマンドは承認ダイアログで確認してから適用

**CLI（自動化・CI 向け）**

```bash
roo "ユーザー認証モジュールを実装して"          # インタラクティブ
roo -p "バグを修正して" --output-format json   # 非インタラクティブ
roo -c                                         # 直前のタスクを継続
roo --session-id <id>                          # セッション再開
```

### 4. エージェントループの内部フロー

```
入力プロンプト
  → モード選択（Code / Architect / Debug …）
  → LLM が計画立案・ツール呼び出しを提案
  → ユーザー承認（or 自動承認）
  → ファイル操作 / コマンド実行 / 検索
  → 結果を LLM にフィードバック → 繰り返し
  → タスク完了 or チェックポイント保存
```

### 5. カスタマイズ（任意）

```yaml
# .roomodes（プロジェクトルート）
customModes:
  - slug: reviewer
    name: Code Reviewer
    roleDefinition: "コードレビュアーとして..."
    groups: [read]
```

プロジェクト専用の役割・制約を持つエージェントモードを簡単に追加できる。

---

**現在のバージョン**: v3.53.0（累計 300 万+ インストール）  
**ライセンス**: Apache 2.0
