import os
import json
import re

TARGETS = {
    "handles": ["DemonSmooch", "TammyBUsagi"],
    "channels": ["Hannaki"],
    "locations": ["Montreal", "Canada"],
    "domains": ["stlawrenceparish"]
}

def main():
    print("[*] Starting local workspace and external cross-reference sweep...")
    
    # 1. Local Deep Probe
    email_pat = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    findings = {}
    
    excluded = {".git", "Core", "GUI"}
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in excluded]
        for file in files:
            if file.endswith((".txt", ".json", ".log", ".md", ".csv")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        hits = []
                        for idx, line in enumerate(f):
                            l_low = line.lower()
                            matched = [t for t in TARGETS["handles"] + TARGETS["channels"] + TARGETS["locations"] + TARGETS["domains"] if t.lower() in l_low]
                            emails = email_pat.findall(line)
                            if matched or emails:
                                hits.append({
                                    "line": idx + 1,
                                    "content": line.strip(),
                                    "matches": matched,
                                    "emails": emails
                                })
                        if hits:
                            findings[path] = hits
                except Exception:
                    pass

    print(f"[+] Local deep probe found contextual hits in {len(findings)} files.")

    # 2. External Dork Generation
    queries = []
    for h in TARGETS["handles"]:
        for loc in TARGETS["locations"]:
            queries.append(f"https://www.google.com/search?q=intext:(\"{h}\")+intext:(\"{loc}\")")
            queries.append(f"https://yandex.com/search/?text=(\"{h}\")%2B(\"{loc}\")")
        for d in TARGETS["domains"]:
            queries.append(f"https://www.google.com/search?q=site:{d}+\"{h}\"")

    for c in TARGETS["channels"]:
        for h in TARGETS["handles"]:
            queries.append(f"https://www.google.com/search?q=intext:(\"{c}\")+intext:(\"{h}\")+intext:(\"Montreal\")")

    for d in TARGETS["domains"]:
        queries.append(f"https://www.google.com/search?q=site:{d}+filetype:txt")
        queries.append(f"https://yandex.com/search/?text=site:{d}+mime:txt")

    os.makedirs("GUI/Reports", exist_ok=True)
    out_path = "GUI/Reports/deep_probe_report.json"
    
    report = {
        "local_deep_hits": findings,
        "cross_reference_dorks": queries
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Generated {len(queries)} cross-reference vectors.")
    print(f"[+] Comprehensive report successfully written to {out_path}")

if __name__ == "__main__":
    main()
