import sqlite3
import re
import os
import json

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_TIMELINE = "GUI/Reports/universal_chronological_timeline.json"

# Universal timestamp patterns covering logs, JSON timestamps, ISO dates, and standard strings
UNIVERSAL_PATTERNS = [
    r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} \d{2}:\d{2}:\d{2} \+\d{4} \d{4}\b", # Twitter CSV
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?", # ISO 8601 / JSON logs
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b", # Month DD, YYYY
    r"\b\d{4}/\d{2}/\d{2}\b", # YYYY/MM/DD
    r"\b\d{2}/\d{2}/\d{4}\b"  # MM/DD/YYYY
]

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source_file, content FROM artifacts")
    artifacts = cursor.fetchall()
    conn.close()

    print(f"[*] Parsing {len(artifacts)} files for universal chronological markers...")
    events = []

    for filename, content in artifacts:
        if not content:
            continue
        for pattern in UNIVERSAL_PATTERNS:
            for match in re.finditer(pattern, content):
                ts = match.group(0)
                start = max(0, match.start() - 40)
                end = min(len(content), match.end() + 40)
                context = content[start:end].strip().replace("\n", " ")

                events.append({
                    "timestamp": ts,
                    "source_file": filename,
                    "context": context
                })

    # Deduplicate
    seen = set()
    unique_events = []
    for ev in events:
        key = (ev["timestamp"], ev["context"])
        if key not in seen:
            seen.add(key)
            unique_events.append(ev)

    # Sort chronologically
    unique_events.sort(key=lambda x: x["timestamp"])

    os.makedirs(os.path.dirname(OUTPUT_TIMELINE), exist_ok=True)
    with open(OUTPUT_TIMELINE, "w", encoding="utf-8") as out:
        json.dump(unique_events, out, indent=2, ensure_ascii=False)

    print(f"\n[+] Universal extraction complete. Saved {len(unique_events)} events to {OUTPUT_TIMELINE}")

if __name__ == "__main__":
    main()
