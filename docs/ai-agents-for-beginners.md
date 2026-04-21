---
url: https://github.com/microsoft/ai-agents-for-beginners
keywords: AI Agents, Microsoft Agent Framework, Azure AI Foundry, Tutorial, Jupyter Notebook
oneliner: AIエージェント開発の基礎を12レッスン以上のハンズオン教材で学べる、Microsoft公式の初心者向けコース。
---

# microsoft/ai-agents-for-beginners

## このリポジトリは何？

Microsoft公式が提供する「AIエージェントを作り始めるための初心者向けコース教材」。当初は12レッスン構成だったが、現在は **16レッスン（+3つがComing Soon）** まで拡充されている大規模教材リポジトリで、主要コンテンツは Jupyter Notebook。

- **対象**: これからAIエージェントを学び始める人。GenAIの前提があると望ましい（未経験者には姉妹コース `Generative AI for Beginners` を推奨）。
- **中身**: 各レッスンごとに `README.md`（解説）+ `code_samples/`（`*-python-agent-framework.ipynb` と `*-dotnet-agent-framework.cs`）+ YouTube動画リンク+追加学習リンク。
- **扱うトピック**: イントロ → エージェントフレームワーク探訪 → 設計パターン（Tool Use / Agentic RAG / Planning / Multi-Agent / Metacognition）→ Trustworthy / 本番運用 → MCP・A2A・NLWebなどの **Agentic Protocol** → Context Engineering → Agent Memory → Microsoft Agent Framework → Browser/Computer Use Agent、までを網羅。
- **実装基盤**: **Microsoft Agent Framework (MAF)** + **Azure AI Foundry Agent Service V2 (Responses API)**。認証は `AzureCliCredential`（APIキー不要のkeyless）。一部レッスンは GitHub Models / Azure AI Search / Bing Grounding / MiniMax (OpenAI互換) もサポート。
- **多言語**: Co-op Translatorで50以上の言語に自動翻訳済み（日本語含む）。ただしフルクローンだと~3GB超えるため sparse-checkout 推奨。

## このリポジトリは何が嬉しい？（類似手段との比較）

| 比較対象 | このリポジトリの優位点 |
|---|---|
| LangChainなどの**公式ドキュメント**を読む | ドキュメントは網羅的すぎて学習順序が不明瞭。本コースは **「レッスン単位で段階的に学ぶ」カリキュラム化** されている。 |
| 個人ブログ/Qiita記事の断片的チュートリアル | **Microsoft公式**で品質・保守が担保され、動画+コード+文章が揃う。PR/Issueで継続更新。 |
| 他の `*-for-beginners` シリーズ（ML/AI for Beginners等） | 本リポは「エージェント」という最新トピックに特化。**MCP・A2A・Context Engineering・Agent Memory** など2025年の最前線概念まで追従。 |
| LangChain/LlamaIndexでエージェントを自作する | **Azure AI Foundry + Microsoft Agent Framework** を前提にしているので、クラウドスケーリング・keyless認証・エンタープライズ運用まで見据えた構成を最初から学べる。 |
| Microsoft純正のサンプルリポジトリ単品 | 単体のSDKサンプル集と違い、「**設計パターンの理論 → コード演習 → 本番化**」まで横断する体系教材。 |

要するに「**公式・体系的・最新トピック網羅・Azureで動かせる**」の4点セットが強み。

## 使うときの流れ

1. **準備**
   - `git clone --filter=blob:none --sparse` + `git sparse-checkout` で翻訳を除外してクローン（容量節約）。
   - Python 3.12+ の venv を作り `pip install -r requirements.txt`。.NETサンプルを使うなら .NET 10 SDK も。
2. **Azure側セットアップ** (`00-course-setup/README.md`)
   - ai.azure.com で Foundry Hub → Project → モデルデプロイ（例: `gpt-4o`）。
   - `az login`（Codespacesなら `--use-device-code`）でサインイン。
   - `.env.example` を `.env` にコピーし、`AZURE_AI_PROJECT_ENDPOINT` と `AZURE_AI_MODEL_DEPLOYMENT_NAME` を記入。
   - レッスン5 (RAG) なら Azure AI Search、レッスン6/8なら GitHub Models、レッスン8のBingなら `BING_CONNECTION_ID` を追加。
3. **学習ループ** — レッスン01〜15を好きな順で：
   - `README.md` を読む → 該当動画を視聴 → `code_samples/*-python-agent-framework.ipynb` をVSCode/Jupyterで実行 → 追加リンクで深掘り。
   - 独立したレッスン構成なので興味あるパターン（例: 04 Tool Use、08 Multi-Agent、11 MCP/A2A）から入ってもOK。
4. **詰まったら**
   - Microsoft Foundry Discord / GitHub Issuesで質問、または `STUDY_GUIDE.md` を参照。
5. **応用**
   - 学習後は `14-microsoft-agent-framework`（MAF本体の深掘り）や `15-browser-use`（CUA）、姉妹コース `mcp-for-beginners` などへ展開。
