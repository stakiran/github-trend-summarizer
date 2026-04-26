---
url: https://github.com/trycua/cua
keywords: Computer-Use Agent, VM サンドボックス, macOS仮想化, LLM, デスクトップ自動化
oneliner: AI エージェントがデスクトップ (macOS/Linux/Windows/Android) を操作するためのオープンソース統合基盤（サンドボックス・SDK・ベンチマーク）。
---

## このリポジトリは何？

**Cua**（pronounced "coo-ah"）は、AI エージェントにコンピュータを操作させるための **オープンソース統合プラットフォーム**。「GUI を持つ一般的な PC 作業」をエージェントが自律的にこなすための、サンドボックス環境・SDK・ベンチマーク・ドライバを一式提供する。

### 主要コンポーネント

| コンポーネント | 役割 | 言語 |
|---|---|---|
| **Cua（サンドボックス SDK）** | Linux/macOS/Windows/Android VM を統一 API で制御 | Python |
| **cua-agent** | Claude・GPT-4o・Gemini など複数 LLM をバックエンドにしたエージェントフレームワーク | Python |
| **Cua Driver** | macOS ネイティブアプリをバックグラウンドで操作（カーソルを奪わない） | Swift |
| **CuaBot** | AI エージェント向け CLI サンドボックス（デスクトップにネイティブ表示） | TypeScript |
| **Lume** | Apple Silicon 上で macOS/Linux VM を Virtualization.Framework で高速起動 | Swift |
| **cua-bench** | OSWorld・ScreenSpot などのベンチマーク + RL 用軌跡エクスポート | Python |
| **cua-som** | YOLOv8 + EasyOCR による UI 要素検出ビジョンライブラリ | Python |

---

## 何が嬉しいの？既存の似た手段との比較

### 比較対象

| 観点 | **Cua** | Playwright / Selenium | OpenAI Computer Use API | Browser Use / Browserbase |
|---|---|---|---|---|
| 対象範囲 | OS 全体（デスクトップ GUI） | ブラウザのみ | OS 全体（クラウド完結） | ブラウザのみ |
| LLM の選択 | 何でも使える（liteLLM 経由） | 関係なし | OpenAI 固定 | 任意 |
| VM/サンドボックス | ローカル QEMU・クラウドの両方 | なし（実機 or CI） | 完全クラウド依存 | クラウド依存 |
| macOS ネイティブ操作 | ✅（Cua Driver / AX API） | ❌ | ❌ | ❌ |
| バックグラウンド動作 | ✅（フォーカスを奪わない） | △（ブラウザのみ） | ❌（VNC 相当） | ❌ |
| ベンチマーク | ✅（cua-bench） | なし | なし | なし |
| RL 学習データ生成 | ✅（軌跡記録・エクスポート） | なし | なし | なし |
| OSS / MIT | ✅ | ✅ | ❌ | 一部 |

### Cua ならではの強み

1. **OS を選ばない統一インタフェース** — `computer.screenshot()` / `computer.click(x, y)` という単一 API が macOS・Linux・Windows・Android に対応。
2. **バックグラウンド操作** — Cua Driver は画面フォーカスやカーソルを奪わず、ユーザーが作業しながらエージェントを並走させられる（既存製品にほぼない特性）。
3. **LLM 非依存** — liteLLM 抽象化で Claude / GPT-4o / Gemini / Qwen / ローカルモデルを差し替え可能。
4. **研究〜本番まで一気通貫** — ベンチマーク評価 → 軌跡収集 → RL 学習データ生成 → 本番デプロイを同一エコシステムで完結。
5. **Apple Silicon ネイティブ VM** — Lume が Virtualization.Framework を使うため、Rosetta 経由の QEMU より高速で起動もシンプル。

---

## 使うときの流れ

### ① サンドボックスを立ち上げる

```bash
# ローカル macOS 上で Linux VM を起動（Lume が必要）
curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh | bash
lume run macos-sequoia-vanilla:latest
```

```python
# Python SDK でサンドボックスに接続
from cua import Computer

async with Computer(os_type="linux") as computer:
    await computer.screenshot()          # スクリーンショット取得
    await computer.click(x=100, y=200)  # クリック
    await computer.type("Hello World")  # テキスト入力
```

### ② AI エージェントを動かす

```python
from cua import Computer
from cua_agent import ComputerAgent, LLM, LLMProvider

async with Computer() as computer:
    agent = ComputerAgent(
        computer=computer,
        llm=LLM(provider=LLMProvider.ANTHROPIC, model="claude-opus-4-5"),
    )
    async for result in agent.run("ブラウザを開いてニュースを検索して要約して"):
        print(result)
```

### ③ macOS ネイティブ操作（Cua Driver）

```bash
# バックグラウンドで macOS アプリを操作（MCP サーバーとして）
curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.sh | bash
cua-driver mcp  # MCP サーバー起動 → Claude Desktop や任意 LLM から呼び出せる
```

### ④ ベンチマーク評価

```bash
pip install cua-bench
cb run --suite osworld --agent claude-opus-4-5  # 標準ベンチマークを実行
cb export trajectories/                          # RL 学習用軌跡を書き出し
```

### 典型的なユースケース別の選択

| やりたいこと | 使うもの |
|---|---|
| ブラウザ自動化のみ | `cua-computer` + Docker プロバイダー |
| macOS アプリ操作（フォーカス不要） | `cua-driver` |
| 複数 OS で統一テスト | `cua-computer` + QEMU/クラウド |
| 研究・LLM 評価 | `cua-bench` |
| Claude Desktop / Cursor に統合 | `cua-mcp-server` |
| モバイル (iOS/Android) | `cuabot` の agent-device |
