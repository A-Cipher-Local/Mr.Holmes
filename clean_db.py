#!/usr/bin/env python3
import sqlite3

DB_FILE = "investigations.db"

def clean_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Fix the corrupted SCA auction entry if present
    cur.execute('''
        UPDATE entities 
        SET value = 'SCA Public Auto Auction Cleveland (Lorain / Cleveland, OH) - Public Salvage & Repairable Auction [https://sca.auction]'
        WHERE id = 13
    ''')
    
    conn.commit()
    
    # Verify records
    cur.execute("SELECT id, indicator_type, value FROM entities")
    print("[*] Current Database Integrity Check:")
    for r in cur.fetchall():
        print(f"    [{r[0]}] {r[1]} -> {r[2][:60]}...")
        
    conn.close()
    print("\n[+] Database audit and repair complete.")

if __name__ == "__main__":
    clean_database()
