import sqlite3
import csv
from itertools import combinations

DB_PATH = "pesci_intelligence.db"
ENTITIES = ["Boogie", "Keem", "Morning Star", "Nicholas DeOrio", "Scooter", "Tammy", "Wonder Woman", "YoMama"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT title FROM stream_archives WHERE title LIKE '%Beyond%';")
titles = [r[0] for r in cursor.fetchall()]
conn.close()

# Initialize N x N matrix
matrix = {e1: {e2: 0 for e2 in ENTITIES} for e1 in ENTITIES}

for title in titles:
    # Match entities in title
    present = [e for e in ENTITIES if e.lower() in title.lower()]
    # Count pairwise occurrences
    for e1, e2 in combinations(present, 2):
        matrix[e1][e2] += 1
        matrix[e2][e1] += 1

# 1. Print formatted Markdown Matrix to terminal
col_width = 16
header = f"| {'Entity':<{col_width}} | " + " | ".join([f"{e[:4]:^4}" for e in ENTITIES]) + " |"
divider = "|:" + "-" * (col_width + 1) + "|" + "|".join([":---:" for _ in ENTITIES]) + "|"

print("\n=== ENTITY CO-OCCURRENCE MATRIX ===")
print(header)
print(divider)

for e1 in ENTITIES:
    row_str = f"| {e1:<{col_width}} | " + " | ".join([f"{matrix[e1][e2]:^4}" for e2 in ENTITIES]) + " |"
    print(row_str)

# 2. Export to CSV using built-in csv module
with open("entity_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Entity"] + ENTITIES)
    for e1 in ENTITIES:
        writer.writerow([e1] + [matrix[e1][e2] for e2 in ENTITIES])

print("\n[+] Successfully exported matrix to entity_matrix.csv without pandas dependency.")
