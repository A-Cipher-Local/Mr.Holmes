#!/usr/bin/env bash
set -e

# ==============================================================================
# Export Entity Pivot Matrix to GEXF Network Graph File
# ==============================================================================

python3 - << 'PYEOF'
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

input_path = "GUI/Reports/entity_pivot_matrix.json"
output_path = "GUI/Reports/target_network.gexf"

if not os.path.exists(input_path):
    print(f"[-] Matrix file not found at {input_path}")
    exit(1)

with open(input_path, "r", encoding="utf-8") as f:
    pivots = json.load(f)

# Create GEXF XML structure
gexf = ET.Element("gexf", xmlns="http://www.gexf.net/1.2draft", version="1.2")
graph = ET.SubElement(gexf, "graph", defaultedgetype="undirected", mode="static")

nodes_elem = ET.SubElement(graph, "nodes")
edges_elem = ET.SubElement(graph, "edges")

node_set = set()
edge_id = 0

# Add Central Target Node
node_set.add("tammybusagi")
ET.SubElement(nodes_elem, "node", id="tammybusagi", label="@tammybusagi")

for p in pivots:
    indicator = p.get("indicator", "").lstrip("@").lower()
    if not indicator or indicator in ("youtube", "tammybusagi"):
        continue

    if indicator not in node_set:
        node_set.add(indicator)
        ET.SubElement(nodes_elem, "node", id=indicator, label=f"@{indicator}")
        
        # Draw edge to central target node
        weight = str(p.get("shared_source_count", 1))
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source="tammybusagi", target=indicator, weight=weight)
        edge_id += 1

# Format pretty XML output
raw_str = ET.tostring(gexf, encoding="utf-8")
parsed = minidom.parseString(raw_str)
pretty_xml = parsed.toprettyxml(indent="  ")

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print(f"[+] GEXF Network Graph Export Complete: {len(node_set)} nodes, {edge_id} edges.")
print(f"[+] Output saved to {output_path}")
PYEOF

