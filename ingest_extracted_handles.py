import json
import re
import sqlite3

DB_PATH = "GUI/Database/osint_intelligence.db"
TIMELINE_PATH = "GUI/Reports/universal_chronological_timeline.json"

def main():
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure indicators table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            indicator_type TEXT,
            indicator_value TEXT
        )
    """)

    inserted = 0
    for event in events:
        source = event.get("source_file", "TammyBUsagi_data_postings_80769774.csv.txt")
        text = str(event.get("context", ""))
        mentions = set(re.findall(r"@([A-Za-z0-9_]+)", text))
        
        for handle in mentions:
            val = handle.lower()
            if val not in ("youtube", "tammybusagi"):  # Skip self-references and platform tags
                cursor.execute(
                    "INSERT INTO indicators (source_file, indicator_type, indicator_value) VALUES (?, ?, ?)",
                    (source, "twitter_handle", f"@{val}")
                )
                inserted += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully registered {inserted} extracted target handle indicators into database.")

if __name__ == "__main__":
    main()
