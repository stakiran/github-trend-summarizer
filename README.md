# github-trend-summarizer
GitHub Trending のリポジトリを収集し、Claude Code で各リポジトリを自律探索してサマリーを生成するツール。

## 必要なもの
- Python 3.9+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (`claude` コマンドが使えること)
- curl, tar

## セットアップ

```
pip install -r requirements.txt
```

## 使い方

```
python main.py
```

## 出力
- `workspace/{repo}/` — ダウンロードしたソースコード (.git/ なし)
- `docs/{repo}.md` — 各リポジトリのサマリー (frontmatter 付き)
- `docs/index.md` — 一覧ページ (GitHub Pages 用)