#!/usr/bin/env bash
set -e

DB_PATH="pesci_intelligence.db"
JSON_DUMP="pesci_intelligence_full_dump.json"
HTML_DASH="entity_matrix_dashboard.html"

echo "=== [PROJECT ARGUS] Starting Master Pipeline Fix ==="

if [ ! -f "$DB_PATH" ]; then
    echo "[-] Error: Database $DB_PATH not found in current directory."
    exit 1
fi

# 1. Purge noise and lock records to verified 'Beyond' series
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
cursor.execute('DELETE FROM stream_archives WHERE title NOT LIKE \"%Beyond%\";')
conn.commit()
cursor.execute('SELECT COUNT(*) FROM stream_archives;')
count = cursor.fetchone()[0]
conn.close()
print(f'[+] Database sanitized. Verified active records: {count}')
"

# 2. Rebuild FTS5 Virtual Table
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS stream_fts;')
cursor.execute('''
    CREATE VIRTUAL TABLE stream_fts USING fts5(
        video_id, 
        upload_date, 
        title, 
        description
    );
''')
cursor.execute('''
    INSERT INTO stream_fts(video_id, upload_date, title, description)
    SELECT video_id, COALESCE(upload_date, 'N/A'), title, COALESCE(description, '') 
    FROM stream_archives;
''')
conn.commit()
conn.close()
print('[+] FTS5 virtual table rebuilt successfully.')
"

# 3. Export Full JSON Master Dump
python3 -c "
import sqlite3, json
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
cursor.execute('SELECT rowid, video_id, upload_date, title, COALESCE(description, \'\'), COALESCE(transcript, \'\') FROM stream_archives ORDER BY rowid ASC;')
rows = cursor.fetchall()
conn.close()

archive_data = [{
    'rowid': r[0], 'video_id': r[1], 'upload_date': r[2] if r[2] else None,
    'title': r[3], 'description': r[4], 'transcript': r[5] if r[5] else None,
    'url': f'https://www.youtube.com/watch?v={r[1]}'
} for r in rows]

payload = {'project': 'PROJECT ARGUS', 'total_records': len(archive_data), 'records': archive_data}
with open('$JSON_DUMP', 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)
print(f'[+] Exported fresh JSON dump to $JSON_DUMP')
"

# 4. Generate Responsive HTML Matrix Dashboard with YouTube Embeds
python3 -c "
import json, os

JSON_PATH = '$JSON_DUMP'
OUTPUT_HTML = '$HTML_DASH'
TARGET_ENTITIES = ['Boogie', 'Keem', 'Morning Star', 'Nicholas DeOrio', 'Scooter', 'Tammy', 'Wonder Woman', 'YoMama']

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
records = data.get('records', [])

html = f'''<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>PROJECT ARGUS - Entity Co-Occurrence Matrix</title>
    <style>
        body {{ font-family: monospace; background: #121212; color: #00ff66; padding: 20px; }}
        h1, h2 {{ border-bottom: 2px solid #00ff66; padding-bottom: 5px; }}
        p {{ color: #888; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #333; padding: 10px; text-align: center; }}
        th {{ background: #1a1a1a; color: #00ff66; position: sticky; top: 0; }}
        td.title-col {{ text-align: left; }}
        tr:nth-child(even) {{ background: #181818; }}
        tr:hover {{ background: #222; }}
        .hit {{ background: #00ff66; color: #121212; font-weight: bold; }}
        .none {{ color: #444; }}
        a {{ color: #00bcff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .embed-container {{ display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px; }}
        .embed-box {{ background: #181818; border: 1px solid #333; padding: 15px; }}
    </style>
</head>
<body>
    <h1>[+] PROJECT ARGUS - ENTITY MAPPING MATRIX</h1>
    <p>Mapping verified target entities across all {len(records)} 'Beyond the Pit' archives.</p>
    <table>
        <thead>
            <tr>
                <th>Row</th>
                <th>Video ID</th>
                <th>Episode Title</th>
'''
for entity in TARGET_ENTITIES:
    html += f'                <th>{entity}</th>\n'
html += '''            </tr>
        </thead>
        <tbody>
'''

for r in records:
    title = r['title']
    vid = r['video_id']
    rowid = r['rowid']
    text_corpus = f\"{title} {r['description']}\".lower()

    html += f'            <tr>\n'
    html += f'                <td>{rowid}</td>\n'
    html += f'                <td><a href=\"https://youtube.com/watch?v={vid}\" target=\"_blank\">{vid}</a></td>\n'
    html += f'                <td class=\"title-col\">{title}</td>\n'

    for entity in TARGET_ENTITIES:
        if entity.lower() in text_corpus:
            html += f'                <td class=\"hit\">X</td>\n'
        else:
            html += f'                <td class=\"none\">-</td>\n'
    html += f'            </tr>\n'

html += '''        </tbody>
    </table>
    <div style=\"margin-top: 40px;\">
        <h2>[+] KEY CO-OCCURRENCE NODE EMBEDS</h2>
        <div class=\"embed-container\">
            <div class=\"embed-box\">
                <h3>Ep. 19: Nicholas DeOrio & Keem</h3>
                <iframe width=\"420\" height=\"236\" src=\"https://www.youtube.com/embed/EZ-x2Azc_GA\" frameborder=\"0\" allowfullscreen></iframe>
            </div>
            <div class=\"embed-box\">
                <h3>Ep. 9: Morning Star & Scooter</h3>
                <iframe width=\"420\" height=\"236\" src=\"https://www.youtube.com/embed/V6wVRk0tGNI\" frameborder=\"0\" allowfullscreen></iframe>
            </div>
        </div>
    </div>
</body>
</html>
'''

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'[+] Successfully generated updated dashboard: {OUTPUT_HTML}')
"

echo "=== [PROJECT ARGUS] Master Fix Pipeline Complete ==="
