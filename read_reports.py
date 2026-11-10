import json
import os

reports_dir = "GUI/Reports"
print("[*] Inspecting intelligence report contents...\n")

dossier_path = os.path.join(reports_dir, "dossier_sweep_report.json")
if os.path.exists(dossier_path):
    print("=== DOSSIER SWEEP REPORT ===")
    try:
        with open(dossier_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error reading dossier report: {e}")

print("\n=== CATEGORY ARTIFACTS ===")
for category in ["Usernames", "Websites", "E-Mail", "Phone", "People", "Dorks", "Ports"]:
    p = os.path.join(reports_dir, category)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()
                display_content = content if content else "(Empty)"
                print(f"[{category}] -> {display_content}")
        except Exception as e:
            print(f"[{category}] -> Error: {e}")
