import sqlite3
import re
from collections import Counter

DB_PATH = "pesci_intelligence.db"

def build_fts_and_analyze():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create and populate FTS5 table for high-speed textual querying
    cursor.execute("DROP TABLE IF EXISTS stream_fts;")
    cursor.execute("""
        CREATE VIRTUAL TABLE stream_fts USING fts5(
            video_id, 
            upload_date, 
            title, 
            description
        );
    """)
    cursor.execute("""
        INSERT INTO stream_fts(video_id, upload_date, title, description)
        SELECT video_id, COALESCE(upload_date, 'N/A'), title, COALESCE(description, '') 
        FROM stream_archives;
    """)
    conn.commit()

    # 2. Extract all streams for anomaly and structural parsing
    cursor.execute("SELECT video_id, upload_date, title FROM stream_archives ORDER BY rowid ASC;")
    records = cursor.fetchall()

    episodes = []
    fractionals = []
    unindexed = []

    for vid, date, title in records:
        # Match standard episode numbering
        ep_match = re.search(r'Ep\.\s*(\d+)', title, re.IGNORECASE)
        # Match fractional numbering (.5 or 1/2)
        frac_match = re.search(r'(\d+[\.\½]5?)', title)

        if ep_match:
            episodes.append(int(ep_match.group(1)))
        elif "½" in title or ".5" in title:
            fractionals.append((vid, title))
        else:
            unindexed.append((vid, title))

    # Identify numerical gaps in the catalog
    min_ep, max_ep = (min(episodes), max(episodes)) if episodes else (0, 0)
    missing_eps = [ep for ep in range(min_ep, max_ep + 1) if ep not in episodes]

    # 3. Target Personality / Handle Detection
    target_handles = [
        "nicholas", "deorio", "keem", "boogie", "scooter", 
        "tammy", "wonder woman", "yomama", "morning star", "fall guys", "rejects"
    ]
    
    handle_matches = Counter()
    for vid, date, title in records:
        title_lower = title.lower()
        for handle in target_handles:
            if handle in title_lower:
                handle_matches[handle] += 1

    # 4. Generate Master Intelligence Payload File
    output_path = "master_intelligence_audit.md"
    with open(output_path, "w") as f:
        f.write("# PROJECT ARGUS: Master OSINT Intelligence Audit\n\n")
        
        f.write("## 1. Sequence Continuity & Missing Episode Index\n")
        f.write(f"- **Indexed Range:** Ep. {min_ep} to Ep. {max_ep}\n")
        f.write(f"- **Missing Indexes:** {missing_eps if missing_eps else 'None detected'}\n")
        f.write(f"- **Total Fractional / Interstitial Streams (.5 Releases):** {len(fractionals)}\n")
        for vid, title in fractionals:
            f.write(f"  - [`{vid}`] {title}\n")

        f.write("\n## 2. High-Density Entity & Topic Tag Counts\n")
        f.write("| Entity / Topic Handle | Mention Count |\n|---|---|\n")
        for handle, count in handle_matches.most_common():
            f.write(f"| `{handle.title()}` | {count} |\n")

        f.write("\n## 3. Unindexed / Non-Standard Title Entries\n")
        for vid, title in unindexed:
            f.write(f"- [`{vid}`] {title}\n")

    conn.close()
    print(f"[+] Analysis complete. FTS5 table created and report saved to {output_path}")

if __name__ == "__main__":
    build_fts_and_analyze()
