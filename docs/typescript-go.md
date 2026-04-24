---
url: https://github.com/microsoft/typescript-go
keywords: TypeScript, Go, compiler, native port, tsgo, LSP, type-checker, TypeScript 7, Corsa
oneliner: Microsoft 公式の TypeScript コンパイラ／言語サービスを Go で書き直した「TypeScript 7（ネイティブ版）」のステージング開発リポジトリ。
---

# microsoft/typescript-go 整理メモ

## このリポジトリは何？

- **TypeScript 本体（tsc）を Go 言語で書き直した「ネイティブ版」の開発リポジトリ**。社内コードネームは **Corsa**、将来的に **TypeScript 7** として公開される想定。従来の TS で書かれた tsc は **Strada** と呼ばれ区別される。
- README によれば、最終的には `microsoft/TypeScript` 本体へマージされ、このリポジトリ自体はクローズ予定の“staging repo”。
- 主な構成要素（`internal/` 配下に Go で実装）：
  - `scanner` / `parser` / `binder` / `checker` …パーサ〜型チェッカ一式
  - `transformers` / `printer` / `sourcemap` …JS 出力・宣言ファイル出力
  - `module` / `modulespecifiers` / `tsoptions` …モジュール解決、`tsconfig.json`
  - `lsp` / `ls` / `project` …Language Server 実装
  - `api` / `jsonrpc` …外部 API
- エントリポイント：
  - `cmd/tsgo`（CLI。`tsgo` / `tsgo --lsp` / `tsgo --api` の3モード）
  - `_packages/native-preview`（`@typescript/native-preview` として npm 配布）
  - `_extension`（VS Code 拡張 “TypeScript (Native Preview)”）

## 何が嬉しいの？（既存手段との比較）

- **本家 tsc（TypeScript／Strada）比**：同一の意味論を保ったまま **Go でネイティブビルド** され、コンパイル・型チェック・エディタ補完が桁違いに高速化される（公式発表では~10倍級）。`README` の機能対応表でも「TS 6.0 と同じ構文エラー／同じ型／同じメッセージ」と明記しており、**振る舞い互換のドロップイン置換**を目指している点が最大の差。
- **esbuild / swc / Babel 比**：それらは主に「**型を捨てて高速トランスパイル**」するツールで、型チェックや `.d.ts` 出力、`tsconfig` の project references などには対応していない。`typescript-go` は **型チェック・宣言ファイル生成・LSP まで含むフルスタックの正式な TypeScript 実装**で、単なるトランスパイラではない。
- **deno/bun の内蔵 TS 比**：個別エコシステムに閉じた実装ではなく、**Microsoft 公式・tsc と同一仕様**を維持する点が本質的に違う。
- **エディタ体験**：LSP サーバ (`tsgo --lsp`) と VS Code 拡張が同梱されており、`tsserver`（Node 実装）を置き換える形で **補完・ホバー・診断のレイテンシを削減**できる。

制約：現時点は preview。`CHANGES.md` にある通り JSDoc 周りなど一部仕様は意図的に簡素化されており、API・Watch モードなどは "in progress / prototype" ステータス。

## 使うときの流れ

1. **インストール（ユーザー視点）**
   ```sh
   npm install @typescript/native-preview
   npx tsgo            # tsc と同じ感覚で呼ぶ
   npx tsgo -p tsconfig.json
   npx tsgo --lsp      # LSP サーバとして起動
   ```
2. **VS Code で試す**：Marketplace から “TypeScript (Native Preview)” 拡張を入れ、settings に
   ```json
   { "js/ts.experimental.useTsgo": true }
   ```
   を追加すると、組み込みの tsserver の代わりに tsgo の LSP が言語サービスを担当。
3. **動作内容**：`cmd/tsgo/main.go` → `internal/execute.CommandLine` が CLI エントリ。引数を `tsoptions` で解析し、`compiler` パッケージでプログラム生成 → `checker` で型検査 → `transformers`/`printer` で JS/`.d.ts` を出力、という本家 tsc と対応するパイプライン。
4. **コントリビュータ視点**
   - `go build ./cmd/tsgo` で CLI をビルド。タスクランナーは `Herebyfile.mjs`（hereby）。
   - TS 本家のテストは `_submodules/TypeScript` を参照しつつ `testdata/` / `internal/testrunner` で実行（baseline 比較方式）。
   - 互換性の境界は `CHANGES.md` に列挙（Closure 系 JSDoc 削除など）。バグ報告は README の “done / in progress / prototype / not ready” ステータスを確認してから行う運用。

要約すると、**「tsc の完全互換をうたう高速ネイティブ実装 + LSP」を段階的に仕上げるためのモノレポ**で、ユーザーは `npx tsgo` や VS Code 拡張経由でそのまま試せる、という位置づけ。
