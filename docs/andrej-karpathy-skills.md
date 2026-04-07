---
url: https://github.com/forrestchang/andrej-karpathy-skills
keywords: Claude Code, CLAUDE.md, LLMコーディング品質, プロンプトガイドライン, Karpathy
oneliner: Andrej Karpathy が指摘した LLM コーディングの悪癖を矯正する Claude Code 向けガイドライン集。
---

## このリポジトリは何？

Andrej Karpathy が [X のポスト](https://x.com/karpathy/status/2015883857489522876)で指摘した「LLM にコードを書かせたときのよくある問題」を解決するための **Claude Code 用行動ガイドライン**。実体は `CLAUDE.md` というテキストファイル1枚で、Claude Code がコード生成時に従うべき **4 つの原則** を定義している。

| 原則 | 矯正する問題 |
|---|---|
| **Think Before Coding** — 仮定を明示し、不明点は質問する | 勝手に前提を決めて突っ走る |
| **Simplicity First** — 必要最小限のコードだけ書く | 過剰な抽象化・不要機能の作り込み |
| **Surgical Changes** — 依頼箇所だけを変更する | 関係ないコードの "ついで改善" |
| **Goal-Driven Execution** — 成功基準を定義しテストで検証する | 曖昧なまま実装してやり直し |

コードは一切含まれず、純粋に **プロンプトエンジニアリング資産（Markdown）** だけで構成されている。

## 何が嬉しいの？（既存手段との比較）

| 比較対象 | 違い |
|---|---|
| **自前で CLAUDE.md を書く** | Karpathy の知見を体系化済みなので、ゼロから書く手間が省ける。4 原則は汎用的で、そのままプロジェクト固有ルールと合成できる |
| **Cursor Rules / .cursorrules** | Cursor 専用だが、本リポジトリは Claude Code 専用。Plugin 形式で配布でき、全プロジェクト横断で適用可能 |
| **一般的な LLM プロンプトテンプレート** | 「コードを書かせる」場面に特化。diff の肥大化・過剰設計・勝手なリファクタといった **実務で頻発する具体的失敗パターン** に焦点を当てている |

最大の価値は、**LLM が出力するコードの "ノイズ" を減らせる**こと。不要な変更が減れば、レビュー負荷が下がり、手戻りも減る。

## 使うときの流れ

### 方法 A：Claude Code Plugin（推奨・全プロジェクト共通）

```bash
# 1. Claude Code 内でマーケットプレイスを追加
/plugin marketplace add forrestchang/andrej-karpathy-skills

# 2. プラグインをインストール
/plugin install andrej-karpathy-skills@karpathy-skills
```

これだけで、以後すべてのプロジェクトで 4 原則が自動的に適用される。

### 方法 B：CLAUDE.md を直接配置（プロジェクト単位）

```bash
# 新規プロジェクト → ファイルをダウンロード
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md

# 既存プロジェクト → 末尾に追記
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

その後は **普段通り Claude Code を使うだけ**。ガイドラインは Claude が自動で参照し、以下の変化が期待できる。

- diff に不要な変更が混ざらなくなる
- 曖昧な依頼に対して、実装前に確認質問が来るようになる
- コードが最初からシンプルになり、書き直しが減る

必要に応じて `## Project-Specific Guidelines` セクションを追記し、プロジェクト固有ルール（言語設定、テスト方針など）と組み合わせる。
