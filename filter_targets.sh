#!/usr/bin/env bash
set -e

# ==============================================================================
# Filter Timeline Telemetry for Primary Nodes: @wonderosa & @og_grim
# ==============================================================================

TIMELINE_PATH="GUI/Reports/universal_chronological_timeline.json"
OUTPUT_PATH="GUI/Reports/priority_targets_timeline.json"

python3 - << 'PYEOF'
import json
import os
import re

timeline_path = "GUI/Reports/universal_chronological_timeline.json"
output_path = "GUI/Reports/priority_targets_timeline.json"

if not os.path.exists(timeline_path):
    print(f"[-] Error: {timeline_path} not found.")
    exit(1)

with open(timeline_path, "r", encoding="utf-8") as f:
    events = json.load(f)

targets = {"wonderosa", "og_grim"}
matched_events = []

for event in events:
    # Check all possible text fields
    text = str(event.get("context", event.get("content", event.get("text", ""))))
    mentions = {m.lower() for m in re.findall(r"@([A-Za-z0-9_]+)", text)}
    
    # Check for direct handle matches in context
    if targets.intersection(mentions) or any(t in text.lower() for t in targets):
        matched_events.append(event)

# Write targeted report
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matched_events, f, indent=2)

print(f"[+] Found {len(matched_events)} matching target events for @wonderosa and @og_grim.")
print(f"[+] Isolated timeline report saved to {output_path}")

print("\n--- SAMPLE INTERACTION TELEMETRY ---")
for idx, ev in enumerate(matched_events[:5], 1):
    ts = ev.get("timestamp", "N/A")
    ctx = str(ev.get("context", ev.get("content", "")))[:100]
    print(f"{idx}. [{ts}] -> {ctx}")
PYEOF

