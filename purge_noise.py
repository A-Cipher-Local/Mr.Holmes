import sqlite3

DB_PATH = "pesci_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Count records before purge
cursor.execute("SELECT COUNT(*) FROM stream_archives;")
total_before = cursor.fetchone()[0]

# Delete anything that does NOT contain "Beyond" in the title
cursor.execute("DELETE FROM stream_archives WHERE title NOT LIKE '%Beyond%';")
conn.commit()

# Count records after purge
cursor.execute("SELECT COUNT(*) FROM stream_archives;")
total_after = cursor.fetchone()[0]

conn.close()
print(f"[+] Purged {total_before - total_after} unrelated noise entries.")
print(f"[+] Active 'Beyond the Pit' archive count locked at: {total_after}")
