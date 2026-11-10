import urllib.request
import urllib.parse
import json

QUERIES = ["stlawrenceparish", "DemonSmooch", "TammyBUsagi", "Hannaki", "lukege287@gmail.com"]

# Embedded token directly in the script
TOKEN = "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"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0",
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {TOKEN}"
}

def main():
    print("[*] Querying GitHub Code Search API with embedded token...")
    for q in QUERIES:
        encoded = urllib.parse.quote(q)
        url = f"https://api.github.com/search/code?q={encoded}"
        print(f"\n[*] Searching code for: {q}")
        
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                data = json.loads(response.read().decode())
                total = data.get("total_count", 0)
                print(f"    -> Results found: {total}")
                for item in data.get("items", [])[:3]:
                    repo = item.get('repository', {}).get('full_name', 'N/A')
                    path = item.get('path', 'N/A')
                    print(f"        - Repo: {repo} | File: {path}")
        except urllib.error.HTTPError as e:
            print(f"    -> HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            print(f"    -> Error: {e}")

if __name__ == "__main__":
    main()
