#!/usr/bin/env bash
set -e

# ==============================================================================
# Execute Entity Pivot Mapper across active indicators in SQLite DB
# ==============================================================================

DB_PATH="GUI/Database/osint_intelligence.db"
OUTPUT_PATH="GUI/Reports/entity_pivot_matrix.json"

python3 - << 'PYEOF'
import sqlite3
import json
import os

db_path = "GUI/Database/osint_intelligence.db"
output_path = "GUI/Reports/entity_pivot_matrix.json"

if not os.path.exists(db_path):
    print(f"[-] Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query indicators grouped by value to count distinct sources
cursor.execute("""
    SELECT indicator_value, indicator_type, COUNT(DISTINCT source_file) as src_count, GROUP_CONCAT(DISTINCT source_file)
    FROM indicators
    GROUP BY indicator_value
    ORDER BY src_count DESC, COUNT(*) DESC
""")

rows = cursor.fetchall()

pivots = []
for val, itype, count, sources in rows:
    pivots.append({
        "indicator": val,
        "type": itype,
        "shared_source_count": count,
        "sources": sources.split(",") if sources else []
    })

conn.close()

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(pivots, f, indent=2)

print(f"[+] Matrix Pivot Complete: Mapped {len(pivots)} distinct indicators across database artifacts.")
print(f"[+] Pivot matrix saved to {output_path}\n")

print("--- TOP CROSS-ARTIFACT PIVOT NODES ---")
for p in pivots[:15]:
    print(f"  {p['indicator']} ({p['type']}): Linked across {p['shared_source_count']} artifact(s)")
PYEOF

