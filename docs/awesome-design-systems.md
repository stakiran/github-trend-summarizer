---
url: https://github.com/alexpate/awesome-design-systems
keywords: awesome-list, design-systems, UI-library, curated-list, pattern-library
oneliner: 世界中の企業・組織が公開しているデザインシステムを一覧化し、機能の有無をひと目で比較できるキュレーションリスト。
---

## awesome-design-systems

### これは何？

GitHub の「Awesome リスト」形式で、**世界中のデザインシステム 187 件以上**をアルファベット順に収録したキュレーションリポジトリ。リポジトリ自体は `README.md`・`LICENSE`・カバー画像の 3 ファイルのみで構成される、ビルド不要の純粋な Markdown プロジェクトである。

各デザインシステムについて、以下の 4 つの観点を ✅ の有無で一覧比較できる。

| 観点 | 内容 |
|---|---|
| **Components** | コード化された UI コンポーネント集があるか |
| **Voice & Tone** | 言語・トーンのガイドラインがあるか |
| **Designers Kit** | Figma / Sketch 等のデザイナー向けアセットがあるか |
| **Source Code** | ソースコードが公開されているか（GitHub 等へのリンク付き） |

収録対象は Adobe Spectrum、Google Material Design、Shopify Polaris、IBM Carbon、GOV.UK など、大企業から政府機関まで幅広い。

---

### 何が嬉しいのか？（既存手段との比較）

| 比較対象 | 課題 | awesome-design-systems の優位性 |
|---|---|---|
| **Google 検索** | 検索のたびにノイズが多く、網羅的な比較が困難 | 一覧表で **187 件を俯瞰**でき、機能軸でフィルタ的に眺められる |
| **個別ブログ記事**（「おすすめデザインシステム 10 選」等） | 執筆時点で固定され、陳腐化しやすい | コミュニティの PR で**継続的に更新**される（Unlicense で誰でも貢献可） |
| **designsystemsrepo.com 等の専用サイト** | リッチだが更新頻度やメンテナ依存が大きい | GitHub の仕組み（Star・PR・Issue）に乗るため**発見性・透明性が高い** |
| **自分でスプレッドシートを作る** | 調査コストが膨大 | 既に分類・リンク済みの表をそのまま使える |

つまり、**「デザインシステムを選定・調査したい」という場面で、最も低コストに全体像を掴める出発点**として機能する。

---

### 使うときの流れ

```
1. リポジトリにアクセス
   └─ GitHub 上の README がそのまま閲覧画面になる

2. 一覧テーブルを眺める
   └─ 「Components ✅ かつ Source Code ✅」など、
      自分の要件に合うデザインシステムを絞り込む

3. 気になるデザインシステムのリンクを開く
   └─ 公式ドキュメントや GitHub リポジトリに直接遷移

4. （任意）足りない情報があれば貢献する
   └─ README.md のテーブルにアルファベット順で行を追加し、
      Pull Request を送るだけ（CONTRIBUTING.md 等は無く、敷居が低い）
```

ビルド手順やインストールは一切不要。ブラウザで README を開くだけで完結する、**読むためのリポジトリ**である。
