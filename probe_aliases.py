#!/usr/bin/env python3
import requests
import json

# Target CDX API for historical domain/handle footprints
CDX_API = "https://web.archive.org/cdx/search/cdx"

def check_cdx(url_query):
    params = {
        "url": url_query,
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "limit": 10
    }
    print(f"[*] Querying Wayback CDX for: {url_query}")
    try:
        res = requests.get(CDX_API, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if len(data) > 1:
                print(f"    [+] Found {len(data)-1} historical snapshots/redirects:")
                for row in data[1:]:
                    print(f"        - [{row[0]}] HTTP {row[2]} -> {row[1]}")
            else:
                print("    [-] No historical CDX records found for this exact path.")
    except Exception as e:
        print(f"    [!] Error: {e}")

def main():
    targets = [
        "youtube.com/@SirJosephPesci",
        "twitch.tv/sirjosephpesci",
        "twitter.com/SirJosephPesci"
    ]
    print("============================================================")
    print(" HISTORICAL ALIAS & CDX ARCHIVE PROBE")
    print("============================================================\n")
    for t in targets:
        check_cdx(t)
        print("-" * 50)

if __name__ == "__main__":
    main()
