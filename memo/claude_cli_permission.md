# claude CLI のパーミッションに関する整理

## 結論
現状の構成ではパーミッション問題は発生しない。

## 理由
- `claude -p` モードで実行している
- Claude CLI 側は `Read`, `Glob`, `Grep` による探索のみ → デフォルトのパーミッションで許可済み
- ファイル書き込み (`docs/{repo}.md`, `docs/index.md`) は Python スクリプト側が行っている
- Claude CLI は stdout にサマリーテキストを出力し、Python が `capture_output=True` で受け取って書き込む

## 補足
- `--dangerously-skip-permissions` は使わない
- `--allowed-tools` で個別指定することもできるが、今の構成では不要
- 書き込み系ツール (`Edit`, `Write`, `Bash`) を使おうとした場合のみパーミッション確認が発生するが、今の構成では該当しない
