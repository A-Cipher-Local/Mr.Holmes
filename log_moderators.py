import sqlite3

DB_PATH = "pesci_intelligence.db"

def log_moderators():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create moderators table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moderators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT UNIQUE NOT NULL,
            associated_entity TEXT,
            notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    mods = [
        ("@UmmAndUhh01", "Nick and Tammy", "Confirmed channel moderator"),
        ("@nope-xix", "Nick and Tammy", "Confirmed channel moderator")
    ]

    for handle, entity, notes in mods:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO moderators (handle, associated_entity, notes)
                VALUES (?, ?, ?)
            """, (handle, entity, notes))
            print(f"[+] Logged moderator: {handle}")
        except Exception as e:
            print(f"[-] Error logging {handle}: {e}")

    conn.commit()
    
    # Verify records
    cursor.execute("SELECT id, handle, associated_entity, timestamp FROM moderators")
    rows = cursor.fetchall()
    print("\n[+] Current Moderators in Database:")
    print("=" * 50)
    for r in rows:
        print(f"ID: {r[0]} | Handle: {r[1]} | Target: {r[2]} | Logged: {r[3]}")
    print("=" * 50)

    conn.close()

if __name__ == "__main__":
    log_moderators()
