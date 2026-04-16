以下に整理しました。

---
url: https://github.com/EvoMap/evolver
keywords: AIエージェント, 自己進化, GEPプロトコル, プロンプト生成, 監査ログ
oneliner: AIエージェントの挙動を「遺伝子＋プロトコル」で監査可能に進化させるGEPベースのプロンプト生成エンジン。
---

# Evolver（EvoMap/evolver）概要

## このリポジトリは何？

**AIエージェント向けの「自己進化エンジン」**。Node.js 18+ のCLIで動く単一リポジトリで、中心概念である **GEP (Genome Evolution Protocol)** に沿って「次にエージェントをどう進化させるか」を示すプロンプトを生成する。

- 入力: `memory/` 配下のランタイムログ・エラーパターン・過去履歴（signals）。
- 参照資産: `assets/gep/` に格納された **Gene / Capsule / EvolutionEvent**（＝再利用可能な進化の設計片、JSON/JSONL）。
- 出力: GEP制約に従う厳密なプロンプト文字列を stdout に出し、同時に `EvolutionEvent` を監査ログとして追記。
- あくまで **プロンプト生成器であり、ソースコードを直接書き換えない**。シェル実行も `solidify.js` の validation に限定され、`node/npm/npx` のみ・置換やパイプ禁止・180秒タイムアウトで守られる。
- オプションで **EvoMap Hub (evomap.ai)** に接続し、Skill Store のDL/共有、Worker Pool としてのタスク受託、ノード間の進化リーダーボード参加が可能（未設定でも完全オフライン動作）。

主要ディレクトリ: `src/evolve.js`（本体）、`src/gep/`（selector/prompt/solidify）、`src/ops/`（ライフサイクル・自己修復）、`scripts/`（取り込み・昇格・ログ抽出等）、`test/`（40以上のユニットテスト）。

## このリポジトリは何が嬉しいの？（既存手段との比較）

一般的な「プロンプト改善」の手段と比べた差別点。

| 観点 | 手動プロンプトチューニング | LangChain等の汎用フレームワーク | AutoGPT/自律エージェント | **Evolver** |
|---|---|---|---|---|
| 変更の再現性 | なし（勘と経験） | 個別実装に依存 | 自由記述で揺らぐ | **Gene/Capsuleで資産化** |
| 監査ログ | 手書きで残すしかない | 不定 | 実行ログのみ | **EvolutionEventで強制記録** |
| 安全性 | － | 任意のツール実行 | 任意コード実行しがち | **validation許可リスト＋rollback前提** |
| 戦略の切替 | 人が書き直す | 手動 | なし | `EVOLVE_STRATEGY=balanced/innovate/harden/repair-only` |
| ネットワーク資産 | なし | なし | なし | **Skill Store / Worker Poolで共有** |

要するに「**場当たりのプロンプト修正を、監査可能で再利用可能な"進化資産"に変える**」のが嬉しさ。stagnation検出やシグナル重複排除によるrepairループ防止、連続失敗時のGitHub Issue自動起票（機密情報をredactionしてから）など、長期運用向けの仕掛けが揃う。

## 使うときの流れ

1. **導入**: `git clone` → `cd evolver` → `npm install`（前提: Node.js ≥18 と **gitリポジトリ配下**。gitが無い場所ではエラー）。
2. **（任意）Hub接続**: `.env` に `A2A_HUB_URL` と `A2A_NODE_ID` を設定。オフライン運用ならスキップ。
3. **単発実行**: `node index.js` でログ走査→Gene選定→GEPプロンプトをstdoutへ出力し終了。
4. **レビュー運用**: `node index.js --review` で人間確認を挟む（本番投入時の推奨）。
5. **戦略指定**: 例 `EVOLVE_STRATEGY=harden node index.js --loop`（日常は `balanced`、新機能は `innovate`、緊急時は `repair-only`）。
6. **常駐化**: `node index.js --loop` か `node src/ops/lifecycle.js start|stop|status|check` でバックグラウンド運用（`pm2` なら `bash -lc 'node index.js --loop'` でラップ推奨）。
7. **ホスト連携**: OpenClaw等のホストランタイム配下で動かすと、出力中の `sessions_spawn(...)` が解釈され次アクションへ連鎖。単体ではただの文字列なので安全。
8. **資産の取り込み/公開**: `node index.js fetch --skill <id>` でSkill Store DL、`scripts/a2a_ingest.js` で外部資産をステージング→`scripts/a2a_promote.js --validated` で本採用（同IDのGeneは上書き不可）。
9. **出力の確認**: `assets/gep/events.jsonl`（監査トレイル）、`memory/` のログ、およびstdoutのGEPプロンプトをレビューし、コード反映は人間または上位ランタイムが行う。
