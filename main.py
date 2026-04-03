#!/usr/bin/env python3
"""GitHub Trend Summarizer - トレンドリポジトリを収集しサマリーを生成する"""

import subprocess
import sys
from datetime import date
from pathlib import Path

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


SYSTEM_PROMPT = """\
出力はMarkdownのみで、余計な前置きは不要です。

出力の先頭に、以下のフォーマットで YAML frontmatter を必ず付与すること。
---
url: リポジトリのURL
keywords: キーワード1, キーワード2, キーワード3
oneliner: このリポジトリの端的な日本語の説明（1文）
---
"""


def generate_summary_with_claude_cli(owner, repo, language, description, repo_dir):
    """claude CLI でリポジトリを自律探索させてサマリーを生成する"""
    user_prompt = f"""このディレクトリは GitHub リポジトリ {owner}/{repo} のソースコードです。

リポジトリのURL: https://github.com/{owner}/{repo}
リポジトリの説明: {description}
主要言語: {language}

自分でソースコードを探索して、以下を A4 一枚程度で整理して。

- このリポジトリは何？
- このリポジトリは何が嬉しいの？既存の似た手段と比較して。
- 使うときはどういう流れに沿う？
"""

    result = subprocess.run(
        ["claude", "-p", user_prompt, "--system-prompt", SYSTEM_PROMPT, "--max-turns", "10"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(repo_dir),
    )
    if result.returncode != 0:
        print(f"  claude CLI error: {result.stderr}")
        return None
    return result.stdout


def parse_summary_response(response_text):
    """Claude の応答から frontmatter とサマリー本文を分離する"""
    text = response_text.strip()
    keywords = ""
    oneliner = ""
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].strip()
            for line in frontmatter.strip().split("\n"):
                if line.startswith("keywords:"):
                    keywords = line.replace("keywords:", "").strip()
                elif line.startswith("oneliner:"):
                    oneliner = line.replace("oneliner:", "").strip()

    return body, keywords, oneliner


def save_summary(repo, summary_text):
    """サマリーを docs/{repo}.md に保存する"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = DOCS_DIR / f"{repo}.md"
    path.write_text(summary_text, encoding="utf-8")
    print(f"  Saved: {path}")


def update_index(today_str, entries):
    """docs/index.md を更新する（最新日付を先頭に prepend）

    entries: list of {"repo": str, "owner": str, "stars": str, "keywords": str, "oneliner": str}
    """
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 今日のセクションを生成
    new_lines = [f"# {today_str}", ""]
    for e in entries:
        stars = format_stars(e["stars"])
        url = f"https://github.com/{e['owner']}/{e['repo']}"
        line = f"- [{e['repo']}]({e['repo']}.md) [⭐{stars}]({url}) {e['keywords']} {e['oneliner']}"
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
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    today_str = date.today().isoformat()

    print(f"=== GitHub Trend Summarizer ({today_str}) ===\n")

    # 1. トレンド取得
    print("Fetching trending repositories...")
    repos = fetch_trending_repos()
    if not repos:
        print("No trending repositories found.")
        sys.exit(1)
    if limit:
        repos = repos[:limit]
    print(f"Processing {len(repos)} repositories.\n")

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
                "owner": owner,
                "stars": info["stars"],
                "keywords": keywords,
                "oneliner": oneliner,
            })
            continue

        repo_dir = WORKSPACE_DIR / repo
        if not repo_dir.exists():
            continue

        print("  Generating summary with claude CLI...")
        response = generate_summary_with_claude_cli(
            owner, repo,
            info["language"], info["description"], repo_dir,
        )
        if response is None:
            continue
        summary, keywords, oneliner = parse_summary_response(response)

        # keywords が空ならトレンドページの情報で補完
        if not keywords and info["language"]:
            keywords = info["language"]
        if not oneliner and info["description"]:
            oneliner = info["description"]

        save_summary(repo, response)

        index_entries.append({
            "repo": repo,
            "owner": owner,
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
