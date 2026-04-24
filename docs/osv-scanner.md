---
url: https://github.com/google/osv-scanner
keywords: vulnerability-scanner, OSV, SCA, dependency-scan, container-scan, Go, SBOM, guided-remediation, offline-mode
oneliner: OSV.dev のオープンな脆弱性DBを用いて、プロジェクトの依存関係・コンテナ・OSパッケージの既知脆弱性を検出する Google 公式の Go 製スキャナ。
---

# google/osv-scanner 概要

## このリポジトリは何？

- **OSV.dev の公式フロントエンドとなる CLI 型の脆弱性スキャナ**（Go 製）。裏側では拡張可能な SCA ライブラリ [OSV-Scalibr](https://github.com/google/osv-scalibr) を利用。
- ソースディレクトリ・ロックファイル・コンテナイメージ・SBOM などを入力に、対象が利用している OSS パッケージを列挙し、それに対応する既知脆弱性（CVE/GHSA など）を OSV 形式のデータベースから突き合わせる。
- 主なサブコマンド（`cmd/osv-scanner/` 配下）：
  - `scan source` … ローカルディレクトリの再帰スキャン（`package.json`, `go.mod`, `pom.xml`, `Cargo.lock` など 19+ 種類のロックファイル対応）
  - `scan image` … Docker/OCI イメージをレイヤ単位で解析（Alpine/Debian/Ubuntu + Go/Java/Node/Python）
  - `fix` … 実験的な **Guided Remediation**（npm / Maven で安全にバージョンを上げる提案）
  - `update` / `mcp` / `--licenses` … 依存の更新支援、MCP サーバ連携、deps.dev に基づくライセンス監査
- 対応言語は C/C++, Go, Java, JS, Python, PHP, Ruby, Rust, Dart, Elixir, R など広範。GitHub Actions 用ラッパも同梱（`actions/`）。

## 何が嬉しいのか（既存手段との比較）

- **OSV.dev という「オープンかつ機械可読」な DB を使える**：GitHub Security Advisory、RustSec、Ubuntu USN などの一次ソースを OSV スキーマで統合しており、影響バージョン範囲が曖昧な CVE テキストではなく **マシンリーダブルな範囲比較** でマッチするため、誤検知・取りこぼしが少ない。
- **Snyk / Mend / Black Duck などの商用 SCA と比較して**：ライセンス費用が不要で、Google 公式かつ OSS。データ源が公開・監査可能。
- **GitHub Dependabot と比較して**：単一ホスト/CI に閉じず、ローカル/任意 CI から実行でき、**コンテナイメージや vendored C/C++ 同梱コード**のスキャンまでカバー。`--call-analysis` により「脆弱関数が実際に呼ばれているか」で偽陽性を抑えられる。
- **Trivy / Grype と比較して**：コンテナだけでなく **ソースツリー・ロックファイル・マニフェスト解析**が主戦場で、さらに `fix` による *推奨バージョンの自動提案* という踏み込んだ修正支援を持つ。
- **オフライン運用可**：`--offline --download-offline-databases` で DB をローカルにミラーし、ネットワーク遮断環境や閉域 CI でも利用可能（多くの SaaS 型 SCA では困難）。
- **SLSA Level 3・OpenSSF Scorecard** で供給網自体の信頼性を担保。

## 利用の流れ

1. **インストール**  
   `go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest`、または Releases からバイナリ取得、Docker イメージ、GitHub Action (`actions/`) も選択可。

2. **スキャン対象を選ぶ（3 パターンが代表的）**  
   ```bash
   # ① ソースツリー全体を再帰スキャン
   osv-scanner scan source -r /path/to/repo

   # ② コンテナイメージをスキャン
   osv-scanner scan image my-image:tag

   # ③ ライセンス監査（許可リスト方式）
   osv-scanner --licenses="MIT,Apache-2.0" /path/to/repo
   ```

3. **設定・無視ルールの調整**  
   ルート直下の `osv-scanner.toml` に誤検知・未対応脆弱性の `IgnoredVulns`、パスごとの例外、ライセンス許可リストを記述。`docs/configuration.md` 参照。

4. **出力形式を選ぶ**  
   `--format` で `table`（既定）、`json`、`sarif`（GitHub Code Scanning 連携）、`html`、`cyclonedx` など。CI なら SARIF をアップロードするのが定番。

5. **修正フェーズ（任意・実験的）**  
   ```bash
   osv-scanner fix -M package.json -L package-lock.json   # 対話型
   osv-scanner fix --strategy=in-place --max-depth=3 --min-severity=5 -L package-lock.json
   ```
   依存の深さ・最低 Severity・戦略（`in-place` / `relock` / `override`）を指定し、ROI の高い修正案を適用。

6. **CI への組み込み**  
   `actions/` 配下の reusable workflow を呼ぶか、Docker で実行 → SARIF を GitHub Security タブへ。PR 差分に導入された脆弱性のみ失敗させる運用も可能。オフライン CI では事前に DB を配布。

7. **運用**  
   OSV.dev の DB は日次で更新されるため、定期実行（cron / スケジュール済み GH Actions）で再スキャンし、新規に登場した CVE を検出する運用が基本。
