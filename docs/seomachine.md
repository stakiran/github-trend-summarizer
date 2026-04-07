---
url: https://github.com/TheCraigHewitt/seomachine
keywords: Claude Code, SEO, コンテンツ作成, ブログ最適化, WordPress
oneliner: Claude Codeのカスタムコマンド・エージェント・Python分析を組み合わせ、SEO最適化されたブログ記事のリサーチから公開までを一気通貫で行うワークスペース。
---

## SEO Machine とは

**Claude Code 上に構築された、SEOブログ記事の制作ワークスペース**。22個のスラッシュコマンド、11個の専門エージェント、24個のPython分析モジュールを組み合わせ、キーワード調査→執筆→最適化→WordPress公開までのパイプラインを提供する。コードそのものではなく「Claude Codeの設定・プロンプト・分析スクリプトの集合体」である点が特徴的。

## 何が嬉しいのか？（既存手段との比較）

| 観点 | 従来の手段（SurferSEO / Jasper 等） | SEO Machine |
|---|---|---|
| **統合度** | リサーチ・執筆・分析・公開が別ツール | 1つのClaude Codeセッション内で完結 |
| **カスタマイズ性** | SaaS側の設定範囲に限定 | `context/` にブランドボイス・SEOガイドライン等をMarkdownで自由定義。コマンドやエージェントもテキストファイルなので改変が容易 |
| **分析の深さ** | ツール固有のスコアリング | Python製の分析パイプライン（読みやすさ・キーワード密度・SERP競合比較・検索意図分類・SEOスコア 0-100）をローカルで実行。GA4/GSC/DataForSEO連携でデータドリブンな優先度付けも可能 |
| **コスト構造** | 月額$50〜$200+のSaaS課金 | OSSなのでClaude API利用料+外部API料金のみ |
| **公開フロー** | コピペや外部連携が必要 | WordPress REST API＋Yoast SEOメタデータ付きで直接公開 |

要するに **「SEOコンテンツ制作に必要な知識・ワークフロー・ツール連携を、Claude Codeのカスタムコマンドとしてパッケージ化した」** ことが最大の価値。個別の専門知識がなくても、コマンド一発で専門家レベルの分析・最適化が走る。

## 使い方の流れ

```
1. 初期設定
   context/ 配下のテンプレートを自社向けに編集
   （brand-voice.md, seo-guidelines.md, target-keywords.md 等）
   必要に応じて GA4/GSC/DataForSEO/WordPress の API キーを .env に設定

2. リサーチ（topics/ → research/）
   /research [トピック]     … キーワード調査＋競合分析 → リサーチブリーフ生成
   /research-gaps           … 競合とのコンテンツギャップ発見
   /research-trending       … トレンドトピック探索
   /cluster [トピック]      … ピラー＋サポート記事のクラスター設計

3. 執筆（research/ → drafts/）
   /write [トピック]        … 2000-3000語の記事を生成
   　→ 自動で4つのエージェントが順次実行：
   　  SEO Optimizer / Meta Creator / Internal Linker / Keyword Mapper

4. 品質チェック・最適化
   /analyze-existing [ファイル] … SEOスコア・読みやすさ等を数値評価
   /optimize [ファイル]         … 最終SEO仕上げ
   /scrub [ファイル]            … AI臭い表現の除去

5. 公開（drafts/ → published/）
   /publish-draft [ファイル]    … WordPress に Yoast メタデータ付きで投稿

6. 運用・改善
   /performance-review          … GA4/GSCデータから改善優先度を自動算出
   /rewrite [トピック]          … 既存記事のリライト
   /priorities                  … コンテンツ優先度マトリクス
```

ポイントは **「コマンドを叩くだけで、裏側のエージェント群とPython分析が自動連鎖する」** 設計。ユーザーはトピックを与えるだけで、SEOの専門的な最適化プロセスが一通り回る。
