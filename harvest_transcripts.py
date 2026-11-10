import sqlite3
import subprocess
import json
import os

DB_PATH = "pesci_intelligence.db"

def update_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE stream_archives ADD COLUMN transcript TEXT;")
        conn.commit()
        print("[+] Added 'transcript' column to stream_archives schema.")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.close()

def harvest_subtitles():
    update_schema()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT video_id FROM stream_archives WHERE transcript IS NULL OR transcript = '';")
    vids = [r[0] for r in cursor.fetchall()]
    
    print(f"[*] Attempting subtitle extraction for {len(vids)} streams...")
    
    for idx, vid in enumerate(vids, 1):
        print(f"[{idx}/{len(vids)}] Processing video: {vid}")
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "--output", f"temp_{vid}",
            f"https://www.youtube.com/watch?v={vid}"
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check for generated VTT file
        vtt_file = f"temp_{vid}.en.vtt"
        if os.path.exists(vtt_file):
            with open(vtt_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            
            # Clean VTT header and timestamp lines
            clean_lines = [
                line.strip() for line in lines 
                if not line.startswith("WEBVTT") 
                and "-->" not in line 
                and line.strip() 
                and not line.strip().isdigit()
            ]
            transcript_text = " ".join(clean_lines)
            
            cursor.execute(
                "UPDATE stream_archives SET transcript = ? WHERE video_id = ?;", 
                (transcript_text, vid)
            )
            conn.commit()
            print(f"  [+] Saved transcript ({len(transcript_text)} chars)")
            os.remove(vtt_file)
        else:
            print("  [!] No subtitles available for this stream.")
            
    conn.close()
    print("[+] Transcript harvest pipeline complete.")

if __name__ == "__main__":
    harvest_subtitles()
