#!/usr/init/env python3
import os
import json
import time
import sqlite3
import requests

TARGETS_FILE = "targets.txt"
DB_FILE = "investigations.db"
WAYBACK_API = "https://archive.org/wayback/available"

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
        print(f"[!] {TARGETS_FILE} not found. Creating default list...")
        with open(TARGETS_FILE, "w") as f:
            f.write("https://pastebin.com/u/DemonSmooch\nhttps://github.com/DemonSmooch\n")
    with open(TARGETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def check_archive(url):
    print(f"[*] Querying Archive API: {url}")
    try:
        res = requests.get(WAYBACK_API, params={"url": url}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            snapshot = data.get("archived_snapshots", {}).get("closest", {})
            if snapshot and snapshot.get("available"):
                return snapshot.get("url")
    except Exception as e:
        print(f"    [!] Error: {e}")
    return None

def store_result(url, archive_url):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Tammy Busagi", "Archive.org", "Snapshot URL", archive_url, "HIGH"))
    conn.commit()
    conn.close()
    print(f"    [+] Logged to {DB_FILE}")

def main():
    init_db()
    targets = load_targets()
    print(f"[+] Loaded {len(targets)} targets from {TARGETS_FILE}\n")
    
    for url in targets:
        hit = check_archive(url)
        if hit:
            print(f"    [+] FOUND: {hit}")
            store_result(url, hit)
        else:
            print("    [-] No archive snapshot found.")
        time.sleep(1.0)

if __name__ == "__main__":
    main()
