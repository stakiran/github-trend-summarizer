---
url: https://github.com/XTLS/Xray-core
keywords: proxy, VLESS, REALITY, XTLS, v2ray, circumvention, Go, VMess, Shadowsocks, Trojan
oneliner: VLESS/XTLS/REALITY を中核に据えた、検閲回避・秘匿通信向けの多機能プロキシプラットフォーム（v2ray-core 改良版）。
---

# XTLS/Xray-core 調査メモ

## このリポジトリは何？

- **Go 製のネットワークプロキシ基盤**。`main/main.go` → `xray run -c config.json` という単一バイナリ型の CLI で、設定ファイル（JSON/JSONC/TOML/YAML）に書いた「inbound（受け口）＋ outbound（出口）＋ routing（経路）」を実行する。
- `v1.0.0` は **v2fly / v2ray-core から fork** されたもので、以降は XTLS チームが多数の独自拡張（VLESS、XTLS Vision、REALITY、XHTTP など）を積み上げてきた派生系。ライセンスは MPL-2.0。
- 対応プロトコルの幅がとにかく広い。`proxy/` 配下に以下が並ぶ:
  - **VLESS / VMess**（本家系プロトコル、TLS・XTLS 対応）
  - **Shadowsocks / Shadowsocks 2022 / Trojan**（他エコシステム互換）
  - **SOCKS / HTTP**（一般的なプロキシ入口）
  - **Hysteria / WireGuard / Tun / Freedom / Blackhole / Dokodemo / Loopback / DNS**（特殊用途・L3 統合）
- トランスポート層も `transport/internet/` に TCP/UDP, WebSocket, gRPC, KCP, HTTPUpgrade, SplitHTTP, **REALITY**, TLS, Hysteria などが揃う。
- `app/` には router, dns, dispatcher, policy, observatory（経路の自動品質計測）, metrics, reverse proxy, commander（gRPC API）など、単なるトンネラを超えた統合機能群。
- CLI 補助コマンド（`main/commands/all/`）として UUID/x25519/curve25519/ML-KEM768/ML-DSA65 生成、TLS ping、WG ツール、VLESS encryption 鍵ツールなどを同梱。

## 何が嬉しい？（既存手段との比較）

- **対 v2ray-core（本家）**: fork 元だが、XTLS Vision（TLS in TLS の二重暗号化オーバーヘッドを削る）や **REALITY**（有名サイトの TLS 証明書チェーンをそのまま転用し、自前の TLS 証明書が不要で能動プロービングにも耐える）など、**2020 年代の検閲対策の主要発明が “本家的に” 入っているのが Xray 側**。性能・生態系（v2rayN/NG, 3X-UI, Marzban, Hiddify など）も Xray を前提にしたものが多い。
- **対 sing-box / mihomo(Clash Meta)**: これらも類似の守備範囲だが、VLESS + XTLS Vision + REALITY の “ファーストパーティ実装” は Xray。新プロトコル（XHTTP、VLESS ポスト量子暗号化など）は Xray でまず議論・実装される傾向。逆に sing-box はユーザー向け統合 UI や Clash ルール互換に強み、mihomo は Clash 文化圏との親和性に強み、という棲み分け。
- **対 Shadowsocks / Trojan 単体クライアント**: 単一プロトコル専用の軽量実装に対し、Xray は **1 バイナリで多プロトコル・多トランスポート・ルーティング・DNS・可観測性まで** 持つオールインワン。Shadowsocks/Trojan サーバとしても動かせるので置き換えや相互運用が容易。
- **対 OpenVPN / WireGuard**: VPN は通信全体を丸ごと包むのが目的だが、Xray は **検閲突破 & 細粒度ルーティング** が主眼。WireGuard を「inbound」「outbound」として取り込むことも可能で、両者を組み合わせる運用にも向く。
- 実装面の利点: Go 製でクロスコンパイルが楽、CGO_ENABLED=0 の 1 行ビルド、再現可能ビルド手順が README に記載、Docker/Homebrew/各種 Web パネル（3X-UI, Marzban, Hiddify 等）・GUI（v2rayN/NG, Streisand, Shadowrocket 互換など）から利用できる豊富なエコシステム。

## 使うときの流れ

1. **入手**: 公式 Linux スクリプト（XTLS/Xray-install）、Docker（`ghcr.io/xtls/xray-core`）、`brew install xray`、または `go build -o xray ./main` で自前ビルド。Web パネル（3X-UI, Marzban など）を被せる運用も一般的。
2. **鍵・ID を発行**: `xray uuid`, `xray x25519`（REALITY 用）, `xray wg` などサブコマンドで必要な ID／鍵を生成。
3. **config を書く**: inbound（例: ポート 443 で VLESS+REALITY を受ける）、outbound（例: freedom＝直結、あるいは別 Xray へ中継）、routing（ドメイン・IP ルールで国内直結／国外プロキシ振り分け）、任意で dns / policy / observatory を定義。XTLS/Xray-examples や REALITY チュートリアルが定番の雛形。
4. **起動・検証**: `xray run -c config.json`（`-confdir` で分割設定、`-test` で構文のみ検証、`-dump` で解決後の設定をダンプ）。systemd や Docker でデーモン化。
5. **クライアント側**: v2rayN (Windows)、v2rayNG (Android)、Streisand/Happ (iOS/macOS)、v2rayA (Linux) などの GUI に同じ UUID/鍵/REALITY 公開鍵を入れて接続。サーバ状態は gRPC API（commander）や metrics/observatory から監視可能。
6. **運用拡張**: ルーティング調整、フォールバック（`All-in-One-fallbacks-Nginx` 例）、複数 outbound の自動品質選択（observatory）、reverse proxy などで用途に合わせて育てていく。
