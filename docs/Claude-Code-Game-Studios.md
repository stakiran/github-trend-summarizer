---
url: https://github.com/Donchitos/Claude-Code-Game-Studios
keywords: Claude Code, ゲーム開発, AIエージェント, ワークフロー自動化, インディーゲーム
oneliner: Claude Codeを49体のAIエージェントが連携する仮想ゲーム開発スタジオに変えるテンプレートフレームワーク。
---

## Claude Code Game Studios とは

Claude Code のセッション上に、**実際のゲームスタジオの組織構造を再現する設定テンプレート**。49体の専門エージェント（クリエイティブディレクター、リードプログラマー、QAリードなど）と72個のスキル（スラッシュコマンド）を定義し、コンセプト立案からリリースまでのゲーム開発全工程をカバーする。ソースコード（ゲーム本体）は含まず、あくまで **Claude Code の振る舞いを制御する .claude/ ディレクトリ一式とドキュメント群** が本体。

### 構成要素

| 要素 | 数量 | 例 |
|---|---|---|
| エージェント定義 | 49体 | creative-director, gameplay-programmer, qa-tester 等 |
| スキル（/コマンド） | 72個 | `/brainstorm`, `/design-system`, `/dev-story`, `/launch-checklist` 等 |
| 自動フック | 12本 | コミット検証、セッション復旧、アセット命名チェック 等 |
| コーディングルール | 11件 | パス別に適用（gameplay→データ駆動必須、engine→ホットパス割当禁止 等） |
| ドキュメントテンプレート | 38種 | GDD、ADR、スプリント計画、QA計画、アートバイブル 等 |

エージェントは **3層の階層構造**（ディレクター → リード → スペシャリスト）で、Claude のモデルティアも使い分ける（Opus=高難度判断、Sonnet=通常作業、Haiku=ステータス確認）。

---

## 何が嬉しいのか ― 素のClaude Codeとの比較

| 観点 | 素の Claude Code | 本フレームワーク |
|---|---|---|
| **構造** | 1つの汎用チャット | 専門分化した49エージェントがロール別に応答 |
| **品質ゲート** | なし | フックがコミット時にハードコード値・GDD不備・JSON破損を自動検出 |
| **ドキュメント** | ユーザー任せ | GDDに8必須セクション、テンプレートで形式統一 |
| **スコープ管理** | なし | `/scope-check` でスコープクリープを検出、ピラー基準で優先度判定 |
| **セッション断絶** | コンテキスト消失 | `active.md` に状態保存、フックが自動復旧 |
| **協調モデル** | AI が自律生成 | **Question→Options→Decision→Draft→Approval** の5段階で常にユーザーが意思決定 |

最大の差別化は **「自律実行ではなく協調設計」** という原則。エージェントは必ず選択肢を提示し、ユーザーの承認なしにファイルを書かない。これにより、AIの生産性を活かしつつクリエイティブの主導権を手放さない設計になっている。

---

## 使うときの流れ ― 7フェーズパイプライン

```
Phase 1: Concept（構想）
  /start → /brainstorm → /setup-engine → /art-bible → /map-systems

Phase 2: Systems Design（設計）
  /design-system [システム名] → /design-review → /review-all-gdds

Phase 3: Technical（技術基盤）
  /create-architecture → /architecture-decision → /create-control-manifest

Phase 4: Pre-Production（準備）
  /create-epics → /create-stories → /sprint-plan

Phase 5: Production（実装） ← メインループ
  /story-readiness → /dev-story → /code-review → /story-done

Phase 6: Polish & QA（品質）
  /qa-plan → /smoke-check → /team-qa → /perf-profile → /tech-debt

Phase 7: Release（リリース）
  /launch-checklist → /changelog → /patch-notes
```

各フェーズは `/gate-check` で通過判定でき、成果物が揃っていなければ次に進めない。Phase 5 の実装ループでは、ストーリーファイルにGDD要件・ADR・受入基準が埋め込まれ、適切な専門プログラマーエージェントに自動ルーティングされる。

**初回セットアップ**: リポジトリをクローンし、Claude Code で開いて `/start` を実行するだけ。エンジン選択（Godot/Unity/Unreal）、ゲームコンセプト策定、命名規則設定までガイドされる。
