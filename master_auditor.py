#!/usr/bin/env python3
import json
import os
import urllib.request
import datetime

DOSSIER_FILE = "master_intel_dossier.json"

def load_dossier():
    print(f"[*] Loading {DOSSIER_FILE}...")
    if not os.path.exists(DOSSIER_FILE):
        print(f"[!] Error: {DOSSIER_FILE} not found in current directory.")
        return None
    
    with open(DOSSIER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def query_github_repo(repo_slug):
    url = f"https://api.github.com/repos/{repo_slug}/contributors"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json"
    }
    print(f"[*] Querying GitHub API for: {repo_slug}")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            contributors = json.loads(response.read().decode("utf-8"))
            return [c.get("login") for c in contributors]
    except Exception as e:
        return f"Error or rate-limited: {str(e)}"

def main():
    print("==========================================")
    print("   MASTER INTELLIGENCE AUDIT PIPELINE     ")
    print("==========================================")
    
    dossier = load_dossier()
    if not dossier:
        return

    print(f"[+] Dossier Timestamp: {dossier.get('timestamp', 'Unknown')}")
    print(f"[+] Targets Loaded: {len(dossier.get('targets', {}))}")

    # Repositories to audit
    repos = ["HappyPunch/hp-reports", "KeemStar58/mobile-app"]
    audit_results = {}

    for repo in repos:
        audit_results[repo] = query_github_repo(repo)

    # Update dossier actionable assets
    dossier.setdefault("actionable_assets", {})["live_github_audit"] = audit_results

    # Save back out
    with open(DOSSIER_FILE, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=4)

    print(f"[+] Audit complete. Updated dossier saved to {DOSSIER_FILE}")
    print("==========================================")

if __name__ == "__main__":
    main()
