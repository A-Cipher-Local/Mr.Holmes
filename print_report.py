import json
import os

REPORT_PATH = "multi_entity_report.json"

if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(data, indent=2))
else:
    print(f"[-] Error: {REPORT_PATH} not found.")
