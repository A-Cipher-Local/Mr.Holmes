#!/usr/bin/env python3
import sqlite3
from datetime import datetime

DB_FILE = "investigations.db"
OUTPUT_FILE = "DOSSIER_SIRJOSEPHPESCI.md"

def update_dossier():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("SELECT id, target_alias, platform, indicator_type, value, confidence, timestamp FROM entities")
    records = cur.fetchall()
    conn.close()

    md = []
    md.append("# EXECUTIVE INTELLIGENCE DOSSIER")
    md.append(f"**Target Identifier**: `@SirJosephPesci` / `Sirjosephpesci`  ")
    md.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Source Database**: `{DB_FILE}`\n")
    
    md.append("---")
    md.append("## 1. Identity & Descriptor Summary\n")
    md.append("| Attribute | Value | Confidence |")
    md.append("|---|---|---|")
    
    handles = []
    geo_vocation = []
    hubs = []
    descriptions = []
    
    for r in records:
        if r[2] == "Direct Audit":
            handles.append(r)
        elif r[2] in ["Geolocation", "Vocation"]:
            geo_vocation.append(r)
        elif r[2] == "Regional Vocation Hub":
            hubs.append(r)
        elif r[2] == "YouTube Description":
            descriptions.append(r)

    for g in geo_vocation:
        md.append(f"| **{g[3]}** | `{g[4]}` | {g[5]} |")
    
    md.append("\n---")
    md.append("## 2. Platform Handles & Endpoints\n")
    md.append("| Endpoint / Platform | Status / URL | Confidence | Last Audited |")
    md.append("|---|---|---|---|")
    for h in handles:
        md.append(f"| {h[3]} | `{h[4]}` | {h[5]} | {h[6]} |")
        
    md.append("\n---")
    md.append("## 3. Discovered Infrastructure & Referral Links\n")
    md.append("| Indicator Type | Target Value / Endpoint | Confidence |")
    md.append("|---|---|---|")
    for d in descriptions:
        md.append(f"| {d[3]} | `{d[4]}` | {d[5]} |")

    md.append("\n---")
    md.append("## 4. Cleveland Regional Auto Auction Registry Overlay\n")
    md.append("| ID | Candidate Facility & Type |")
    md.append("|---|---|")
    for hub in hubs:
        md.append(f"| **[{hub[0]}]** | {hub[4]} |")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(md))
        
    print(f"[+] Dossier updated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    update_dossier()
