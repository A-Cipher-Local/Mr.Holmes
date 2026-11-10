import time
import json
from ddgs import DDGS

TARGETS = ["DramaAlert", "Keemstar", "HappyPunch"]
OUTPUT_FILE = "brand_dork_results.json"

DORK_TEMPLATES = [
    'intext:"{target}" filetype:pdf',
    'intitle:"{target}" (email OR contact)',
    'site:pastebin.com "{target}"',
    'site:github.com "{target}"',
    'inurl:"{target}"',
    '"{target}" contact email',
    '"{target}" press kit details'
]

def run_pivot_scan():
    all_results = {}
    print(f"[*] Initializing DuckDuckGo reconnaissance scan for targets: {TARGETS}\n")

    with DDGS() as ddgs:
        for target in TARGETS:
            print(f"\n[+] Target Pivot: {target}")
            all_results[target] = {}

            for template in DORK_TEMPLATES:
                query = template.format(target=target)
                print(f"  [>] Querying: {query}")

                try:
                    results = list(ddgs.text(query, max_results=5))
                    all_results[target][query] = results
                    print(f"      [+] Found {len(results)} hit(s)")
                except Exception as e:
                    print(f"      [-] Failed: {e}")
                    all_results[target][query] = []

                time.sleep(2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n[+] Pivot scan complete! Structured results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_pivot_scan()
