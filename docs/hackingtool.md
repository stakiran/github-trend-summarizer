---
url: https://github.com/Z4nzu/hackingtool
keywords: ペネトレーションテスト, ハッキングツール統合, セキュリティ診断
oneliner: 185以上のペネトレーションテストツールをカテゴリ別メニューから一括インストール・起動できるオールインワンハッキングツールランチャー。
---

# Z4nzu/hackingtool — リポジトリ概要

## このリポジトリは何？

**ペネトレーションテスト用ツール群を一元管理する「メタツール（ランチャー）」。**

185以上の著名なオープンソースセキュリティツールを20カテゴリに整理し、TUIメニューから選択するだけでインストール・起動・アップデートができる。Python 3.10+ で実装されており、Linux（Kali / Parrot 含む）と macOS に対応。依存パッケージは `rich` のみで軽量。

**20カテゴリの例：**

| カテゴリ | 代表ツール |
|---|---|
| 情報収集 | Nmap, Amass, TheHarvester, RustScan |
| Webアタック | Nuclei, ffuf, Nikto, OWASP ZAP |
| フィッシング | Evilginx3, HiddenEye, Gophish |
| Active Directory | BloodHound, Impacket, Certipy |
| クラウドセキュリティ | Prowler, Pacu, Trivy |
| ワイヤレス | Aircrack-ng 系 13ツール |

---

## 何が嬉しいの？既存の似た手段と比較して

### 既存の手段
- **Kali Linux / Parrot OS** ── 多くのツールが最初からインストール済みだが、ディスク使用量が大きく、都度 `apt install` で個別管理が必要。
- **GitHub スター管理 / 手動 clone** ── ツールごとにインストール手順が異なり、更新も手動。初学者には敷居が高い。
- **Metasploit Framework 単体** ── 強力だが exploit 系に特化しており、OSINT・フォレンジック・クラウド診断等はカバー外。

### hackingtool の優位点

1. **ゼロ知識で即起動** ── `curl ... | sudo bash` の一行で環境構築完了。ツールごとの依存関係は自動解決。
2. **インストール状態の可視化** ── メニューに ✔/✘ が表示され、何が入っているか一目で把握できる。
3. **検索・タグ・レコメンド機能** ── `/nmap` で即検索、`t` でタグ絞り込み、`r` で「ネットワークをスキャンしたい」などのユースケースからツールを提案。
4. **スマートアップデート** ── git clone / pip / go install / gem それぞれのインストール方法を自動検出して適切なアップデートコマンドを実行。
5. **Docker 対応** ── ホスト環境を汚さずに利用可能。

---

## 使うときの流れ

```
① インストール（初回のみ）
   curl -sSL https://raw.githubusercontent.com/Z4nzu/hackingtool/master/install.sh | sudo bash

② 起動
   hackingtool
   # → ASCII バナー + システム情報 + 20カテゴリのグリッドメニューが表示される

③-A カテゴリから選ぶ場合
   番号を入力 → サブメニューへ → ツール番号を入力
   → [I]nstall / [R]un / [U]pdate / open folder など選択

③-B ツール名で検索する場合
   /nmap  と入力 → 候補テーブルが表示 → 番号を選んで操作

③-C ユースケースからツールを探す場合
   r  と入力 → 「scan a network」「crack passwords」等のシナリオ一覧 → 選択

④ カテゴリ一括インストール
   サブメニューで 97 → 現在のカテゴリの全ツールを自動インストール

⑤ 終了
   q  または 99（一つ上に戻る）
```

> **注意:** ペネトレーションテストは許可されたシステムに対してのみ実施すること。本ツールの使用には利用者自身が法的責任を負う。
