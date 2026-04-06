---
url: https://github.com/NVIDIA/personaplex
keywords: speech-to-speech, full-duplex, persona-control, voice-cloning, real-time-conversation
oneliner: テキストプロンプトで会話スタイル、音声プロンプトで声質を制御できるリアルタイム全二重音声対話モデル
---

## PersonaPlex — NVIDIA のリアルタイム音声対話モデル

### これは何？

PersonaPlex は、**リアルタイム・全二重（Full-Duplex）の Speech-to-Speech 対話モデル**である。Kyutai の [Moshi](https://arxiv.org/abs/2410.00037) アーキテクチャをベースに NVIDIA がファインチューニングしたもので、2 つの軸でモデルの振る舞いを制御できる点が最大の特徴。

| 制御軸 | 方法 | 例 |
|---|---|---|
| **ペルソナ（何を・どう話すか）** | テキストのシステムプロンプト | 「あなたはピザ店の店員マルコです。親しみやすく丁寧に対応してください」 |
| **声質（誰の声で話すか）** | 音声プロンプト（`.wav` / `.pt`） | 参考音声を数秒与えるだけでその声色を模倣 |

内部は **音声コーデック（Mimi）→ マルチストリーム言語モデル（Depformer）→ 音声デコード** の一気通貫パイプラインで、80 ms/フレームの低遅延ストリーミング推論を実現する。ユーザの割り込み・相槌・沈黙といった自然な会話動態にも対応している。

---

### 既存手段と比べて何が嬉しいのか？

| 比較対象 | PersonaPlex の優位点 |
|---|---|
| **ElevenLabs 等の TTS サービス** | TTS は「読み上げ」専用。PersonaPlex は音声理解＋生成が単一モデル内で完結し、**対話**ができる |
| **LLM + 外付け ASR/TTS パイプライン** | ASR→LLM→TTS の直列構成は遅延が大きく全二重が困難。PersonaPlex はエンドツーエンドで **50〜100 ms レベルの応答** |
| **オリジナル Moshi** | Moshi はペルソナ・声質の制御機構を持たない。PersonaPlex は **プロンプトだけで人格と声を切り替え可能**（再学習不要） |
| **Replica / 固定キャラクタ音声** | キャラクタが固定。PersonaPlex は自然言語プロンプトで **動的にロールを定義** できる |

要約すると、「低遅延の全二重音声対話」と「プロンプトベースのペルソナ＋声質制御」を **単一モデルで両立** している点がユニーク。

---

### 使うときの流れ

```
1. 環境構築
   └─ Docker (nvidia-docker) でコンテナ起動、または pip install で依存解決
      （PyTorch ≥2.2, CUDA 必須）

2. モデルのロード
   └─ HuggingFace Hub から Mimi コーデック + LM の重みを自動ダウンロード
      （moshi/moshi/models/loaders.py が担当）

3. プロンプト設定
   ├─ テキストプロンプト: <system> タグで囲んだペルソナ指示を記述
   └─ 音声プロンプト: 参考音声 .wav を指定（初回エンコード後 .pt にキャッシュ可能）

4. サーバ起動（moshi/moshi/server.py）
   └─ WebSocket サーバが立ち上がり、3 つの非同期ループが並走
      recv_loop → opus_loop（Mimi→LM→デコード） → send_loop

5. クライアント接続（client/ の React アプリ or 任意の WebSocket クライアント）
   └─ ブラウザからマイク入力 → Opus エンコード → WebSocket 送信
      → モデルがリアルタイムで応答音声＋テキストを返却

6. オフライン推論（moshi/moshi/offline.py）
   └─ バッチ処理で音声ファイルを入力→応答音声を生成することも可能
```

用意されている声色プリセットは **Natural 系**（NATF0〜3 / NATM0〜3）と **Varied 系**（VARF0〜4 / VARM0〜4）の計 18 種。独自の参考音声を `.wav` で渡せば任意の声質にも対応する。
