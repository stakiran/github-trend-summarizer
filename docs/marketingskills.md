---
url: https://github.com/coreyhaines31/marketingskills
keywords: Agent Skills, マーケティング, CRO, SEO, コピーライティング, Claude Code, プラグイン, Growth
oneliner: マーケティング業務（CRO・コピー・SEO・分析・グロース）を AI エージェントに任せるための Agent Skills 集。
---

# coreyhaines31/marketingskills

## このリポジトリは何？

**Marketing Skills** は、マーケティング業務に特化した **AI エージェント用「Skill」集**。Corey Haines 氏が MIT ライセンスで公開している。

- 中身は **37 個のマーケティング Skill**（Markdown ファイル群）。たとえば `page-cro`（ランディングページ改善）、`copywriting`、`seo-audit`、`ai-seo`、`email-sequence`、`cold-email`、`paid-ads`、`ab-test-setup`、`pricing-strategy`、`referral-program`、`revops` など、CRO / コピー / SEO / 有料広告 / リテンション / セールス領域を網羅。
- [Agent Skills 仕様](https://agentskills.io) 準拠で、**Claude Code / Codex / Cursor / Windsurf** など複数のエージェントで横断利用できる。Claude Code 向けには `.claude-plugin/marketplace.json` が同梱され、**プラグインマーケットプレイス**としても機能する。
- おまけとして `tools/` 配下に **51 個の Zero-dependency Node.js CLI**（GA4、Stripe、HubSpot、Ahrefs、Meta Ads など各 SaaS 用）と、各ツールの API 連携ガイド（`tools/integrations/*.md`）、Composio 経由の MCP マッピングが用意されている。
- 各 Skill は SKILL.md 内で YAML frontmatter（`name`／`description`）＋手順記述で構成。すべての Skill がまず `.agents/product-marketing-context.md`（製品・ICP・ポジショニング情報）を参照し、そこからタスク別のフレームワークを適用する設計。

## 何が嬉しいか？既存手段との比較

| 比較対象 | 既存手段の課題 | このリポジトリで解決される点 |
|---|---|---|
| **プロンプトを毎回自作** | 質が属人的、再利用できない、文脈の説明をやり直す | CRO/SEO/コピーのベストプラクティスがフレームワーク化済み。「LP 改善して」で `page-cro` が自動発火 |
| **ChatGPT / Claude に素で聞く** | 一般論しか出ない、自社プロダクト文脈を毎回入力 | `product-marketing-context` が一度きりの設定で全 Skill から共有される |
| **Notion / Google Docs のプレイブック** | 人間は読むが、AI は読まない | エージェントが自動ディスカバリして適用する |
| **Marketing SaaS（Jasper, Copy.ai 等）** | 月額課金、ツールに閉じた UI、コード作業と分断 | 自分のエディタ／ターミナルで完結、MIT で無料、自分の GitHub/コードベースに直接反映 |
| **Anthropic 公式 Skill の汎用セット** | 汎用タスク（PDF 処理等）寄り | マーケ特化で 37 本、互いに参照し合うよう設計されている |
| **単発のカスタム GPT / Gem** | 単一エージェント縛り、Skill 間連携なし | クロスエージェント、Skill 同士がリンク（例：`copywriting` ↔ `page-cro` ↔ `ab-test-setup`）|

要は、**「技術寄りのマーケター／創業者が、自分のコーディングエージェントをそのまま CMO 補佐として使えるようになる」**のが最大の価値。

## 使うときの流れ

1. **インストール**（どれか1つ）
   - 推奨：`npx skills add coreyhaines31/marketingskills`（`.agents/skills/` に配置、Claude Code 用に `.claude/skills/` へもシンボリックリンク）
   - Claude Code プラグイン：`/plugin marketplace add coreyhaines31/marketingskills` → `/plugin install marketing-skills`
   - その他、`git clone` / submodule / fork / SkillKit もサポート
2. **前提コンテキストを1回作る**
   - `product-marketing-context` Skill を最初に実行し、`.agents/product-marketing-context.md`（製品概要、ICP、ベネフィット、顧客の生の声、競合など）を生成。README やコードから自動ドラフト → 人がレビュー・加筆の流れ。
3. **自然文 or スラッシュで Skill を呼ぶ**
   - 「このランディングページの改善点を出して」→ `page-cro` が自動起動
   - 「5通のウェルカムメール作って」→ `email-sequence`
   - 明示指定：`/seo-audit`、`/copywriting`、`/ab-test-setup` など
4. **Skill 内の標準フレームワークに沿って実行される**
   - 例：`page-cro` なら「Initial Assessment → 価値提案の明瞭度 → 見出し → CTA → ソーシャルプルーフ → …」の順に分析・提案
   - 必要に応じて関連 Skill（Related Skills 節）へ自動遷移
5. **必要なら外部ツールと連携**
   - `tools/REGISTRY.md` から該当 SaaS を特定し、`tools/integrations/<tool>.md` の API ガイド、または `tools/clis/<tool>.js` の CLI で実データ取得・書き込みを行う（GA4 抽出、HubSpot 更新、広告配信など）。MCP 未対応のツールは Composio 経由。
6. **運用**
   - セッションの最初に `VERSIONS.md` を見て更新有無をチェック、`update skills` で `git pull`
   - カスタマイズしたい場合は fork、または `.claude/skills/` 以下で上書き（Claude Code 限定の `!``command``` 動的差し込み等もここで使う）
