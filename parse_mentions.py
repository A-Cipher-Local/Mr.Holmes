import re
import json
import os
from collections import Counter

TIMELINE_PATH = "GUI/Reports/universal_chronological_timeline.json"
RAW_CSV_PATH = "TammyBUsagi_data_postings_80769774.csv.txt"

def main():
    events = []
    if os.path.exists(TIMELINE_PATH):
        print(f"[*] Reading timeline from {TIMELINE_PATH}...")
        with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Print keys of the first record to debug structure if needed
            if data and isinstance(data, list):
                print(f"[*] Sample event keys: {list(data[0].keys())}")
                events = data
    else:
        print("[-] Timeline JSON not found.")
        return

    mentions = Counter()
    urls = Counter()

    for event in events:
        # Check all possible text keys used in timeline exports
        text_content = ""
        for key in ["content", "text", "message", "post", "body"]:
            if key in event and event[key]:
                text_content = str(event[key])
                break
        
        if not text_content:
            # Fallback: join all string values in the event dict
            text_content = " ".join([str(v) for v in event.values() if isinstance(v, str)])

        # Extract handle mentions
        found_mentions = re.findall(r"@([A-Za-z0-9_]+)", text_content)
        for m in found_mentions:
            mentions[m.lower()] += 1
        
        # Extract embedded URLs
        found_urls = re.findall(r"(https?://\S+)", text_content)
        for u in found_urls:
            urls[u] += 1

    print("\n--------------------------------------------------")
    print(f"TOP MENTIONED HANDLES (Total unique: {len(mentions)}):")
    print("--------------------------------------------------")
    for handle, count in mentions.most_common(10):
        print(f"  @{handle}: {count} occurrences")

    print("\n--------------------------------------------------")
    print(f"TOP EMBEDDED URLS (Total unique: {len(urls)}):")
    print("--------------------------------------------------")
    for url, count in urls.most_common(10):
        print(f"  {url}: {count} occurrences")

if __name__ == "__main__":
    main()
