import sqlite3
import re
from collections import Counter

DB_PATH = "pesci_intelligence.db"

def run_deep_audit():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Fetch all available stream records
    cursor.execute("SELECT rowid, video_id, upload_date, title, description FROM stream_archives;")
    rows = cursor.fetchall()

    print(f"[+] Total records loaded from database: {len(rows)}")

    # 2. Episode Number Extraction & Gap Analysis
    ep_numbers = []
    title_words = []
    
    for rowid, vid, date, title, desc in rows:
        # Extract episode number patterns (e.g., Ep. 14, ep3, etc.)
        match = re.search(r'(?:ep\.?|episode)\s*(\d+(?:\½|\.5)?)', title, re.IGNORECASE)
        if match:
            ep_numbers.append((match.group(1), vid, title))
        
        # Tokenize titles for frequency analysis (excluding stop words)
        clean_title = re.sub(r'[^\w\s]', '', title).lower()
        words = [w for w in clean_title.split() if w not in ['beyond', 'the', 'pit', 'ep', 'a', 'to', 'of']]
        title_words.extend(words)

    # 3. Frequency Analysis of Hidden Terms
    word_counts = Counter(title_words)

    # 4. Write High-Density Intelligence Report
    report_path = "hidden_intelligence_report.md"
    with open(report_path, "w") as f:
        f.write("# PROJECT ARGUS: Deep Intelligence Audit & Hidden Data Extraction\n\n")
        
        f.write("## 1. High-Frequency Title Keywords & Thematic Clusters\n")
        f.write("Terms appearing across stream titles indicating recurring narrative motifs:\n\n")
        f.write("| Keyword | Frequency |\n|---|---|\n")
        for word, count in word_counts.most_common(10):
            f.write(f"| `{word}` | {count} |\n")

        f.write("\n## 2. Sequenced Episode Index & Metadata Audit\n")
        f.write("| Row | Video ID | Upload Date | Title |\n|---|---|---|---|\n")
        for rowid, vid, date, title, desc in rows:
            u_date = date if date else "N/A"
            f.write(f"| {rowid} | `{vid}` | {u_date} | {title} |\n")

    print(f"[+] Deep audit complete. Generated structured report: {report_path}")
    conn.close()

if __name__ == "__main__":
    run_deep_audit()
