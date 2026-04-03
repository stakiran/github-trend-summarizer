# 仕様まとめ

## 概要
GitHub Trends のリポジトリをニュースのように収集し、サマリーを生成する。

## 技術スタック
- Python スクリプト
- スクレイピング: requests + BeautifulSoup
- サマリー生成: Claude API
- 出力: Markdown（GitHub Pages で公開）

## 処理フロー
1. `github.com/trending` をスクレイピングしてトレンドリポジトリ一覧を取得
2. 各リポジトリについて:
   - `workspace/{repo}/` が存在すればサマリー生成はスキップ
   - 存在しなければ tarball で `.git/` なしでソース取得
     ```
     mkdir -p workspace/{repo}
     curl -L https://github.com/{owner}/{repo}/archive/refs/heads/main.tar.gz | tar -xz --strip-components=1 -C workspace/{repo}
     ```
3. Claude API でサマリー生成し `docs/{repo}.md` に保存
4. `docs/index.md` を更新

## ディレクトリ構成
- `workspace/{repo}/` — ソースファイル（.git/ なし）
- `docs/{repo}.md` — 各リポジトリのサマリー
- `docs/index.md` — 一覧ページ

## docs/{repo}.md
- Claude API によるリポジトリのサマリー

## docs/index.md
- 最新日付を先頭に prepend
- 見出しは `# yyyy-mm-dd`
- 各行のフォーマット:
  ```
  - [repo-a](repo-a.md) ⭐1.2k Python, CLI, AI このリポジトリの端的な説明
  ```
- star数・言語はトレンドページから取得
- キーワード（3つ以内）と端的な説明は Claude API で生成
- 同じリポジトリが別日にトレンド入りした場合、サマリー生成はスキップだが index.md のリンクには載せる

## 重複判定
- `workspace/{repo}/` の存在チェックで判定
- 存在する場合はソース取得・サマリー生成をスキップ
