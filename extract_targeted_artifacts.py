import urllib.request
import urllib.parse
import json
import base64
import os
import time

<<<<<<< HEAD
TOKEN = "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"
=======
TOKEN = "YOUR_GITHUB_TOKEN"
>>>>>>> 39f90d6 (chore: sanitize hardcoded tokens and update core OSINT modules)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0",
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {TOKEN}"
}

# Focus on high-confidence, low-noise targets to pull exact files
TARGET_FILES = [
    {"target": "DemonSmooch", "repo": "dylandoamaral/pokinder", "query": "DemonSmooch"},
    {"target": "TammyBUsagi", "repo": "shenjunfei/columbia", "query": "TammyBUsagi"},
    {"target": "stlawrenceparish", "repo": "whosonfirst-data/whosonfirst-data-venue-us-oh", "query": "stlawrenceparish"},
    {"target": "lukege287", "repo": "Lucksi/Mr.Holmes", "query": "lukege287"}
]

os.makedirs("GUI/Reports/github_extractions", exist_ok=True)

def fetch_file_content(repo, path):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode())
            if "content" in data:
                return base64.b64decode(data["content"]).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    [-] Failed to fetch {path} from {repo}: {e}")
    return None

def main():
    print("[*] Starting targeted artifact extraction...")
    for item_spec in TARGET_FILES:
        target = item_spec["target"]
        repo = item_spec["repo"]
        query = item_spec["query"]
        
        print(f"\n[*] Searching target '{target}' in repo '{repo}'...")
        search_url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}+repo:{repo}"
        
        req = urllib.request.Request(search_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                result = json.loads(resp.read().decode())
                for item in result.get("items", []):
                    path = item.get("path")
                    print(f"    -> Found matching file path: {path}")
                    content = fetch_file_content(repo, path)
                    if content:
                        filename = f"GUI/Reports/github_extractions/{target}_{path.replace('/', '_')}.txt"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"    [+] Successfully saved extracted content to {filename}")
        except urllib.error.HTTPError as e:
            print(f"    [-] HTTP Error {e.code} for {target}: {e.reason}")
        except Exception as e:
            print(f"    [-] Error for {target}: {e}")
        
        time.sleep(3)

if __name__ == "__main__":
    main()
