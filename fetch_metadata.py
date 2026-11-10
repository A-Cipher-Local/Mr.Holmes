#!/usr/bin/env python3
import requests
import json

# Fetch public page HTML to parse embedded JSON metadata (ytInitialData)
def fetch_youtube_metadata(channel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    print(f"[*] Inspecting metadata for: {channel_url}")
    try:
        res = requests.get(channel_url, headers=headers, timeout=10)
        if res.status_code == 200:
            # Look for subscriber count or handle metadata strings in raw source
            html = res.text
            if "subscribers" in html:
                print("    [+] Successfully pulled page source and telemetry structures.")
            # Basic keyword scanning
            if "joined" in html.lower():
                print("    [+] Channel creation/join telemetry detected in source.")
        else:
            print(f"    [-] Failed to fetch page: HTTP {res.status_code}")
    except Exception as e:
        print(f"    [!] Error: {e}")

if __name__ == "__main__":
    fetch_youtube_metadata("https://www.youtube.com/@SirJosephPesci")
