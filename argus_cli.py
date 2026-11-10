import argparse
import sqlite3

DB_PATH = "pesci_intelligence.db"

def main():
    parser = argparse.ArgumentParser(description="Project Argus Intelligence CLI")
    parser.add_argument("-e", "--entity", help="Entity to search in stream archives")
    parser.add_argument("-k", "--keyword", help="Keyword to search in title/description")
    parser.add_argument("--query", help="Custom text search query string")
    parser.add_argument("-m", "--moderators", action="store_true", help="List or search logged moderators")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max results to display")
    
    args = parser.parse_args()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if args.moderators:
            cursor.execute("""
                SELECT id, handle, associated_entity, notes, timestamp 
                FROM moderators
                ORDER BY id DESC
                LIMIT ?
            """, (args.limit,))
            rows = cursor.fetchall()
            if rows:
                print(f"\n[+] Logged Moderators ({len(rows)} found):")
                print("=" * 65)
                for r in rows:
                    print(f"ID: {r[0]} | Handle: {r[1]} | Target: {r[2]}")
                    print(f"Notes: {r[3]} | Logged: {r[4]}")
                    print("-" * 65)
            else:
                print("[+] No moderators logged in database.")
        elif args.query or args.keyword or args.entity:
            term = args.query or args.keyword or args.entity
            cursor.execute("""
                SELECT rowid, video_id, upload_date, title, description 
                FROM stream_archives 
                WHERE title LIKE ? OR description LIKE ?
                LIMIT ?
            """, (f'%{term}%', f'%{term}%', args.limit))
            rows = cursor.fetchall()
            if rows:
                print(f"\n[+] Search Results for '{term}' ({len(rows)} matches found):")
                print("=" * 65)
                for r in rows:
                    print(f"RowID: {r[0]} | Video ID: {r[1]} | Date: {r[2]}")
                    print(f"Title: {r[3]}")
                    print(f"URL:   https://www.youtube.com/watch?v={r[1]}")
                    print("-" * 65)
            else:
                print(f"[+] No matching records found for '{term}'.")
        else:
            cursor.execute("""
                SELECT rowid, video_id, upload_date, title 
                FROM stream_archives 
                ORDER BY rowid DESC
                LIMIT ?
            """, (args.limit,))
            rows = cursor.fetchall()
            if rows:
                print(f"\n[+] Recent Stream Archives ({len(rows)} records):")
                print("=" * 65)
                for r in rows:
                    print(f"RowID: {r[0]} | Video ID: {r[1]} | Date: {r[2]}")
                    print(f"Title: {r[3]}")
                    print("-" * 65)
            else:
                print("[+] Stream archives table is empty.")

    except Exception as e:
        print(f"[-] Query execution error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
