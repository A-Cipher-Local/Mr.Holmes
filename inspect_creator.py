import sqlite3
import re

DB_PATH = "GUI/Database/osint_intelligence.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Search for creator/author lines or email references across all stored artifacts
cursor.execute("SELECT source_file, content FROM artifacts WHERE content LIKE '%lukege287%' OR content LIKE '%Luca Garofalo%'")
rows = cursor.fetchall()
conn.close()

print(f"[*] Found {len(rows)} artifact matches for creator signature 'lukege287' / 'Luca Garofalo':\n")
for source, content in rows:
    print(f"File: {source}")
    for line in content.splitlines():
        if "lukege287" in line.lower() or "luca" in line.lower() or "copyright" in line.lower() or "author" in line.lower():
            print(f"  -> {line.strip()}")
    print("-" * 40)
