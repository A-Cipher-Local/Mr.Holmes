#!/usr/bin/env python3
import json
import urllib.request

def fetch_json(url):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def analyze_user(username):
    print(f"\n[*] Analyzing User / Org Profile: {username}")
    
    # Fetch user public repositories
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=20"
    repos = fetch_json(repos_url)
    
    if isinstance(repos, list):
        print(f"  [+] Found {len(repos)} public repositories:")
        for r in repos:
            name = r.get("name")
            is_fork = r.get("fork")
            language = r.get("language")
            desc = r.get("description")
            print(f"      - {name} [Fork: {is_fork}] [Lang: {language}]")
            if desc:
                print(f"        Desc: {desc}")

if __name__ == "__main__":
    users = ["breezythedev", "KeemStar58"]
    for u in users:
        analyze_user(u)
