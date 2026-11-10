import sqlite3
import re
from collections import defaultdict
from urllib.parse import urlparse

DB_PATH = "GUI/Database/osint_intelligence.db"
URL_REGEX = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w ./?%&=-]*"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source_file, content FROM artifacts")
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Analyzing {len(rows)} artifact files for domain and URL cross-references...\n")

    domain_to_files = defaultdict(set)
    file_to_domains = defaultdict(set)

    for source_file, content in rows:
        if not content:
            continue
        urls = re.findall(URL_REGEX, content)
        for url in urls:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
                if domain:
                    domain_to_files[domain].add(source_file)
                    file_to_domains[source_file].add(domain)
            except Exception:
                continue

    print("========================================")
    print("[*] Domains appearing across MULTIPLE files:")
    print("========================================")
    cross_refs_found = False
    for domain, files in domain_to_files.items():
        if len(files) > 1:
            cross_refs_found = True
            print(f"\n[+] Domain: {domain} (Found in {len(files)} files)")
            for f in files:
                print(f"    - {f}")

    if not cross_refs_found:
        print("    [-] No shared domains span across multiple files in this batch.")

if __name__ == "__main__":
    main()
