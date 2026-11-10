#!/usr/bin/env bash

DB_PATH="pesci_intelligence.db"
QUERY="${1:-Keem}"

if [ ! -f "$DB_PATH" ]; then
    echo "[-] Error: $DB_PATH not found in current directory."
    exit 1
fi

echo "=== FTS5 SEARCH RESULTS FOR: '$QUERY' ==="
sqlite3 "$DB_PATH" "
    SELECT video_id, upload_date, title 
    FROM stream_fts 
    WHERE stream_fts MATCH '$QUERY' 
    ORDER BY rank;
"
