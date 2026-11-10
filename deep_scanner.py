#!/usr/bin/env python3
import json
import urllib.request
import sys

def fetch_json(url):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def audit_repo(repo_slug):
    print(f"\n[*] Deep Scanning Repository: {repo_slug}")
    
    # 1. Fetch Commit History (looking for sensitive keywords or debug notes)
    commits_url = f"https://api.github.com/repos/{repo_slug}/commits?per_page=10"
    commits = fetch_json(commits_url)
    if isinstance(commits, list):
        print("  [+] Recent Commits:")
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            author = c.get("commit", {}).get("author", {}).get("name", "Unknown")
            print(f"      - [{author}]: {msg}")

    # 2. Fetch Repository Tree / Contents
    tree_url = f"https://api.github.com/repos/{repo_slug}/git/trees/main?recursive=1"
    tree_data = fetch_json(tree_url)
    if tree_data and "tree" in tree_data:
        print("  [+] Project File Structure:")
        for item in tree_data["tree"]:
            print(f"      - {item.get('path')} ({item.get('type')})")
    else:
        # Fallback to master branch if main fails
        tree_url_master = f"https://api.github.com/repos/{repo_slug}/git/trees/master?recursive=1"
        tree_data_master = fetch_json(tree_url_master)
        if tree_data_master and "tree" in tree_data_master:
            print("  [+] Project File Structure (master branch):")
            for item in tree_data_master["tree"]:
                print(f"      - {item.get('path')} ({item.get('type')})")

if __name__ == "__main__":
    targets = ["HappyPunch/hp-reports", "KeemStar58/mobile-app"]
    for t in targets:
        audit_repo(t)
