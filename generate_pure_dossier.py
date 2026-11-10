import sqlite3

DB_PATH = "pesci_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT video_id, upload_date, title FROM stream_archives ORDER BY rowid ASC;")
records = cursor.fetchall()
conn.close()

with open("pure_intelligence_dossier.md", "w") as f:
    f.write("# PROJECT ARGUS: Pure 'Beyond the Pit' Intelligence Dossier\n\n")
    f.write("| Index | Video ID | Upload Date | Title |\n")
    f.write("|---|---|---|---|\n")
    
    for idx, (vid, date, title) in enumerate(records, 1):
        u_date = date if date else "N/A"
        f.write(f"| {idx} | `{vid}` | {u_date} | {title} |\n")

print("[+] Successfully generated pure_intelligence_dossier.md")
