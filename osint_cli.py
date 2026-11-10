import sqlite3
import sys

DB_PATH = "GUI/Database/osint_intelligence.db"

def print_banner():
    print("=" * 60)
    print("       MR. HOLMES OSINT INTELLIGENCE PIVOT CONSOLE       ")
    print("=" * 60)

def search_indicator(cursor, term):
    print(f"\n[*] Searching for indicator matching: '{term}'...\n")
    query = """
        SELECT source_file, indicator_type, indicator_value 
        FROM indicators 
        WHERE indicator_value LIKE ? OR indicator_type LIKE ?
    """
    cursor.execute(query, (f"%{term}%", f"%{term}%"))
    results = cursor.fetchall()
    
    if not results:
        print("    [-] No matching indicators found.")
        return

    print(f"    [+] Found {len(results)} matches:")
    for source, ind_type, ind_val in results:
        print(f"      - [{ind_type.upper()}] {ind_val}")
        print(f"        Source File: {source}")
    print()

def file_pivot(cursor, filename):
    print(f"\n[*] Pivoting on file: '{filename}'...\n")
    query = """
        SELECT indicator_type, indicator_value 
        FROM indicators 
        WHERE source_file LIKE ?
    """
    cursor.execute(query, (f"%{filename}%",))
    results = cursor.fetchall()

    if not results:
        print("    [-] No indicators found for this file.")
        return

    print(f"    [+] Indicators extracted from {filename} ({len(results)} total):")
    for ind_type, ind_val in results:
        print(f"      - [{ind_type.upper()}] {ind_val}")
    print()

def main():
    if not sqlite3.connect(DB_PATH):
        print(f"[-] Error: Could not connect to database at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print_banner()
    
    while True:
        print("\nCommands:")
        print("  1. search <indicator/term>  - Search for emails, handles, or URLs")
        print("  2. pivot <filename>         - List all indicators inside a specific file")
        print("  3. stats                    - Show database summary counts")
        print("  4. exit                     - Quit console")
        
        try:
            choice = input("\nosint_cli> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting console.")
            break

        if not choice:
            continue

        parts = choice.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "exit":
            print("[*] Closing intelligence console.")
            break
        elif cmd == "search":
            if not arg:
                print("[-] Error: Please provide a search term (e.g., search lukege287)")
                continue
            search_indicator(cursor, arg)
        elif cmd == "pivot":
            if not arg:
                print("[-] Error: Please provide a filename to pivot on.")
                continue
            file_pivot(cursor, arg)
        elif cmd == "stats":
            cursor.execute("SELECT COUNT(DISTINCT source_file) FROM indicators")
            file_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM indicators")
            ind_count = cursor.fetchone()[0]
            print(f"\n[+] Database Stats:")
            print(f"    - Indexed Source Files: {file_count}")
            print(f"    - Total Extracted Indicators: {ind_count}\n")
        else:
            print("[-] Unknown command. Type 'search', 'pivot', 'stats', or 'exit'.")

    conn.close()

if __name__ == "__main__":
    main()
