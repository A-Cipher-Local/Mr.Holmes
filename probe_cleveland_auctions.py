#!/usr/bin/env python3
import sqlite3
import json

DB_FILE = "investigations.db"

# Primary vehicle auction platforms, wholesale hubs, and repossession centers in Greater Cleveland
CLEVELAND_AUCTION_REGISTRIES = [
    {
        "name": "Manheim Cleveland",
        "location": "Brook Park, OH",
        "type": "Dealer Wholesale Auction",
        "url": "https://www.manheim.com",
        "notes": "Major wholesale vehicle auction hub in Brook Park/Cleveland area."
    },
    {
        "name": "ADESA Cleveland",
        "location": "Northfield, OH",
        "type": "Dealer & Fleet Auction",
        "url": "https://www.adesa.com",
        "notes": "Dealer consignment, repo, and fleet remarketing sales."
    },
    {
        "name": "IAAI Cleveland West / Lorain",
        "location": "Lorain / Cleveland West, OH",
        "type": "Insurance Salvage Auction",
        "url": "https://www.iaai.com",
        "notes": "Insurance Auto Auctions salvage and total loss liquidation facility."
    },
    {
        "name": "Copart Cleveland",
        "location": "Columbia Station / Cleveland East, OH",
        "type": "Salvage & Wholesale Auction",
        "url": "https://www.copart.com",
        "notes": "Copart salvage vehicle yard and public/dealer bidding platform."
    },
    {
        "name": "Capital Auto Auction Cleveland",
        "location": "Cleveland, OH",
        "type": "Public & Dealer Vehicle Auction",
        "url": "https://www.capitalautoauction.com",
        "notes": "Public online vehicle auctions and municipal/bank repo liquidation."
    },
    {
        "name": "SCA Public Auto Auction Cleveland",
        "location": "Lorain / Cleveland, OH",
        "type": "Public Salvage & Repairable Auction",
        "url": "https://sca.auction",
        "notes": "Public access repairable vehicle auction branch."
    }
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

def log_auction_registries():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    print("============================================================")
    print(" LOGGING CLEVELAND REGIONAL AUTO AUCTION TARGETS")
    print("============================================================\n")
    
    logged_count = 0
    for hub in CLEVELAND_AUCTION_REGISTRIES:
        val_str = f"{hub['name']} ({hub['location']}) - {hub['type']} [{hub['url']}]"
        
        # Avoid duplicate database entries
        cur.execute("SELECT id FROM entities WHERE value = ?", (val_str,))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO entities (target_alias, platform, indicator_type, value, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', ("Sirjosephpesci", "Regional Vocation Hub", "Candidate Auto Auction Registry", val_str, "MEDIUM"))
            print(f"    [+] Logged: {hub['name']} -> {hub['location']}")
            logged_count += 1
        else:
            print(f"    [*] Already Indexed: {hub['name']}")
            
    conn.commit()
    conn.close()
    print(f"\n[+] Processing complete. {logged_count} new candidate auction registries logged to {DB_FILE}.\n")

if __name__ == "__main__":
    init_db()
    log_auction_registries()
