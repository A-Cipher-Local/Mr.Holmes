import sqlite3
import sys

DB_PATH = "GUI/Database/osint_intelligence.db"

def search_term(term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT source_file, length(content) FROM artifacts WHERE content LIKE ?"
    cursor.execute(query, (f"%{term}%",))
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n[+] Search results for '{term}': Found in {len(results)} file(s)")
    for source, length in results:
        print(f"    - File: {source} (Size: {length} bytes)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 search_db.py <search_term>")
        print("Example: python3 search_db.py stlawrenceparish")
        return
    
    term = sys.argv[1]
    search_term(term)

if __name__ == "__main__":
    main()
