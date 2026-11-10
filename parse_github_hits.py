import urllib.request
import urllib.parse
json
import os
import json

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

TARGETS = {
    "DemonSmooch": "dylandoamaral/pokinder",
    "stlawrenceparish": "whosonfirst-data/whosonfirst-data-venue-us-oh"
}

os.makedirs("GUI/Reports/github_extractions", exist_ok=True)

def fetch_file_content(repo, path):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode())
            # GitHub returns base64 encoded content for file requests
            if "content" in data:
                import base64
                return base64.b64decode(data["content"]).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    [-] Failed to fetch {path} from {repo}: {e}")
    return None

def main():
    print("[*] Pulling target artifact details...")
    for target, repo in TARGETS.items():
        print(f"\n[*] Inspecting target '{target}' in repo '{repo}'...")
        search_url = f"https://api.github.com/search/code?q={urllib.parse.quote(target)}+repo:{repo}"
        req = urllib.request.Request(search_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                result = json.loads(resp.read().decode())
                for item in result.get("items", []):
                    path = item.get("path")
                    print(f"    -> Found match at path: {path}")
                    content = fetch_file_content(repo, path)
                    if content:
                        filename = f"GUI/Reports/github_extractions/{target}_{path.replace('/', '_')}.txt"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"    [+] Saved extracted content to {filename}")
        except Exception as e:
            print(f"    [-] Search error for {target}: {e}")

if __name__ == "__main__":
    main()
