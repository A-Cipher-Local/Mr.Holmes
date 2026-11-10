#!/usr/bin/env python3
import sqlite3
import urllib.parse

DB_FILE = "investigations.db"

LOCAL_REGISTRIES = [
    {
        "jurisdiction": "Local - Ohio State",
        "entity": "Ohio Secretary of State (Business & LLC Filings)",
        "search_url": "https://businesssearch.ohiosos.gov/",
        "query_type": "Corporate Filings / Trade Names",
        "notes": "Searches registered business entities, trade names, and agent registrations in Ohio."
    },
    {
        "jurisdiction": "Local - Ohio State",
        "entity": "Ohio Dept of Agriculture (Auctioneer Licensing Board)",
        "search_url": "https://agri.ohio.gov/divisions/auctioneers/licensee-search",
        "query_type": "Professional License Verification",
        "notes": "Cross-references active and historical licensed car auctioneers in Ohio."
    },
    {
        "jurisdiction": "Local - Cuyahoga County",
        "entity": "Cuyahoga County Fiscal Officer & Property Records",
        "search_url": "https://fiscalofficer.cuyahogacounty.us/en-US/real-estate-information.aspx",
        "query_type": "Property Assessment / Deed Index",
        "notes": "Searches real estate parcel ownership records in Greater Cleveland."
    },
    {
        "jurisdiction": "Local - Lorain County",
        "entity": "Lorain County Auditor Property Search",
        "search_url": "http://www.loraincounty.us/auditor/",
        "query_type": "Property Assessment Index",
        "notes": "Covers western Cleveland suburbs and adjacent auction hub zones."
    }
]

GLOBAL_REGISTRIES = [
    {
        "jurisdiction": "Global / US Open-Data",
        "entity": "OpenCorporates API / Global Corporate Search",
        "search_url": "https://opencorporates.com/",
        "query_type": "Global Corporate Registry Index",
        "notes": "Aggregates corporate registrations across all 50 US states and international jurisdictions."
    },
    {
        "jurisdiction": "National - US Federal",
        "entity": "FCC Universal Licensing System (ULS)",
        "search_url": "https://wireless2.fcc.gov/UlsApp/UlsSearch/searchLicense.jsp",
        "query_type": "Federal Call Sign & Amateur License Index",
        "notes": "Useful for mapping aliases/names to registered radio, broadcast, or GMRS operator licenses."
    },
    {
        "jurisdiction": "National - US Federal",
        "entity": "SEC EDGAR Database Search",
        "search_url": "https://www.sec.gov/edgar/searchedgar/companysearch",
        "query_type": "Commercial & Officer Filings",
        "notes": "Cross-references corporate officers, directors, and vehicle remarketing group filings."
    },
    {
        "jurisdiction": "Global - Digital Footprint",
        "entity": "WhatsMyName Keybase / OSINT Name Index",
        "search_url": "https://whatsmyname.app/",
        "query_type": "Multi-Platform Username Enumeration",
        "notes": "Enumerates candidate monikers across 500+ global web communities and forums."
    }
]

def init_registry_schema():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS registry_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jurisdiction TEXT,
            entity_name TEXT,
            search_url TEXT,
            query_type TEXT,
            notes TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def populate_registry_targets():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    all_targets = LOCAL_REGISTRIES + GLOBAL_REGISTRIES
    added = 0
    
    print("==================================================================")
    print(" MAPPING LOCAL (OHIO) & GLOBAL (OPEN-DATA) INVESTIGATIVE REGISTRIES")
    print("==================================================================\n")
    
    for t in all_targets:
        cur.execute("SELECT id FROM registry_targets WHERE entity_name = ?", (t["entity"],))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO registry_targets (jurisdiction, entity_name, search_url, query_type, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (t["jurisdiction"], t["entity"], t["search_url"], t["query_type"], t["notes"]))
            print(f"  [+] Logged [{t['jurisdiction']}]: {t['entity']}")
            added += 1
        else:
            print(f"  [*] Already Exists: {t['entity']}")
            
    conn.commit()
    conn.close()
    print(f"\n[+] Pipeline updated: {added} new local & global search targets logged to {DB_FILE}.\n")

def execute_live_keyword_audit(candidate_terms):
    print("==================================================================")
    print(" GENERATING MULTI-JURISDICTIONAL AUDIT TARGET STRINGS")
    print("==================================================================")
    for term in candidate_terms:
        print(f"\n[*] Candidate Term: '{term}'")
        encoded = urllib.parse.quote(term)
        print(f"    -> OpenCorporates Search : https://opencorporates.com/search?q={encoded}")
        print(f"    -> Ohio SOS Search       : https://businesssearch.ohiosos.gov/?searchTerm={encoded}")
        print(f"    -> WhatsMyName Direct    : https://whatsmyname.app/ (Target string: {term})")

if __name__ == "__main__":
    init_registry_schema()
    populate_registry_targets()
    
    candidate_keywords = ["Sirjosephpesci", "AlwayzSmoking", "Pit Crew Commentary LLC"]
    execute_live_keyword_audit(candidate_keywords)
