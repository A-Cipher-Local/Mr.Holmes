#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import sqlite3
import re

DB_FILE = "investigations.db"
CHANNEL_ID = "UCnYHQpxTkmRXuwRAbPyZinQ"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def deep_inspect_feed():
    print(f"[*] Extracting video descriptions and external links for channel: {CHANNEL_ID}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(RSS_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}
            
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            
            entries = root.findall('atom:entry', ns)
            print(f"    [+] Parsing {len(entries)} RSS feed entries for external links & mentions...\n")
            
            for entry in entries:
                title = entry.find('atom:title', ns).text
                video_id = entry.find('yt:videoId', ns).text
                media_group = entry.find('media:group', ns)
                description = media_group.find('media:description', ns).text if media_group is not None else ""
                
                print(f"    - Analyzing Video: {title} (ID: {video_id})")
                
                # Extract URLs or Discord links from description
                urls = re.findall(r'(https?://[^\s]+)', description)
                for u in urls:
                    print(f"        [Found Link]: {u}")
                    cur.execute("SELECT id FROM entities WHERE value = ?", (u,))
                    if not cur.fetchone():
                        cur.execute('''
                            INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
                            VALUES (?, ?, ?, ?, ?)
                        ''', ("Sirjosephpesci", "YouTube Description", "External Link / Referral", u, "HIGH"))
            
            conn.commit()
            conn.close()
            print("\n[+] Deep inspection complete. New telemetry logged to investigations.db")
        else:
            print(f"    [-] Failed to fetch RSS feed: HTTP {res.status_code}")
    except Exception as e:
    print(f"    [!] Error during deep inspection: {e}")

if __name__ == "__main__":
    deep_inspect_feed()
