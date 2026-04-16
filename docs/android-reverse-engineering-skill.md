---
url: https://github.com/SimoneAvogadro/android-reverse-engineering-skill
keywords: Android, reverse-engineering, APK, jadx, API-extraction
oneliner: Android の APK/XAPK/JAR/AAR を Claude Code 上で decompile し、HTTP API を抽出・文書化するワークフローを提供する Claude Code プラグイン（Skill）。
---

# android-reverse-engineering-skill 概要

## 1. このリポジトリは何？

Claude Code（Anthropic 製のコーディングエージェント）向けの**プラグイン / Skill** で、Android アプリ（`.apk` / `.xapk` / `.jar` / `.aar`）を **decompile し、そこから HTTP API の仕様を取り出して文書化する**作業を、自然言語または `/decompile` スラッシュコマンドから半自動で進めるためのもの。

構成要素：

- `plugins/android-reverse-engineering/skills/.../SKILL.md`  
  5 フェーズのワークフローを記述した Skill 定義（依存確認 → decompile → 構造解析 → コールフロー追跡 → API 抽出）。
- `scripts/`（Shell）  
  - `check-deps.sh` / `install-dep.sh`: Java・jadx・Vineflower/Fernflower・dex2jar の有無を確認し OS に応じて導入  
  - `decompile.sh`: jadx または Fernflower（もしくは両方並走）で decompile。XAPK は内部の APK を自動展開して個別に処理  
  - `find-api-calls.sh`: Retrofit アノテーション、OkHttp 呼び出し、URL リテラル、認証ヘッダを grep ベースで抽出
- `references/`（Markdown）  
  jadx/Fernflower の CLI リファレンス、API 抽出パターン、コールフロー解析テクニック、セットアップ手順。
- `commands/decompile.md`  
  `/decompile <file>` スラッシュコマンドの挙動定義。
- `.claude-plugin/marketplace.json` と `plugin.json`  
  Claude Code の `/plugin marketplace add ...` でインストール可能にするためのメタ情報。

ライセンスは Apache 2.0。主言語は Shell。

## 2. 何が嬉しいの？（類似手段との比較）

既存の「生の CLI ツール」で同じことをやる場合、利用者は jadx / Fernflower / Vineflower / dex2jar / apktool などを個別にインストールし、APK なのか JAR なのか XAPK なのかで手順を切り替え、decompile 後のソースを grep しながら自力で Retrofit/OkHttp の断片から API 仕様を再構築する必要がある。

このリポジトリの嬉しさは以下：

- **「どのツールをいつ使うか」がワークフロー化されている**。jadx は速くて Android 一式を処理できる、Fernflower は複雑な Java（ラムダ・ジェネリクス・ストリーム）で品質が高い、迷ったら `--engine both` で並走して比較 —— という判断基準を Skill に埋め込み、Claude に選ばせられる。
- **依存のインストールまで面倒を見る**。`install-dep.sh` が OS と sudo の有無を判定し、可能なら `~/.local/` へ user-local インストールする。sudo が必要で不可なら手動コマンドを提示して終了するので環境構築でハマらない。
- **XAPK（base + split APK バンドル）を透過的に処理**。apktool や jadx 単体では自分で unzip して各 APK を回す必要があるが、本 Skill は自動展開して各 APK を個別に decompile する。
- **「decompile して終わり」ではなく、API 仕様書化までがスコープ**。`find-api-calls.sh` で Retrofit/OkHttp/URL/Auth を一掃し、LLM がコールチェーン（Activity → ViewModel → Repository → ApiService）を辿って、エンドポイントごとに「メソッド / パス / パラメータ / ヘッダ / 呼び出し元」を含む決まったフォーマットで Markdown を吐く。ここが MobSF や単発 CLI との一番大きな差。
- **難読化（ProGuard/R8）前提のヒント**が references に入っており、Retrofit アノテーションや URL リテラルを難読化されないアンカーとして使う戦略が明示されている。

用途としては、**セキュリティリサーチ、相互運用のための API 解析、マルウェア解析、CTF** が想定され、利用者の責任で合法的に使うことが README で明示されている。

## 3. 使うときの流れ

1. **インストール**  
   Claude Code 内で `/plugin marketplace add SimoneAvogadro/android-reverse-engineering-skill` → `/plugin install android-reverse-engineering@android-reverse-engineering-skill`。ローカルクローンからも可。
2. **起動**  
   `/decompile path/to/app.apk` もしくは「Decompile this APK」「Extract API endpoints from this app」等の自然言語。trigger フレーズで Skill が自動起動する。
3. **Phase 1: 依存確認**  
   `check-deps.sh` で Java17+/jadx（必須）と Vineflower/dex2jar（推奨）を検査。不足は `install-dep.sh` で導入。
4. **Phase 2: decompile**  
   入力種別に応じてエンジンを選択：APK/XAPK は jadx を第一選択、JAR/AAR は Fernflower、品質比較したいときは `--engine both`、難読化 APK は `--deobf`。出力は `<file>-decompiled/`（both なら `jadx/` と `fernflower/` サブディレクトリ）。
5. **Phase 3: 構造解析**  
   `AndroidManifest.xml` からランチャー Activity・Application クラス・パーミッションを把握、`sources/` のパッケージ構造から `api` / `network` / `repository` 等を特定、MVP/MVVM/Clean Architecture を判別。
6. **Phase 4: コールフロー追跡**  
   Application.onCreate の HTTP クライアント初期化から始め、UI → ViewModel → Repository → ApiService → 実 HTTP 呼び出しへ辿る。Dagger/Hilt の `@Module` で DI バインディングを確認。難読化時は文字列リテラルとライブラリ API をアンカーに。
7. **Phase 5: API 抽出と文書化**  
   `find-api-calls.sh`（`--retrofit` / `--urls` / `--auth` で絞り込み可）で候補を列挙し、各エンドポイントについてメソッド・ベース URL・パラメータ・ヘッダ・レスポンス型・呼び出し元を定型 Markdown で記録。
8. **成果物**  
   decompile 済みソース、アーキテクチャサマリ、API ドキュメント、主要機能（特に認証）のコールフローマップが最終的に手元に残る。
