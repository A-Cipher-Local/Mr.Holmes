import sqlite3

DB_PATH = "GUI/Database/osint_intelligence.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT source_file, substr(content, 1, 300) FROM artifacts LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    print("--------------------------------------------------")
    print("SAMPLE ARTIFACT PREVIEWS:")
    print("--------------------------------------------------")
    for source, snippet in rows:
        print(f"[FILE] {source}")
        print(f"Snippet:\n{snippet.strip()}")
        print("-" * 50)

if __name__ == "__main__":
    main()
