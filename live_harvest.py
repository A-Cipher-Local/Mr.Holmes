#!/usr/init/env python3
import os
import json
import time
import sqlite3
import requests
from urllib.parse import quote_plus, urlparse

DB_FILE = "investigations.db"
TARGET_QUERIES = [
    "Sirjosephpesci",
    "Sir Joseph Pesci",
    "Sirjosephpesci archive",
    "Sirjosephpesci lolcow",
    "Sirjosephpesci youtube"
]

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

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }
    
    print(f"[*] Querying DuckDuckGo HTML for: \"{query}\"")
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(res.text, "html.parser")
            results = []
            # Broaden selector to catch any result links
            for a in soup.find_all("a", class_="result__url"):
                link = a.get("href")
                if link and link.startswith("http"):
                    results.append(link)
            # Fallback if specific class missed
            if not results:
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "uddg=" in href:
                        # Extract actual URL from DuckDuckGo redirect wrapper if present
                        import urllib.parse as up
                        parsed = up.parse_qs(up.urlparse(href).query)
                        if "uddg" in parsed:
                            results.append(parsed["uddg"][0])
            return list(set(results))
    except Exception as e:
        print(f"    [!] Search error: {e}")
    return []

def store_result(alias, live_url):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id FROM entities WHERE value = ?", (live_url,))
    if not cur.fetchone():
        cur.execute('''
            INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (alias, "Live Web", "Discovered URL", live_url, "MEDIUM"))
        conn.commit()
        print(f"    [+] Logged new URL to {DB_FILE}: {live_url}")
    conn.close()

def main():
    init_db()
    print("============================================================")
    print(" ROBUST LIVE OSINT DISCOVERY HARVESTER")
    print("============================================================\n")
    
    for query in TARGET_QUERIES:
        urls = search_duckduckgo(query)
        print(f"    [+] Found {len(urls)} references for {query}.")
        for link in urls:
            store_result(query, link)
        time.sleep(3.0)
        
    print("\n[+] Harvest sweep complete.\n")

if __name__ == "__main__":
    main()
