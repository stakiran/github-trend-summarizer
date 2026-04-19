---
url: https://github.com/Fincept-Corporation/FinceptTerminal
keywords: Finance, Bloomberg alternative, Qt6, C++20, Python, Trading, Portfolio, AI Agents, Market Data, CFA
oneliner: Bloombergターミナル級の分析性能を目指す、C++20/Qt6ネイティブ＋埋め込みPythonで構築されたオープンソースの統合金融インテリジェンス・デスクトップアプリ。
---

# Fincept Terminal 要約

## このリポジトリは何？

**Fincept Terminal v4** は、Fincept Corporation が開発するオープンソースの統合金融分析デスクトップアプリケーション（AGPL-3.0 / 商用デュアルライセンス）。

- **技術スタック**：純ネイティブ C++20 + **Qt6 (6.8.3)** UI、分析ロジックに **Python 3.11 埋め込み**、ビルドは CMake + Ninja。単一ネイティブバイナリで配布。
- **対応OS**：Windows x64 / Linux x64 / macOS Apple Silicon（インストーラ、Docker、ソースビルドを提供）。
- **規模感**：`fincept-qt/src` 配下に `ai_chat` `auth` `core` `datahub` `mcp` `network` `python` `screens` `services` `storage` `trading` `ui` など多数のモジュール。
- **主な機能群**
  - CFA カリキュラム級アナリティクス（DCF、ポートフォリオ最適化、VaR/Sharpe、デリバティブ価格計算）
  - **37体のAIエージェント**（Buffett / Graham / Lynch / Munger 等の投資家フレーム、経済・地政学系）と、OpenAI/Anthropic/Gemini/Groq/DeepSeek/Ollama などマルチプロバイダ対応 + ローカル LLM
  - **100+ データコネクタ**（Yahoo Finance、FRED、IMF、World Bank、DBnomics、Polygon、Kraken、AkShare、各国政府 API、Adanos 市場センチメント 等）
  - リアルタイムトレーディング（Kraken/HyperLiquid WebSocket）、**16ブローカー統合**（Zerodha、Angel One、IBKR、Alpaca、Tradier、Saxo 等）、ペーパートレード
  - QuantLib 18モジュール（価格設定・リスク・確率過程・ボラ・債券）、ML/強化学習/HFT 用 AI Quant Lab
  - 海事追跡・地政学・衛星データ、ノードエディタによる視覚的ワークフロー、MCP ツール連携

## 既存手段との比較 — 何が嬉しい？

| 比較対象 | Fincept が解く課題 |
|---|---|
| **Bloomberg / Refinitiv 等の商用ターミナル** | 数千ドル/月級の高コストと閉じたデータに対し、**AGPL-3.0 で無料**、個人・教育・非商用なら自由に使える。100+ のオープン/公的データ源を同梱し「データは制約じゃない」を掲げる。 |
| **Electron ベースの OSS 金融アプリ（OpenBB 等）** | Web ランタイム（Node.js / ブラウザ）を排し **C++20 + Qt6 ネイティブ**。単一バイナリで起動が速く、メモリ消費が軽く、チャート描画も GPU 寄り。 |
| **Python 単体スクリプト / Jupyter** | Python の分析資産（QuantLib、各種モデル）を埋め込みつつ、UI・リアルタイム配信・ブローカー接続・認証・テーマといった "アプリ層" を Qt で一気通貫に提供。 |
| **国別ブローカー個別アプリ** | インド系（Zerodha/Angel One/Upstox 他）から米国（IBKR/Alpaca）、欧州（Saxo）、暗号資産（Kraken/HyperLiquid）まで1つのターミナルで横断。 |
| **AI コパイロット単体** | 37の投資哲学ペルソナ／地政学エージェントを分析画面と直結し、単なるチャットではなく "エージェント駆動の自動調査" に統合。 |

端的に言えば、**「Bloomberg級の分析深度 × OpenBB級のオープン性 × ネイティブアプリの軽快さ」** を 1 バイナリで同時に満たすことが差別化点。

## 使うときの流れ

1. **入手**
   - 一番簡単：[Releases](https://github.com/Fincept-Corporation/FinceptTerminal/releases) から OS 別インストーラ（v4.0.2：Windows `.exe` / Linux `.run` / macOS `.dmg`）を DL。
   - ソースから：`git clone` → `setup.sh`（Linux/macOS）か `setup.bat`（Windows VS 2022 Dev Cmd）でコンパイラ・CMake・Qt6・Python 依存を一括セットアップ＆ビルド。
   - 手動ビルド：Qt 6.8.3、CMake 3.27.7、Ninja 1.11.1、Python 3.11.9 を入れて `cmake --preset <os>-release && cmake --build --preset <os>-release`。
   - Docker：`ghcr.io/fincept-corporation/fincept-terminal:latest`（主に Linux + X11 前提）。

2. **初回起動・認証**：PIN 認証／テーマ選択を経てダッシュボードへ。

3. **データ接続設定**：「Data Sources」でコネクタを選び API キー登録（FRED、Polygon、Kraken、ブローカー、Adanos 代替データ 等）。未設定のコネクタはドーマント。

4. **日常利用**：
   - **Equity Research / Portfolio / News** 画面でリサーチ・保有管理・ニュース＋センチメント横断閲覧
   - **Trading** で実取引・ペーパートレード（16ブローカー）
   - **AI Agents / AI Chat** に銘柄やマクロ質問を投げて投資家ペルソナ別の意見を取得
   - **Node Editor** で「データ取得→加工→エージェント評価→発注/通知」をビジュアル自動化
   - **QuantLib / AI Quant Lab** で価格モデル・ファクター発見・ML/RL 実験

5. **拡張・貢献**：新データコネクタ、AI エージェント、C++ スクリーン、Python 分析モジュールを `docs/CONTRIBUTING.md` と Python/C++ 別のコントリビュータガイドに沿って追加。大学・機関向けには月額 $799/20 アカウントの教育ライセンスあり。
