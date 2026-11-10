#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime

DB_FILE = "investigations.db"
JSON_OUT = f"investigations_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

def export_json():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, target_alias, platform, indicator_type, value, confidence, timestamp FROM entities")
    rows = cur.fetchall()
    conn.close()
    
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "target_alias": r[1],
            "platform": r[2],
            "indicator_type": r[3],
            "value": r[4],
            "confidence": r[5],
            "timestamp": r[6]
        })
        
    with open(JSON_OUT, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"[+] Snapshot saved to {JSON_OUT}")

if __name__ == "__main__":
    export_json()
