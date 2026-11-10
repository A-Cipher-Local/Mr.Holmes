import sqlite3
import json

DB_PATH = "pesci_intelligence.db"
TARGETS = ["Nicholas", "Keem", "Scooter", "Morning Star", "Boogie", "Tammy", "Wonder Woman", "YoMama"]

def run_batch_audit():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    summary = {}
    for target in TARGETS:
        cursor.execute("""
            SELECT video_id, title 
            FROM stream_fts 
            WHERE stream_fts MATCH ?;
        """, (target,))
        rows = cursor.fetchall()
        summary[target] = [{"video_id": r[0], "title": r[1]} for r in rows]

    conn.close()
    print("=== TARGET ENTITY HIT MATRIX ===")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    run_batch_audit()
