---
url: https://github.com/ruvnet/RuView
keywords: WiFi CSI, 人物姿勢推定, 非接触バイタル, ESP32センシング, エッジAI
oneliner: 市販WiFiのCSI信号から、カメラなしで人物姿勢・呼吸・心拍・在室をリアルタイム検知するRustベースのセンシング基盤。
---

# RuView (WiFi DensePose) 概観

## 1. このリポジトリは何？

**RuView** は「WiFi 電波を“レーダー兼カメラ”として使う」センシングプラットフォーム。ルータや ESP32 から得られる **Channel State Information (CSI)** を解析して、映像を一切使わずに以下を検出する。

- **人物姿勢推定**：17 COCO キーポイント（独自の WiFlow アーキテクチャ、カメラ教師で PCK@20 = 92.9%）
- **バイタルサイン**：呼吸 6–30 BPM、心拍 40–120 BPM（接触なし）
- **在室・人数・動線**：MinCut ベースの人数カウント、在室精度 100%
- **環境センシング**：部屋の RF フィンガープリント、家具移動や侵入検知、壁越しモーション、RF トモグラフィ、パッシブレーダ

実装は **Rust 中心のモノレポ**（`rust-port/wifi-densepose-rs/` に 15+ のクレート：`-core / -signal / -nn / -train / -mat / -hardware / -ruvector / -api / -wasm / -cli / -sensing-server …`）＋ Python v1 リファレンス＋ **ESP32-S3 ファームウェア**（`firmware/esp32-csi-node/`）＋ Three.js の可視化 UI で構成。関連設計は `docs/adr/` に **ADR が 79 本**、DDD モデルが 7 本。**1,400+ テスト**、Docker マルチアーチ配布、HuggingFace に学習済みモデル (`ruv/ruview`)、MIT。

エッジ側は **WASM モジュール群（全 60+）** が `wifi-densepose-wasm-edge` に揃っており、医療・セキュリティ・スマートビル・小売・産業など 13 カテゴリのユースケースを 5〜30KB の WASM としてセンサに OTA 投入できる。

## 2. 既存手段と比べて何が嬉しいのか

| 観点 | RuView (WiFi CSI) | カメラ / ビデオAI | PIR・専用mmWave | ウェアラブル |
|---|---|---|---|---|
| プライバシ | 画像を撮らない、GDPR/HIPAA の映像規制対象外 | 同意・保管・マスキングが必要 | △ | ユーザ負担 |
| 暗所・壁越し | **壁・煙・塵・闇でも動作**（最大 ~5m壁越え） | 基本 NG | 壁越え不可 | — |
| ハード単価 | **$9 の ESP32-S3** 1 台から。全部入りで **$140** (+Cognitum Seed) | $200–2,000/ゾーン | $3〜だが機能限定 | 人数分必要 |
| カバー範囲 | 既設 WiFi に乗るので**新配線不要**、1AP で 3〜5 人、多AP で 15〜20 人 | 1台1部屋、死角多い | 点単位 | 装着者限定 |
| 取得できる情報 | 姿勢・呼吸・心拍・動線・部屋指紋を**同時に**1 パイプで | 映像 + 後段推論が必要 | 動きの有無のみ | 装着者の生体のみ |
| 学習コスト | ラベルなしの自己教師 (ADR-024)、30 秒以内にその部屋へ順応（SNN / LoRA 部屋アダプタ） | 大量ラベルデータ必須 | 学習不可 | — |
| ランタイム | Rust で **54,000 frame/s**、推論 0.008–0.012ms、8KB 4bit 量子化モデルで ESP32 オンボード推論、クラウド不要 | GPU/クラウド前提 | 軽量だが拡張不可 | クラウド連携多い |
| 信頼性 | Ed25519 ウィットネスチェーン＋SHA-256 再現プルーフ (`v1/data/proof/verify.py`) で測定を暗号学的に証明 | — | — | — |

要するに **「安い」「映らない」「壁の向こうまで届く」「クラウド要らず」「再現性が検証できる」** を同時に満たすのが他手段に対する優位。

## 3. 使うときの流れ

### A. まず触る（ハード不要・数十秒）
```bash
docker pull ruvnet/wifi-densepose:latest
docker run -p 3000:3000 ruvnet/wifi-densepose:latest   # http://localhost:3000
python v1/data/proof/verify.py                         # 決定論プルーフで信号処理系を検証
```

### B. 実センシング（ESP32-S3 1 台〜メッシュ 3–6 台、~$9〜$54）
1. **ファーム書き込み**：`python -m esptool --chip esp32s3 --port COMx write_flash …`
2. **プロビジョン**：`python firmware/esp32-csi-node/provision.py --port COMx --ssid … --password … --target-ip …`（必要ならチャネルホッピング `--hop-channels "1,6,11"`）
3. **センシングサーバ起動**：`cargo run -p wifi-densepose-sensing-server` または Docker を `CSI_SOURCE=esp32` で起動
4. **UI / API / WS**：Web UI でポーズ・呼吸・心拍を表示、REST/WebSocket から外部連携

### C. 用途別スクリプト（Node.js ワンライナー）
- 人数カウント：`node scripts/mincut-person-counter.js --port 5006`
- 睡眠・無呼吸・ストレス・歩行：`sleep-monitor.js / apnea-detector.js / stress-monitor.js / gait-analyzer.js`
- 環境：`room-fingerprint.js / material-detector.js / rf-tomography.js / through-wall-detector.js`
- オフライン再生：任意スクリプトに `--replay data/recordings/*.csi.jsonl`

### D. 自分の部屋に合わせ込む（学習）
1. データ収集：`python scripts/collect-training-data.py --duration 120`（任意でカメラ教師：`collect-ground-truth.py` + MediaPipe）
2. 位置合わせ：`node scripts/align-ground-truth.js …`
3. 学習：`node scripts/train-ruvllm.js …` / `train-wiflow-supervised.js --scale lite|small|medium|full`
4. 評価：`node scripts/eval-wiflow.js …`、出力は `.rvf` 1 ファイル（エッジ・クラウド・ブラウザ WASM で共通）
5. 既成モデルで始めたい場合：`huggingface-cli download ruv/ruview --local-dir models/`

### E. エッジ展開 & 検証
- 60+ の WASM エッジモジュール（医療/セキュリティ/ビル/小売/産業 …）を ESP32-S3 に OTA 投入して 10ms 未満で判定
- リリース前・マージ前は **ウィットネスバンドル**：`cargo test --workspace --no-default-features` → `python v1/data/proof/verify.py` → `bash scripts/generate-witness-bundle.sh` → `VERIFY.sh` で 7/7 PASS を確認（ADR-028）。

> 最小体験は **Docker だけ**、本番は **ESP32-S3 + 任意で Cognitum Seed($131)** のレイヤーで段階的に拡張できる設計になっている。
