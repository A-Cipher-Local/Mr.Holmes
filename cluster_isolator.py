import sqlite3
import json
import os
from collections import defaultdict

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/isolated_clusters.json"

def main():
    print(f"[*] Connecting to database at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print(f"[-] Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query only active (non-sandbox) artifacts and their indicators
    query = """
        SELECT i.source_file, i.indicator_value 
        FROM indicators i
        JOIN artifacts a ON i.source_file = a.source_file
        WHERE a.domain_type = 'active' OR a.domain_type IS NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("[-] Warning: No active operational indicators found to cluster.")
        return

    indicator_to_files = defaultdict(set)
    file_to_indicators = defaultdict(set)

    for source_file, indicator in rows:
        ind_lower = indicator.lower()
        indicator_to_files[ind_lower].add(source_file)
        file_to_indicators[source_file].add(ind_lower)

    files = list(file_to_indicators.keys())
    adj = defaultdict(set)
    for ind, associated_files in indicator_to_files.items():
        if len(associated_files) > 1:
            files_list = list(associated_files)
            for i in range(len(files_list)):
                for j in range(i + 1, len(files_list)):
                    adj[files_list[i]].add(files_list[j])
                    adj[files_list[j]].add(files_list[i])

    visited = set()
    clusters = []

    for f in files:
        if f not in visited:
            cluster = set()
            stack = [f]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    cluster.add(node)
                    stack.extend(adj[node] - visited)
            clusters.append(list(cluster))

    clusters.sort(key=len, reverse=True)

    cluster_report = []
    for idx, cluster in enumerate(clusters, 1):
        cluster_report.append({
            "cluster_id": idx,
            "file_count": len(cluster),
            "files": cluster
        })

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(cluster_report, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Active cluster isolation complete (sandbox domains excluded). Saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
