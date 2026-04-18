---
url: https://github.com/tractorjuice/arc-kit
keywords: エンタープライズアーキテクチャ, ガバナンス, UK政府, ベンダー調達, AIアシスタント, スラッシュコマンド, テンプレート駆動, Claude Code プラグイン
oneliner: AIコーディングアシスタント上でスラッシュコマンドを叩くだけで、要件定義から調達・設計レビューまでのエンタープライズアーキテクチャ成果物を体系的に生成するガバナンスツールキット。
---

# ArcKit — Enterprise Architecture Governance & Vendor Procurement Toolkit

## このリポジトリは何？

**ArcKit** は、エンタープライズアーキテクト向けの「AI 駆動ガバナンス」ツールキットです。Claude Code / Gemini CLI / GitHub Copilot / Codex CLI / OpenCode CLI といった AI アシスタント上に **68 個のスラッシュコマンド**（`/arckit.requirements`, `/arckit.sobc`, `/arckit.risk`, `/arckit.wardley` など）を注入し、テンプレート駆動でアーキテクチャ成果物（要件書、リスクレジスタ、SOBC ビジネスケース、データモデル、Wardley Map、ADR、DPIA、RFP、HLD/DLD レビューなど）を自動生成します。

配布形態は 6 種類：

1. **Claude Code プラグイン** (`arckit-claude/`) — 主戦場。10 個の自律調査エージェント、5 種のフック、MCP サーバ（AWS Knowledge / Microsoft Learn / GCP / govreposcrape）同梱
2. **Gemini CLI 拡張** (`arckit-gemini/`)
3. **OpenCode CLI 拡張** (`arckit-opencode/`)
4. **Codex CLI 拡張** (`arckit-codex/`)
5. **GitHub Copilot 拡張** (`arckit-copilot/`) — `.github/prompts/` ＋ カスタムエージェント
6. **Python CLI** (`src/arckit_cli/`) — `arckit init` でプロジェクト雛形を展開

成果物は `projects/NNN-<name>/ARC-NNN-<TYPE>-vX.Y.md` という統一ファイル名規約で Git 管理されます。HM Treasury Green Book（SOBC）、Orange Book（リスク）、GDS Service Standard、Technology Code of Practice、NCSC CAF、UK GDPR、MOD JSP 440/936 など **UK 公共部門コンプライアンス** に深く対応している点が特徴です。

## 何が嬉しい？既存手段との比較

従来の EA ガバナンスは「Word / Confluence / PowerPoint に散在」「フォーマット不統一」「要件と設計のトレーサビリティ喪失」「ベンダー評価が属人的」といった課題を抱えます。ArcKit は次の点で差別化されます：

| 観点 | 既存手段（Word/Confluence/手書き）| **ArcKit** |
|---|---|---|
| ドキュメント生成 | ゼロから執筆、抜け漏れ多発 | テンプレート駆動 + AI 生成、Document Control ヘッダ自動付与 |
| トレーサビリティ | 手動リンク、すぐ陳腐化 | Stakeholder → Goal → Requirement (BR/FR/NFR/INT/DR) → Data Model → Component → Story まで機械的に連鎖 |
| ベンダー評価 | Excel、バイアス混入 | `/arckit.evaluate` で構造化スコアリング、G-Cloud/DOS 連携 |
| 調査コスト | 手作業 WebSearch | `arckit-research` など 10 の自律エージェントが数十回の Web/MCP 呼び出しを隔離コンテキストで実行 |
| UK 政府準拠 | チェックリストを自作 | TCoP 13 項目、Service Standard 14 点、CAF、ATRS、JSP 936 を専用コマンドで評価 |
| バージョン管理 | SharePoint 履歴頼み | Git ネイティブ、`ARC-NNN-TYPE-vX.Y.md` 命名規則をフックで強制 |
| 複数 AI 対応 | ― | 1 ソース (`arckit-claude/`) から `scripts/converter.py` が 5 プラットフォーム分を生成 |

類似の ADR ツール（adr-tools）、Structurizr、Archi、C4 モデル単体と比べ、**「アーキテクチャ全ライフサイクル（企画→ガバナンス→調達→設計→運用→レビュー）を 1 本のワークフローで貫く」** 点が独自価値です。

## 使うときの流れ

1. **導入**：Claude Code なら `/plugin marketplace add tractorjuice/arc-kit` → プラグイン有効化。その他は `pip install git+...` ＋ `arckit init my-project --ai codex|copilot|opencode`。
2. **Phase 0–1 基盤**：`/arckit.plan`（全体計画）→ `/arckit.principles`（アーキテクチャ原則）。
3. **Phase 2–4 ガバナンス**：`/arckit.stakeholders` → `/arckit.risk`（Orange Book）→ `/arckit.sobc`（Green Book 5-case）で投資判断。
4. **Phase 5–7 定義と戦略**：`/arckit.requirements` → `/arckit.data-model` → `/arckit.dpia` → `/arckit.datascout` → `/arckit.research`（build vs buy）→ `/arckit.wardley` → `/arckit.roadmap` → `/arckit.strategy` → `/arckit.adr`。
5. **Phase 8 調達**（必要時）：`/arckit.sow` / `/arckit.dos` / `/arckit.gcloud-search` / `/arckit.evaluate`。
6. **Phase 9–11 設計と運用**：`/arckit.hld-review` → `/arckit.dld-review` → `/arckit.backlog`（→ Trello/Jira エクスポート）→ `/arckit.servicenow`。
7. **Phase 12–14 検査**：`/arckit.traceability` → `/arckit.analyze` → UK 政府系なら `/arckit.tcop` / `/arckit.secure` / `/arckit.service-assessment` / `/arckit.ai-playbook` など。
8. **Phase 15–16 公開**：`/arckit.story`（プロジェクト史）→ `/arckit.presentation`（MARP スライド）→ `/arckit.pages`（静的サイト生成）で成果物を配布。

各コマンドは `handoffs:` メタデータで次のコマンドを提案し、テンプレートは `.arckit/templates-custom/` でユーザカスタマイズを保持したまま更新可能。Document Control ヘッダ（分類、レビュー期限、承認者等）は全テンプレートに統一付与され、フックが古い成果物を自動検知します。
