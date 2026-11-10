import sqlite3
import json
import os

CORPUS_FILE = "GUI/Reports/llm_ingest_corpus.json"
DB_PATH = "GUI/Database/osint_intelligence.db"

os.makedirs("GUI/Database", exist_ok=True)

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table for ingested corpus artifacts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT UNIQUE,
            content_length INTEGER,
            content TEXT
        )
    """)
    conn.commit()

    if not os.path.exists(CORPUS_FILE):
        print(f"[-] Corpus file {CORPUS_FILE} not found. Run the ingestion script first.")
        return

    print(f"[*] Loading corpus from {CORPUS_FILE}...")
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    inserted = 0
    for item in corpus:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO artifacts (source_file, content_length, content)
                VALUES (?, ?, ?)
            """, (item["source_file"], item["content_length"], item["data"]))
            inserted += 1
        except Exception as e:
            print(f"[-] Error inserting {item['source_file']}: {e}")

    conn.commit()
    conn.close()
    print(f"[+] Successfully inserted/updated {inserted} records into SQLite database.")

if __name__ == "__main__":
    main()
