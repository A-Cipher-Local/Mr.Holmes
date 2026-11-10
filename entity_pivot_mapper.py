import sqlite3
import json
import os
from collections import defaultdict

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_MAP = "GUI/Reports/entity_relationship_matrix.json"

def main():
    print(f"[*] Connecting to database at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print(f"[-] Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query indicators exclusively from 'active' non-sandbox artifacts
    query = """
        SELECT i.source_file, i.indicator_type, i.indicator_value 
        FROM indicators i
        JOIN artifacts a ON i.source_file = a.source_file
        WHERE a.domain_type = 'active' OR a.domain_type IS NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Processing {len(rows)} active indicators (sandbox artifacts excluded)...")
    
    # Map indicators to sources
    indicator_map = defaultdict(set)
    for source, ind_type, ind_val in rows:
        indicator_map[ind_val.lower()].add((source, ind_type))

    # Build relational intersections
    intersections = defaultdict(set)
    for ind, sources in indicator_map.items():
        if len(sources) > 1:
            source_list = list(sources)
            for i in range(len(source_list)):
                for j in range(i + 1, len(source_list)):
                    file_a = source_list[i][0]
                    file_b = source_list[j][0]
                    if file_a != file_b:
                        intersections[ind].add((file_a, file_b))

    report = []
    for ind, pairs in intersections.items():
        for f_a, f_b in pairs:
            report.append({
                "shared_indicator": ind,
                "file_a": f_a,
                "file_b": f_b
            })

    os.makedirs(os.path.dirname(OUTPUT_MAP), exist_ok=True)
    with open(OUTPUT_MAP, "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Relational mapping complete. Found {len(report)} active cross-artifact overlaps.")
    print(f"[+] Relationship matrix saved to {OUTPUT_MAP}")

if __name__ == "__main__":
    main()
