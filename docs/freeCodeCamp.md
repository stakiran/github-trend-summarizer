---
url: https://github.com/freeCodeCamp/freeCodeCamp
keywords: プログラミング学習, 無料教育, カリキュラム, 認定証, オープンソース
oneliner: 数学・プログラミング・CS を無料で学べるオープンソースの学習プラットフォーム
---

## freeCodeCamp/freeCodeCamp

### これは何？

freeCodeCamp.org のオープンソースコードベースおよびカリキュラム一式。**Fastify (API) + Gatsby/React (クライアント) + MongoDB** のモノレポ構成で、ブラウザ上でコーディング課題を解きながらプログラミングを学べるプラットフォームを提供する。130 種類以上のチャレンジブロックと、以下の主要認定コースを含む。

| 認定カリキュラム (v9) | 内容 |
|---|---|
| Responsive Web Design | HTML/CSS/アクセシビリティ |
| JavaScript | アルゴリズム・データ構造 |
| Front-End Development Libraries | React・Redux 等 |
| Python | Python 基礎〜応用 |
| Relational Databases | SQL・PostgreSQL |
| Back-End Development and APIs | Node.js・Express |

加えて英語・スペイン語・中国語の語学コース (Beta) や、コーディング面接対策・Project Euler 等の補助教材もある。

### 何が嬉しいのか？（既存手段との比較）

| 観点 | freeCodeCamp | Udemy / Coursera 等 | The Odin Project |
|---|---|---|---|
| **費用** | 完全無料 | 有料コースが中心 | 無料 |
| **認定証** | 6 つの公式認定証を無料発行 | 有料修了証 | なし |
| **実践性** | ブラウザ内蔵エディタ (Monaco) で即コード実行・テスト | 動画中心、手を動かす機会が少ない | 外部環境を自前構築 |
| **カリキュラム網羅性** | フロント〜バック〜DB〜Python〜数学まで一貫 | 講座ごとにバラバラ | Web 開発特化 |
| **多言語対応** | 11 言語以上 (Crowdin 連携) | コースによる | 英語のみ |
| **コミュニティ** | フォーラム・ニュース・数百万人の学習者 | 講座単位のQ&A | Discord 中心 |

最大の強みは **「無料で体系的なカリキュラム → 実践課題 → 認定証取得」を一気通貫で提供**している点。有料サービスのペイウォールも、動画偏重の受動的学習もなく、コードを書いてテストをパスする能動的な学習体験が得られる。

### 使い方の流れ

#### 学習者として

```
1. https://freecodecamp.org にアクセスし、無料アカウントを作成
2. カリキュラムカタログから学びたい認定コースを選択
3. ブラウザ上のエディタで課題（チャレンジ）を順番に解く
   └─ テストが自動実行され、パスすれば次の課題へ進む
4. 各セクション末のプロジェクト課題を完成させる
5. すべてのプロジェクトを完了 → 認定証を取得・共有
```

#### 開発者 / コントリビューターとして

```
1. リポジトリを Fork & Clone
2. VS Code Dev Container で開く（Docker + MongoDB が自動起動）
   └─ pnpm install → MongoDB セットアップ → pnpm seed が自動実行
3. pnpm run develop で API (localhost:3000) + Client (localhost:8000) を起動
4. カリキュラム修正: curriculum/challenges/ 以下の Markdown/JSON を編集
   コード修正: client/ または api/ 配下の TypeScript を編集
5. pnpm run test / pnpm run lint で品質チェック
6. PR を作成 → CI (GitHub Actions: テスト・E2E・i18n検証) を通過後マージ
```
