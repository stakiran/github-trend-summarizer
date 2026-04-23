---
url: https://github.com/chiphuyen/aie-book
keywords: AI Engineering, 書籍補助資料, 基盤モデル, LLM, リソース集
oneliner: Chip Huyen著『AI Engineering』(O'Reilly, 2025) の補助資料と、AIエンジニア向け学習リソースを集約した公式リポジトリ。
---

# chiphuyen/aie-book の整理

## このリポジトリは何？

Chip Huyen 氏が執筆した書籍 **『AI Engineering: Building Applications with Foundation Models』（O'Reilly, 2025）** の **公式サポートリポジトリ** 兼、**AI エンジニアリング領域の学習リソース集** です。書籍そのもののソースコードではなく、書籍を補完するテキスト資料・リンク集が中心で、主要言語は Jupyter Notebook となっていますが実態は Markdown が大半を占めます。

主なコンテンツ:

- **`ToC.md` / `ToC.pdf`**: 全10章の詳細な目次（基盤モデル、評価、プロンプトエンジニアリング、RAG と Agent、Finetuning、Dataset Engineering、推論最適化、アーキテクチャなど）
- **`chapter-summaries.md`**: 各章の要約（書籍本体からの抜粋）
- **`resources.md`**: 1200以上の参照リンクから厳選した、章別の推奨リソース（論文・ブログ・ツール・ベンチマーク）
- **`prompt-examples.md`**: Brex / Cursor / Pinterest / Grab などの実プロダクトで使われた実プロンプト集
- **`case-studies.md` / `misalignment.md` / `appendix.md`**: 事例と補遺（一部は執筆中のプレースホルダー）
- **`study-notes.md`**: 読者コミュニティの読書会・要約ブログへのポインタ
- **`scripts/ai-heatmap.ipynb`**: ChatGPT / Claude の会話ログを GitHub 草風のヒートマップ化するおまけツール
- **`assets/`**: 書籍内の図版（AI スタック進化、RAG アーキ、RLHF など）

なお「tools become outdated quickly, but fundamentals should last longer」という著者の方針で、チュートリアル本ではなく「フレームワーク」「判断軸」の提示を重視しています。

## 既存の類似手段との比較で、何が嬉しいのか

同種のリソースとしては、個人のブログ記事、`awesome-llm` 系リンク集、各ベンダー（OpenAI / Anthropic / LangChain）のドキュメント、あるいは他の LLM 入門書籍（Sebastian Raschka『Build a LLM from Scratch』等）があります。これらとの差別化ポイント:

- **書籍と連動した体系性**: Awesome リストは網羅的だが玉石混交で取捨選択が難しい。本リポは **「著者が書籍執筆中に実際に読んだ1200件超の中から精選した」** リソース群で、章立て（Evaluation → Prompt → RAG/Agent → Finetuning → Inference Optimization → Architecture）に沿って整理されているため、知識の地図が得られる。
- **ツール非依存の普遍性**: LangChain 公式ドキュメントや各 SaaS のガイドは特定ツールに紐づく。本書・本リポは「いつ RAG を選ぶか」「いつ Finetuning するか」「どうハルシネーションを検知するか」といった **意思決定の観点** を扱うため、ツールが陳腐化しても使える。
- **実プロダクトの一次ソース**: 一般的なプロンプトエンジニアリング記事は教科書的な例が多いが、本リポは Brex・Cursor・Pinterest・Whatnot 等が **本番で使っている実プロンプト** を掲載。
- **前著 DMLS との接続**: 同著者の『Designing Machine Learning Systems』は従来 ML を扱い、本書は基盤モデル時代を扱う、という **MLOps → AI エンジニアリング** の橋渡し構造になっている。

## 使うときの流れ

想定読者は AI エンジニア、ML エンジニア、データサイエンティスト、技プロマネなど。

1. **入口選定**: `README.md` から自分の興味にあたる章を決める（アプリ設計なら1章、評価で困っていれば3・4章、RAG/Agent なら6章）。
2. **概観の把握**: `ToC.md` で詳細目次、`chapter-summaries.md` で各章のサマリを読む。書籍を買う前の意思決定、または読んだ後の復習に使える。
3. **深掘り**: `resources.md` の該当章セクションから外部論文・ブログを辿る。書籍の内容を裏付ける一次資料にアクセスできる。
4. **実装の参考**: `prompt-examples.md` で実企業のプロンプト構造を模倣し、自分のユースケースに応用する。
5. **コミュニティ学習**: `study-notes.md` から他読者のサマリや読書会に参加して理解を深める。
6. **（任意）書籍本体の購入**: Amazon / O'Reilly へのリンクから購入し、リポジトリを副読本として併用。
7. **貢献**: 有用な追加リソース・プロンプト・読書ノートは PR で投稿可能（WIP 状態の領域が多く、継続的に拡張されている）。

要するに、**書籍の「索引・参考文献・付録」をオープンに公開し続けているリビングドキュメント** として使うのが本リポの基本的な活用形です。
