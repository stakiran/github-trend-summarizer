---
url: https://github.com/anthropics/financial-services
keywords: Claude, financial-services, plugins, managed-agents, MCP, skills, investment-banking, equity-research
oneliner: 投資銀行・エクイティリサーチ・PE・ウェルスマネジメント向けの Claude エージェント／スキル／データコネクタのリファレンス実装集（Anthropic 公式）。
---

# anthropics/financial-services 概要

## このリポジトリは何？

Anthropic が公式に公開している **「金融サービス業務向け Claude リファレンス実装集」**。投資銀行 (IB)、エクイティリサーチ、プライベートエクイティ (PE)、ウェルスマネジメント、ファンドアドミン、KYC など、現場で頻出するワークフローを Claude エージェントとして実装したテンプレート集である。

中身は大きく3層に分かれる。

- **Agents (`plugins/agent-plugins/`)** — 業務単位で完結するエージェント群。Pitch Agent、Meeting Prep、Market Researcher、Earnings Reviewer、Model Builder、Valuation Reviewer、GL Reconciler、Month-End Closer、Statement Auditor、KYC Screener の10種。
- **Vertical plugins (`plugins/vertical-plugins/`)** — 業種別のスキル＋スラッシュコマンド束（`/comps`, `/dcf`, `/lbo`, `/earnings`, `/ic-memo`, `/tlh` …）と、Daloopa／Morningstar／FactSet／S&P／Moody's／LSEG／PitchBook／Egnyte 等の **MCP データコネクタ** を同梱。
- **Managed-agent cookbooks (`managed-agent-cookbooks/`)** — 同じシステムプロンプト・スキルを Anthropic Managed Agents API (`/v1/agents`) にヘッドレスでデプロイするための `agent.yaml` 群。

すべて Markdown と YAML／JSON のみ。ビルド工程はなく、Python スクリプト (`check.py`, `sync-agent-skills.py`, `orchestrate.py`, `deploy-managed-agent.sh`) が検証・同期・デプロイを担う。

## 何が嬉しい？（既存手段との比較）

| 比較対象 | 違い／このリポジトリの利点 |
|---|---|
| **Claude をゼロからプロンプトで運用** | コンプス、DCF、LBO、3表モデル、Excel 監査、IC メモ、KYC ルール評価といった **金融固有の手順とフォーマットがスキル化** 済み。アナリスト成果物に必要な「お作法」を自前で書き起こす必要がない。 |
| **Bloomberg / FactSet / Capital IQ などのベンダー個別ツール** | LSEG・S&P・Daloopa・PitchBook など **11種のデータプロバイダを MCP で横断接続** でき、同じエージェントの中で連携できる。ベンダーロックインから解放される。 |
| **汎用 RPA / Copilot 系（Microsoft 365 Copilot 等）** | 単発タスクでなく **「ワークフロー単位のエージェント」** として設計され、各エージェントが自分の使うスキルを自己完結で同梱。Excel／PowerPoint への成果物出力 (`xlsx-author`, `pptx-author`, `ppt-template`) もネイティブ対応。 |
| **自社内製エージェント** | 同一ソースから **Claude Cowork プラグイン** としても **Managed Agents API** としてもデプロイ可能（"two ways from one source"）。インタラクティブ用途と無人実行用途を分岐実装する必要がない。 |
| **OSS LLM テンプレート** | Anthropic 公式・Apache-2.0、`scripts/check.py` でマニフェスト lint と参照整合性検査が走り、**人間サインオフ前提の安全設計**（投資判断・取引執行・元帳記帳はしない）が明示。規制業界で導入しやすい。 |

要するに、**「金融アナリスト業務をすぐ走らせられる、ベンダー中立かつ二経路デプロイ可能な Claude リファレンス」** という点が最大の差別化。

## 使うときの流れ

1. **インストール経路を選ぶ**
   - 対話用途 → **Cowork**: Settings → Plugins → Add plugin にリポジトリ URL を貼るか、`plugins/` 配下を zip でアップロード。
   - CLI → **Claude Code**:
     ```bash
     claude plugin marketplace add anthropics/claude-for-financial-services
     claude plugin install financial-analysis@claude-for-financial-services   # まずコア
     claude plugin install pitch-agent@claude-for-financial-services           # 必要な agent を追加
     ```
   - 無人運用 → **Managed Agents**:
     ```bash
     export ANTHROPIC_API_KEY=sk-ant-...
     scripts/deploy-managed-agent.sh gl-reconciler
     ```
2. **コアを最初に入れる** — `financial-analysis` プラグインに共通モデリングスキルと全 MCP コネクタが集約されているので、ここから始めて必要な vertical（`investment-banking`、`equity-research`、`private-equity`、`wealth-management`、`fund-admin`、`operations` など）を追加する。
3. **データ接続を構成** — `.mcp.json` でベンダー（Daloopa／Morningstar／FactSet／S&P／LSEG／PitchBook 等）の MCP に API キーを設定。社内データソースに差し替えてもよい。
4. **使う**
   - エージェントは Cowork ディスパッチに登場し、関連局面で自動的にスキルが発火。
   - スラッシュコマンドで明示的に呼び出す：`/comps`、`/dcf`、`/earnings`、`/ic-memo`、`/tlh` など。
   - 出力は Excel／PowerPoint／Markdown ドラフトとして **人間レビュー前提** で staging される。
5. **自社向けにチューニング**
   - `.mcp.json` を社内データに向ける。
   - スキルファイルに firm 用語・テンプレート・規程を追記。
   - `/ppt-template` で自社ブランドの PPT レイアウトを学習させる。
   - 新スキルを `vertical-plugins/<vertical>/skills/` に追加し、`python3 scripts/sync-agent-skills.py` で各エージェントへ伝播。
6. **PR 前検証** — `python3 scripts/check.py` でマニフェスト lint・参照解決・スキルドリフト検出を実行。
7. **（任意）Microsoft 365 連携** — `claude-for-msft-365-install` プラグインで、Excel/PowerPoint/Word/Outlook の Claude アドインを自社クラウド（Vertex AI／Bedrock／社内 LLM ゲートウェイ）経由で配備。
