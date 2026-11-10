#!/usr/bin/env python3
import sqlite3
import sys
import os

DB_PATH = os.path.expanduser("~/llama.cpp/Mr.Holmes/tammy_memory.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_memory(source, content):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lore (source, content) VALUES (?, ?)", (source, content))
    conn.commit()
    conn.close()
    print(f"[+] Successfully ingested new lore from '{source}' into active memory.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 learn.py <source_name> '<text_content>'")
        sys.exit(1)
    
    source_name = sys.argv[1]
    text_content = sys.argv[2]
    add_memory(source_name, text_content)
