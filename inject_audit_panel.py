import json
import os

HTML_PATH = "entity_matrix_dashboard.html"
JSON_PATH = "multi_entity_report.json"

def inject_panel():
    if not os.path.exists(HTML_PATH) or not os.path.exists(JSON_PATH):
        print("[-] Error: Dashboard HTML or JSON report missing.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        report = json.load(f)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Build HTML summary panel
    panel_html = f"""
    <div style="margin-top: 40px; background: #181818; border: 1px solid #00ff66; padding: 20px;">
        <h2>[+] MULTI-ENTITY CO-OCCURRENCE AUDIT SUMMARY</h2>
        <p><strong>Generated:</strong> {report.get('generated_timestamp', 'N/A')} | <strong>Total Nodes Found:</strong> {report.get('total_multi_entity_nodes', 0)}</p>
        <ul style="list-style-type: square; color: #00ff66; margin-top: 10px;">
"""

    for res in report.get("results", []):
        entities_str = ", ".join(res["matched_entities"])
        panel_html += f"""            <li style="margin-bottom: 8px;">
                <span style="color: #fff;">{res['title']}</span> 
                (<a href="{res['url']}" target="_blank">{res['video_id']}</a>) — 
                <strong style="color: #00bcff;">[{entities_str}]</strong>
            </li>\n"""

    panel_html += """        </ul>
    </div>
"""

    # Inject panel before closing body tag
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", f"{panel_html}\n</body>")
    else:
        html_content += panel_html

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Successfully injected multi-entity audit panel into {HTML_PATH}")

if __name__ == "__main__":
    inject_panel()
