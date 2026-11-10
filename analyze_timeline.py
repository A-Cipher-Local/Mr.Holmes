import json
import os
from collections import Counter

TIMELINE_PATH = "GUI/Reports/master_chronological_timeline.json"

def main():
    if not os.path.exists(TIMELINE_PATH):
        print(f"[-] Error: Timeline report not found at {TIMELINE_PATH}")
        return

    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    print(f"[*] Analyzing {len(events)} chronological events...")

    sources = Counter()
    years = Counter()

    for event in events:
        sources[event["source_file"]] += 1
        # Extract 4-digit year from timestamp string if present
        ts = event["timestamp"]
        year_match = ts[-4:] if len(ts) >= 4 else "Unknown"
        years[year_match] += 1

    print("\n--------------------------------------------------")
    print("EVENTS BY SOURCE FILE:")
    print("--------------------------------------------------")
    for src, count in sources.most_common():
        print(f"  - {src}: {count} temporal events")

    print("\n--------------------------------------------------")
    print("ACTIVITY SPREAD BY YEAR:")
    print("--------------------------------------------------")
    for yr, count in sorted(years.items()):
        print(f"  - {yr}: {count} events")

if __name__ == "__main__":
    main()
