cat << 'EOF' > run_audit.py
#!/usr/bin/env python3
import sqlite3

DB_FILE = "investigations.db"

def verify_database():
    print(f"[*] Connecting to local database: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print(f"    [+] Active tables found: {[t[0] for t in tables]}")
    
    conn.close()

if __name__ == "__main__":
    verify_database()
EOF

chmod +x run_audit.py
python3 run_audit.py
