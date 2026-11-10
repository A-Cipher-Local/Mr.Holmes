import json
import os

INGEST_DIR = "./ingest_queue"
TEST_FILE = os.path.join(INGEST_DIR, "test_stream_feed.json")

test_payload = [
    {
        "video_id": "TEST_ID_001",
        "upload_date": "2026-11-09",
        "title": "Beyond The Pit Test Ep.99: Keem and Boogie emergency breakdown",
        "description": "An emergency breakdown featuring Keem and Boogie discussing current events."
    }
]

if not os.path.exists(INGEST_DIR):
    os.makedirs(INGEST_DIR)

with open(TEST_FILE, "w", encoding="utf-8") as f:
    json.dump(test_payload, f, indent=2)

print(f"[+] Successfully dropped test payload into {TEST_FILE}")
