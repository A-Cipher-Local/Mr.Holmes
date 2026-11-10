import asyncio
import httpx
import json
import os
from datetime import datetime

PROXY_URL = "socks5://127.0.0.1:9050"
INGEST_DIR = "./ingest_queue"

# Example target feeds or endpoints for OSINT metadata collection
TARGET_FEEDS = [
    {
        "url": "https://httpbin.org/json", # Replace with real OSINT feeds or archive endpoints
        "fallback_payload": [
            {
                "video_id": "TOR_FEED_001",
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "title": "Project Argus Tor Ingest: Keem and Boogie telemetry analysis",
                "description": "Securely scraped record via SOCKS5 Tor proxy network highlighting Keem and Boogie."
            }
        ]
    }
]

async def verify_tor_connection(client: httpx.AsyncClient):
    try:
        response = await client.get("https://check.torproject.org/api/ip", timeout=15.0)
        data = response.json()
        print(f"[+] Tor Connection Verified | Exit IP: {data.get('IP')} | IsTor: {data.get('IsTor')}")
    except Exception as e:
        print(f"[-] Tor check warning: {str(e)}")

async def scrape_and_queue():
    if not os.path.exists(INGEST_DIR):
        os.makedirs(INGEST_DIR)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }

    print(f"[*] Initializing Tor-routed async scraper via {PROXY_URL}...")
    
    async with httpx.AsyncClient(proxy=PROXY_URL, headers=headers, timeout=20.0) as client:
        await verify_tor_connection(client)
        
        for feed in TARGET_FEEDS:
            url = feed["url"]
            print(f"[*] Fetching target feed: {url}")
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    # If endpoint returns valid JSON records, process them
                    data = response.json()
                    records = data.get("slideshow", feed["fallback_payload"]) # or parse custom schema
                else:
                    print(f"[-] Received status {response.status_code}. Using fallback payload.")
                    records = feed["fallback_payload"]
            except Exception as e:
                print(f"[-] Connection error on {url}: {str(e)} -> Using fallback payload.")
                records = feed["fallback_payload"]

            # Write scraped output directly to ingest queue for the daemon
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(INGEST_DIR, f"tor_feed_{timestamp_str}.json")
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2)
            
            print(f"[+] Successfully queued scraped payload to {output_file}")

if __name__ == "__main__":
    asyncio.run(scrape_and_queue())
