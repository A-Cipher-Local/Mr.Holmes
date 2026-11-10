import sqlite3
import json
import os

DB_PATH = "GUI/Database/osint_intelligence.db"
PATTERN_REPORT = "GUI/Reports/pattern_match_refined.json"

def main():
    if not os.path.exists(PATTERN_REPORT):
        print(f"[-] Pattern report {PATTERN_REPORT} not found. Run the pattern matcher first.")
        return

    print(f"[*] Loading pattern report from {PATTERN_REPORT}...")
    with open(PATTERN_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create dedicated table for indicators
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            indicator_type TEXT,
            indicator_value TEXT
        )
    """)
    
    # Optional: Clear out old entries for a clean reload
    cursor.execute("DELETE FROM indicators")
    conn.commit()

    inserted_count = 0
    for source_file, categories in data.items():
        for ind_type, values in categories.items():
            for val in values:
                cursor.execute("""
                    INSERT INTO indicators (source_file, indicator_type, indicator_value)
                    VALUES (?, ?, ?)
                """, (source_file, ind_type, val))
                inserted_count += 1

    conn.commit()
    conn.close()
    
    print(f"[+] Successfully inserted {inserted_count} indicators into the 'indicators' table.")

if __name__ == "__main__":
    main()
