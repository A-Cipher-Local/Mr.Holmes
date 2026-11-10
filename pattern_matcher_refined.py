import json
import re
import os

CORPUS_FILE = "GUI/Reports/llm_ingest_corpus.json"
OUTPUT_REPORT = "GUI/Reports/pattern_match_refined.json"

# Exclude programming decorators/keywords
IGNORED_HANDLES = {"@staticmethod", "@ECHO", "@gmail", "@set", "@echo", "@if", "@for"}

PATTERNS = {
    "emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "ipv4": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
    "urls": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w ./?%&=-]*",
    "handles": r"@[a-zA-Z0-9_]{3,30}"
}

def main():
    if not os.path.exists(CORPUS_FILE):
        print(f"[-] Corpus file {CORPUS_FILE} not found.")
        return

    print(f"[*] Loading corpus for refined pattern extraction...")
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    findings = {}

    for item in corpus:
        source = item["source_file"]
        text = item["data"]
        
        file_matches = {}
        for key, pattern in PATTERNS.items():
            matches = list(set(re.findall(pattern, text)))
            if key == "handles":
                matches = [h for h in matches if h not in IGNORED_HANDLES]
            if matches:
                file_matches[key] = matches
                
        if file_matches:
            findings[source] = file_matches

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as out:
        json.dump(findings, out, indent=2, ensure_ascii=False)

    print(f"[+] Refined pattern matching complete. Saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
