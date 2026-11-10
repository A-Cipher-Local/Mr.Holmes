#!/usr/bin/env python3
import urllib.request
import re

# Regex patterns for sensitive indicators
PATTERNS = {
    "Discord Webhook": r"https://discord\.com/api/webhooks/\d+/[A-Za-z0-9_-]+",
    "IP Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "API Key / Token": r"(['\"])[A-Za-z0-9_-]{32,}(['\"])",
    "Lua Event Handler": r"RegisterNetEvent\s*\(\s*(['\"])(.*?)\1\s*\)"
}

def fetch_file_content(repo, filepath):
    url = f"https://raw.githubusercontent.com/{repo}/main/{filepath}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except:
        # Fallback to master
        url_master = f"https://raw.githubusercontent.com/{repo}/master/{filepath}"
        try:
            req = urllib.request.Request(url_master, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")
        except:
            return None

def scan_code():
    print("[*] Starting Regex Intelligence Scan...")
    repo = "HappyPunch/hp-reports"
    files_to_check = ["fxmanifest.lua", "sv_config.lua", "source/server.lua", "source/client.lua"]
    
    for filepath in files_to_check:
        content = fetch_file_content(repo, filepath)
        if not content:
            continue
            
        print(f"\n[+] Analyzing file: {filepath}")
        for label, pattern in PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                print(f"    [MATCH FOUND] {label}:")
                for m in matches:
                    print(f"      -> {m}")

if __name__ == "__main__":
    scan_code()
