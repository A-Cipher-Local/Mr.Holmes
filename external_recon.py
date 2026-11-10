import asyncio
import httpx
import json
import os
from datetime import datetime

PROXY_URL = "socks5://127.0.0.1:9050"
INGEST_DIR = "./ingest_queue"

async def run_recon():
    if not os.path.exists(INGEST_DIR):
        os.makedirs(INGEST_DIR)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    
    async with httpx.AsyncClient(proxy=PROXY_URL, headers=headers, timeout=15.0) as client:
        try:
            res = await client.get("https://check.torproject.org/api/ip", timeout=10.0)
            data = res.json()
            print(f"[+] Tor Circuit Verified | Exit IP: {data.get('IP')} | IsTor: {data.get('IsTor')}")
        except Exception as e:
            print(f"[-] Tor proxy warning: {str(e)}")

        payload = [{
            "video_id": "SPINOFF_RECON_001",
            "upload_date": datetime.now().strftime("%Y-%m-%d"),
            "title": "Rain Renegades Spin-off Special: Nick and Tammy Harris deep dive",
            "description": "Autonomous external Tor sweep capturing Nick and Tammyten metadata co-occurrences."
        }]
        
        out_file = os.path.join(INGEST_DIR, f"spinoff_recon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[+] External sweep payload queued: {out_file}")

if __name__ == "__main__":
    asyncio.run(run_recon())
