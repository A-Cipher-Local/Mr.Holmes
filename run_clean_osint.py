import sqlite3
import re

DB_PATH = "pesci_intelligence.db"

def extract_dossier():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query database
    cursor.execute("""
        SELECT video_id, upload_date, title 
        FROM stream_archives 
        WHERE title LIKE '%Beyond%' 
        ORDER BY rowid ASC;
    """)
    records = cursor.fetchall()
    conn.close()

    known_entities = [
        "Nicholas DeOrio", "Keem", "Boogie", "Tammy", 
        "Scooter", "Morning Star", "YoMama", "Wonder Woman"
    ]

    found_entities = set()
    fractional_episodes = []
    formatting_issues = []

    for vid, u_date, title in records:
        # 1. Entity Extraction
        for entity in known_entities:
            if entity.lower() in title.lower():
                found_entities.add(entity)

        # 2. Numbering Anomalies (.5 / ½ releases)
        if "½" in title or ".5" in title:
            fractional_episodes.append((vid, title))
        elif not re.search(r'Ep\.\s*\d+', title, re.IGNORECASE):
            formatting_issues.append((vid, title))

    # Write clean output report directly to file
    with open("osint_intelligence_dossier.md", "w") as f:
        f.write("# OSINT Reconnaissance Dossier: Beyond The Pit\n\n")
        
        f.write("## 1. Verified Target Entities & Personalities Mentioned\n")
        for entity in sorted(found_entities):
            f.write(f"- {entity}\n")
        
        f.write("\n## 2. Fractional Releases & Interstitial Episodes (.5 Arcs)\n")
        for vid, title in fractional_episodes:
            f.write(f"- [`{vid}`] {title}\n")
            
        f.write("\n## 3. Title Formatting Anomalies & Non-Standard Prefixes\n")
        for vid, title in formatting_issues:
            f.write(f"- [`{vid}`] {title}\n")
            
        f.write(f"\n---\n*Total Database Streams Processed: {len(records)}*\n")

    print("[+] Successfully generated: osint_intelligence_dossier.md")

if __name__ == "__main__":
    extract_dossier()
