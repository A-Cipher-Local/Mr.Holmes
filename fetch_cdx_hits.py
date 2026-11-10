#!/usr/bin/env python3
import json
import time
import requests

TARGET_URLS = [
    "http://hikkipedia.com/",
    "https://hikkipedia.com/",
    "https://pastebin.com/u/DemonSmooch",
    "https://pastebin.com/u/smooch",
    "https://github.com/DemonSmooch"
]

WAYBACK_AVAIL_API = "https://archive.org/wayback/available"

def check_wayback_availability(target_url):
    params = {"url": target_url}
    headers = {"User-Agent": "ArchiveChecker/2.0"}
    print(f"[*] Checking Availability API for: {target_url}")
    try:
        response = requests.get(WAYBACK_AVAIL_API, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            snapshot = data.get("archived_snapshots", {}).get("closest", {})
            if snapshot and snapshot.get("available"):
                return {
                    "url": target_url,
                    "timestamp": snapshot.get("timestamp"),
                    "archive_url": snapshot.get("url")
                }
        print("    [-] No archived snapshot found via Availability API.")
        return None
    except Exception as e:
        print(f"    [!] Error checking {target_url}: {e}")
        return None

def main():
    results = []
    print("============================================================")
    print(" LIGHTWEIGHT WAYBACK AVAILABILITY CHECKER")
    print("============================================================\n")
    for url in TARGET_URLS:
        hit = check_wayback_availability(url)
        if hit:
            results.append(hit)
            print(f"    [+] FOUND SNAPSHOT: {hit['archive_url']}")
        time.sleep(1.0)
    
    output_file = "wayback_availability_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"\n[+] Scan complete. Saved {len(results)} valid records to {output_file}\n")

if __name__ == "__main__":
    main()
