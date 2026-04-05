---
url: https://github.com/google-ai-edge/LiteRT-LM
keywords: on-device LLM, edge inference, LiteRT, Gemma, mobile AI
oneliner: Google製のエッジデバイス向け高性能LLM推論フレームワーク
---

## LiteRT-LM — エッジデバイス向けLLM推論エンジン

### これは何？

Google が開発した、**スマートフォン・PC・IoT などのエッジデバイス上で LLM を動かすための推論フレームワーク**。Chrome、Chromebook Plus、Pixel Watch など Google の実製品で使われている実績がある。Gemma、Llama、Phi-4、Qwen など主要モデルに対応し、テキストだけでなく画像・音声のマルチモーダル入力や、Function Calling（ツール呼び出し）もサポートする。C++ / Python / Kotlin の API を提供し、Android・iOS・Web・デスクトップをカバーする。

### 何が嬉しいのか？（既存手段との比較）

| 観点 | LiteRT-LM | llama.cpp | MLC-LLM |
|---|---|---|---|
| **出自・実績** | Google 製品で実運用済み | コミュニティ主導 | 研究寄り |
| **バックエンド** | CPU / GPU / **NPU** を統一 API で切替 | CPU 中心（GPU は限定的） | GPU 中心（Vulkan 等） |
| **マルチモーダル** | Vision・Audio を一級サポート | テキスト中心 | テキスト中心 |
| **Function Calling** | 組込みサポート（ANTLR パーサ + 制約付きデコード） | なし（自前実装が必要） | なし |
| **制約付き生成** | 正規表現・JSON Schema・文脈自由文法で出力を強制 | 部分的 | なし |
| **モバイル統合** | Kotlin/Android・Swift/iOS 向け SDK あり | JNI 等で自前ラップが必要 | Android 対応はあるが薄い |
| **投機的デコード** | MTP（Multi-Token Prediction）内蔵 | 一部対応 | なし |

**要するに**、エッジ上で LLM を「製品レベル」で使いたいときに、バックエンド選択・マルチモーダル・ツール呼び出し・出力制約といった実用機能がワンパッケージで揃っている点が最大の強み。

### 使い方の流れ

```
① モデル準備 → ② エンジン作成 → ③ 会話 → ④ レスポンス取得
```

**① モデルを用意する** — HuggingFace から `.litertlm` 形式のモデルをダウンロード、または変換する。

**② エンジンを作成する** — モデルパスとバックエンド（CPU/GPU/NPU）を指定して初期化。

**③ 会話セッションを開く** — `Conversation` を作成し、必要に応じてシステムプロンプトやツール定義を渡す。

**④ メッセージを送りレスポンスを得る** — `send_message()`（ブロッキング）または `send_message_async()`（ストリーミング）で推論を実行。

Python での最小例:

```python
import litert_lm

with litert_lm.Engine("model.litertlm") as engine:
    with engine.create_conversation() as conv:
        reply = conv.send_message("東京タワーの高さは？")
        print(reply["content"][0]["text"])
```

CLI でさらに手軽に試すことも可能:

```bash
uv tool install litert-lm
litert-lm run \
  --from-huggingface-repo=google/gemma-3n-E2B-it-litert-lm \
  gemma-3n-E2B-it-int4 \
  --prompt="Hello!"
```
