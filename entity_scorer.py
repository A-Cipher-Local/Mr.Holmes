import sqlite3
import json
import os
from collections import defaultdict

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/entity_pivot_scorecard.json"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query all indicators with their source file counts
    query = """
        SELECT indicator_type, indicator_value, COUNT(DISTINCT source_file) as file_count, GROUP_CONCAT(source_file, '||')
        FROM indicators
        GROUP BY indicator_type, indicator_value
        ORDER BY file_count DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Processing {len(rows)} unique indicators for network centrality and pivoting...")

    scorecard = []
    for ind_type, value, count, files_str in rows:
        files = files_str.split("||")
        weight_score = count * 10 if ind_type == "emails" else count * 5
        
        scorecard.append({
            "indicator_type": ind_type,
            "indicator_value": value,
            "file_appearance_count": count,
            "connected_files": files,
            "calculated_weight": weight_score
        })

    # Sort by weight score descending
    scorecard.sort(key=lambda x: x["calculated_weight"], reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(scorecard, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Analysis complete. Top weighted indicators saved to {OUTPUT_REPORT}")
    print("\n--------------------------------------------------")
    print("TOP 5 HIGHEST CENTRALITY NODES:")
    print("--------------------------------------------------")
    for item in scorecard[:5]:
        print(f"[{item['indicator_type'].upper()}] {item['indicator_value']}")
        print(f"  - Cross-File Links: {item['file_appearance_count']} files | Weight Score: {item['calculated_weight']}")
        print(f"  - Primary Source: {item['connected_files'][0]}")
        print()

if __name__ == "__main__":
    main()
