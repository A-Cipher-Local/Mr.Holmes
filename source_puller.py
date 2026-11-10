#!/usr/bin/env python3
import urllib.request
import json

def fetch_file_content(repo, filepath):
    url = f"https://raw.githubusercontent.com/{repo}/main/{filepath}"
    print(f"[*] Fetching: {filepath} from {repo}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        # Try master branch fallback
        url_master = f"https://raw.githubusercontent.com/{repo}/master/{filepath}"
        try:
            req = urllib.request.Request(url_master, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")
        except Exception as err:
            print(f"[!] Failed to fetch {filepath}: {err}")
            return None

if __name__ == "__main__":
    repo = "HappyPunch/hp-reports"
    files = ["fxmanifest.lua", "sv_config.lua", "source/server.lua"]
    
    for f in files:
        content = fetch_file_content(repo, f)
        if content:
            print(f"\n--- [ FILE: {f} ] ---")
            print(content[:500] + ("...\n[Content Truncated]" if len(content) > 500 else ""))
