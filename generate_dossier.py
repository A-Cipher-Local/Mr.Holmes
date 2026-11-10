import sqlite3
import subprocess
import os

DB_PATH = "pesci_intelligence.db"
MODEL_PATH = "/home/skull/llama.cpp/models/qwen2.5-coder-1.5b-q4_k_m.gguf"
LLAMA_CLI = "/home/skull/llama.cpp/build/bin/llama-cli"

def run():
    if not os.path.exists(DB_PATH):
        print(f"[-] Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Extract catalog rows
    cursor.execute("SELECT video_id, upload_date, title FROM stream_archives WHERE title LIKE '%Beyond%' ORDER BY rowid ASC;")
    records = cursor.fetchall()
    conn.close()

    # Build Markdown table cleanly
    table_lines = ["| Video_ID | Date | Title |", "|---|---|---|"]
    for v_id, u_date, title in records:
        date_str = u_date if u_date else "N/A"
        table_lines.append(f"| {v_id} | {date_str} | {title} |")
    dataset = "\n".join(table_lines)

    # Construct prompt with strict structural formatting instructions
    prompt = f"""<|im_start|>system
You are an OSINT content analyst. Analyze the provided video catalog dataset and output a concise Markdown report containing:
1. Primary Drama Arcs
2. Tagged Personalities & Co-hosts
3. Episode Numbering Anomalies
Keep your points brief and do not repeat entries.
<|im_end|>
<|im_start|>user
DATASET:
{dataset}
<|im_end|>
<|im_start|>assistant
"""

    print("[*] Running local LLM inference with repetition penalties...")
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "--temp", "0.2",
        "--repeat-penalty", "1.18",
        "-n", "400",
        "-p", prompt
    ]

    with open("final_intelligence_dossier.md", "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL)

    print("[+] Dossier successfully generated: final_intelligence_dossier.md")

if __name__ == "__main__":
    run()
