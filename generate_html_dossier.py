import sqlite3
import json

DB_PATH = "pesci_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    SELECT video_id, upload_date, title, COALESCE(description, '') 
    FROM stream_archives 
    WHERE title LIKE '%Beyond%' 
    ORDER BY rowid ASC;
""")
rows = cursor.fetchall()
conn.close()

data = [
    {
        "id": r[0],
        "date": r[1] or "N/A",
        "title": r[2],
        "desc": r[3]
    }
    for r in rows
]

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Beyond The Pit - Intelligence Dossier</title>
    <style>
        body {{ font-family: monospace; background: #121212; color: #00ff66; padding: 20px; }}
        h1 {{ border-bottom: 2px solid #00ff66; padding-bottom: 5px; }}
        input {{ width: 100%; padding: 10px; background: #222; color: #fff; border: 1px solid #00ff66; margin-bottom: 20px; box-sizing: border-box; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #333; padding: 8px 12px; text-align: left; }}
        th {{ background: #1a1a1a; color: #00ff66; }}
        tr:nth-child(even) {{ background: #181818; }}
        tr:hover {{ background: #252525; }}
        a {{ color: #00bcff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>[+] PROJECT ARGUS - BEYOND THE PIT INTELLIGENCE DOSSIER</h1>
    <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Search titles, video IDs, or dates...">
    
    <table id="dossierTable">
        <thead>
            <tr>
                <th>Index</th>
                <th>Video ID</th>
                <th>Date</th>
                <th>Title</th>
            </tr>
        </thead>
        <tbody>
"""

for idx, item in enumerate(data, 1):
    html_content += f"""
            <tr>
                <td>{idx}</td>
                <td><a href="https://youtube.com/watch?v={item['id']}" target="_blank">{item['id']}</a></td>
                <td>{item['date']}</td>
                <td>{item['title']}</td>
            </tr>"""

html_content += """
        </tbody>
    </table>

    <script>
        function filterTable() {
            var input = document.getElementById("searchInput");
            var filter = input.value.toLowerCase();
            var trs = document.getElementById("dossierTable").getElementsByTagName("tr");
            
            for (var i = 1; i < trs.length; i++) {
                var text = trs[i].textContent.toLowerCase();
                trs[i].style.display = text.indexOf(filter) > -1 ? "" : "none";
            }
        }
    </script>
</body>
</html>
"""

with open("dossier_dashboard.html", "w") as f:
    f.write(html_content)

print(f"[+] Successfully generated dossier_dashboard.html with {len(data)} indexed entries.")
