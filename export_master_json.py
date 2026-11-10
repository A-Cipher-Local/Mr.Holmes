import sqlite3
import json
import re

DB_PATH = "pesci_intelligence.db"
OUTPUT_JSON = "pesci_intelligence_master.json"

TARGET_ENTITIES = [
    "Boogie", "Keem", "Morning Star", "Nicholas DeOrio", 
    "Scooter", "Tammy", "Wonder Woman", "YoMama"
]

def generate_master_payload():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT video_id, COALESCE(upload_date, 'N/A'), title, COALESCE(description, '') FROM stream_archives ORDER BY rowid ASC;")
    rows = cursor.fetchall()
    conn.close()

    archives = []
    entity_co_occurrences = []

    for idx, (vid, date, title, desc) in enumerate(rows, 1):
        # Extract tagged entities
        text = f"{title} {desc}".lower()
        tagged = [e for e in TARGET_ENTITIES if e.lower() in text]
        
        # Determine episode type
        if "½" in title or ".5" in title:
            ep_type = "fractional"
        elif re.search(r'ep\.?\s*\d+', title, re.IGNORECASE):
            ep_type = "standard"
        else:
            ep_type = "unindexed"

        item = {
            "index": idx,
            "video_id": vid,
            "upload_date": date,
            "title": title,
            "episode_type": ep_type,
            "tagged_entities": tagged,
            "url": f"https://www.youtube.com/watch?v={vid}"
        }
        archives.append(item)

        if len(tagged) > 1:
            entity_co_occurrences.append({
                "video_id": vid,
                "title": title,
                "entities": tagged
            })

    master_payload = {
        "project": "PROJECT ARGUS",
        "target_series": "Beyond The Pit",
        "total_verified_archives": len(archives),
        "co_occurrence_count": len(entity_co_occurrences),
        "co_occurrences": entity_co_occurrences,
        "archives": archives
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=2)

    print(f"[+] Exported {len(archives)} records into {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_master_payload()
