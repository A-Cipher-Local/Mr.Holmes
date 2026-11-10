import sqlite3
import json
from collections import defaultdict
from itertools import combinations

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/network_similarity_filtered.json"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Identify ubiquitous infrastructure indicators (appearing in > 5 files)
    cursor.execute("""
        SELECT indicator_value, COUNT(DISTINCT source_file) as fc
        FROM indicators
        GROUP BY indicator_value
        HAVING fc > 5
    """)
    ubiquitous = {row[0].lower() for row in cursor.fetchall()}
    print(f"[*] Filtering out {len(ubiquitous)} ubiquitous infrastructure indicators (e.g., developer email/anchors)...")

    # Step 2: Fetch all indicators, excluding ubiquitous ones
    cursor.execute("SELECT source_file, indicator_value FROM indicators")
    rows = cursor.fetchall()
    conn.close()

    file_to_indicators = defaultdict(set)
    for source_file, indicator in rows:
        ind_lower = indicator.lower()
        if ind_lower not in ubiquitous:
            file_to_indicators[source_file].add(ind_lower)

    # Step 3: Compute filtered Jaccard similarity
    files = [f for f, inds in file_to_indicators.items() if inds]
    print(f"[*] Computing filtered Jaccard similarity across {len(files)} target files...")

    network_links = []
    for file1, file2 in combinations(files, 2):
        set1 = file_to_indicators[file1]
        set2 = file_to_indicators[file2]
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        if union:
            jaccard_score = len(intersection) / len(union)
            if jaccard_score > 0.0:
                network_links.append({
                    "file_a": file1,
                    "file_b": file2,
                    "shared_count": len(intersection),
                    "shared_indicators": list(intersection),
                    "jaccard_similarity": round(jaccard_score, 4)
                })

    network_links.sort(key=lambda x: (x["shared_count"], x["jaccard_similarity"]), reverse=True)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(network_links, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Filtered analysis complete. Saved to {OUTPUT_REPORT}")
    print("\n--------------------------------------------------")
    print("TOP FILTERED FILE-TO-FILE CONNECTIONS:")
    print("--------------------------------------------------")
    
    if not network_links:
        print("    [-] No shared non-ubiquitous indicators found between files in this batch.")
        return

    for link in network_links[:5]:
        print(f"Link: {link['file_a']} <---> {link['file_b']}")
        print(f"  - Shared Count: {link['shared_count']} | Similarity: {link['jaccard_similarity']}")
        print(f"  - Shared Indicators: {link['shared_indicators']}")
        print()

if __name__ == "__main__":
    main()
