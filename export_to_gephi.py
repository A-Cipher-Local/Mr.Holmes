import sqlite3
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

DB_PATH = "GUI/Database/osint_intelligence.db"
OUTPUT_GEXF = "GUI/Reports/osint_network_graph.gexf"

def main():
    print(f"[*] Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all source_file to indicator relationships
    cursor.execute("SELECT DISTINCT source_file, indicator_type, indicator_value FROM indicators")
    rows = cursor.fetchall()
    conn.close()

    print(f"[*] Processing {len(rows)} relational links for GEXF graph generation...")

    # Build GEXF XML Structure
    gexf = ET.Element("gexf", xmlns="http://www.gephi.org/gexf/1.2draft", version="1.2")
    graph = ET.SubElement(gexf, "graph", defaultedgetype="undirected", mode="static")
    
    # Define attributes for nodes
    attributes = ET.SubElement(graph, "attributes", class_="node")
    attr1 = ET.SubElement(attributes, "attribute", id="node_type", title="NodeType", type="string")

    nodes_el = ET.SubElement(graph, "nodes")
    edges_el = ET.SubElement(graph, "edges")

    node_set = set()
    edge_id = 1

    for source_file, ind_type, ind_value in rows:
        # Add source file node if not present
        if source_file not in node_set:
            node_set.add(source_file)
            n = ET.SubElement(nodes_el, "node", id=source_file, label=source_file)
            attvalues = ET.SubElement(n, "attvalues")
            ET.SubElement(attvalues, "attvalue", for_="node_type", value="source_file")

        # Add indicator node if not present (using indicator value as ID)
        ind_id = f"{ind_type}:{ind_value}"
        if ind_id not in node_set:
            node_set.add(ind_id)
            n = ET.SubElement(nodes_el, "node", id=ind_id, label=ind_value)
            attvalues = ET.SubElement(n, "attvalues")
            ET.SubElement(attvalues, "attvalue", for_="node_type", value=ind_type)

        # Create edge connecting file to indicator
        ET.SubElement(edges_el, "edge", id=str(edge_id), source=source_file, target=ind_id)
        edge_id += 1

    # Pretty print XML to GEXF file
    os.makedirs(os.path.dirname(OUTPUT_GEXF), exist_ok=True)
    rough_string = ET.tostring(gexf, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(OUTPUT_GEXF, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"\n[+] Graph export complete! GEXF file saved to {OUTPUT_GEXF}")
    print(f"    - Total Nodes (Files + Indicators): {len(node_set)}")
    print(f"    - Total Edges (Relationships): {edge_id - 1}")
    print("\n[i] You can now open this file directly in Gephi (File -> Open) to render your network graph.")

if __name__ == "__main__":
    main()
