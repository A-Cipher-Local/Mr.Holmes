#!/usr/bin/env bash
# ==============================================================================
# Script: harvest_descriptions.sh
# Description: Fetch missing video descriptions & upload dates for pesci_intelligence.db
# ==============================================================================

DB_FILE="pesci_intelligence.db"
LOG_FILE="description_harvest.log"

echo "[*] Initializing database schema..." | tee -a "$LOG_FILE"

# Ensure column exists without throwing errors
sqlite3 "$DB_FILE" "ALTER TABLE stream_archives ADD COLUMN description TEXT;" 2>/dev/null

# Fetch list of video IDs needing update
VIDEO_IDS=$(sqlite3 "$DB_FILE" "SELECT video_id FROM stream_archives WHERE description IS NULL OR description = '' OR upload_date = 'N/A';")

TOTAL_VIDS=$(echo "$VIDEO_IDS" | wc -l)
echo "[*] Found $TOTAL_VIDS records requiring metadata update..." | tee -a "$LOG_FILE"

COUNTER=1
for vid in $VIDEO_IDS; do
    if [ -n "$vid" ]; then
        echo "[$COUNTER/$TOTAL_VIDS] Querying YouTube metadata for ID: $vid..." | tee -a "$LOG_FILE"
        
        # Pull single video JSON metadata payload
        JSON_PAYLOAD=$(yt-dlp --dump-json --skip-download "https://www.youtube.com/watch?v=$vid" 2>> "$LOG_FILE")
        
        if [ -n "$JSON_PAYLOAD" ]; then
            date=$(echo "$JSON_PAYLOAD" | jq -r '.upload_date // "N/A"')
            desc=$(echo "$JSON_PAYLOAD" | jq -r '.description // ""' | sed "s/'/''/g")
            
            sqlite3 "$DB_FILE" <<EOF
UPDATE stream_archives 
SET upload_date = CASE WHEN upload_date = 'N/A' OR upload_date IS NULL THEN '$date' ELSE upload_date END,
    description = '$desc'
WHERE video_id = '$vid';
EOF
            echo "  [+] Updated $vid -> Date: $date | Desc Length: ${#desc} chars" | tee -a "$LOG_FILE"
        else
            echo "  [!] Failed to pull metadata for $vid" | tee -a "$LOG_FILE"
        fi
        COUNTER=$((COUNTER + 1))
    fi
done

echo "[*] Regenerating clean Markdown catalog with dates and metadata..." | tee -a "$LOG_FILE"

sqlite3 -header -markdown "$DB_FILE" "
SELECT 
    upload_date AS Date, 
    video_id AS Video_ID, 
    title AS Title,
    LENGTH(description) AS Desc_Length
FROM stream_archives 
WHERE title LIKE '%Beyond%' 
ORDER BY upload_date ASC;
" > beyond_the_pit_catalog.md

echo "[+] Harvest complete! File updated: beyond_the_pit_catalog.md" | tee -a "$LOG_FILE"
