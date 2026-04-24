---
url: https://github.com/codecrafters-io/build-your-own-x
keywords: tutorial-collection, learn-by-building, awesome-list, from-scratch, programming-education
oneliner: 有名な技術（OS・DB・Git・ブラウザ等）を自作するチュートリアル記事を分野別に集めた巨大なリンク集リポジトリ。
---

# build-your-own-x 整理

## このリポジトリは何？

`codecrafters-io/build-your-own-x` は、**「自分の好きな技術をゼロから作り直す」ステップバイステップ型チュートリアルを分野別にまとめた巨大キュレーション型 README** である。実装コードは含まず、リポジトリ本体は実質 1 ファイル（`README.md`、約 46KB・500 行超）＋ `ISSUE_TEMPLATE.md` のみ。ライセンスは CC0（パブリックドメイン）。元は Daniel Stefanovic 氏が開始し、現在は CodeCrafters, Inc. が保守。

扱う「x」のカテゴリは 30 近くあり、網羅範囲は広い:

- **システム低レイヤ系**: OS / Shell / Docker / Emulator・VM / Processor / Memory Allocator / Network Stack
- **データ・言語系**: Database / Programming Language / Regex Engine / Template Engine / Search Engine
- **Web/アプリ系**: Web Browser / Web Server / Front-end Framework (React・Redux・Angular 等) / Bot / CLI Tool / Git / Text Editor
- **AI・グラフィクス系**: AI Model (LLM・Diffusion・RAG) / Neural Network / 3D Renderer / Voxel Engine / Physics Engine / AR / Visual Recognition
- **その他**: BitTorrent / Blockchain / Game / Uncategorized（DNS・Load Balancer・Module Bundler 等）

各エントリは `**言語**: _タイトル_` のリンク形式で統一されており、C / C++ / Rust / Go / Python / JavaScript / TypeScript / Ruby / Haskell / Nim / Zig など多様な言語をカバー。動画系には `[video]` の注記が付く。

## このリポジトリは何が嬉しい？既存手段との比較

学習リソースを見つける選択肢は他にもあるが、本リポジトリは以下の点で差別化される。

| 比較対象 | 特徴 | build-your-own-x との差 |
| --- | --- | --- |
| **各種 Awesome リスト** (awesome-python 等) | ライブラリ・ツールのリンク集 | awesome 系は「使う側」中心。こちらは「作る側」＝実装チュートリアル限定 |
| **freeCodeCamp / Udemy 等** | 講座プラットフォーム。体系的だが課金 or 偏り | 無料・多言語・分野横断。一か所で比較検討できる |
| **dev.to / Medium 個別記事** | 良記事は多いが分散 | 分野×言語の 2 軸で集約され、単一 README で一覧性が高い |
| **CodeCrafters 本家サービス** | 有料の採点付き実装演習 | こちらは純粋に無料リンク集。採点なしで自由に進められる |

つまり「**Feynman 的な "作れないものは理解していない" 精神で、既存技術の中身を自分で再実装するための入口カタログ**」として、選別基準（単なるフレームワーク紹介や外部ライブラリの糊付けは採用しない、という `ISSUE_TEMPLATE.md` のポリシー）を伴った質の高いエントリが揃っていることが最大の価値。スター数も GitHub 上位クラスで、その信頼性と鮮度も強み。

## 使うときの流れ

1. **学びたい領域を選ぶ** — README 冒頭の目次から `Database` `Operating System` `Git` などカテゴリへ飛ぶ。
2. **言語でフィルタ**する — 各エントリは `**言語名**:` プレフィクスで始まるので、手になじむ言語（または学びたい言語）を目視で絞り込む。分量・記事 or 動画の種別（`[video]` 注記）も確認。
3. **リンク先のチュートリアルを進める** — 本リポジトリはあくまでインデックス。実装と解説は外部サイト側にあるので、そちらで手を動かす。
4. **（任意）自分の手元でリポジトリを作って写経** — `git clone` で README を取得する必要はほぼなく、ブラウザで README を開くだけで十分。実装物は各自のリポジトリに作る。
5. **良い記事を見つけたら貢献する** — `ISSUE_TEMPLATE.md` に従って「言語 / タイトル / URL / カテゴリ」を埋めた Issue か PR を送る。受理基準は「ゼロから何かを作る step-by-step チュートリアルであること」「フレームワーク紹介や既製ライブラリを繋ぐだけのものは不可」。

用途としては、①特定技術の内部理解を深めたいエンジニアの学習ロードマップ作り、②新しい言語を習得する際のお題探し、③勉強会・ブートキャンプの題材ソース、として使うのが典型。
