#!/usr/bin/env python3
import sqlite3

DB_FILE = "investigations.db"

def update_profile():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Ensure table structure exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_alias TEXT,
            platform TEXT,
            indicator_type TEXT,
            value TEXT,
            confidence TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    new_indicators = [
        ("Sirjosephpesci", "Geolocation", "Residence / Location", "Cleveland, OH", "MEDIUM"),
        ("Sirjosephpesci", "Vocation", "Occupation / Background", "Car Auctioneer", "MEDIUM")
    ]
    
    for alias, platform, ind_type, val, conf in new_indicators:
        cur.execute("SELECT id FROM entities WHERE value = ?", (val,))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (alias, platform, ind_type, val, conf))
            print(f"[+] Added indicator: {ind_type} -> {val}")
        else:
            print(f"[*] Indicator already exists: {val}")
            
    conn.commit()
    conn.close()
    print("\n[+] Profile telemetry successfully updated.")

if __name__ == "__main__":
    update_profile()
