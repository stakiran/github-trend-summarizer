---
url: https://github.com/VoltAgent/awesome-agent-skills
keywords: agent-skills, awesome-list, claude-code, codex, ai-coding-assistant
oneliner: Claude Code / Codex / Cursor などに対応した「Agent Skill」1100+ 件を、公式配布と実運用されている有用なものだけに絞って厳選した awesome リスト。
---

# awesome-agent-skills 要約

## このリポジトリは何？

**AI コーディングアシスタント向け「Agent Skill」のキュレーションリスト**（awesome リスト形式）。README.md 1,494 行に、1,100+ の Skill がカテゴリ別にリンク集として掲載されているだけのシンプルな構成（他には LICENSE と CONTRIBUTING.md のみ）。VoltAgent が運営。

- **Agent Skill とは**: `SKILL.md` とサポートファイルの塊で、特定ドメインの知識・手順を AI エージェントに後付けする拡張。エージェントは必要に応じて自動ロードする。
- **対応ツール**: Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Windsurf（README 末尾にプロジェクト/グローバルの配置パス対応表あり）。
- **収録範囲**:
  - **公式 Skill**: Anthropic / Vercel / Stripe / Cloudflare / Netlify / Google Gemini / HashiCorp / Cloudflare / Sentry / Hugging Face / Figma / OpenAI / MongoDB / Firebase / Flutter / Notion / Auth0 / Supabase / Neon / ClickHouse など 40+ ベンダー。
  - **コミュニティ Skill**: Marketing, Productivity, Development/Testing, Context Engineering, AI/Data, n8n Automation, Specialized Domains（法務・ゲノム・音楽・KiCad・VMware など）。
- **方針**: "Hand-picked, not AI-slop generated"。大量 AI 生成された Skill は除外し、開発チーム公式 or 実利用実績のあるものだけに絞る。CONTRIBUTING にも「作って3時間のものは受け付けない」と明記。

## 何が嬉しいのか（既存手段との比較）

| 比較対象 | このリポジトリの優位 |
|---|---|
| **Google / GitHub で個別に探す** | Skill は各チームの repo に散在している。本リストは公式＋実績ありに厳選＆分類済みで、発見コストが劇的に下がる。 |
| **[officialskills.sh](https://officialskills.sh/)（関連ポータル）** | Web ポータルは「公式のみ」寄り。このリポジトリは公式＋成熟したコミュニティ Skill まで横断、かつ PR ベースで追加/議論が透明。 |
| **AI 生成 Skill 集・大量投稿型のリポジトリ** | 品質基準（description 明瞭・progressive disclosure・絶対パス禁止・scoped tools）を README で提示し、"Quality over quantity" を実践。低品質 Skill を踏むリスクが低い。 |
| **ベンダーごとの公式ドキュメント** | 複数ベンダーを横串で比較・検索できる。類似カテゴリ（例: 認証は Better Auth / Auth0 / Supabase, DB は Neon / ClickHouse / MongoDB / DuckDB）を並べて選定可能。 |
| **awesome-claude-code-subagents 等の姉妹 awesome** | Subagent ではなく「Skill」に特化。Claude Code 以外の CLI（Codex, Gemini CLI, Cursor 等）にも配置パスを示しており、ツール非依存で使える。 |

注意: **セキュリティ監査はされていない**。README に "curated, not audited" と明記、Snyk Skill Security Scanner 等の別ツールでの検査を推奨している。

## 使うときの流れ

1. **探す**: README の目次テーブルまたはカテゴリから、自分のドメイン／ツールに合う Skill を探す（例: Next.js を書くなら `vercel-labs/next-best-practices`、Terraform なら `hashicorp/*`）。
2. **評価する**: リンク先（officialskills.sh もしくは GitHub）に飛び、`SKILL.md` とソースを読む。発行者が公式チームか、コミュニティか、最終更新はいつか等を確認。
3. **セキュリティレビュー**: プロンプトインジェクション・ツール毒化・秘密情報の取り扱いをチェック（README の Security Notice に従う）。
4. **配置する**: 使っているアシスタントに対応するパスへ Skill ディレクトリをコピー。
   - Claude Code → `.claude/skills/`（プロジェクト）/ `~/.claude/skills/`（グローバル）
   - Codex → `.agents/skills/` 
   - Cursor → `.cursor/skills/`
   - Gemini CLI → `.gemini/skills/`
   - GitHub Copilot → `.github/skills/`
   - OpenCode → `.opencode/skills/`
   - Windsurf → `.windsurf/skills/`
   - Antigravity → `.agent/skills/`
5. **使う**: エージェントが description を見て必要時に自動的にロード・呼び出す（明示的に `/skill 名前` 等で呼べる場合もある）。
6. **貢献する（任意）**: 自作 Skill が他者に使われ成熟したら、CONTRIBUTING.md の基準（10 語以内の説明・公開 repo・ドキュメント有・実利用実績）に沿って PR（タイトル `Add skill: author/skill-name`）。
