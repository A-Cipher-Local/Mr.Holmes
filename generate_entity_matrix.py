import json
import os

JSON_PATH = "pesci_intelligence_full_dump.json"
OUTPUT_HTML = "entity_matrix_dashboard.html"

TARGET_ENTITIES = [
    "Boogie", "Keem", "Morning Star", "Nicholas DeOrio", 
    "Scooter", "Tammy", "Wonder Woman", "YoMama"
]

def build_matrix():
    if not os.path.exists(JSON_PATH):
        print(f"[-] Error: {JSON_PATH} not found. Run your full database export script first.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = data.get("records", [])

    # HTML Header and CSS styling
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PROJECT ARGUS - Entity Co-Occurrence Matrix</title>
    <style>
        body {{ font-family: monospace; background: #121212; color: #00ff66; padding: 20px; }}
        h1 {{ border-bottom: 2px solid #00ff66; padding-bottom: 5px; }}
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
"""

    for entity in TARGET_ENTITIES:
        html += f"                <th>{entity}</th>\n"

    html += """            </tr>
        </thead>
        <tbody>
"""

    for r in records:
        title = r["title"]
        vid = r["video_id"]
        rowid = r["rowid"]
        text_corpus = f"{title} {r['description']}".lower()

        html += f"            <tr>\n"
        html += f"                <td>{rowid}</td>\n"
        html += f"                <td><a href=\"https://youtube.com/watch?v={vid}\" target=\"_blank\">{vid}</a></td>\n"
        html += f"                <td class=\"title-col\">{title}</td>\n"

        for entity in TARGET_ENTITIES:
            if entity.lower() in text_corpus:
                html += f"                <td class=\"hit\">X</td>\n"
            else:
                html += f"                <td class=\"none\">-</td>\n"

        html += f"            </tr>\n"

    html += """        </tbody>
    </table>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Successfully generated entity matrix dashboard: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_matrix()
