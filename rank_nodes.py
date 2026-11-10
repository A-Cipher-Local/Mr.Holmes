#!/usr/bin/env python3
# ==============================================================================
# Parse target_network.gexf and Rank Nodes by Degree Centrality
# ==============================================================================

import xml.etree.ElementTree as ET
import os
from collections import defaultdict

GEXF_PATH = "GUI/Reports/target_network.gexf"

def main():
    if not os.path.exists(GEXF_PATH):
        print(f"[-] Error: {GEXF_PATH} not found.")
        return

    print(f"[*] Parsing network graph from {GEXF_PATH}...")
    tree = ET.parse(GEXF_PATH)
    root = tree.getroot()

    # XML namespaces in GEXF
    namespaces = {'gexf': 'http://www.gexf.net/1.2draft'}
    
    # Extract nodes (id -> label mapping)
    nodes = {}
    for node in root.findall('.//gexf:node', namespaces):
        nid = node.get('id')
        label = node.get('label', nid)
        nodes[nid] = label

    # Calculate degrees (connections per node)
    degrees = defaultdict(int)
    edge_count = 0
    
    for edge in root.findall('.//gexf:edge', namespaces):
        source = edge.get('source')
        target = edge.get('target')
        degrees[source] += 1
        degrees[target] += 1
        edge_count += 1

    print(f"[+] Graph loaded successfully: {len(nodes)} nodes, {edge_count} edges.\n")
    print("=" * 60)
    print(f"  TOP NODES RANKED BY DEGREE CENTRALITY")
    print("=" * 60)

    # Sort nodes by degree descending
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

    for rank, (nid, deg) in enumerate(sorted_nodes[:20], 1):
        label = nodes.get(nid, nid)
        print(f"  {rank:02d}. {label:<25} -> Degree Centrality: {deg} connection(s)")

if __name__ == "__main__":
    main()
