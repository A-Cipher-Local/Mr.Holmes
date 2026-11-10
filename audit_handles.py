#!/usr/bin/env python3
import os
import time
import sqlite3
import requests

TARGETS_FILE = "targets.txt"
DB_FILE = "investigations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
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
    conn.commit()
    conn.close()

def load_targets():
    if not os.path.exists(TARGETS_FILE):
        return []
    with open(TARGETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def audit_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    print(f"[*] Auditing: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        return res.status_code, res.url
    except Exception as e:
        print(f"    [!] Error: {e}")
        return None, url

def store_result(alias, url, status):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id FROM entities WHERE value = ?", (url,))
    if not cur.fetchone():
        confidence = "HIGH" if status == 200 else "LOW"
        cur.execute('''
            INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (alias, "Direct Audit", f"HTTP {status}", url, confidence))
        conn.commit()
    conn.close()

def main():
    init_db()
    targets = load_targets()
    print("============================================================")
    print(f" DIRECT HANDLE STATUS AUDITOR ({len(targets)} targets)")
    print("============================================================\n")
    
    for url in targets:
        status, final_url = audit_url(url)
        if status:
            print(f"    [+] Status: {status} | Final URL: {final_url}")
            store_result("Sirjosephpesci", final_url, status)
        else:
            print(f"    [-] Failed to reach endpoint.")
        time.sleep(1.5)
        
    print("\n[+] Audit sweep complete. Results logged to investigations.db\n")

if __name__ == "__main__":
    main()
