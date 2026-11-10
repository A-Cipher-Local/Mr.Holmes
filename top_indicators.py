import json
import os
from collections import Counter

MATRIX_PATH = "GUI/Reports/entity_relationship_matrix.json"

def main():
    if not os.path.exists(MATRIX_PATH):
        print(f"[-] Error: Relationship matrix not found at {MATRIX_PATH}")
        return

    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        matrix = json.load(f)

    print(f"[*] Analyzing {len(matrix)} relationship entries...")

    # Count frequencies of shared indicators
    indicator_counts = Counter(item["shared_indicator"] for item in matrix)

    print("\n--------------------------------------------------")
    print("TOP 10 MOST SHARED ACTIVE INDICATORS:")
    print("--------------------------------------------------")
    for ind, count in indicator_counts.most_common(10):
        print(f"  - [{count} cross-links] {ind}")

if __name__ == "__main__":
    main()
