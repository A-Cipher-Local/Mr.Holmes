#!/usr/bin/env python3
# ==============================================================================
# Deep Behavioral & Cultural Context Telemetry Extractor
# ==============================================================================

import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter

TIMELINE_PATH = "GUI/Reports/universal_chronological_timeline.json"
OUTPUT_GEXF = "GUI/Reports/tammy_trait_network.gexf"
OUTPUT_JSON = "GUI/Reports/tammy_profile_schema.json"
CENTRAL_HUB = "tammybusagi"

# Cultural / Commentary ecosystem keywords to track as behavioral sub-nodes
CULTURAL_VECTORS = ["lolcow", "stream", "drama", "podcast", "live", "keem", "commentary", "video", "content"]

def extract_deep_profile(events):
    heuristics = Counter()
    vocab_counter = Counter()
    cultural_hits = Counter()
    
    total_words = 0
    total_events = len(events)

    for ev in events:
        text = str(ev.get("context", ev.get("content", "")))
        text_lower = text.lower()
        
        # 1. Punctuation & Structural Tone
        if "!" in text:
            heuristics["exclamation_intensity"] += text.count("!")
        if "?" in text:
            heuristics["interrogative_probing"] += text.count("?")
        if "..." in text or "…" in text:
            heuristics["hesitation_ellipsis"] += 1

        # 2. Capitalization / Intensity
        words = text.split()
        total_words += len(words)
        caps = [w for w in words if w.isupper() and len(w) > 1]
        if caps:
            heuristics["caps_emphasis"] += len(caps)

        # 3. Cultural & Commentary Ecosystem Mapping
        for vector in CULTURAL_VECTORS:
            if vector in text_lower:
                cultural_hits[vector] += text_lower.count(vector)

        # 4. General Tokenization (excluding noise)
        tokens = re.findall(r'\b[a-z]{4,}\b', text_lower)
        for token in tokens:
            if token not in ["https", "http", "tco", "tammybusagi", "twitter", "retweet"]:
                vocab_counter[token] += 1

    avg_words = round(total_words / max(total_events, 1), 2)
    top_vocab = [w for w, _ in vocab_counter.most_common(8)]
    
    return heuristics, avg_words, top_vocab, cultural_hits

def main():
    if not os.path.exists(TIMELINE_PATH):
        print(f"[-] Error: {TIMELINE_PATH} not found.")
        return

    print(f"[*] Extracting deep psychological and cultural vectors from {TIMELINE_PATH}...")
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    heuristics, avg_words, top_vocab, cultural_hits = extract_deep_profile(events)

    schema = {
        "subject": CENTRAL_HUB,
        "metrics": {
            "total_events": len(events),
            "avg_words_per_event": avg_words
        },
        "behavioral_heuristics": dict(heuristics),
        "cultural_ecosystem_alignment": dict(cultural_hits),
        "dominant_vocabulary": top_vocab
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)

    # Build GEXF Multi-Tier Radial Graph
    gexf = ET.Element("gexf", xmlns="http://www.gexf.net/1.2draft", version="1.2")
    graph = ET.SubElement(gexf, "graph", defaultedgetype="directed", mode="static")
    nodes_elem = ET.SubElement(graph, "nodes")
    edges_elem = ET.SubElement(graph, "edges")

    # Central Hub
    ET.SubElement(nodes_elem, "node", id=CENTRAL_HUB, label=f"@{CENTRAL_HUB} (Core Target)")

    categories = {
        "cat_rhetorical": "RHETORICAL STYLE",
        "cat_cultural": "CULTURAL & STREAM ECOSYSTEM",
        "cat_lexical": "DOMINANT LEXICON"
    }

    edge_id = 0
    for cat_id, cat_label in categories.items():
        ET.SubElement(nodes_elem, "node", id=cat_id, label=cat_label)
        edge_id += 1
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source=cat_id, target=CENTRAL_HUB, weight="10")

    # Connect Rhetorical Traits
    for k, v in heuristics.items():
        node_id = f"heur_{k}"
        ET.SubElement(nodes_elem, "node", id=node_id, label=f"{k} ({v})")
        edge_id += 1
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source=node_id, target="cat_rhetorical", weight=str(v))

    # Connect Cultural Vectors (Lolcow / Stream / Commentary)
    for k, v in cultural_hits.items():
        node_id = f"cult_{k}"
        ET.SubElement(nodes_elem, "node", id=node_id, label=f"ecosystem: {k} ({v})")
        edge_id += 1
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source=node_id, target="cat_cultural", weight=str(max(v * 2, 2)))

    # Connect Lexical Tokens
    for word in top_vocab:
        node_id = f"lex_{word}"
        ET.SubElement(nodes_elem, "node", id=node_id, label=f"token: {word}")
        edge_id += 1
        ET.SubElement(edges_elem, "edge", id=str(edge_id), source=node_id, target="cat_lexical", weight="3")

    raw_str = ET.tostring(gexf, encoding="utf-8")
    pretty_xml = minidom.parseString(raw_str).toprettyxml(indent="  ")

    with open(OUTPUT_GEXF, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"[+] Advanced Profile Schema saved to {OUTPUT_JSON}")
    print(f"[+] Multi-Tier Radial Network exported to {OUTPUT_GEXF}\n")
    
    print("--- DEEP TELEMETRY SUMMARY ---")
    for k, v in heuristics.items():
        print(f"  - {k:<25}: {v}")
    print(f"  - Cultural Vectors Hit         : {dict(cultural_hits)}")
    print(f"  - Top Lexical Tokens           : {', '.join(top_vocab)}")

if __name__ == "__main__":
    main()
