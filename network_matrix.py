import sqlite3
import json
import os
from collections import defaultdict
from itertools import combinations

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/network_similarity_matrix.json"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Map each source file to the set of indicators it contains
    cursor.execute("SELECT source_file, indicator_value FROM indicators")
    rows = cursor.fetchall()
    conn.close()

    file_to_indicators = defaultdict(set)
    for source_file, indicator in rows:
        file_to_indicators[source_file].add(indicator.lower())

    files = list(file_to_indicators.keys())
    print(f"[*] Computing Jaccard similarity across {len(files)} files...")

    network_links = []
    
    # Calculate pairwise Jaccard similarity: Intersection over Union
    for file1, file2 in combinations(files, 2):
        set1 = file_to_indicators[file1]
        set2 = file_to_indicators[file2]
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        if union:
            jaccard_score = len(intersection) / len(union)
            if jaccard_score > 0.0: # Record any shared overlap
                network_links.append({
                    "file_a": file1,
                    "file_b": file2,
                    "shared_count": len(intersection),
                    "shared_indicators": list(intersection),
                    "jaccard_similarity": round(jaccard_score, 4)
                })

    # Sort by similarity score descending
    network_links.sort(key=lambda x: x["jaccard_similarity"], reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(network_links, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Network similarity analysis complete. Saved to {OUTPUT_REPORT}")
    print("\n--------------------------------------------------")
    print("TOP FILE-TO-FILE CONNECTIONS (Jaccard Overlap):")
    print("--------------------------------------------------")
    
    # Display top 5 strongest file connections
    for link in network_links[:5]:
        print(f"Link: {link['file_a']} <---> {link['file_b']}")
        print(f"  - Similarity Score: {link['jaccard_similarity']} ({link['shared_count']} shared indicators)")
        print(f"  - Shared Items: {link['shared_indicators'][:3]}{'...' if len(link['shared_indicators']) > 3 else ''}")
        print()

if __name__ == "__main__":
    main()
