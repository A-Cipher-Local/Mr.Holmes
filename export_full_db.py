import sqlite3
import json

DB_PATH = "pesci_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT rowid, video_id, upload_date, title, COALESCE(description, ''), COALESCE(transcript, '') FROM stream_archives ORDER BY rowid ASC;")
rows = cursor.fetchall()
conn.close()

archive_data = []
for r in rows:
    archive_data.append({
        "rowid": r[0],
        "video_id": r[1],
        "upload_date": r[2] if r[2] else None,
        "title": r[3],
        "description": r[4],
        "transcript": r[5] if r[5] else None,
        "url": f"https://www.youtube.com/watch?v={r[1]}"
    })

payload = {
    "project": "PROJECT ARGUS",
    "total_records": len(archive_data),
    "records": archive_data
}

with open("pesci_intelligence_full_dump.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print(f"[+] Successfully exported {len(archive_data)} records to pesci_intelligence_full_dump.json")
