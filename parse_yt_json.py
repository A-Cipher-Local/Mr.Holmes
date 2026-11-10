#!/usr/bin/env python3
import requests
import json
import re

def extract_channel_metadata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    print(f"[*] Requesting telemetry payload from: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            html = res.text
            match = re.search(r'var ytInitialData = ({.*?});</script>', html)
            if match:
                print("    [+] Successfully isolated ytInitialData JSON block.")
                data = json.loads(match.group(1))
                
                # Check multiple potential header renderer locations
                header = {}
                if "header" in data:
                    if "c4TabbedHeaderRenderer" in data["header"]:
                        header = data["header"]["c4TabbedHeaderRenderer"]
                    elif "pageHeaderRenderer" in data["header"]:
                        header = data["header"]["pageHeaderRenderer"]
                
                # Fallback to microformat metadata if header renderers miss
                meta = data.get("metadata", {}).get("channelMetadataRenderer", {})
                
                title = header.get("title") or meta.get("title", "N/A")
                channel_id = header.get("channelId") or meta.get("externalId", "N/A")
                subscribers = header.get("subscriberCountText", {}).get("simpleText", "N/A")
                
                print(f"\n--- Extracted Channel Telemetry ---")
                print(f"    Title        : {title}")
                print(f"    Channel ID   : {channel_id}")
                print(f"    Subscribers  : {subscribers}")
            else:
                print("    [-] ytInitialData script block not matched.")
        else:
            print(f"    [-] HTTP Error: {res.status_code}")
    except Exception as e:
        print(f"    [!] Error: {e}")

if __name__ == "__main__":
    extract_channel_metadata("https://www.youtube.com/@SirJosephPesci")
