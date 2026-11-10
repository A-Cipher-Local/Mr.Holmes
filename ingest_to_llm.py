import os
import json
import glob

INPUT_DIR = "GUI/Reports/github_extractions"
OUTPUT_FILE = "GUI/Reports/llm_ingest_corpus.json"

def main():
    print(f"[*] Scanning {INPUT_DIR} for extracted artifacts...")
    corpus = []
    
    files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))
    if not files:
        print("    [-] No extracted artifact files found to ingest.")
        return

    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"    [+] Ingesting: {filename}")
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            corpus.append({
                "source_file": filename,
                "content_length": len(content),
                "data": content
            })
        except Exception as e:
            print(f"    [-] Failed to read {filename}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(corpus, out, indent=2, ensure_ascii=False)
        
    print(f"\n[+] Successfully compiled {len(corpus)} records into LLM ingestion corpus: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
