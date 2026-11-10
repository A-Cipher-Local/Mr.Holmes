import json
import os

INGEST_DIR = "./ingest_queue"
TEST_FILE = os.path.join(INGEST_DIR, "test_full_pipeline_feed.json")

# Payload featuring multiple target entities (Morning Star and Scooter)
test_payload = [
    {
        "video_id": "TEST_ID_002",
        "upload_date": "2026-11-09",
        "title": "Beyond The Pit Emergency: Morning Star responds to Scooter",
        "description": "An emergency telemetry archive capturing the direct exchange between Morning Star and Scooter."
    }
]

if not os.path.exists(INGEST_DIR):
    os.makedirs(INGEST_DIR)

with open(TEST_FILE, "w", encoding="utf-8") as f:
    json.dump(test_payload, f, indent=2)

print(f"[+] Dropped full-pipeline test payload into {TEST_FILE}")
