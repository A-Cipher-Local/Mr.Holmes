import sqlite3
import sys
import argparse

DB_PATH = "GUI/Database/osint_intelligence.db"

def search_database(terms, logic="AND"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Build dynamic SQL query to search both source_file and content columns
    term_clauses = []
    params = []
    
    for term in terms:
        # Match term in either source_file or content
        term_clauses.append("(source_file LIKE ? OR content LIKE ?)")
        params.extend([f"%{term}%", f"%{term}%"])
        
    operator = " AND " if logic.upper() == "AND" else " OR "
    where_clause = operator.join(term_clauses)
    
    query = f"SELECT source_file, content FROM artifacts WHERE {where_clause}"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n[+] Search Query: [{ ' '.join([f'\"{t}\"' for t in terms]) }] using {logic.upper()} logic (Searching filename + content)")
    print(f"[+] Total Matching Files: {len(results)}\n")
    
    for source_file, content in results:
        print(f"--------------------------------------------------")
        print(f"File: {source_file}")
        print(f"--------------------------------------------------")
        
        # Check if filename itself matched any of the terms
        filename_matched = any(t.lower() in source_file.lower() for t in terms)
        if filename_matched:
            print(f"  > [Filename Match]")
            
        # Extract brief matching snippets from content for context
        if content:
            lines = content.splitlines()
            match_count = 0
            for line in lines:
                if logic.upper() == "AND":
                    match = all(t.lower() in line.lower() for t in terms)
                else:
                    match = any(t.lower() in line.lower() for t in terms)
                    
                if match and match_count < 3:
                    print(f"  > {line.strip()[:120]}...")
                    match_count += 1
        print()

def main():
    parser = argparse.ArgumentParser(description="Advanced Boolean Search for OSINT SQLite Database")
    parser.add_argument("terms", nargs="+", help="Search terms (e.g., TammyBUsagi data)")
    parser.add_argument("--logic", choices=["AND", "OR"], default="AND", help="Boolean operator between terms (default: AND)")
    
    args = parser.parse_args()
    search_database(args.terms, args.logic)

if __name__ == "__main__":
    main()
