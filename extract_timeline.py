import sqlite3
import re
import os
import json

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_TIMELINE = "GUI/Reports/master_chronological_timeline.json"

# Expanded date/timestamp regex patterns including Twitter/X created_at formats
TIMESTAMP_PATTERNS = [
    r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} \d{2}:\d{2}:\d{2} \+\d{4} \d{4}\b", # Twitter CSV (e.g. Tue Nov 24 14:04:56 +0000 2015)
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?", # ISO 8601
    r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}", # YYYY/MM/DD HH:MM:SS
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b", # Month DD, YYYY
    r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}" # MM/DD/YYYY HH:MM:SS
]

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source_file, content FROM artifacts")
    artifacts = cursor.fetchall()
    conn.close()

    print(f"[*] Scanning {len(artifacts)} files for temporal markers...")
    timeline_events = []

    for filename, content in artifacts:
        if not content:
            continue
        for pattern in TIMESTAMP_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                timestamp_str = match.group(0)
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip().replace("\n", " ")

                timeline_events.append({
                    "timestamp": timestamp_str,
                    "source_file": filename,
                    "context": context
                })

    # Deduplicate events based on timestamp + context
    seen = set()
    unique_events = []
    for ev in timeline_events:
        identifier = (ev["timestamp"], ev["context"])
        if identifier not in seen:
            seen.add(identifier)
            unique_events.append(ev)

    os.makedirs(os.path.dirname(OUTPUT_TIMELINE), exist_ok=True)
    with open(OUTPUT_TIMELINE, "w", encoding="utf-8") as out:
        json.dump(unique_events, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Timeline extraction complete. Saved {len(unique_events)} events to {OUTPUT_TIMELINE}")
    print("\n--------------------------------------------------")
    print("EXTRACTED TIMELINE EVENTS (SAMPLE):")
    print("--------------------------------------------------")
    
    if not unique_events:
        print("    [-] No temporal markers detected.")
        return

    for event in unique_events[:10]:
        print(f"[{event['timestamp']}] ({event['source_file']})")
        print(f"  Context: ...{event['context']}...\n")

if __name__ == "__main__":
    main()
