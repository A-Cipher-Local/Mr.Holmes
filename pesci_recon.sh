#!/usr/bin/env bash
# ==============================================================================
# Script Name: pesci_recon.sh
# Description: Resolved ID telemetry sweep for @SirJosephPesci
# ==============================================================================

DB_FILE="pesci_intelligence.db"
LOG_FILE="recon_execution.log"

echo "[*] Initializing telemetry index..." | tee -a "$LOG_FILE"

# Initialize SQLite database schema
sqlite3 "$DB_FILE" <<EOF
CREATE TABLE IF NOT EXISTS stream_archives (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    duration INTEGER,
    upload_date TEXT,
    indexed_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
EOF

# Use yt-dlp with explicit user agent and search-based query fallback for the handle
TARGET_URL="ytsearch50:SirJosephPesci Beyond The Pit"

echo "[*] Harvesting target metadata payload via search/channel index..." | tee -a "$LOG_FILE"

yt-dlp --flat-playlist --ignore-errors --dump-json "$TARGET_URL" 2>> "$LOG_FILE" | \
jq -c '{id: .id, title: .title, duration: (.duration // 0), date: (.upload_date // "N/A")}' | \
while read -r json_line; do
    vid=$(echo "$json_line" | jq -r '.id')
    title=$(echo "$json_line" | jq -r '.title' | sed "s/'/''/g")
    dur=$(echo "$json_line" | jq -r '.duration')
    date=$(echo "$json_line" | jq -r '.date')

    if [ -n "$vid" ] && [ "$vid" != "null" ]; then
        sqlite3 "$DB_FILE" "INSERT OR IGNORE INTO stream_archives (video_id, title, duration, upload_date) VALUES ('$vid', '$title', $dur, '$date');"
    fi
done

TOTAL_RECORDS=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM stream_archives;")
echo "[+] Recon complete. Successfully indexed $TOTAL_RECORDS assets into $DB_FILE." | tee -a "$LOG_FILE"
