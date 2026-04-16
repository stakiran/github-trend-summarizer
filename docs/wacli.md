---
url: https://github.com/steipete/wacli
keywords: WhatsApp, CLI, whatsmeow, Go, SQLite FTS5, sync, search, send, QRログイン, bot/automation
oneliner: WhatsApp Web プロトコル（whatsmeow）を土台に、メッセージのローカル同期・全文検索・送信・グループ管理までを 1 つの Go 製 CLI にまとめたサードパーティツール。
---

# wacli — WhatsApp CLI: sync, search, send

## このリポジトリは何？

`steipete/wacli` は、**WhatsApp を CLI から操作するためのサードパーティ製コマンドラインツール**。実装言語は Go（go 1.25）、認証と送受信のコアには `go.mau.fi/whatsmeow`（WhatsApp Web プロトコルの Go 実装）を採用し、ローカル永続化に SQLite、全文検索に **SQLite FTS5** を使う。CLI フレームワークは `spf13/cobra`、QR コード表示は `mdp/qrterminal` 。

主なユースケースは次の 4 つにフォーカスしている：

- **Best-effort なローカル履歴同期**（初期バックフィル＋常時追従）
- **オフラインでの高速メッセージ検索**（FTS5 ベースの `messages search`、スニペット出力、`--chat/--from/--after/--before/--type` などで絞り込み）
- **メッセージ / ファイル送信**（`send text`, `send file`、`--caption`, `--filename` でのファイル名上書き対応）
- **連絡先 / グループ管理**（一覧・リネーム・参加者追加/削除/昇格、招待リンク生成/失効、招待コードで参加、退出など）

保存先は既定で `~/.wacli`（`--store DIR` で変更可）。中身は `session.db`（whatsmeow のデバイスID/鍵）、`wacli.db`（メッセージ/チャット/FTS）、`media/`、`LOCK` で構成される。複数インスタンスの同時起動はデバイス置換事故を招くので、ストアディレクトリに排他ロックを取り fail-fast する設計。配布は Homebrew tap（`brew install steipete/tap/wacli`）または `go build -tags sqlite_fts5 ./cmd/wacli` でのローカルビルド。

## 既存手段との比較 — 何が嬉しい？

WhatsApp を自動化・検索したいときの既存手段は大きく 3 系統あり、それぞれ弱点がある：

| 手段 | 弱点 |
|---|---|
| 公式 WhatsApp Business API / Cloud API | 企業向け。個人番号で気軽に使えず、通常会話のバックフィルや検索は守備範囲外 |
| 公式アプリのエクスポート機能 | 1 チャットずつ手動、全文検索 DB にはならない、継続取り込みができない |
| `whatsmeow` 等の生ライブラリ自作 | コード必須。鍵管理、ロック、FTS、CLI UX まで全部自前 |
| `vicentereig/whatsapp-cli` ほか先行 CLI | 直接の着想元。`wacli` はここから学びつつ、「sync + search + send」の三本柱を明確化 |

`wacli` が嬉しいポイントは：

1. **個人の WhatsApp アカウントで動く**。QR ペアリング 1 回で Linked Device として接続し、以降は CLI / スクリプトから叩ける。
2. **人間向け表示とスクリプト向け `--json` が両立**。`jq` と組み合わせて全チャットを一括バックフィル、といった使い方が README にも例示されている。
3. **FTS5 による高速オフライン検索**。メディアのキャプション、ドキュメントのファイル名、リアクション/返信の表示テキストも検索対象に入る（v0.2.0）。
4. **安全なランタイム特性**：`auth` だけが対話（QR 表示）を行い、`sync` は QR を絶対に出さず未認証ならエラー終了。cron/デーモンに載せやすい。
5. **単一ディレクトリ `~/.wacli` にすべてが入る**ので、バックアップ・移行・隔離が容易。

要するに、**「公式 API に手が届かない個人ユーザが、自分の WhatsApp 履歴を grep でき、送信も自動化できる」**のが一番の価値。

## 使うときの流れ

1. **インストール**：`brew install steipete/tap/wacli`、もしくは `go build -tags sqlite_fts5 -o ./dist/wacli ./cmd/wacli`。`sqlite_fts5` タグを忘れると検索が LIKE フォールバックになり遅くなる。
2. **初回認証**：`wacli auth` を実行するとターミナルに QR が表示される。スマホの WhatsApp → 「リンク済みデバイス」で読み取り、成功後はそのまま初期（ブートストラップ）同期に入る。必要なら `WACLI_DEVICE_LABEL` / `WACLI_DEVICE_PLATFORM` で表示名やプラットフォームを上書き。
3. **継続同期**：`wacli sync --follow` を常駐させる（再接続は指数バックオフ）。scripts/systemd/tmux で走らせ、新着メッセージと WhatsApp が送ってくる履歴イベントを `wacli.db` に upsert し続ける。
4. **健全性確認**：`wacli doctor` で接続・ストア状態をチェック。
5. **古い履歴の取り寄せ**：`wacli history backfill --chat <JID> --requests 10 --count 50` を使うと、ローカル最古メッセージをアンカーに、**プライマリ端末（スマホ本体）がオンラインであることを前提に** best-effort で過去をもらいに行く。README には全チャットを回すワンライナー（`chats list --json | jq | while read`）も掲載。
6. **検索する**：`wacli messages search "meeting" --chat ... --after ...`。`--json` を付ければ構造化結果が得られる。
7. **送信する**：`wacli send text --to 1234567890 --message "hello"` / `wacli send file --to ... --file ./pic.jpg --caption "hi"`、必要に応じて `--filename report.pdf` で表示名を差し替え。
8. **連絡先・グループ管理**：`contacts search/show/alias`、`groups list/info/rename/participants add|remove|promote|demote`、`groups invite link get|revoke`、`groups join --code`、`groups leave` など。メディアは `media download --chat ... --id <msg-id>` で個別取得。

運用上のコツは **`auth` は対話 UI 前提の端末で 1 回だけ、以降は `sync --follow` をバックグラウンドに置き、検索・送信は別シェルから叩く**という役割分担。これが `wacli` の設計思想（対話コマンドと非対話コマンドの厳格な分離、ストア単一化とロック）に最もよく合う使い方になる。
