import sqlite3
import datetime

def export_dossier():
    db_path = "pesci_intelligence.db"
    out_file = "THE_LOLCOW_UNIVERSE_v2.9.2_MASTER.md"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Dynamically query moderators table without hardcoding column names
    cursor.execute("SELECT * FROM moderators")
    mods = cursor.fetchall()
    
    # Query stream archives
    cursor.execute("SELECT rowid, video_id, title, description FROM stream_archives")
    archives = cursor.fetchall()
    
    # Query FTS records for target keywords
    cursor.execute("SELECT * FROM stream_fts WHERE stream_fts MATCH 'tammy* OR tammyten*'")
    fts_matches = cursor.fetchall()
    
    conn.close()
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc = f"# PROJECT ARGUS - MASTER INTELLIGENCE DOSSIER\n"
    doc += f"**Package ID:** THE_LOLCOW_UNIVERSE_v2.9.2_MASTER  \n"
    doc += f"**Generated:** {now}  \n"
    doc += f"**Database Repository:** `pesci_intelligence.db`  \n\n"
    
    doc += "## 1. Target & Moderator Profiles\n"
    for m in mods:
        doc += f"- {m}\n"
        
    doc += "\n## 2. Indexed Stream Archives Telemetry\n"
    doc += "| RowID | Video ID | Title | Description |\n"
    doc += "|---|---|---|---|\n"
    for a in archives:
        doc += f"| {a[0]} | `{a[1]}` | {a[2]} | {a[3]} |\n"
        
    doc += "\n## 3. Verified Co-Occurrence Sweep Results (`tammy*` / `tammyten*` FTS)\n"
    for idx, f in enumerate(fts_matches, 1):
        doc += f"### Match #{idx}\n"
        doc += f"- **Video ID:** `{f[0]}`\n"
        doc += f"- **Title:** {f[2]}\n"
        doc += f"- **Summary/Sweep Details:** {f[3]}\n\n"
        
    with open(out_file, "w") as f_out:
        f_out.write(doc)
        
    print(f"[+] Successfully exported master dossier to '{out_file}'")

if __name__ == "__main__":
    export_dossier()
