---
url: https://github.com/jqlang/jq
keywords: json, command-line, filter, data-transformation, cli-tool
oneliner: JSON データをコマンドラインで自在にフィルタリング・変換するための軽量プロセッサ
---

## jqlang/jq — コマンドライン JSON プロセッサ

### これは何？

**jq** は、JSON に特化した軽量コマンドラインツール。テキスト処理における `sed` / `awk` / `grep` の JSON 版にあたる。C 言語で実装されており、外部ランタイム依存ゼロ・シングルバイナリで動作する。

内部的には **レキサー → パーサー（Bison）→ バイトコードコンパイラ → スタックベース VM** というパイプラインを持ち、ユーザが書いたフィルタ式を解釈・実行する。単なるフィールド抽出から、`reduce`・`foreach`・ユーザ定義関数・モジュールシステムまで備えた関数型ミニ言語になっている。

### 何が嬉しいのか？（既存手段との比較）

| 比較対象 | jq の優位点 |
|---|---|
| **`grep` / `sed` / `awk`** | テキストの行指向処理では JSON の構造（ネスト・配列・型）を正しく扱えない。jq は JSON の意味構造を理解した上で操作できる |
| **Python / Ruby ワンライナー** | `python3 -c "import json; ..."` は起動が重く、記述が冗長。jq は `jq '.users[] | select(.age>30) | .name'` のように宣言的かつ短い |
| **`fx` / `jless` 等の TUI ツール** | インタラクティブ閲覧には便利だが、パイプラインに組み込むバッチ処理には不向き。jq は Unix パイプとの親和性が高い |
| **`yq` / `dasel` 等の類似 CLI** | jq は最も歴史が長くエコシステムが成熟。100 以上の組み込み関数、正規表現、ストリーミング解析（巨大 JSON 対応）、パス操作など機能が圧倒的に豊富 |

**要するに**：「シェルスクリプトやパイプラインの中で、JSON を構造的に正しく・短い記述で・高速に加工できる」のが最大の価値。

### 使うときの流れ

```
① インストール
   brew install jq          # macOS
   apt-get install jq       # Debian/Ubuntu
   docker run ghcr.io/jqlang/jq  # Docker

② 基本：フィールド抽出
   curl -s https://api.example.com/users | jq '.[0].name'

③ 配列のフィルタリング・変換
   cat data.json | jq '[.items[] | select(.price > 1000) | {name, price}]'

④ 集計・畳み込み
   jq '[.[] | .amount] | add' sales.json

⑤ 外部変数の注入
   jq --arg status "active" '.users[] | select(.status == $status)' db.json

⑥ 複雑な変換（ユーザ定義関数）
   jq 'def normalize: ascii_downcase | gsub("\\s+"; "_");
       .items | map(.name |= normalize)' input.json

⑦ パイプラインへの組み込み（実践例）
   kubectl get pods -o json \
     | jq -r '.items[] | select(.status.phase != "Running") | .metadata.name' \
     | xargs kubectl delete pod
```

**基本パターンは常に同じ**：`入力 JSON | jq 'フィルタ式'`。フィルタ式の中で `.field`（抽出）、`|`（パイプ）、`select()`（条件絞り込み）、`map()`（変換）を組み合わせるだけで、大半のユースケースに対応できる。より高度な処理が必要になったら `reduce`・`foreach`・`def` を使って関数型プログラミング的に拡張していく。
