---
url: https://github.com/f/prompts.chat
keywords: AI prompts, prompt sharing, self-hosted, ChatGPT, community platform
oneliner: AIプロンプトを共有・発見・収集できるオープンソースのコミュニティプラットフォーム（旧 Awesome ChatGPT Prompts）
---

## このリポジトリは何？

**prompts.chat** は、AIプロンプトの共有・発見・収集を行うためのオープンソース Web プラットフォーム。GitHub Stars 14万超の「Awesome ChatGPT Prompts」が前身で、静的なプロンプト集から本格的な Web アプリへと進化した。

技術スタックは Next.js 16 (App Router) + React 19 + TypeScript + PostgreSQL (Prisma ORM)。Docker 一発でセルフホストでき、ブランディングや機能の ON/OFF を環境変数だけで制御可能。ChatGPT・Claude・Gemini など特定 AI に依存しない汎用設計。

---

## 何が嬉しいの？（既存手段との比較）

| 比較軸 | GitHub Gist / README 管理 | FlowGPT 等の商用サービス | **prompts.chat** |
|---|---|---|---|
| **構造化** | テキスト羅列で検索困難 | ○ | ○ カテゴリ・タグ・バージョン管理 |
| **検索** | Ctrl+F 程度 | キーワード検索 | キーワード＋**AI セマンティック検索**（OpenAI Embeddings） |
| **コミュニティ機能** | Issue/PR のみ | 投票・コメント | 投票・コメント・**Change Request（PR的な改善提案）** |
| **セルフホスト** | — | ✗（SaaS のみ） | ✓ `docker compose up` で完結。社内利用・プライバシー確保が容易 |
| **ホワイトラベル** | — | ✗ | ✓ ロゴ・色・名前を環境変数で差し替え可能 |
| **AI ツール連携** | — | 限定的 | **MCP (Model Context Protocol) サーバー内蔵**。Claude Code 等から直接プロンプトを取得・作成できる |
| **テンプレート変数** | — | 一部 | `${role:デフォルト値}` 形式で動的に値を差し込める |
| **ライセンス** | 様々 | 商用 | **CC0（パブリックドメイン）** — 自由に利用可能 |

**要するに**：個人のプロンプト管理なら Gist で十分だが、チームや組織で「プロンプトの知見を蓄積・検索・改善サイクルを回したい」場合に、商用サービスに依存せずセルフホストできる唯一の実用的選択肢。

---

## 使うときの流れ

### A. 公開インスタンス（prompts.chat）を使う場合

```
1. サイトにアクセス → プロンプトを閲覧・検索（認証不要）
2. GitHub / Google でログイン
3. プロンプトを作成（カテゴリ・タグ・変数を設定）
4. 投票・コメント・コレクション保存で活用
5. MCP 経由で Claude Code 等から直接呼び出し
```

### B. セルフホストする場合

```
1. リポジトリを clone
2. docker compose up -d  → localhost:4444 で起動
3. 環境変数でブランド名・認証プロバイダ・機能の ON/OFF を設定
   - PCHAT_NAME, PCHAT_AUTH_PROVIDERS, PCHAT_FEATURE_* 等
4. （任意）OPENAI_API_KEY を設定すると AI 検索・プロンプト改善が有効化
5. 管理者ダッシュボード（/admin）でカテゴリ・タグを整備
6. チームメンバーを招待し、プロンプトの蓄積・改善サイクルを開始
```

### C. MCP 連携（AI ツールから直接利用）

Claude Code や Claude Desktop の MCP 設定に以下を追加するだけ：

```json
{
  "mcpServers": {
    "prompts.chat": {
      "url": "https://prompts.chat/api/mcp"
    }
  }
}
```

これにより、AI ツール上から `list_prompts` / `get_prompt` / `create_prompt` 等のコマンドでプロンプトライブラリを直接操作できる。
