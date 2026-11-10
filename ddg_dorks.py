import time
import json
from ddgs import DDGS

INPUT_FILE = "extracted_dorks.txt"
OUTPUT_FILE = "dork_results.json"

def clean_dork_query(url_or_dork):
    """Converts standard Google search URLs back into raw dork text queries if needed."""
    if "google.com/search?q=" in url_or_dork:
        query = url_or_dork.split("google.com/search?q=")[-1]
        import urllib.parse
        return urllib.parse.unquote(query)
    return url_or_dork

def run_dorks():
    try:
        with open(INPUT_FILE, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: {INPUT_FILE} not found.")
        return

    all_results = {}
    print(f"[*] Starting search for {len(lines)} dork queries...\n")

    with DDGS() as ddgs:
        for idx, item in enumerate(lines, 1):
            query = clean_dork_query(item)
            print(f"[{idx}/{len(lines)}] Querying: {query}")

            try:
                results = list(ddgs.text(query, max_results=5))
                all_results[query] = results
                print(f"    [+] Found {len(results)} hit(s)")
            except Exception as e:
                print(f"    [-] Failed: {e}")
                all_results[query] = []

            time.sleep(2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n[+] Processing complete! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_dorks()
