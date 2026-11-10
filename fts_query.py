import sqlite3
import sys
import json

DB_PATH = "pesci_intelligence.db"

def query_fts(term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query the FTS5 virtual table
    cursor.execute("""
        SELECT video_id, upload_date, title 
        FROM stream_fts 
        WHERE stream_fts MATCH ? 
        ORDER BY rank;
    """, (term,))
    
    rows = cursor.fetchall()
    conn.close()

    results = [
        {"video_id": r[0], "upload_date": r[1] or "N/A", "title": r[2]}
        for r in rows
    ]
    
    print(f"\n=== FTS5 QUERY RESULTS: '{term}' ({len(results)} matches) ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else "Beyond"
    query_fts(search_term)
