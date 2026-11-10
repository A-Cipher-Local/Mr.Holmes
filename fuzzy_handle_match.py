import sqlite3
import json
import os
from difflib import SequenceMatcher

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/fuzzy_handle_matches.json"

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all unique handles and their source files
    cursor.execute("SELECT DISTINCT indicator_value, source_file FROM indicators WHERE indicator_type = 'handles'")
    rows = cursor.fetchall()
    conn.close()

    handle_map = {}
    for handle, source in rows:
        if handle not in handle_map:
            handle_map[handle] = set()
        handle_map[handle].add(source)

    handles = list(handle_map.keys())
    print(f"[*] Analyzing {len(handles)} unique handles for fuzzy string variations...")

    fuzzy_matches = []
    
    # Compare unique handles pairwise for high similarity (e.g., > 0.8)
    for i in range(len(handles)):
        for j in range(i + 1, len(handles)):
            h1 = handles[i]
            h2 = handles[j]
            score = similarity(h1, h2)
            
            if 0.75 <= score < 1.0: # High similarity but not identical
                fuzzy_matches.append({
                    "handle_a": h1,
                    "sources_a": list(handle_map[h1]),
                    "handle_b": h2,
                    "sources_b": list(handle_map[h2]),
                    "similarity_score": round(score, 3)
                })

    fuzzy_matches.sort(key=lambda x: x["similarity_score"], reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(fuzzy_matches, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Fuzzy analysis complete. Saved to {OUTPUT_REPORT}")
    print("\n--------------------------------------------------")
    print("TOP SIMILAR HANDLE VARIANTS:")
    print("--------------------------------------------------")

    if not fuzzy_matches:
        print("    [-] No high-similarity handle variants found in this batch.")
        return

    for match in fuzzy_matches[:10]:
        print(f"[MATCH] '{match['handle_a']}' <---> '{match['handle_b']}' (Score: {match['similarity_score']})")
        print(f"  - Files A: {match['sources_a']}")
        print(f"  - Files B: {match['sources_b']}")
        print()

if __name__ == "__main__":
    main()
