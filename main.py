#!/usr/bin/env python3
"""GitHub Trend Summarizer - トレンドリポジトリを収集しサマリーを生成する"""

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import anthropic
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR / "workspace"
DOCS_DIR = BASE_DIR / "docs"
INDEX_MD = DOCS_DIR / "index.md"

TRENDING_URL = "https://github.com/trending"


def fetch_trending_repos():
    """GitHub Trending ページをスクレイピングしてリポジトリ情報を取得する"""
    resp = requests.get(TRENDING_URL, headers={"Accept-Language": "en-US,en;q=0.9"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    repos = []
    for article in soup.select("article.Box-row"):
        # owner/repo
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        full_name = h2.get("href", "").strip("/")  # "owner/repo"
        if "/" not in full_name:
            continue
        owner, repo = full_name.split("/", 1)

        # language
        lang_span = article.select_one("[itemprop='programmingLanguage']")
        language = lang_span.text.strip() if lang_span else ""

        # stars
        star_link = article.select_one("a[href$='/stargazers']")
        stars = star_link.text.strip().replace(",", "") if star_link else ""

        # description
        p = article.select_one("p")
        description = p.text.strip() if p else ""

        repos.append({
            "owner": owner.strip(),
            "repo": repo.strip(),
            "language": language,
            "stars": stars,
            "description": description,
        })

    return repos


def format_stars(stars_str):
    """star数を 1.2k のような表記にする"""
    if not stars_str:
        return "0"
    try:
        n = int(stars_str)
    except ValueError:
        return stars_str
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def download_repo(owner, repo):
    """tarball でリポジトリのソースを workspace/{repo}/ にダウンロードする"""
    dest = WORKSPACE_DIR / repo
    if dest.exists():
        return False  # already exists

    dest.mkdir(parents=True, exist_ok=True)

    # try main branch first, then master
    for branch in ["main", "master"]:
        url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.tar.gz"
        result = subprocess.run(
            ["curl", "-fsSL", url],
            capture_output=True,
        )
        if result.returncode == 0:
            tar_result = subprocess.run(
                ["tar", "-xz", "--strip-components=1", "-C", str(dest)],
                input=result.stdout,
                capture_output=True,
            )
            if tar_result.returncode == 0:
                print(f"  Downloaded: {owner}/{repo} ({branch})")
                return True

    # cleanup empty dir on failure
    if not any(dest.iterdir()):
        dest.rmdir()
    print(f"  Failed to download: {owner}/{repo}")
    return False


def collect_source_files(repo_dir, max_chars=50000):
    """サマリー生成用にソースファイルの内容を収集する"""
    content_parts = []
    total = 0

    # README を優先
    for name in ["README.md", "README.rst", "README.txt", "README"]:
        readme = repo_dir / name
        if readme.exists():
            text = readme.read_text(encoding="utf-8", errors="replace")
            content_parts.append(f"=== {name} ===\n{text}")
            total += len(text)
            break

    # その他の主要ファイルを収集
    extensions = {".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".cpp", ".h",
                  ".rb", ".php", ".swift", ".kt", ".scala", ".cs", ".toml", ".yaml",
                  ".yml", ".json", ".md"}
    for path in sorted(repo_dir.rglob("*")):
        if total >= max_chars:
            break
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        # skip large files and common non-essential dirs
        rel = path.relative_to(repo_dir)
        skip_dirs = {"node_modules", "vendor", "dist", "build", ".git", "__pycache__"}
        if any(part in skip_dirs for part in rel.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if len(text) > 10000:
            text = text[:10000] + "\n... (truncated)"
        content_parts.append(f"=== {rel} ===\n{text}")
        total += len(text)

    return "\n\n".join(content_parts)


def generate_summary(client, owner, repo, language, description, source_text):
    """Claude API でリポジトリのサマリーを生成する"""
    prompt = f"""以下は GitHub リポジトリ {owner}/{repo} のソースコードです。

リポジトリの説明: {description}
主要言語: {language}

{source_text}

---

以下の2つを生成してください:

1. **サマリー**: このリポジトリの詳細なサマリーを日本語の Markdown で書いてください。見出しはリポジトリ名にしてください。何ができるのか、どういう技術を使っているのか、どういう人に役立つのかを含めてください。

2. **メタ情報** (最後に以下のフォーマットで出力):
META_KEYWORDS: キーワード1, キーワード2, キーワード3
META_ONELINER: このリポジトリの端的な日本語の説明（1文）
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def parse_summary_response(response_text):
    """Claude の応答からサマリー本文とメタ情報を分離する"""
    lines = response_text.strip().split("\n")
    keywords = ""
    oneliner = ""
    summary_lines = []

    for line in lines:
        if line.startswith("META_KEYWORDS:"):
            keywords = line.replace("META_KEYWORDS:", "").strip()
        elif line.startswith("META_ONELINER:"):
            oneliner = line.replace("META_ONELINER:", "").strip()
        else:
            summary_lines.append(line)

    # 末尾の空行を除去
    while summary_lines and not summary_lines[-1].strip():
        summary_lines.pop()

    return "\n".join(summary_lines), keywords, oneliner


def save_summary(repo, summary_text):
    """サマリーを docs/{repo}.md に保存する"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = DOCS_DIR / f"{repo}.md"
    path.write_text(summary_text, encoding="utf-8")
    print(f"  Saved: {path}")


def update_index(today_str, entries):
    """docs/index.md を更新する（最新日付を先頭に prepend）

    entries: list of {"repo": str, "stars": str, "keywords": str, "oneliner": str}
    """
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 今日のセクションを生成
    new_lines = [f"# {today_str}", ""]
    for e in entries:
        stars = format_stars(e["stars"])
        line = f"- [{e['repo']}]({e['repo']}.md) ⭐{stars} {e['keywords']} {e['oneliner']}"
        new_lines.append(line)
    new_lines.append("")
    new_section = "\n".join(new_lines)

    # 既存の index.md を読み込み
    existing = ""
    if INDEX_MD.exists():
        existing = INDEX_MD.read_text(encoding="utf-8")

    # prepend
    updated = new_section + "\n" + existing if existing else new_section
    INDEX_MD.write_text(updated, encoding="utf-8")
    print(f"  Updated: {INDEX_MD}")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is required.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    today_str = date.today().isoformat()

    print(f"=== GitHub Trend Summarizer ({today_str}) ===\n")

    # 1. トレンド取得
    print("Fetching trending repositories...")
    repos = fetch_trending_repos()
    if not repos:
        print("No trending repositories found.")
        sys.exit(1)
    print(f"Found {len(repos)} repositories.\n")

    index_entries = []

    for i, info in enumerate(repos, 1):
        owner = info["owner"]
        repo = info["repo"]
        print(f"[{i}/{len(repos)}] {owner}/{repo}")

        already_exists = (WORKSPACE_DIR / repo).exists()

        # 2. ソース取得
        if not already_exists:
            downloaded = download_repo(owner, repo)
            if not downloaded:
                continue

        # 3. サマリー生成（既存ならスキップ）
        summary_md_path = DOCS_DIR / f"{repo}.md"
        if already_exists and summary_md_path.exists():
            print("  Already exists, skipping summary generation.")
            # 既存のメタ情報を読み込む（index用）
            keywords = info["language"] if info["language"] else ""
            oneliner = info["description"]
            index_entries.append({
                "repo": repo,
                "stars": info["stars"],
                "keywords": keywords,
                "oneliner": oneliner,
            })
            continue

        repo_dir = WORKSPACE_DIR / repo
        if not repo_dir.exists():
            continue

        print("  Collecting source files...")
        source_text = collect_source_files(repo_dir)

        print("  Generating summary with Claude API...")
        response = generate_summary(
            client, owner, repo,
            info["language"], info["description"], source_text,
        )
        summary, keywords, oneliner = parse_summary_response(response)

        # keywords が空ならトレンドページの情報で補完
        if not keywords and info["language"]:
            keywords = info["language"]
        if not oneliner and info["description"]:
            oneliner = info["description"]

        save_summary(repo, summary)

        index_entries.append({
            "repo": repo,
            "stars": info["stars"],
            "keywords": keywords,
            "oneliner": oneliner,
        })

    # 4. index.md 更新
    if index_entries:
        print(f"\nUpdating index.md with {len(index_entries)} entries...")
        update_index(today_str, index_entries)

    print("\nDone!")


if __name__ == "__main__":
    main()
