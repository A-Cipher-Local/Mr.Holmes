import json

with open("brand_dork_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("[*] Filtering for GitHub, Gist, and Code Artifacts:\n")
for target, queries in data.items():
    for q, results in queries.items():
        for r in results:
            url = r.get("href", "")
            if "github.com" in url or "gist.github.com" in url or "pastebin.com" in url:
                print(f"[{target}] {url}")
                print(f"    Title: {r.get('title')}")
                print(f"    Snippet: {r.get('body', '')[:100]}...\n")
