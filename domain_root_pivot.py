import sqlite3
import json
import os
from collections import defaultdict
from urllib.parse import urlparse

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_REPORT = "GUI/Reports/domain_root_pivot_report.json"

def get_root_domain(url):
    try:
        parsed = urlparse(url if "://" in url else f"http://{url}")
        netloc = parsed.netloc.lower()
        if not netloc and parsed.path:
            netloc = parsed.path.split("/")[0].lower()
        parts = netloc.split(".")
        if len(parts) > 2:
            return ".".join(parts[-2:])
        return netloc
    except Exception:
        return None

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Pull all URL indicators
    cursor.execute("SELECT source_file, indicator_value FROM indicators WHERE indicator_type = 'urls'")
    rows = cursor.fetchall()
    conn.close()

    domain_to_files = defaultdict(set)
    file_to_domains = defaultdict(set)

    for source_file, url in rows:
        root_dom = get_root_domain(url)
        if root_dom:
            domain_to_files[root_dom].add(source_file)
            file_to_domains[source_file].add(root_dom)

    print(f"[*] Analyzed URLs across files. Found {len(domain_to_files)} unique root domains.")

    # Filter for domains appearing across multiple different source files
    shared_infrastructure = []
    for dom, files in domain_to_files.items():
        if len(files) > 1:
            shared_infrastructure.append({
                "root_domain": dom,
                "file_count": len(files),
                "connected_files": list(files)
            })

    shared_infrastructure.sort(key=lambda x: x["file_count"], reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(shared_infrastructure, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Domain infrastructure analysis complete. Saved to {OUTPUT_REPORT}")
    print("\n--------------------------------------------------")
    print("SHARED ROOT DOMAINS ACROSS MULTIPLE FILES:")
    print("--------------------------------------------------")

    if not shared_infrastructure:
        print("    [-] No shared root domains span across multiple files.")
        return

    for item in shared_infrastructure[:10]:
        print(f"[DOM] {item['root_domain']} (Found in {item['file_count']} files)")
        for f in item['connected_files']:
            print(f"  - {f}")
        print()

if __name__ == "__main__":
    main()
