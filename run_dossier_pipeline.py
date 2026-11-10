import sqlite3
import subprocess
import json
import re

DB_PATH = "pesci_intelligence.db"

def update_descriptions():
    print("[*] Fetching missing descriptions from YouTube stream archives...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Extract channel feed JSON metadata safely
    cmd = ["yt-dlp", "--flat-playlist", "--dump-json", "https://www.youtube.com/@SirJosephPesci/streams"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    updated = 0
    for line in proc.stdout:
        try:
            data = json.loads(line)
            vid = data.get("id")
            title = data.get("title", "")
            # Fallback to title string if description payload is omitted by endpoint
            desc = data.get("description") or title
            
            if vid:
                cursor.execute(
                    "UPDATE stream_archives SET description = ? WHERE video_id = ?",
                    (desc, vid)
                )
                updated += cursor.rowcount
        except Exception:
            continue
            
    conn.commit()
    conn.close()
    print(f"[+] Synced descriptions for {updated} records.")

def build_prompt_dataset():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT video_id, upload_date, title 
        FROM stream_archives 
        WHERE title LIKE '%Beyond%' 
        ORDER BY rowid ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    markdown_table = "| Video_ID | Upload_Date | Title |\n|---|---|---|\n"
    for r in rows:
        v_id, u_date, title = r
        markdown_table += f"| {v_id} | {u_date or 'N/A'} | {title} |\n"
    return markdown_table

def run_inference():
    dataset = build_prompt_dataset()
    prompt = f"""<|im_start|>system
You are an OSINT intelligence analyst. Analyze the provided video catalog dataset and output a structured report in valid Markdown.
Include:
1. Primary Drama Arcs (categorized by titles)
2. Tagged Entities (creators, guests, co-hosts mentioned in titles)
3. Numbering Anomalies (.5 episodes, formatting inconsistencies)
<|im_end|>
<|im_start|>user
DATASET:
{dataset}
<|im_end|>
<|im_start|>assistant
"""
    
    print("[*] Launching local llama-cli inference...")
    cmd = [
        "/home/skull/llama.cpp/build/bin/llama-cli",
        "-m", "/home/skull/llama.cpp/models/qwen2.5-coder-1.5b-q4_k_m.gguf",
        "--temp", "0.1",
        "-n", "768",
        "-p", prompt
    ]
    
    with open("final_intelligence_dossier.md", "w") as outfile:
        subprocess.run(cmd, stdout=outfile, stderr=subprocess.DEVNULL)
    
    print("[+] Dossier generated: final_intelligence_dossier.md")

if __name__ == "__main__":
    update_descriptions()
    run_inference()
