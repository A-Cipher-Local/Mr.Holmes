import urllib.request
import json
import os
import datetime

print("[*] Initializing comprehensive intelligence extraction and compilation pipeline...\n")

master_dossier = {
    "timestamp": datetime.datetime.now().isoformat(),
    "targets": {},
    "actionable_assets": {}
}

# 1. Target Footprint Consolidation from brand_dork_results.json
if os.path.exists("brand_dork_results.json"):
    with open("brand_dork_results.json", "r", encoding="utf-8") as f:
        master_dossier["targets"] = json.load(f)
    print("[+] Loaded brand_dork_results.json into master dossier.")

# 2. GitHub Contributor / Repo Deep Scan (HappyPunch & KeemStar)
repos_to_check = [
    "HappyPunch/hp-reports",
    "KeemStar58/mobile-app"
]

github_findings = {}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github.v3+json"
}

for repo in repos_to_check:
    url = f"https://api.github.com/repos/{repo}/contributors"
    print(f"[*] Querying GitHub API for repository: {repo}")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            contributors = json.loads(response.read().decode("utf-8"))
            github_findings[repo] = [c.get("login") for c in contributors]
    except Exception as e:
        github_findings[repo] = f"Error or rate-limited: {str(e)}"

master_dossier["actionable_assets"]["github_contributors"] = github_findings

# 3. Save Master Dossier
output_filename = "master_intel_dossier.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(master_dossier, f, indent=4)

print(f"\n[+] Comprehensive pipeline complete! Master dossier compiled and saved to {output_filename}")
