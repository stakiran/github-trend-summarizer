---
url: https://github.com/PowerShell/PowerShell
keywords: PowerShell, cross-platform, shell, automation, .NET, cmdlet, scripting, CLI, DevOps, object-pipeline
oneliner: Windows / Linux / macOS で動作する、オブジェクト指向パイプラインを備えたクロスプラットフォーム自動化シェル&スクリプト言語 (PowerShell 7+) の本体ソースコード。
---

# PowerShell/PowerShell リポジトリ整理

## このリポジトリは何？

Microsoft が OSS (MIT ライセンス) として公開している **PowerShell 7 系 (旧称 PowerShell Core) の本体**。元は Windows 専用だった Windows PowerShell 5.1 のコードベースを fork し、.NET Core / .NET 上で **Windows・Linux・macOS すべてで動く** ように作り直したもの。

中身は大きく 3 つの要素で構成される。
- **コマンドラインシェル** (`pwsh` 実行ファイル)
- **スクリプト言語** (cmdlet, 変数, パイプ, 制御構文など)
- **cmdlet 処理フレームワーク** (.NET クラスで cmdlet を実装するための SDK)

主要ディレクトリ:
- `src/System.Management.Automation` … エンジン本体 (パーサ、ランタイム、パイプライン)
- `src/Microsoft.PowerShell.Commands.*` … Management / Utility / Security / Diagnostics 等の標準 cmdlet 群
- `src/Microsoft.PowerShell.ConsoleHost` … 対話コンソールホスト
- `src/Microsoft.PowerShell.SDK` … 他アプリから PowerShell を組み込むための NuGet SDK
- `src/powershell-win-core` / `powershell-unix` … OS 別の `pwsh` エントリポイント
- `test/` (Pester テスト), `docs/`, `build.psm1` (ビルド用 PS モジュール), `PowerShell.sln`
- 言語は C# がほぼ全て。

## このリポジトリは何が嬉しいの？

**bash / zsh / cmd / Python スクリプトなど既存手段との違い**が価値になる。

| 観点 | bash / zsh | Python など | **PowerShell 7+** |
|---|---|---|---|
| パイプで流れるもの | テキスト (文字列) | プロセス毎に自作 | **.NET オブジェクト** (`.Property` や型付きメソッドでそのまま操作可) |
| クロスプラットフォーム | Unix 系のみ | ○ | ○ (Win/Linux/mac) |
| Windows 管理 (レジストリ/WMI/AD/Exchange/Azure) | ほぼ不可 | SDK 経由 | **ネイティブに cmdlet** で扱える |
| JSON/CSV/XML/REST | jq+curl 等の組合わせ | ライブラリ追加 | `ConvertTo-Json` / `Invoke-RestMethod` 等が標準 |
| 実行基盤 | shell + coreutils | CPython | 単一 .NET ランタイム (配布しやすい) |
| 組み込み利用 | 難 | 容易 | **Microsoft.PowerShell.SDK** で C# アプリに埋め込める |

つまり「**テキストを awk/sed で泣きながら整形しなくても、コマンドの出力がオブジェクトなのでそのまま `.Name` `.Length` `Where-Object` `Sort-Object` で操作できる**」のが最大の売り。Windows 管理タスクと DevOps/Azure/Docker 運用を、**同じスクリプトで Linux/Mac からも流用できる**点は、Windows 限定だった Windows PowerShell 5.1 や、Windows 管理が弱い Unix シェルに対する明確な優位点になる。

## 使うときの流れ

一般ユーザと開発者で 2 パターンある。

### A. 「PowerShell を使う」ユーザの流れ
1. [公式インストール手順](https://learn.microsoft.com/powershell/scripting/install/installing-powershell) で OS 別に `pwsh` を入れる (winget / apt / brew / MSI 等)。
2. ターミナルで `pwsh` を起動し、`Get-Command` `Get-Help <cmdlet>` で cmdlet を探索。
3. `Get-Process | Where-Object WS -gt 100MB | Sort-Object CPU -Desc` のように **動詞-名詞 (Verb-Noun)** の cmdlet をパイプで繋いで書く。
4. `.ps1` ファイルに保存してスクリプト化、必要なら関数/モジュール (`.psm1`) へ昇格。
5. REST API, JSON, Azure, Active Directory, ファイル/プロセス管理などは標準 cmdlet or Gallery モジュールで拡張。

### B. 「このリポジトリを開発する / ビルドする」流れ (`docs/building/` 系準拠)
1. リポジトリを clone (`git clone https://github.com/PowerShell/PowerShell.git`)。
2. 既存の `pwsh` を起動し、同梱のビルドモジュールを読み込む:
   ```powershell
   Import-Module ./build.psm1
   Start-PSBootstrap         # .NET SDK など依存をセットアップ
   Start-PSBuild -Clean -PSModuleRestore -UseNuGetOrg
   ```
   → `src/powershell-win-core/bin/Debug/net*/…/pwsh.exe` が生成される。
3. 動作確認は `& (Get-PSOutput)` で開発ビルドを起動、テストは Pester ベースの `Start-PSPester`。
4. 変更は RFC リポジトリ (PowerShell-RFC) と `.github/CONTRIBUTING.md` に沿って Issue / PR を出す。Windows PowerShell 5.1 には **バックポートされない** 点に注意 (このリポは 7.x 以降専用)。
5. 他アプリへ組み込みたい場合は `Microsoft.PowerShell.SDK` NuGet を参照し、C# から PowerShell ランタイムをホストする形で利用する。
