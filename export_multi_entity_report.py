import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "pesci_intelligence.db"
OUTPUT_JSON = "multi_entity_report.json"

TARGET_ENTITIES = [
    "Boogie", "Keem", "Morning Star", "Nicholas DeOrio", 
    "Scooter", "Tammy", "Wonder Woman", "YoMama"
]

def generate_report():
    if not os.path.exists(DB_PATH):
        print(f"[-] Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT rowid, video_id, upload_date, title, COALESCE(description, '') FROM stream_archives;")
    rows = cursor.fetchall()
    conn.close()

    cooccurrences = []

    for r in rows:
        rowid, video_id, upload_date, title, description = r[0], r[1], r[2], r[3], r[4]
        corpus = f"{title} {description}".lower()
        
        found_entities = [entity for entity in TARGET_ENTITIES if entity.lower() in corpus]

        if len(found_entities) >= 2:
            cooccurrences.append({
                "rowid": rowid,
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "upload_date": upload_date if upload_date else "N/A",
                "title": title,
                "matched_entity_count": len(found_entities),
                "matched_entities": found_entities
            })

    report_payload = {
        "project": "PROJECT ARGUS",
        "report_type": "Multi-Entity Co-Occurrence Audit",
        "generated_timestamp": datetime.now().isoformat(),
        "total_multi_entity_nodes": len(cooccurrences),
        "results": cooccurrences
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    print(f"[+] Successfully generated structured report: {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_report()
