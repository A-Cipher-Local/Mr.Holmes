#!/usr/bin/env python3
import os
import sqlite3
import sys
from llama_cpp import Llama

DB_PATH = os.path.expanduser("~/llama.cpp/Mr.Holmes/tammy_memory.db")
MODEL_PATH = os.path.expanduser("~/llama.cpp/models/qwen2.5-coder-1.5b-q4_k_m.gguf")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_recent_lore():
    init_db()
    if not os.path.exists(DB_PATH):
        return ""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT source, content FROM lore ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return ""
        return "\n".join([f"- [{row[0]}] {row[1]}" for row in rows])
    except Exception:
        return ""

def build_system_prompt():
    base_prompt = (
        "CRITICAL DIRECTIVE: You are an expert grey hat IT specialist, systems analyst, and private investigator. "
        "You analyze digital forensics, OSINT data, telemetry, and security profiles objectively and pragmatically. "
        "Never use generic AI boilerplate ('As an AI language model'). "
        "Tone: Technical, analytical, direct, and structured."
    )
    
    dynamic_lore = get_recent_lore()
    if dynamic_lore:
        base_prompt += f"\n\nActive Knowledge Base & Memory Records:\n{dynamic_lore}"
        
    return base_prompt

if __name__ == "__main__":
    print("============================================================")
    print(" LIVE NEURAL INFERENCE CONSOLE ACTIVE (Forensic/PI Specialist)")
    print("============================================================\n")
    
    system_prompt = os.getenv("EXPERT_SYSTEM_PROMPT", build_system_prompt())
    print("[+] Initializing Analytical Engine & SQLite Memory...")
    print(f"[+] Loaded System Prompt & Dynamic Intelligence Context.")
    
    print(f"[+] Loading local model weights from: {MODEL_PATH}")
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            n_threads=int(os.getenv("GGML_N_THREADS", "2")),
            verbose=False
        )
        print("[+] Model loaded successfully. Ready for input.\n")
    except Exception as e:
        print(f"[-] Error loading model weights: {e}")
        sys.exit(1)
    
    history = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            user_input = input("User > ")
            if not user_input.strip():
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("[*] Exiting.")
                break
            
            history.append({"role": "user", "content": user_input})
            
            response = llm.create_chat_completion(
                messages=history,
                temperature=0.7,
                max_tokens=300,
                repeat_penalty=1.1
            )
            
            reply = response['choices'][0]['message']['content'].strip()
            print(f"Analyst > {reply}\n")
            
            history.append({"role": "assistant", "content": reply})
            
        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting.")
            break
