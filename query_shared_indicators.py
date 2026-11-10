import sqlite3

DB_PATH = "GUI/Database/osint_intelligence.db"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query to find indicators appearing in more than 1 distinct file
    query = """
        SELECT indicator_type, indicator_value, COUNT(DISTINCT source_file) as file_count, GROUP_CONCAT(source_file, ', ')
        FROM indicators
        GROUP BY indicator_type, indicator_value
        HAVING file_count > 1
        ORDER BY file_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    print("\n========================================")
    print("[*] Indicators Shared Across Multiple Files:")
    print("========================================")
    
    if not results:
        print("    [-] No shared indicators found across multiple files in this batch.")
        return

    for ind_type, value, count, files in results:
        print(f"\n[+] Type: {ind_type.upper()} | Value: {value}")
        print(f"    - Found in {count} files:")
        for f in files.split(", "):
            print(f"      * {f}")

if __name__ == "__main__":
    main()
