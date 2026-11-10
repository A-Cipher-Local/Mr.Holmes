import json
import os
from datetime import datetime

REPORTS_DIR = "GUI/Reports"
OUTPUT_DOSSIER = "GUI/Reports/master_intelligence_dossier.md"

def load_json(filename):
    path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    print("[*] Compiling analytical reports into a master OSINT dossier...")

    scorecard = load_json("entity_pivot_scorecard.json")
    network = load_json("network_similarity_matrix.json")
    domains = load_json("domain_root_pivot_report.json")

    dossier = []
    
    dossier.append("# Master Intelligence Investigation Dossier")
    dossier.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    dossier.append("**Database:** osint_intelligence.db\n")
    
    dossier.append("---")
    dossier.append("## 1. Executive Summary & Top Centrality Nodes")
    if scorecard:
        dossier.append(f"Total Evaluated Indicators: **{len(scorecard)}**\n")
        dossier.append("| Type | Indicator Value | File Spread | Weight Score |")
        dossier.append("|---|---|---|---|")
        for item in scorecard[:5]:
            dossier.append(f"| `{item['indicator_type']}` | `{item['indicator_value']}` | {item['file_appearance_count']} files | {item['calculated_weight']} |")
    else:
        dossier.append("_No scorecard data found._")

    dossier.append("\n---")
    dossier.append("## 2. Infrastructure Domain Pivots")
    if domains:
        dossier.append(f"Identified shared infrastructure root domains: **{len(domains)}**\n")
        for dom in domains:
            dossier.append(f"- **{dom['root_domain']}** (Shared across {dom['file_count']} files)")
    else:
        dossier.append("_No shared domains identified._")

    dossier.append("\n---")
    dossier.append("## 3. Network Similarity Overlaps")
    if network:
        dossier.append(f"Total pairwise file connections analyzed: **{len(network)}**\n")
        for link in network[:5]:
            dossier.append(f"- `{link['file_a']}` <---> `{link['file_b']}` (Similarity: `{link['jaccard_similarity']}` | Shared: {link['shared_count']})")
    else:
        dossier.append("_No network similarity links recorded._")

    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_content = "\n".join(dossier)
    
    with open(OUTPUT_DOSSIER, "w", encoding="utf-8") as out:
        out.write(report_content)

    print(f"[+] Master dossier compiled successfully and saved to {OUTPUT_DOSSIER}")

if __name__ == "__main__":
    main()
