#!/usr/bin/env python3
# ==============================================================================
# Build Co-occurrence Network Matrix and GEXF from Timeline Telemetry
# ==============================================================================

import json
import re
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict, Counter

TIMELINE_PATH = "GUI/Reports/universal_chronological_timeline.json"
OUTPUT_GEXF = "GUI/Reports/full_target_network.gexf"

def main():
    if not os.path.exists(TIMELINE_PATH):
        print(f"[-] Error: {TIMELINE_PATH} not found.")
        return

    print(f"[*] Reading timeline telemetry from {TIMELINE_PATH}...")
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    # Track edge weights between handles
    edge_weights = Counter()
    node_frequencies = Counter()

    for event in events:
        text = str(event.get("context", event.get("content", "")))
        # Extract all handles in this single event
        handles = sorted(list(set(m.lower() for m in re.findall(r"@([A-Za-z0-9_]+)", text))))
        
        # Filter out noise handles
        handles = [h for h in handles if h not in ("youtube",)]

        for h in handles:
            node_frequencies[h] += 1

        # If multiple handles appear in the same event, form co-occurrence edges
        if len(handles) > 1:
            for i in range(len(handles)):
                for j in range(i + 1, len(handles)):
                    pair = tuple(sorted((handles[i], handles[j])))
                    edge_weights[pair] += 1

    print(f"[+] Processed {len(node_frequencies)} unique handles and {len(edge_weights)} co-occurrence links.")

    # Generate GEXF
    gexf = ET.Element("gexf", xmlns="http://www.gexf.net/1.2draft", version="1.2")
    graph = ET.SubElement(gexf, "graph", defaultedgetype="undirected", mode="static")

    nodes_elem = ET.SubElement(graph, "nodes")
    edges_elem = ET.SubElement(graph, "edges")

    for node, freq in node_frequencies.items():
        ET.SubElement(nodes_elem, "node", id=node, label=f"@{node}")

    for edge_id, ((source, target), weight) in enumerate(edge_weights.items(), 1):
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source=source, target=target, weight=str(weight))

    raw_str = ET.tostring(gexf, encoding="utf-8")
    parsed = minidom.parseString(raw_str)
    pretty_xml = parsed.toprettyxml(indent="  ")

    os.makedirs(os.path.dirname(OUTPUT_GEXF), exist_ok=True)
    with open(OUTPUT_GEXF, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"[+] Advanced network graph exported to {OUTPUT_GEXF}")
    print("\n--- TOP CO-OCCURRING HANDLE PAIRS ---")
    for (h1, h2), weight in edge_weights.most_common(10):
        print(f"  @{h1} <---> @{h2} : {weight} shared interaction(s)")

if __name__ == "__main__":
    main()
