import os
import json
import feedparser
import httpx
from datetime import datetime
from httpx_socks import SyncProxyTransport

# Configuration
PROXY_URL = "socks5://127.0.0.1:9050"
INGEST_DIR = "./ingest_queue"
STATE_FILE = ".rss_poller_state.json"

# Target Feeds (Add target channel RSS/Atom feeds here)
TARGET_FEEDS = [
    {
        "name": "Rain Renegades Spin-off Feed",
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=TARGET_CHANNEL_ID_HERE"
    }
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def poll_feeds():
    if not os.path.exists(INGEST_DIR):
        os.makedirs(INGEST_DIR)

    state = load_state()
    
    # Configure httpx client with SOCKS5 Tor transport
    transport = SyncProxyTransport.from_url(PROXY_URL)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

    print(f"[*] Initializing Tor-routed RSS sweep via {PROXY_URL}...")

    with httpx.Client(transport=transport, headers=headers, timeout=20.0) as client:
        for feed_info in TARGET_FEEDS:
            name = feed_info["name"]
            url = feed_info["url"]
            print(f"[*] Polling feed: {name} ({url})")
            
            try:
                response = client.get(url)
                if response.status_code != 200:
                    print(f"[-] Failed to fetch {url} | Status Code: {response.status_code}")
                    continue
                
                # Parse XML content using feedparser
                parsed_feed = feedparser.parse(response.content)
                last_seen_id = state.get(url, "")
                new_entries = []

                for entry in parsed_feed.entries:
                    entry_id = entry.get("id") or entry.get("link")
                    if entry_id == last_seen_id:
                        break  # Stop when we hit already ingested entries
                    
                    new_entries.append({
                        "video_id": entry.get("yt_videoid", entry_id.split(":")[-1]),
                        "upload_date": datetime.now().strftime("%Y-%m-%d"),
                        "title": entry.get("title", "Untitled"),
                        "description": entry.get("summary", "")
                    })

                if new_entries:
                    # Reverse so chronological order is preserved
                    new_entries.reverse()
                    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    queue_file = os.path.join(INGEST_DIR, f"rss_feed_{timestamp_str}.json")
                    
                    with open(queue_file, "w", encoding="utf-8") as f:
                        json.dump(new_entries, f, indent=2)
                    
                    print(f"[+] Queued {len(new_entries)} new items from {name} -> {queue_file}")
                    
                    # Update state with the latest entry ID
                    state[url] = parsed_feed.entries[0].get("id") or parsed_feed.entries[0].get("link")
                else:
                    print(f"[+] No new items found for {name}.")

            except Exception as e:
                print(f"[-] Error polling {name}: {str(e)}")

    save_state(state)
    print("[*] RSS poll sequence completed.")

if __name__ == "__main__":
    poll_feeds()
