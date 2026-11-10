import sqlite3
import re
from collections import defaultdict

DB_PATH = "GUI/Database/osint_intelligence.db"

# Refined handle regex (excluding code decorators)
HANDLE_REGEX = r"@[a-zA-Z0-9_]{3,30}"
IGNORED_HANDLES = {"@staticmethod", "@ECHO", "@gmail", "@set", "@echo", "@if", "@for", "@include", "@import"}

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source_file, content FROM artifacts")
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Analyzing {len(rows)} artifact files for handle co-occurrences...\n")

    # Mapping: handle -> set of source files where it appears
    handle_to_files = defaultdict(set)
    # Mapping: source_file -> set of handles found within it
    file_to_handles = defaultdict(set)

    for source_file, content in rows:
        if not content:
            continue
        matches = set(re.findall(HANDLE_REGEX, content))
        clean_handles = {h for h in matches if h not in IGNORED_HANDLES}
        
        for handle in clean_handles:
            handle_to_files[handle].add(source_file)
            file_to_handles[source_file].add(handle)

    print("========================================")
    print("[*] Handles appearing across MULTIPLE files (Cross-References):")
    print("========================================")
    cross_refs_found = False
    for handle, files in handle_to_files.items():
        if len(files) > 1:
            cross_refs_found = True
            print(f"\n[+] Handle: {handle} (Found in {len(files)} files)")
            for f in files:
                print(f"    - {f}")

    if not cross_refs_found:
        print("    [-] No individual handles span across multiple isolated files in this batch.")

    print("\n========================================")
    print("[*] File Co-Occurrence Summary:")
    print("========================================")
    for source_file, handles in file_to_handles.items():
        if handles:
            print(f"\nFile: {source_file}")
            print(f"    Handles ({len(handles)}): {', '.join(list(handles)[:10])}{'...' if len(handles) > 10 else ''}")

if __name__ == "__main__":
    main()
