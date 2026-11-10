import os
import sqlite3
import re

DB_PATH = "GUI/Database/osint_intelligence.db"
RAW_DUMPS_DIR = "GUI/RawDumps"

# Regex patterns for OSINT extraction
PATTERNS = {
    "emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "urls": r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
    "handles": r"@[a-zA-Z0-9_]+"
}

def init_db(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            content TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            indicator_type TEXT,
            indicator_value TEXT
        )
    """)

def main():
    os.makedirs(RAW_DUMPS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    print(f"[*] Scanning {RAW_DUMPS_DIR} for new raw text dumps...")
    files = [f for f in os.listdir(RAW_DUMPS_DIR) if f.endswith(('.txt', '.md', '.csv', '.json'))]

    if not files:
        print(f"[-] No new raw files found in {RAW_DUMPS_DIR}. Drop files there to ingest.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    init_db(cursor)

    new_count = 0
    for filename in files:
        file_path = os.path.join(RAW_DUMPS_DIR, filename)
        
        # Check if already ingested
        cursor.execute("SELECT id FROM artifacts WHERE filename = ?", (filename,))
        if cursor.fetchone():
            continue

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Insert artifact
        cursor.execute("INSERT OR IGNORE INTO artifacts (filename, content) VALUES (?, ?)", (filename, content))

        # Extract indicators
        for ind_type, pattern in PATTERNS.items():
            matches = set(re.findall(pattern, content))
            for match in matches:
                cursor.execute(
                    "INSERT INTO indicators (source_file, indicator_type, indicator_value) VALUES (?, ?, ?)",
                    (filename, ind_type, match)
                )

        print(f"[+] Successfully parsed and ingested: {filename}")
        new_count += 1

    conn.commit()
    conn.close()
    print(f"\n[+] Ingestion complete. Added {new_count} new files into {DB_PATH}")

if __name__ == "__main__":
    main()
