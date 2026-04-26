# claude CLI の "Credit balance is too low" エラー

## 起きたこと
2026-04-27 の `python main.py` 実行中、13 リポジトリのうち 1 件目のサマリー生成（trycua/cua）成功直後から、後続のすべてが以下のエラーで失敗した。

```
claude CLI error:
```

stderr が空で原因不明だった。

## 原因
Anthropic API のクレジット残高不足。

`trycua/cua` の処理中に残高を使い切り、それ以降の `claude -p` 呼び出しが API 側で弾かれていた。エラーメッセージは **stderr ではなく stdout** に `Credit balance is too low` として出力されていたため、当初の実装（stderr のみ出力）では原因が見えなかった。

## 対応
`generate_summary_with_claude_cli` のエラー出力を stdout も含めるように修正（main.py:158-164）。

```python
if result.returncode != 0:
    print(f"  claude CLI error (returncode={result.returncode})")
    if result.stderr:
        print(f"    stderr: {result.stderr.strip()}")
    if result.stdout:
        print(f"    stdout: {result.stdout.strip()[:1000]}")
    return None
```

クレジットは https://console.anthropic.com/settings/billing で追加。

## 教訓
- claude CLI は失敗時のメッセージを **stdout に出すケースがある**。エラー時は stderr / stdout の両方を出すべき。
- 直前にセキュリティ系の修正（b625a09）を入れていたので最初はそちらを疑ったが、無関係だった。エラー内容を見る前にコードの差分から原因を推測すると遠回りになる。
- 1日あたりのトークンコストは $1〜2（13 リポジトリを `--max-turns 10` で探索）が相場。月 $30〜40 ペース。残高は余裕を持たせておくと安全。
