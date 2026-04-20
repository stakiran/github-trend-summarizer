---
url: https://github.com/koala73/worldmonitor
keywords: geopolitical intelligence, real-time dashboard, news aggregation, globe visualization, TypeScript
oneliner: 500以上のニュースフィードと30以上の外部データソースをAIで横断的に集約・相関分析し、3D地球儀/平面マップ上にリアルタイムで可視化する「グローバル状況認識ダッシュボード」。
---

# koala73/worldmonitor 概要

## このリポジトリは何？

**World Monitor** は、地政学・軍事・金融・エネルギー・災害・サイバー・航空・海運などの情報を1枚の画面に束ねる「リアルタイム世界監視ダッシュボード」の SPA（TypeScript 製）+ デスクトップアプリ（Tauri 2）のモノレポ。

主な構成:
- **フロント**: Vanilla TypeScript + Vite。`globe.gl`（Three.js ベース 3D 地球儀）と `deck.gl` + MapLibre GL（WebGL 平面地図）のデュアルマップ、86 クラス以上の Panel コンポーネント。
- **API 層**: Vercel Edge Functions 60+（`api/` 配下、自己完結 JS）、Railway 上の AIS WebSocket リレー、Upstash Redis の 3 段キャッシュ、Convex（問い合わせ/waitlist）。
- **AI/ML**: Ollama / Groq / OpenRouter でのサーバサイド要約と、`@xenova/transformers`（ONNX, MiniLM など）を Web Worker で走らせるブラウザ内推論（埋め込み、感情、要約、NER、ベクトル検索）。
- **データ**: 500+ 厳選 RSS、ACLED・UCDP・GDELT・FIRMS・OpenSky・Finnhub・FRED・CoinGecko 等 30〜65+ の外部ソース。Wingbits による ADS-B フライトデータ供給。
- **バリアント**: 単一コードベースから `world / tech / finance / commodity / happy` の 5 サイトを生成（ホスト名や `VITE_VARIANT` で切替）。21 言語・RTL 対応。
- **配布形態**: Web（`worldmonitor.app`）、Tauri 2 デスクトップ（macOS arm64/x64, Windows, Linux AppImage, Node.js サイドカー同梱）、Docker（GHCR マルチアーチ）、PWA。
- **ライセンス**: AGPL-3.0（非商用）/ 商用は別途ライセンス。Copyright © 2024–2026 Elie Habib。

## このリポジトリは何が嬉しい？（既存手段との比較）

| 比較対象 | World Monitor の優位点 |
|---|---|
| **Bloomberg Terminal / Refinitiv** | 金融だけでなく軍事・災害・サイバー・航空まで**クロスドメイン相関**（escalation signal convergence）を行う。無償で自己ホスト可能。 |
| **Flightradar24 / MarineTraffic / ACLED 個別サイト** | AIS・ADS-B・紛争・気象・為替・ニュースを**1つの地球儀/マップに 45 レイヤ**として統合。横断 API を叩き分ける必要がない。 |
| **Google News / Feedly などのニュースアグリゲータ** | 500 フィードを **AI が要約・ジャンル横断でクラスタリング**し、**Country Intelligence Index（12 カテゴリのコンポジットリスクスコア）**まで付与。 |
| **一般的な OSS ダッシュボード（Grafana 等）** | 最初から地政学インテリジェンス用にチューニングされた **Panel / Map / AI 要約** が揃っており、自前でパイプラインを組む必要なし。Tauri 版でローカル常駐も可能。 |
| **SaaS 型 OSINT ツール** | **Ollama によるローカル AI** で API キー不要運用が可能、Edge Functions + Upstash で低レイテンシ、AGPL で透明性あり。 |

要するに「**1画面で世界を把握する**」を既製品に頼らずセルフホスト可能な形で実装しており、無料〜API 無しでも動かせる点が独自性。

## 使うときの流れ

1. **素早く試す（Web / ローカル開発）**
   ```bash
   git clone https://github.com/koala73/worldmonitor.git
   cd worldmonitor && npm install && npm run dev
   # → http://localhost:5173  （環境変数なしで基本動作）
   ```
   バリアントを切り替えるなら `npm run dev:tech` / `dev:finance` / `dev:commodity` / `dev:happy`。

2. **設定（必要に応じて）** `.env.example` を `.env` にコピーし、Finnhub・Groq・Ollama・Upstash・Sentry など使いたい外部サービスのキーを埋める（未設定でも多くのパネルは graceful degradation）。

3. **ブラウザでの使い方**
   - 3D グローブ / 平面マップをトグルし、**45 レイヤ**（紛争、AIS、フライト、地震、サイバー、市場、コモディティ…）をオンオフ。
   - 右側の Panel グリッドで AI 要約ブリーフ、Country Intelligence Index、Finance Radar、Cross-stream Correlation を確認。Panel はドラッグでリサイズし localStorage に保存。
   - URL に状態が双方向同期されるので、注目のビューは URL 共有で再現可能。

4. **デスクトップアプリ**（常駐用途）
   `worldmonitor.app/api/download?platform=…` から .exe / .dmg / .AppImage を入手、または `npm run desktop:dev` / `desktop:build:full`。Node.js サイドカーが同梱され、ローカル API として動作。

5. **セルフホスト / 本番デプロイ**
   - Vercel: `vercel.json` 済み、Edge Functions そのまま。
   - Docker: `docker-compose.yml` または GHCR の nginx イメージ。
   - Railway: `scripts/ais-relay.cjs` を AIS リレー + シードループとして常駐。
   - 詳細は `SELF_HOSTING.md` と `DEPLOYMENT-PLAN.md`。

6. **開発への貢献** `npm run typecheck` / `npm run build:full` / `npm run test:data` / Playwright E2E / `npm run lint` を通し、`CONTRIBUTING.md` と `AGENTS.md` のガイドに従って PR。API 層は `api/` 配下のみ、`src/` や `server/` から import しない等、境界ルールが lint で強制されている。
