---
url: https://github.com/Tracer-Cloud/opensre
keywords: AI SRE, incident response, LangGraph, observability, RCA
oneliner: 本番インフラのインシデント調査・根本原因分析を自動化するオープンソースのAI SREエージェント構築フレームワーク。
---

# OpenSRE リポジトリ概要

## このリポジトリは何？

**OpenSRE** は Tracer-Cloud が開発する、**自前の AI SRE（Site Reliability Engineer）エージェントを構築・運用・評価するためのオープンソース・フレームワーク**（Apache 2.0、Python 製、Public Alpha）。

- 本番で障害が起きた際、ログ・メトリクス・トレース・Runbook・Slack スレッドなど散在する情報を LLM エージェントが自動で横断調査し、**根本原因（RCA）レポート**を生成する。
- 提供内容は大きく3層:
  1. **エージェント本体**: `opensre` CLI + LangGraph ベースのパイプライン（`app/graph_pipeline.py`, `app/nodes/`, `app/pipeline/`）。Anthropic / OpenAI / Ollama / Gemini / OpenRouter / NVIDIA NIM / Bedrock を差し替え可能。
  2. **60+ 統合**: Grafana, Datadog, CloudWatch, Sentry, Kubernetes, AWS, GitHub, Slack, PagerDuty, MCP/ACP 等を `app/integrations/` として実装。
  3. **評価・学習環境**: `tests/synthetic/`（採点付きの合成 RCA シナリオ）と `tests/e2e/`（Kubernetes / EC2 / Lambda / ECS Fargate / Flink 等の実クラウド E2E）。将来的に **AI SRE 版 SWE-bench** を目指すベンチマーク基盤でもある。
- Railway へのデプロイや、デプロイ済みサービスのリモート操作（`opensre remote ops logs/status/restart`）にも対応。

## 既存手段と比較した嬉しさ

| 比較対象 | 既存の手段 | OpenSRE の嬉しさ |
|---|---|---|
| **PagerDuty AIOps / Datadog Watchdog / New Relic AI など商用 AIOps** | SaaS にログを送り、クローズドなモデルで相関解析。ブラックボックスかつ自社データが外に出る。 | Apache 2.0・**自社インフラで完結**。生ログはセッション外に保持しない。LLM・プロンプト・ツール呼び出しが監査可能。 |
| **自作 LangChain / LangGraph エージェント** | 統合（Datadog, k8s, Slack, GitHub …）を全部自分で書く必要。評価基盤も自前。 | 60+ 統合と LangGraph パイプライン、CLI、onboarding がすでに揃う。**テスト用合成インシデントと E2E スイートが同梱**され、精度改善のループが回せる。 |
| **Runbook 自動化（Rundeck, StackStorm）** | 事前に書いたスクリプトを実行するだけで「診断」は人間。 | Runbook を**読み取って推論**し、証拠リンク付き RCA を出して Slack / PagerDuty に要約投稿。 |
| **コード用 SWE-bench 系ベンチ** | コード修正用で、分散システム障害には使えない。 | 分散障害・敵対的なノイズを含む**本番 RCA 用のベンチ兼訓練環境**を志向。 |

要するに「**自分の環境に閉じた AI SRE を、統合と評価セットごと手に入れられる**」点が中核価値。

## 利用の流れ

1. **インストール**: `curl … install.sh | bash` / `brew install Tracer-Cloud/opensre/opensre` / `irm install.ps1 | iex`。開発参加なら `git clone && make install`。
2. **オンボーディング**: `opensre onboard` で LLM プロバイダ（Anthropic など）を選び、Grafana / Datadog / Honeycomb / Coralogix / Slack / AWS / GitHub MCP / Sentry 等の認証情報を検証・保存。
3. **調査実行**: アラート JSON（例: `tests/e2e/kubernetes/fixtures/datadog_k8s_alert.json`）を `opensre investigate -i <alert.json>` に渡すと、
   - アラート取得 → 関連ログ/メトリクス/トレース収集 → 異常の相関推論 → 根本原因と証拠リンク付きレポート生成 → 次アクション提案 → Slack/PagerDuty へ要約投稿、が一気通貫で走る。
4. **精度検証**: `make benchmark` / `make test-rca` で合成 RCA を採点、`tests/e2e/` で実クラウドシナリオを回して回帰を防ぐ。
5. **本番運用**: `opensre deploy railway --project … --service …`（事前に Postgres/Redis と `DATABASE_URI`/`REDIS_URI` を設定）でホスティング。運用後は `opensre remote ops status/logs --follow/restart` で面倒を見る。
6. **更新・拡張**: `opensre update` で CLI を更新。統合追加・runbook 改善は `CONTRIBUTING.md` に沿って PR。テレメトリは `OPENSRE_NO_TELEMETRY=1` でオフ可能。
