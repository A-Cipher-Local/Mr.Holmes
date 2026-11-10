import os
import json
import subprocess
import urllib.parse
import re

QUERIES = [
    "stlawrenceparish",
    "DemonSmooch Montreal",
    "TammyBUsagi Canada",
    "Hannaki DemonSmooch",
    "site:stlawrenceparish"
]

PROXY = "socks5h://127.0.0.1:9050"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def main():
    print(f"[*] Querying DuckDuckGo HTML via Tor proxy: {PROXY}")
    results = {}

    for q in QUERIES:
        encoded_q = urllib.parse.quote(q)
        url = f"https://html.duckduckgo.com/html/?q={encoded_q}"
        print(f"[*] Probing vector: {q}")

        cmd = [
            "curl", "--socks5-hostname", "127.0.0.1:9050",
            "-s", "-L",
            "-A", USER_AGENT,
            "--max-time", "15",
            url
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=18)
            if res.returncode != 0:
                print(f"    -> Curl failed with code {res.returncode}")
                continue

            html = res.stdout
            # Simple regex to extract result snippets or links from DDG HTML
            # Look for class 'result__snippet' and 'result__url'
            snippets = re.findall(r'class="result__snippet[^"]*">(.*?)<\/a>', html, re.DOTALL)
            clean_snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets]

            print(f"    -> Found {len(clean_snippets)} result snippets.")
            results[q] = clean_snippets[:5] # Store top 5 snippets per query

        except Exception as e:
            print(f"    -> Error executing probe: {e}")

    os.makedirs("GUI/Reports", exist_ok=True, mode=0o755)
    out_path = "GUI/Reports/ddg_tor_probe_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n[+] Probe complete. Results saved to {out_path}")

if __name__ == "__main__":
    main()
