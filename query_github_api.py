import urllib.request
import urllib.parse
import json
import ssl

QUERIES = ["stlawrenceparish", "DemonSmooch", "TammyBUsagi", "Hannaki", "lukege287@gmail.com"]

# Note: GitHub API requires a User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0",
    "Accept": "application/vnd.github.v3+json"
}

def main():
    print("[*] Querying GitHub Code and User APIs...")
    for q in QUERIES:
        encoded = urllib.parse.quote(q)
        url = f"https://api.github.com/search/code?q={encoded}"
        print(f"\n[*] Searching code for: {q}")
        
        req = urllib.request.Request(url, headers=headers)
        try:
            # Direct request (or configure proxy handler if routing via SOCKS5)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                total = data.get("total_count", 0)
                print(f"    -> Results found: {total}")
                for item in data.get("items", [])[:3]:
                    print(f"        - Repo: {item.get('repository', {}).get('full_name')} | File: {item.get('path')}")
        except Exception as e:
            print(f"    -> Error or rate-limited: {e}")

if __name__ == "__main__":
    main()
