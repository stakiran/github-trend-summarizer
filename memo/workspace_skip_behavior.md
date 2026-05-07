# workspace のフォルダだけ残して中身を消した場合のスキップ挙動

## 背景
ローカル容量削減のため `workspace/{repo}/` の中身は消したいが、フォルダ自体は残しておけば「処理済み」とみなしてスキップしてくれるかが知りたかった。

## 結論
**空フォルダだけ残しておけば、ダウンロードもサマリー生成もスキップされる。** 中身を削除して問題なし。

## 現在の判定ロジック（main.py）

スキップ判定はフォルダの「存在」のみを見ており、中身の有無は別の箇所で弾く構造になっている。

### 1. ダウンロードのスキップ（main.py:248, 251-254）
```python
already_exists = (WORKSPACE_DIR / repo).exists()
...
if not already_exists:
    downloaded = download_repo(owner, repo)
```
→ 空フォルダでも `exists()` は True。ダウンロードは走らない。

### 2. サマリー生成のスキップ（2 段ガード）

**段 1**: main.py:258-270
```python
if already_exists and summary_md_path.exists():
    print("  Already exists, skipping summary generation.")
    # index には trending ページの情報で entry を追加
    continue
```
→ `docs/{repo}.md` があれば即 continue。claude CLI は呼ばれない。

**段 2**: main.py:273-275
```python
if not repo_dir.exists() or not any(repo_dir.iterdir()):
    print(f"  Skipping: {repo_dir} is empty or missing.")
    continue
```
→ `docs/{repo}.md` が無くても、フォルダが空なら弾かれる。空フォルダが claude CLI に渡って無駄な探索をする事故は起きない。

## 状態別の挙動表

| workspace/{repo}/ | docs/{repo}.md | DL | サマリー生成 | index への追加 |
|---|---|---|---|---|
| 中身あり | 有 | skip | skip | される（trending 情報） |
| 空フォルダ | 有 | skip | skip | される（trending 情報） |
| 空フォルダ | 無 | skip | skip | されない |
| 無し | 無 | 実行 | 実行 | される |

## 運用メモ
- 容量が厳しくなったら `workspace/{repo}/` の中身だけ消して空フォルダを残す運用で OK。
- ただし `docs/{repo}.md` も消してしまうと「空フォルダ + サマリー無し」になり、その日の index にも entry が出ない。サマリーは残すこと。
