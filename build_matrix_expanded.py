import sqlite3
import csv
from itertools import combinations

DB_PATH = "pesci_intelligence.db"
ENTITIES = ["Boogie", "Keem", "Morning Star", "Nicholas DeOrio", "Scooter", "Tammy", "Wonder Woman", "YoMama"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT title, COALESCE(description, '') FROM stream_archives WHERE title LIKE '%Beyond%';")
records = cursor.fetchall()
conn.close()

matrix = {e1: {e2: 0 for e2 in ENTITIES} for e1 in ENTITIES}
entity_counts = {e: 0 for e in ENTITIES}

for title, desc in records:
    combined_text = f"{title} {desc}".lower()
    present = [e for e in ENTITIES if e.lower() in combined_text]
    
    for e in present:
        entity_counts[e] += 1
        
    for e1, e2 in combinations(present, 2):
        matrix[e1][e2] += 1
        matrix[e2][e1] += 1

print("=== INDIVIDUAL ENTITY MENTIONS (Titles + Descriptions) ===")
for e, count in sorted(entity_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"- {e:<16}: {count} streams")

col_width = 16
header = f"\n| {'Entity':<{col_width}} | " + " | ".join([f"{e[:4]:^4}" for e in ENTITIES]) + " |"
divider = "|:" + "-" * (col_width + 1) + "|" + "|".join([":---:" for _ in ENTITIES]) + "|"

print("\n=== EXPANDED CO-OCCURRENCE MATRIX ===")
print(header)
print(divider)

for e1 in ENTITIES:
    row_str = f"| {e1:<{col_width}} | " + " | ".join([f"{matrix[e1][e2]:^4}" for e2 in ENTITIES]) + " |"
    print(row_str)

with open("entity_matrix_expanded.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Entity"] + ENTITIES)
    for e1 in ENTITIES:
        writer.writerow([e1] + [matrix[e1][e2] for e2 in ENTITIES])

print("\n[+] Exported expanded matrix to entity_matrix_expanded.csv")
