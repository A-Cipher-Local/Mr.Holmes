import sqlite3
import os

DB_PATH = "pesci_intelligence.db"

def verify_database():
    if not os.path.exists(DB_PATH):
        print(f"[-] Error: {DB_PATH} not found in current directory.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=== [PROJECT ARGUS] DATABASE INTEGRITY & METRICS ===")

    # 1. Check SQLite Integrity
    cursor.execute("PRAGMA integrity_check;")
    integrity = cursor.fetchone()[0]
    print(f"[+] PRAGMA integrity_check: {integrity.upper()}")

    # 2. Get Record Counts
    cursor.execute("SELECT COUNT(*) FROM stream_archives;")
    archive_count = cursor.fetchone()[0]
    print(f"[+] Total records in 'stream_archives': {archive_count}")

    cursor.execute("SELECT COUNT(*) FROM stream_fts;")
    fts_count = cursor.fetchone()[0]
    print(f"[+] Total records in FTS5 index ('stream_fts'): {fts_count}")

    # 3. Sample Row Verification
    cursor.execute("SELECT rowid, video_id, title FROM stream_archives ORDER BY rowid ASC LIMIT 3;")
    samples = cursor.fetchall()
    print("\n[+] Sample Records (First 3):")
    for r in samples:
        print(f"    Row {r[0]} | ID: {r[1]} | Title: {r[2]}")

    conn.close()

if __name__ == "__main__":
    verify_database()
