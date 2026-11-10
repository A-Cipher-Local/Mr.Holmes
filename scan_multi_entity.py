import sqlite3
import os

DB_PATH = "pesci_intelligence.db"

# Target entities to cross-reference
TARGET_ENTITIES = [
    "Boogie", "Keem", "Morning Star", "Nicholas DeOrio", 
    "Scooter", "Tammy", "Wonder Woman", "YoMama"
]

def scan_cooccurrences():
    if not os.path.exists(DB_PATH):
        print(f"[-] Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT rowid, video_id, title, COALESCE(description, '') FROM stream_archives;")
    rows = cursor.fetchall()
    conn.close()

    print("=== [PROJECT ARGUS] MULTI-ENTITY CO-OCCURRENCE AUDIT ===")
    multi_entity_hits = 0

    for r in rows:
        rowid, video_id, title, description = r[0], r[1], r[2], r[3]
        corpus = f"{title} {description}".lower()
        
        found_entities = []
        for entity in TARGET_ENTITIES:
            # Check case-insensitive substring match
            if entity.lower() in corpus:
                found_entities.append(entity)

        # Report episodes where 2 or more target entities appear
        if len(found_entities) >= 2:
            multi_entity_hits += 1
            print(f"\n[+] Co-Occurrence Detected (Row {rowid} | ID: {video_id})")
            print(f"    Title: {title}")
            print(f"    Matched Entities ({len(found_entities)}): {', '.join(found_entities)}")

    print(f"\n[+] Audit Complete. Total multi-entity episodes found: {multi_entity_hits}")

if __name__ == "__main__":
    scan_cooccurrences()
