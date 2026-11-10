import asyncio
import httpx
import json
import os
from datetime import datetime

PROXY_URL = "socks5://127.0.0.1:9050"
INGEST_DIR = "./ingest_queue"

async def verify_identity():
    if not os.path.exists(INGEST_DIR):
        os.makedirs(INGEST_DIR)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    
    async with httpx.AsyncClient(proxy=PROXY_URL, headers=headers, timeout=15.0) as client:
        try:
            res = await client.get("https://check.torproject.org/api/ip", timeout=10.0)
            data = res.json()
            print(f"[+] Tor Circuit Active | Exit IP: {data.get('IP')} | IsTor: {data.get('IsTor')}")
        except Exception as e:
            print(f"[-] Tor proxy warning: {str(e)}")

        # Queue verification telemetry payload for daemon ingestion
        payload = [{
            "video_id": "VERIFY_TAMMY_NICK_001",
            "upload_date": datetime.now().strftime("%Y-%m-%d"),
            "title": "Rain Renegades Deep Verification: Tammy Harris and Nick Co-occurrence Check",
            "description": "Automated Tor-routed OSINT sweep cross-referencing alias Tammyten with legal/public identity records."
        }]
        
        out_file = os.path.join(INGEST_DIR, f"verify_sweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[+] Verification payload queued: {out_file}")

if __name__ == "__main__":
    asyncio.run(verify_identity())
